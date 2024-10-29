from splints.decorators import method

from splints.types.server import State


@method(DidChangeConfigurationClientCapabilities)
def document_closed(args: DidChangeConfigurationClientCapabilities, state: State):
    state.text_documents.pop(args.params.textDocument.uri)
    return None
