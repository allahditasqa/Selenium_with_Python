# Test Case Standard (the same format in every module)

Every test case of this project is written in **this format**, so a new team member can read, review and run any case without help.
The language is **simple English**: short sentences, active voice, exact UI text in quotes.

## 1. Folder structure

| Item | Location | Example |
| --- | --- | --- |
| Test case document (source of truth) | `docs/test-cases/<module-slug>.md` | `docs/test-cases/data-entry-form.md` |
| **Master CSV** (regression list, one fixed file per module) | `docs/test-cases/<module-slug>.csv` | `docs/test-cases/data-entry-form.csv` |
| Automation code | `tests/ui/test_<NN>_<name>.py` | `tests/ui/test_02_data_entry_form.py` |
| Page objects / components | `pages/`, `pages/components/` | `pages/components/data_entry_form.py` |
| Run report (new file for every run) | `reports/<module-slug>/<Module> test <DD-MM-YYYY>_<HH-mm-ss>.html` | `reports/tables/Tables test 18-11-2026_12-52-10.html` |
| Run CSV (only the cases that ran) | `reports/<module-slug>/<Module> test cases <DD-MM-YYYY>_<HH-mm-ss>.csv` | `reports/tables/Tables test cases 18-11-2026_12-52-10.csv` |
| History of all runs | `reports/index.html`, `reports/history.json` | |

One module = one document + one master CSV + one test file + one report per run.

## 2. Test case ID

`TC_<MODULE>_<NN>` (NN = 01, 02, 03 ...), for example `TC_FORM_07`. An ID is never used twice and never reused for another case.
Data-driven cases (one test, many data sets) get `TC_FORM_07.1`, `TC_FORM_07.2` ... one row per data set.

**The same ID is in the code**, in three places:

| Place | Example |
| --- | --- |
| Test function name | `def test_tc_form_07_select_several_days(self, home):` |
| First line of the docstring: `<ID> - <title>` | `"""TC_FORM_07 - Select Monday, Wednesday and Friday and check only these three days are selected."""` |
| Data-driven test: pytest parameter ids | `@pytest.mark.parametrize("day", DAYS, ids=tc_ids("TC_FORM_06", 7))` |

The docstring title is what shows in the report, so it must be **exactly** the same sentence as the Title column of the document.
For data-driven tests the docstring uses `{parameter}` placeholders (for example `{day}`).

| Module | Prefix | Test file |
| --- | --- | --- |
| Home Page | `TC_HOME_` | `test_01_home_page.py` |
| Data Entry Form | `TC_FORM_` | `test_02_data_entry_form.py` |
| Upload Files | `TC_UPLOAD_` | `test_03_upload_files.py` |
| Tables | `TC_TABLE_` | `test_04_tables.py` |
| Widgets | `TC_WIDGET_` | `test_05_widgets.py` |
| Alerts And Windows | `TC_ALERT_` | `test_06_alerts_and_windows.py` |
| Links, Sections And Shadow DOM | `TC_LINK_` | `test_07_links_sections_shadow.py` |
| Hidden Elements And AJAX | `TC_HIDDEN_` | `test_08_hidden_elements_ajax.py` |
| Downloads | `TC_DOWNLOAD_` | `test_09_downloads.py` |

## 3. Document format

Every `.md` file has these sections in this order:

1. **Title:** `# <Module> Test Cases`
2. **Header lines:** automation file, report location, application URL, ID prefix, master CSV.
3. **Overview:** 2-3 lines about what the module covers.
4. **Scope and notes:** what is and is not tested, data rules, known site quirks, external dependencies.
5. **Test case tables:** one table per group (`## A. ...`), same columns in every table.
6. **Summary:** cases and automated cases per group, and the total.

### Columns of the test case table (never change them)

| Column | Meaning |
| --- | --- |
| **ID** | Rule above |
| **Title** | One full sentence: what is done and which data is used. Ends with a full stop. |
| **Priority** | `P1 - Critical` (the feature is unusable if it fails), `P2 - High`, `P3 - Medium`, `P4 - Low` (cosmetic or rare) |
| **Type** | Smoke, Functional, Negative, Boundary, Validation, UI, End to end |
| **Preconditions** | What must be true before step 1 |
| **Test data** | Exact data used, `-` if none |
| **Steps** | Numbered, short, action based (`1. Click ...`) |
| **Expected result** | Clear and checkable; exact message texts in quotes |
| **Automation** | `Automated` and the test method: `<file>::<Class>::<method>` |

The master CSV has the same content with these columns: `ID, Module, Sub-module, Title, Priority, Type, Preconditions, Test Data, Steps, Expected Result, Automation Status, Test File, Test Method, Last Updated`.
The Sub-module is the group heading (`## A. Text fields` becomes `Text fields`).

## 4. Writing rules

1. One test case checks one thing.
2. The title says the action and the data. Never write a secret in a title.
3. Quote exact UI texts: `"You selected a range of 10 days."`.
4. Do not hard-code values that keep changing (counters, dates); write the relation instead.
5. **Only automated cases are documented**, and **every automated case is documented**. There are no manual-only rows and no undocumented tests.
6. A new case gets a new ID; an old ID is never reused. If a case is removed, remove the test and the row together.
7. Known site defects are not hidden: the test is marked `xfail` with a reason and an entry is added to `docs/DEFECTS.md`.

## 5. How the documents, the CSV and the code stay in sync

| Command | What it does |
| --- | --- |
| `python scripts/cases_csv.py` | Rebuilds the master CSV files from the `.md` documents. Unchanged rows keep their `Last Updated` date. |
| `python scripts/cases_csv.py --check` | Fails if a master CSV is older than its document. |
| `python scripts/check_traceability.py` | Collects the tests (no browser) and compares them with the master CSV: ID, title, test method. Fails on any difference. |

The CI pipeline runs both checks before the tests. The run CSV and the HTML report take priority, steps, test data and expected result from the master CSV by test case ID, so a documented case always shows its written steps in the report.

## 6. Checklist for a new test case

- [ ] Added the row (new ID) to `docs/test-cases/<module>.md`
- [ ] Wrote the test in `tests/ui/test_<NN>_<name>.py` with the ID in the function name and docstring (and `ids=tc_ids(...)` if data-driven)
- [ ] Title in the docstring is the same sentence as in the document
- [ ] Ran `python scripts/cases_csv.py` and `python scripts/check_traceability.py`
- [ ] Ran the test and looked at the new report in `reports/`
- [ ] Updated the counts in the README
