import os
import yaml

from splinter.types.linting import LintRule, Rules


def parse() -> list[LintRule]:
    rules_file = os.getenv("SPLINTER_RULES", "splinter.yaml")
    return Rules.model_validate(yaml.safe_load(open(rules_file))).root
