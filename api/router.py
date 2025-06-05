from fastapi import APIRouter

from api.methods import APIMethods
from services.cloudflare.model import ZoneModel
from services.cloudflare.zone_class import cloudflare_dns_zone

api_router = APIRouter()


@api_router.post("/kuma/alert")
async def kuma_alert(alert_json: dict):
    await APIMethods.process_alert(alert_json)


@api_router.get("/cloudflare/zones",
                response_model=list[ZoneModel])
async def cloudflare_zone_list():
    return await APIMethods.get_all_dns()


@api_router.post("/cloudflare/zones/update",
                 response_model=str)
async def update_cloudflare_zone_list() -> str:
    await cloudflare_dns_zone.cache_dns_zone_model_list()
    return "OK"


@api_router.post("/cloudflare/zones/turn_on",
                 response_model=str)
async def cloudflare_zone_turn_on(ip: str) -> str:
    dns = await APIMethods.get_dns_zone(ip)
    if dns is None:
        return "Сервер не найден"

    await APIMethods.turn_on_node(dns)
    return "OK"


@api_router.post("/cloudflare/zones/turn_off",
                 response_model=str)
async def cloudflare_zone_turn_off(ip: str) -> str:
    dns = await APIMethods.get_dns_zone(ip)
    if dns is None:
        return "Сервер не найден"

    await APIMethods.turn_off_node(dns)
    return "OK"


@api_router.get("/servers/waiting_for_update",
                response_model=dict)
async def get_servers_for_update():
    return await APIMethods.get_servers_for_update()


@api_router.get("/servers/add",
                response_model=str)
async def add_server_for_update(ip: str) -> str:
    await APIMethods.add_server_for_update(ip)
    return "OK"


@api_router.get("/servers/remove",
                response_model=str)
async def remove_server_for_update(ip: str) -> str:
    await APIMethods.remove_server_for_update(ip)
    return "OK"
