from datetime import datetime
from services.cloudflare.state import ServersState
from services.node.methods import reboot_node


async def reboot_servers():
    servers = await ServersState.get()
    if not servers:
        return

    current_time = datetime.now()
    servers_for_reboot = [ip for ip, expire_time in servers
                          if datetime.fromisoformat(expire_time) >= current_time]
    if not servers_for_reboot:
        return

    for ip in servers_for_reboot:
        reboot_node(ip)
        await ServersState.remove(ip)
