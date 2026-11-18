"""Build (or check) the master CSV of every test case document.

    python scripts/cases_csv.py            # write the master CSV next to every .md document
    python scripts/cases_csv.py --check    # only report if a CSV is out of date (exit code 1 if so)

The markdown documents are the source of truth. A row that did not change keeps its "Last Updated" date;
a new or changed row gets today's date. Do not edit the CSV files by hand.
"""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "docs" / "test-cases"

ESC = chr(92)  # markdown escape for a pipe inside a table cell

COLUMNS = [
    "ID",
    "Module",
    "Sub-module",
    "Title",
    "Priority",
    "Type",
    "Preconditions",
    "Test Data",
    "Steps",
    "Expected Result",
    "Automation Status",
    "Test File",
    "Test Method",
    "Last Updated",
]


@dataclass(frozen=True)
class Case:
    id: str
    module: str
    submodule: str
    title: str
    priority: str
    type: str
    preconditions: str
    test_data: str
    steps: str
    expected: str
    status: str
    test_file: str
    test_method: str

    def row(self) -> list[str]:
        return [
            self.id,
            self.module,
            self.submodule,
            self.title,
            self.priority,
            self.type,
            self.preconditions,
            self.test_data,
            self.steps,
            self.expected,
            self.status,
            self.test_file,
            self.test_method,
        ]


def _split_row(line: str) -> list[str]:
    cells = re.split("(?<!" + re.escape(ESC) + ")[|]", line.strip().strip("|"))
    return [c.strip().replace(ESC + "|", "|") for c in cells]


def parse_markdown(path: Path) -> list[Case]:
    """Read all test case rows of one document."""
    module = path.stem
    group = ""
    cases: list[Case] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"# (.+) Test Cases\s*$", line)
        if heading:
            module = heading.group(1)
        sub = re.match(r"## (?:[A-Z]\. )?(.+)$", line)
        if sub:
            group = sub.group(1)
        if not re.match(r"\| TC_[A-Z0-9]+_\d+(\.\d+)? \|", line):
            continue
        cells = _split_row(line)
        if len(cells) != 9:
            raise ValueError(f"{path.name}: expected 9 columns, found {len(cells)} in: {line[:80]}")
        cid, title, prio, typ, pre, data, steps, expected, auto = cells
        found = re.match(r"(\w[\w ]*?) `([^`]+)`$", auto)
        if not found:
            raise ValueError(f"{path.name}: bad Automation cell for {cid}: {auto}")
        status, target = found.groups()
        file, _, method = target.partition("::")
        cases.append(
            Case(
                cid,
                module,
                group,
                title,
                prio,
                typ,
                pre,
                data,
                steps.replace("<br>", " "),
                expected,
                status,
                f"tests/ui/{file}",
                method,
            )
        )
    return cases


def read_existing(path: Path) -> dict[str, tuple[list[str], str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    return {r[0]: (r[:-1], r[-1]) for r in rows[1:] if len(r) == len(COLUMNS)}


def build(md: Path, today: str) -> tuple[Path, list[list[str]], bool]:
    """Return (csv path, rows, changed?)."""
    target = md.with_suffix(".csv")
    existing = read_existing(target)
    rows: list[list[str]] = []
    for case in parse_markdown(md):
        values = case.row()
        old = existing.get(case.id)
        rows.append([*values, old[1] if old and old[0] == values else today])
    changed = [r[:-1] for r in rows] != [v[0] for v in existing.values()] or len(rows) != len(existing)
    return target, rows, changed


def main() -> int:
    check = "--check" in sys.argv
    today = date.today().strftime("%d-%m-%Y")
    stale = 0
    total = 0
    for md in sorted(CASES_DIR.glob("*.md")):
        target, rows, changed = build(md, today)
        total += len(rows)
        if check:
            if changed:
                stale += 1
                print(f"OUT OF DATE: {target.relative_to(ROOT)} (run: python scripts/cases_csv.py)")
            continue
        if changed or not target.exists():
            with target.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle, quoting=csv.QUOTE_ALL)
                writer.writerow(COLUMNS)
                writer.writerows(rows)
            print(f"written {target.relative_to(ROOT)} ({len(rows)} cases)")
        else:
            print(f"unchanged {target.relative_to(ROOT)} ({len(rows)} cases)")
    if check:
        print(f"{total} cases checked, {stale} master CSV file(s) out of date")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
