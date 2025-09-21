from abc import ABC, abstractmethod


class BaseSyncConnectable(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def accept_client(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        pass


class BaseAsyncConnectable(ABC):

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def close_connection(self):
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        pass


class BaseSyncSendRecv(ABC):

    @abstractmethod
    def send(self, data: bytes):
        pass

    @abstractmethod
    def recv(self) -> bytes:
        pass

class BaseAsyncSendRecv(ABC):

    @abstractmethod
    def send(self, data: bytes):
        pass

    @abstractmethod
    def recv(self) -> bytes:
        pass


class BaseSyncMixin(BaseSyncConnectable, BaseSyncSendRecv, ABC):
    """Комбинированный интерфейс для синхронных миксинов"""
    pass

class BaseAsyncMixin(BaseAsyncConnectable, BaseAsyncSendRecv, ABC):
    """Комбинированный интерфейс для асинхронных миксинов"""
    pass
