# Alerts And Windows Test Cases

**Automation:** `tests/ui/test_06_alerts_and_windows.py`  |  **Report:** `reports/alerts-and-windows/Alerts And Windows test <DD-MM-YYYY>_<HH-mm-ss>.html` (all reports: `reports/index.html`)
**Application:** https://testautomationpractice.blogspot.com/  |  **ID prefix:** `TC_ALERT_`  |  **Master CSV:** `docs/test-cases/alerts-and-windows.csv`

## Overview
JavaScript alerts, confirm and prompt boxes, the buttons that open new tabs or popup windows, and the Wikipedia search widget (Tabs section).

## Scope and notes
- New window and Wikipedia cases need internet access to third-party sites and are marked `external`; CI skips them (`-m "not external"`).
- The browser must close every extra window at the end of each case.

## A. JavaScript alerts

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_ALERT_01 | Click "Simple Alert" and check the alert text is "I am an alert box!". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click Simple Alert.<br>2. Read the alert text.<br>3. Accept the alert. | The alert text is "I am an alert box!". | Automated `test_06_alerts_and_windows.py::TestJavaScriptAlerts::test_tc_alert_01_simple_alert_text` |
| TC_ALERT_02 | Click "Confirmation Alert", press OK and check the page shows "You pressed OK!". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click Confirmation Alert.<br>2. Accept the alert.<br>3. Read the result text. | The result is "You pressed OK!". | Automated `test_06_alerts_and_windows.py::TestJavaScriptAlerts::test_tc_alert_02_confirm_accept` |
| TC_ALERT_03 | Click "Confirmation Alert", press Cancel and check the page shows "You pressed Cancel!". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click Confirmation Alert.<br>2. Dismiss the alert.<br>3. Read the result text. | The result is "You pressed Cancel!". | Automated `test_06_alerts_and_windows.py::TestJavaScriptAlerts::test_tc_alert_03_confirm_dismiss` |
| TC_ALERT_04 | Click "Prompt Alert" and check the prompt asks "Please enter your name:". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click Prompt Alert.<br>2. Read the prompt text.<br>3. Dismiss the prompt. | The prompt text is "Please enter your name:". | Automated `test_06_alerts_and_windows.py::TestJavaScriptAlerts::test_tc_alert_04_prompt_message` |
| TC_ALERT_05 | Enter the name "Allah" in the prompt, press OK and check the greeting "Hello Allah! How are you today?". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Name: "Allah" | 1. Click Prompt Alert.<br>2. Type the name in the prompt.<br>3. Accept the prompt.<br>4. Read the result text. | The result is "Hello Allah! How are you today?". | Automated `test_06_alerts_and_windows.py::TestJavaScriptAlerts::test_tc_alert_05_prompt_accept_with_name` |
| TC_ALERT_06 | Click "Prompt Alert", press Cancel and check the page shows "User cancelled the prompt.". | P3 - Medium | Negative | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click Prompt Alert.<br>2. Dismiss the prompt.<br>3. Read the result text. | The result is "User cancelled the prompt.". | Automated `test_06_alerts_and_windows.py::TestJavaScriptAlerts::test_tc_alert_06_prompt_dismiss` |

## B. New tab and popup windows

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_ALERT_07 | Click "New Tab" and check a second tab opens with pavantestingtools.com. | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click the New Tab button.<br>2. Wait for a second window.<br>3. Switch to the window with pavantestingtools.com.<br>4. Close the new window.<br>5. Read the heading of the first window. | A new tab with pavantestingtools.com opens. After closing it, the practice page heading is still shown. | Automated `test_06_alerts_and_windows.py::TestNewWindows::test_tc_alert_07_new_tab_button_opens_pavan_blog` |
| TC_ALERT_08 | Click "Popup Windows" and check two windows open (selenium.dev and playwright.dev). | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click the Popup Windows button.<br>2. Wait for 3 windows in total.<br>3. Switch to the selenium.dev window.<br>4. Switch to the playwright.dev window.<br>5. Close the extra windows. | Two popup windows open (selenium.dev and playwright.dev); after closing them one window is left. | Automated `test_06_alerts_and_windows.py::TestNewWindows::test_tc_alert_08_popup_button_opens_two_windows` |

## C. Wikipedia tabs widget

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_ALERT_09 | Search Wikipedia for "Selenium" and check "Selenium" and "Selenium (software)" are listed. | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Search: "Selenium" | 1. Type the search text in the Wikipedia box.<br>2. Click Search.<br>3. Read the result list. | The results contain "Selenium" and "Selenium (software)". | Automated `test_06_alerts_and_windows.py::TestWikipediaTabs::test_tc_alert_09_search_returns_results` |
| TC_ALERT_10 | Search Wikipedia for "Selenium" and check the result links open in a new tab. | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Search: "Selenium" | 1. Search for Selenium.<br>2. Read the target attribute of a result link. | The link target is "_blank". | Automated `test_06_alerts_and_windows.py::TestWikipediaTabs::test_tc_alert_10_result_links_open_in_new_tab` |
| TC_ALERT_11 | Open the result "Selenium (software)" and check the Wikipedia page opens in a new tab. | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Search: "Selenium" | 1. Search for Selenium.<br>2. Click the result "Selenium (software)".<br>3. Switch to the new window.<br>4. Read the page title.<br>5. Close the new window. | A new tab with wikipedia.org/wiki/Selenium_(software) opens and its title contains "Selenium". | Automated `test_06_alerts_and_windows.py::TestWikipediaTabs::test_tc_alert_11_open_result_in_new_tab` |
| TC_ALERT_12 | Search for "Python", click "More" and check the full Wikipedia search opens in a new tab. | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Search: "Python" | 1. Search for Python.<br>2. Click the More link.<br>3. Switch to the new window.<br>4. Read the URL.<br>5. Close the new window. | A new tab with the Wikipedia search "search=Python" opens. | Automated `test_06_alerts_and_windows.py::TestWikipediaTabs::test_tc_alert_12_more_link_opens_full_search` |

## Summary

| Group | Cases | Automated |
| --- | --- | --- |
| A. JavaScript alerts | 6 | 6 |
| B. New tab and popup windows | 2 | 2 |
| C. Wikipedia tabs widget | 4 | 4 |
| **Total** | **12** | **12** |
