from dataclasses import dataclass
from typing import List
from dto.data_source_response import DataSourceResponse
from enum.llm_client import LlmClient


@dataclass
class LlmResponse:
    llm_client: LlmClient
    response: List[DataSourceResponse]