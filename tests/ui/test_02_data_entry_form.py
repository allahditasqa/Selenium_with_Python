"""Data Entry Form: inputs, radio buttons, checkboxes, dropdowns, date pickers and date range."""

import re

import pytest

from test_data.loader import load
from tests.ids import tc_ids

DATA = load("form_data")
USER = DATA["valid_user"]


@pytest.mark.regression
class TestTextFields:
    def test_tc_form_01_fill_all_text_fields(self, home):
        """TC_FORM_01 - Fill name, email, phone and address with valid data and check every field keeps its value."""
        home.form.fill_name(USER["name"][:15])
        home.form.fill_email(USER["email"])
        home.form.fill_phone(USER["phone"])
        home.form.fill_address(USER["address"])
        assert home.form.value(home.form.NAME) == USER["name"][:15]
        assert home.form.value(home.form.EMAIL) == USER["email"]
        assert home.form.value(home.form.PHONE) == USER["phone"]
        assert home.form.value(home.form.ADDRESS) == USER["address"]

    def test_tc_form_02_name_is_limited_to_15_characters(self, home):
        """TC_FORM_02 - Type 30 characters in the Name field and check only 15 are accepted."""
        home.form.fill_name("A" * 30)
        assert len(home.form.value(home.form.NAME)) == 15

    def test_tc_form_03_email_is_limited_to_25_characters(self, home):
        """TC_FORM_03 - Type 40 characters in the Email field and check only 25 are accepted."""
        home.form.fill_email("e" * 40)
        assert len(home.form.value(home.form.EMAIL)) == 25

    def test_tc_form_04_phone_is_limited_to_10_characters(self, home):
        """TC_FORM_04 - Type 20 digits in the Phone field and check only 10 are accepted."""
        home.form.fill_phone("1" * 20)
        assert home.form.value(home.form.PHONE) == "1" * 10


@pytest.mark.regression
class TestRadioAndCheckboxes:
    def test_tc_form_05_gender_radio_buttons_are_mutually_exclusive(self, home):
        """TC_FORM_05 - Select Male and then Female and check only one gender is selected at a time."""
        home.form.choose_gender("male")
        assert home.form.is_gender_selected("male")
        assert not home.form.is_gender_selected("female")
        home.form.choose_gender("female")
        assert home.form.is_gender_selected("female")
        assert not home.form.is_gender_selected("male")

    @pytest.mark.parametrize("day", DATA["weekdays"], ids=tc_ids("TC_FORM_06", 7))
    def test_tc_form_06_each_day_checkbox_can_be_checked_and_unchecked(self, home, day):
        """TC_FORM_06 - Check and uncheck the {day} checkbox and check its state changes each time."""
        home.form.set_day(day, True)
        assert home.form.is_day_selected(day)
        home.form.set_day(day, False)
        assert not home.form.is_day_selected(day)

    def test_tc_form_07_select_several_days(self, home):
        """TC_FORM_07 - Select Monday, Wednesday and Friday and check only these three days are selected."""
        for day in USER["days"]:
            home.form.set_day(day)
        selected = [d for d in DATA["weekdays"] if home.form.is_day_selected(d)]
        assert selected == [d for d in DATA["weekdays"] if d in USER["days"]]

    def test_tc_form_08_select_all_days(self, home):
        """TC_FORM_08 - Select all seven day checkboxes and check all of them are checked."""
        for day in DATA["weekdays"]:
            home.form.set_day(day)
        assert all(home.form.is_day_selected(d) for d in DATA["weekdays"])


@pytest.mark.regression
class TestDropdowns:
    def test_tc_form_09_country_has_expected_options(self, home):
        """TC_FORM_09 - Open the Country dropdown and check it lists the ten expected countries in order."""
        assert home.form.country_options() == DATA["expected_countries"]

    @pytest.mark.parametrize("country", DATA["expected_countries"], ids=tc_ids("TC_FORM_10", 10))
    def test_tc_form_10_select_each_country(self, home, country):
        """TC_FORM_10 - Select the country "{country}" and check the dropdown shows it."""
        home.form.select_country(country)
        assert home.form.selected_country() == country

    def test_tc_form_11_colors_list_contains_duplicates(self, home):
        """TC_FORM_11 - Read the Colors list and check Red and Green each appear twice (site quirk)."""
        colors = home.form.options(home.form.COLORS)
        assert colors == ["Red", "Blue", "Green", "Yellow", "Red", "White", "Green"]

    def test_tc_form_12_colors_multi_select(self, home):
        """TC_FORM_12 - Select "Red" and "Green" in the Colors list and check both duplicate Red options are selected."""
        # Selecting by visible text picks every option with that text, so duplicates are both selected.
        home.form.select_multiple(home.form.COLORS, USER["colors"])
        selected = home.form.selected_multiple(home.form.COLORS)
        assert sorted(set(selected)) == sorted(USER["colors"])
        assert selected.count("Red") == 2

    def test_tc_form_13_animals_list_is_sorted_alphabetically(self, home):
        """TC_FORM_13 - Read the Animals list and check it has 10 options in alphabetical order."""
        animals = home.form.options(home.form.ANIMALS)
        assert animals == sorted(animals)
        assert len(animals) == 10

    def test_tc_form_14_animals_multi_select(self, home):
        """TC_FORM_14 - Select "Cat" and "Zebra" in the Animals list and check exactly these are selected."""
        home.form.select_multiple(home.form.ANIMALS, USER["animals"])
        assert home.form.selected_multiple(home.form.ANIMALS) == USER["animals"]


@pytest.mark.regression
class TestDatePickers:
    def test_tc_form_15_date_picker_1_uses_mm_dd_yyyy(self, home):
        """TC_FORM_15 - Pick day 15 in Date Picker 1 and check the date format is MM/DD/YYYY."""
        value = home.form.pick_date(home.form.DATE_PICKER_1, 15)
        assert re.fullmatch(r"\d{2}/15/\d{4}", value), value

    def test_tc_form_16_date_picker_2_uses_dd_mm_yyyy(self, home):
        """TC_FORM_16 - Pick day 20 in Date Picker 2 and check the date format is DD/MM/YYYY."""
        value = home.form.pick_date(home.form.DATE_PICKER_2, 20)
        assert re.fullmatch(r"20/\d{2}/\d{4}", value), value

    def test_tc_form_17_date_range_counts_days(self, home):
        """TC_FORM_17 - Submit the date range 2026-01-01 to 2026-01-11 and check the message "You selected a range of 10 days."."""
        home.form.set_date_range("2026-01-01", "2026-01-11")
        assert home.form.submit() == "You selected a range of 10 days."

    def test_tc_form_18_same_start_and_end_date(self, home):
        """TC_FORM_18 - Submit a date range where start and end are both 2026-03-05 and check the message "You selected a range of 0 days."."""
        home.form.set_date_range("2026-03-05", "2026-03-05")
        assert home.form.submit() == "You selected a range of 0 days."

    def test_tc_form_19_end_date_before_start_date_is_rejected(self, home):
        """TC_FORM_19 - Submit a date range where the end date is before the start date and check the error "End date must be after start date."."""
        home.form.set_date_range("2026-01-11", "2026-01-01")
        assert home.form.submit() == "End date must be after start date."

    def test_tc_form_20_submit_without_dates_asks_for_both(self, home):
        """TC_FORM_20 - Click Submit without any date and check the message "Please select both start and end dates."."""
        assert home.form.submit() == "Please select both start and end dates."


@pytest.mark.regression
def test_tc_form_21_complete_form_end_to_end(home):
    """TC_FORM_21 - Fill the complete form with valid data and submit a date range of 14 days."""
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
