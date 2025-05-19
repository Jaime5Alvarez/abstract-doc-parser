from src.modules.docs_parser.domain.interfaces import IDocsParser
from markitdown import MarkItDown
import tempfile
import os

# from openai import OpenAI


class MarkItDownDocumentParser(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            md = MarkItDown(enable_plugins=True)  # Set to True to enable plugins
            result = md.convert(path)
            text = result.text_content
            return text.replace("\n", "")
            # return text
            # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            # md = MarkItDown(llm_client=client, llm_model="gpt-4o-mini")
            # result = md.convert(path)
            # return result.text_content

            if not os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"):
                raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is not set")

            md = MarkItDown(
                docintel_endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
            )
            result = md.convert(path)
            return result.text_content
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")

    def parse_with_blob(self, blob: bytes) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(blob)
                temp_file_path = temp_file.name

            try:
                md = MarkItDown(enable_plugins=True)
                result = md.convert(temp_file_path)
                text = result.text_content
                return text.replace("\n", "")
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
