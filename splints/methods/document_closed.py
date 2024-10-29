from splints.decorators import method

from splints.types.methods.document_closed import DidCloseTextDocumentNotification
from splints.types.server import State


@method(DidCloseTextDocumentNotification)
def document_closed(args: DidCloseTextDocumentNotification, state: State):
    state.text_documents.pop(args.params.textDocument.uri)
    return None
