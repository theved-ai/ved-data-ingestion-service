from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.service.input_data_source_to_service_registry import InputDataSourceToServiceRegistry
from services.ingestion_service.service.kafka_publisher_service import KafkaPublisherService
from services.ingestion_service.utils.mapper import enrich_ingestion_data, generate_kafka_publish_event


class IngestionFacadeService:
    def __init__(self):
        self.storage_registry_service = InputDataSourceToServiceRegistry()
        self.kafka_publisher_service = KafkaPublisherService()


    async def ingest_data(self, ingestion_req: IngestionRequest):
        storage_service = self.storage_registry_service.get_storage_service(ingestion_req.data_source)
        ingested_data_metadata = await storage_service.process(ingestion_req)
        enriched_ingestion_data = enrich_ingestion_data(ingested_data_metadata, ingestion_req)
        kafka_publish_event = generate_kafka_publish_event(enriched_ingestion_data)
        await self.kafka_publisher_service.publish_event(kafka_publish_event)