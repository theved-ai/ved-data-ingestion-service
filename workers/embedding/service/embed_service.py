from typing import List

from workers.embedding.utils.application_constants import EMBEDDING_MODEL_NAME
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def generate_vector(self, content: str) -> List[float]:
        return self.model.encode(
            content,
            show_progress_bar=True,
            convert_to_numpy=True
        )