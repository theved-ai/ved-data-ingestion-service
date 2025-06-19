from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.init_payload import InitPayload
from services.ingestion_service.dto.stream_response import StreamResponse
from services.ingestion_service.enums.stream_event_type import StreamEventType
from services.ingestion_service.enums.stream_response_status import StreamResponseStatus
from services.ingestion_service.registry.event_type_to_handler_registry import EventTypeHandlerRegistry
from services.ingestion_service.registry.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.stream_handler.stream_handler_base import StreamHandlerBase


@EventTypeHandlerRegistry.register_handler
class StreamInitHandler(StreamHandlerBase):
    def __init__(self):
        self.storage_registry = InputDataSourceToServiceRegistry()

    def supported_event_type(self) -> StreamEventType:
        return StreamEventType.init

    async def handle(self, payload: InitPayload) -> StreamResponse:
        storage_service = self.storage_registry.get_storage_service(payload.input_data_source)
        raw_data_ingestion_req = IngestionRequest(
            user_id=payload.user_id,
            data_source=payload.input_data_source
        )
        raw_data_record = await storage_service.process(raw_data_ingestion_req)
        return StreamResponse(
            event_type=self.supported_event_type().name,
            status=StreamResponseStatus.success,
            raw_data_id=raw_data_record.raw_data_id
        )