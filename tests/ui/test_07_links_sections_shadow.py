"""Labels & links, broken links, Form sections, Shadow DOM, footer navigation, visitors counter."""

import re

import pytest

from utils.link_checker import status_code


@pytest.mark.regression
class TestLabelsAndLinks:
    def test_mobile_labels(self, home):
        assert home.labels_links.mobile_labels() == ["Samsung", "Real Me", "Moto"]

    def test_laptop_links(self, home):
        links = home.labels_links.laptop_links()
        assert list(links) == ["Apple", "Lenovo", "Dell"]
        assert links["Apple"].startswith("https://www.apple.com")
        assert links["Lenovo"].startswith("https://www.lenovo.com")
        assert links["Dell"].startswith("https://www.dell.com")

    @pytest.mark.external
    def test_click_laptop_link_navigates(self, home):
        home.labels_links.click_laptop_link("Apple")
        home.wait_until(lambda d: "apple.com" in d.current_url, "Did not navigate to apple.com")

    def test_eight_broken_link_entries(self, home):
        links = home.labels_links.broken_links()
        codes = [re.search(r"e=(\d+)", url).group(1) for url in links.values()]
        assert codes == ["400", "401", "403", "404", "408", "500", "502", "503"]

    @pytest.mark.external
    @pytest.mark.parametrize("code", [400, 401, 403, 404, 408, 500, 502, 503])
    def test_broken_link_returns_error_status(self, home, code):
        url = f"http://www.deadlinkcity.com/error-page.asp?e={code}"
        assert url in home.labels_links.broken_links().values()
        assert status_code(url) >= 400


@pytest.mark.regression
class TestFormSections:
    @pytest.mark.parametrize("number", [1, 2, 3])
    def test_section_content(self, home, number):
        assert home.sections.heading(number) == f"Section {number}"
        assert home.sections.paragraph(number) == f"This is a paragraph in Section {number}."

    @pytest.mark.parametrize("number", [1, 2, 3])
    def test_each_section_input_works_independently(self, home, number):
        home.sections.fill(number, f"value {number}")
        home.sections.submit(number)
        assert home.sections.value(number) == f"value {number}"
        for other in (n for n in (1, 2, 3) if n != number):
            assert home.sections.value(other) == ""


@pytest.mark.regression
class TestShadowDom:
    def test_text_inside_shadow_root(self, home):
        assert home.shadow.info_text() == "Mobiles"

    def test_text_inside_nested_shadow_root(self, home):
        assert home.shadow.nested_text() == "Laptops"

    def test_type_in_shadow_input(self, home):
        assert home.shadow.type_in_input("shadow text") == "shadow text"

    def test_check_shadow_checkbox(self, home):
        assert home.shadow.toggle_checkbox() is True

    def test_link_inside_shadow_root(self, home):
        assert home.shadow.link_href().startswith("https://www.pavantestingtools.com")


@pytest.mark.regression
class TestFooterAndVisitors:
    @pytest.mark.parametrize(
        ("link", "fragment"),
        [("Hidden Elements & AJAX", "gui-elements-ajax-hidden"), ("Download Files", "download-files")],
    )
    def test_footer_link_navigates(self, home, link, fragment):
        home.footer.open(link)
        home.wait_until(lambda d: fragment in d.current_url, f"URL did not contain {fragment}")

    @pytest.mark.external
    def test_visitor_counter_is_a_number(self, home):
        assert re.fullmatch(r"[\d,]+", home.visitors.count_text())
