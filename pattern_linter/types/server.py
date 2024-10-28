from enum import IntEnum, StrEnum
from typing import Any, Literal
from pydantic import BaseModel

from pattern_linter.types.base import (
    DocumentUri,
    Notification,
    Range,
    Response,
)


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


class InitializeResponse(Response):
    result: InitializeResult


class ShutdownResponse(Response):
    result: None = None


class DiagnosticSeverity(IntEnum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    HINT = 4


class CodeDescription(BaseModel):
    href: str


class DiagnosticTag(IntEnum):
    UNNECESSARY = 1
    DEPRECATED = 2


class Location(BaseModel, frozen=True):
    uri: DocumentUri
    range: Range


class DiagnosticRelatedInformation(BaseModel, frozen=True):
    location: Location
    message: str


class Diagnostic(BaseModel, frozen=True):
    range: Range
    severity: DiagnosticSeverity | None = None
    code: str | int | None = None
    codeDescription: CodeDescription | None = None
    source: str | None = None
    message: str
    tags: tuple[DiagnosticTag] | None = None
    relatedInformation: tuple[DiagnosticRelatedInformation] | None = None
    data: Any = None


class PublishDiagnosticsParams(BaseModel):
    uri: DocumentUri
    version: int | None = None
    diagnostics: list[Diagnostic]


class PublishDiagnosticsNotification(Notification):
    method: Literal["textDocument/publishDiagnostics"]
    params: PublishDiagnosticsParams


class DocumentDiagnosticReportKind(StrEnum):
    FULL = "full"
    UNCHANGED = "unchanged"


class FullDocumentDiagnosticReport(BaseModel):
    kind: Literal[DocumentDiagnosticReportKind.FULL] = DocumentDiagnosticReportKind.FULL
    resultId: str | None = None
    items: list[Diagnostic]


class UnchangedDocumentDiagnosticReport(BaseModel):
    kind: Literal[DocumentDiagnosticReportKind.UNCHANGED] = DocumentDiagnosticReportKind.UNCHANGED
    resultId: str


class RelatedFullDocumentDiagnosticReport(FullDocumentDiagnosticReport):
    relatedDocuments: (
        list[FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport] | None
    ) = None


class RelatedUnchangedDocumentDiagnosticReport(UnchangedDocumentDiagnosticReport):
    relatedDocuments: (
        list[FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport] | None
    ) = None

class DocumentDiagnosticResponse(Response):
    result: RelatedFullDocumentDiagnosticReport | RelatedUnchangedDocumentDiagnosticReport
