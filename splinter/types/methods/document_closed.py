from typing import Literal
from pydantic import BaseModel

from splinter.types.base import NotificationBase
from splinter.types.shared import TextDocumentIdentifier


class DidCloseTextDocumentParams(BaseModel):
    textDocument: TextDocumentIdentifier


class DidCloseTextDocumentNotification(NotificationBase):
    method: Literal["textDocument/didClose"]
    params: DidCloseTextDocumentParams
