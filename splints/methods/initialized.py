from typing import Literal

from pydantic import BaseModel
from splints.decorators import method
from splints.types.lsp.base import NotificationBase
from splints.types.server import State


class InitializedParams(BaseModel):
    pass


class InitializedNotification(NotificationBase):
    method: Literal["initialized"]
    params: InitializedParams


@method(InitializedNotification)
def initialized(args: InitializedNotification, state: State):
    return None
