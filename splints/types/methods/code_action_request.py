from typing import Literal

from pydantic import BaseModel

from splints.types.lsp.base import RequestBase, ResponseBase
from splints.types.lsp.shared import (
    Diagnostic,
    DocumentUri,
    Range,
    TextDocumentIdentifier,
)


class CodeActionContext(BaseModel):
    diagnostics: list[Diagnostic]


class CodeActionParams(BaseModel):
    textDocument: TextDocumentIdentifier
    range: Range
    context: CodeActionContext


class CodeActionRequest(RequestBase):
    method: Literal["textDocument/codeAction"]
    params: CodeActionParams


class TextEdit(BaseModel):
    range: Range
    newText: str


class WorkspaceEdit(BaseModel):
    changes: dict[DocumentUri, list[TextEdit]]


class CodeAction(BaseModel):
    title: str
    kind: Literal["quickfix"]
    diagnostics: list[Diagnostic]
    edit: WorkspaceEdit


class CodeActionResponse(ResponseBase):
    result: list[CodeAction]
