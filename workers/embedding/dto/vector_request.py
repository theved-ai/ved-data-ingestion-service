import json
from datetime import datetime
from typing import List, Any

from pydantic import BaseModel, ConfigDict

from workers.embedding.dto.chuked_data_consumed_event import ChunkedDataConsumedEvent

class VectorRequest(BaseModel):
    user_id: str
    embedding_model: str
    chunk_id: str
    chunk_index: int
    vector: list[float]
    data_input_source: str
    status: str
    ingestion_timestamp: datetime
    content_timestamp: datetime
    event_published_at: datetime
    model_config = ConfigDict(extra="allow")

def build_vector_request(chunk_data_event: 'ChunkedDataConsumedEvent', vector: List[float]) -> VectorRequest:
    metadata_dict: dict[str, Any] = json.loads(chunk_data_event.metadata)
    return VectorRequest(
        user_id=chunk_data_event.user_id,
        embedding_model=chunk_data_event.embedding_model,
        chunk_id=chunk_data_event.chunk_id,
        chunk_index=chunk_data_event.chunk_index,
        vector=vector,
        data_input_source=chunk_data_event.data_input_source,
        status=chunk_data_event.status,
        ingestion_timestamp=chunk_data_event.ingestion_timestamp,
        content_timestamp=chunk_data_event.content_timestamp or chunk_data_event.ingestion_timestamp,
        event_published_at=chunk_data_event.event_published_at,
        **metadata_dict
    )