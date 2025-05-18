from src.modules.docs_parser.domain.interfaces import IDocsParser
from llama_cloud_services import LlamaParse
import os


class LlamaParseDocumentParser(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            if not os.getenv("LLAMA_CLOUD_API_KEY"):
                raise ValueError("LLAMA_CLOUD_API_KEY is not set")

            llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY") or ""

            parser = LlamaParse(
                api_key=llama_cloud_api_key,  # can also be set in your env as LLAMA_CLOUD_API_KEY
                num_workers=4,  # if multiple files passed, split in `num_workers` API calls
                verbose=True,
                language="en",  # optionally define a language, default=en
            )
            result = parser.parse(path)
            markdown_documents = result.get_markdown_documents(split_by_page=True)  # type: ignore

            return markdown_documents[0].text  # type: ignore
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
