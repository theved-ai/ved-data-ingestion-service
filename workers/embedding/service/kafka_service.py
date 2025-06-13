import json
import os
from typing import AsyncIterator
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from workers.embedding.config.logging_config import logger
from workers.embedding.utils.application_constants import CHUNKED_DATA_TOPIC, KAFKA_BOOTSTRAP_SERVER, CHUNK_DATA_CONSUMER_GROUP


class KafkaService:
    def __init__(self):
        self.kafka_consumer = None

    async def __get_kafka_consumer(self):
        if self.kafka_consumer is None:
            self.kafka_consumer = AIOKafkaConsumer(
                CHUNKED_DATA_TOPIC,
                bootstrap_servers=os.getenv(KAFKA_BOOTSTRAP_SERVER),
                group_id=CHUNK_DATA_CONSUMER_GROUP,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                key_deserializer=lambda v: v.decode("utf-8")
            )
            await self.kafka_consumer.start()
        return self.kafka_consumer


    async def consumer_event(self) -> AsyncIterator[ConsumerRecord]:
        try:
            consumer = await self.__get_kafka_consumer()
            async for msg in consumer:
                yield msg
        except Exception:
            logger.exception(f"Exception while consuming event from kafka")
        finally:
            await self.kafka_consumer.stop()