from .base_serializer import BaseSerializer
from .base_mixin import BaseSyncMixin, BaseAsyncMixin
from abc import ABC, abstractmethod
from typing import Any, Union


class BaseTransport:
    """
        Base class for transport implementations.

        Designed to separate the concerns of data transmission (transport)
        from data formatting and interaction logic (protocol), enabling
        flexible composition of different transports and protocols.
    """

    def __init__(self, mixin: Union[BaseAsyncMixin, BaseSyncMixin], serializer: BaseSerializer):
        self.mixin = mixin
        self.serializer = serializer

