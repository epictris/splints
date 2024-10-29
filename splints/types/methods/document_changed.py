
from typing import Literal
from pydantic import BaseModel

from splints.types.lsp.base import NotificationBase
from splints.types.lsp.shared import Range, VersionedTextDocumentIdentifier


class TextDocumentContentChangeEvent(BaseModel):
    range: Range | None = None
    text: str

class DidChangeTextDocumentParams(BaseModel):
    textDocument: VersionedTextDocumentIdentifier
    contentChanges: list[TextDocumentContentChangeEvent]


class DidChangeTextDocumentNotification(NotificationBase):
    method: Literal["textDocument/didChange"]
    params: DidChangeTextDocumentParams
