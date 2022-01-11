from datetime import datetime

import pytest

from prmexporter.date_converter import date_range_to_dates_converter


def test_returns_datetimes_between_start_and_end_datetime():
    start_datetime = datetime(year=2021, month=2, day=1, hour=0, minute=0, second=0)
    end_datetime = datetime(year=2021, month=2, day=3, hour=0, minute=0, second=0)

    actual = date_range_to_dates_converter(start_datetime, end_datetime)

    expected = [
        datetime(year=2021, month=2, day=1, hour=0, minute=0, second=0),
        datetime(year=2021, month=2, day=2, hour=0, minute=0, second=0),
    ]

    assert actual == expected


def test_throws_exception_when_end_datetime_is_before_start_datetime():
    start_datetime = datetime(year=2021, month=2, day=1, hour=0, minute=0, second=0)
    end_datetime = datetime(year=2021, month=1, day=31, hour=0, minute=0, second=0)

    with pytest.raises(ValueError) as e:
        date_range_to_dates_converter(start_datetime, end_datetime)

    assert str(e.value) == "Start datetime must be before end datetime"


def test_throws_exception_when_start_and_end_datetimes_are_the_same():
    start_datetime = datetime(year=2021, month=2, day=1, hour=0, minute=0, second=0)
    end_datetime = datetime(year=2021, month=2, day=1, hour=0, minute=0, second=0)

    with pytest.raises(ValueError) as e:
        date_range_to_dates_converter(start_datetime, end_datetime)

    assert str(e.value) == "Start datetime must be before end datetime"
