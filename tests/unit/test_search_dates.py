from datetime import datetime

import pytest
from freezegun import freeze_time

from prmexporter.search_dates import SearchDates


def test_throws_exception_when_only_end_datetime_is_passed():
    end_datetime_input = datetime(year=2020, month=6, day=6)

    with pytest.raises(ValueError) as e:
        SearchDates(start_datetime=None, end_datetime=end_datetime_input)

    assert str(e.value) == "Start datetime must be provided if end datetime is provided"


def test_returns_list_of_datetimes_when_start_and_end_datetimes_are_passed():
    start_datetime_input = datetime(year=2021, month=12, day=30)
    end_datetime_input = datetime(year=2022, month=1, day=3)

    search_dates = SearchDates(start_datetime=start_datetime_input, end_datetime=end_datetime_input)

    expected = [
        datetime(year=2021, month=12, day=30, hour=0, minute=0, second=0),
        datetime(year=2021, month=12, day=31, hour=0, minute=0, second=0),
        datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0),
        datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
    ]

    actual = search_dates.get_dates()

    assert actual == expected


def test_returns_list_with_one_start_datetime_when_only_start_datetime_is_passed():
    start_datetime_input = datetime(year=2021, month=12, day=30)

    search_dates = SearchDates(start_datetime=start_datetime_input, end_datetime=None)

    expected = [datetime(year=2021, month=12, day=30, hour=0, minute=0, second=0)]

    actual = search_dates.get_dates()

    assert actual == expected


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, minute=4, second=45))
def test_returns_list_with_yesterday_midnight_datetime_when_start_and_end_datetime_not_passed():
    search_dates = SearchDates(start_datetime=None, end_datetime=None)

    expected = [datetime(year=2020, month=12, day=31, hour=0, minute=0, second=0)]

    actual = search_dates.get_dates()

    assert actual == expected


def test_throws_exception_when_start_datetime_is_not_at_midnight():
    start_datetime_input = datetime(year=2020, month=6, day=6, hour=6, minute=6, second=6)

    with pytest.raises(ValueError) as e:
        SearchDates(start_datetime=start_datetime_input, end_datetime=None)

    assert str(e.value) == "Datetime must be at midnight"


def test_throws_exception_when_end_datetime_is_not_at_midnight():
    start_datetime_input = datetime(year=2020, month=6, day=6, hour=0, minute=0, second=0)
    end_datetime_input = datetime(year=2020, month=6, day=8, hour=6, minute=6, second=6)

    with pytest.raises(ValueError) as e:
        SearchDates(start_datetime=start_datetime_input, end_datetime=end_datetime_input)

    assert str(e.value) == "Datetime must be at midnight"
