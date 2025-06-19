from abc import ABC, abstractmethod

from services.ingestion_service.dto.payload import Payload
from services.ingestion_service.dto.stream_response import StreamResponse
from services.ingestion_service.enums.stream_event_type import StreamEventType


class StreamHandlerBase(ABC):

    @abstractmethod
    def supported_event_type(self) -> StreamEventType:
        pass

    @abstractmethod
    async def handle(self, payload: Payload) -> StreamResponse:
        pass