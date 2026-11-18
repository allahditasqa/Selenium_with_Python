"""Static, dynamic and paginated web tables."""

import pytest


@pytest.mark.regression
class TestStaticTable:
    def test_headers(self, home):
        assert home.static_table.headers() == ["BookName", "Author", "Subject", "Price"]

    def test_row_count(self, home):
        assert home.static_table.row_count() == 6

    def test_books_by_author(self, home):
        names = [b.name for b in home.static_table.books_by_author("Mukesh")]
        assert names == ["Learn Java", "Master In Selenium"]

    def test_total_price_of_all_books(self, home):
        assert home.static_table.total_price() == 7100

    def test_total_price_of_selenium_books(self, home):
        assert home.static_table.total_price("Selenium") == 3300

    def test_most_expensive_book(self, home):
        most_expensive = max(home.static_table.books(), key=lambda b: b.price)
        assert most_expensive.name == "Master In Selenium"


@pytest.mark.regression
class TestDynamicTable:
    def test_headers_contain_all_columns_in_any_order(self, home):
        assert sorted(home.dynamic_table.headers()) == sorted(
            ["Name", "Network (Mbps)", "CPU (%)", "Memory (MB)", "Disk (MB/s)"]
        )

    def test_expected_processes(self, home):
        assert sorted(home.dynamic_table.processes()) == ["Chrome", "Firefox", "Internet Explorer", "System"]

    @pytest.mark.parametrize(
        ("process", "column"),
        [
            ("Chrome", "CPU (%)"),
            ("Firefox", "Memory (MB)"),
            ("Chrome", "Network (Mbps)"),
            ("Firefox", "Disk (MB/s)"),
        ],
    )
    def test_value_below_table_matches_table_cell(self, home, process, column):
        assert home.dynamic_table.displayed_value(process, column) == home.dynamic_table.value(
            process, column
        )

    def test_every_cell_has_a_unit(self, home):
        units = {"Network (Mbps)": "Mbps", "CPU (%)": "%", "Memory (MB)": "MB", "Disk (MB/s)": "MB/s"}
        for process, row in home.dynamic_table.snapshot().items():
            for column, unit in units.items():
                assert row[column].endswith(unit), f"{process}/{column} = {row[column]}"


@pytest.mark.regression
class TestPaginationTable:
    def test_has_four_pages_with_five_rows(self, home):
        assert home.pagination.page_count() == 4
        assert len(home.pagination.rows()) == 5

    def test_first_page_is_active_by_default(self, home):
        assert home.pagination.active_page() == 1

    @pytest.mark.parametrize("page", [1, 2, 3, 4])
    def test_each_page_shows_its_own_ids(self, home, page):
        home.pagination.go_to_page(page)
        ids = [int(r["id"]) for r in home.pagination.rows()]
        assert ids == list(range((page - 1) * 5 + 1, (page - 1) * 5 + 1 + len(ids)))
        assert home.pagination.active_page() == page

    def test_all_pages_have_unique_products(self, home):
        rows = home.pagination.all_rows()
        assert len(rows) == 20
        assert len({r["id"] for r in rows}) == 20

    def test_prices_use_dollar_format(self, home):
        for row in home.pagination.all_rows():
            assert row["price"].startswith("$"), row

    def test_select_product_on_first_page(self, home):
        home.pagination.select_product("Laptop")
        assert home.pagination.is_product_selected("Laptop")
        assert not home.pagination.is_product_selected("Smartphone")

    def test_selection_is_per_page(self, home):
        home.pagination.select_product("Smartphone")
        home.pagination.go_to_page(2)
        assert not any(home.pagination.is_product_selected(r["name"]) for r in home.pagination.rows())
