from typing import Optional, Dict, Any

from pydantic import BaseModel

from services.ingestion_service.enums.input_data_source import InputDataSource


class IngestionRequest(BaseModel):
    user_id: str
    data_source: InputDataSource
    content: Optional[str] = ''
    metadata: Optional[Dict[str, Any]] = {}
