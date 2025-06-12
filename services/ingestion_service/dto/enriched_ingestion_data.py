from datetime import datetime

from pydantic import BaseModel

from services.ingestion_service.enums.input_data_source import InputDataSource


class EnrichedIngestionData(BaseModel):
    user_id: str
    raw_data_id: str
    status: str
    ingestion_timestamp: datetime
    data_input_source: InputDataSource
    content_timestamp: datetime
    event_published_at_timestamp: datetime