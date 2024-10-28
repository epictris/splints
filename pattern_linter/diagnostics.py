from deprecated_pattern_linter.types.base import Position, Range
from deprecated_pattern_linter.types.server import Diagnostic
import re

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
                        range=Range(
                            start=Position(line=lineno, character=match.start()),
                            end=Position(line=lineno, character=match.end()),
                        ),
                        message=f"Deprecated pattern '{pattern}'",
                    )
                )
    return diagnostics
