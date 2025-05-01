import json
from datetime import datetime, timedelta

from services.cloudflare.model import ZoneModel
from services.cache.redis.redis import redis_cache

DNS_ZONES_KEY = 'dns_zones'
SERVERS_WAITING_FOR_UPDATES_KEY = 'servers_waiting_for_updates'


class DnsZoneState:
    @staticmethod
    async def set_dns_zones(zones: list[ZoneModel]) -> None:
        zones_json = json.dumps([zone.model_dump() for zone in zones])
        await redis_cache.set(DNS_ZONES_KEY, zones_json)

    @staticmethod
    async def get_dns_zones() -> list[ZoneModel]:
        zones_json = await redis_cache.get(DNS_ZONES_KEY)
        if zones_json is None:
            return []

        zones_data = json.loads(zones_json)
        return [ZoneModel(**zone_data) for zone_data in zones_data]


class ServersState:
    @staticmethod
    async def add(ip: str, expire_minutes: int = 10) -> None:
        expire_time = (datetime.now() + timedelta(minutes=expire_minutes)).isoformat()

        servers_data = await redis_cache.get(SERVERS_WAITING_FOR_UPDATES_KEY)
        servers = json.loads(servers_data) if servers_data else {}
        servers[ip] = expire_time

        await redis_cache.set(SERVERS_WAITING_FOR_UPDATES_KEY, json.dumps(servers))

    @staticmethod
    async def remove(ip: str) -> bool:
        servers_data = await redis_cache.get(SERVERS_WAITING_FOR_UPDATES_KEY)
        if not servers_data:
            return False

        servers = json.loads(servers_data)
        if ip not in servers:
            return False

        del servers[ip]

        await redis_cache.set(SERVERS_WAITING_FOR_UPDATES_KEY, json.dumps(servers))
        return True

    @staticmethod
    async def get() -> dict:
        servers_data = await redis_cache.get(SERVERS_WAITING_FOR_UPDATES_KEY)
        return json.loads(servers_data) if servers_data else {}
