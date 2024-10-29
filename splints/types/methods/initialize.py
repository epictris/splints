from enum import IntEnum, StrEnum
from typing import Any, Literal
from pydantic import BaseModel

from splints.types.lsp.base import RequestBase, ResponseBase
from splints.types.lsp.shared import DocumentUri


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
    codeActionProvider: bool = True


class ClientInfo(BaseModel):
    name: str
    version: str | None = None


class Workspace(BaseModel):
    pass


class TagSupport(BaseModel):
    valueSet: list[Literal[1] | Literal[2]]


class ServerInfo(BaseModel):
    name: str
    version: str | None = None


class InitializeResult(BaseModel):
    capabilities: ServerCapabilities
    serverInfo: ServerInfo


class InitializeResponse(ResponseBase):
    result: InitializeResult


class PublishDiagnosticsClientCapabilities(BaseModel):
    relatedInformation: bool
    tagSupport: TagSupport | None = None
    versionSupport: bool | None = None
    codeDescriptionSupport: bool | None = None
    dataSupport: bool | None = None


class DiagnosticClientCapabilities(BaseModel):
    dynamicRegistration: bool | None = None
    relatedDocumentSupport: bool | None = None


class TextDocumentClientCapabilities(BaseModel):
    publishDiagnostics: PublishDiagnosticsClientCapabilities
    diagnostic: DiagnosticClientCapabilities


class ClientCapabilities(BaseModel):
    textDocument: TextDocumentClientCapabilities


class TraceValue(StrEnum):
    OFF = "off"
    MESSAGE = "messages"
    VERBOSE = "verbose"


class WorkspaceFolder(BaseModel):
    pass


class InitializeParams(BaseModel):
    processId: int | None = None
    clientInfo: ClientInfo | None = None
    locale: str | None = None
    rootPath: str | None = None
    rootUri: DocumentUri | None = None
    initializationOptions: Any = None
    capabilities: ClientCapabilities
    trace: TraceValue | None = None
    workspaceFolders: list[WorkspaceFolder] | None = None


class InitializeRequest(RequestBase):
    method: Literal["initialize"]
    params: InitializeParams
