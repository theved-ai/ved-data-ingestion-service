from typing import Type, Dict

from services.ingestion_service.enums.input_data_source import InputDataSource
from services.ingestion_service.service.storage_service_base import StorageServiceBase


class InputDataSourceToServiceRegistry:
    storage_registry: Dict[InputDataSource, StorageServiceBase] = {}

    @classmethod
    def register_service(cls, service_cls: Type["StorageServiceBase"]):
        instance = service_cls()
        for input_data_source in instance.supported_data_source():
            cls.storage_registry[input_data_source] = instance
        return service_cls


    def get_storage_service(self, input_data_source: InputDataSource) -> StorageServiceBase:
        storage_service = self.storage_registry.get(input_data_source)
        if not storage_service:
            raise ValueError(f"No storage service registered for source: {input_data_source}")
        return storage_service
