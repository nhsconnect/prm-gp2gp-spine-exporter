from datetime import date, datetime, time, timedelta


class SearchWindow:
    def __init__(self, start_datetime, end_datetime):
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime

    @classmethod
    def prior_to_now(cls, number_of_days: int):
        today = date.today()
        end_datetime = datetime.combine(today, time.min)
        start_datetime = end_datetime - timedelta(days=number_of_days)

        return cls(start_datetime, end_datetime)

    @staticmethod
    def _to_datetime_string(a_datetime: datetime) -> str:
        return a_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def get_end_datetime_string(self) -> str:
        return self._to_datetime_string(self._end_datetime)

    def get_start_datetime_string(self) -> str:
        return self._to_datetime_string(self._start_datetime)

    def get_start_datetime(self) -> datetime:
        return self._start_datetime
