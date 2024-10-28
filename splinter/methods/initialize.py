from splinter.decorators import method

from splinter.types.methods.initialize import (
    DiagnosticOptions,
    InitializeRequest,
    InitializeResponse,
    InitializeResult,
    ServerCapabilities,
    ServerInfo,
    TextDocumentSyncKind,
    TextDocumentSyncOptions,
)
from splinter.types.shared import State


@method(InitializeRequest, InitializeResponse)
def initialize(message: InitializeRequest, state: State):
    return InitializeResponse(
        id=message.id,
        result=InitializeResult(
            capabilities=ServerCapabilities(
                diagnosticProvider=DiagnosticOptions(
                    interFileDependencies=False,
                    workspaceDiagnostics=False,
                ),
                textDocumentSync=TextDocumentSyncOptions(
                    openClose=True,
                    change=TextDocumentSyncKind.INCREMENTAL,
                ),
            ),
            serverInfo=ServerInfo(name="python-lsp", version="0.0.0"),
        ),
    )
