"""Small interactive widgets: dynamic button, alerts & popups, hover menu, double click,
drag and drop, jQuery UI slider, SVG shapes, scrolling dropdown."""

from __future__ import annotations

import re

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.base_page import BasePage, Locator


class DynamicButton(BasePage):
    BUTTON: Locator = (By.CSS_SELECTOR, "#HTML5 button")

    def label(self) -> str:
        return self.text(self.BUTTON)

    def click_button(self) -> None:
        self.click(self.BUTTON)

    def name_attribute(self) -> str | None:
        return self.attribute(self.BUTTON, "name")

    def css_classes(self) -> list[str]:
        return (self.attribute(self.BUTTON, "class") or "").split()


class AlertsAndPopups(BasePage):
    SIMPLE: Locator = (By.ID, "alertBtn")
    CONFIRM: Locator = (By.ID, "confirmBtn")
    PROMPT: Locator = (By.ID, "promptBtn")
    RESULT: Locator = (By.ID, "demo")
    NEW_TAB: Locator = (By.XPATH, "//button[normalize-space()='New Tab']")
    POPUP: Locator = (By.ID, "PopUp")

    def simple_alert(self) -> str:
        self.click(self.SIMPLE)
        return self.accept_alert()

    def confirm(self, accept: bool) -> str:
        """Returns the text shown on the page after the alert was handled."""
        self.click(self.CONFIRM)
        if accept:
            self.accept_alert()
        else:
            self.dismiss_alert()
        return self.result_text()

    def prompt(self, answer: str | None) -> str:
        """answer=None dismisses the prompt. Returns the text shown on the page afterwards."""
        self.click(self.PROMPT)
        if answer is None:
            self.dismiss_alert()
        else:
            self.accept_alert(prompt_text=answer)
        return self.result_text()

    def prompt_text(self) -> str:
        self.click(self.PROMPT)
        text = self.alert_text()
        self.dismiss_alert()
        return text

    def result_text(self) -> str:
        self.wait_until(lambda d: self.find(self.RESULT).text.strip() != "", "Alert result text not shown")
        return self.text(self.RESULT)

    def open_new_tab(self) -> None:
        self.click(self.NEW_TAB)

    def open_popup_windows(self) -> None:
        self.click(self.POPUP)


class MouseHover(BasePage):
    BUTTON: Locator = (By.CSS_SELECTOR, ".dropbtn")
    MENU_ITEMS: Locator = (By.CSS_SELECTOR, ".dropdown-content a")

    def menu_visible(self) -> bool:
        items = self.find_all(self.MENU_ITEMS)
        return bool(items) and all(i.is_displayed() for i in items)

    def hover_menu(self) -> list[str]:
        self.hover(self.BUTTON)
        self.wait_until(lambda d: self.menu_visible(), "Hover menu did not open")
        return self.texts(self.MENU_ITEMS)


class DoubleClick(BasePage):
    FIELD_1: Locator = (By.ID, "field1")
    FIELD_2: Locator = (By.ID, "field2")
    COPY_BUTTON: Locator = (By.XPATH, "//button[normalize-space()='Copy Text']")

    def set_source(self, text: str) -> None:
        self.type(self.FIELD_1, text)

    def double_click_copy(self) -> None:
        self.double_click(self.COPY_BUTTON)

    def single_click_copy(self) -> None:
        self.click(self.COPY_BUTTON)

    def target_value(self) -> str:
        return self.value(self.FIELD_2)


class DragAndDrop(BasePage):
    SOURCE: Locator = (By.ID, "draggable")
    TARGET: Locator = (By.ID, "droppable")

    def drag_to_target(self) -> None:
        source = self.scroll_to(self.SOURCE)
        target = self.find(self.TARGET)
        ActionChains(self.driver).click_and_hold(source).move_to_element(target).release().perform()

    def target_text(self) -> str:
        return self.text(self.TARGET)

    def target_highlighted(self) -> bool:
        return "ui-state-highlight" in (self.attribute(self.TARGET, "class") or "")


class Slider(BasePage):
    HANDLES: Locator = (By.CSS_SELECTOR, "#slider-range .ui-slider-handle")
    AMOUNT: Locator = (By.ID, "amount")

    def range(self) -> tuple[int, int]:
        low, high = re.findall(r"\$(\d+)", self.value(self.AMOUNT))
        return int(low), int(high)

    def nudge_min(self, steps: int, direction: str = Keys.ARROW_RIGHT) -> None:
        handle = self.scroll_to(self.find_all(self.HANDLES)[0])
        for _ in range(steps):
            handle.send_keys(direction)

    def nudge_max(self, steps: int, direction: str = Keys.ARROW_LEFT) -> None:
        handle = self.scroll_to(self.find_all(self.HANDLES)[1])
        for _ in range(steps):
            handle.send_keys(direction)

    def drag_max_handle(self, x_offset: int) -> None:
        handle = self.scroll_to(self.find_all(self.HANDLES)[1])
        ActionChains(self.driver).click_and_hold(handle).move_by_offset(x_offset, 0).release().perform()


class SvgShapes(BasePage):
    CONTAINER = ".svg-container"

    def fill(self, shape: str) -> str | None:
        return self.attribute((By.CSS_SELECTOR, f"{self.CONTAINER} {shape}"), "fill")

    def shape_visible(self, shape: str) -> bool:
        return self.is_displayed((By.CSS_SELECTOR, f"{self.CONTAINER} {shape}"))

    def svg_count(self) -> int:
        return self.count((By.CSS_SELECTOR, f"{self.CONTAINER} svg"))


class ScrollingDropdown(BasePage):
    INPUT: Locator = (By.ID, "comboBox")
    OPTIONS: Locator = (By.CSS_SELECTOR, "#dropdown .option, #dropdown div")

    def open(self) -> None:
        self.click(self.INPUT)
        self.wait_until(lambda d: self.is_displayed((By.ID, "dropdown")), "Dropdown did not open")

    def option_count(self) -> int:
        return self.count(self.OPTIONS)

    def choose(self, item: str) -> str:
        self.open()
        option = (By.XPATH, f"//div[@id='dropdown']//div[normalize-space()='{item}']")
        self.scroll_to(option)
        self.click(option)
        return self.value(self.INPUT)
