"""'Hidden Elements & AJAX' page."""

import pytest


@pytest.mark.regression
class TestHiddenElements:
    def test_tc_hidden_01_initial_state(self, hidden_page):
        """TC_HIDDEN_01 - Open the page and check the status is "Ready" and only Input Box 1 is visible."""
        assert hidden_page.status() == "Ready"
        assert hidden_page.is_displayed(hidden_page.INPUT_1)
        assert not hidden_page.is_displayed(hidden_page.INPUT_2)
        assert not hidden_page.is_displayed(hidden_page.CHECKBOX_2)

    def test_tc_hidden_02_toggle_input_box_2(self, hidden_page):
        """TC_HIDDEN_02 - Toggle Input Box 2 twice and check the status "Input Box 2 shown" then "Input Box 2 hidden"."""
        hidden_page.toggle_input_2()
        assert hidden_page.is_displayed(hidden_page.INPUT_2)
        assert hidden_page.status() == "Input Box 2 shown"
        hidden_page.toggle_input_2()
        assert not hidden_page.is_displayed(hidden_page.INPUT_2)
        assert hidden_page.status() == "Input Box 2 hidden"

    def test_tc_hidden_03_toggle_checkbox_2(self, hidden_page):
        """TC_HIDDEN_03 - Toggle Checkbox 2 twice and check it is shown and hidden again."""
        hidden_page.toggle_checkbox_2()
        assert hidden_page.is_displayed(hidden_page.CHECKBOX_2)
        assert hidden_page.status() == "Checkbox 2 shown"
        hidden_page.toggle_checkbox_2()
        assert not hidden_page.is_displayed(hidden_page.CHECKBOX_2)

    def test_tc_hidden_04_revealed_input_accepts_text(self, hidden_page):
        """TC_HIDDEN_04 - Show Input Box 2, type "now visible" and check the text is kept."""
        hidden_page.toggle_input_2()
        hidden_page.type(hidden_page.INPUT_2, "now visible")
        assert hidden_page.value(hidden_page.INPUT_2) == "now visible"


@pytest.mark.regression
class TestAjax:
    def test_tc_hidden_05_ajax_content_appears_after_delay(self, hidden_page):
        """TC_HIDDEN_05 - Click the AJAX load button and check the content "AJAX Content Loaded" appears after the delay."""
        content = hidden_page.load_ajax_content()
        assert "AJAX Content Loaded" in content
        assert "This is some dynamic content loaded through AJAX." in content

    def test_tc_hidden_06_status_label_after_ajax(self, hidden_page):
        """TC_HIDDEN_06 - Load the AJAX content and check the status label shows "AJAX content loaded"."""
        hidden_page.load_ajax_content()
        hidden_page.wait_for_text(hidden_page.STATUS, "AJAX content loaded")
