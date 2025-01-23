from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class TextFormat(StrEnum):
    STRIKETHROUGH = "strikethrough"
    FADE = "fade"


class CodeActionType(StrEnum):
    REPLACE = "replace"
    IMPORT = "import"

class PatternScope(StrEnum):
    CHARACTERS = "characters"
    LINES = "lines"


@dataclass(kw_only=True)
class PatternReplacement:
    description: str | None = None
    pattern: str = "(\n|.)*"
    replacement: str
    imports: list[str] | None = None
    scope: PatternScope = PatternScope.CHARACTERS


class ActiveLintRule(BaseModel):
    pattern: str
    message: str
    code: str | None
    format: TextFormat | None
    severity: Severity
    multiline: bool


LintRuleId = int


@dataclass(kw_only=True)
class LintRule:
    pattern: str
    message: str
    code: str | None = None
    include_globs: list[str] = field(default_factory=lambda: ["*"])
    exclude_globs: list[str] = field(default_factory=list)
    severity: Severity = Severity.WARNING
    format: TextFormat | None = None
    multiline: bool = False
    replacement_options: list[PatternReplacement] | None = None
