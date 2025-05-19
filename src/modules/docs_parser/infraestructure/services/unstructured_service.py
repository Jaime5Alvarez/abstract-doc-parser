from src.modules.docs_parser.domain.interfaces import IDocsParser
from unstructured.partition.auto import partition
import tempfile
import os


class UnstructuredService(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            elements = partition(url=path)
            return "\n".join(str(element) for element in elements)
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")

    def parse_with_blob(self, blob: bytes) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(blob)
                temp_file_path = temp_file.name

            try:
                elements = partition(filename=temp_file_path)
                return "\n".join(str(element) for element in elements)
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
