"""Creates WebDriver instances. Driver binaries are resolved by Selenium Manager (no manual downloads)."""

from __future__ import annotations

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Settings


class DriverFactory:
    @staticmethod
    def create(settings: Settings, download_dir: Path) -> WebDriver:
        browser = settings.browser.lower()
        width, height = (int(x) for x in settings.window_size.split(","))
        download_dir.mkdir(parents=True, exist_ok=True)

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if settings.headless:
                options.add_argument("--headless=new")
            options.add_argument(f"--window-size={width},{height}")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-search-engine-choice-screen")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.page_load_strategy = "eager"
            options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": str(download_dir),
                    "download.prompt_for_download": False,
                    "plugins.always_open_pdf_externally": True,
                    "profile.default_content_setting_values.automatic_downloads": 1,
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                },
            )
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            driver = DriverFactory._build(settings, options, webdriver.Chrome)
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if settings.headless:
                options.add_argument("-headless")
            options.page_load_strategy = "eager"
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", str(download_dir))
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,application/pdf")
            options.set_preference("pdfjs.disabled", True)
            driver = DriverFactory._build(settings, options, webdriver.Firefox)
        elif browser == "edge":
            options = webdriver.EdgeOptions()
            if settings.headless:
                options.add_argument("--headless=new")
            options.add_argument(f"--window-size={width},{height}")
            options.page_load_strategy = "eager"
            options.add_experimental_option(
                "prefs",
                {"download.default_directory": str(download_dir), "download.prompt_for_download": False},
            )
            driver = DriverFactory._build(settings, options, webdriver.Edge)
        else:
            raise ValueError(f"Unsupported browser '{settings.browser}'. Use chrome, firefox or edge.")

        driver.set_page_load_timeout(settings.page_load_timeout)
        if not settings.headless:
            driver.set_window_size(width, height)
        return driver

    @staticmethod
    def _build(settings: Settings, options, local_driver_class) -> WebDriver:
        if settings.remote_url:
            return webdriver.Remote(command_executor=settings.remote_url, options=options)
        return local_driver_class(options=options)
