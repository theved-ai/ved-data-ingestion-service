from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChunkedDataConsumedEvent(BaseModel):
    raw_data_id: str
    user_id: str
    chunk_id: str
    chunk_index: int
    chunk_content: str
    data_input_source: str
    status: str
    metadata: str
    ingestion_timestamp: datetime
    event_published_at: datetime
    embedding_model: str
    content_timestamp: Optional[datetime] = None

