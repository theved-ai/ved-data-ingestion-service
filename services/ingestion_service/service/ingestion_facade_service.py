import asyncio

from services.ingestion_service.dto.audio_ingestion_req import AudioIngestionRequest
from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.enums.stream_event_type import StreamEventType
from services.ingestion_service.registry.event_type_to_handler_registry import EventTypeHandlerRegistry
from services.ingestion_service.registry.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.kafka_publisher_service import KafkaPublisherService
from services.ingestion_service.utils.mapper import enrich_ingestion_data, generate_kafka_publish_event


class IngestionFacadeService:
    def __init__(self):
        self.storage_registry_service = InputDataSourceToServiceRegistry()
        self.kafka_publisher_service = KafkaPublisherService()
        self.event_type_handler_registry = EventTypeHandlerRegistry()


    async def ingest_data(self, ingestion_req: IngestionRequest):
        storage_service = self.storage_registry_service.get_storage_service(ingestion_req.data_source)
        ingested_data_metadata = await storage_service.process(ingestion_req)
        await self.enrich_and_publish_to_kafka(ingested_data_metadata, ingestion_req)

    async def enrich_and_publish_to_kafka(self, ingested_data_metadata, ingestion_req):
        enriched_ingestion_data = enrich_ingestion_data(ingested_data_metadata, ingestion_req)
        kafka_publish_event = generate_kafka_publish_event(enriched_ingestion_data)
        await self.kafka_publisher_service.publish_event(kafka_publish_event)


    async def ingest_audio_chunks(self, audio_chunk_req: AudioIngestionRequest):
        handler_service = self.event_type_handler_registry.get_handler(audio_chunk_req.event_type)
        response = await handler_service.handle(audio_chunk_req.payload)

        if audio_chunk_req.event_type == StreamEventType.close_connection:
            ingestion_req = response.to_ingestion_request(audio_chunk_req.payload)
            ingestion_metadata = response.to_storage_service_response(audio_chunk_req.payload)
            asyncio.create_task(self.enrich_and_publish_to_kafka(ingestion_metadata, ingestion_req))

        return response
