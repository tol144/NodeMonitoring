from common.remote.ssh import SSHRemote

from config import settings


class NodeCommandClass:
    def __init__(self, host):
        self.ssh = SSHRemote(host)

    def __del__(self):
        del self.ssh

    def restart(self):
        self.ssh.run_command(settings.restart_node_command())

    def stop(self):
        self.ssh.run_command(settings.stop_node_command())
