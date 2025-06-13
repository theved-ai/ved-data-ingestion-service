from workers.embedding.db.db_conn_pool import get_pg_pool


async def update_chunk_status(chunk_id: str, status: str):
    pool = get_pg_pool()
    async with pool.acquire() as conn:
        query = """
            update chunked_data
            set status = $1
            where uuid = $2 
        """
        await conn.execute(query, status, chunk_id)
