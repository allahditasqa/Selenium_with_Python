"""Shared fixtures and hooks.

* `cfg`          - effective settings (env + command line)
* `driver`       - a fresh browser per test, closed afterwards
* `home`         - HomePage object already opened
* screenshot of the failing page is attached to the HTML report
"""

from __future__ import annotations

import base64
import dataclasses
from collections.abc import Iterator
from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Settings, settings
from core.driver_factory import DriverFactory
from pages.download_files_page import DownloadFilesPage
from pages.hidden_elements_page import HiddenElementsPage
from pages.home_page import HomePage


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("framework")
    group.addoption(
        "--browser", default=None, help="chrome | firefox | edge (default: BROWSER env or chrome)"
    )
    group.addoption(
        "--headless", default=None, choices=["true", "false"], help="run without UI (default: true)"
    )
    group.addoption("--base-url", default=None, help="override BASE_URL")


@pytest.fixture(scope="session")
def cfg(request: pytest.FixtureRequest) -> Settings:
    overrides = {}
    if request.config.getoption("--browser"):
        overrides["browser"] = request.config.getoption("--browser").lower()
    if request.config.getoption("--headless"):
        overrides["headless"] = request.config.getoption("--headless") == "true"
    if request.config.getoption("--base-url"):
        overrides["base_url"] = request.config.getoption("--base-url").rstrip("/")
    return dataclasses.replace(settings, **overrides)


@pytest.fixture
def download_dir(tmp_path: Path) -> Path:
    path = tmp_path / "downloads"
    path.mkdir()
    return path


@pytest.fixture
def driver(cfg: Settings, download_dir: Path, request: pytest.FixtureRequest) -> Iterator[WebDriver]:
    browser = DriverFactory.create(cfg, download_dir)
    request.node.driver = browser
    yield browser
    browser.quit()


@pytest.fixture
def home(driver: WebDriver, cfg: Settings) -> HomePage:
    return HomePage(driver, cfg).open()


@pytest.fixture
def hidden_page(driver: WebDriver, cfg: Settings) -> HiddenElementsPage:
    return HiddenElementsPage(driver, cfg).open()


@pytest.fixture
def download_page(driver: WebDriver, cfg: Settings) -> DownloadFilesPage:
    return DownloadFilesPage(driver, cfg).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """On failure: save a screenshot and embed it in the pytest-html report."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return
    browser = getattr(item, "driver", None)
    if browser is None:
        return
    try:
        png = browser.get_screenshot_as_png()
    except Exception:  # browser may already be gone
        return
    shots = settings.screenshot_dir
    shots.mkdir(parents=True, exist_ok=True)
    (shots / f"{item.name}.png".replace("/", "_")).write_bytes(png)
    try:
        import pytest_html

        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(base64.b64encode(png).decode("ascii")))
        report.extras = extras
    except ImportError:
        pass
