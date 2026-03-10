# This file is generated. Do not edit! Edit gherkin-python.razor instead.
from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import TypeVar, cast

from .ast_builder import AstBuilder
from .errors import (
    CompositeParserException,
    ParserException,
    UnexpectedEOFException,
    UnexpectedTokenException,
)
from .parser_types import GherkinDocument
from .token import Token
from .token_matcher import TokenMatcher
from .token_scanner import TokenScanner

_T = TypeVar("_T")
_U = TypeVar("_U")
_V = TypeVar("_V")

RULE_TYPE = [
    "None",
    "_EOF",  # #EOF
    "_Empty",  # #Empty
    "_Comment",  # #Comment
    "_TagLine",  # #TagLine
    "_StochasticFeatureLine",  # #StochasticFeatureLine
    "_StochasticScenarioLine",  # #StochasticScenarioLine
    "_StepLine",  # #StepLine
    "_DocStringSeparator",  # #DocStringSeparator
    "_TableRow",  # #TableRow
    "_Language",  # #Language
    "_EmbeddedBehaviorLine",  # #EmbeddedBehaviorLine
    "_Other",  # #Other
    "StochasticGherkinDocument",  # StochasticGherkinDocument! := StochasticFeature?
    "StochasticFeature",  # StochasticFeature! := StochasticFeatureHeader StochasticScenarioDefinition*
    "StochasticFeatureHeader",  # StochasticFeatureHeader! := #Language? Tags? #StochasticFeatureLine DescriptionHelper
    "StochasticScenarioDefinition",  # StochasticScenarioDefinition! [#Empty|#Comment|#TagLine->#StochasticScenarioLine] := Tags? StochasticScenario
    "StochasticScenario",  # StochasticScenario! := #StochasticScenarioLine DescriptionHelper StochasticStep*
    "StochasticStep",  # StochasticStep! := #StepLine StochasticStepArg?
    "StochasticStepArg",  # StochasticStepArg := (DataTable | DocString | EmbeddedBehavior)
    "EmbeddedBehavior",  # EmbeddedBehavior! := #EmbeddedBehaviorLine+
    "DataTable",  # DataTable! := #TableRow+
    "DocString",  # DocString! := #DocStringSeparator #Other* #DocStringSeparator
    "Tags",  # Tags! := #TagLine+
    "DescriptionHelper",  # DescriptionHelper := #Empty* Description?
    "Description",  # Description! := (#Other | #Comment)+
]


class ParserContext:
    def __init__(
        self,
        token_scanner: TokenScanner,
        token_matcher: TokenMatcher,
        token_queue: deque[Token],
        errors: list[ParserException],
    ) -> None:
        self.token_scanner = token_scanner
        self.token_matcher = token_matcher
        self.token_queue = token_queue
        self.errors = errors


