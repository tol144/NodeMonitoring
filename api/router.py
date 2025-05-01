from fastapi import APIRouter

from api.methods import APIMethods
from services.cloudflare.model import ZoneModel

api_router = APIRouter()


@api_router.post("/kuma/alert")
async def kuma_alert(alert_json: dict):
    await APIMethods.process_alert(alert_json)


@api_router.get("/cloudflare/zone",
                response_model=list[ZoneModel])
async def cloudflare_zone_list():
    return await APIMethods.get_all_dns()


@api_router.get("/servers/waiting_for_update",
                response_model=dict)
async def get_servers_for_update():
    return await APIMethods.get_servers_for_update()


@api_router.get("/servers/add",
                response_model=str)
async def add_server_for_update(ip: str):
    await APIMethods.add_server_for_update(ip)
    return "OK"


@api_router.get("/servers/remove",
                response_model=str)
async def remove_server_for_update(ip: str):
    await APIMethods.remove_server_for_update(ip)
    return "OK"
