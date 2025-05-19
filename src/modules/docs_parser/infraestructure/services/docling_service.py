from src.modules.docs_parser.domain.interfaces import IDocsParser
from docling.document_converter import DocumentConverter
import tempfile
import os


class DoclingService(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            converter = DocumentConverter()
            document = converter.convert(path)
            return document.document.export_to_markdown()
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")

    def parse_with_blob(self, blob: bytes) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(blob)
                temp_file_path = temp_file.name

            try:
                converter = DocumentConverter()
                document = converter.convert(temp_file_path)
                return document.document.export_to_markdown()
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
