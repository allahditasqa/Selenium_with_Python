"""Module-wise HTML + CSV test reports with a screenshot for every executed test case.

Layout (same as the Selenium_with_DotNet reference repo):

    reports/index.html                                             history of all runs, newest first
    reports/history.json                                           machine readable history (append only)
    reports/<module-slug>/<Module> test <DD-MM-YYYY>_<HH-mm-ss>.html
    reports/<module-slug>/<Module> test cases <DD-MM-YYYY>_<HH-mm-ss>.csv

How it works (also with pytest-xdist):
  * in the worker, after each test, a screenshot is taken and attached to the report as a user property
  * in the controller process every finished test is collected
  * at the end of the session the written test case (docs/test-cases/*.csv, found by test case ID)
    is merged with the result and the module reports, the run CSV, history.json and index.html are written
Old reports are never overwritten or deleted: a name that already exists gets a " (2)" suffix.
"""

from __future__ import annotations

import base64
import csv
import html
import json
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import pytest

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"
CASES_DIR = ROOT / "docs" / "test-cases"

# test file stem -> module name shown in the report (must be the title used in docs/test-cases/<slug>.md)
MODULE_TITLES = {
    "test_01_home_page": "Home Page",
    "test_02_data_entry_form": "Data Entry Form",
    "test_03_upload_files": "Upload Files",
    "test_04_tables": "Tables",
    "test_05_widgets": "Widgets",
    "test_06_alerts_and_windows": "Alerts And Windows",
    "test_07_links_sections_shadow": "Links, Sections And Shadow DOM",
    "test_08_hidden_elements_ajax": "Hidden Elements And AJAX",
    "test_09_downloads": "Downloads",
}

CSV_COLUMNS = [
    "Test Case ID",
    "Module",
    "Test Case Title",
    "Priority",
    "Test Type",
    "Preconditions",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Actual Result",
    "Execution Status",
    "Execution Type",
    "Automation Method",
    "Duration (s)",
    "Executed On",
    "Browser",
    "Environment (URL)",
]

_NAME_ID = re.compile(r"^test_tc_([a-z0-9]+)_(\d+)_")
_DOC_ID = re.compile(r"^(TC_[A-Z0-9]+_\d+) - (.+)$")

_records: list[dict] = []
_run = {"start": None, "clock": None}


# ----------------------------------------------------------------------------- helpers
def _prettify(name: str) -> str:
    name = re.sub(r"^test_?", "", name)
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name).replace("_", " ").strip()
    return name[:1].upper() + name[1:]


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _module_title(stem: str) -> str:
    return MODULE_TITLES.get(stem, _prettify(re.sub(r"^test_\d+_", "test_", stem)))


def _is_worker(config: pytest.Config) -> bool:
    return hasattr(config, "workerinput")


