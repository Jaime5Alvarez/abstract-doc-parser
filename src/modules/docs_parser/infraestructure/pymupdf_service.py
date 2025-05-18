from src.modules.docs_parser.domain.interfaces import IDocsParser
import pymupdf4llm
import requests
import tempfile
import os


class DocumentParserPymupdfService(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                response = requests.get(path)
                response.raise_for_status()
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            try:
                md_text = pymupdf4llm.to_markdown(temp_file_path)
                return md_text
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
