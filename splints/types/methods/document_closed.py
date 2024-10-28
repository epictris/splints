from typing import Literal
from pydantic import BaseModel

from splints.types.base import NotificationBase
from splints.types.shared import TextDocumentIdentifier


class DidCloseTextDocumentParams(BaseModel):
    textDocument: TextDocumentIdentifier


class DidCloseTextDocumentNotification(NotificationBase):
    method: Literal["textDocument/didClose"]
    params: DidCloseTextDocumentParams