from typing import Optional

from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.meet_payload import MeetPayload
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse
from services.ingestion_service.enums.db_status import DbStatus
from services.ingestion_service.enums.input_data_source import InputDataSource
from services.ingestion_service.registry.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.storage.storage_service_base import StorageServiceBase
from services.ingestion_service.db.db_processor import insert_raw_data, insert_audio_chunks, \
    update_audio_chunk_transcript, update_raw_data_status, fetch_audio_chunks, save_raw_data_transcript


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

    async def update_status(self, raw_data_id, status):
        return await update_raw_data_status(raw_data_id, status)

    async def save_audio_chunk(self, request: MeetPayload) -> Optional[str]:
        await self.update_status(request.raw_data_id, DbStatus.TRANSCRIPTION_IN_PROGRESS)
        return await insert_audio_chunks(request)

    async def save_audio_chunk_transcript(self, transcript: str, chunk_id: str):
        return await update_audio_chunk_transcript(transcript, chunk_id)

    async def get_audio_chunks(self, raw_data_id):
        return await fetch_audio_chunks(raw_data_id)

    async def save_transcript(self, final_stitched_transcript, raw_data_id) -> StorageServiceResponse:
        return await save_raw_data_transcript(final_stitched_transcript, raw_data_id)