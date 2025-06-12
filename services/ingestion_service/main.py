import logging.config
from config.logging_config import LOGGING_CONFIG
import os
from contextlib import asynccontextmanager

from services.ingestion_service.api.ingestion_controller import IngestionController
from services.ingestion_service.db.db_conn_pool import init_pg_pool, close_pg_pool
from services.ingestion_service.service.ingestion_facade_service import IngestionFacadeService
from services.ingestion_service.utils.application_constants import SERVICE_PACKAGE
from services.ingestion_service.utils.import_util import load_package
from fastapi import FastAPI

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

facade_instance = IngestionFacadeService()
ingestion_controller = IngestionController(facade_instance)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App is starting up...")
    load_package(SERVICE_PACKAGE)
    await init_pg_pool(os.getenv("DB_URL"))
    yield
    await close_pg_pool()
    logger.info("App is shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(ingestion_controller.router)