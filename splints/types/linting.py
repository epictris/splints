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


class Tag(StrEnum):
    UNNECESSARY = "unnecessary"
    DEPRECATED = "deprecated"


class TextFormat(StrEnum):
    STRIKETHROUGH = "strikethrough"
    FADE = "fade"


class LintRule(BaseModel):
    pattern: str
    message: str
    code: str | None = None
    format: TextFormat | None = None
    severity: Severity = Severity.WARNING
    multiline: bool = False
    file_globs: list[str]
    engine: RegexEngine = RegexEngine.PYTHON


class Rules(RootModel):
    root: list[LintRule]
