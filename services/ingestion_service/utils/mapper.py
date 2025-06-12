from datetime import datetime

import pytz

from services.ingestion_service.dto.enriched_ingestion_data import EnrichedIngestionData
from services.ingestion_service.dto.ingestion_kafka_event import IngestionKafkaEvent
from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse


def generate_kafka_publish_event(data: EnrichedIngestionData):
    return IngestionKafkaEvent(
        user_id=data.user_id,
        raw_data_id=data.raw_data_id,
        data_input_source=data.data_input_source,
        status=data.status,
        event_published_at=data.event_published_at_timestamp,
        ingestion_timestamp=data.ingestion_timestamp,
        content_timestamp= data.content_timestamp
    )

def enrich_ingestion_data(data: StorageServiceResponse, req_data: IngestionRequest):
    return EnrichedIngestionData(
        user_id=data.user_id,
        raw_data_id=data.raw_data_id,
        data_input_source=data.data_input_source,
        status=data.status,
        event_published_at_timestamp=datetime.now(tz=pytz.timezone('Asia/Kolkata')),
        ingestion_timestamp=data.ingestion_timestamp,
        content_timestamp= req_data.metadata['content_timestamp'] if req_data.metadata and req_data.metadata.get('content_timestamp') else data.ingestion_timestamp
    )