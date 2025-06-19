from abc import ABC

from services.ingestion_service.enums.input_data_source import InputDataSource


class Payload(ABC):
    input_data_source: InputDataSource
    user_id: str