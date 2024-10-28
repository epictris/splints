from typing import Literal
from splints.types.base import RequestBase, ResponseBase


class ShutdownResponse(ResponseBase):
    result: None = None


class ShutdownRequest(RequestBase):
    id: int | str
    method: Literal["shutdown"]