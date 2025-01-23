from splints.decorators import method
import os
import fnmatch

from splints.types.linting import ActiveLintRule
from splints.types.methods.document_opened import DidOpenTextDocumentNotification
from splints.types.server import State, TextDocumentData

import urllib.parse


@method(DidOpenTextDocumentNotification)
def document_opened(args: DidOpenTextDocumentNotification, state: State):
    file_path = os.path.relpath(
        urllib.parse.urlparse(args.params.textDocument.uri).path
    )
    applicable_rules = {
        rule_id: ActiveLintRule(
            pattern=rule.pattern,
            message=rule.message,
            code=rule.code,
            format=rule.format,
            severity=rule.severity,
            multiline=rule.multiline,
        )
        for rule_id, rule in state.lint_rules.items()
        if any(fnmatch.fnmatch(file_path, path) for path in rule.include_globs)
    }
    state.text_documents[args.params.textDocument.uri] = TextDocumentData(
        document=args.params.textDocument,
        lint_rules=applicable_rules,
        diagnostics=set(),
    )
    return None
