from typing import Callable
from splinter.logger import logger
from typing import TypeVar

from splinter.rpc import await_message, rpc_write
from splinter.types.base import (
    NotificationBase,
    RequestBase,
    ResponseBase,
)


from splinter.types.methods.exit import ExitNotification
from splinter.types.shared import State
from splinter.types.unions import Notification, Request, Response


NotificationDataT = TypeVar("NotificationDataT", bound=NotificationBase)
RequestDataT = TypeVar("RequestDataT", bound=RequestBase)
ResponseDataT = TypeVar("ResponseDataT", bound=ResponseBase)


class Server:
    def __init__(self):
        self.method_handlers: dict[str, Callable] = {}
        self._state = State(text_documents={}, diagnostics_by_uri={})

    def register_method(
        self,
        name: str,
        func: Callable[[RequestDataT, State], ResponseDataT]
        | Callable[[NotificationDataT, State], None],
    ) -> None:
        self.method_handlers[name] = func

    def _process_output(self, result: Response | None) -> None:
        if isinstance(result, Response):
            rpc_write(result)

    def _process_input(self, message: Request | Notification) -> Response | None:
        logger.info(message.__class__.__name__)
        if message.__class__.__name__ not in self.method_handlers:
            return
        return self.method_handlers[message.__class__.__name__](message, self._state)

    def start(self):
        while True:
            message = await_message()
            result = self._process_input(message)
            self._process_output(result)
            if isinstance(message, ExitNotification):
                return
