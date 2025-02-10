import paramiko

from config import settings
from common.remote.remote_connection import RemoteConnection


class SSHRemote(RemoteConnection):
    def __init__(self,
                 hostname):
        self.ssh = None
        port = settings.ssh_port
        username = settings.ssh_username
        super().__init__(hostname,
                         port,
                         username)

    def connect(self,
                hostname,
                port,
                username):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        private_key = paramiko.RSAKey.from_private_key_file(settings.ssh_key_path)
        self.ssh.connect(hostname,
                         port=port,
                         username=username,
                         pkey=private_key)

    def run_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        return output, error

    def close(self):
        self.ssh.close()
