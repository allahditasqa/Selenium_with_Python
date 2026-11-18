"""Smoke: the page loads and every practice section is present."""

import pytest

EXPECTED_SECTIONS = [
    "Data Entry Form",
    "Upload Files",
    "Static Web Table",
    "Dynamic Web Table",
    "Pagination Web Table",
    "Tabs",
    "Dynamic Button",
    "Alerts & Popups",
    "Mouse Hover",
    "Double Click",
    "Drag and Drop",
    "Slider",
    "SVG Elements",
    "Scrolling DropDown",
    "Labels And Links",
    "Visitors",
    "Form",
    "Footer Links",
    "ShadowDOM",
]


@pytest.mark.smoke
class TestHomePage:
    def test_title_and_heading(self, home):
        assert home.title() == "Automation Testing Practice"
        assert home.heading_text() == "Automation Testing Practice"

    @pytest.mark.parametrize("section", EXPECTED_SECTIONS)
    def test_section_is_present(self, home, section):
        assert section in home.section_titles()

    def test_footer_links(self, home):
        links = home.footer.links()
        assert list(links) == ["Home", "Hidden Elements & AJAX", "Download Files"]
