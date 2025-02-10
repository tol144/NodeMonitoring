from common.ip import is_valid_ip
from services.uptime_kuma.model import AlertDataModel


class KumaAlerts:
    @staticmethod
    def process_alert(alert_data: dict) -> AlertDataModel | None:
        heartbeat = alert_data['heartbeat']
        if heartbeat is None:
            return None

        message: str = heartbeat['msg']
        if message is None:
            return None

        monitor = alert_data['monitor']
        if monitor is None:
            return None

        description = monitor['description']
        if description is None \
                or not is_valid_ip(description):
            return None

        return AlertDataModel(message=message,
                              ip=description)
