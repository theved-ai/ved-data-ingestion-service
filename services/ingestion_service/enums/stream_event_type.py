from enum import Enum


class StreamEventType(Enum):
    init = "init"
    audio_chunk = "audio_chunk"
    close_connection = "close_connection"