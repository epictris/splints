from splints.decorators import method
from splints.diagnostics import generate_diagnostics
from splints.types.methods.diagnostic import (
    DocumentDiagnosticRequest,
    DocumentDiagnosticResponse,
    RelatedFullDocumentDiagnosticReport,
    RelatedUnchangedDocumentDiagnosticReport,
)
from splints.types.server import State


@method(DocumentDiagnosticRequest, DocumentDiagnosticResponse)
def diagnostic(message: DocumentDiagnosticRequest, state: State):
    text_document = state.text_documents[message.params.textDocument.uri]
    diagnostics = generate_diagnostics(
        text_document=text_document.document, rules=text_document.lint_rules
    )
    if (
        text_document.diagnostics == diagnostics
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
        text_document.diagnostics = diagnostics
        return DocumentDiagnosticResponse(
            id=message.id,
            result=RelatedFullDocumentDiagnosticReport(
                relatedDocuments=[],
                items=list(diagnostics),
                resultId=str(message.id),
            ),
        )
