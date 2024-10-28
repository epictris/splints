from pydantic import RootModel

from splinter.methods.initialized import InitializedNotification
from splinter.types.methods.diagnostic import (
    DocumentDiagnosticRequest,
    DocumentDiagnosticResponse,
)
from splinter.types.methods.document_changed import DidChangeTextDocumentNotification
from splinter.types.methods.document_opened import DidOpenTextDocumentNotification
from splinter.types.methods.exit import ExitNotification
from splinter.types.methods.initialize import InitializeRequest, InitializeResponse
from splinter.types.methods.shutdown import ShutdownRequest, ShutdownResponse


Notification = (
    InitializedNotification
    | DidOpenTextDocumentNotification
    | DidChangeTextDocumentNotification
    | ExitNotification
)
Request = InitializeRequest | ShutdownRequest | DocumentDiagnosticRequest


Response = InitializeResponse | DocumentDiagnosticResponse | ShutdownResponse


class RootInput(RootModel):
    root: Notification | Request
