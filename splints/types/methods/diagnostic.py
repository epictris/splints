from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from splints.types.lsp.base import RequestBase, ResponseBase
from splints.types.lsp.shared import Diagnostic, TextDocumentIdentifier


class DocumentDiagnosticReportKind(StrEnum):
    FULL = "full"
    UNCHANGED = "unchanged"


class FullDocumentDiagnosticReport(BaseModel):
    kind: Literal[DocumentDiagnosticReportKind.FULL] = DocumentDiagnosticReportKind.FULL
    resultId: str | None = None
    items: list[Diagnostic]


class UnchangedDocumentDiagnosticReport(BaseModel):
    kind: Literal[DocumentDiagnosticReportKind.UNCHANGED] = (
        DocumentDiagnosticReportKind.UNCHANGED
    )
    resultId: str


class RelatedFullDocumentDiagnosticReport(FullDocumentDiagnosticReport):
    relatedDocuments: (
        list[FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport] | None
    ) = None


class RelatedUnchangedDocumentDiagnosticReport(UnchangedDocumentDiagnosticReport):
    relatedDocuments: (
        list[FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport] | None
    ) = None


class DocumentDiagnosticParams(BaseModel):
    textDocument: TextDocumentIdentifier
    identifier: str | None = None
    previousResultId: str | None = None


class DocumentDiagnosticRequest(RequestBase):
    method: Literal["textDocument/diagnostic"]
    params: DocumentDiagnosticParams


class DocumentDiagnosticResponse(ResponseBase):
    result: (
        RelatedFullDocumentDiagnosticReport | RelatedUnchangedDocumentDiagnosticReport
    )
