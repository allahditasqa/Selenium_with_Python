# Selenium_with_Python

**Automation Framework:** Selenium 4 + Python + Pytest, built with the Page Object Model and reusable components, running against the public practice site **[testautomationpractice.blogspot.com](https://testautomationpractice.blogspot.com/)**.

It covers **every practice section** of that site (main page + "Hidden Elements & AJAX" + "Download Files" pages) with 152 automated tests.

---

## 1. What you get

| Feature | How it is done |
|---|---|
| Page Object Model | One class per page, one small **component** class per section (`pages/components/`) |
| No `time.sleep()` | Explicit waits only, wrapped once in `core/base_page.py` |
| Browsers | Chrome (default), Firefox, Edge, or a remote Selenium Grid - chosen by a command-line flag |
| Driver management | Selenium Manager downloads the right driver automatically |
| Config | `.env` file + command-line options (`--browser`, `--headless`, `--base-url`) |
| Test data | JSON files in `test_data/`, not hard-coded in tests |
| Reports | **Module-wise HTML reports** (one per test file) with every test case, its status, duration and a **screenshot**, plus CSV of test cases and an `index.html` |
| Parallel run | `pytest -n 4` (pytest-xdist). Every test has its own browser and its own download folder |
| Flaky test retry | `pytest --reruns 1` (pytest-rerunfailures), used in CI only |
| Logging | Every click/type is logged to `logs/test.log` |
| Markers | `smoke`, `regression`, `external`, `slow` to run subsets |
| Code quality | `ruff` lint + format configured in `pyproject.toml` |
| CI | GitHub Actions: lint, then tests in headless Chrome, report uploaded as an artifact |

---

## 2. Folder structure

```
Selenium_with_Python/
├── conftest.py              # fixtures: cfg, driver, home, hidden_page, download_page
├── pytest.ini               # pytest options, markers, logging, HTML report path
├── pyproject.toml           # ruff (lint/format) settings
├── requirements.txt         # runtime dependencies
├── requirements-dev.txt     # + ruff
├── .env.example             # copy to .env to change defaults
│
├── config/
│   └── settings.py          # Settings dataclass (reads .env / environment)
│
├── core/                    # framework engine - knows nothing about the website
│   ├── driver_factory.py    # builds Chrome / Firefox / Edge / Remote drivers
│   ├── base_page.py         # explicit waits, click/type/select/hover/alerts/windows helpers
│   └── logger.py
│
├── pages/                   # page objects (what the website looks like)
│   ├── home_page.py                 # main page: composes all section components
│   ├── hidden_elements_page.py      # Hidden Elements & AJAX page
│   ├── download_files_page.py       # Download Files page
│   └── components/                  # one class per page section
│       ├── data_entry_form.py       # inputs, radio, checkbox, dropdowns, date pickers, date range
│       ├── upload_files.py
│       ├── static_table.py   dynamic_table.py   pagination_table.py
│       ├── wikipedia_tabs.py        # "Tabs" section (links open in new tabs)
│       ├── widgets.py               # dynamic button, alerts, hover, double click,
│       │                            #   drag & drop, slider, SVG, scrolling dropdown
│       └── links_and_sections.py    # labels & links, form sections, footer, Shadow DOM, visitors
│
├── tests/ui/                # the test cases (one file per area)
│   ├── test_01_home_page.py
│   ├── test_02_data_entry_form.py
│   ├── test_03_upload_files.py
│   ├── test_04_tables.py
│   ├── test_05_widgets.py
│   ├── test_06_alerts_and_windows.py
│   ├── test_07_links_sections_shadow.py
│   ├── test_08_hidden_elements_ajax.py
│   └── test_09_downloads.py
│
├── test_data/               # JSON data + loader
├── reporting/plugin.py      # pytest plugin that writes the module-wise HTML/CSV reports
├── utils/                   # file helpers (wait for download) and a link status checker
└── .github/workflows/tests.yml
```

**The idea in one line:** tests say *what* to check, page objects say *where* things are, `core/` says *how* to talk to the browser. Nothing else is mixed in.

---

## 3. Setup (5 minutes)

You need **Python 3.10+** and **Google Chrome** installed.

```bash
git clone https://github.com/allahditasqa/Selenium_with_Python.git
cd Selenium_with_Python

# create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

Optional: `copy .env.example .env` (Windows) or `cp .env.example .env` and edit values.

---

## 4. Run the tests

```bash
pytest                                  # everything, headless Chrome
pytest -n 4                             # 4 tests in parallel (much faster)
pytest --headless false                 # watch the browser
pytest --browser firefox                # chrome | firefox | edge
pytest -m smoke                         # only the quick smoke tests
pytest -m "not external"                # skip tests that need other websites
pytest tests/ui/test_04_tables.py       # one file
pytest -k "slider"                      # tests with "slider" in the name
pytest -n 4 --reruns 1                  # retry a failed test once
```

### Reports

After every run open **`reports/index.html`**. It lists one report per module:

```
reports/
├── index.html                                   # all modules, totals, links, previous runs
├── data-entry-form/
│   ├── Data Entry Form test 18-11-2026_12-30.html    # every test case + status + time + screenshot
│   └── Data Entry Form test cases 18-11-2026_12-30.csv
├── tables/ ...   widgets/ ...   downloads/ ...
└── screenshots/                                 # PNG/JPG of failed tests only
```

The latest sample reports of a full run (152 passed) are committed in the `reports/` folder - clone the repo and open `reports/index.html` (GitHub shows HTML as text, so download or clone it).

Each module report shows total / passed / failed / skipped, then one card per test case (`TC_DATA_ENTRY_FORM_01 - ...`) with the error text (if it failed) and a screenshot - click a screenshot to enlarge it. Test case IDs are numbered per module in file order and stay the same even if you run only a subset. Detailed step logs are in `logs/test.log`.

### Test markers

| Marker | Meaning |
|---|---|
| `smoke` | page loads, every section exists |
| `regression` | full functional tests |
| `external` | needs another website (Wikipedia, selenium.dev, apple.com, deadlinkcity.com ...). Can be slow or flaky because we do not control those sites |

---

## 5. What is tested (152 tests)

| Section on the site | What the tests check |
|---|---|
| **Home page** | title, heading, all 19 section titles, footer links |
| **Data Entry Form** | text fields + max-length limits, gender radio (mutually exclusive), 7 day checkboxes, country dropdown (all 10 options), colors/animals multi-select, sorted animal list, 2 jQuery date pickers (mm/dd/yyyy and dd/mm/yyyy), date range (valid, same day, reversed, empty), one full end-to-end form |
| **Upload Files** | single file, multiple files, no file chosen |
| **Static Web Table** | headers, row count, filter by author, total / max price |
| **Dynamic Web Table** | columns and values change on every load, so cells are found **by header name**; values shown below the table match the table |
| **Pagination Table** | 4 pages, ids per page, unique products over all pages, price format, checkbox selection |
| **Tabs (Wikipedia)** | search results, links open in a new tab, "More" link |
| **Dynamic Button** | START <-> STOP text, `name` and CSS class change |
| **Alerts & Popups** | simple alert, confirm (OK / Cancel), prompt (text / cancel), "New Tab" button, popup windows |
| **Mouse Hover** | menu hidden, then visible on hover |
| **Double Click** | double click copies text, single click does not |
| **Drag and Drop** | drag the box on the target, text becomes "Dropped!" |
| **Slider** | default range, keyboard and mouse movement of both handles |
| **SVG Elements** | circle / rectangle / triangle are visible with the right color |
| **Scrolling DropDown** | 100 items, scroll to Item 1 / 50 / 100 and select |
| **Labels And Links** | mobile labels, laptop link URLs, link navigation, 8 "broken link" URLs and their HTTP status |
| **Form (Sections 1-3)** | text, input and submit in each section, sections are independent |
| **Shadow DOM** | text, input, checkbox and link inside a shadow root and a nested shadow root |
| **Visitors** | counter is a number |
| **Hidden Elements & AJAX page** | hidden input/checkbox toggled, status label text, AJAX content appears after a delay |
| **Download Files page** | generate and download a `.txt` and a `.pdf` file, check file name and content |

### Things the tests found about the practice site (not framework bugs)

* The **Colors** list contains *Red* and *Green* twice, so selecting "Red" by text selects both. The test documents this.
* The "Generate and Download **PDF**" button saves the typed text with a `.pdf` extension; it is not a real PDF file. The test checks what the site really does.
* The "Playwright Practice" page (getByRole / getByText examples) is **not** covered: it targets Playwright locators and is outside this Selenium suite.

---

## 6. How to write a new test (example)

1. Add locators and methods for the new element to a component in `pages/components/`:
   ```python
   class DynamicButton(BasePage):
       BUTTON = (By.CSS_SELECTOR, "#HTML5 button")

       def label(self) -> str:
           return self.text(self.BUTTON)
   ```
2. Use it in a test in `tests/ui/`. The `home` fixture opens the site and gives you the page object:
   ```python
   @pytest.mark.regression
   def test_button_label(home):
       assert home.dynamic_button.label() == "START"
   ```
3. Run it: `pytest -k test_button_label --headless false`

Rules used in this repo:
* Tests contain **assertions only**, never locators.
* Page objects contain locators and actions, **never assertions**.
* No `time.sleep()` - use `wait_until(...)`, `wait_for_text(...)` etc.
* Locate dynamic content by meaning (header text, link text), not by position.

---

## 7. Run on CI (GitHub Actions)

`.github/workflows/tests.yml` runs on every push: `ruff check`, then the suite without the `external` tests (third-party sites can block cloud runners) in headless Chrome with 2 workers and up to two retries, and uploads `reports/` as a build artifact.

## 8. Run on Selenium Grid / Docker

Start any Grid (for example `docker run -d -p 4444:4444 selenium/standalone-chrome`) and run:

```bash
set SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub      # Windows
# export SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub  # macOS / Linux
pytest -n 2
```
(The remote option is implemented in `core/driver_factory.py`; it was not exercised in the verification run described below.)

## 9. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: config` | run `pytest` from the repository root |
| Browser does not open | add `--headless false`; make sure Chrome is installed and up to date |
| `external` tests fail | those sites may be slow or blocking bots - run `pytest -m "not external"` |
| Tests slow | use `pytest -n 4` |

---

## 10. Verification status

The full suite was run locally on Windows 11 with Python 3.14 and headless Chrome (`pytest -n 4`): **152 passed in about 10 minutes**. The Linux CI result is in the repository Actions tab.

## License

MIT - free to use for learning and practice.
