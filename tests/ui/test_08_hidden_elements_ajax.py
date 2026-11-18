"""'Hidden Elements & AJAX' page."""

import pytest


@pytest.mark.regression
class TestHiddenElements:
    def test_initial_state(self, hidden_page):
        assert hidden_page.status() == "Ready"
        assert hidden_page.is_displayed(hidden_page.INPUT_1)
        assert not hidden_page.is_displayed(hidden_page.INPUT_2)
        assert not hidden_page.is_displayed(hidden_page.CHECKBOX_2)

    def test_toggle_input_box_2(self, hidden_page):
        hidden_page.toggle_input_2()
        assert hidden_page.is_displayed(hidden_page.INPUT_2)
        assert hidden_page.status() == "Input Box 2 shown"
        hidden_page.toggle_input_2()
        assert not hidden_page.is_displayed(hidden_page.INPUT_2)
        assert hidden_page.status() == "Input Box 2 hidden"

    def test_toggle_checkbox_2(self, hidden_page):
        hidden_page.toggle_checkbox_2()
        assert hidden_page.is_displayed(hidden_page.CHECKBOX_2)
        assert hidden_page.status() == "Checkbox 2 shown"
        hidden_page.toggle_checkbox_2()
        assert not hidden_page.is_displayed(hidden_page.CHECKBOX_2)

    def test_revealed_input_accepts_text(self, hidden_page):
        hidden_page.toggle_input_2()
        hidden_page.type(hidden_page.INPUT_2, "now visible")
        assert hidden_page.value(hidden_page.INPUT_2) == "now visible"


@pytest.mark.regression
class TestAjax:
    def test_ajax_content_appears_after_delay(self, hidden_page):
        content = hidden_page.load_ajax_content()
        assert "AJAX Content Loaded" in content
        assert "This is some dynamic content loaded through AJAX." in content

    def test_status_label_after_ajax(self, hidden_page):
        hidden_page.load_ajax_content()
        hidden_page.wait_for_text(hidden_page.STATUS, "AJAX content loaded")
