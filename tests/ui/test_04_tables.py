"""Static, dynamic and paginated web tables."""

import pytest

from tests.ids import tc_ids


@pytest.mark.regression
class TestStaticTable:
    def test_tc_table_01_headers(self, home):
        """TC_TABLE_01 - Read the Static Web Table headers and check they are "BookName", "Author", "Subject" and "Price"."""
        assert home.static_table.headers() == ["BookName", "Author", "Subject", "Price"]

    def test_tc_table_02_row_count(self, home):
        """TC_TABLE_02 - Count the rows of the Static Web Table and check there are 6 data rows."""
        assert home.static_table.row_count() == 6

    def test_tc_table_03_books_by_author(self, home):
        """TC_TABLE_03 - Filter the Static Web Table by author "Mukesh" and check the two book names."""
        names = [b.name for b in home.static_table.books_by_author("Mukesh")]
        assert names == ["Learn Java", "Master In Selenium"]

    def test_tc_table_04_total_price_of_all_books(self, home):
        """TC_TABLE_04 - Add the prices of all books in the Static Web Table and check the total is 7100."""
        assert home.static_table.total_price() == 7100

    def test_tc_table_05_total_price_of_selenium_books(self, home):
        """TC_TABLE_05 - Add the prices of the books with the subject "Selenium" and check the total is 3300."""
        assert home.static_table.total_price("Selenium") == 3300

    def test_tc_table_06_most_expensive_book(self, home):
        """TC_TABLE_06 - Find the most expensive book in the Static Web Table and check it is "Master In Selenium"."""
        most_expensive = max(home.static_table.books(), key=lambda b: b.price)
        assert most_expensive.name == "Master In Selenium"


@pytest.mark.regression
class TestDynamicTable:
    def test_tc_table_07_headers_contain_all_columns_in_any_order(self, home):
        """TC_TABLE_07 - Read the Dynamic Web Table headers and check the five columns exist in any order."""
        assert sorted(home.dynamic_table.headers()) == sorted(
            ["Name", "Network (Mbps)", "CPU (%)", "Memory (MB)", "Disk (MB/s)"]
        )

    def test_tc_table_08_expected_processes(self, home):
        """TC_TABLE_08 - Read the process names of the Dynamic Web Table and check the four expected processes."""
        assert sorted(home.dynamic_table.processes()) == ["Chrome", "Firefox", "Internet Explorer", "System"]

    @pytest.mark.parametrize(
        ("process", "column"),
        [
            ("Chrome", "CPU (%)"),
            ("Firefox", "Memory (MB)"),
            ("Chrome", "Network (Mbps)"),
            ("Firefox", "Disk (MB/s)"),
        ],
        ids=tc_ids("TC_TABLE_09", 4),
    )
    def test_tc_table_09_value_below_table_matches_table_cell(self, home, process, column):
        """TC_TABLE_09 - Compare the "{column}" value of "{process}" shown below the table with its table cell."""
        assert home.dynamic_table.displayed_value(process, column) == home.dynamic_table.value(
            process, column
        )

    def test_tc_table_10_every_cell_has_a_unit(self, home):
        """TC_TABLE_10 - Read every cell of the Dynamic Web Table and check it ends with the unit of its column."""
        units = {"Network (Mbps)": "Mbps", "CPU (%)": "%", "Memory (MB)": "MB", "Disk (MB/s)": "MB/s"}
        for process, row in home.dynamic_table.snapshot().items():
            for column, unit in units.items():
                assert row[column].endswith(unit), f"{process}/{column} = {row[column]}"


@pytest.mark.regression
class TestPaginationTable:
    def test_tc_table_11_has_four_pages_with_five_rows(self, home):
        """TC_TABLE_11 - Open the Pagination Web Table and check it has 4 pages and 5 rows on the first page."""
        assert home.pagination.page_count() == 4
        assert len(home.pagination.rows()) == 5

    def test_tc_table_12_first_page_is_active_by_default(self, home):
        """TC_TABLE_12 - Open the Pagination Web Table and check page 1 is active."""
        assert home.pagination.active_page() == 1

    @pytest.mark.parametrize("page", [1, 2, 3, 4], ids=tc_ids("TC_TABLE_13", 4))
    def test_tc_table_13_each_page_shows_its_own_ids(self, home, page):
        """TC_TABLE_13 - Open page {page} of the Pagination Web Table and check its product ids and active page."""
        home.pagination.go_to_page(page)
        ids = [int(r["id"]) for r in home.pagination.rows()]
        assert ids == list(range((page - 1) * 5 + 1, (page - 1) * 5 + 1 + len(ids)))
        assert home.pagination.active_page() == page

    def test_tc_table_14_all_pages_have_unique_products(self, home):
        """TC_TABLE_14 - Visit all 4 pages of the Pagination Web Table and check there are 20 unique product ids."""
        rows = home.pagination.all_rows()
        assert len(rows) == 20
        assert len({r["id"] for r in rows}) == 20

    def test_tc_table_15_prices_use_dollar_format(self, home):
        """TC_TABLE_15 - Visit all 4 pages of the Pagination Web Table and check every price starts with "$"."""
        for row in home.pagination.all_rows():
            assert row["price"].startswith("$"), row

    def test_tc_table_16_select_product_on_first_page(self, home):
        """TC_TABLE_16 - Tick the checkbox of product "Laptop" and check only that product is selected."""
        home.pagination.select_product("Laptop")
        assert home.pagination.is_product_selected("Laptop")
        assert not home.pagination.is_product_selected("Smartphone")

    def test_tc_table_17_selection_is_per_page(self, home):
        """TC_TABLE_17 - Tick "Smartphone" on page 1, open page 2 and check no product is selected there."""
        home.pagination.select_product("Smartphone")
        home.pagination.go_to_page(2)
        assert not any(home.pagination.is_product_selected(r["name"]) for r in home.pagination.rows())
