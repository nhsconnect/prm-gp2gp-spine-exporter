from datetime import datetime

from freezegun import freeze_time

from prmexporter.io.search_window import SearchWindow


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
def test_returns_end_datetime_midnight_string():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_today_midnight = search_window.get_end_datetime_string()

    expected_today_midnight = "2021-11-13T00:00:00"

    assert actual_today_midnight == expected_today_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
def test_returns_start_datetime_midnight_string():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_yesterday_midnight = search_window.get_start_datetime_string()

    expected_yesterday_midnight = "2021-11-12T00:00:00"

    assert actual_yesterday_midnight == expected_yesterday_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=0, second=0))
def test_returns_end_datetime_midnight_string_when_at_midnight():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_today_midnight = search_window.get_end_datetime_string()

    expected_today_midnight = "2021-11-13T00:00:00"

    assert actual_today_midnight == expected_today_midnight


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, second=0))
def test_returns_start_datetime_midnight_string_when_changing_years():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_yesterday_midnight = search_window.get_start_datetime_string()

    expected_yesterday_midnight = "2020-12-31T00:00:00"

    assert actual_yesterday_midnight == expected_yesterday_midnight


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, second=0))
def test_returns_year_of_yesterday():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_year = search_window.get_year()

    expected_year = 2020

    assert actual_year == expected_year


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, second=0))
def test_returns_month_of_yesterday():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_month = search_window.get_month()

    expected_month = 12

    assert actual_month == expected_month


@freeze_time(datetime(year=2021, month=1, day=27, hour=2, second=0))
def test_returns_day_of_yesterday():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_day = search_window.get_day()

    expected_day = 26

    assert actual_day == expected_day
