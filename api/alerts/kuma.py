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

        name = monitor['name']
        if name is None:
            return None

        return AlertDataModel(message=message,
                              node_name=name)