def _id_sort_key(case_id: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", case_id))


def _unique_path(folder: Path, base: str, ext: str) -> Path:
    path = folder / f"{base}{ext}"
    counter = 2
    while path.exists():
        path = folder / f"{base} ({counter}){ext}"
        counter += 1
    return path


def _take_screenshot(browser) -> tuple[bytes, str] | None:
    """JPEG through the Chrome DevTools protocol (about 5x smaller than PNG); PNG for other browsers."""
    try:
        result = browser.execute_cdp_cmd("Page.captureScreenshot", {"format": "jpeg", "quality": 55})
        return base64.b64decode(result["data"]), "image/jpeg"
    except Exception:
        pass
    try:
        return browser.get_screenshot_as_png(), "image/png"
    except Exception:
        return None


def _written_cases() -> dict[str, dict[str, str]]:
    """The written test cases (master CSV files in docs/test-cases), by test case ID."""
    cases: dict[str, dict[str, str]] = {}
    for path in sorted(CASES_DIR.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                cases[row["ID"]] = row
    return cases


def _identify(item: pytest.Item) -> tuple[str, str]:
    """(test case ID, title) of a test: the id and title come from the docstring `TC_X_NN - title`."""
    function = getattr(item, "function", None)
    doc = (function.__doc__ or "").strip().splitlines()[0] if function and function.__doc__ else ""
    match = _DOC_ID.match(doc)
    callspec = getattr(item, "callspec", None)
    if match:
        base, title = match.groups()
        if callspec is not None:
            return callspec.id, title.format(**callspec.params)
        return base, title
    name = _NAME_ID.match(getattr(item, "originalname", item.name))
    case_id = f"TC_{name.group(1).upper()}_{name.group(2)}" if name else item.name
    return case_id, doc or _prettify(getattr(item, "originalname", item.name))


# ----------------------------------------------------------------------------- worker side
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    finished_test = report.when == "call"
    broken_setup = report.when == "setup" and not report.passed
    if not (finished_test or broken_setup):
        return

    case_id, title = _identify(item)
    group = item.cls.__name__ if item.cls else ""
    method = ((group + "::") if group else "") + getattr(item, "originalname", item.name)
    report.user_properties.extend(
        [
            ("module", item.path.stem),
            ("tc_id", case_id),
            ("title", title),
            ("file", item.path.relative_to(ROOT).as_posix()),
            ("method", method),
        ]
    )

    browser = getattr(item, "driver", None)
    if browser is None:
        return
    shot = _take_screenshot(browser)
    if shot is None:  # browser already closed or crashed
        return
    data, mime = shot
    report.user_properties.append(("screenshot", base64.b64encode(data).decode("ascii")))
    report.user_properties.append(("screenshot_mime", mime))
    if not report.passed:
        shots = REPORT_DIR / "screenshots"
        shots.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.name)
        (shots / f"{safe}.{'jpg' if mime == 'image/jpeg' else 'png'}").write_bytes(data)


# ----------------------------------------------------------------------------- controller side
def pytest_sessionstart(session: pytest.Session) -> None:
    _run["start"] = datetime.now()
    _run["clock"] = time.perf_counter()


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if report.outcome == "rerun":
        return
    is_call = report.when == "call"
    is_setup_problem = report.when == "setup" and report.outcome in ("failed", "skipped")
    if not (is_call or is_setup_problem):
        return
    props = dict(report.user_properties)
    stem = props.get("module")
    if stem is None:  # skipped before makereport could tag it
        stem = report.nodeid.split("::")[0].split("/")[-1].removesuffix(".py")
    error = ""
    if report.failed:
        text = report.longreprtext
        lines = [ln for ln in text.splitlines() if ln.startswith("E ")]
        error = "\n".join(lines[:15]) or text[-1500:]
    elif report.skipped and isinstance(report.longrepr, tuple):
        error = str(report.longrepr[2])
    leaf = report.nodeid.split("::")[-1]
    _records.append(
        {
            "stem": stem,
            "tc_id": props.get("tc_id", leaf),
            "title": props.get("title") or _prettify(leaf),
            "file": props.get("file", stem + ".py"),
            "method": props.get("method", leaf),
            "outcome": report.outcome,
            "duration": report.duration,
            "error": error,
            "screenshot": props.get("screenshot"),
            "mime": props.get("screenshot_mime", "image/png"),
        }
    )


def pytest_sessionfinish(session: pytest.Session) -> None:
    if _is_worker(session.config) or not _records:
        return
    config = session.config
    started: datetime = _run["start"] or datetime.now()
    run_seconds = time.perf_counter() - _run["clock"] if _run["clock"] else 0.0
    stamp = started.strftime("%d-%m-%Y_%H-%M-%S")
    try:
        cfg = config.pluginmanager.get_plugin("conftest")
        settings = cfg.settings if cfg is not None else None
    except Exception:
        settings = None
    browser = (config.getoption("--browser", default=None) or getattr(settings, "browser", "chrome")).lower()
    base_url = (config.getoption("--base-url", default=None) or getattr(settings, "base_url", "")).rstrip("/")
    written = _written_cases()

    by_module: dict[str, list[dict]] = {}
    for record in _records:
        by_module.setdefault(record["stem"], []).append(record)

    modules: list[dict] = []
    for stem, records in sorted(by_module.items()):
        records.sort(key=lambda r: _id_sort_key(r["tc_id"]))
        title = _module_title(stem)
        folder = REPORT_DIR / _slug(title)
        folder.mkdir(parents=True, exist_ok=True)
        html_path = _unique_path(folder, f"{title} test {stamp}", ".html")
        csv_path = _unique_path(folder, f"{title} test cases {stamp}", ".csv")
        for r in records:
            r["spec"] = written.get(r["tc_id"])
        html_path.write_text(_module_html(title, records, started), encoding="utf-8")
        _write_csv(csv_path, title, records, started, browser, base_url)
        counts = _counts(records)
        modules.append(
            {
                "Module": title,
                "ReportPath": f"{folder.name}/{html_path.name}",
                "CsvPath": f"{folder.name}/{csv_path.name}",
                "Total": counts["total"],
                "Passed": counts["passed"],
                "Failed": counts["failed"],
                "Skipped": counts["skipped"],
                "DurationSeconds": round(sum(r["duration"] for r in records), 3),
            }
        )

    run = {
        "RunId": started.strftime("%Y%m%d-%H%M%S"),
        "StartedAt": started.isoformat(timespec="seconds"),
        "DurationSeconds": round(run_seconds, 3),
        "Modules": modules,
    }
    _append_history_and_index(run)
    reporter = config.pluginmanager.get_plugin("terminalreporter")
    if reporter:
        reporter.write_line(f"HTML reports: {REPORT_DIR / 'index.html'}")


# ----------------------------------------------------------------------------- rendering
def _counts(records: list[dict]) -> dict[str, int]:
    return {
        "total": len(records),
        "passed": sum(r["outcome"] == "passed" for r in records),
        "failed": sum(r["outcome"] == "failed" for r in records),
        "skipped": sum(r["outcome"] == "skipped" for r in records),
    }


_CSS = """
:root{--bg:#f6f7f9;--fg:#1c1f24;--card:#fff;--line:#dde1e6;--pass:#1a7f37;--fail:#cf222e;--skip:#8a6d00;--mute:#6b7380}
@media(prefers-color-scheme:dark){:root{--bg:#14161a;--fg:#e6e8eb;--card:#1d2026;--line:#2e333b;--pass:#3fb950;--fail:#ff7b72;--skip:#d4a72c;--mute:#9aa3b0}}
body{margin:0;padding:24px 16px;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}
main{max-width:1100px;margin:auto}h1{margin:0 0 4px}h2{margin:28px 0 8px}.meta{color:var(--mute);font-size:13px}a{color:inherit}
.sum{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}.sum div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 16px}
.sum b{font-size:22px;display:block}.card{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:8px;padding:12px 16px;margin:12px 0}
.card.passed{border-left-color:var(--pass)}.card.failed{border-left-color:var(--fail)}.card.skipped{border-left-color:var(--skip)}
.head{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}.badge{font-size:12px;text-transform:uppercase;padding:2px 8px;border-radius:99px;border:1px solid currentColor}
.badge.passed{color:var(--pass)}.badge.failed{color:var(--fail)}.badge.skipped{color:var(--skip)}
pre{background:var(--bg);padding:10px;border-radius:6px;overflow:auto;white-space:pre-wrap;color:var(--fail)}
.shots{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px}figure{margin:0}img{max-width:300px;border:1px solid var(--line);border-radius:6px;cursor:zoom-in}
img.big{max-width:100%;cursor:zoom-out}figcaption{font-size:12px;color:var(--mute)}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line)}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line)}
.passed-t{color:var(--pass)}.failed-t{color:var(--fail)}.skipped-t{color:var(--skip)}
"""


def _page(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)}</title><style>{_CSS}</style></head>"
        f"<body><main>{body}</main></body></html>"
    )


