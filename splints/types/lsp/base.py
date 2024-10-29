from typing import Any, Literal

from pydantic import BaseModel


class Message(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"


class RequestBase(Message):
    id: int | str
    method: str
    params: Any = None


class NotificationBase(Message):
    method: str
    params: Any = None


class ResponseBase(Message):
    id: int | str
    result: Any = None
    error: Any = None
