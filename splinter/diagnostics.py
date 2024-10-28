import re

from splinter.types.shared import Diagnostic, DiagnosticSeverity, DiagnosticTag, Position, Range

DEPRECATED_PATTERNS = [
    "deprecated",
    "pattern",
]


def generate_diagnostics(text: str) -> set[Diagnostic]:
    lines = text.splitlines()
    diagnostics: set[Diagnostic] = set()
    for lineno, line in enumerate(lines):
        for pattern in DEPRECATED_PATTERNS:
            matches = re.finditer(pattern, line)
            for match in matches:
                diagnostics.add(
                    Diagnostic(
                        source="splinter",
                        severity=DiagnosticSeverity.INFO,
                        tags=frozenset({DiagnosticTag.UNNECESSARY, DiagnosticTag.DEPRECATED}),
                        code=f"test-deprecated-pattern-code",
                        range=Range(
                            start=Position(line=lineno, character=match.start()),
                            end=Position(line=lineno, character=match.end()),
                        ),
                        message=f"Deprecated pattern '{pattern}'",
                    )
                )
    return diagnostics
