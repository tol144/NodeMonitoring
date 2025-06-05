import re

from api.alerts.kuma import KumaAlerts
from services.node.methods import restart_node

from services.uptime_kuma.model import AlertData

from services.cloudflare.model import DnsSearchResult, ZoneModel
from services.cloudflare.zone_class import ZoneClass, cloudflare_dns_zone
from services.cloudflare.state import DnsZoneState, ServersState

from loguru import logger


class APIMethods:
    @staticmethod
    @logger.catch
    async def process_alert(alert_data: dict):
        alert_data_model = KumaAlerts.process_alert(alert_data)
        if alert_data_model is None:
            return

        dns = await APIMethods.get_dns_zone(alert_data_model.ip)
        if dns is None:
            return

        if re.search(AlertData.ok, alert_data_model.message, re.IGNORECASE):
            await APIMethods.ok_alert(dns)
        elif re.search(AlertData.fail, alert_data_model.message, re.IGNORECASE):
            await APIMethods.fail_alert(dns)

    @staticmethod
    async def get_dns_zone(ip: str) -> DnsSearchResult | None:
        dns = await ZoneClass.get_cached_dns_zone_by_ip(ip)
        if dns is not None:
            return dns

        await cloudflare_dns_zone.cache_dns_zone_model_list()
        return await ZoneClass.get_cached_dns_zone_by_ip(ip)

    @staticmethod
    async def ok_alert(dns: DnsSearchResult):
        cloudflare_dns_zone.update_dns_ok(dns)
        await ServersState.remove(dns.ip)

    @staticmethod
    async def fail_alert(dns: DnsSearchResult):
        cloudflare_dns_zone.update_dns_fail(dns)
        await ServersState.add(dns.ip)
        restart_node(dns.ip)

    @staticmethod
    async def get_all_dns() -> list[ZoneModel]:
        # return cloudflare_dns_zone.get_zone_model_list()
        return await DnsZoneState.get_dns_zones()

    @staticmethod
    async def get_servers_for_update() -> dict:
        return await ServersState.get()

    @staticmethod
    async def add_server_for_update(ip: str):
        return await ServersState.add(ip)

    @staticmethod
    async def remove_server_for_update(ip: str):
        return await ServersState.remove(ip)
