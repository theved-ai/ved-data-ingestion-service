from dataclasses import dataclass
from datetime import datetime

from services.ingestion_service.enums.input_data_source import InputDataSource


@dataclass
class StorageServiceResponse:
    user_id: str
    raw_data_id: str
    status: str
    ingestion_timestamp: datetime
    data_input_source: InputDataSource