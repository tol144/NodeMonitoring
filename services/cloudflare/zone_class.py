from services.cloudflare.cloudflare import BaseCloudFlare

from common.ip import is_valid_ip
from services.cloudflare.model import DnsZoneModel, ZoneModel, DnsSearchResult


class ZoneClass(BaseCloudFlare):
    def get_zone_model_list(self) -> list[ZoneModel]:
        zone_resource = self.get_zones_resource().list()
        zone_list = zone_resource.result
        zone_id_list = []
        for zone in zone_list:
            zone_id = zone.id
            dns = self.get_zone_dns_model_list(zone_id)
            zone_model = ZoneModel(id=zone.id,
                                   dns=dns)
            zone_id_list.append(zone_model)

        return zone_id_list

    def get_zone_dns_model_list(self, zone_id: str) -> list[DnsZoneModel]:
        record_list = self.get_dns_resources().records.list(zone_id=zone_id)
        dns_model_list = []
        for record in record_list:
            ip = record.content
            if not is_valid_ip(ip):
                continue

            try:
                dns_model = DnsZoneModel(zone_id=zone_id,
                                         id=record.id,
                                         ip=ip,
                                         name=record.name)
            except Exception:
                continue

            dns_model_list.append(dns_model)

        return dns_model_list

    def update_dns(self,
                   dns: DnsSearchResult,
                   name: str):
        dns_resource = self.get_dns_resources()
        dns_resource.records.edit(zone_id=dns.zone_id,
                                  dns_record_id=dns.id,
                                  name=name)

    @staticmethod
    def find_dns_zone_by_ip(zone_model_list: list[ZoneModel],
                            ip: str) -> DnsSearchResult | None:
        for zone_model in zone_model_list:
            search_result = zone_model.find_by_ip(ip)
            if search_result is not None:
                return search_result

        return None

    def get_dns_zone_by_ip(self, ip: str) -> DnsSearchResult | None:
        zone_model_list = self.get_zone_model_list()
        return self.find_dns_zone_by_ip(zone_model_list, ip)


cloudflare_dns_zone = ZoneClass()
