from typing import Union

from pydantic import BaseModel

from services.ingestion_service.dto.close_connection_payload import CloseConnectionPayload
from services.ingestion_service.dto.init_payload import InitPayload
from services.ingestion_service.dto.meet_payload import MeetPayload
from services.ingestion_service.enums.stream_event_type import StreamEventType


class AudioIngestionRequest(BaseModel):
    event_type: StreamEventType
    payload: Union[InitPayload, MeetPayload, CloseConnectionPayload]