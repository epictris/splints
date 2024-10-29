import sys
from dataclasses import dataclass
from splints.logger import logger

from splints.types.lsp.base import Message
from splints.types.lsp.unions import Notification, Request, RootInput


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


def read_header() -> Header:
    header_fields = read_header_fields()
    return Header(
        content_length=parse_content_length(header_fields),
        content_type=parse_content_type(header_fields),
    )


def read_content(header: Header) -> str:
    return sys.stdin.buffer.read(header.content_length).decode("utf-8")


def await_message() -> Request | Notification:
    content = read_content(read_header())
    message = RootInput.model_validate_json(content).root
    logger.info(f"Recieved message with method {message.method}")
    return message


def rpc_write(message: Message) -> None:
    content = message.model_dump_json(indent=4)
    headers = f"Content-Length: {len(content)}\r\n"
    sys.stdout.write(headers + "\r\n" + content)
    sys.stdout.flush()
