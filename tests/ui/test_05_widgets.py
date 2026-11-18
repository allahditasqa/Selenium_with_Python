"""Dynamic button, mouse hover, double click, drag and drop, slider, SVG, scrolling dropdown."""

import pytest
from selenium.webdriver.common.keys import Keys


@pytest.mark.regression
class TestDynamicButton:
    def test_starts_as_start(self, home):
        assert home.dynamic_button.label() == "START"
        assert home.dynamic_button.name_attribute() == "start"
        assert "start" in home.dynamic_button.css_classes()

    def test_click_toggles_to_stop_and_back(self, home):
        home.dynamic_button.click_button()
        assert home.dynamic_button.label() == "STOP"
        assert home.dynamic_button.name_attribute() == "stop"
        assert "stop" in home.dynamic_button.css_classes()
        home.dynamic_button.click_button()
        assert home.dynamic_button.label() == "START"
        assert "start" in home.dynamic_button.css_classes()


@pytest.mark.regression
class TestMouseHover:
    def test_menu_hidden_before_hover(self, home):
        assert not home.hover.menu_visible()

    def test_menu_opens_on_hover(self, home):
        assert home.hover.hover_menu() == ["Mobiles", "Laptops"]


@pytest.mark.regression
class TestDoubleClick:
    def test_default_source_text(self, home):
        assert home.double_click_section.value(home.double_click_section.FIELD_1) == "Hello World!"

    def test_double_click_copies_text(self, home):
        home.double_click_section.double_click_copy()
        assert home.double_click_section.target_value() == "Hello World!"

    def test_double_click_copies_custom_text(self, home):
        home.double_click_section.set_source("Selenium with Python")
        home.double_click_section.double_click_copy()
        assert home.double_click_section.target_value() == "Selenium with Python"

    def test_single_click_does_not_copy(self, home):
        home.double_click_section.single_click_copy()
        assert home.double_click_section.target_value() == ""


@pytest.mark.regression
class TestDragAndDrop:
    def test_target_before_drop(self, home):
        assert home.drag_drop.target_text() == "Drop here"
        assert not home.drag_drop.target_highlighted()

    def test_drag_source_onto_target(self, home):
        home.drag_drop.drag_to_target()
        assert home.drag_drop.target_text() == "Dropped!"
        assert home.drag_drop.target_highlighted()


@pytest.mark.regression
class TestSlider:
    def test_default_range(self, home):
        assert home.slider.range() == (75, 300)

    def test_min_handle_moves_with_keyboard(self, home):
        home.slider.nudge_min(3, Keys.ARROW_RIGHT)
        assert home.slider.range() == (78, 300)

    def test_max_handle_moves_with_keyboard(self, home):
        home.slider.nudge_max(5, Keys.ARROW_LEFT)
        assert home.slider.range() == (75, 295)

    def test_max_handle_moves_with_mouse_drag(self, home):
        home.slider.drag_max_handle(-60)
        low, high = home.slider.range()
        assert low == 75
        assert high < 300


@pytest.mark.regression
class TestSvgElements:
    def test_three_svg_shapes(self, home):
        assert home.svg.svg_count() == 3

    @pytest.mark.parametrize(("shape", "color"), [("circle", "red"), ("rect", "green"), ("polygon", "blue")])
    def test_shape_is_visible_with_expected_color(self, home, shape, color):
        assert home.svg.shape_visible(shape)
        assert home.svg.fill(shape) == color


@pytest.mark.regression
class TestScrollingDropdown:
    def test_has_100_options(self, home):
        home.scroll_dropdown.open()
        assert home.scroll_dropdown.option_count() == 100

    @pytest.mark.parametrize("item", ["Item 1", "Item 50", "Item 100"])
    def test_select_item_after_scrolling(self, home, item):
        assert home.scroll_dropdown.choose(item) == item
