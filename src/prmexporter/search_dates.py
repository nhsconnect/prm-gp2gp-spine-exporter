from datetime import date, datetime, time, timedelta
from typing import List, Optional

from prmexporter.date_converter import convert_date_range_to_dates


class SearchDates:
    def __init__(
        self, start_datetime: Optional[datetime] = None, end_datetime: Optional[datetime] = None
    ):
        self._dates = self._calculate_search_dates(start_datetime, end_datetime)

    def _calculate_search_dates(
        self, start_datetime: Optional[datetime] = None, end_datetime: Optional[datetime] = None
    ) -> List[datetime]:
        self._validate_datetime(start_datetime)
        self._validate_datetime(end_datetime)

        if start_datetime and end_datetime:
            return convert_date_range_to_dates(start_datetime, end_datetime)
        if start_datetime:
            return [start_datetime]
        elif end_datetime:
            raise ValueError("Start datetime must be provided if end datetime is provided")
        else:
            return [self._calculate_yesterday_midnight_datetime()]

    @staticmethod
    def _validate_datetime(a_datetime: Optional[datetime]):
        midnight = time(hour=0, minute=0, second=0)
        if a_datetime and a_datetime.time() != midnight:
            raise ValueError("Datetime must be at midnight")

    @staticmethod
    def _calculate_yesterday_midnight_datetime() -> datetime:
        today_midnight_datetime = datetime.combine(date.today(), time.min)
        return today_midnight_datetime - timedelta(days=1)

    def get_dates(self) -> List[datetime]:
        return self._dates