import importlib
from splinter.logger import logger
from splinter.types.linting import Rules, LintRule
import os


def parse() -> list[LintRule]:
    splinter_parser = os.environ.get("SPLINTER_PARSER", "default")
    logger.info(f"Using splinter parser {splinter_parser}")
    rules = importlib.import_module(f"splinter_parser.{splinter_parser}").parse()
    scopes = Rules.model_validate(rules)
    return scopes.root
