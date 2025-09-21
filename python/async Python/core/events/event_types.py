from enum import Enum

class EventCategory(Enum):
    SERVER = "server"
    CLIENT = "client"
    ERROR = "error"
    MESSAGE = "message"


class EventType:
    SERVER_STARTED = (EventCategory.SERVER, "started")
    SERVER_STOPPED = (EventCategory.SERVER, "stopped")
    SERVER_SEND = (EventCategory.SERVER, "send")
    SERVER_RECEIVE = (EventCategory.SERVER, "receive")
    SERVER_DISCONNECT_CLIENT = (EventCategory.SERVER, "disconnect_client")

    CLIENT_CONNECTED = (EventCategory.CLIENT, "connected")
    CLIENT_DISCONNECTED = (EventCategory.CLIENT, "disconnected")
    CLIENT_SEND = (EventCategory.CLIENT, "send")
    CLIENT_RECEIVE = (EventCategory.CLIENT, "receive")

    ERROR_TIMEOUT = (EventCategory.ERROR, "timeout")
    ERROR_INVALID_DATA = (EventCategory.ERROR, "invalid_data")
    ERROR_CONNECTION = (EventCategory.ERROR, "connection")

    MESSAGE_SENT = (EventCategory.MESSAGE, "sent")
    MESSAGE_RECEIVED = (EventCategory.MESSAGE, "received")

    @staticmethod
    def get_full_name(event_type):
        category, name = event_type
        return f"{category.value}_{name}"