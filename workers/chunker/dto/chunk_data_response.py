from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class ChunkedDataResponse(BaseModel):
    chunk_id: UUID
    raw_data_id: UUID
    chunk_content: str
    status: str
    chunk_index: int
    created_at: datetime
