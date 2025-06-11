from fastapi import HTTPException
from fastapi.responses import JSONResponse

from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.main import app
from services.ingestion_service.service.ingestion_facade_service import IngestionFacadeService

ingestion_facade_service = IngestionFacadeService()


@app.post("/v1/ingest")
async def ingest_data(req: IngestionRequest):
    try:
        result = await ingestion_facade_service.ingest_data(req)
        return JSONResponse(content=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
