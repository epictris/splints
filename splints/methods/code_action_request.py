from splints.decorators import method
import re
from splints.types.lsp.shared import Position, Range
from splints.types.methods.code_action_request import (
    CodeAction,
    CodeActionRequest,
    CodeActionResponse,
    TextEdit,
    WorkspaceEdit,
)
from splints.types.server import State


@method(CodeActionRequest, CodeActionResponse)
def code_action_request(message: CodeActionRequest, state: State):
    code_actions: list[CodeAction] = []
    for diagnostic in message.params.context.diagnostics:
        if diagnostic.data is None:
            continue
        rule = state.lint_rules[diagnostic.data.rule_id]
        text = diagnostic.data.text
        for option in rule.replacement_options:
            imports = [
                TextEdit(
                    range=Range(
                        start=Position(line=0, character=0),
                        end=Position(line=0, character=0),
                    ),
                    newText=line + "\n",
                )
                for line in option.imports
            ]
            replaced_text = re.sub(option.pattern, option.replacement, text)
            code_actions.append(
                CodeAction(
                    title=option.description,
                    kind="quickfix",
                    diagnostics=[],
                    edit=WorkspaceEdit(
                        changes={
                            message.params.textDocument.uri: [
                                TextEdit(range=diagnostic.range, newText=replaced_text),
                                *imports,
                            ]
                        }
                    ),
                )
            )
    return CodeActionResponse(id=message.id, result=code_actions)
