# Widgets Test Cases

**Automation:** `tests/ui/test_05_widgets.py`  |  **Report:** `reports/widgets/Widgets test <DD-MM-YYYY>_<HH-mm-ss>.html` (all reports: `reports/index.html`)
**Application:** https://testautomationpractice.blogspot.com/  |  **ID prefix:** `TC_WIDGET_`  |  **Master CSV:** `docs/test-cases/widgets.csv`

## Overview
Small interactive widgets of the home page: dynamic START/STOP button, mouse hover menu, double click copy, drag and drop, range slider, SVG shapes and a scrolling dropdown.

## Scope and notes
- The slider is checked with the keyboard (exact) and with the mouse (relative, the exact pixel to value ratio is not fixed).
- The scrolling dropdown holds 100 items (Item 1 to Item 100).

## A. Dynamic button

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_01 | Open the page and check the dynamic button shows "START". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Scroll to the dynamic button.<br>2. Read its label, name and class. | The label is "START", the name is "start" and the class contains "start". | Automated `test_05_widgets.py::TestDynamicButton::test_tc_widget_01_starts_as_start` |
| TC_WIDGET_02 | Click the dynamic button twice and check it changes to "STOP" and back to "START". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click the button.<br>2. Read label, name and class.<br>3. Click the button again.<br>4. Read label and class. | After the first click it is "STOP" (name "stop"). After the second click it is "START" again. | Automated `test_05_widgets.py::TestDynamicButton::test_tc_widget_02_click_toggles_to_stop_and_back` |

## B. Mouse hover

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_03 | Open the page and check the hover menu is hidden before the mouse is moved over the button. | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Scroll to Mouse Hover.<br>2. Check the dropdown menu. | The menu is not visible. | Automated `test_05_widgets.py::TestMouseHover::test_tc_widget_03_menu_hidden_before_hover` |
| TC_WIDGET_04 | Move the mouse over "Point Me" and check the menu shows "Mobiles" and "Laptops". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Move the mouse over the Point Me button.<br>2. Read the menu items. | The menu shows "Mobiles" and "Laptops". | Automated `test_05_widgets.py::TestMouseHover::test_tc_widget_04_menu_opens_on_hover` |

## C. Double click

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_05 | Open the Double Click section and check the first field contains "Hello World!". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Scroll to the Double Click section.<br>2. Read the first field. | The first field holds "Hello World!". | Automated `test_05_widgets.py::TestDoubleClick::test_tc_widget_05_default_source_text` |
| TC_WIDGET_06 | Double click "Copy Text" and check "Hello World!" is copied to the second field. | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | "Hello World!" | 1. Double click the Copy Text button.<br>2. Read the second field. | The second field holds "Hello World!". | Automated `test_05_widgets.py::TestDoubleClick::test_tc_widget_06_double_click_copies_text` |
| TC_WIDGET_07 | Type "Selenium with Python" in the first field, double click "Copy Text" and check the text is copied. | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | "Selenium with Python" | 1. Replace the text of the first field.<br>2. Double click the Copy Text button.<br>3. Read the second field. | The second field holds "Selenium with Python". | Automated `test_05_widgets.py::TestDoubleClick::test_tc_widget_07_double_click_copies_custom_text` |
| TC_WIDGET_08 | Click "Copy Text" only once and check nothing is copied. | P3 - Medium | Negative | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Click the Copy Text button once.<br>2. Read the second field. | The second field stays empty. | Automated `test_05_widgets.py::TestDoubleClick::test_tc_widget_08_single_click_does_not_copy` |

## D. Drag and drop

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_09 | Open the Drag and Drop section and check the target shows "Drop here". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Scroll to Drag and Drop.<br>2. Read the target text. | The target shows "Drop here" and is not highlighted. | Automated `test_05_widgets.py::TestDragAndDrop::test_tc_widget_09_target_before_drop` |
| TC_WIDGET_10 | Drag the source box onto the target and check the target shows "Dropped!". | P2 - High | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Drag the source box onto the target.<br>2. Read the target text. | The target shows "Dropped!" and is highlighted. | Automated `test_05_widgets.py::TestDragAndDrop::test_tc_widget_10_drag_source_onto_target` |

