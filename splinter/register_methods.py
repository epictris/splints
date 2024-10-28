from splinter.methods.diagnostic import diagnostic
from splinter.methods.document_changed import document_changed
from splinter.methods.document_opened import document_opened
from splinter.methods.initialize import initialize
from splinter.methods.initialized import initialized
from splinter.methods.shutdown import shutdown
from splinter.server import Server


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
    server.register_method(name=shutdown.arg_type.__name__, func=shutdown.func)
