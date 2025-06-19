from services.ingestion_service.dto.payload import Payload
from pydantic import BaseModel

class InitPayload(BaseModel, Payload):
    pass