from enum import IntEnum, StrEnum
from typing import Any, Literal
from pydantic import BaseModel


class DiagnosticOptions(BaseModel):
    identifier: str | None = None
    interFileDependencies: bool
    workspaceDiagnostics: bool
    workDoneProgress: bool | None = None


class DocumentFilter(BaseModel):
    language: str | None = None
    scheme: str | None = None
    pattern: str | None = None


class DiagnosticRegistrationOptions(BaseModel):
    identifier: str
    interFileDependencies: bool
    workspaceDiagnostics: bool
    workDoneProgress: bool | None = None
    documentSelector: list[DocumentFilter] | None = None
    id: str | None = None

class TextDocumentSyncKind(IntEnum):
    NONE = 0
    FULL = 1
    INCREMENTAL = 2

class TextDocumentSyncOptions(BaseModel):
    openClose: bool | None = None
    change: TextDocumentSyncKind | None = None

class ServerCapabilities(BaseModel):
    diagnosticProvider: DiagnosticOptions | DiagnosticRegistrationOptions | None = None
    textDocumentSync: TextDocumentSyncOptions


class ServerInfo(BaseModel):
    name: str
    version: str | None = None


class InitializeResult(BaseModel):
    capabilities: ServerCapabilities
    serverInfo: ServerInfo

class ResponseMessage(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str

class InitializeResponse(ResponseMessage):
    result: InitializeResult

class ShutdownResponse(ResponseMessage):
    result: None = None


class PublishDiagnosticsNotification(BaseModel):

