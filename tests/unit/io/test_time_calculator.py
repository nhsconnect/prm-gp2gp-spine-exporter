from datetime import datetime

from freezegun import freeze_time

from prmexporter.io.time_calculator import TimeCalculator


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
def test_returns_today_midnight():
    time_calculator = TimeCalculator()

    actual_today_midnight = time_calculator.get_today_midnight_unix_timestamp()

    expected_today_midnight = 1636761600

    assert actual_today_midnight == expected_today_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
def test_returns_yesterday_midnight():
    time_calculator = TimeCalculator()

    actual_yesterday_midnight = time_calculator.get_yesterday_midnight_unix_timestamp()

    expected_yesterday_midnight = 1636675200

    assert actual_yesterday_midnight == expected_yesterday_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=0, second=0))
def test_returns_today_midnight_when_at_midnight():
    time_calculator = TimeCalculator()

    actual_today_midnight = time_calculator.get_today_midnight_unix_timestamp()

    expected_today_midnight = 1636761600

    assert actual_today_midnight == expected_today_midnight


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, second=0))
def test_returns_yesterday_midnight_when_changing_years():
    time_calculator = TimeCalculator()

    actual_yesterday_midnight = time_calculator.get_yesterday_midnight_unix_timestamp()

    expected_yesterday_midnight = 1609372800

    assert actual_yesterday_midnight == expected_yesterday_midnight


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, second=0))
def test_returns_year_of_yesterday():
    time_calculator = TimeCalculator()

    actual_year = time_calculator.get_year()

    expected_year = 2020

    assert actual_year == expected_year


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, second=0))
def test_returns_month_of_yesterday():
    time_calculator = TimeCalculator()

    actual_month = time_calculator.get_month()

    expected_month = 12

    assert actual_month == expected_month


@freeze_time(datetime(year=2021, month=1, day=27, hour=2, second=0))
def test_returns_day_of_yesterday():
    time_calculator = TimeCalculator()

    actual_day = time_calculator.get_day()

    expected_day = 26

    assert actual_day == expected_day