def _summary_html(c: dict[str, int]) -> str:
    return (
        '<div class="sum">'
        f"<div><b>{c['total']}</b>total</div>"
        f'<div><b class="passed-t">{c["passed"]}</b>passed</div>'
        f'<div><b class="failed-t">{c["failed"]}</b>failed</div>'
        f'<div><b class="skipped-t">{c["skipped"]}</b>skipped</div>'
        "</div>"
    )


def _details_html(spec: dict[str, str]) -> str:
    steps = "<br>".join(html.escape(part) for part in re.split(r"(?<=\.) (?=\d+\. )", spec["Steps"]))
    return (
        f'<div class="meta">{html.escape(spec["Priority"])} &middot; {html.escape(spec["Type"])}</div>'
        '<details><summary class="meta">Test case details</summary><table>'
        f"<tr><th>Preconditions</th><td>{html.escape(spec['Preconditions'])}</td></tr>"
        f"<tr><th>Test steps</th><td>{steps}</td></tr>"
        f"<tr><th>Test data</th><td>{html.escape(spec['Test Data'])}</td></tr>"
        f"<tr><th>Expected result</th><td>{html.escape(spec['Expected Result'])}</td></tr>"
        "</table></details>"
    )


def _module_html(title: str, records: list[dict], started: datetime) -> str:
    c = _counts(records)
    overall = "failed" if c["failed"] else "passed"
    total_time = sum(r["duration"] for r in records)
    cards = []
    for r in records:
        shot = (
            '<div class="shots"><figure><img src="data:' + r["mime"] + ";base64,"
            f'{r["screenshot"]}" alt="screenshot" onclick="this.classList.toggle(\'big\')">'
            "<figcaption>screenshot</figcaption></figure></div>"
            if r["screenshot"]
            else ""
        )
        error = f"<pre>{html.escape(r['error'])}</pre>" if r["error"] else ""
        details = _details_html(r["spec"]) if r["spec"] else ""
        cards.append(
            f'<section class="card {r["outcome"]}"><div class="head">'
            f'<span class="badge {r["outcome"]}">{r["outcome"]}</span>'
            f"<b>{html.escape(r['tc_id'])} - {html.escape(r['title'])}</b>"
            f'<span class="meta">{html.escape(r["method"])} &middot; {r["duration"]:.1f}s</span></div>'
            f"{details}{error}{shot}</section>"
        )
    body = (
        '<p class="meta"><a href="../index.html">&larr; All reports</a></p>'
        f"<h1>{html.escape(title)}</h1>"
        f'<div class="meta">Run: {started:%d-%m-%Y %H:%M} &middot; duration {total_time:.0f}s '
        f"&middot; overall: {overall} &middot; click a screenshot to enlarge</div>"
        f"{_summary_html(c)}" + "".join(cards)
    )
    return _page(f"{title} Test Report {started:%d-%m-%Y %H:%M}", body)


