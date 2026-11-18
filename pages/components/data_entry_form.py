"""'Data Entry Form' section: text fields, radio, checkboxes, dropdowns, date pickers, date range."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from core.base_page import BasePage, Locator


class DataEntryForm(BasePage):
    NAME: Locator = (By.ID, "name")
    EMAIL: Locator = (By.ID, "email")
    PHONE: Locator = (By.ID, "phone")
    ADDRESS: Locator = (By.ID, "textarea")
    COUNTRY: Locator = (By.ID, "country")
    COLORS: Locator = (By.ID, "colors")
    ANIMALS: Locator = (By.ID, "animals")
    DATE_PICKER_1: Locator = (By.ID, "datepicker")  # mm/dd/yyyy
    DATE_PICKER_2: Locator = (By.ID, "txtDate")  # dd/mm/yyyy
    START_DATE: Locator = (By.ID, "start-date")
    END_DATE: Locator = (By.ID, "end-date")
    SUBMIT: Locator = (By.CSS_SELECTOR, ".submit-btn")
    RESULT: Locator = (By.ID, "result")

    # --- text fields
    def fill_name(self, value: str) -> None:
        self.type(self.NAME, value)

    def fill_email(self, value: str) -> None:
        self.type(self.EMAIL, value)

    def fill_phone(self, value: str) -> None:
        self.type(self.PHONE, value)

    def fill_address(self, value: str) -> None:
        self.type(self.ADDRESS, value)

    # --- radio / checkbox
    @staticmethod
    def _gender(value: str) -> Locator:
        return (By.ID, value)

    def choose_gender(self, value: str) -> None:
        self.click(self._gender(value))

    def is_gender_selected(self, value: str) -> bool:
        return self.is_selected(self._gender(value))

    def set_day(self, day: str, checked: bool = True) -> None:
        if self.is_selected((By.ID, day)) != checked:
            self.click((By.ID, day))

    def is_day_selected(self, day: str) -> bool:
        return self.is_selected((By.ID, day))

    # --- dropdowns
    def select_country(self, country: str) -> None:
        self.select_by_text(self.COUNTRY, country)

    def selected_country(self) -> str:
        return Select(self.find(self.COUNTRY)).first_selected_option.text.strip()

    def country_options(self) -> list[str]:
        return [o.text.strip() for o in Select(self.find(self.COUNTRY)).options]

    def select_multiple(self, locator: Locator, values: list[str]) -> None:
        select = Select(self.find(locator))
        select.deselect_all()
        for value in values:
            select.select_by_visible_text(value)

    def selected_multiple(self, locator: Locator) -> list[str]:
        return [o.text.strip() for o in Select(self.find(locator)).all_selected_options]

    def options(self, locator: Locator) -> list[str]:
        return [o.text.strip() for o in Select(self.find(locator)).options]

    # --- date pickers (jQuery UI)
    def pick_date(self, input_locator: Locator, day: int) -> str:
        """Open the jQuery UI calendar of the input and click a day of the displayed month."""
        self.click(input_locator)
        day_link = (
            By.XPATH,
            f"//div[@id='ui-datepicker-div']//td[@data-handler='selectDay']/a[normalize-space()='{day}']",
        )
        self.click(day_link)
        return self.value(input_locator)

    # --- date range
    def set_date_range(self, start_iso: str, end_iso: str) -> None:
        """Dates in ISO format (yyyy-mm-dd) - the only format <input type=date> accepts through .value."""
        self.set_value_js(self.START_DATE, start_iso)
        self.set_value_js(self.END_DATE, end_iso)

    def submit(self) -> str:
        self.click(self.SUBMIT)
        self.wait_until(lambda d: self.text_present(self.RESULT), "Result message did not appear")
        return self.text(self.RESULT)

    def text_present(self, locator: Locator) -> bool:
        elements = self.find_all(locator)
        return bool(elements) and bool(elements[0].text.strip())
