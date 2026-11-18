"""'Download Files' page."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Settings
from core.base_page import BasePage, Locator


class DownloadFilesPage(BasePage):
    PATH = "/p/download-files_25.html"

    TEXT_AREA: Locator = (By.ID, "inputText")
    GENERATE_TXT: Locator = (By.ID, "generateTxt")
    TXT_LINK: Locator = (By.ID, "txtDownloadLink")
    GENERATE_PDF: Locator = (By.ID, "generatePdf")
    PDF_LINK: Locator = (By.ID, "pdfDownloadLink")

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        super().__init__(driver, settings.explicit_timeout)
        self.settings = settings

    def open(self) -> DownloadFilesPage:
        self.driver.get(self.settings.base_url + self.PATH)
        self.visible(self.TEXT_AREA)
        return self

    def download_text_file(self, content: str) -> None:
        self.type(self.TEXT_AREA, content)
        self.click(self.GENERATE_TXT)
        self.click(self.TXT_LINK)

    def download_pdf_file(self, content: str) -> None:
        self.type(self.TEXT_AREA, content)
        self.click(self.GENERATE_PDF)
        self.click(self.PDF_LINK)

    def txt_download_name(self) -> str | None:
        return self.attribute(self.TXT_LINK, "download")

    def pdf_download_name(self) -> str | None:
        return self.attribute(self.PDF_LINK, "download")
