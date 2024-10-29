from enum import StrEnum

from pydantic import BaseModel
from pydantic.root_model import RootModel


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class RegexEngine(StrEnum):
    PYTHON = "python"
    PCRE2 = "pcre2"
    RE2 = "re2"


class TextFormat(StrEnum):
    STRIKETHROUGH = "strikethrough"
    FADE = "fade"


class CodeActionType(StrEnum):
    REPLACE = "replace"
    IMPORT = "import"


class PatternReplacement(BaseModel):
    description: str
    pattern: str
    replacement: str
    imports: list[str] = []


class LintRule(BaseModel):
    pattern: str
    message: str
    code: str | None = None
    include_globs: list[str] = ["*"]
    exclude_globs: list[str] = []
    severity: Severity = Severity.WARNING
    format: TextFormat | None = None
    multiline: bool = False
    engine: RegexEngine = RegexEngine.PYTHON
    replacement_options: list[PatternReplacement] = []


class ActiveLintRule(BaseModel):
    pattern: str
    message: str
    code: str | None
    format: TextFormat | None
    severity: Severity
    multiline: bool
    engine: RegexEngine


LintRuleId = int


class Rules(RootModel):
    root: list[LintRule]
