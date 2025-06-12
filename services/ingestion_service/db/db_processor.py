import json
import logging
import uuid
from datetime import datetime

from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.db.db_conn_pool import get_pg_pool
from services.ingestion_service.dto.storage_service_response import StorageServiceResponse
from services.ingestion_service.enums.db_status import DbStatus
from services.ingestion_service.enums.input_data_source import InputDataSource

logger = logging.getLogger(__name__)

async def insert_raw_data(ingestion_data: IngestionRequest) -> StorageServiceResponse:
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            query = """
                INSERT INTO raw_data (
                    uuid, user_id, content, source, status, metadata, retries, is_archived, created_at, updated_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
                ) RETURNING uuid, user_id, source, status, created_at;
            """
            now = datetime.utcnow()
            doc_id = str(uuid.uuid4())
            row = await conn.fetchrow(
                query,
                doc_id,
                ingestion_data.user_id,
                ingestion_data.content,
                ingestion_data.data_source.value,
                DbStatus.RAW_DATA,
                json.dumps(dict(ingestion_data.metadata or {})),
                0,
                False,
                now,
                now
            )
            return StorageServiceResponse(
                user_id=str(row["user_id"]),
                raw_data_id=str(row['uuid']),
                data_input_source=InputDataSource(row["source"]),
                status=str(row["status"]),
                ingestion_timestamp=row["created_at"]
            )
    except Exception as e:
        logger.exception("Exception in db level processing: ", e)
