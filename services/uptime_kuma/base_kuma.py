from uptime_kuma_api import UptimeKumaApi

from config import settings


class UptimeKuma:
    def __init__(self):
        self.api = UptimeKumaApi(settings.uptime_kuma_url)
        self.api.login(settings.uptime_kuma_username, settings.uptime_kuma_password)

    def __del__(self):
        self.api.disconnect()

    def get_monitors(self):
        return self.api.get_monitors()
