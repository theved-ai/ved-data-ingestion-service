from __future__ import annotations

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
    ingestion_timestamp: float
    content_timestamp: float
    event_published_at: float
    model_config = ConfigDict(extra="allow", strict=True)

def build_vector_request(chunk_data_event: 'ChunkedDataConsumedEvent', vector: List[float]) -> VectorRequest:
    metadata_dict: dict[str, Any] = json.loads(chunk_data_event.metadata)

    def safe_timestamp(dt: datetime | None) -> float | None:
        return dt.timestamp() if dt else None

    ingestion_ts = safe_timestamp(chunk_data_event.ingestion_timestamp)
    content_ts = safe_timestamp(chunk_data_event.content_timestamp) or ingestion_ts
    event_published_ts = safe_timestamp(chunk_data_event.event_published_at)

    return VectorRequest(
        user_id=chunk_data_event.user_id,
        embedding_model=chunk_data_event.embedding_model,
        chunk_id=chunk_data_event.chunk_id,
        chunk_index=chunk_data_event.chunk_index,
        vector=vector,
        data_input_source=chunk_data_event.data_input_source,
        status=chunk_data_event.status,
        ingestion_timestamp=ingestion_ts,
        content_timestamp=content_ts,
        event_published_at=event_published_ts,
        **metadata_dict
    )