## E. Slider

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_11 | Open the Slider section and check the default range is 75 to 300. | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Scroll to the Slider.<br>2. Read the range. | The range is 75 - 300. | Automated `test_05_widgets.py::TestSlider::test_tc_widget_11_default_range` |
| TC_WIDGET_12 | Press the Right arrow 3 times on the minimum handle and check the range becomes 78 to 300. | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Right arrow x 3 | 1. Focus the minimum handle.<br>2. Press the Right arrow 3 times.<br>3. Read the range. | The range is 78 - 300. | Automated `test_05_widgets.py::TestSlider::test_tc_widget_12_min_handle_moves_with_keyboard` |
| TC_WIDGET_13 | Press the Left arrow 5 times on the maximum handle and check the range becomes 75 to 295. | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Left arrow x 5 | 1. Focus the maximum handle.<br>2. Press the Left arrow 5 times.<br>3. Read the range. | The range is 75 - 295. | Automated `test_05_widgets.py::TestSlider::test_tc_widget_13_max_handle_moves_with_keyboard` |
| TC_WIDGET_14 | Drag the maximum handle 60 pixels to the left and check the upper value gets smaller. | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Drag by -60 px | 1. Drag the maximum handle 60 pixels to the left.<br>2. Read the range. | The lower value stays 75 and the upper value is less than 300. | Automated `test_05_widgets.py::TestSlider::test_tc_widget_14_max_handle_moves_with_mouse_drag` |

## F. SVG elements

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_15 | Open the SVG Elements section and check it has 3 SVG shapes. | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Scroll to SVG Elements.<br>2. Count the SVG elements. | There are 3 SVG elements. | Automated `test_05_widgets.py::TestSvgElements::test_tc_widget_15_three_svg_shapes` |
| TC_WIDGET_16.1 | Check the SVG circle is visible and filled with the color "red". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Shape circle, color red | 1. Scroll to SVG Elements.<br>2. Find the circle shape.<br>3. Read its fill color. | The circle is visible and its fill is "red". | Automated `test_05_widgets.py::TestSvgElements::test_tc_widget_16_shape_is_visible_with_expected_color` |
| TC_WIDGET_16.2 | Check the SVG rect is visible and filled with the color "green". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Shape rect, color green | 1. Scroll to SVG Elements.<br>2. Find the rect shape.<br>3. Read its fill color. | The rect is visible and its fill is "green". | Automated `test_05_widgets.py::TestSvgElements::test_tc_widget_16_shape_is_visible_with_expected_color` |
| TC_WIDGET_16.3 | Check the SVG polygon is visible and filled with the color "blue". | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Shape polygon, color blue | 1. Scroll to SVG Elements.<br>2. Find the polygon shape.<br>3. Read its fill color. | The polygon is visible and its fill is "blue". | Automated `test_05_widgets.py::TestSvgElements::test_tc_widget_16_shape_is_visible_with_expected_color` |

## G. Scrolling dropdown

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_WIDGET_17 | Open the Scrolling DropDown and check it has 100 options. | P3 - Medium | UI | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | - | 1. Open the Scrolling DropDown.<br>2. Count the options. | There are 100 options. | Automated `test_05_widgets.py::TestScrollingDropdown::test_tc_widget_17_has_100_options` |
| TC_WIDGET_18.1 | Scroll the Scrolling DropDown and select "Item 1". | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Item: "Item 1" | 1. Open the Scrolling DropDown.<br>2. Scroll to "Item 1".<br>3. Click it.<br>4. Read the selected value. | The selected value is "Item 1". | Automated `test_05_widgets.py::TestScrollingDropdown::test_tc_widget_18_select_item_after_scrolling` |
| TC_WIDGET_18.2 | Scroll the Scrolling DropDown and select "Item 50". | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Item: "Item 50" | 1. Open the Scrolling DropDown.<br>2. Scroll to "Item 50".<br>3. Click it.<br>4. Read the selected value. | The selected value is "Item 50". | Automated `test_05_widgets.py::TestScrollingDropdown::test_tc_widget_18_select_item_after_scrolling` |
| TC_WIDGET_18.3 | Scroll the Scrolling DropDown and select "Item 100". | P3 - Medium | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | Item: "Item 100" | 1. Open the Scrolling DropDown.<br>2. Scroll to "Item 100".<br>3. Click it.<br>4. Read the selected value. | The selected value is "Item 100". | Automated `test_05_widgets.py::TestScrollingDropdown::test_tc_widget_18_select_item_after_scrolling` |

## Summary

| Group | Cases | Automated |
| --- | --- | --- |
| A. Dynamic button | 2 | 2 |
| B. Mouse hover | 2 | 2 |
| C. Double click | 4 | 4 |
| D. Drag and drop | 2 | 2 |
| E. Slider | 4 | 4 |
| F. SVG elements | 4 | 4 |
| G. Scrolling dropdown | 4 | 4 |
| **Total** | **22** | **22** |
