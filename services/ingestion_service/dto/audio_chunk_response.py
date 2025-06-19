from pydantic import BaseModel

class AudioChunk(BaseModel):
    chunk_index: int
    transcript: str