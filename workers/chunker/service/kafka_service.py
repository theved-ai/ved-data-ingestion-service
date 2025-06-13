import json
import os
from typing import AsyncIterator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, ConsumerRecord
from workers.chunker.config.logging_config import logger
from workers.chunker.dto.embed_topic_event import EmbedTopicEvent
from workers.chunker.utils.application_constants import CHUNKED_DATA_TOPIC, RAW_DATA_TOPIC, RAW_DATA_CONSUMER_GROUP, KAFKA_BOOTSTRAP_SERVER


class KafkaService:
    def __init__(self):
        self.kafka_producer = None
        self.kafka_consumer = None

    async def __get_kafka_consumer(self):
        if self.kafka_consumer is None:
            self.kafka_consumer = AIOKafkaConsumer(
                RAW_DATA_TOPIC,
                bootstrap_servers=os.getenv(KAFKA_BOOTSTRAP_SERVER),
                group_id=RAW_DATA_CONSUMER_GROUP,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                key_deserializer=lambda v: v.decode("utf-8")
            )
            await self.kafka_consumer.start()
        return self.kafka_consumer

    async def __get_kafka_producer(self):
        if self.kafka_producer is None:
            self.kafka_producer = AIOKafkaProducer(
                bootstrap_servers=os.getenv(KAFKA_BOOTSTRAP_SERVER),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda v: str(v).encode("utf-8")
            )
            await self.kafka_producer.start()
        return self.kafka_producer


    async def consumer_event(self) -> AsyncIterator[ConsumerRecord]:
        try:
            consumer = await self.__get_kafka_consumer()
            async for msg in consumer:
                yield msg
        except Exception:
            logger.exception(f"Exception while consuming event from kafka")
        finally:
            await self.kafka_consumer.stop()


    async def publish_event(self, event: EmbedTopicEvent):
        try:
            producer = await self.__get_kafka_producer()
            await producer.send_and_wait(
                topic=CHUNKED_DATA_TOPIC,
                key=event.raw_data_id,
                value=event.model_dump_json()
            )
        except Exception:
            logger.exception(f"Exception while publishing event to kafka")