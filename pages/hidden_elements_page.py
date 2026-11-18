"""'Hidden Elements & AJAX' page."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Settings
from core.base_page import BasePage, Locator


class HiddenElementsPage(BasePage):
    PATH = "/p/gui-elements-ajax-hidden.html"

    INPUT_1: Locator = (By.ID, "input1")
    INPUT_2: Locator = (By.ID, "input2")
    CHECKBOX_1: Locator = (By.ID, "checkbox1")
    CHECKBOX_2: Locator = (By.ID, "checkbox2")
    TOGGLE_INPUT: Locator = (By.ID, "toggleInput")
    TOGGLE_CHECKBOX: Locator = (By.ID, "toggleCheckbox")
    LOAD_AJAX: Locator = (By.ID, "loadContent")
    STATUS: Locator = (By.ID, "statusLabel")
    AJAX_CONTENT: Locator = (By.ID, "ajaxContent")

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        super().__init__(driver, settings.explicit_timeout)
        self.settings = settings

    def open(self) -> HiddenElementsPage:
        self.driver.get(self.settings.base_url + self.PATH)
        self.visible(self.TOGGLE_INPUT)
        return self

    def status(self) -> str:
        return self.text(self.STATUS)

    def toggle_input_2(self) -> None:
        self.click(self.TOGGLE_INPUT)

    def toggle_checkbox_2(self) -> None:
        self.click(self.TOGGLE_CHECKBOX)

    def load_ajax_content(self) -> str:
        self.click(self.LOAD_AJAX)
        self.wait_for_text(self.AJAX_CONTENT, "AJAX Content Loaded")
        return self.text(self.AJAX_CONTENT)
