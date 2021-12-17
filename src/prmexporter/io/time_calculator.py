from datetime import date, datetime, time, timedelta


def _to_datetime_string(a_datetime):
    return a_datetime.strftime("%Y/%m/%d:%H:%M:%S")


class TimeCalculator:
    def __init__(self):
        self._today = date.today()
        self._today_midnight = self._get_today_midnight()
        self._yesterday_midnight = self._get_yesterday_midnight()

    def _get_today_midnight(self):
        return datetime.combine(self._today, time.min)

    def _get_yesterday_midnight(self):
        return self._today_midnight - timedelta(days=1)

    def get_today_midnight_datetime_string(self):
        return _to_datetime_string(self._today_midnight)

    def get_yesterday_midnight_datetime_string(self):
        return _to_datetime_string(self._yesterday_midnight)

    def get_year(self):
        return self._yesterday_midnight.year

    def get_month(self):
        return self._yesterday_midnight.month

    def get_day(self):
        return self._yesterday_midnight.day
