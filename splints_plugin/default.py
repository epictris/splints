import os
import yaml

from splints.types.linting import LintRule, Rules

LOCATIONS_TO_CHECK = ["splints.yaml"]


def _locate_rules_file() -> str | None:
    rules_file = os.getenv("SPLINTS_FILE")
    if rules_file is not None:
        return rules_file
    for location in LOCATIONS_TO_CHECK:
        if os.path.exists(location):
            return location
    return None


def parse() -> frozenset[LintRule]:
    rules_file = _locate_rules_file()
    if rules_file is None:
        return frozenset()
    return Rules.model_validate(yaml.safe_load(open(rules_file))).root
