"""Traceability check: the automated tests and the written test cases must match 1:1.

    python scripts/check_traceability.py

It collects the tests (no browser is started) and compares them with docs/test-cases/*.csv:
  * every automated test has a documented case with the same ID, title and test method
  * every documented case is automated by a test with that ID (no "documented but not automated" rows)
  * no ID is used twice in the code
Exit code 0 = in sync, 1 = drift (the problems are printed).
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "docs" / "test-cases"
NAME_ID = re.compile(r"^test_tc_([a-z0-9]+)_(\d+)_")
DOC_ID = re.compile(r"^(TC_[A-Z0-9]+_\d+(?:\.\d+)?) - (.+)$")


class Collector:
    def __init__(self) -> None:
        self.items: list[pytest.Item] = []

    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        self.items = list(items)


def code_cases(items: list[pytest.Item]) -> tuple[dict[str, dict], list[str]]:
    """Return ({id: {title, method, file}}, problems) for all collected tests."""
    cases: dict[str, dict] = {}
    problems: list[str] = []
    for item in items:
        function = getattr(item, "function", None)
        doc = (function.__doc__ or "").strip().splitlines()[0] if function and function.__doc__ else ""
        match = DOC_ID.match(doc)
        name_match = NAME_ID.match(item.originalname)
        if not match or not name_match:
            problems.append(f"{item.nodeid}: test name or docstring has no TC_<MODULE>_<NN> id")
            continue
        base, title = match.groups()
        if base != f"TC_{name_match.group(1).upper()}_{name_match.group(2)}":
            problems.append(f"{item.nodeid}: id in the docstring ({base}) differs from the test name")
        callspec = getattr(item, "callspec", None)
        case_id = base
        if callspec is not None:
            case_id = callspec.id
            if not case_id.startswith(base + "."):
                problems.append(f"{item.nodeid}: parameter id {case_id!r} must start with {base}.")
            title = title.format(**callspec.params)
        if case_id in cases:
            problems.append(f"{case_id}: used by more than one test ({item.nodeid})")
        method = ((item.cls.__name__ + "::") if item.cls else "") + item.originalname
        cases[case_id] = {"title": title, "method": method, "file": item.path.relative_to(ROOT).as_posix()}
    return cases, problems


def documented_cases() -> dict[str, dict]:
    docs: dict[str, dict] = {}
    for path in sorted(CASES_DIR.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                docs[row["ID"]] = {
                    "title": row["Title"],
                    "method": row["Test Method"],
                    "file": row["Test File"],
                    "doc": path.name,
                }
    return docs


def main() -> int:
    collector = Collector()
    code = pytest.main(
        ["--collect-only", "-q", "-p", "no:cacheprovider", "-o", "addopts="], plugins=[collector]
    )
    if code not in (0, 5):
        print("Collection failed")
        return 1
    in_code, problems = code_cases(collector.items)
    in_docs = documented_cases()

    for case_id in sorted(set(in_code) - set(in_docs)):
        problems.append(f"{case_id}: automated in {in_code[case_id]['method']} but NOT documented")
    for case_id in sorted(set(in_docs) - set(in_code)):
        problems.append(f"{case_id}: documented in {in_docs[case_id]['doc']} but NOT automated")
    for case_id in sorted(set(in_code) & set(in_docs)):
        code_case, doc_case = in_code[case_id], in_docs[case_id]
        if code_case["title"] != doc_case["title"]:
            problems.append(
                f"{case_id}: title differs\n    code: {code_case['title']}\n    doc : {doc_case['title']}"
            )
        if code_case["method"] != doc_case["method"] or code_case["file"] != doc_case["file"]:
            problems.append(
                f"{case_id}: automation reference differs (code {code_case['file']}::{code_case['method']}, "
                f"doc {doc_case['file']}::{doc_case['method']})"
            )

    print(f"tests in code: {len(in_code)} | cases in docs: {len(in_docs)}")
    if problems:
        print(f"TRACEABILITY FAILED: {len(problems)} problem(s)")
        for problem in problems:
            print(" -", problem)
        return 1
    print("Traceability OK: every automated test is documented and every documented case is automated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
