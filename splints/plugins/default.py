import os
import yaml

from splints.types.linting import LintRule, PatternReplacement

LOCATIONS_TO_CHECK = ["splints.yaml"]


def _locate_rules_file() -> str | None:
    rules_file = os.getenv("SPLINTS_RULES")
    if rules_file is not None:
        return rules_file
    for location in LOCATIONS_TO_CHECK:
        if os.path.exists(location):
            return location
    return None


def load_rules() -> list[LintRule]:
    rules_file = _locate_rules_file()
    if rules_file is None:
        return list()
    rules = yaml.safe_load(open(rules_file))
    assert isinstance(rules, list)
    parsed_rules: list[LintRule] = []
    for rule in rules:
        assert isinstance(rule, dict)
        replacement_options = rule.get("replacement_options")
        parsed_replacement_options: list[PatternReplacement] = []
        if replacement_options is not None:
            assert isinstance(replacement_options, list)
            for replacement in replacement_options:
                parsed_replacement = PatternReplacement(**replacement)
                parsed_replacement_options.append(parsed_replacement)
        rule["replacement_options"] = parsed_replacement_options
        parsed_rules.append(LintRule(**rule))
    return parsed_rules
