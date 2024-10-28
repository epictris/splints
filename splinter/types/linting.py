from dataclasses import dataclass
from enum import StrEnum


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


@dataclass(kw_only=True)
class LintRule:
    pattern: str
    message: str
    code: str | None = None
    format: TextFormat | None = None
    severity: Severity = Severity.WARNING
    multiline: bool = False
    engine: RegexEngine = RegexEngine.PYTHON


@dataclass(kw_only=True)
class Scope:
    file_types: list[str]
    file_paths: list[str]
    rules: list[LintRule]


@dataclass(kw_only=True)
class Config:
    scopes: list[Scope]
