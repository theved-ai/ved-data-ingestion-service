from typing import Dict, Type

from services.ingestion_service.enums.stream_event_type import StreamEventType
from services.ingestion_service.service.stream_handler.stream_handler_base import StreamHandlerBase


class EventTypeHandlerRegistry:

    _event_type_handler_registry: Dict[StreamEventType, StreamHandlerBase] = {}

    @classmethod
    def register_handler(cls, service_cls: Type["StreamHandlerBase"]):
        instance = service_cls()
        if cls._event_type_handler_registry.get(instance.supported_event_type()):
            raise ValueError(f'Event type: {instance.supported_event_type().value} already registered')
        cls._event_type_handler_registry[instance.supported_event_type()] = instance

    def get_handler(self, event_type: StreamEventType):
        if not self._event_type_handler_registry.get(event_type):
            raise ValueError(f'No handler registered for event type: {event_type.value}')
        return self._event_type_handler_registry.get(event_type)