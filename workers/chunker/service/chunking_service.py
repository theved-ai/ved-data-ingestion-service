import uuid

from transformers import AutoTokenizer
from workers.chunker.dto.chunk_data import ChunkData
from workers.chunker.dto.raw_data_response import RawDataResponse
from workers.chunker.utils.application_constants import EMBEDDING_MODEL_NAME, CHUNK_TOKEN_LIMIT, CHUNK_TOKEN_OVERLAP


class ChunkingService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)

    def chunk_text(self, raw_content_data: RawDataResponse) -> list[ChunkData]:
        # Tokenize full text with no truncation
        tokens = self.tokenizer.encode(
            raw_content_data.content,
            add_special_tokens=False
        )

        chunks = []
        i = 0
        chunk_counter = 1
        while i < len(tokens):
            chunk_tokens = tokens[i:i + CHUNK_TOKEN_LIMIT]
            chunk_str = self.tokenizer.decode(chunk_tokens)

            if chunk_str.strip():
                chunks.append(ChunkData(
                    raw_data_id=str(raw_content_data.raw_data_id),
                    data_input_source=raw_content_data.data_source,
                    chunk_content=chunk_str,
                    chunk_index=chunk_counter,
                    status=raw_content_data.status,
                    user_id=str(raw_content_data.user_id),
                    uuid=str(uuid.uuid4()),
                    metadata=str(raw_content_data.metadata)
                ))

            i += CHUNK_TOKEN_LIMIT - CHUNK_TOKEN_OVERLAP
            chunk_counter+=1
        return chunks