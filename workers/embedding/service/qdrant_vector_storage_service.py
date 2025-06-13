from qdrant_client.async_qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.models import Distance, VectorParams

from workers.embedding.dto.vector_request import VectorRequest
from workers.embedding.service.vector_storage_base import VectorStorageBase
from workers.embedding.utils.application_constants import QDRANT_HOST_ENV, QDRANT_HOST_PORT_ENV


class QdrantVectorStorageService(VectorStorageBase):
    def __init__(self):
        self.client = AsyncQdrantClient(host=QDRANT_HOST_ENV, port=QDRANT_HOST_PORT_ENV)

    async def insert_vector(self, vector_chunk: VectorRequest):
        collection_name = f"{vector_chunk.user_id}__{vector_chunk.embedding_model.replace('/', '_')}"
        await self.ensure_collection_exists(collection_name, vector_chunk)

        qdrant_id = vector_chunk.chunk_id
        qdrant_point = qmodels.PointStruct(
            id=qdrant_id,
            vector=vector_chunk.vector,
            payload=vector_chunk.model_dump(exclude={'vector'})
        )
        await self.client.upsert(
            collection_name=collection_name,
            points=[qdrant_point]
        )

    async def ensure_collection_exists(self, collection_name, vector_chunk):
        collections = await self.client.get_collections()
        if collection_name not in [c.name for c in collections.collections]:
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=len(vector_chunk.vector),
                    distance=Distance.COSINE
                )
            )



