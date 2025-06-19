from services.ingestion_service.dto.payload import Payload
from pydantic import BaseModel

class CloseConnectionPayload(Payload, BaseModel):
    raw_data_id: str