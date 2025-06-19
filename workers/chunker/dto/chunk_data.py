from dataclasses import dataclass
from typing import Any


@dataclass
class ChunkData:
    uuid: str
    raw_data_id: str
    chunk_content: str
    status: str
    chunk_index: int
    data_input_source: str
    user_id: str
    metadata: str
