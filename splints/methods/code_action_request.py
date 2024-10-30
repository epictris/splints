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
    document_lines = state.text_documents[
        message.params.textDocument.uri
    ].document.text.splitlines()
    for diagnostic in message.params.context.diagnostics:
        if diagnostic.data is None:
            continue
        rule = state.lint_rules[diagnostic.data.rule_id]

        diagnostic_lines = document_lines[
            diagnostic.range.start.line : diagnostic.range.end.line + 1
        ]
        text = "\n".join(diagnostic_lines)

        for option in rule.replacement_options:
            text_to_replace = re.search(option.pattern, text)
            if text_to_replace is None:
                continue
            replacement_start_index = text_to_replace.start()
            replacement_end_index = len(text_to_replace.group(0).splitlines()[-1])

            replaced_text = re.sub(
                option.pattern, option.replacement, text, re.MULTILINE
            )

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
            code_actions.append(
                CodeAction(
                    title=option.description,
                    kind="quickfix",
                    diagnostics=[],
                    edit=WorkspaceEdit(
                        changes={
                            message.params.textDocument.uri: [
                                TextEdit(
                                    range=Range(
                                        start=Position(
                                            line=diagnostic.range.start.line,
                                            character=replacement_start_index,
                                        ),
                                        end=Position(
                                            line=diagnostic.range.end.line,
                                            character=replacement_end_index,
                                        ),
                                    ),
                                    newText=replaced_text,
                                ),
                                *imports,
                            ]
                        }
                    ),
                )
            )
    return CodeActionResponse(id=message.id, result=code_actions)
