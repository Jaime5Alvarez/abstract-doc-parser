from fastapi import FastAPI, HTTPException
from src.modules.docs_parser.application.parse_document_by_path_interactor import (
    ParseDocumentByPathInteractorFactory,
)
from fastapi.responses import JSONResponse
import uvicorn
from src.modules.docs_parser.domain.value_objects import DocumentParserProvider
from src.modules.docs_parser.infraestructure.azure_document_intelligence import (
    AzureDocumentIntelligence,
)
from src.modules.docs_parser.infraestructure.docling_service import DoclingService
from src.modules.docs_parser.infraestructure.llamaparse_service import (
    LlamaParseDocumentParser,
)
from src.modules.docs_parser.infraestructure.markitdown_service import (
    MarkItDownDocumentParser,
)
import time

from src.modules.docs_parser.infraestructure.pymupdf_service import (
    DocumentParserPymupdfService,
)
from src.modules.docs_parser.infraestructure.unstructured_service import (
    UnstructuredService,
)

app: FastAPI = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/doc-parser-by-path")
def doc_parser_by_path(path: str, provider: DocumentParserProvider):
    try:
        start_time = time.time()

        interactor = ParseDocumentByPathInteractorFactory(provider).create()

        result = interactor.execute(path=path)
        end_time = time.time()
        return {
            "data": {
                "time": end_time - start_time,
                "path": path,
                "provider": provider,
                "result": result,
            }
        }
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={"data": {"error": e.detail}}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": {
                    "time": 0,
                    "path": path,
                    "provider": provider,
                    "error": str(e),
                    "result": "Error parsing document",
                }
            },
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
