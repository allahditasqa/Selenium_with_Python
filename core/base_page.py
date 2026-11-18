"""BasePage: every page object and component inherits from this class.

It wraps raw Selenium calls with explicit waits, logging and small helpers, so page objects and tests
never use time.sleep() or call WebDriver directly.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from core.logger import get_logger

Locator = tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(
            driver, timeout, poll_frequency=0.25, ignored_exceptions=(StaleElementReferenceException,)
        )
        self.log = get_logger(type(self).__name__)

    # ------------------------------------------------------------------ finding
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator), f"Not present: {locator}")

    def find_all(self, locator: Locator) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    def visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator), f"Not visible: {locator}")

    def clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator), f"Not clickable: {locator}")

    # ------------------------------------------------------------------ actions
    def click(self, locator: Locator) -> None:
        self.log.info("click %s", locator)
        element = self.clickable(locator)
        self.scroll_to(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.log.warning("click intercepted, falling back to JS click for %s", locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        self.log.info("type %r into %s", text, locator)
        element = self.visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def press(self, locator: Locator, *keys: str) -> None:
        self.visible(locator).send_keys(*keys)

    def select_by_text(self, locator: Locator, text: str) -> None:
        Select(self.visible(locator)).select_by_visible_text(text)

    def hover(self, locator: Locator) -> None:
        ActionChains(self.driver).move_to_element(self.visible(locator)).perform()

    def double_click(self, locator: Locator) -> None:
        ActionChains(self.driver).double_click(self.visible(locator)).perform()

    def scroll_to(self, target: Locator | WebElement) -> WebElement:
        element = target if isinstance(target, WebElement) else self.find(target)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def clear_with_keyboard(self, locator: Locator) -> None:
        element = self.visible(locator)
        element.send_keys(Keys.CONTROL, "a", Keys.DELETE)

    def set_value_js(self, locator: Locator, value: str) -> None:
        """Set .value through JavaScript - needed for <input type=date> which is locale dependent."""
        self.driver.execute_script("arguments[0].value = arguments[1];", self.find(locator), value)

    # ------------------------------------------------------------------ reading
    def text(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()

    def texts(self, locator: Locator) -> list[str]:
        return [e.text.strip() for e in self.find_all(locator)]

    def value(self, locator: Locator) -> str:
        return self.find(locator).get_attribute("value") or ""

    def attribute(self, locator: Locator, name: str) -> str | None:
        return self.find(locator).get_attribute(name)

    def is_displayed(self, locator: Locator) -> bool:
        elements = self.find_all(locator)
        return bool(elements) and elements[0].is_displayed()

    def is_selected(self, locator: Locator) -> bool:
        return self.find(locator).is_selected()

    def count(self, locator: Locator) -> int:
        return len(self.find_all(locator))

    # ------------------------------------------------------------------ waiting
    def wait_until(self, condition: Callable[[WebDriver], Any], message: str = "") -> Any:
        return self.wait.until(condition, message)

    def wait_for_text(self, locator: Locator, expected: str) -> None:
        self.wait.until(
            EC.text_to_be_present_in_element(locator, expected), f"{locator} never showed {expected!r}"
        )

    def wait_for_value(self, locator: Locator, expected: str) -> None:
        self.wait.until(
            EC.text_to_be_present_in_element_value(locator, expected),
            f"{locator} never had value {expected!r}",
        )

    def wait_invisible(self, locator: Locator) -> None:
        self.wait.until(EC.invisibility_of_element_located(locator), f"Still visible: {locator}")

    # ------------------------------------------------------------------ alerts
    def alert_text(self) -> str:
        return self.wait.until(EC.alert_is_present(), "No alert appeared").text

    def accept_alert(self, prompt_text: str | None = None) -> str:
        alert = self.wait.until(EC.alert_is_present(), "No alert appeared")
        text = alert.text
        if prompt_text is not None:
            alert.send_keys(prompt_text)
        alert.accept()
        return text

    def dismiss_alert(self) -> str:
        alert = self.wait.until(EC.alert_is_present(), "No alert appeared")
        text = alert.text
        alert.dismiss()
        return text

    # ------------------------------------------------------------------ windows
    def wait_for_window_count(self, count: int) -> None:
        self.wait.until(EC.number_of_windows_to_be(count), f"Expected {count} windows")

    def switch_to_window_with_url(self, fragment: str) -> None:
        """Switch to the window whose URL contains the fragment (waits until it loads)."""

        def _switch(driver: WebDriver) -> bool:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if fragment in driver.current_url:
                    return True
            return False

        self.wait.until(_switch, f"No window with URL containing {fragment!r}")

    def close_other_windows(self, keep_handle: str) -> None:
        for handle in list(self.driver.window_handles):
            if handle != keep_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(keep_handle)

    def open_url(self, url: str, ready: Locator, attempts: int = 3) -> None:
        """Open a URL and wait for a 'page is ready' element. Reloads and retries when a shared public
        site is slow or throttles us (common on cloud CI runners)."""
        for attempt in range(1, attempts + 1):
            self.driver.get(url)
            try:
                self.visible(ready)
                return
            except TimeoutException:
                self.log.warning("attempt %s/%s: %s not ready at %s", attempt, attempts, ready, url)
                if attempt == attempts:
                    raise

    # ------------------------------------------------------------------ page level
    def title(self) -> str:
        return self.driver.title

    def current_url(self) -> str:
        return self.driver.current_url
