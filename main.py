from fastapi import FastAPI, HTTPException, File, UploadFile
from src.modules.docs_parser.application.parse_document_by_path_interactor import (
    ParseDocumentByPathInteractorFactory,
)
from src.modules.docs_parser.application.parse_document_by_blob_interactor import (
    ParseDocumentByBlobInteractorFactory,
)
from fastapi.responses import JSONResponse
import uvicorn
from src.modules.docs_parser.domain.value_objects import DocumentParserProvider
import time

app: FastAPI = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/doc-parser-by-path")
async def doc_parser_by_path(path: str, provider: DocumentParserProvider):
    
    try:
        start_time = time.time()

        interactor = ParseDocumentByPathInteractorFactory(provider).create()

        result = await interactor.execute(path=path)
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


@app.post("/doc-parser-by-blob")
async def doc_parser_by_blob(
    provider: DocumentParserProvider, file: UploadFile = File(...)
):
    try:
        start_time = time.time()
        
        contents = await file.read()
        interactor = ParseDocumentByBlobInteractorFactory(provider).create()
        
        result = await interactor.execute(blob=contents)
        end_time = time.time()
        
        return {
            "data": {
                "time": end_time - start_time,
                "filename": file.filename,
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
                    "filename": file.filename if file else "unknown",
                    "provider": provider,
                    "error": str(e),
                    "result": "Error parsing document",
                }
            },
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
