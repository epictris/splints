import os
import fnmatch
import re

from splints.types.linting import LintRule, Severity, TextFormat
from splints.types.shared import (
    Diagnostic,
    DiagnosticSeverity,
    DiagnosticTag,
    Position,
    Range,
    TextDocumentItem,
)
import urllib.parse

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


def generate_diagnostics(
    text_document: TextDocumentItem, rules: list[LintRule]
) -> set[Diagnostic]:
    file_path = os.path.relpath(urllib.parse.urlparse(text_document.uri).path)
    applicable_rules = [
        rule
        for rule in rules
        if any(fnmatch.fnmatch(file_path, path) for path in rule.file_globs)
    ]
    lines = text_document.text.splitlines()
    diagnostics: set[Diagnostic] = set()
    for lineno, line in enumerate(lines):
        for rule in applicable_rules:
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
                    )
                )
    return diagnostics
