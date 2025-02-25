from fastapi import APIRouter

from api.methods import APIMethods
from services.cloudflare.model import ZoneModel

api_router = APIRouter()


@api_router.post("/kuma/alert")
async def kuma_alert(alert_json: dict):
    APIMethods.process_alert(alert_json)


@api_router.get("/cloudflare/zone",
                response_model=list[ZoneModel])
async def cloudflare_zone_list():
    return APIMethods.get_all_dns()
