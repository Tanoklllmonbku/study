from core.Base import BaseSerializer


class TCPSerializer(BaseSerializer):

    def serialize(self, data: bytes):
        return int.from_bytes(data, byteorder='big')

    def deserialize(self, data: bytes):
        return int.from_bytes(data, byteorder='big')