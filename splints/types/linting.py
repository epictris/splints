from dataclasses import dataclass, field
from enum import StrEnum


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class Tag(StrEnum):
    DEPRECATED = "deprecated"
    UNNECESSARY = "unnecessary"


@dataclass(kw_only=True)
class PatternReplacement:
    description: str | None = None
    pattern: str = "(\n|.)*"
    replacement: str
    imports: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.description is not None:
            assert isinstance(self.description, str), self.description
        assert isinstance(self.pattern, str), self.pattern
        assert isinstance(self.replacement, str), self.replacement
        for import_ in self.imports:
            assert isinstance(import_, str), import_


LintRuleId = int


@dataclass(kw_only=True)
class LintRule:
    pattern: str
    message: str
    code: str | None = None
    include_globs: list[str] = field(default_factory=lambda: ["*"])
    exclude_globs: list[str] = field(default_factory=list)
    severity: Severity = Severity.WARNING
    tags: list[Tag] = field(default_factory=list)
    replacement_options: list[PatternReplacement] = field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.pattern, str), self.pattern
        assert isinstance(self.message, str), self.message
        if self.code is not None:
            assert isinstance(self.code, str), self.code
        for glob in self.include_globs:
            assert isinstance(glob, str), glob
        for glob in self.exclude_globs:
            assert isinstance(glob, str), glob
        self.severity = Severity(self.severity)
        self.tags = [Tag(tag) for tag in self.tags]
        self.replacement_options = [
            replacement
            if isinstance(replacement, PatternReplacement)
            else PatternReplacement(**replacement)
            for replacement in self.replacement_options
        ]
