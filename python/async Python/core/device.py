from events import ServerEvent, EventCategory
from mixin.TCP.SyncServer import SyncServer


class CategoryAwareObserver:
    def __init__(self):
        self.stats = {
            'clients_connected': 0,
            'messages_sent': 0,
            'messages_received': 0,
            'errors': 0
        }

    def on_event(self, event: ServerEvent):
        """Обработчик с фильтрацией по категориям"""

        # Фильтрация по категории
        if event.category == EventCategory.CLIENT:
            self._handle_client_event(event)

        elif event.category == EventCategory.MESSAGE:
            self._handle_message_event(event)

        elif event.category == EventCategory.ERROR:
            self._handle_error_event(event)

        elif event.category == EventCategory.SERVER:
            self._handle_server_event(event)

    def _handle_client_event(self, event: ServerEvent):
        if event.name == "connected":
            self.stats['clients_connected'] += 1
            print(f"📡 Client connected (total: {self.stats['clients_connected']})")

        elif event.name == "disconnected":
            print("📡 Client disconnected")

    def _handle_message_event(self, event: ServerEvent):
        if event.name == "sent":
            self.stats['messages_sent'] += 1
            print(f"📤 Message sent (total: {self.stats['messages_sent']})")

        elif event.name == "received":
            self.stats['messages_received'] += 1
            print(f"📥 Message received (total: {self.stats['messages_received']})")

    def _handle_error_event(self, event: ServerEvent):
        self.stats['errors'] += 1
        print(f"❌ Error: {event.name} (total: {self.stats['errors']})")

    def _handle_server_event(self, event: ServerEvent):
        if event.name == "started":
            print("🚀 Server started")
        elif event.name == "stopped":
            print("🛑 Server stopped")


# Использование
observer = CategoryAwareObserver()
server = SyncServer('localhost', 8888, event_callback=observer.on_event)
print(server.is_connected)
server.start()
print(server.is_running)