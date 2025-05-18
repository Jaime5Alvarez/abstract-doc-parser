from fastapi import HTTPException
from src.modules.docs_parser.domain.interfaces import IDocsParser
from src.modules.docs_parser.domain.value_objects import DocumentParserProvider
from src.modules.docs_parser.infraestructure.services.docling_service import DoclingService
from src.modules.docs_parser.infraestructure.services.markitdown_service import (
    MarkItDownDocumentParser,
)
from src.modules.docs_parser.infraestructure.services.unstructured_service import (
    UnstructuredService,
)
from src.modules.docs_parser.infraestructure.services.pymupdf_service import (
    DocumentParserPymupdfService,
)
from src.modules.docs_parser.infraestructure.services.llamaparse_service import (
    LlamaParseDocumentParser,
)
from src.modules.docs_parser.infraestructure.services.azure_document_intelligence import (
    AzureDocumentIntelligence,
)


class ParseDocumentByPathInteractor:
    def __init__(self, docs_parser: IDocsParser):
        self.docs_parser = docs_parser

    def execute(self, path: str) -> str:
        return self.docs_parser.parse_with_path(path)


class ParseDocumentByPathInteractorFactory:
    def __init__(self, provider: DocumentParserProvider):
        self.provider = provider

    def create(self) -> ParseDocumentByPathInteractor:
        if self.provider not in [
            DocumentParserProvider.Docling,
            DocumentParserProvider.MarkItDown,
            DocumentParserProvider.Unstructured,
            DocumentParserProvider.Pymupdf,
            DocumentParserProvider.LlmParse,
            DocumentParserProvider.AzureDocumentIntelligence,
        ]:
            raise HTTPException(
                status_code=400, detail=f"Provider {self.provider} not supported"
            )

        if self.provider == DocumentParserProvider.Docling:
            interactor = DoclingService()
        elif self.provider == DocumentParserProvider.MarkItDown:
            interactor = MarkItDownDocumentParser()
        elif self.provider == DocumentParserProvider.Unstructured:
            interactor = UnstructuredService()
        elif self.provider == DocumentParserProvider.Pymupdf:
            interactor = DocumentParserPymupdfService()
        elif self.provider == DocumentParserProvider.LlmParse:
            interactor = LlamaParseDocumentParser()
        elif self.provider == DocumentParserProvider.AzureDocumentIntelligence:
            interactor = AzureDocumentIntelligence()
        else:
            raise HTTPException(
                status_code=400, detail=f"Provider {self.provider} not supported"
            )

        return ParseDocumentByPathInteractor(interactor)
