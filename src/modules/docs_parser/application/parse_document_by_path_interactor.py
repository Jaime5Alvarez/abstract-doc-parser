from src.modules.docs_parser.domain.interfaces import IDocsParser


class ParseDocumentByPathInteractor:
    def __init__(self, docs_parser: IDocsParser):
        self.docs_parser = docs_parser

    def execute(self, path: str) -> str:
        return self.docs_parser.parse_with_path(path)


class ParseDocumentByPathInteractorFactory:
    def __init__(self, docs_parser: IDocsParser):
        self.docs_parser = docs_parser

    def create(self) -> ParseDocumentByPathInteractor:
        return ParseDocumentByPathInteractor(self.docs_parser)
