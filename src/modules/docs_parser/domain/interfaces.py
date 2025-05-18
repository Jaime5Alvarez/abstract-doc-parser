from abc import ABC, abstractmethod


class IDocsParser(ABC):
    @abstractmethod
    def parse_with_path(self, path: str) -> str:
        pass
