from typing import Dict, List, Callable, Any
from collections import deque
from datetime import datetime
from uuid import UUID

class Message:
    def __init__(self, event_type: str, payload: Dict[str, Any]):
        self.event_type = event_type
        self.payload = payload
        self.timestamp = datetime.utcnow()
        self.processed = False

class MessageQueue:
    def __init__(self):
        self._queue = deque()
        self._handlers: Dict[str, List[Callable]] = {}

    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish a message to the queue"""
        message = Message(event_type, payload)
        self._queue.append(message)
        # In a real implementation, this would trigger async processing
        # For this demo, we'll just mark it as processed
        message.processed = True

    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Register a handler for a specific event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def get_messages(self) -> List[Message]:
        """Get all messages in the queue"""
        return list(self._queue)

# Global message queue instance
message_queue = MessageQueue()

# Example event types
PAYMENT_CREATED = "payment.created"
PAYMENT_UPDATED = "payment.updated"
ACCOUNT_CREATED = "account.created"
ACCOUNT_UPDATED = "account.updated" 