"""Dynamic button, mouse hover, double click, drag and drop, slider, SVG, scrolling dropdown."""

import pytest
from selenium.webdriver.common.keys import Keys

from tests.ids import tc_ids


@pytest.mark.regression
class TestDynamicButton:
    def test_tc_widget_01_starts_as_start(self, home):
        """TC_WIDGET_01 - Open the page and check the dynamic button shows "START"."""
        assert home.dynamic_button.label() == "START"
        assert home.dynamic_button.name_attribute() == "start"
        assert "start" in home.dynamic_button.css_classes()

    def test_tc_widget_02_click_toggles_to_stop_and_back(self, home):
        """TC_WIDGET_02 - Click the dynamic button twice and check it changes to "STOP" and back to "START"."""
        home.dynamic_button.click_button()
        assert home.dynamic_button.label() == "STOP"
        assert home.dynamic_button.name_attribute() == "stop"
        assert "stop" in home.dynamic_button.css_classes()
        home.dynamic_button.click_button()
        assert home.dynamic_button.label() == "START"
        assert "start" in home.dynamic_button.css_classes()


@pytest.mark.regression
class TestMouseHover:
    def test_tc_widget_03_menu_hidden_before_hover(self, home):
        """TC_WIDGET_03 - Open the page and check the hover menu is hidden before the mouse is moved over the button."""
        assert not home.hover.menu_visible()

    def test_tc_widget_04_menu_opens_on_hover(self, home):
        """TC_WIDGET_04 - Move the mouse over "Point Me" and check the menu shows "Mobiles" and "Laptops"."""
        assert home.hover.hover_menu() == ["Mobiles", "Laptops"]


@pytest.mark.regression
class TestDoubleClick:
    def test_tc_widget_05_default_source_text(self, home):
        """TC_WIDGET_05 - Open the Double Click section and check the first field contains "Hello World!"."""
        assert home.double_click_section.value(home.double_click_section.FIELD_1) == "Hello World!"

    def test_tc_widget_06_double_click_copies_text(self, home):
        """TC_WIDGET_06 - Double click "Copy Text" and check "Hello World!" is copied to the second field."""
        home.double_click_section.double_click_copy()
        assert home.double_click_section.target_value() == "Hello World!"

    def test_tc_widget_07_double_click_copies_custom_text(self, home):
        """TC_WIDGET_07 - Type "Selenium with Python" in the first field, double click "Copy Text" and check the text is copied."""
        home.double_click_section.set_source("Selenium with Python")
        home.double_click_section.double_click_copy()
        assert home.double_click_section.target_value() == "Selenium with Python"

    def test_tc_widget_08_single_click_does_not_copy(self, home):
        """TC_WIDGET_08 - Click "Copy Text" only once and check nothing is copied."""
        home.double_click_section.single_click_copy()
        assert home.double_click_section.target_value() == ""


@pytest.mark.regression
class TestDragAndDrop:
    def test_tc_widget_09_target_before_drop(self, home):
        """TC_WIDGET_09 - Open the Drag and Drop section and check the target shows "Drop here"."""
        assert home.drag_drop.target_text() == "Drop here"
        assert not home.drag_drop.target_highlighted()

    def test_tc_widget_10_drag_source_onto_target(self, home):
        """TC_WIDGET_10 - Drag the source box onto the target and check the target shows "Dropped!"."""
        home.drag_drop.drag_to_target()
        assert home.drag_drop.target_text() == "Dropped!"
        assert home.drag_drop.target_highlighted()


@pytest.mark.regression
class TestSlider:
    def test_tc_widget_11_default_range(self, home):
        """TC_WIDGET_11 - Open the Slider section and check the default range is 75 to 300."""
        assert home.slider.range() == (75, 300)

    def test_tc_widget_12_min_handle_moves_with_keyboard(self, home):
        """TC_WIDGET_12 - Press the Right arrow 3 times on the minimum handle and check the range becomes 78 to 300."""
        home.slider.nudge_min(3, Keys.ARROW_RIGHT)
        assert home.slider.range() == (78, 300)

    def test_tc_widget_13_max_handle_moves_with_keyboard(self, home):
        """TC_WIDGET_13 - Press the Left arrow 5 times on the maximum handle and check the range becomes 75 to 295."""
        home.slider.nudge_max(5, Keys.ARROW_LEFT)
        assert home.slider.range() == (75, 295)

    def test_tc_widget_14_max_handle_moves_with_mouse_drag(self, home):
        """TC_WIDGET_14 - Drag the maximum handle 60 pixels to the left and check the upper value gets smaller."""
        home.slider.drag_max_handle(-60)
        low, high = home.slider.range()
        assert low == 75
        assert high < 300


@pytest.mark.regression
class TestSvgElements:
    def test_tc_widget_15_three_svg_shapes(self, home):
        """TC_WIDGET_15 - Open the SVG Elements section and check it has 3 SVG shapes."""
        assert home.svg.svg_count() == 3

    @pytest.mark.parametrize(
        ("shape", "color"),
        [("circle", "red"), ("rect", "green"), ("polygon", "blue")],
        ids=tc_ids("TC_WIDGET_16", 3),
    )
    def test_tc_widget_16_shape_is_visible_with_expected_color(self, home, shape, color):
        """TC_WIDGET_16 - Check the SVG {shape} is visible and filled with the color "{color}"."""
        assert home.svg.shape_visible(shape)
        assert home.svg.fill(shape) == color


@pytest.mark.regression
class TestScrollingDropdown:
    def test_tc_widget_17_has_100_options(self, home):
        """TC_WIDGET_17 - Open the Scrolling DropDown and check it has 100 options."""
        home.scroll_dropdown.open()
        assert home.scroll_dropdown.option_count() == 100

    @pytest.mark.parametrize("item", ["Item 1", "Item 50", "Item 100"], ids=tc_ids("TC_WIDGET_18", 3))
    def test_tc_widget_18_select_item_after_scrolling(self, home, item):
        """TC_WIDGET_18 - Scroll the Scrolling DropDown and select "{item}"."""
        assert home.scroll_dropdown.choose(item) == item
