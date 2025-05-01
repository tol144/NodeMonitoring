import pytz
from datetime import datetime, timezone, time


class TimeZone:
    DAILY_WRITE_OFF_HOUR = 14

    def __init__(self, zone: str):
        self._zone = zone
        self._timezone = pytz.timezone(zone)
        self._write_off_time = time(14, 0)

    @property
    def timezone_param(self):
        return self._zone

    @property
    def before_write_off(self) -> bool:
        return self.current_timezone_time() < self._write_off_time

    def current_timezone_time(self) -> time:
        return datetime.now(self._timezone).time()

    def local_time(self, time_value: datetime) -> datetime:
        return time_value.astimezone(self._timezone)

    def utc_time(self, time_value: datetime) -> datetime:
        return time_value.astimezone(timezone.utc)


local_timezone = TimeZone("Europe/Moscow")
# local_timezone = TimeZone("Asia/Yekaterinburg")
