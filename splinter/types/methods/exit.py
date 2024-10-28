from typing import Literal
from splinter.types.base import NotificationBase


class ExitNotification(NotificationBase):
    method: Literal["exit"]
