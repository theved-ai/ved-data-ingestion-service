from datetime import datetime

from pydantic import BaseModel


class RawDataKafkaEvent(BaseModel):
    raw_data_id: str
    user_id: str
    data_input_source: str
    status: str
    ingestion_timestamp: datetime
    event_published_at: datetime
    content_timestamp: datetime