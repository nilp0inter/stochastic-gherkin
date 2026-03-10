from __future__ import annotations

from gherkin.gherkin_line import GherkinLine
from gherkin.stochastic_token_matcher import StochasticTokenMatcher
from gherkin.token import Token


def _make_token(text: str, line_number: int = 1) -> Token:
    line = GherkinLine(text, line_number)
    return Token(line, {"line": line_number})


class TestMatchStochasticFeatureLine:
    def test_matches_stochastic_feature(self) -> None:
        matcher = StochasticTokenMatcher()
        token = _make_token("Stochastic Feature: My feature")
        assert matcher.match_StochasticFeatureLine(token)
        assert token.matched_type == "StochasticFeatureLine"
        assert token.matched_text == "My feature"
        assert token.matched_keyword == "Stochastic Feature"

    def test_does_not_match_regular_feature(self) -> None:
        matcher = StochasticTokenMatcher()
        token = _make_token("Feature: My feature")
        assert not matcher.match_StochasticFeatureLine(token)


class TestMatchStochasticScenarioLine:
    def test_matches_stochastic_scenario(self) -> None:
        matcher = StochasticTokenMatcher()
        token = _make_token("Stochastic Scenario: My scenario")
        assert matcher.match_StochasticScenarioLine(token)
        assert token.matched_type == "StochasticScenarioLine"
        assert token.matched_text == "My scenario"

    def test_does_not_match_regular_scenario(self) -> None:
        matcher = StochasticTokenMatcher()
        token = _make_token("Scenario: My scenario")
        assert not matcher.match_StochasticScenarioLine(token)


class TestMatchEmbeddedBehaviorLine:
    def test_no_match_without_step_indent(self) -> None:
        matcher = StochasticTokenMatcher()
        token = _make_token("    Feature: inner")
        assert not matcher.match_EmbeddedBehaviorLine(token)

    def test_matches_when_deeper_than_step(self) -> None:
        matcher = StochasticTokenMatcher()
        matcher._stochastic_step_indent = 4
        token = _make_token("        Feature: inner")
        assert matcher.match_EmbeddedBehaviorLine(token)
        assert token.matched_type == "EmbeddedBehaviorLine"

    def test_no_match_when_same_indent(self) -> None:
        matcher = StochasticTokenMatcher()
        matcher._stochastic_step_indent = 4
        token = _make_token("    Given something")
        assert not matcher.match_EmbeddedBehaviorLine(token)

    def test_no_match_when_shallower(self) -> None:
        matcher = StochasticTokenMatcher()
        matcher._stochastic_step_indent = 4
        token = _make_token("  Given something")
        assert not matcher.match_EmbeddedBehaviorLine(token)

    def test_no_match_on_empty_line(self) -> None:
        matcher = StochasticTokenMatcher()
        matcher._stochastic_step_indent = 4
        token = _make_token("")
        assert not matcher.match_EmbeddedBehaviorLine(token)

    def test_no_match_on_comment_line(self) -> None:
        matcher = StochasticTokenMatcher()
        matcher._stochastic_step_indent = 4
        token = _make_token("        # a comment")
        assert not matcher.match_EmbeddedBehaviorLine(token)

    def test_reset_clears_step_indent(self) -> None:
        matcher = StochasticTokenMatcher()
        matcher._stochastic_step_indent = 4
        matcher.reset()
        assert matcher._stochastic_step_indent is None
