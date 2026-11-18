"""Alerts, prompts, new tab, popup windows and the Wikipedia 'Tabs' widget."""

import pytest


@pytest.mark.regression
class TestJavaScriptAlerts:
    def test_simple_alert_text(self, home):
        assert home.alerts.simple_alert() == "I am an alert box!"

    def test_confirm_accept(self, home):
        assert home.alerts.confirm(accept=True) == "You pressed OK!"

    def test_confirm_dismiss(self, home):
        assert home.alerts.confirm(accept=False) == "You pressed Cancel!"

    def test_prompt_message(self, home):
        assert home.alerts.prompt_text() == "Please enter your name:"

    def test_prompt_accept_with_name(self, home):
        assert home.alerts.prompt("Allah") == "Hello Allah! How are you today?"

    def test_prompt_dismiss(self, home):
        assert home.alerts.prompt(None) == "User cancelled the prompt."


@pytest.mark.regression
@pytest.mark.external
class TestNewWindows:
    def test_new_tab_button_opens_pavan_blog(self, home):
        main = home.driver.current_window_handle
        home.alerts.open_new_tab()
        home.wait_for_window_count(2)
        home.switch_to_window_with_url("pavantestingtools.com")
        assert "pavantestingtools.com" in home.current_url()
        home.close_other_windows(main)
        assert home.heading_text() == "Automation Testing Practice"

    def test_popup_button_opens_two_windows(self, home):
        main = home.driver.current_window_handle
        home.alerts.open_popup_windows()
        home.wait_for_window_count(3)
        home.switch_to_window_with_url("selenium.dev")
        assert "selenium.dev" in home.current_url()
        home.switch_to_window_with_url("playwright.dev")
        assert "playwright.dev" in home.current_url()
        home.close_other_windows(main)
        assert len(home.driver.window_handles) == 1


@pytest.mark.regression
@pytest.mark.external
class TestWikipediaTabs:
    def test_search_returns_results(self, home):
        results = home.wikipedia.search("Selenium")
        assert "Selenium" in results
        assert "Selenium (software)" in results

    def test_result_links_open_in_new_tab(self, home):
        home.wikipedia.search("Selenium")
        assert home.wikipedia.result_target() == "_blank"

    def test_open_result_in_new_tab(self, home):
        main = home.driver.current_window_handle
        home.wikipedia.search("Selenium")
        home.wikipedia.open_result("Selenium (software)")
        home.wait_for_window_count(2)
        home.switch_to_window_with_url("wikipedia.org/wiki/Selenium_(software)")
        assert "Selenium" in home.title()
        home.close_other_windows(main)

    def test_more_link_opens_full_search(self, home):
        main = home.driver.current_window_handle
        home.wikipedia.search("Python")
        home.wikipedia.open_more()
        home.wait_for_window_count(2)
        home.switch_to_window_with_url("search=Python")
        assert "Python" in home.current_url()
        home.close_other_windows(main)
