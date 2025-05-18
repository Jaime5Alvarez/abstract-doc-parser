from src.modules.docs_parser.domain.interfaces import IDocsParser
from unstructured.partition.auto import partition


class UnstructuredService(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            elements = partition(url=path)
            return "\n".join(str(element) for element in elements)
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
