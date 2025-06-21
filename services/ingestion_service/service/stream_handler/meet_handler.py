import asyncio

from services.ingestion_service.dto.meet_payload import MeetPayload
from services.ingestion_service.dto.stream_response import StreamResponse
from services.ingestion_service.enums.stream_event_type import StreamEventType
from services.ingestion_service.enums.stream_response_status import StreamResponseStatus
from services.ingestion_service.registry.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.stream_handler.stream_handler_base import StreamHandlerBase
from services.ingestion_service.service.speech_to_text_service import pcm_b64_to_text
from services.ingestion_service.config.logging_config import logger
from services.ingestion_service.registry.event_type_to_handler_registry import EventTypeHandlerRegistry

async def _transcribe_and_save(payload: MeetPayload, storage_service, audio_chunk_id: str):
    try:
        audio_chunk_transcript = pcm_b64_to_text(audio_blob_b64=payload.audio_blob, audio_chunk_index=payload.audio_chunk_index)
        await storage_service.save_audio_chunk_transcript(audio_chunk_transcript, audio_chunk_id)
    except Exception as e:
        logger.exception(f"Failed to transcribe and save audio chunk {audio_chunk_id}: {e}")

@EventTypeHandlerRegistry.register_handler
class MeetHandler(StreamHandlerBase):
    def __init__(self):
        self.storage_registry = InputDataSourceToServiceRegistry()

    def supported_event_type(self) -> StreamEventType:
        return StreamEventType.audio_chunk

    async def handle(self, payload: MeetPayload) -> StreamResponse:
        try:
            storage_service = self.storage_registry.get_storage_service(payload.input_data_source)
            audio_chunk_id = await storage_service.save_audio_chunk(payload)
            await asyncio.create_task(_transcribe_and_save(payload, storage_service, audio_chunk_id))
            return StreamResponse(
                event_type=self.supported_event_type(),
                status=StreamResponseStatus.success,
                raw_data_id=payload.raw_data_id
            )

        except Exception as e:
            logger.exception(f'Error transcribing audio chunk: {e}')
            return StreamResponse(
                event_type=self.supported_event_type(),
                status=StreamResponseStatus.failure,
                raw_data_id=payload.raw_data_id,
                error_msg=str(e)
            )

