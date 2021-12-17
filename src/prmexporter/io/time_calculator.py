import time
from datetime import date, datetime
from datetime import time as datetime_time
from datetime import timedelta


def _to_unix_timestamp(a_datetime):
    return time.mktime(a_datetime.timetuple())


class TimeCalculator:
    def __init__(self):
        self._today = date.today()
        self._today_midnight = self._get_today_midnight()
        self._yesterday_midnight = self._get_yesterday_midnight()

    def _get_today_midnight(self):
        return datetime.combine(self._today, datetime_time.min)

    def _get_yesterday_midnight(self):
        return self._today_midnight - timedelta(days=1)

    def get_today_midnight_unix_timestamp(self):
        return _to_unix_timestamp(self._today_midnight)

    def get_yesterday_midnight_unix_timestamp(self):
        return _to_unix_timestamp(self._yesterday_midnight)

    def get_year(self):
        return self._yesterday_midnight.year

    def get_month(self):
        return self._yesterday_midnight.month

    def get_day(self):
        return self._yesterday_midnight.day