def _write_csv(
    path: Path, title: str, records: list[dict], started: datetime, browser: str, base_url: str
) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_ALL)
        writer.writerow(CSV_COLUMNS)
        for r in records:
            spec = r["spec"] or {}
            status = {"passed": "Pass", "failed": "Fail"}.get(r["outcome"], "Skipped")
            if r["outcome"] == "passed":
                actual = "As expected (all assertions passed)"
            elif r["outcome"] == "failed":
                actual = r["error"]
            else:
                actual = "Test was not executed: " + r["error"]
            writer.writerow(
                [
                    r["tc_id"],
                    title,
                    r["title"],
                    spec.get("Priority", ""),
                    spec.get("Type", ""),
                    spec.get("Preconditions", ""),
                    spec.get("Steps", ""),
                    spec.get("Test Data", ""),
                    spec.get("Expected Result", ""),
                    " ".join(actual.split()),
                    status,
                    "Automated",
                    f"{r['file']}::{r['method']}",
                    f"{r['duration']:.1f}",
                    started.strftime("%d-%m-%Y %H:%M:%S"),
                    browser,
                    base_url,
                ]
            )


def _append_history_and_index(run: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    history_file = REPORT_DIR / "history.json"
    history: list[dict] = []
    if history_file.exists():
        try:
            history = json.loads(history_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:  # keep the broken file as a backup instead of losing anything
            history_file.replace(_unique_path(REPORT_DIR, "history.corrupt", ".json"))
    history.append(run)
    temp = history_file.with_suffix(".json.tmp")
    temp.write_text(json.dumps(history, indent=2), encoding="utf-8")
    temp.replace(history_file)  # history is append only: all old runs are kept
    (REPORT_DIR / "index.html").write_text(_index_html(history), encoding="utf-8")


def _index_html(history: list[dict]) -> str:
    parts = [
        "<h1>Selenium Python - Test Reports</h1>",
        '<div class="meta">History: newest run on top. Under each date-time you see the module-wise reports. '
        "Old runs are never overwritten or deleted.</div>",
    ]
    for run in sorted(history, key=lambda r: r["StartedAt"], reverse=True):
        modules = run["Modules"]
        total = sum(m["Total"] for m in modules)
        passed = sum(m["Passed"] for m in modules)
        failed = sum(m["Failed"] for m in modules)
        skipped = sum(m["Skipped"] for m in modules)
        when = datetime.fromisoformat(run["StartedAt"])
        parts.append(
            f"<h2>{when:%d-%m-%Y}  &bull;  {when:%H:%M:%S} "
            f'<span class="meta">&nbsp;total {total} &middot; <span class="passed-t">{passed} pass</span> &middot; '
            f'<span class="{"failed-t" if failed else ""}">{failed} fail</span> &middot; '
            f'<span class="skipped-t">{skipped} skip</span> &middot; {run["DurationSeconds"]:.0f}s</span></h2>'
        )
        parts.append(
            "<table><thead><tr><th>Module</th><th>Total</th><th>Pass</th><th>Fail</th><th>Skip</th>"
            "<th>Result</th><th>Report</th><th>Test cases</th></tr></thead><tbody>"
        )
        for m in sorted(modules, key=lambda m: m["Module"]):
            ok = m["Failed"] == 0
            parts.append(
                f"<tr><td>{html.escape(m['Module'])}</td><td>{m['Total']}</td>"
                f'<td class="passed-t">{m["Passed"]}</td>'
                f'<td class="{"failed-t" if m["Failed"] else ""}">{m["Failed"]}</td>'
                f'<td class="skipped-t">{m["Skipped"]}</td>'
                f'<td class="{"passed-t" if ok else "failed-t"}">{"Passed" if ok else "Failed"}</td>'
                f'<td><a href="{quote(m["ReportPath"])}">HTML</a></td>'
                f'<td><a href="{quote(m["CsvPath"])}">CSV</a></td></tr>'
            )
        parts.append("</tbody></table>")
    return _page("Selenium Python - Test Reports", "".join(parts))
