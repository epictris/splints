from typing import Any, Literal

from pydantic import BaseModel


class Message(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"


class Request(Message):
    id: int | str
    method: str
    params: Any


class Notification(Message):
    method: str
    params: Any


class Response(Message):
    id: int | str
    result: Any = None
    error: Any = None


DocumentUri = str

class TextDocumentItem(BaseModel):
    uri: DocumentUri
    languageId: str
    version: int
    text: str

class TextDocumentIdentifier(BaseModel):
    uri: DocumentUri

class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: int

class Position(BaseModel, frozen=True):
    line: int
    character: int

class Range(BaseModel, frozen=True):
    start: Position
    end: Position
