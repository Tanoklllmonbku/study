from abc import ABC, abstractmethod
from typing import Any

from core.Base import BaseTransport
from core.Base.base_parser import BaseParser


class BaseSyncProtocol(ABC):
    def __init__(self, transport: BaseTransport, parser: BaseParser):
        self._transport = transport
        self._parser = parser

    @abstractmethod
    def start_server(self):
        pass

    @abstractmethod
    def stop_server(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send(self, data: Any):
        pass

    @abstractmethod
    def recv(self) -> Any:
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        pass


class BaseAsyncProtocol(ABC):
    def __init__(self, transport: BaseTransport, parser: BaseParser):
        self._transport = transport
        self._parser = parser

    @abstractmethod
    def start_server(self):
        pass

    @abstractmethod
    def stop_server(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send(self, data: Any):
        pass

    @abstractmethod
    def recv(self) -> Any:
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        pass