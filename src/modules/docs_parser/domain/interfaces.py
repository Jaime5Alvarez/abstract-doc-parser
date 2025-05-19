from abc import ABC, abstractmethod


class IDocsParser(ABC):
    @abstractmethod
    def parse_with_path(self, path: str) -> str:
        pass

    @abstractmethod
    def parse_with_blob(self, blob: bytes) -> str:
        pass
