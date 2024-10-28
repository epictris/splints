from splints.decorators import method

from splints.types.methods.document_opened import DidOpenTextDocumentNotification
from splints.types.shared import State


@method(DidOpenTextDocumentNotification)
def document_opened(args: DidOpenTextDocumentNotification, state: State):
    state.text_documents[args.params.textDocument.uri] = args.params.textDocument
    return None
