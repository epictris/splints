from typing import Literal
from pydantic import BaseModel

from splints.types.base import NotificationBase
from splints.types.shared import TextDocumentItem


class DidOpenTextDocumentParams(BaseModel):
    textDocument: TextDocumentItem


class DidOpenTextDocumentNotification(NotificationBase):
    method: Literal["textDocument/didOpen"]
    params: DidOpenTextDocumentParams

