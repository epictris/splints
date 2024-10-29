import importlib
from splints.logger import logger
from splints.types.linting import LintRule
import os


def parse() -> frozenset[LintRule]:
    splints_plugin = os.getenv("SPLINTS_PLUGIN", "default")
    logger.info(f"Using splints plugin {splints_plugin}")
    rules = importlib.import_module(f"splints_plugin.{splints_plugin}").parse()
    assert isinstance(rules, frozenset)
    for rule in rules:
        assert isinstance(rule, LintRule)
    return rules
