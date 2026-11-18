"""'Upload Files' section."""

from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class UploadFiles(BasePage):
    SINGLE_INPUT: Locator = (By.ID, "singleFileInput")
    SINGLE_BUTTON: Locator = (By.CSS_SELECTOR, "#singleFileForm button")
    SINGLE_STATUS: Locator = (By.ID, "singleFileStatus")
    MULTI_INPUT: Locator = (By.ID, "multipleFilesInput")
    MULTI_BUTTON: Locator = (By.CSS_SELECTOR, "#multipleFilesForm button")
    MULTI_STATUS: Locator = (By.ID, "multipleFilesStatus")

    def upload_single(self, file: Path) -> str:
        self.find(self.SINGLE_INPUT).send_keys(str(file))
        self.click(self.SINGLE_BUTTON)
        return self.text(self.SINGLE_STATUS)

    def upload_multiple(self, files: list[Path]) -> str:
        self.find(self.MULTI_INPUT).send_keys("\n".join(str(f) for f in files))
        self.click(self.MULTI_BUTTON)
        return self.text(self.MULTI_STATUS)

    def single_status(self) -> str:
        return self.find(self.SINGLE_STATUS).text.strip()
