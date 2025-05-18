from enum import Enum


class DocumentParserProvider(str, Enum):
    Docling = "docling"
    MarkItDown = "markitdown"
    Unstructured = "unstructured"
    Pymupdf = "pymupdf"
    LlmParse = "llmparse"
    AzureDocumentIntelligence = "azure-document-intelligence"
