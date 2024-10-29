from pydantic import RootModel

from splints.methods.initialized import InitializedNotification
from splints.types.methods.code_action_request import CodeActionRequest, CodeActionResponse
from splints.types.methods.configution_changed import (
    DidChangeConfigurationClientCapabilitiesNotification,
)
from splints.types.methods.diagnostic import (
    DocumentDiagnosticRequest,
    DocumentDiagnosticResponse,
)
from splints.types.methods.document_changed import DidChangeTextDocumentNotification
from splints.types.methods.document_closed import DidCloseTextDocumentNotification
from splints.types.methods.document_opened import DidOpenTextDocumentNotification
from splints.types.methods.exit import ExitNotification
from splints.types.methods.initialize import InitializeRequest, InitializeResponse
from splints.types.methods.shutdown import ShutdownRequest, ShutdownResponse


Notification = (
    InitializedNotification
    | DidOpenTextDocumentNotification
    | DidCloseTextDocumentNotification
    | DidChangeTextDocumentNotification
    | ExitNotification
    | DidChangeConfigurationClientCapabilitiesNotification
)
Request = InitializeRequest | ShutdownRequest | DocumentDiagnosticRequest | CodeActionRequest


Response = InitializeResponse | DocumentDiagnosticResponse | ShutdownResponse | CodeActionResponse


class RootInput(RootModel):
    root: Notification | Request
