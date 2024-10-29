from splints.methods.code_action_request import code_action_request
from splints.methods.diagnostic import diagnostic
from splints.methods.document_changed import document_changed
from splints.methods.document_opened import document_opened
from splints.methods.document_closed import document_closed
from splints.methods.initialize import initialize
from splints.methods.initialized import initialized
from splints.methods.shutdown import shutdown
from splints.methods.exit import exit
from splints.server import Server


def register_methods(server: Server):
    server.register_method(name=initialize.arg_type.__name__, func=initialize.func)
    server.register_method(name=initialized.arg_type.__name__, func=initialized.func)
    server.register_method(name=diagnostic.arg_type.__name__, func=diagnostic.func)
    server.register_method(
        name=document_changed.arg_type.__name__, func=document_changed.func
    )
    server.register_method(
        name=document_opened.arg_type.__name__, func=document_opened.func
    )
    server.register_method(
        name=document_closed.arg_type.__name__, func=document_closed.func
    )
    server.register_method(name=shutdown.arg_type.__name__, func=shutdown.func)
    server.register_method(name=exit.arg_type.__name__, func=exit.func)
    server.register_method(
        name=code_action_request.arg_type.__name__, func=code_action_request.func
    )
