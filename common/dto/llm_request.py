from dataclasses import dataclass

from enum.request_type import RequestType


@dataclass
class LlmRequest:
    request_type: RequestType
    user_prompt: str