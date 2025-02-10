from pydantic import BaseModel


class DnsSearchResult(BaseModel):
    id: str
    ip: str
    zone_id: str


class DnsZoneModel(BaseModel):
    id: str
    name: str
    ip: str


class ZoneModel(BaseModel):
    id: str
    dns: list[DnsZoneModel] | None

    def find_by_ip(self, ip: str) -> DnsSearchResult | None:
        for dns in self.dns:
            if dns.ip == ip:
                return DnsSearchResult(id=dns.id,
                                       ip=ip,
                                       zone_id=self.id)

        return None
