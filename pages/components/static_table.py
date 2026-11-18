"""'Static Web Table' section (book list)."""

from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


@dataclass(frozen=True)
class Book:
    name: str
    author: str
    subject: str
    price: int


class StaticTable(BasePage):
    HEADERS: Locator = (By.CSS_SELECTOR, "table[name='BookTable'] th")
    ROWS: Locator = (By.CSS_SELECTOR, "table[name='BookTable'] tr")

    def headers(self) -> list[str]:
        return self.texts(self.HEADERS)

    def row_count(self) -> int:
        """Rows without the header row."""
        return self.count(self.ROWS) - 1

    def books(self) -> list[Book]:
        books: list[Book] = []
        for row in self.find_all(self.ROWS)[1:]:
            cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
            books.append(Book(cells[0], cells[1], cells[2], int(cells[3])))
        return books

    def books_by_author(self, author: str) -> list[Book]:
        return [b for b in self.books() if b.author == author]

    def total_price(self, subject: str | None = None) -> int:
        return sum(b.price for b in self.books() if subject is None or b.subject.lower() == subject.lower())
