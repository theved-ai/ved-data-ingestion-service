from workers.embedding.dto.chuked_data_consumed_event import ChunkedDataConsumedEvent
from workers.embedding.dto.vector_request import build_vector_request
from workers.embedding.service.embed_service import EmbeddingService
from workers.embedding.service.kafka_service import KafkaService
from workers.embedding.config.logging_config import logger
from workers.embedding.db.db_processor import update_chunk_status
from workers.embedding.enums.db_status import DbStatus
from workers.embedding.service.qdrant_vector_storage_service import QdrantVectorStorageService


class EmbedFacadeService:
    def __init__(self, kafka_service: KafkaService):
        self.kafka_service = kafka_service
        self.embedding_service = EmbeddingService()
        self.vector_service = QdrantVectorStorageService()

    async def process_raw_chunk_event(self, consumed_event: ChunkedDataConsumedEvent):
        try:
            await update_chunk_status(consumed_event.chunk_id, DbStatus.EMBEDDING_IN_PROGRESS)
            chunk_vector = self.embedding_service.generate_vector(consumed_event.chunk_content)
            vector_request = build_vector_request(consumed_event, chunk_vector)
            await update_chunk_status(consumed_event.chunk_id, DbStatus.VECTOR_INGESTION_IN_PROGRESS)
            await self.vector_service.insert_vector(vector_request)
            await update_chunk_status(consumed_event.chunk_id, DbStatus.VECTOR_INGESTION_COMPLETE)
        except Exception:
                logger.exception("Unhandled exception in facade service")