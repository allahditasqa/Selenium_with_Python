"""'Dynamic Web Table' section. Column order and values change on every page load,
so cells are always located by header text, never by index."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class DynamicTable(BasePage):
    HEADERS: Locator = (By.CSS_SELECTOR, "#taskTable thead th")
    ROWS: Locator = (By.CSS_SELECTOR, "#taskTable tbody tr")

    DISPLAYED = {
        ("Chrome", "CPU (%)"): ".chrome-cpu",
        ("Firefox", "Memory (MB)"): ".firefox-memory",
        ("Chrome", "Network (Mbps)"): ".chrome-network",
        ("Firefox", "Disk (MB/s)"): ".firefox-disk",
    }

    def headers(self) -> list[str]:
        return self.texts(self.HEADERS)

    def processes(self) -> list[str]:
        return [row.find_elements(By.TAG_NAME, "td")[0].text.strip() for row in self.find_all(self.ROWS)]

    def snapshot(self) -> dict[str, dict[str, str]]:
        """{process: {column header: value}} read in one pass."""
        headers = self.headers()
        result: dict[str, dict[str, str]] = {}
        for row in self.find_all(self.ROWS):
            cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
            result[cells[0]] = dict(zip(headers, cells, strict=True))
        return result

    def value(self, process: str, column: str) -> str:
        return self.snapshot()[process][column]

    def displayed_value(self, process: str, column: str) -> str:
        """The value printed below the table, e.g. 'CPU load of Chrome process'."""
        css = self.DISPLAYED[(process, column)]
        return self.text((By.CSS_SELECTOR, f"#displayValues {css}"))
