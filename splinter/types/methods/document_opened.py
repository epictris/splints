from typing import Literal
from pydantic import BaseModel

from splinter.types.base import NotificationBase
from splinter.types.shared import TextDocumentItem


class DidOpenTextDocumentParams(BaseModel):
    textDocument: TextDocumentItem


class DidOpenTextDocumentNotification(NotificationBase):
    method: Literal["textDocument/didOpen"]
    params: DidOpenTextDocumentParams

