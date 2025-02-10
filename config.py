import json
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    UVICORN_HOST: str
    UVICORN_PORT: int

    UPTIME_KUMA_URL: str
    UPTIME_KUMA_USERNAME: str
    UPTIME_KUMA_PASSWORD: str
    UPTIME_KUMA_API_KEY: str

    CLOUDFLARE_EMAIL: str
    CLOUDFLARE_API_KEY: str

    SSH_PORT: str
    SSH_USERNAME: str
    SSH_KEY_PATH: str

    RESTART_NODE_COMMAND: str
    STOP_NODE_COMMAND: str

    OK_CLOUDFLARE_URL: str
    FAIL_CLOUDFLARE_URL: str

    @property
    def uvicorn_host(self):
        return self.UVICORN_HOST

    @property
    def uvicorn_port(self):
        return self.UVICORN_PORT

    @property
    def uptime_kuma_url(self):
        return self.UPTIME_KUMA_URL

    @property
    def uptime_kuma_username(self):
        return self.UPTIME_KUMA_USERNAME

    @property
    def uptime_kuma_password(self):
        return self.UPTIME_KUMA_PASSWORD

    @property
    def uptime_kuma_api_key(self):
        return self.UPTIME_KUMA_API_KEY

    @property
    def cloudflare_email(self):
        return self.CLOUDFLARE_EMAIL

    @property
    def cloudflare_api_key(self):
        return self.CLOUDFLARE_API_KEY

    @property
    def ssh_port(self):
        return self.SSH_PORT

    @property
    def ssh_username(self):
        return self.SSH_USERNAME

    @property
    def ssh_key_path(self):
        return self.SSH_KEY_PATH

    @property
    def restart_node_command(self):
        return self.RESTART_NODE_COMMAND

    @property
    def stop_node_command(self):
        return self.STOP_NODE_COMMAND

    @property
    def ok_cloudflare_url(self):
        return self.OK_CLOUDFLARE_URL

    @property
    def fail_cloudflare_url(self):
        return self.FAIL_CLOUDFLARE_URL

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
