"""Data Entry Form: inputs, radio buttons, checkboxes, dropdowns, date pickers and date range."""

import re

import pytest

from test_data.loader import load

DATA = load("form_data")
USER = DATA["valid_user"]


@pytest.mark.regression
class TestTextFields:
    def test_fill_all_text_fields(self, home):
        home.form.fill_name(USER["name"][:15])
        home.form.fill_email(USER["email"])
        home.form.fill_phone(USER["phone"])
        home.form.fill_address(USER["address"])
        assert home.form.value(home.form.NAME) == USER["name"][:15]
        assert home.form.value(home.form.EMAIL) == USER["email"]
        assert home.form.value(home.form.PHONE) == USER["phone"]
        assert home.form.value(home.form.ADDRESS) == USER["address"]

    def test_name_is_limited_to_15_characters(self, home):
        home.form.fill_name("A" * 30)
        assert len(home.form.value(home.form.NAME)) == 15

    def test_email_is_limited_to_25_characters(self, home):
        home.form.fill_email("e" * 40)
        assert len(home.form.value(home.form.EMAIL)) == 25

    def test_phone_is_limited_to_10_characters(self, home):
        home.form.fill_phone("1" * 20)
        assert home.form.value(home.form.PHONE) == "1" * 10


@pytest.mark.regression
class TestRadioAndCheckboxes:
    def test_gender_radio_buttons_are_mutually_exclusive(self, home):
        home.form.choose_gender("male")
        assert home.form.is_gender_selected("male")
        assert not home.form.is_gender_selected("female")
        home.form.choose_gender("female")
        assert home.form.is_gender_selected("female")
        assert not home.form.is_gender_selected("male")

    @pytest.mark.parametrize("day", DATA["weekdays"])
    def test_each_day_checkbox_can_be_checked_and_unchecked(self, home, day):
        home.form.set_day(day, True)
        assert home.form.is_day_selected(day)
        home.form.set_day(day, False)
        assert not home.form.is_day_selected(day)

    def test_select_several_days(self, home):
        for day in USER["days"]:
            home.form.set_day(day)
        selected = [d for d in DATA["weekdays"] if home.form.is_day_selected(d)]
        assert selected == [d for d in DATA["weekdays"] if d in USER["days"]]

    def test_select_all_days(self, home):
        for day in DATA["weekdays"]:
            home.form.set_day(day)
        assert all(home.form.is_day_selected(d) for d in DATA["weekdays"])


@pytest.mark.regression
class TestDropdowns:
    def test_country_has_expected_options(self, home):
        assert home.form.country_options() == DATA["expected_countries"]

    @pytest.mark.parametrize("country", DATA["expected_countries"])
    def test_select_each_country(self, home, country):
        home.form.select_country(country)
        assert home.form.selected_country() == country

    def test_colors_list_contains_duplicates(self, home):
        """Site quirk worth knowing: 'Red' and 'Green' each appear twice in the Colors list."""
        colors = home.form.options(home.form.COLORS)
        assert colors == ["Red", "Blue", "Green", "Yellow", "Red", "White", "Green"]

    def test_colors_multi_select(self, home):
        # Selecting by visible text picks every option with that text, so duplicates are both selected.
        home.form.select_multiple(home.form.COLORS, USER["colors"])
        selected = home.form.selected_multiple(home.form.COLORS)
        assert sorted(set(selected)) == sorted(USER["colors"])
        assert selected.count("Red") == 2

    def test_animals_list_is_sorted_alphabetically(self, home):
        animals = home.form.options(home.form.ANIMALS)
        assert animals == sorted(animals)
        assert len(animals) == 10

    def test_animals_multi_select(self, home):
        home.form.select_multiple(home.form.ANIMALS, USER["animals"])
        assert home.form.selected_multiple(home.form.ANIMALS) == USER["animals"]


@pytest.mark.regression
class TestDatePickers:
    def test_date_picker_1_uses_mm_dd_yyyy(self, home):
        value = home.form.pick_date(home.form.DATE_PICKER_1, 15)
        assert re.fullmatch(r"\d{2}/15/\d{4}", value), value

    def test_date_picker_2_uses_dd_mm_yyyy(self, home):
        value = home.form.pick_date(home.form.DATE_PICKER_2, 20)
        assert re.fullmatch(r"20/\d{2}/\d{4}", value), value

    def test_date_range_counts_days(self, home):
        home.form.set_date_range("2026-01-01", "2026-01-11")
        assert home.form.submit() == "You selected a range of 10 days."

    def test_same_start_and_end_date(self, home):
        home.form.set_date_range("2026-03-05", "2026-03-05")
        assert home.form.submit() == "You selected a range of 0 days."

    def test_end_date_before_start_date_is_rejected(self, home):
        home.form.set_date_range("2026-01-11", "2026-01-01")
        assert home.form.submit() == "End date must be after start date."

    def test_submit_without_dates_asks_for_both(self, home):
        assert home.form.submit() == "Please select both start and end dates."


@pytest.mark.regression
def test_complete_form_end_to_end(home):
    form = home.form
    form.fill_name(USER["name"][:15])
    form.fill_email(USER["email"])
    form.fill_phone(USER["phone"])
    form.fill_address(USER["address"])
    form.choose_gender(USER["gender"])
    for day in USER["days"]:
        form.set_day(day)
    form.select_country(USER["country"])
    form.select_multiple(form.COLORS, USER["colors"])
    form.select_multiple(form.ANIMALS, USER["animals"])
    form.pick_date(form.DATE_PICKER_1, 10)
    form.set_date_range("2026-02-01", "2026-02-15")

    assert form.is_gender_selected(USER["gender"])
    assert form.selected_country() == USER["country"]
    assert form.submit() == "You selected a range of 14 days."
