from typing import Optional, Dict

from pydantic import BaseModel

from services.ingestion_service.enums.input_data_source import InputDataSource


class IngestionRequest(BaseModel):
    user_id: str
    data_source: InputDataSource
    content: str
    metadata: Optional[Dict[str, str]] = {}
