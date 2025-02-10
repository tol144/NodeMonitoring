from fastapi import APIRouter

from api.methods import APIMethods


api_router = APIRouter()


@api_router.post("/kuma/alert")
async def kuma_alert(alert_json: dict):
    APIMethods.process_alert(alert_json)
