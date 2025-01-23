from splints.decorators import method
import re
from splints.types.linting import PatternScope
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

        if rule.replacement_options is None:
            continue

        diagnostic_lines = document_lines[
            diagnostic.range.start.line : diagnostic.range.end.line + 1
        ]

        matched_text = "\n".join(diagnostic_lines)

        for option in rule.replacement_options:
            if option.scope == PatternScope.CHARACTERS:
                post_scope_character_count = (
                    len(diagnostic_lines[-1]) - diagnostic.range.end.character
                )
                pre_scope_character_count = diagnostic.range.start.character
                text_to_replace = re.search(
                    option.pattern,
                    matched_text[
                        pre_scope_character_count : len(matched_text)
                        - post_scope_character_count
                    ],
                )
            else:
                pre_scope_character_count = 0
                text_to_replace = re.search(option.pattern, matched_text)

            if text_to_replace is None:
                continue


            replaced_lines = text_to_replace.group().splitlines()
            if len(replaced_lines) == 0:
                continue

            lines_before_match = matched_text[
                : text_to_replace.start()
            ].splitlines() or [""]

            edit_start_line = diagnostic.range.start.line + len(lines_before_match) - 1
            edit_end_line = edit_start_line + len(replaced_lines) - 1

            edit_start_character = pre_scope_character_count + len(lines_before_match[-1])
            edit_end_character = len(replaced_lines[-1]) + (edit_start_character if len(replaced_lines) == 1 else 0)

            replaced_text = re.sub(
                option.pattern,
                option.replacement,
                text_to_replace.group(),
                1,
                re.MULTILINE,
            )

            imports = (
                [
                    TextEdit(
                        range=Range(
                            start=Position(line=0, character=0),
                            end=Position(line=0, character=0),
                        ),
                        newText=line + "\n",
                    )
                    for line in option.imports
                ]
                if option.imports is not None
                else []
            )

            code_actions.append(
                CodeAction(
                    title=option.description or f"Replace with: {replaced_text}",
                    kind="quickfix",
                    diagnostics=[],
                    edit=WorkspaceEdit(
                        changes={
                            message.params.textDocument.uri: [
                                TextEdit(
                                    range=Range(
                                        start=Position(
                                            line=edit_start_line,
                                            character=edit_start_character,
                                        ),
                                        end=Position(
                                            line=edit_end_line,
                                            character=edit_end_character,
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