class StochasticParserBase:
    def __init__(self, ast_builder: AstBuilder | None = None) -> None:
        self.ast_builder = ast_builder if ast_builder is not None else AstBuilder()
        self.stop_at_first_error = False

    def parse(
        self,
        token_scanner_or_str: TokenScanner | str,
        token_matcher: TokenMatcher | None = None,
    ) -> GherkinDocument:
        token_scanner = (
            TokenScanner(token_scanner_or_str)
            if isinstance(token_scanner_or_str, str)
            else token_scanner_or_str
        )
        self.ast_builder.reset()
        if token_matcher is None:
            token_matcher = TokenMatcher()
        token_matcher.reset()
        context = ParserContext(token_scanner, token_matcher, deque(), [])

        self.start_rule(context, "StochasticGherkinDocument")
        state = 0
        token = None
        while True:
            token = self.read_token(context)
            state = self.match_token(state, token, context)
            if token.eof():
                break

        self.end_rule(context, "StochasticGherkinDocument")

        if context.errors:
            raise CompositeParserException(context.errors)

        return cast(GherkinDocument, self.get_result())

    def build(self, context: ParserContext, token: Token) -> None:
        self.handle_ast_error(context, token, self.ast_builder.build)

    def add_error(self, context: ParserContext, error: ParserException) -> None:
        if str(error) not in (str(e) for e in context.errors):
            context.errors.append(error)
            if len(context.errors) > 10:
                raise CompositeParserException(context.errors)

    def start_rule(self, context: ParserContext, rule_type: str) -> None:
        self.handle_ast_error(context, rule_type, self.ast_builder.start_rule)

    def end_rule(self, context: ParserContext, rule_type: str) -> None:
        self.handle_ast_error(context, rule_type, self.ast_builder.end_rule)

    def get_result(self) -> object:
        return self.ast_builder.get_result()

    def read_token(self, context: ParserContext) -> Token:
        if context.token_queue:
            return context.token_queue.popleft()
        return context.token_scanner.read()

    def match_EOF(self, context: ParserContext, token: Token) -> bool:
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_EOF,
        )

    def match_Empty(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_Empty,
        )

    def match_Comment(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_Comment,
        )

    def match_TagLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_TagLine,
        )

    def match_StochasticFeatureLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_StochasticFeatureLine,
        )

    def match_StochasticScenarioLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_StochasticScenarioLine,
        )

    def match_StepLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_StepLine,
        )

    def match_DocStringSeparator(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_DocStringSeparator,
        )

    def match_TableRow(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_TableRow,
        )

    def match_Language(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_Language,
        )

    def match_EmbeddedBehaviorLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_EmbeddedBehaviorLine,
        )

    def match_Other(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context,
            False,
            token,
            context.token_matcher.match_Other,
        )

    def match_token(self, state: int, token: Token, context: ParserContext) -> int:
        state_map: dict[int, Callable[[Token, ParserContext], int]] = {
            0: self.match_token_at_0,
            1: self.match_token_at_1,
            2: self.match_token_at_2,
            3: self.match_token_at_3,
            4: self.match_token_at_4,
            5: self.match_token_at_5,
            6: self.match_token_at_6,
            7: self.match_token_at_7,
            8: self.match_token_at_8,
            9: self.match_token_at_9,
            11: self.match_token_at_11,
            12: self.match_token_at_12,
            13: self.match_token_at_13,
        }

        if state not in state_map:
            raise RuntimeError(f"Unknown state: {state}")

        return state_map[state](token, context)

    # Start
    def match_token_at_0(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.build(context, token)
            return 10
        if self.match_Language(context, token):
            self.start_rule(context, "StochasticFeature")
            self.start_rule(context, "StochasticFeatureHeader")
            self.build(context, token)
            return 1
        if self.match_TagLine(context, token):
            self.start_rule(context, "StochasticFeature")
            self.start_rule(context, "StochasticFeatureHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 2
        if self.match_StochasticFeatureLine(context, token):
            self.start_rule(context, "StochasticFeature")
            self.start_rule(context, "StochasticFeatureHeader")
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.build(context, token)
            return 0
        if self.match_Empty(context, token):
            self.build(context, token)
            return 0

        state_comment = "State: 0 - Start"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Language",
            "#TagLine",
            "#StochasticFeatureLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 0

    # StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:0>#Language:0
    def match_token_at_1(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 2
        if self.match_StochasticFeatureLine(context, token):
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.build(context, token)
            return 1
        if self.match_Empty(context, token):
            self.build(context, token)
            return 1

        state_comment = "State: 1 - StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:0>#Language:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#StochasticFeatureLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 1

    # StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:1>Tags:0>#TagLine:0
    def match_token_at_2(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 2
        if self.match_StochasticFeatureLine(context, token):
            self.end_rule(context, "Tags")
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.build(context, token)
            return 2
        if self.match_Empty(context, token):
            self.build(context, token)
            return 2

        state_comment = "State: 2 - StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:1>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#StochasticFeatureLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 2

    # StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:2>#StochasticFeatureLine:0
    def match_token_at_3(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "StochasticFeatureHeader")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_Empty(context, token):
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 4
        if self.match_TagLine(context, token):
            self.end_rule(context, "StochasticFeatureHeader")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "StochasticFeatureHeader")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 4

        state_comment = "State: 3 - StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:2>#StochasticFeatureLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 3

    # StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:3>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_4(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "StochasticFeatureHeader")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_Comment(context, token):
            self.build(context, token)
            return 4
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "StochasticFeatureHeader")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "StochasticFeatureHeader")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Other(context, token):
            self.build(context, token)
            return 4

        state_comment = "State: 4 - StochasticGherkinDocument:0>StochasticFeature:0>StochasticFeatureHeader:3>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 4

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:0>Tags:0>#TagLine:0
    def match_token_at_5(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "Tags")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Comment(context, token):
            self.build(context, token)
            return 5
        if self.match_Empty(context, token):
            self.build(context, token)
            return 5

        state_comment = "State: 5 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:0>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#StochasticScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 5

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:0>#StochasticScenarioLine:0
    def match_token_at_6(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_Empty(context, token):
            self.build(context, token)
            return 6
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 7
        if self.match_StepLine(context, token):
            self.start_rule(context, "StochasticStep")
            self.build(context, token)
            return 8
        if self.match_TagLine(context, token):
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 7

        state_comment = "State: 6 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:0>#StochasticScenarioLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 6

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_7(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_Comment(context, token):
            self.build(context, token)
            return 7
        if self.match_StepLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "StochasticStep")
            self.build(context, token)
            return 8
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Other(context, token):
            self.build(context, token)
            return 7

        state_comment = "State: 7 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 7

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:0>#StepLine:0
    def match_token_at_8(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_TableRow(context, token):
            self.start_rule(context, "DataTable")
            self.build(context, token)
            return 9
        if self.match_DocStringSeparator(context, token):
            self.start_rule(context, "DocString")
            self.build(context, token)
            return 11
        if self.match_EmbeddedBehaviorLine(context, token):
            self.start_rule(context, "EmbeddedBehavior")
            self.build(context, token)
            return 13
        if self.match_StepLine(context, token):
            self.end_rule(context, "StochasticStep")
            self.start_rule(context, "StochasticStep")
            self.build(context, token)
            return 8
        if self.match_TagLine(context, token):
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Comment(context, token):
            self.build(context, token)
            return 8
        if self.match_Empty(context, token):
            self.build(context, token)
            return 8

        state_comment = "State: 8 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:0>#StepLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#DocStringSeparator",
            "#EmbeddedBehaviorLine",
            "#StepLine",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 8

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:0>DataTable:0>#TableRow:0
    def match_token_at_9(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 9
        if self.match_StepLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "StochasticStep")
            self.start_rule(context, "StochasticStep")
            self.build(context, token)
            return 8
        if self.match_TagLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Comment(context, token):
            self.build(context, token)
            return 9
        if self.match_Empty(context, token):
            self.build(context, token)
            return 9

        state_comment = "State: 9 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:0>DataTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#StepLine",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 9

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0
    def match_token_at_11(self, token: Token, context: ParserContext) -> int:
        if self.match_DocStringSeparator(context, token):
            self.build(context, token)
            return 12
        if self.match_Other(context, token):
            self.build(context, token)
            return 11

        state_comment = "State: 11 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#DocStringSeparator",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 11

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0
    def match_token_at_12(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_StepLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "StochasticStep")
            self.start_rule(context, "StochasticStep")
            self.build(context, token)
            return 8
        if self.match_TagLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Comment(context, token):
            self.build(context, token)
            return 12
        if self.match_Empty(context, token):
            self.build(context, token)
            return 12

        state_comment = "State: 12 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#StepLine",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 12

    # StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:2>EmbeddedBehavior:0>#EmbeddedBehaviorLine:0
    def match_token_at_13(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "EmbeddedBehavior")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.end_rule(context, "StochasticFeature")
            self.build(context, token)
            return 10
        if self.match_EmbeddedBehaviorLine(context, token):
            self.build(context, token)
            return 13
        if self.match_StepLine(context, token):
            self.end_rule(context, "EmbeddedBehavior")
            self.end_rule(context, "StochasticStep")
            self.start_rule(context, "StochasticStep")
            self.build(context, token)
            return 8
        if self.match_TagLine(context, token):
            self.end_rule(context, "EmbeddedBehavior")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 5
        if self.match_StochasticScenarioLine(context, token):
            self.end_rule(context, "EmbeddedBehavior")
            self.end_rule(context, "StochasticStep")
            self.end_rule(context, "StochasticScenario")
            self.end_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenarioDefinition")
            self.start_rule(context, "StochasticScenario")
            self.build(context, token)
            return 6
        if self.match_Comment(context, token):
            self.build(context, token)
            return 13
        if self.match_Empty(context, token):
            self.build(context, token)
            return 13

        state_comment = "State: 13 - StochasticGherkinDocument:0>StochasticFeature:1>StochasticScenarioDefinition:1>StochasticScenario:2>StochasticStep:1>StochasticStepArg:0>__alt0:2>EmbeddedBehavior:0>#EmbeddedBehaviorLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#EmbeddedBehaviorLine",
            "#StepLine",
            "#TagLine",
            "#StochasticScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 13

    def lookahead_0(self, context: ParserContext, currentToken: Token) -> bool:
        currentToken.detach()
        token = None
        queue = []
        match = False
        # Effectively do-while
        continue_lookahead = True
        while continue_lookahead:
            token = self.read_token(context)
            token.detach()
            queue.append(token)

            if self.match_StochasticScenarioLine(context, token):
                match = True
                break

            continue_lookahead = False

            if self.match_Empty(context, token):
                continue_lookahead = True
                continue
            if self.match_Comment(context, token):
                continue_lookahead = True
                continue
            if self.match_TagLine(context, token):
                continue_lookahead = True
                continue

        context.token_queue.extend(queue)

        return match

    # private

    def handle_ast_error(
        self,
        context: ParserContext,
        argument: _T,
        action: Callable[[_T], object],
    ) -> None:
        self.handle_external_error(context, True, argument, action)

    def handle_external_error(
        self,
        context: ParserContext,
        default_value: _U,
        argument: _T,
        action: Callable[[_T], _V],
    ) -> _V | _U:
        if self.stop_at_first_error:
            return action(argument)

        try:
            return action(argument)
        except CompositeParserException as e:
            for error in e.errors:
                self.add_error(context, error)
        except ParserException as e:
            self.add_error(context, e)
        return default_value
