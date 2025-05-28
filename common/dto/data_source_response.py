from dataclasses import dataclass


@dataclass
class DataSourceResponse:
    data_source: str
    data_source_response: str