from src.modules.docs_parser.domain.interfaces import IDocsParser
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import os


class AzureDocumentIntelligence(IDocsParser):
    def parse_with_path(self, path: str) -> str:
        try:
            endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT") or ""
            key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY") or ""
            if not endpoint or not key:
                raise ValueError(
                    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or AZURE_DOCUMENT_INTELLIGENCE_KEY is not set"
                )

            document_intelligence_client = DocumentIntelligenceClient(
                endpoint=endpoint, credential=AzureKeyCredential(key)
            )

            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-read", AnalyzeDocumentRequest(url_source=path)
            )
            result = poller.result()

            return result.content.replace("\n", " ")
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")

    def parse_with_blob(self, blob: bytes) -> str:
        try:
            endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT") or ""
            key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY") or ""
            if not endpoint or not key:
                raise ValueError(
                    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or AZURE_DOCUMENT_INTELLIGENCE_KEY is not set"
                )

            document_intelligence_client = DocumentIntelligenceClient(
                endpoint=endpoint, credential=AzureKeyCredential(key)
            )

            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-read", AnalyzeDocumentRequest(bytes_source=blob)
            )
            result = poller.result()

            return result.content.replace("\n", " ")
        except Exception as e:
            raise ValueError(f"Error parsing document: {e}")
