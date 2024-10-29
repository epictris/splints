from typing import Any, Literal
from pydantic import BaseModel

from splints.types.lsp.base import NotificationBase


class DidChangeConfigurationParams(BaseModel):
    settings: Any


class DidChangeConfigurationClientCapabilitiesNotification(NotificationBase):
    method: Literal["workspace/didChangeConfiguration"]
    params: DidChangeConfigurationParams
