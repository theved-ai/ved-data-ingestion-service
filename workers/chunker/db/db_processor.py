from datetime import datetime

from workers.chunker.db.db_conn_pool import get_pg_pool
from workers.chunker.dto.chunk_data import ChunkData
from workers.chunker.dto.chunk_data_response import ChunkedDataResponse
from workers.chunker.dto.raw_data_response import RawDataResponse
from workers.chunker.enums.db_status import DbStatus


async def fetch_raw_data_by_id(raw_data_id: str) -> RawDataResponse:
    pool = get_pg_pool()
    async with pool.acquire() as conn:
        query = """
                select uuid, user_id, content, source, created_at, status from raw_data
                where uuid = $1
            """
        row = await conn.fetchrow(query, raw_data_id)
        return RawDataResponse(
            raw_data_id=row['uuid'],
            user_id=row['user_id'],
            content=row['content'],
            data_source=row['source'],
            created_at=row['created_at'],
            status=row['status']
        )


async def insert_chunk(chunk_data: ChunkData) -> ChunkedDataResponse:
    pool = get_pg_pool()
    async with pool.acquire() as conn:
        query = """
                Insert into chunked_data
                values($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                returning uuid, raw_data_id, chunk_content, status, chunk_index, created_at
            """
        row = await conn.fetchrow(
            query,
            chunk_data.uuid,
            chunk_data.raw_data_id,
            chunk_data.chunk_content,
            chunk_data.chunk_index,
            DbStatus.RAW_CHUNKS,
            None,
            None,
            0,
            datetime.now(),
            datetime.now()
        )

        return ChunkedDataResponse(
            chunk_id=row['uuid'],
            raw_data_id=row['raw_data_id'],
            chunk_content=row['chunk_content'],
            status=row['status'],
            chunk_index=row['chunk_index'],
            created_at=row['created_at']
        )
