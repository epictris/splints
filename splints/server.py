from typing import Callable
from splints.logger import logger
from typing import TypeVar

from splints.rpc import await_message, rpc_write
from splints.types.lsp.base import (
    NotificationBase,
    RequestBase,
    ResponseBase,
)


from splints.types.linting import LintRule, LintRuleId
from splints.types.methods.exit import ExitNotification
from splints.types.server import State
from splints.types.lsp.unions import Notification, Request, Response


NotificationDataT = TypeVar("NotificationDataT", bound=NotificationBase)
RequestDataT = TypeVar("RequestDataT", bound=RequestBase)
ResponseDataT = TypeVar("ResponseDataT", bound=ResponseBase)


class Server:
    def __init__(self, rules: dict[LintRuleId, LintRule]):
        self.method_handlers: dict[str, Callable] = {}
        self._state = State(text_documents={}, lint_rules=rules)

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
