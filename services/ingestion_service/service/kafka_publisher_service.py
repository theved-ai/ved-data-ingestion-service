import json
from aiokafka import AIOKafkaProducer

from services.ingestion_service.dto.ingestion_kafka_event import IngestionKafkaEvent
from services.ingestion_service.utils.application_constants import RAW_DATA_INGEST_TOPIC


class KafkaPublisherService:
    def __init__(self):
        self.kafka_producer = None

    def __get_kafka_producer(self):
        if self.kafka_producer is None:
            self.kafka_producer = AIOKafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda v: str(v).encode("utf-8")
            )
        return self.kafka_producer


    async def publish_event(self, event: IngestionKafkaEvent):
        producer = self.__get_kafka_producer()
        await producer.send_and_wait(
            topic=RAW_DATA_INGEST_TOPIC,
            key=event.raw_data_id.encode(),
            value=event.model_dump_json().encode()
        )