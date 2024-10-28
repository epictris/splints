from enum import StrEnum
from typing import Any, Literal
from pydantic import BaseModel, RootModel

from pattern_linter.types.base import DocumentUri, Range, Request, TextDocumentIdentifier, TextDocumentItem, VersionedTextDocumentIdentifier


class BaseRequest(BaseModel):
    id: int | str
    method: str
    params: dict[str, Any]

class ClientInfo(BaseModel):
    name: str
    version: str | None = None


class Workspace(BaseModel):
    pass
    
class TagSupport(BaseModel):
    valueSet: list[Literal[1] | Literal[2]]


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



class InitializeRequest(BaseModel):
    id: int | str
    method: Literal["initialize"]
    params: InitializeParams

class ShutdownRequest(BaseModel):
    id: int | str
    method: Literal["shutdown"]

class InitializedParams(BaseModel):
    pass

class InitializedNotification(BaseModel):
    method: Literal["initialized"]
    params: InitializedParams


class DidOpenTextDocumentParams(BaseModel):
    textDocument: TextDocumentItem

class DidOpenTextDocumentNotification(BaseModel):
    method: Literal["textDocument/didOpen"]
    params: DidOpenTextDocumentParams


class TextDocumentContentChangeEvent(BaseModel):
    range: Range | None = None
    text: str

class DidChangeTextDocumentParams(BaseModel):
    textDocument: VersionedTextDocumentIdentifier
    contentChanges: list[TextDocumentContentChangeEvent]

class DidChangeTextDocumentNotification(BaseModel):
    method: Literal["textDocument/didChange"]
    params: DidChangeTextDocumentParams


class DocumentDiagnosticParams(BaseModel):
    textDocument: TextDocumentIdentifier
    identifier: str | None = None
    previousResultId: str | None = None

class DocumentDiagnosticRequest(Request):
    method: Literal["textDocument/diagnostic"]
    params: DocumentDiagnosticParams



InputNotification = InitializedNotification | DidOpenTextDocumentNotification | DidChangeTextDocumentNotification
InputRequest = InitializeRequest | ShutdownRequest | DocumentDiagnosticRequest
InputMessage = InputNotification | InputRequest

class RootMessage(RootModel):
    root: InputMessage
