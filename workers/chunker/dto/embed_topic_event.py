from datetime import datetime
from typing import Optional

import pytz
from pydantic import BaseModel

from workers.chunker.dto.chunk_data import ChunkData
from workers.chunker.dto.chunk_data_response import ChunkedDataResponse
from workers.chunker.utils.application_constants import EMBEDDING_MODEL_NAME


def from_chunk(chunk_data_req: ChunkData, chunk_data_db: ChunkedDataResponse):
    return EmbedTopicEvent(
        raw_data_id=chunk_data_req.raw_data_id,
        user_id=chunk_data_req.user_id,
        chunk_id=chunk_data_req.uuid,
        chunk_index=chunk_data_req.chunk_index,
        chunk_content=chunk_data_req.chunk_content,
        data_input_source=chunk_data_req.data_input_source,
        status=chunk_data_db.status,
        ingestion_timestamp=chunk_data_db.created_at,
        content_timestamp=None,
        event_published_at=datetime.now(tz=pytz.timezone('Asia/Kolkata')),
        embedding_model=EMBEDDING_MODEL_NAME
    )


class EmbedTopicEvent(BaseModel):
    raw_data_id: str
    user_id: str
    chunk_id: str
    chunk_index: int
    chunk_content: str
    data_input_source: str
    status: str
    ingestion_timestamp: datetime
    event_published_at: datetime
    embedding_model: str
    content_timestamp: Optional[datetime] = None

