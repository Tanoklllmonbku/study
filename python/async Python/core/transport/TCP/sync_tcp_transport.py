from core.Base import BaseSyncMixin
from core.Base.base_transport import BaseTransport
from core.serializers.TCP_serializer import TCPSerializer
from core.mixin.TCP.SyncServer import SyncServer
from typing import Any


class SyncTCPTransport(BaseTransport):
    def __init__(self, mixin: BaseSyncMixin, serializer: TCPSerializer):
        super().__init__(mixin, serializer)

    def start(self):
        return self.mixin.start()

    def close(self):
        return self.mixin.close()

    def close_connection(self):
        return self.mixin.close_connection()

    def send(self, data: bytes):
        return self.mixin.send(self.serializer.serialize(data))

    def recv(self) -> Any:
        return self.serializer.deserialize(self.mixin.recv())

    def is_connected(self):
        return self.mixin.is_connected

    def is_running(self):
        return self.mixin.is_running

transport = SyncTCPTransport(SyncServer("localhost", 8080), TCPSerializer())
transport.start()