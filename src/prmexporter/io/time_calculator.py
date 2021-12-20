from datetime import date, datetime, time, timedelta


class TimeCalculator:
    def __init__(self):
        self._today = date.today()
        self._today_midnight = self._get_today_midnight()
        self._yesterday_midnight = self._get_yesterday_midnight()

    def _get_today_midnight(self) -> datetime:
        return datetime.combine(self._today, time.min)

    def _get_yesterday_midnight(self) -> datetime:
        return self._today_midnight - timedelta(days=1)

    @staticmethod
    def _to_datetime_string(a_datetime: datetime) -> str:
        return a_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def get_today_midnight_datetime_string(self) -> str:
        return self._to_datetime_string(self._today_midnight)

    def get_yesterday_midnight_datetime_string(self) -> str:
        return self._to_datetime_string(self._yesterday_midnight)

    def get_year(self) -> int:
        return self._yesterday_midnight.year

    def get_month(self) -> int:
        return self._yesterday_midnight.month

    def get_day(self) -> int:
        return self._yesterday_midnight.day
