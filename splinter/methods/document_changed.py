from splinter.decorators import method
from splinter.diagnostics import generate_diagnostics
from splinter.types.methods.document_changed import (
    DidChangeTextDocumentNotification,
    TextDocumentContentChangeEvent,
)
from splinter.types.methods.publish_diagnostics import (
    PublishDiagnosticsNotification,
    PublishDiagnosticsParams,
)
from splinter.types.shared import State


def apply_change(text: str, change: TextDocumentContentChangeEvent) -> str:
    if change.range is None:
        return change.text
    lines = text.splitlines()

    chars_preceding_change = (
        lines[change.range.start.line][: change.range.start.character]
        if len(lines) > change.range.start.line
        else ""
    )
    chars_following_change = (
        lines[change.range.end.line][change.range.end.character :]
        if len(lines) > change.range.end.line
        else ""
    )

    update = chars_preceding_change + change.text + chars_following_change
    lines = (
        lines[: change.range.start.line] + [update] + lines[change.range.end.line + 1 :]
    )

    return "\n".join(lines) + "\n"


@method(DidChangeTextDocumentNotification)
def document_changed(message: DidChangeTextDocumentNotification, state: State):
    text_document = state.text_documents[message.params.textDocument.uri]
    for change in message.params.contentChanges:
        text_document.text = apply_change(text_document.text, change)
    text_document.version = message.params.textDocument.version
    diagnostics = generate_diagnostics(text_document=text_document, rules=state.rules)
    state.diagnostics_by_uri[text_document.uri] = diagnostics
    return PublishDiagnosticsNotification(
        method="textDocument/publishDiagnostics",
        params=PublishDiagnosticsParams(
            uri=text_document.uri,
            version=text_document.version,
            diagnostics=list(diagnostics),
        ),
    )
