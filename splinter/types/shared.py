from dataclasses import dataclass
from enum import IntEnum
from typing import Any
from pydantic import BaseModel

from splinter.types.linting import LintRule



DocumentUri = str


class Position(BaseModel, frozen=True):
    line: int
    character: int


class Range(BaseModel, frozen=True):
    start: Position
    end: Position


class TextDocumentItem(BaseModel):
    uri: DocumentUri
    languageId: str
    version: int
    text: str


class TextDocumentIdentifier(BaseModel):
    uri: DocumentUri


class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: int


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
    tags: frozenset[DiagnosticTag] | None = None
    relatedInformation: tuple[DiagnosticRelatedInformation] | None = None
    data: Any = None


@dataclass(kw_only=True)
class State:
    text_documents: dict[DocumentUri, TextDocumentItem]
    diagnostics_by_uri: dict[DocumentUri, set[Diagnostic]]
    rules: list[LintRule]
