import importlib
from splints.logger import logger
from splints.types.linting import LintRule, LintRuleId
import pkgutil
import splints.plugins as plugins


def load_plugins() -> dict[LintRuleId, LintRule]:
    rules: list[LintRule] = []
    for _, name, _ in pkgutil.iter_modules(plugins.__path__, plugins.__name__ + "."):
        logger.info(f"Loading plugin {name}")
        try:
            plugin_rules = importlib.import_module(name).load_rules()
            assert isinstance(
                plugin_rules, list
            ), f"{name} failed to generate a valid rules list"
            for rule in plugin_rules:
                assert isinstance(
                    rule, LintRule
                ), f"{name} failed to generate a valid rules list"
                rules.append(rule)
        except BaseException as e:
            logger.error(e)
    return {id: rule for id, rule in enumerate(rules)}
