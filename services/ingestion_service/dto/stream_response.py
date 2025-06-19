from datetime import datetime
from typing import Optional, Union

from services.ingestion_service.dto.close_connection_payload import CloseConnectionPayload
from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.meet_payload import MeetPayload
from services.ingestion_service.dto.init_payload import InitPayload
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse
from services.ingestion_service.enums.db_status import DbStatus
from services.ingestion_service.enums.stream_event_type import StreamEventType
from services.ingestion_service.enums.stream_response_status import StreamResponseStatus
from pydantic import BaseModel



class StreamResponse(BaseModel):
    event_type: StreamEventType
    status: StreamResponseStatus
    raw_data_id: str
    transcript: Optional[str] = None
    db_status: Optional[DbStatus] = None
    ingestion_ts: Optional[datetime] = None
    error_msg: Optional[str] = None

    def to_ingestion_request(self, payload: Union[InitPayload, MeetPayload, CloseConnectionPayload]) -> 'IngestionRequest':
        return IngestionRequest(
            user_id=payload.user_id,
            data_source=payload.input_data_source,
            content=self.transcript or '',
            metadata={}
        )

    def to_storage_service_response(self, payload: Union[InitPayload, MeetPayload, CloseConnectionPayload]) -> 'StorageServiceResponse':
        return StorageServiceResponse(
            user_id=payload.user_id,
            raw_data_id=self.raw_data_id,
            status=self.db_status.name,
            ingestion_timestamp=self.ingestion_ts,
            data_input_source=payload.input_data_source
        )