import re

from splints.types.linting import ActiveLintRule, LintRuleId, Severity, TextFormat
from splints.types.lsp.shared import (
    Diagnostic,
    DiagnosticData,
    DiagnosticSeverity,
    DiagnosticTag,
    Position,
    Range,
    TextDocumentItem,
)

CONVERT_SEVERITY = {
    Severity.ERROR: DiagnosticSeverity.ERROR,
    Severity.WARNING: DiagnosticSeverity.WARNING,
    Severity.INFO: DiagnosticSeverity.INFO,
    Severity.HINT: DiagnosticSeverity.HINT,
}

CONVERT_FORMAT = {
    TextFormat.STRIKETHROUGH: {DiagnosticTag.DEPRECATED},
    TextFormat.FADE: {DiagnosticTag.UNNECESSARY},
}

LineIndex = int
LineCharIndex = int

FileCharIndex = int

LineStartIndex = int
LineEndIndex = int


def _construct_line_index_by_file_char_range_lookup(
    text: str,
) -> dict[tuple[LineStartIndex, LineEndIndex], LineIndex]:
    line_by_char_index_range: dict[tuple[LineStartIndex, LineEndIndex], LineIndex] = {}
    current_line = 0
    current_range_start = 0
    current_range_end = 0
    for index, char in enumerate(text):
        current_range_end = index
        if char == "\n":
            line_by_char_index_range[(current_range_start, current_range_end)] = (
                current_line
            )
            current_line += 1
            current_range_start = current_range_end + 1
    return line_by_char_index_range


def get_line_and_char_index_by_file_char_index(
    index: FileCharIndex,
    line_lookup: dict[tuple[LineStartIndex, LineEndIndex], LineIndex],
) -> tuple[LineIndex, LineCharIndex]:
    for [start, end], line in line_lookup.items():
        if start <= index <= end:
            return (line, index - start)
    raise ValueError(f"No line found for index {index}")


def _gen_multiline_diagnostics(
    rule: ActiveLintRule,
    id: LintRuleId,
    line_by_char_range_lookup: dict[tuple[LineStartIndex, LineEndIndex], LineIndex],
    text: str,
) -> set[Diagnostic]:
    diagnostics: set[Diagnostic] = set()
    for match in re.finditer(rule.pattern, text, re.MULTILINE):
        start_line, start_char = get_line_and_char_index_by_file_char_index(
            index=match.start(), line_lookup=line_by_char_range_lookup
        )
        end_line, end_char = get_line_and_char_index_by_file_char_index(
            index=match.end(), line_lookup=line_by_char_range_lookup
        )
        diagnostics.add(
            Diagnostic(
                source="splints",
                severity=CONVERT_SEVERITY[rule.severity],
                tags=frozenset(CONVERT_FORMAT[rule.format] if rule.format else set()),
                code=rule.code,
                range=Range(
                    start=Position(line=start_line, character=start_char),
                    end=Position(line=end_line, character=end_char),
                ),
                message=rule.message,
                data=DiagnosticData(rule_id=id, text=match.group(0)),
            )
        )
    return diagnostics


def _gen_singleline_diagnostics(
    rule: ActiveLintRule, id: LintRuleId, lines: list[str]
) -> set[Diagnostic]:
    diagnostics: set[Diagnostic] = set()
    for lineno, line in enumerate(lines):
        matches = re.finditer(rule.pattern, line)
        for match in matches:
            diagnostics.add(
                Diagnostic(
                    source="splints",
                    severity=CONVERT_SEVERITY[rule.severity],
                    tags=frozenset(
                        CONVERT_FORMAT[rule.format] if rule.format else set()
                    ),
                    code=rule.code,
                    range=Range(
                        start=Position(line=lineno, character=match.start()),
                        end=Position(line=lineno, character=match.end()),
                    ),
                    message=rule.message,
                    data=DiagnosticData(rule_id=id, text=match.group(0)),
                )
            )
    return diagnostics


def generate_diagnostics(
    text_document: TextDocumentItem, rules: dict[LintRuleId, ActiveLintRule]
) -> set[Diagnostic]:
    line_by_char_range_lookup = _construct_line_index_by_file_char_range_lookup(
        text_document.text
    )
    lines = text_document.text.splitlines()
    diagnostics: set[Diagnostic] = set()

    for id, rule in rules.items():
        if rule.multiline:
            diagnostics.update(
                _gen_multiline_diagnostics(
                    rule, id, line_by_char_range_lookup, text_document.text
                )
            )
        else:
            diagnostics.update(_gen_singleline_diagnostics(rule, id, lines))

    return diagnostics
