"""Module-wise HTML test reports with a screenshot for every executed test case.

For every test module (file) a report is written to
    reports/<module-slug>/<Module Title> test DD-MM-YYYY_HH-MM.html
plus a CSV of the test cases and a top-level reports/index.html that links all modules.

How it works (works with pytest-xdist too):
  * in the worker, after each test, a screenshot is taken and attached to the report as a user property
  * in the controller process every finished test is collected
  * at the end of the session the collected results are written as HTML / CSV
"""

from __future__ import annotations

import base64
import csv
import html
import re
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"

# test file stem -> title shown in the report (unknown files fall back to a prettified file name)
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

_records: list[dict] = []


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


# ----------------------------------------------------------------------------- worker side
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Give every test a stable number inside its module (before -m / -k deselection)."""
    counters: dict[str, int] = {}
    for item in items:
        stem = item.path.stem
        counters[stem] = counters.get(stem, 0) + 1
        item.user_properties.append(("tc_no", str(counters[stem])))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    finished_test = report.when == "call"
    broken_setup = report.when == "setup" and not report.passed
    if not (finished_test or broken_setup):
        return

    function = getattr(item, "function", None)
    doc = (function.__doc__ or "").strip().splitlines()[0] if function and function.__doc__ else ""
    title = doc or _prettify(item.originalname if hasattr(item, "originalname") else item.name)
    callspec = getattr(item, "callspec", None)
    if callspec is not None and not doc:
        title = f"{title} [{callspec.id}]"
    group = _prettify(item.cls.__name__.removeprefix("Test")) if item.cls else ""
    report.user_properties.extend(
        [
            ("module", item.path.stem),
            ("group", group),
            ("title", title),
            ("file", item.path.name),
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
    _records.append(
        {
            "stem": stem,
            "tc_no": int(props.get("tc_no", 0)),
            "group": props.get("group", ""),
            "title": props.get("title") or _prettify(report.nodeid.split("::")[-1]),
            "file": props.get("file", stem + ".py"),
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
    now = datetime.now()
    stamp = now.strftime("%d-%m-%Y_%H-%M")
    by_module: dict[str, list[dict]] = {}
    for record in _records:
        by_module.setdefault(record["stem"], []).append(record)

    written: list[dict] = []
    for stem, records in sorted(by_module.items()):
        records.sort(key=lambda r: r["tc_no"])
        title = _module_title(stem)
        folder = REPORT_DIR / _slug(title)
        folder.mkdir(parents=True, exist_ok=True)
        name = f"{title} test {stamp}"
        for r in records:
            r["tc_id"] = f"TC_{_slug(title).upper().replace('-', '_')}_{r['tc_no']:02d}"
        (folder / f"{name}.html").write_text(_module_html(title, records, now), encoding="utf-8")
        _write_csv(folder / f"{title} test cases {stamp}.csv", records)
        written.append({"title": title, "folder": folder.name, "file": f"{name}.html", "records": records})

    (REPORT_DIR / "index.html").write_text(_index_html(written, now), encoding="utf-8")
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
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


def _summary_html(c: dict[str, int]) -> str:
    return (
        '<div class="sum">'
        f"<div><b>{c['total']}</b>total</div>"
        f'<div><b class="passed-t">{c["passed"]}</b>passed</div>'
        f'<div><b class="failed-t">{c["failed"]}</b>failed</div>'
        f'<div><b class="skipped-t">{c["skipped"]}</b>skipped</div>'
        "</div>"
    )


def _module_html(title: str, records: list[dict], now: datetime) -> str:
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
        group = f" &middot; {html.escape(r['group'])}" if r["group"] else ""
        cards.append(
            f'<section class="card {r["outcome"]}">\n'
            f'  <div class="head"><span class="badge {r["outcome"]}">{r["outcome"]}</span>'
            f"<b>{r['tc_id']} - {html.escape(r['title'])}</b>\n"
            f'  <span class="meta">{html.escape(r["file"])}{group} &middot; {r["duration"]:.1f}s</span></div>\n'
            f"  {error}\n  {shot}\n</section>"
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)} Test Report {now:%d-%m-%Y %H:%M}</title><style>{_CSS}</style></head>"
        '<body><main>\n<p class="meta"><a href="../index.html">&larr; All reports</a></p>\n'
        f"<h1>{html.escape(title)}</h1>\n"
        f'<div class="meta">Run: {now:%d-%m-%Y %H:%M} &middot; total test time {total_time:.0f}s '
        f"&middot; overall: {overall} &middot; click a screenshot to enlarge</div>\n"
        f"{_summary_html(c)}\n" + "\n".join(cards) + "\n</main></body></html>"
    )


def _write_csv(path: Path, records: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Test case ID", "Title", "Group", "File", "Status", "Duration (s)", "Error"])
        for r in records:
            writer.writerow(
                [
                    r["tc_id"],
                    r["title"],
                    r["group"],
                    r["file"],
                    r["outcome"],
                    f"{r['duration']:.1f}",
                    r["error"],
                ]
            )


def _index_html(modules: list[dict], now: datetime) -> str:
    all_records = [r for m in modules for r in m["records"]]
    rows = []
    for m in modules:
        c = _counts(m["records"])
        link = f"{m['folder']}/{m['file']}"
        rows.append(
            f'<tr><td><a href="{html.escape(link)}">{html.escape(m["title"])}</a></td>'
            f"<td>{c['total']}</td>"
            f'<td class="passed-t">{c["passed"]}</td>'
            f'<td class="failed-t">{c["failed"]}</td>'
            f'<td class="skipped-t">{c["skipped"]}</td></tr>'
        )
    history = []
    for folder in sorted(p for p in REPORT_DIR.iterdir() if p.is_dir() and p.name != "screenshots"):
        files = sorted(folder.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if files:
            links = " &middot; ".join(
                f'<a href="{folder.name}/{html.escape(f.name)}">{html.escape(f.stem.split(" test ")[-1])}</a>'
                for f in files[:10]
            )
            history.append(f"<tr><td>{html.escape(folder.name)}</td><td>{links}</td></tr>")
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Test Reports {now:%d-%m-%Y %H:%M}</title><style>{_CSS}</style></head><body><main>"
        "<h1>Test reports</h1>"
        f'<div class="meta">Latest run: {now:%d-%m-%Y %H:%M} &middot; one report per module</div>'
        f"{_summary_html(_counts(all_records))}"
        "<h2>Modules (latest run)</h2>"
        "<table><tr><th>Module</th><th>Total</th><th>Passed</th><th>Failed</th><th>Skipped</th></tr>"
        + "".join(rows)
        + "</table><h2>Previous runs</h2><table><tr><th>Module folder</th><th>Reports (newest first)</th></tr>"
        + "".join(history)
        + "</table></main></body></html>"
    )
