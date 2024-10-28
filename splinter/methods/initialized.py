from typing import Literal

from pydantic import BaseModel
from splinter.decorators import method
from splinter.types.base import NotificationBase
from splinter.types.shared import State


class InitializedParams(BaseModel):
    pass


class InitializedNotification(NotificationBase):
    method: Literal["initialized"]
    params: InitializedParams


@method(InitializedNotification)
def initialized(args: InitializedNotification, state: State):
    return None
