from core.Base import BaseSyncMixin
import socket
from typing import Optional, Callable
from core.events import ServerEvent

class SyncClient(BaseSyncMixin):

    def __init__(self, host: str, port: int,
                 event_callback: Optional[Callable[[ServerEvent], None]] = None):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self._is_connected = False
        self._is_running = False
        self._event_callback = event_callback

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._is_running = True
            self.socket.connect((self.host, self.port))
            self._is_connected = True
            start_event = ServerEvent.server_started(self.host, self.port)
            self._notify_event(start_event)
        except Exception as e:
            self._is_connected = False
            self._is_running = False
            error_event = ServerEvent.server_stopped(self.host, self.port)
            self._notify_event(error_event)
            raise

    def send(self, data:bytes):
        try:
            self.socket.sendall(data)
            sent_event = ServerEvent.message_sent(len(data), data[:100])
            self._notify_event(sent_event)
        except socket.timeout:
            timeout_event = ServerEvent.error_timeout("send", 0.0)
            self._notify_event(timeout_event)
            raise TimeoutError("Send operation timed out")
        except (ConnectionError, OSError) as e:
            error_event = ServerEvent.error_connection("send", str(e))
            self._notify_event(error_event)
            raise ConnectionError(f"Send operation failed: {e}")

    def recv(self) -> bytes:
        if self.socket:
            try:
                data = self.socket.recv(1024)
                if data:
                    received_event = ServerEvent.message_received(len(data), data[:100])
                    self._notify_event(received_event)
                else:
                    self.close()
                    raise ConnectionError("Disconnected")
                return data

            except socket.timeout:
                timeout_event = ServerEvent.error_timeout("receive", 0.0)
                self._notify_event(timeout_event)
                raise TimeoutError("Receive operation timed out")
            except (ConnectionError, OSError) as e:
                error_event = ServerEvent.error_connection("receive", str(e))
                self._notify_event(error_event)
                raise ConnectionError(f"Receive operation failed: {e}")

    def close_connection(self):
        if self.socket:
            if self._is_connected:
                disconnect_event = ServerEvent.client_disconnected()
                self._notify_event(disconnect_event)
            self.socket.close()
            self.socket = None
        self._is_connected = False

    def close(self):
        self.close_connection()
        self._is_running = False
        stop_event = ServerEvent.server_stopped(self.host, self.port)
        self._notify_event(stop_event)

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def is_running(self) -> bool:
        return self._is_running

    def _notify_event(self, event: ServerEvent):
        if self._event_callback:
            try:
                self._event_callback(event)
            except Exception as e:
                raise f"Event callback failed: {e}"