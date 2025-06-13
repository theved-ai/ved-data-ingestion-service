from abc import ABC, abstractmethod

from workers.embedding.dto.vector_request import VectorRequest


class VectorStorageBase(ABC):

    @abstractmethod
    async def insert_vector(self, req: VectorRequest):
        pass