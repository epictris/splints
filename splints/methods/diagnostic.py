from splints.decorators import method
from splints.diagnostics import generate_diagnostics
from splints.types.methods.diagnostic import (
    DocumentDiagnosticRequest,
    DocumentDiagnosticResponse,
    RelatedFullDocumentDiagnosticReport,
    RelatedUnchangedDocumentDiagnosticReport,
)
from splints.types.shared import State


@method(DocumentDiagnosticRequest, DocumentDiagnosticResponse)
def diagnostic(message: DocumentDiagnosticRequest, state: State):
    text_document = state.text_documents[message.params.textDocument.uri]
    diagnostics = generate_diagnostics(text_document=text_document, rules=state.rules)
    existing_diagnostics = state.diagnostics_by_uri.get(text_document.uri, set())
    if (
        existing_diagnostics == diagnostics
        and message.params.previousResultId is not None
    ):
        return DocumentDiagnosticResponse(
            id=message.id,
            result=RelatedUnchangedDocumentDiagnosticReport(
                relatedDocuments=[],
                resultId=message.params.previousResultId,
            ),
        )
    else:
        state.diagnostics_by_uri[text_document.uri] = diagnostics
        return DocumentDiagnosticResponse(
            id=message.id,
            result=RelatedFullDocumentDiagnosticReport(
                relatedDocuments=[],
                items=list(diagnostics),
                resultId=str(message.id),
            ),
        )
