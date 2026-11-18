"""Main page of the practice site. Each section of the page is a component object."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Settings
from core.base_page import BasePage
from pages.components.data_entry_form import DataEntryForm
from pages.components.dynamic_table import DynamicTable
from pages.components.links_and_sections import (
    FooterLinks,
    FormSections,
    LabelsAndLinks,
    ShadowDom,
    Visitors,
)
from pages.components.pagination_table import PaginationTable
from pages.components.static_table import StaticTable
from pages.components.upload_files import UploadFiles
from pages.components.widgets import (
    AlertsAndPopups,
    DoubleClick,
    DragAndDrop,
    DynamicButton,
    MouseHover,
    ScrollingDropdown,
    Slider,
    SvgShapes,
)
from pages.components.wikipedia_tabs import WikipediaTabs


class HomePage(BasePage):
    HEADING = (By.CSS_SELECTOR, "h1")
    SECTION_TITLES = (By.CSS_SELECTOR, "h2.title, .widget > h2, h3")

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        super().__init__(driver, settings.explicit_timeout)
        self.settings = settings
        t = settings.explicit_timeout
        self.form = DataEntryForm(driver, t)
        self.upload = UploadFiles(driver, t)
        self.static_table = StaticTable(driver, t)
        self.dynamic_table = DynamicTable(driver, t)
        self.pagination = PaginationTable(driver, t)
        self.wikipedia = WikipediaTabs(driver, t)
        self.dynamic_button = DynamicButton(driver, t)
        self.alerts = AlertsAndPopups(driver, t)
        self.hover = MouseHover(driver, t)
        self.double_click_section = DoubleClick(driver, t)
        self.drag_drop = DragAndDrop(driver, t)
        self.slider = Slider(driver, t)
        self.svg = SvgShapes(driver, t)
        self.scroll_dropdown = ScrollingDropdown(driver, t)
        self.labels_links = LabelsAndLinks(driver, t)
        self.visitors = Visitors(driver, t)
        self.sections = FormSections(driver, t)
        self.footer = FooterLinks(driver, t)
        self.shadow = ShadowDom(driver, t)

    def open(self) -> HomePage:
        self.log.info("open %s", self.settings.base_url)
        self.driver.get(self.settings.base_url + "/")
        self.visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.text(self.HEADING)

    def section_titles(self) -> list[str]:
        return [
            t
            for t in (e.get_attribute("textContent").strip() for e in self.find_all(self.SECTION_TITLES))
            if t
        ]
