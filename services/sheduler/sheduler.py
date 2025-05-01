from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.timezone import local_timezone
from services.cloudflare.zone_class import cloudflare_dns_zone
from services.sheduler.reboot_servers import reboot_servers


class Scheduler:
    @staticmethod
    async def start():
        scheduler = AsyncIOScheduler(timezone=local_timezone.timezone_param)
        scheduler.add_job(cloudflare_dns_zone.cache_dns_zone_model_list,
                          trigger='interval',
                          minutes=15)
        scheduler.add_job(reboot_servers,
                          trigger='interval',
                          minutes=1)
        scheduler.start()
