from abc import ABC, abstractmethod

from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse
from services.ingestion_service.enums.input_data_source import InputDataSource

class StorageServiceBase(ABC):

    @abstractmethod
    def supported_data_source(self) -> list[InputDataSource]:
        pass

    @abstractmethod
    async def process(self, request: IngestionRequest) -> StorageServiceResponse:
        pass