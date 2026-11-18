"""'Tabs' section: Wikipedia search widget whose result links open in new browser tabs."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class WikipediaTabs(BasePage):
    INPUT: Locator = (By.ID, "Wikipedia1_wikipedia-search-input")
    BUTTON: Locator = (By.CSS_SELECTOR, ".wikipedia-search-button")
    RESULTS: Locator = (By.CSS_SELECTOR, "#Wikipedia1_wikipedia-search-results a")
    MORE: Locator = (By.CSS_SELECTOR, "#Wikipedia1_wikipedia-search-more a")

    def search(self, term: str) -> list[str]:
        self.type(self.INPUT, term)
        self.click(self.BUTTON)
        self.wait_until(lambda d: self.count(self.RESULTS) > 0, f"No Wikipedia results for {term!r}")
        return self.texts(self.RESULTS)

    def open_result(self, title: str) -> None:
        self.click(
            (By.XPATH, f"//div[@id='Wikipedia1_wikipedia-search-results']//a[normalize-space()='{title}']")
        )

    def result_target(self, index: int = 0) -> str | None:
        return self.find_all(self.RESULTS)[index].get_attribute("target")

    def open_more(self) -> None:
        self.click(self.MORE)
