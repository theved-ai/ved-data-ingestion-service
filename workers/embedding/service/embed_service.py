from sentence_transformers import SentenceTransformer

from workers.embedding.utils.application_constants import EMBEDDING_MODEL_NAME


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def generate_vector(self, content: str) -> list[float]:
        nd_vector_array = self.model.encode(
            content,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return [float(x) for x in nd_vector_array.flatten()]
