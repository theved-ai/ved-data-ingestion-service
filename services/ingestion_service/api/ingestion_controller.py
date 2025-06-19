import json

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from services.ingestion_service.dto.audio_ingestion_req import AudioIngestionRequest
from services.ingestion_service.dto.ingestion_request import IngestionRequest
from services.ingestion_service.config.logging_config import logger
from services.ingestion_service.enums.stream_event_type import StreamEventType


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


        @self.router.websocket("/v1/ingest/audio")
        async def websocket_ingest(websocket: WebSocket):
            await websocket.accept()

            try:
                while True:
                    data = await websocket.receive_text()
                    payload_dict = json.loads(data)
                    audio_chunk_req = AudioIngestionRequest(**payload_dict)
                    response = await self.facade_service.ingest_audio_chunks(audio_chunk_req)
                    await websocket.send_text(response.json())
                    if audio_chunk_req.event_type == StreamEventType.close_connection:
                        await websocket.close()
                        break

            except WebSocketDisconnect:
                print("Client disconnected")
            except Exception as e:
                logger.exception("WebSocket ingestion error")
                await websocket.send_text(json.dumps({
                    "event_type": "error",
                    "status": "failure",
                    "message": str(e)
                }))