from .event_types import EventType, EventCategory
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time


@dataclass
class ServerEvent:
    event_type: tuple  # (EventCategory, str)
    timestamp: float
    details: Optional[Dict[str, Any]] = None

    @property
    def category(self) -> EventCategory:
        return self.event_type[0]

    @property
    def name(self) -> str:
        return self.event_type[1]

    @property
    def full_name(self) -> str:
        return EventType.get_full_name(self.event_type)

    def to_dict(self) -> Dict[str, Any]:
        category, name = self.event_type
        return {
            'category': category.value,
            'name': name,
            'full_name': self.full_name,
            'timestamp': self.timestamp,
            'details': self.details or {}
        }

    @staticmethod
    def server_started(host: str, port: int) -> 'ServerEvent':
        return ServerEvent(
            event_type=EventType.SERVER_STARTED,
            timestamp=time.time(),
            details={'host': host, 'port': port}
        )

    @staticmethod
    def server_stopped(host: str, port: int) -> 'ServerEvent':
        return ServerEvent(
            event_type=EventType.SERVER_STOPPED,
            timestamp=time.time(),
            details={'host': host, 'port': port}
        )

    @staticmethod
    def client_connected(address: Any, client_id: int) -> 'ServerEvent':
        return ServerEvent(
            event_type=EventType.CLIENT_CONNECTED,
            timestamp=time.time(),
            details={'address': address, 'client_id': client_id}
        )

    @staticmethod
    def client_disconnected(reason: str = "Disconnected by server") -> 'ServerEvent':
        return ServerEvent(
            event_type=EventType.CLIENT_DISCONNECTED,
            timestamp=time.time(),
            details={'reason': reason}
        )

    @staticmethod
    def message_sent(data_size: int, data_preview: bytes = None) -> 'ServerEvent':
        details = {'data_size': data_size}
        if data_preview:
            details['data_preview'] = data_preview
        return ServerEvent(
            event_type=EventType.MESSAGE_SENT,
            timestamp=time.time(),
            details=details
        )

    @staticmethod
    def message_received(data_size: int, data_preview: bytes = None) -> 'ServerEvent':
        details = {'data_size': data_size}
        if data_preview:
            details['data_preview'] = data_preview
        return ServerEvent(
            event_type=EventType.MESSAGE_RECEIVED,
            timestamp=time.time(),
            details=details
        )

    @staticmethod
    def error_timeout(operation: str, duration: float) -> 'ServerEvent':
        return ServerEvent(
            event_type=EventType.ERROR_TIMEOUT,
            timestamp=time.time(),
            details={'operation': operation, 'duration': duration}
        )

    @staticmethod
    def error_invalid_data(operation: str, data: Any = None) -> 'ServerEvent':
        details = {'operation': operation}
        if data is not None:
            details['invalid_data'] = data
        return ServerEvent(
            event_type=EventType.ERROR_INVALID_DATA,
            timestamp=time.time(),
            details=details
        )

    @staticmethod
    def error_connection(operation: str, error: str) -> 'ServerEvent':
        return ServerEvent(
            event_type=EventType.ERROR_CONNECTION,
            timestamp=time.time(),
            details={'operation': operation, 'error': error}
        )

