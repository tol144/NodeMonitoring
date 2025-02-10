from cloudflare import Cloudflare

from config import settings


class BaseCloudFlare:
    def __init__(self):
        self.client = Cloudflare(
            api_email=settings.cloudflare_email,
            api_key=settings.cloudflare_api_key,
        )

    def get_zones_resource(self):
        return self.client.zones

    def get_dns_resources(self):
        return self.client.dns
