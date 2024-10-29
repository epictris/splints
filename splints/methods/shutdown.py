from splints.decorators import method
from splints.types.methods.shutdown import ShutdownRequest, ShutdownResponse
from splints.types.server import State


@method(ShutdownRequest, ShutdownResponse)
def shutdown(message: ShutdownRequest, state: State):
    return ShutdownResponse(id=message.id)
