from pydantic import RootModel

from splints.methods.initialized import InitializedNotification
from splints.types.methods.diagnostic import (
    DocumentDiagnosticRequest,
    DocumentDiagnosticResponse,
)
from splints.types.methods.document_changed import DidChangeTextDocumentNotification
from splints.types.methods.document_opened import DidOpenTextDocumentNotification
from splints.types.methods.exit import ExitNotification
from splints.types.methods.initialize import InitializeRequest, InitializeResponse
from splints.types.methods.shutdown import ShutdownRequest, ShutdownResponse


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
