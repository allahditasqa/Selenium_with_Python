"""Labels & links, broken links, Form sections, Shadow DOM, footer navigation, visitors counter."""

import re

import pytest

from tests.ids import tc_ids
from utils.link_checker import status_code


@pytest.mark.regression
class TestLabelsAndLinks:
    def test_tc_link_01_mobile_labels(self, home):
        """TC_LINK_01 - Read the Labels And Links section and check the mobile labels are "Samsung", "Real Me" and "Moto"."""
        assert home.labels_links.mobile_labels() == ["Samsung", "Real Me", "Moto"]

    def test_tc_link_02_laptop_links(self, home):
        """TC_LINK_02 - Read the laptop links and check "Apple", "Lenovo" and "Dell" point to their official sites."""
        links = home.labels_links.laptop_links()
        assert list(links) == ["Apple", "Lenovo", "Dell"]
        assert links["Apple"].startswith("https://www.apple.com")
        assert links["Lenovo"].startswith("https://www.lenovo.com")
        assert links["Dell"].startswith("https://www.dell.com")

    @pytest.mark.external
    def test_tc_link_03_click_laptop_link_navigates(self, home):
        """TC_LINK_03 - Click the laptop link "Apple" and check the browser goes to apple.com."""
        home.labels_links.click_laptop_link("Apple")
        home.wait_until(lambda d: "apple.com" in d.current_url, "Did not navigate to apple.com")

    def test_tc_link_04_eight_broken_link_entries(self, home):
        """TC_LINK_04 - Read the broken link list and check it has 8 entries for the codes 400, 401, 403, 404, 408, 500, 502 and 503."""
        links = home.labels_links.broken_links()
        codes = [re.search(r"e=(\d+)", url).group(1) for url in links.values()]
        assert codes == ["400", "401", "403", "404", "408", "500", "502", "503"]

    @pytest.mark.external
    @pytest.mark.parametrize("code", [400, 401, 403, 404, 408, 500, 502, 503], ids=tc_ids("TC_LINK_05", 8))
    def test_tc_link_05_broken_link_returns_error_status(self, home, code):
        """TC_LINK_05 - Request the broken link for the code {code} and check the server answers with an error status."""
        url = f"http://www.deadlinkcity.com/error-page.asp?e={code}"
        assert url in home.labels_links.broken_links().values()
        assert status_code(url) >= 400


@pytest.mark.regression
class TestFormSections:
    @pytest.mark.parametrize("number", [1, 2, 3], ids=tc_ids("TC_LINK_06", 3))
    def test_tc_link_06_section_content(self, home, number):
        """TC_LINK_06 - Read the heading and the paragraph of "Section {number}"."""
        assert home.sections.heading(number) == f"Section {number}"
        assert home.sections.paragraph(number) == f"This is a paragraph in Section {number}."

    @pytest.mark.parametrize("number", [1, 2, 3], ids=tc_ids("TC_LINK_07", 3))
    def test_tc_link_07_each_section_input_works_independently(self, home, number):
        """TC_LINK_07 - Type "value {number}" in Section {number} and check the other two sections stay empty."""
        home.sections.fill(number, f"value {number}")
        home.sections.submit(number)
        assert home.sections.value(number) == f"value {number}"
        for other in (n for n in (1, 2, 3) if n != number):
            assert home.sections.value(other) == ""


@pytest.mark.regression
class TestShadowDom:
    def test_tc_link_08_text_inside_shadow_root(self, home):
        """TC_LINK_08 - Read the text inside the Shadow DOM and check it is "Mobiles"."""
        assert home.shadow.info_text() == "Mobiles"

    def test_tc_link_09_text_inside_nested_shadow_root(self, home):
        """TC_LINK_09 - Read the text inside the nested Shadow DOM and check it is "Laptops"."""
        assert home.shadow.nested_text() == "Laptops"

    def test_tc_link_10_type_in_shadow_input(self, home):
        """TC_LINK_10 - Type "shadow text" in the input inside the Shadow DOM and check it keeps the value."""
        assert home.shadow.type_in_input("shadow text") == "shadow text"

    def test_tc_link_11_check_shadow_checkbox(self, home):
        """TC_LINK_11 - Click the checkbox inside the Shadow DOM and check it becomes checked."""
        assert home.shadow.toggle_checkbox() is True

    def test_tc_link_12_link_inside_shadow_root(self, home):
        """TC_LINK_12 - Read the link inside the Shadow DOM and check it points to pavantestingtools.com."""
        assert home.shadow.link_href().startswith("https://www.pavantestingtools.com")


@pytest.mark.regression
class TestFooterAndVisitors:
    @pytest.mark.parametrize(
        ("link", "fragment"),
        [("Hidden Elements & AJAX", "gui-elements-ajax-hidden"), ("Download Files", "download-files")],
        ids=tc_ids("TC_LINK_13", 2),
    )
    def test_tc_link_13_footer_link_navigates(self, home, link, fragment):
        """TC_LINK_13 - Click the footer link "{link}" and check the page address contains "{fragment}"."""
        home.footer.open(link)
        home.wait_until(lambda d: fragment in d.current_url, f"URL did not contain {fragment}")

    @pytest.mark.external
    def test_tc_link_14_visitor_counter_is_a_number(self, home):
        """TC_LINK_14 - Read the Visitors counter and check it is a number."""
        assert re.fullmatch(r"[\d,]+", home.visitors.count_text())
