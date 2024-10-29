from typing import Literal
from pydantic import BaseModel

from splints.types.lsp.base import NotificationBase
from splints.types.lsp.shared import Diagnostic, DocumentUri


class PublishDiagnosticsParams(BaseModel):
    uri: DocumentUri
    version: int | None = None
    diagnostics: list[Diagnostic]


class PublishDiagnosticsNotification(NotificationBase):
    method: Literal["textDocument/publishDiagnostics"]
    params: PublishDiagnosticsParams
