from __future__ import annotations

import textwrap
from typing import Any, cast

from .ast_builder import AstBuilder
from .parser import Parser
from .parser_types import GherkinDocument
from .stochastic_ast_builder import StochasticAstBuilder
from .stochastic_parser_base import ParserContext, StochasticParserBase
from .stochastic_token_matcher import StochasticTokenMatcher
from .stream.id_generator import IdGenerator
from .token import Token
from .token_matcher import TokenMatcher


class StochasticParser(StochasticParserBase):
    def __init__(self, ast_builder: StochasticAstBuilder | None = None) -> None:
        if ast_builder is None:
            ast_builder = StochasticAstBuilder()
        super().__init__(ast_builder)
        self._in_stochastic_step = False
        self._source_lines: list[str] = []
        self.id_generator = ast_builder.id_generator

    def parse(
        self,
        token_scanner_or_str: str,
        token_matcher: TokenMatcher | None = None,
    ) -> dict[str, Any]:
        if token_matcher is None:
            token_matcher = StochasticTokenMatcher()
        if isinstance(token_scanner_or_str, str):
            self._source_lines = token_scanner_or_str.split("\n")
        else:
            self._source_lines = []
        ast = super().parse(token_scanner_or_str, token_matcher)
        result = cast(dict[str, Any], ast)
        self._resolve_embedded_behaviors(result)
        return result

    def start_rule(self, context: ParserContext, rule_type: str) -> None:
        super().start_rule(context, rule_type)
        if rule_type == "StochasticStep":
            self._in_stochastic_step = True

    def end_rule(self, context: ParserContext, rule_type: str) -> None:
        if rule_type == "StochasticStep":
            self._in_stochastic_step = False
            context.token_matcher._stochastic_step_indent = None  # type: ignore[attr-defined]
        super().end_rule(context, rule_type)

    def build(self, context: ParserContext, token: Token) -> None:
        if self._in_stochastic_step and token.matched_type == "StepLine":
            context.token_matcher._stochastic_step_indent = token.matched_indent  # type: ignore[attr-defined]
        super().build(context, token)

    def _resolve_embedded_behaviors(self, ast: dict[str, Any]) -> None:
        feature = ast.get("stochasticFeature")
        if not feature:
            return

        for child in feature.get("children", []):
            scenario = child.get("stochasticScenario")
            if not scenario:
                continue
            for step in scenario.get("steps", []):
                embedded = step.get("embeddedBehavior")
                if not embedded:
                    continue
                resolved = self._resolve_single_embedded(embedded)
                step["embeddedBehavior"] = resolved

    def _resolve_single_embedded(
        self,
        placeholder: dict[str, Any],
    ) -> dict[str, Any]:
        start_line = placeholder["startLine"]
        end_line = placeholder["endLine"]

        # Extract the raw lines from source
        raw_lines = self._source_lines[start_line - 1 : end_line]
        content = "\n".join(raw_lines)
        dedented = textwrap.dedent(content)

        # Wrap in a Feature so the standard parser can parse it
        wrapped = "Feature: _embedded\n" + textwrap.indent(dedented, "  ")

        standard_parser = Parser(
            ast_builder=AstBuilder(IdGenerator()),
        )
        parsed: GherkinDocument = standard_parser.parse(wrapped)

        feature = parsed.get("feature")  # type: ignore[union-attr]
        if not feature:
            return {
                "location": placeholder["location"],
                "background": None,
                "scenarios": [],
            }

        background = None
        scenarios: list[dict[str, Any]] = []
        for child in feature.get("children", []):
            if "background" in child:
                bg = dict(child["background"])
                self._adjust_line_numbers(bg, start_line - 2)
                background = bg
            elif "scenario" in child:
                sc = dict(child["scenario"])
                self._adjust_line_numbers(sc, start_line - 2)
                scenarios.append(sc)

        result: dict[str, Any] = {
            "location": placeholder["location"],
            "scenarios": scenarios,
        }
        if background is not None:
            result["background"] = background

        return result

    def _adjust_line_numbers(self, node: dict[str, Any], offset: int) -> None:
        if "location" in node:
            node["location"] = dict(node["location"])
            node["location"]["line"] += offset

        for key in ("steps", "examples", "tags", "tableBody"):
            items = node.get(key)
            if items:
                for item in items:
                    if isinstance(item, dict):
                        self._adjust_line_numbers(item, offset)

        if "tableHeader" in node and node["tableHeader"]:
            node["tableHeader"] = dict(node["tableHeader"])
            self._adjust_line_numbers(node["tableHeader"], offset)

        if "dataTable" in node and node["dataTable"]:
            node["dataTable"] = dict(node["dataTable"])
            self._adjust_line_numbers(node["dataTable"], offset)
            rows = node["dataTable"].get("rows")
            if rows:
                for row in rows:
                    if isinstance(row, dict):
                        self._adjust_line_numbers(row, offset)

        if "docString" in node and node["docString"]:
            node["docString"] = dict(node["docString"])
            self._adjust_line_numbers(node["docString"], offset)

        if "cells" in node:
            for cell in node["cells"]:
                if isinstance(cell, dict) and "location" in cell:
                    cell["location"] = dict(cell["location"])
                    cell["location"]["line"] += offset

        if "background" in node and isinstance(node["background"], dict):
            self._adjust_line_numbers(node["background"], offset)

        for child_key in ("children", "scenarios"):
            children = node.get(child_key)
            if children and isinstance(children, list):
                for child in children:
                    if isinstance(child, dict):
                        self._adjust_line_numbers(child, offset)
