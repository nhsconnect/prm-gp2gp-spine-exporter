from datetime import date, datetime, time, timedelta
from typing import Optional


class SearchWindow:
    def __init__(self, start_datetime, end_datetime):
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime

    @classmethod
    def calculate_start_and_end_time(
        cls, start_datetime: Optional[datetime] = None, end_datetime: Optional[datetime] = None
    ):
        if start_datetime and end_datetime:
            return cls(start_datetime, end_datetime)
        if start_datetime:
            end_datetime = start_datetime + timedelta(days=1)
            return cls(start_datetime, end_datetime)
        elif end_datetime:
            raise ValueError("Start datetime must be provided if end datetime is provided")
        else:
            today_midnight_datetime = datetime.combine(date.today(), time.min)
            start_of_yesterday_datetime = today_midnight_datetime - timedelta(days=1)
            return cls(start_of_yesterday_datetime, today_midnight_datetime)

    @staticmethod
    def _to_datetime_string(a_datetime: datetime) -> str:
        return a_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def get_end_datetime_string(self) -> str:
        return self._to_datetime_string(self._end_datetime)

    def get_start_datetime_string(self) -> str:
        return self._to_datetime_string(self._start_datetime)

    def get_start_datetime(self) -> datetime:
        return self._start_datetime

    def get_end_datetime(self) -> datetime:
        return self._end_datetime
