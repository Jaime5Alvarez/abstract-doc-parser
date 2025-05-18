from src.modules.docs_parser.domain.interfaces import IDocsParser
from docling.document_converter import DocumentConverter


class DoclingService(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            converter = DocumentConverter()
            document = converter.convert(path)
            return document.document.export_to_markdown()
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
