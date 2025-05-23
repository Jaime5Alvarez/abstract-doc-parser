from abc import ABC, abstractmethod
from typing import Any, Coroutine


class IDocsParser(ABC):
    @abstractmethod
    def parse_with_path(self, path: str) -> str | Coroutine[Any, Any, str]:
        pass

    @abstractmethod
    def parse_with_blob(self, blob: bytes) -> str | Coroutine[Any, Any, str]:
        pass
