import asyncio
import json
import logging
import os

from workers.chunker.db.db_conn_pool import init_pg_pool, close_pg_pool
from workers.chunker.dto.raw_data_consumed_event import RawDataKafkaEvent
from workers.chunker.service.chunk_facade_service import ChunkFacadeService
from workers.chunker.service.kafka_service import KafkaService

logger = logging.getLogger(__name__)


async def main():
    try:
        db_url = os.getenv("DB_URL")
        await init_pg_pool(db_url)

        # Start Kafka consumer loop
        kafka_service = KafkaService()
        chunking_facade_service = ChunkFacadeService(kafka_service)
        async for raw_data_event in kafka_service.consumer_event():
            event_data = RawDataKafkaEvent.model_validate(json.loads(raw_data_event.value))
            await chunking_facade_service.chunk_data_and_publish_for_embedding(event_data)

    except Exception:
        logger.exception("Unhandled exception in main loop")

    finally:
        await close_pg_pool()
        logger.info("Database pool closed. Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
