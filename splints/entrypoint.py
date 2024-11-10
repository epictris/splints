from splints.rules import load_plugins
from splints.register_methods import register_methods
from splints.server import Server
from splints.logger import logger


def run():
    try:
        logger.info("Starting server")
        rules = load_plugins()
        server = Server(rules=rules)
        register_methods(server)
        server.start()
    except Exception as e:
        logger.exception(e)
        raise e
