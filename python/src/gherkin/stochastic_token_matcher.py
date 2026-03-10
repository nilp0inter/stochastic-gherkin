from __future__ import annotations

from .token import Token
from .token_matcher import TokenMatcher


class StochasticTokenMatcher(TokenMatcher):
    _stochastic_step_indent: int | None

    def __init__(self, dialect_name: str = "en") -> None:
        super().__init__(dialect_name)
        self._stochastic_step_indent = None

    def reset(self) -> None:
        super().reset()
        self._stochastic_step_indent = None

    def match_StochasticFeatureLine(self, token: Token) -> bool:
        return self._match_title_line(
            token,
            "StochasticFeatureLine",
            self.dialect.stochastic_feature_keywords,
        )

    def match_StochasticScenarioLine(self, token: Token) -> bool:
        return self._match_title_line(
            token,
            "StochasticScenarioLine",
            self.dialect.stochastic_scenario_keywords,
        )

    def match_EmbeddedBehaviorLine(self, token: Token) -> bool:
        if self._stochastic_step_indent is None:
            return False
        if token.line.is_empty():
            return False
        if token.line._trimmed_line_text.startswith("#"):
            return False
        if token.line.indent <= self._stochastic_step_indent:
            return False
        self._set_token_matched(
            token,
            "EmbeddedBehaviorLine",
            text=token.line._line_text,
        )
        return True
