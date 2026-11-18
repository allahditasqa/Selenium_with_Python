"""Smoke: the page loads and every practice section is present."""

import pytest

from tests.ids import tc_ids

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
    def test_tc_home_01_title_and_heading(self, home):
        """TC_HOME_01 - Open the home page and check the browser title and the heading are "Automation Testing Practice"."""
        assert home.title() == "Automation Testing Practice"
        assert home.heading_text() == "Automation Testing Practice"

    @pytest.mark.parametrize("section", EXPECTED_SECTIONS, ids=tc_ids("TC_HOME_02", 19))
    def test_tc_home_02_section_is_present(self, home, section):
        """TC_HOME_02 - Open the home page and check the section "{section}" is present."""
        assert section in home.section_titles()

    def test_tc_home_03_footer_links(self, home):
        """TC_HOME_03 - Open the home page and check the footer shows the three navigation links in order."""
        links = home.footer.links()
        assert list(links) == ["Home", "Hidden Elements & AJAX", "Download Files"]
