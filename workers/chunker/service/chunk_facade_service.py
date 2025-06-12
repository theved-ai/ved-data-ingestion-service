from workers.chunker.db.db_processor import fetch_raw_data_by_id, insert_chunk
from workers.chunker.dto.raw_data_consumed_event import RawDataKafkaEvent
from workers.chunker.service.chunking_service import ChunkingService
from workers.chunker.service.kafka_service import KafkaService
from workers.chunker.dto.embed_topic_event import from_chunk


class ChunkFacadeService:

    def __init__(self, kafka_service: KafkaService):
        self.kafka_service = kafka_service
        self.chunking_service = ChunkingService()

    async def chunk_data_and_publish_for_embedding(self, raw_data_kafka_event: RawDataKafkaEvent):
        raw_data_content = await fetch_raw_data_by_id(raw_data_kafka_event.raw_data_id)
        raw_data_chunks = self.chunking_service.chunk_text(raw_data_content)

        for raw_data_chunk in raw_data_chunks:
            chunk_response = await insert_chunk(raw_data_chunk)
            embed_topic_event = from_chunk(raw_data_chunk, chunk_response)
            await self.kafka_service.publish_event(embed_topic_event)

