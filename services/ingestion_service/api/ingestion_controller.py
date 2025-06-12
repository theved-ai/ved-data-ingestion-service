from services.ingestion_service.service.ingestion_facade_service import IngestionFacadeService

ingestion_facade_service = IngestionFacadeService()


from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.ingestion_service.dto.ingestion_request import IngestionRequest

class IngestionController:
    def __init__(self, facade_service):
        self.router = APIRouter()
        self.facade_service = facade_service
        self._add_routes()

    def _add_routes(self):
        @self.router.post("/v1/ingest")
        async def ingest_data(req: IngestionRequest):
            try:
                await self.facade_service.ingest_data(req)
            except ValueError as ve:
                raise HTTPException(status_code=400, detail=str(ve))
            except Exception:
                raise HTTPException(status_code=500, detail="Internal server error")

