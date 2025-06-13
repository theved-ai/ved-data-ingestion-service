import asyncio
import json
import os

from workers.embedding.config.logging_config import logger
from workers.embedding.db.db_conn_pool import init_pg_pool, close_pg_pool
from workers.embedding.dto.chuked_data_consumed_event import ChunkedDataConsumedEvent
from workers.embedding.service.embed_facade_service import EmbedFacadeService
from workers.embedding.service.kafka_service import KafkaService


async def main():
    try:
        db_url = os.getenv("DB_URL")
        await init_pg_pool(db_url)

        # Start Kafka consumer loop
        kafka_service = KafkaService()
        embedding_facade_service = EmbedFacadeService(kafka_service)
        async for raw_data_event in kafka_service.consumer_event():
            event_data = ChunkedDataConsumedEvent.model_validate(json.loads(raw_data_event.value))
            await embedding_facade_service.process_raw_chunk_event(event_data)

    except Exception:
        logger.exception("Unhandled exception in main loop")

    finally:
        await close_pg_pool()
        logger.info("Database pool closed. Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
