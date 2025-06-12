from datetime import datetime
from pydantic import BaseModel
from services.ingestion_service.enums.input_data_source import InputDataSource


class StorageServiceResponse(BaseModel):
    user_id: str
    raw_data_id: str
    status: str
    ingestion_timestamp: datetime
    data_input_source: InputDataSource