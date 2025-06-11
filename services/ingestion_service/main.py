import os
from contextlib import asynccontextmanager

from services.ingestion_service.db.db_conn_pool import init_pg_pool, close_pg_pool
from services.ingestion_service.utils.application_constants import SERVICE_PACKAGE
from services.ingestion_service.utils.import_util import load_package
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pg_pool(os.getenv("DB_URL"))
    yield
    await close_pg_pool()

app = FastAPI(lifespan=lifespan)

def main():
    load_package(SERVICE_PACKAGE)


if __name__ == '__main__':
    main()