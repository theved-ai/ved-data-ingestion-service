import json
import logging
import uuid
from datetime import datetime
from typing import Optional, List

from services.ingestion_service.dto.audio_chunk_response import AudioChunk
from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.dto.meet_payload import MeetPayload
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
                    id, user_id, content, source, status, metadata, retries, is_archived, created_at, updated_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
                ) RETURNING id, user_id, source, status, created_at;
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
                raw_data_id=str(row['id']),
                data_input_source=InputDataSource(row["source"]),
                status=str(row["status"]),
                ingestion_timestamp=row["created_at"]
            )
    except Exception as e:
        logger.exception("Exception in db level processing: ", e)

async def update_raw_data_status(raw_data_id, status):
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            query="""
                update raw_data
                set status = $1
                where id = $2
            """
            await conn.execute(query, status, raw_data_id)

    except Exception:
        logger.exception("Exception occurred while updating audio chunk status into DB.")


async def insert_audio_chunks(req: MeetPayload) -> Optional[str]:
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            query = """
                INSERT INTO meet_transcript_audio_chunks 
                (raw_data_id, chunk_index, audio_format, audio_blob, transcript)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
            """
            row = await conn.fetchrow(query, req.raw_data_id, req.audio_chunk_index, req.audio_format, req.audio_blob, '')
            return str(row['id']) if row else None

    except Exception:
        logger.exception("Exception occurred while inserting audio chunk into DB.")


async def update_audio_chunk_transcript(transcript:str, chunk_id:str):
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            query = """
                update meet_transcript_audio_chunks
                set transcript = $1
                where id = $2 
            """
            await conn.execute(query, transcript, chunk_id)
    except Exception:
        logger.exception("Exception occurred while inserting audio chunk into DB.")


async def fetch_audio_chunks(raw_data_id) -> List[AudioChunk]:
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            query = """
                select chunk_index, transcript from meet_transcript_audio_chunks
                where raw_data_id = $1
            """
            rows = await conn.fetch(query, raw_data_id)
            return [AudioChunk(
                chunk_index=row['chunk_index'],
                transcript=row['transcript']
            ) for row in rows]

    except Exception as e:
        logger.exception(f"Exception occurred while fetching audio chunks for raw_data_id={raw_data_id}: {e}")
        return []


async def save_raw_data_transcript(final_transcript: str, raw_data_id: str):
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            query = """
                UPDATE raw_data
                SET content = $1, status = $2
                WHERE id = $3
                RETURNING id, user_id, source, status, created_at;
            """
            row = await conn.fetchrow(query, final_transcript, DbStatus.TRANSCRIPTION_COMPLETE, raw_data_id)
            if row == "UPDATE 0":
                logger.warning(f"No raw_data record found for uuid={raw_data_id}")

            return StorageServiceResponse(
                user_id=str(row["user_id"]),
                raw_data_id=str(row['id']),
                data_input_source=InputDataSource(row["source"]),
                status=str(row["status"]),
                ingestion_timestamp=row["created_at"]
            )

    except Exception as e:
        logger.exception(f"Exception occurred while saving the final transcript for uuid={raw_data_id}: {e}")
