from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RawDataResponse(BaseModel):
    raw_data_id: UUID
    user_id: UUID
    content: str
    data_source: str
    created_at: datetime
    status: str
    metadata: str