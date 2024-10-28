from splinter.rules import parse
from splinter.register_methods import register_methods
from splinter.server import Server
from splinter.logger import logger


def run():
    try:
        logger.info("Starting server")
        rules = parse()
        server = Server(rules=rules)
        register_methods(server)
        server.start()
    except Exception as e:
        logger.exception(e)
        raise e
