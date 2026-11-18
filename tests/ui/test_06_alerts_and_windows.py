"""Alerts, prompts, new tab, popup windows and the Wikipedia 'Tabs' widget."""

import pytest


@pytest.mark.regression
class TestJavaScriptAlerts:
    def test_tc_alert_01_simple_alert_text(self, home):
        """TC_ALERT_01 - Click "Simple Alert" and check the alert text is "I am an alert box!"."""
        assert home.alerts.simple_alert() == "I am an alert box!"

    def test_tc_alert_02_confirm_accept(self, home):
        """TC_ALERT_02 - Click "Confirmation Alert", press OK and check the page shows "You pressed OK!"."""
        assert home.alerts.confirm(accept=True) == "You pressed OK!"

    def test_tc_alert_03_confirm_dismiss(self, home):
        """TC_ALERT_03 - Click "Confirmation Alert", press Cancel and check the page shows "You pressed Cancel!"."""
        assert home.alerts.confirm(accept=False) == "You pressed Cancel!"

    def test_tc_alert_04_prompt_message(self, home):
        """TC_ALERT_04 - Click "Prompt Alert" and check the prompt asks "Please enter your name:"."""
        assert home.alerts.prompt_text() == "Please enter your name:"

    def test_tc_alert_05_prompt_accept_with_name(self, home):
        """TC_ALERT_05 - Enter the name "Allah" in the prompt, press OK and check the greeting "Hello Allah! How are you today?"."""
        assert home.alerts.prompt("Allah") == "Hello Allah! How are you today?"

    def test_tc_alert_06_prompt_dismiss(self, home):
        """TC_ALERT_06 - Click "Prompt Alert", press Cancel and check the page shows "User cancelled the prompt."."""
        assert home.alerts.prompt(None) == "User cancelled the prompt."


@pytest.mark.regression
@pytest.mark.external
class TestNewWindows:
    def test_tc_alert_07_new_tab_button_opens_pavan_blog(self, home):
        """TC_ALERT_07 - Click "New Tab" and check a second tab opens with pavantestingtools.com."""
        main = home.driver.current_window_handle
        home.alerts.open_new_tab()
        home.wait_for_window_count(2)
        home.switch_to_window_with_url("pavantestingtools.com")
        assert "pavantestingtools.com" in home.current_url()
        home.close_other_windows(main)
        assert home.heading_text() == "Automation Testing Practice"

    def test_tc_alert_08_popup_button_opens_two_windows(self, home):
        """TC_ALERT_08 - Click "Popup Windows" and check two windows open (selenium.dev and playwright.dev)."""
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
    def test_tc_alert_09_search_returns_results(self, home):
        """TC_ALERT_09 - Search Wikipedia for "Selenium" and check "Selenium" and "Selenium (software)" are listed."""
        results = home.wikipedia.search("Selenium")
        assert "Selenium" in results
        assert "Selenium (software)" in results

    def test_tc_alert_10_result_links_open_in_new_tab(self, home):
        """TC_ALERT_10 - Search Wikipedia for "Selenium" and check the result links open in a new tab."""
        home.wikipedia.search("Selenium")
        assert home.wikipedia.result_target() == "_blank"

    def test_tc_alert_11_open_result_in_new_tab(self, home):
        """TC_ALERT_11 - Open the result "Selenium (software)" and check the Wikipedia page opens in a new tab."""
        main = home.driver.current_window_handle
        home.wikipedia.search("Selenium")
        home.wikipedia.open_result("Selenium (software)")
        home.wait_for_window_count(2)
        home.switch_to_window_with_url("wikipedia.org/wiki/Selenium_(software)")
        assert "Selenium" in home.title()
        home.close_other_windows(main)

    def test_tc_alert_12_more_link_opens_full_search(self, home):
        """TC_ALERT_12 - Search for "Python", click "More" and check the full Wikipedia search opens in a new tab."""
        main = home.driver.current_window_handle
        home.wikipedia.search("Python")
        home.wikipedia.open_more()
        home.wait_for_window_count(2)
        home.switch_to_window_with_url("search=Python")
        assert "Python" in home.current_url()
        home.close_other_windows(main)
