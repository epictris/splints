from typing import Literal
from splints.types.base import NotificationBase


class ExitNotification(NotificationBase):
    method: Literal["exit"]
