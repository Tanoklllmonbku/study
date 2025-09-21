from abc import ABC, abstractmethod
from typing import Union, Any


class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        pass