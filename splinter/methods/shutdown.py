from splinter.decorators import method
from splinter.types.methods.shutdown import ShutdownRequest, ShutdownResponse
from splinter.types.shared import State


@method(ShutdownRequest, ShutdownResponse)
def shutdown(message: ShutdownRequest, state: State):
    return ShutdownResponse(id=message.id)
