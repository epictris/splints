from splints.decorators import method

from splints.types.methods.document_closed import DidCloseTextDocumentNotification
from splints.types.shared import State


@method(DidCloseTextDocumentNotification)
def document_opened(args: DidCloseTextDocumentNotification, state: State):
    state.text_documents.pop(args.params.textDocument.uri)
    return None
