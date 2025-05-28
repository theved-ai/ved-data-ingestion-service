from common.enum.request_type import RequestType
from llm_core.llm_clients.base import ILlmClient


class LlmRegistry:

    _registry = {}

    @classmethod
    def register(cls, request_type: RequestType, llm_client: ILlmClient):
        cls._registry[request_type] = llm_client