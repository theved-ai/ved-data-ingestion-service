from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse
from services.ingestion_service.enums.input_data_source import InputDataSource
from services.ingestion_service.service.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.storage_service_base import StorageServiceBase
from services.ingestion_service.db.db_processor import insert_raw_data


@InputDataSourceToServiceRegistry.register_service
class PostgresStorageService(StorageServiceBase):
    def supported_data_source(self) -> list[InputDataSource]:
        return [
            InputDataSource.USER_TYPED,
            InputDataSource.MEET_TRANSCRIPT,
            InputDataSource.SLACK,
            InputDataSource.PDF,
            InputDataSource.WEB_PAGE,
            InputDataSource.YT_TRANSCRIPT
        ]

    async def process(self, request: IngestionRequest) -> StorageServiceResponse:
        return await insert_raw_data(request)