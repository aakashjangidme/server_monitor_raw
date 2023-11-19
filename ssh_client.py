from abc import ABC, abstractmethod


class SSHClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def execute_command(self, command: str) -> str:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
