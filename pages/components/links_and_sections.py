"""Labels & links, 'Form' sections 1-3, footer links, Shadow DOM and the visitors counter."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.shadowroot import ShadowRoot

from core.base_page import BasePage, Locator


class LabelsAndLinks(BasePage):
    MOBILE_LABELS: Locator = (By.CSS_SELECTOR, "#mobiles label")
    LAPTOP_LINKS: Locator = (By.CSS_SELECTOR, "#laptops a")
    BROKEN_LINKS: Locator = (By.CSS_SELECTOR, "#broken-links a")

    def mobile_labels(self) -> list[str]:
        return self.texts(self.MOBILE_LABELS)

    def laptop_links(self) -> dict[str, str]:
        return {a.text.strip(): a.get_attribute("href") for a in self.find_all(self.LAPTOP_LINKS)}

    def broken_links(self) -> dict[str, str]:
        return {a.text.strip(): a.get_attribute("href") for a in self.find_all(self.BROKEN_LINKS)}

    def click_laptop_link(self, brand: str) -> None:
        self.click((By.XPATH, f"//div[@id='laptops']//a[normalize-space()='{brand}']"))


class FormSections(BasePage):
    """Three similar blocks (section1..3), each with a paragraph, an input and a Submit button."""

    SECTIONS = (1, 2, 3)

    def heading(self, number: int) -> str:
        return self.text((By.CSS_SELECTOR, f"#section{number} h4"))

    def paragraph(self, number: int) -> str:
        return self.text((By.ID, f"para{number}"))

    def fill(self, number: int, value: str) -> None:
        self.type((By.ID, f"input{number}"), value)

    def value(self, number: int) -> str:  # type: ignore[override]
        return super().value((By.ID, f"input{number}"))

    def submit(self, number: int) -> None:
        self.click((By.ID, f"btn{number}"))


class FooterLinks(BasePage):
    LINKS: Locator = (By.CSS_SELECTOR, "#PageList1 a")

    def links(self) -> dict[str, str]:
        return {a.text.strip(): a.get_attribute("href") for a in self.find_all(self.LINKS)}

    def open(self, text: str) -> None:
        self.click((By.XPATH, f"//div[@id='PageList1']//a[normalize-space()='{text}']"))


class ShadowDom(BasePage):
    """Elements inside open shadow roots (one nested two levels deep)."""

    HOST: Locator = (By.ID, "shadow_host")

    def _root(self) -> ShadowRoot:
        self.scroll_to(self.HOST)
        return self.find(self.HOST).shadow_root

    def _nested_root(self) -> ShadowRoot:
        return self._root().find_element(By.CSS_SELECTOR, "#nested_shadow_host").shadow_root

    def info_text(self) -> str:
        return self._root().find_element(By.CSS_SELECTOR, ".info").text.strip()

    def nested_text(self) -> str:
        return self._nested_root().find_element(By.CSS_SELECTOR, "#nested_shadow_content div").text.strip()

    def type_in_input(self, text: str) -> str:
        field = self._root().find_element(By.CSS_SELECTOR, "input[type='text']")
        field.send_keys(text)
        return field.get_attribute("value")

    def toggle_checkbox(self) -> bool:
        box = self._root().find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        box.click()
        return box.is_selected()

    def link_href(self) -> str:
        return self._root().find_element(By.CSS_SELECTOR, "a").get_attribute("href")


class Visitors(BasePage):
    COUNTER: Locator = (By.ID, "Stats1_content")

    def count_text(self) -> str:
        self.wait_until(lambda d: self.find(self.COUNTER).text.strip() != "", "Visitor counter empty")
        return self.find(self.COUNTER).text.strip()
