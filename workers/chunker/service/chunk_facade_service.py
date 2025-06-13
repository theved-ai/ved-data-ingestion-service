from workers.chunker.config.logging_config import logger
from workers.chunker.db.db_processor import fetch_raw_data_by_id, insert_chunk
from workers.chunker.dto.embed_topic_event import from_chunk
from workers.chunker.dto.raw_data_consumed_event import RawDataKafkaEvent
from workers.chunker.service.chunking_service import ChunkingService
from workers.chunker.service.kafka_service import KafkaService


class ChunkFacadeService:

    def __init__(self, kafka_service: KafkaService):
        self.kafka_service = kafka_service
        self.chunking_service = ChunkingService()

    async def chunk_data_and_publish_for_embedding(self, raw_data_kafka_event: RawDataKafkaEvent):
        logger.info(f"Received raw data event:\n {raw_data_kafka_event}\n\n")
        raw_data_content = await fetch_raw_data_by_id(raw_data_kafka_event.raw_data_id)

        logger.info(f"Raw data id {raw_data_kafka_event.raw_data_id} metadata:\n {raw_data_content}\n\n")
        raw_data_chunks = self.chunking_service.chunk_text(raw_data_content)

        logger.info(f"Raw data chunks: {raw_data_chunks.__sizeof__()} \n\n")
        for raw_data_chunk in raw_data_chunks:
            chunk_response = await insert_chunk(raw_data_chunk)
            logger.info(f"Inserted chunk: {chunk_response} \n\n")

            embed_topic_event = from_chunk(raw_data_chunk, chunk_response)
            logger.info(f"chunked data event: {embed_topic_event} \n\n")
            await self.kafka_service.publish_event(embed_topic_event)

            logger.info(f"Event published!!\n\n")

