# Hidden Elements And AJAX Test Cases

**Automation:** `tests/ui/test_08_hidden_elements_ajax.py`  |  **Report:** `reports/hidden-elements-and-ajax/Hidden Elements And AJAX test <DD-MM-YYYY>_<HH-mm-ss>.html` (all reports: `reports/index.html`)
**Application:** https://testautomationpractice.blogspot.com/  |  **ID prefix:** `TC_HIDDEN_`  |  **Master CSV:** `docs/test-cases/hidden-elements-and-ajax.csv`

## Overview
The 'Hidden Elements & AJAX' page: buttons that show and hide input fields and checkboxes, and a button that loads content after a delay (AJAX).

## Scope and notes
- Waits are explicit; the AJAX content is awaited, never slept for.

## A. Hidden elements

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_HIDDEN_01 | Open the page and check the status is "Ready" and only Input Box 1 is visible. | P2 - High | UI | Browser is open on the 'Hidden Elements & AJAX' page of the practice site | - | 1. Open the Hidden Elements & AJAX page.<br>2. Read the status.<br>3. Check Input Box 1, Input Box 2 and Checkbox 2. | The status is "Ready", Input Box 1 is visible, Input Box 2 and Checkbox 2 are hidden. | Automated `test_08_hidden_elements_ajax.py::TestHiddenElements::test_tc_hidden_01_initial_state` |
| TC_HIDDEN_02 | Toggle Input Box 2 twice and check the status "Input Box 2 shown" then "Input Box 2 hidden". | P2 - High | Functional | Browser is open on the 'Hidden Elements & AJAX' page of the practice site | - | 1. Click the toggle button of Input Box 2.<br>2. Check the box and the status.<br>3. Click the toggle button again.<br>4. Check the box and the status. | After step 2 the box is visible and the status is "Input Box 2 shown". After step 4 it is hidden and the status is "Input Box 2 hidden". | Automated `test_08_hidden_elements_ajax.py::TestHiddenElements::test_tc_hidden_02_toggle_input_box_2` |
| TC_HIDDEN_03 | Toggle Checkbox 2 twice and check it is shown and hidden again. | P3 - Medium | Functional | Browser is open on the 'Hidden Elements & AJAX' page of the practice site | - | 1. Click the toggle button of Checkbox 2.<br>2. Check the checkbox and the status.<br>3. Click the toggle button again.<br>4. Check the checkbox. | After step 2 the checkbox is visible and the status is "Checkbox 2 shown". After step 4 it is hidden. | Automated `test_08_hidden_elements_ajax.py::TestHiddenElements::test_tc_hidden_03_toggle_checkbox_2` |
| TC_HIDDEN_04 | Show Input Box 2, type "now visible" and check the text is kept. | P3 - Medium | Functional | Browser is open on the 'Hidden Elements & AJAX' page of the practice site | "now visible" | 1. Click the toggle button of Input Box 2.<br>2. Type "now visible" in Input Box 2.<br>3. Read its value. | Input Box 2 holds "now visible". | Automated `test_08_hidden_elements_ajax.py::TestHiddenElements::test_tc_hidden_04_revealed_input_accepts_text` |

## B. AJAX

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_HIDDEN_05 | Click the AJAX load button and check the content "AJAX Content Loaded" appears after the delay. | P2 - High | Functional | Browser is open on the 'Hidden Elements & AJAX' page of the practice site | - | 1. Click the load AJAX content button.<br>2. Wait for the content. | The content contains "AJAX Content Loaded" and "This is some dynamic content loaded through AJAX.". | Automated `test_08_hidden_elements_ajax.py::TestAjax::test_tc_hidden_05_ajax_content_appears_after_delay` |
| TC_HIDDEN_06 | Load the AJAX content and check the status label shows "AJAX content loaded". | P3 - Medium | Functional | Browser is open on the 'Hidden Elements & AJAX' page of the practice site | - | 1. Click the load AJAX content button.<br>2. Wait for the content.<br>3. Read the status. | The status shows "AJAX content loaded". | Automated `test_08_hidden_elements_ajax.py::TestAjax::test_tc_hidden_06_status_label_after_ajax` |

## Summary

| Group | Cases | Automated |
| --- | --- | --- |
| A. Hidden elements | 4 | 4 |
| B. AJAX | 2 | 2 |
| **Total** | **6** | **6** |
