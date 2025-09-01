import re
import fnmatch
import urllib.parse
import os
import logging
from lsprotocol.types import (
    INITIALIZE,
    TEXT_DOCUMENT_CODE_ACTION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_OPEN,
    CodeAction,
    CodeActionKind,
    CodeActionOptions,
    CodeActionParams,
    Diagnostic,
    DiagnosticOptions,
    DiagnosticSeverity,
    DiagnosticTag,
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    InitializeParams,
    InitializeResult,
    Position,
    Range,
    ServerCapabilities,
    TextDocumentSyncKind,
    TextEdit,
    WorkspaceEdit,
)
from pygls.server import LanguageServer
from splints.rules import load_plugins
from splints.types.linting import LintRule, LintRuleId, Severity, Tag

CONVERT_SEVERITY = {
    Severity.ERROR: DiagnosticSeverity.Error,
    Severity.WARNING: DiagnosticSeverity.Warning,
    Severity.INFO: DiagnosticSeverity.Information,
    Severity.HINT: DiagnosticSeverity.Hint,
}

CONVERT_TAG = {
    Tag.DEPRECATED: DiagnosticTag.Deprecated,
    Tag.UNNECESSARY: DiagnosticTag.Unnecessary,
}


class Server(LanguageServer):
    def __init__(self, name: str, version: str):
        super().__init__(name, version)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logfile = os.getenv("SPLINTS_LOGFILE")
        if logfile is not None:
            logger.setLevel(logging.DEBUG)
            logger.addHandler(logging.FileHandler(logfile))
        self.logger = logger
        self.rules: dict[LintRuleId, LintRule] = load_plugins(self.logger)


server = Server("splints-server", "v0.0.3")


@server.feature(INITIALIZE)
async def initialize(params: InitializeParams) -> InitializeResult:
    server.logger.info(f"Initializing server with root: {params.root_uri}")
    return InitializeResult(
        capabilities=ServerCapabilities(
            diagnostic_provider=DiagnosticOptions(
                inter_file_dependencies=False, workspace_diagnostics=False
            ),
            text_document_sync=TextDocumentSyncKind.Full,
            code_action_provider=CodeActionOptions(
                code_action_kinds=[CodeActionKind.QuickFix]
            ),
        )
    )


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def text_document_did_change(params: DidChangeTextDocumentParams):
    await validate_document(params.text_document.uri)


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def text_document_did_open(params: DidOpenTextDocumentParams) -> None:
    await validate_document(params.text_document.uri)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
async def text_document_did_close(params: DidCloseTextDocumentParams):
    server.logger.info(f"Document closed: {params.text_document.uri}")
    server.publish_diagnostics(params.text_document.uri, [])


async def validate_document(uri: str) -> None:
    document = server.workspace.get_document(uri)
    document_text = "".join(document.lines)

    file_path = os.path.relpath(urllib.parse.urlparse(uri).path)
    applicable_rules = {
        rule_id: rule
        for rule_id, rule in server.rules.items()
        if any(fnmatch.fnmatch(file_path, path) for path in rule.include_globs)
        and not any(fnmatch.fnmatch(file_path, path) for path in rule.exclude_globs)
    }

    diagnostics: list[Diagnostic] = []

    for rule_id, rule in applicable_rules.items():
        diagnostics.extend(
            [
                Diagnostic(
                    source="splints",
                    severity=CONVERT_SEVERITY[rule.severity],
                    tags=[CONVERT_TAG[tag] for tag in rule.tags],
                    code=rule.code,
                    range=Range(
                        start=Position(
                            line=document_text.count("\n", 0, match.start()),
                            character=match.start()
                            - document_text.rfind("\n", 0, match.start())
                            - 1,
                        ),
                        end=Position(
                            line=document_text.count("\n", 0, match.end()),
                            character=match.end()
                            - document_text.rfind("\n", 0, match.end())
                            - 1,
                        ),
                    ),
                    message=rule.message,
                    data={"rule_id": rule_id, "text": match.group(0)},
                )
                for match in re.finditer(rule.pattern, document_text)
            ]
        )

    server.publish_diagnostics(uri, diagnostics)


@server.feature(TEXT_DOCUMENT_CODE_ACTION)
async def text_document_code_action(params: CodeActionParams) -> list[CodeAction]:
    document = server.workspace.get_document(params.text_document.uri)
    code_actions: list[CodeAction] = []
    for diagnostic in params.context.diagnostics:
        if diagnostic.source != "splints":
            continue
        if diagnostic.data is None:
            continue
        rule = server.rules[diagnostic.data.get("rule_id")]

        if rule.replacement_options is None:
            continue

        diagnostic_lines = [
            *document.lines[diagnostic.range.start.line : diagnostic.range.end.line + 1]
        ]

        diagnostic_lines[-1] = diagnostic_lines[-1][: diagnostic.range.end.character]
        diagnostic_lines[0] = diagnostic_lines[0][diagnostic.range.start.character :]

        matched_text = "\n".join(diagnostic_lines)

        for option in rule.replacement_options:
            replaced_text = re.sub(
                option.pattern,
                option.replacement,
                matched_text,
                1,
            )

            code_actions.append(
                CodeAction(
                    title=option.description or f"Replace with: {replaced_text}",
                    kind=CodeActionKind.QuickFix,
                    diagnostics=[diagnostic],
                    edit=WorkspaceEdit(
                        changes={
                            params.text_document.uri: [
                                TextEdit(
                                    range=diagnostic.range,
                                    new_text=replaced_text,
                                ),
                                *[
                                    TextEdit(
                                        range=Range(
                                            start=Position(line=0, character=0),
                                            end=Position(line=0, character=0),
                                        ),
                                        new_text=line + "\n",
                                    )
                                    for line in option.imports
                                ],
                            ]
                        }
                    ),
                )
            )
    return code_actions


def run():
    server.start_io()


if __name__ == "__main__":
    run()
