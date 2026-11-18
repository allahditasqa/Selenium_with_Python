"""'Pagination Web Table' section (products, 5 rows per page)."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class PaginationTable(BasePage):
    ROWS: Locator = (By.CSS_SELECTOR, "#productTable tbody tr")
    PAGES: Locator = (By.CSS_SELECTOR, "#pagination li a")

    @staticmethod
    def _page_link(number: int) -> Locator:
        return (By.XPATH, f"//ul[@id='pagination']//a[normalize-space()='{number}']")

    def page_count(self) -> int:
        return self.count(self.PAGES)

    def go_to_page(self, number: int) -> None:
        self.click(self._page_link(number))
        self.wait_until(
            lambda d: "active" in (self.attribute(self._page_link(number), "class") or ""),
            f"Page {number} did not become active",
        )

    def active_page(self) -> int:
        active = self.find((By.CSS_SELECTOR, "#pagination a.active"))
        return int(active.text)

    def rows(self) -> list[dict[str, str]]:
        data = []
        for row in self.find_all(self.ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            data.append(
                {"id": cells[0].text.strip(), "name": cells[1].text.strip(), "price": cells[2].text.strip()}
            )
        return data

    def select_product(self, name: str) -> None:
        checkbox = (
            By.XPATH,
            f"//table[@id='productTable']//tr[td[normalize-space()='{name}']]//input[@type='checkbox']",
        )
        if not self.is_selected(checkbox):
            self.click(checkbox)

    def is_product_selected(self, name: str) -> bool:
        checkbox = (
            By.XPATH,
            f"//table[@id='productTable']//tr[td[normalize-space()='{name}']]//input[@type='checkbox']",
        )
        return self.is_selected(checkbox)

    def all_rows(self) -> list[dict[str, str]]:
        """Walk through every page and collect all rows."""
        collected: list[dict[str, str]] = []
        for number in range(1, self.page_count() + 1):
            self.go_to_page(number)
            collected.extend(self.rows())
        return collected
