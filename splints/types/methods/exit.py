from typing import Literal
from splints.types.lsp.base import NotificationBase


class ExitNotification(NotificationBase):
    method: Literal["exit"]
