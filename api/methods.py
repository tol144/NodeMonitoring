import re

from api.alerts.kuma import KumaAlerts
from services.node.methods import restart_node

from services.uptime_kuma.model import AlertData

from services.cloudflare.model import DnsSearchResult, ZoneModel
from services.cloudflare.zone_class import cloudflare_dns_zone


class APIMethods:
    @staticmethod
    def process_alert(alert_data: dict):
        alert_data_model = KumaAlerts.process_alert(alert_data)
        if alert_data_model is None:
            return

        dns = cloudflare_dns_zone.get_dns_zone_by_ip(alert_data_model.ip)
        if dns is None:
            return

        if re.search(AlertData.ok, alert_data_model.message, re.IGNORECASE):
            APIMethods.ok_alert(dns)
        elif re.search(AlertData.fail, alert_data_model.message, re.IGNORECASE):
            APIMethods.fail_alert(dns)

    @staticmethod
    def ok_alert(dns: DnsSearchResult):
        cloudflare_dns_zone.update_dns_ok(dns)

    @staticmethod
    def fail_alert(dns: DnsSearchResult):
        cloudflare_dns_zone.update_dns_fail(dns)
        restart_node(dns.ip)

    @staticmethod
    def get_all_dns() -> list[ZoneModel]:
        return cloudflare_dns_zone.get_zone_model_list()
