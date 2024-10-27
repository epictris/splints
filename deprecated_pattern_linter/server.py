from dataclasses import dataclass
from logging import FileHandler, Logger, getLogger, DEBUG
import sys
from typing import Any
from pydantic import BaseModel

from deprecated_pattern_linter.client_types import (
    DidChangeTextDocumentNotification,
    DidOpenTextDocumentNotification,
    DocumentDiagnosticRequest,
    DocumentUri,
    InitializeRequest,
    InitializedNotification,
    InputMessage,
    RootMessage,
    ShutdownRequest,
    TextDocumentContentChangeEvent,
    TextDocumentItem,
)
from deprecated_pattern_linter.server_types import (
    DiagnosticOptions,
    InitializeResponse,
    InitializeResult,
    ResponseMessage,
    ServerCapabilities,
    ServerInfo,
    ShutdownResponse,
    TextDocumentSyncKind,
    TextDocumentSyncOptions,
)

logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(FileHandler("/Users/tris/test/logs.logs"))
logger.info("Starting server")


def read_field() -> bytes:
    field: bytes = b""
    while True:
        x = sys.stdin.buffer.read(1)
        if x:
            field += x
        if field[-2:] == b"\r\n":
            return field


def read_header_fields() -> list[str]:
    fields: list[str] = []
    while True:
        field = read_field()
        if field == b"\r\n":
            return fields
        fields.append(field.decode("ascii"))


def parse_content_length(header_fields: list[str]) -> int:
    for field in header_fields:
        if field.startswith("Content-Length: "):
            return int(field[15:-2])
    raise ValueError(f"Content-Length not found in header fields: {header_fields}")


def parse_content_type(header_fields: list[str]) -> str | None:
    for field in header_fields:
        if field.startswith("Content-Type: "):
            return field[13:-2]
    return None


@dataclass(kw_only=True)
class Header:
    content_length: int
    content_type: str | None


class ResponseError(BaseModel):
    code: int
    message: str
    data: Any


def read_header() -> Header:
    header_fields = read_header_fields()
    return Header(
        content_length=parse_content_length(header_fields),
        content_type=parse_content_type(header_fields),
    )


def read_content(header: Header) -> str:
    return sys.stdin.buffer.read(header.content_length).decode("utf-8")


def read_message() -> InputMessage:
    content = read_content(read_header())
    message = RootMessage.model_validate_json(content).root
    logger.info(f"recieved message with method {message.method}")
    logger.info(content)
    return message


def run():
    try:
        start(logger)
    except Exception as e:
        logger.error(e)
        raise e


def rpc_write(message: ResponseMessage) -> None:
    content = message.model_dump_json(indent=4)
    headers = f"Content-Length: {len(content)}\r\n"
    sys.stdout.write(headers + "\r\n" + content)
    sys.stdout.flush()


def apply_change(text: str, change: TextDocumentContentChangeEvent) -> str:
    if change.range is None:
        return change.text
    lines = text.splitlines()

    chars_preceding_change = lines[change.range.start.line][:change.range.start.character] if len(lines) > change.range.start.line else ""
    chars_following_change = lines[change.range.end.line][change.range.end.character:] if len(lines) > change.range.end.line else ""

    update = chars_preceding_change + change.text + chars_following_change
    lines = lines[:change.range.start.line] + [update] + lines[change.range.end.line + 1:]

    return "\n".join(lines) + "\n"

def start(logger: Logger):
    open_documents: dict[DocumentUri, TextDocumentItem] = {}
    while True:
        message = read_message()
        if isinstance(message, InitializeRequest):
            rpc_write(
                InitializeResponse(
                    id=message.id,
                    result=InitializeResult(
                        capabilities=ServerCapabilities(
                            diagnosticProvider=DiagnosticOptions(
                                interFileDependencies=False, workspaceDiagnostics=False
                            ),
                            textDocumentSync=TextDocumentSyncOptions(
                                openClose=True, change=TextDocumentSyncKind.INCREMENTAL
                            ),
                        ),
                        serverInfo=ServerInfo(name="python-lsp", version="0.0.0"),
                    ),
                )
            )
        if isinstance(message, InitializedNotification):
            pass
        if isinstance(message, ShutdownRequest):
            rpc_write(ShutdownResponse(id=message.id))
            logger.info("Shutting down")
            return
        if isinstance(message, DidOpenTextDocumentNotification):
            open_documents[message.params.textDocument.uri] = message.params.textDocument
        if isinstance(message, DidChangeTextDocumentNotification):
            text_document = open_documents[message.params.textDocument.uri]
            for change in message.params.contentChanges:
                text_document.text = apply_change(text_document.text, change)
            text_document.version = message.params.textDocument.version

        if isinstance(message, DocumentDiagnosticRequest):
            pass
