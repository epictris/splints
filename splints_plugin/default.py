import os
import yaml

from splints.types.linting import LintRule, Rules


def parse() -> list[LintRule]:
    rules_file = os.getenv("SPLINTS_RULES", "splints.yaml")
    return Rules.model_validate(yaml.safe_load(open(rules_file))).root
