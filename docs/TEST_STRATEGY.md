# Test Strategy: Practice Site UI Automation (Selenium 4 + Python + Pytest)

**Version:** 1.0  |  **Prepared by:** QA (SDET)

## 1. Objective
Give a complete, repeatable and readable UI automation suite for every control type that a real web application uses
(forms, dropdowns, date pickers, tables, alerts, windows, Shadow DOM, downloads, AJAX). The suite is the reference
for the Page Object Model and the reporting approach of this QA portfolio.

## 2. Application under test

| Application | URL | Purpose |
| --- | --- | --- |
| Test Automation Practice | https://testautomationpractice.blogspot.com/ | Public practice site, main page + "Hidden Elements & AJAX" + "Download Files" pages |

## 3. Scope

| Module | Test file | Cases | Type |
| --- | --- | --- | --- |
| Home Page | `test_01_home_page.py` | 21 | Smoke, UI |
| Data Entry Form | `test_02_data_entry_form.py` | 36 | Functional, Boundary, Negative, End to end |
| Upload Files | `test_03_upload_files.py` | 3 | Functional, Negative |
| Tables | `test_04_tables.py` | 23 | UI, Validation |
| Widgets | `test_05_widgets.py` | 22 | Functional, UI |
| Alerts And Windows | `test_06_alerts_and_windows.py` | 12 | Functional |
| Links, Sections And Shadow DOM | `test_07_links_sections_shadow.py` | 26 | Functional, UI, Negative |
| Hidden Elements And AJAX | `test_08_hidden_elements_ajax.py` | 6 | Functional, UI |
| Downloads | `test_09_downloads.py` | 3 | Functional |
| **Total** | | **152** | |

**Out of scope:** load and performance testing, visual regression, accessibility audit, security testing of the
third-party hosting platform, mobile browsers.

## 4. Approach

| Type | How | Automated |
| --- | --- | --- |
| Smoke | Page loads, every section is present | Yes (`-m smoke`) |
| Functional (positive) | Every control is used the way a user uses it | Yes |
| Negative and validation | Empty date range, reversed range, single click instead of double click, upload without file | Yes |
| Boundary | Field length limits (15 / 25 / 10 characters), same start and end date | Yes |
| Data driven | One test, many data sets (`pytest.mark.parametrize`), one report row per data set | Yes |
| External dependency | New windows, Wikipedia widget, broken links, visitors counter (marker `external`) | Yes, skipped in CI |
| Cross-browser | Chrome (default), Firefox, Edge or a remote Selenium Grid (`--browser`) | On demand |
| Exploratory, usability, accessibility | By hand before a release | No |

Design rules: Page Object Model with one component class per page section; explicit waits only (no `time.sleep`);
every test starts with its own browser, so tests run in any order and in parallel (`pytest -n 4`);
test data in `test_data/*.json`; no secrets in code.

## 5. Environment and data
- **Python** 3.10 or newer, **Selenium** 4.20+, **Pytest** 8+, Google Chrome (driver by Selenium Manager).
- Default run: headless Chrome, window 1920x1080, `pytest -n 4`.
- The site is public and read-only. Nothing is saved on the server, so no clean-up is needed.
- Files for the upload cases are created in a temporary folder by the test; downloads go to a per-test folder.

## 6. Entry and exit criteria
- **Entry:** the practice site opens in a browser, the dependencies are installed (`pip install -r requirements.txt`), `python scripts/check_traceability.py` passes.
- **Exit:** all P1 and P2 cases pass, the pass rate is 98% or more, every failure is either fixed or logged as a defect with an `xfail` marker.
  A release candidate needs a full run with retries switched off.

## 7. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Public site is slow or down | Failing tests that are not product bugs | Longer page-load timeout in CI, page open is retried, `external` cases are skipped in CI |
| Third-party sites (Wikipedia, deadlinkcity.com, apple.com) change or block | Flaky `external` cases | Marker `external`, small independent cases, retries (`--reruns`) only in CI |
| Site markup changes | Broken locators | Locators live only in page objects and components, so a fix is one line |
| Advertisement or cookie overlays | Clicks intercepted | Helpers scroll the element into view and retry on interception |

## 8. Deliverables
Test case documents and master CSV (`docs/test-cases/`), automation code, per-run CSV and module-wise HTML reports with a
history index (`reports/`), traceability check, CI pipeline (GitHub Actions: lint, traceability, tests).
