from dataclasses import dataclass

from splints.types.linting import ActiveLintRule, LintRule, LintRuleId
from splints.types.lsp.shared import Diagnostic, DocumentUri, TextDocumentItem


@dataclass(kw_only=True)
class TextDocumentData:
    document: TextDocumentItem
    lint_rules: dict[LintRuleId, ActiveLintRule]
    diagnostics: set[Diagnostic]


@dataclass(kw_only=True)
class State:
    text_documents: dict[DocumentUri, TextDocumentData]
    lint_rules: dict[LintRuleId, LintRule]
