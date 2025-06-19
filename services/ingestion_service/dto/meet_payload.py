from services.ingestion_service.dto.payload import Payload
from pydantic import BaseModel

class MeetPayload(BaseModel, Payload):
    audio_blob: str
    audio_format: str
    raw_data_id: str
    audio_chunk_index: int