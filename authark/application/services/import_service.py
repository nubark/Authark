import json
from typing import Dict
from abc import ABC, abstractmethod
from ..models import User


class ImportService(ABC):
    @abstractmethod
    def import_users(self, filepath: str, source: str) -> []:
        "Generate method to be implemented."


class MemoryImportService(ImportService):
    def import_users(self, filepath: str, source: str) -> []:
        return []
