from abc import ABC, abstractmethod


class RemoteConnection(ABC):
    def __init__(self,
                 hostname,
                port,
                username):
        self.connect(hostname,
                     port,
                     username)

    def __del__(self):
        self.close()

    @abstractmethod
    def connect(self,
                hostname,
                port,
                username):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def run_command(self, command):
        pass
