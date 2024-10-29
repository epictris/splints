from splints.decorators import method
from splints.types.methods.exit import ExitNotification
from splints.types.server import State


@method(ExitNotification)
def exit(message: ExitNotification, state: State):
    return None
