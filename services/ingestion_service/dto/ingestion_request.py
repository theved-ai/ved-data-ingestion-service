from dataclasses import dataclass

from services.ingestion_service.enums.input_data_source import InputDataSource


@dataclass
class IngestionRequest:
    user_uuid: str
    data_source: InputDataSource
    content: str
    metadata: dict
