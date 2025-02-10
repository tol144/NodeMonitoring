import re

from config import settings
from api.alerts.kuma import KumaAlerts
from services.node.methods import restart_node

from services.uptime_kuma.node_class import kuma_node
from services.uptime_kuma.model import AlertData, AlertDataModel

from services.cloudflare.model import DnsSearchResult
from services.cloudflare.zone_class import cloudflare_dns_zone


class APIMethods:
    @staticmethod
    def process_alert(alert_data: dict):
        alert_data_model = KumaAlerts.process_alert(alert_data)
        if alert_data_model is None:
            return

        dns = APIMethods.get_dns_zone_by_alert_data(alert_data_model)
        if dns is None:
            return

        if re.search(AlertData.ok, alert_data_model.message, re.IGNORECASE):
            APIMethods.ok_alert(dns)
        elif re.search(AlertData.fail, alert_data_model.message, re.IGNORECASE):
            APIMethods.fail_alert(dns)

    @staticmethod
    def get_dns_zone_by_alert_data(alert_data_model: AlertDataModel) -> DnsSearchResult | None:
        node = kuma_node.get_node_by_name(alert_data_model.node_name)
        if node is None:
            return None

        return cloudflare_dns_zone.get_dns_zone_by_ip(node.ip)

    @staticmethod
    def ok_alert(dns: DnsSearchResult):
        cloudflare_dns_zone.update_dns(dns, settings.ok_cloudflare_url)

    @staticmethod
    def fail_alert(dns: DnsSearchResult):
        cloudflare_dns_zone.update_dns(dns, settings.fail_cloudflare_url)
        restart_node(dns.ip)

