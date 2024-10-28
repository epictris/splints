from splinter.decorators import method
from splinter.types.methods.exit import ExitNotification
from splinter.types.shared import State


@method(ExitNotification)
def exit(message: ExitNotification, state: State):
    return None
