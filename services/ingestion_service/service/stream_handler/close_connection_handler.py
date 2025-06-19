from typing import List

from services.ingestion_service.dto.audio_chunk_response import AudioChunk
from services.ingestion_service.dto.close_connection_payload import CloseConnectionPayload
from services.ingestion_service.dto.stream_response import StreamResponse
from services.ingestion_service.enums.stream_event_type import StreamEventType
from services.ingestion_service.enums.stream_response_status import StreamResponseStatus
from services.ingestion_service.registry.event_type_to_handler_registry import EventTypeHandlerRegistry
from services.ingestion_service.registry.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.stream_handler.stream_handler_base import StreamHandlerBase


def _order_audio_chunks(chunks: List[AudioChunk]) -> List[AudioChunk]:
    return sorted(chunks, key=lambda chunk: chunk.chunk_index)


def _stitch_transcript(audio_chunk_transcript_ordered):
    return ' '.join(audio_chunk.transcript for audio_chunk in audio_chunk_transcript_ordered)


@EventTypeHandlerRegistry.register_handler
class CloseConnectionHandler(StreamHandlerBase):
    def __init__(self):
        self.storage_registry = InputDataSourceToServiceRegistry()

    def supported_event_type(self) -> StreamEventType:
        return StreamEventType.close_connection


    async def handle(self, payload: CloseConnectionPayload) -> StreamResponse:
        storage_service = self.storage_registry.get_storage_service(payload.input_data_source)
        audio_chunk_transcript_unordered = await storage_service.get_audio_chunks(payload.raw_data_id)
        audio_chunk_transcript_ordered = _order_audio_chunks(audio_chunk_transcript_unordered)
        final_stitched_transcript = _stitch_transcript(audio_chunk_transcript_ordered)
        storage_service_response = await storage_service.save_transcript(final_stitched_transcript, payload.raw_data_id)
        return StreamResponse(
            event_type=self.supported_event_type().value,
            status=StreamResponseStatus.success,
            raw_data_id=storage_service_response.raw_data_id,
            transcript=final_stitched_transcript,
            db_status=storage_service_response.status,
            ingestion_ts=storage_service_response.ingestion_timestamp
        )


