from splinter.decorators import method

from splinter.types.methods.document_opened import DidOpenTextDocumentNotification
from splinter.types.shared import State


@method(DidOpenTextDocumentNotification)
def document_opened(args: DidOpenTextDocumentNotification, state: State):
    state.text_documents[args.params.textDocument.uri] = args.params.textDocument
    return None
