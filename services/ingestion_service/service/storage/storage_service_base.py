from abc import ABC, abstractmethod
from typing import Optional

from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.meet_payload import MeetPayload
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse
from services.ingestion_service.enums.input_data_source import InputDataSource

class StorageServiceBase(ABC):

    @abstractmethod
    def supported_data_source(self) -> list[InputDataSource]:
        pass

    @abstractmethod
    async def process(self, request: IngestionRequest) -> StorageServiceResponse:
        pass

    @abstractmethod
    async def save_audio_chunk(self, request: MeetPayload) -> Optional[str]:
        pass

    @abstractmethod
    async def save_audio_chunk_transcript(self, transcript: str, chunk_id: str):
        pass

    @abstractmethod
    async def get_audio_chunks(self, raw_data_id):
        pass

    @abstractmethod
    async def save_transcript(self, final_stitched_transcript, raw_data_id) -> StorageServiceResponse:
        pass