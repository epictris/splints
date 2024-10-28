import importlib
from splints.logger import logger
from splints.types.linting import Rules, LintRule
import os


def parse() -> list[LintRule]:
    splints_plugin = os.getenv("SPLINTS_PLUGIN", "default")
    logger.info(f"Using splints plugin {splints_plugin}")
    rules = importlib.import_module(f"splints_plugin.{splints_plugin}").parse()
    scopes = Rules.model_validate(rules)
    return scopes.root
