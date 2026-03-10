from __future__ import annotations

from typing import Union, cast

from .ast_builder import AstBuilder
from .ast_node import AstNode
from .parser_types import (
    DataTable,
    DocString,
    Examples,
    Feature,
    GherkinDocument,
    Rule,
    Scenario,
    Step,
    TableRow,
)
from .stream.id_generator import IdGenerator
from .token import Token


class StochasticAstBuilder(AstBuilder):
    def __init__(self, id_generator: IdGenerator | None = None) -> None:
        super().__init__(id_generator)

    def get_result(self) -> object:
        return self.current_node.get_single("StochasticGherkinDocument")

    def transform_node(  # noqa: C901
        self,
        node: AstNode,
    ) -> (
        Step
        | DocString
        | DataTable
        | Scenario
        | Examples
        | list[TableRow]
        | str
        | None
        | Rule
        | Feature
        | GherkinDocument
        | AstNode
        | dict[str, object]
    ):
        if node.rule_type == "StochasticStep":
            step_line = node.get_token("StepLine")
            step_argument_type = "dummy_type"
            step_argument = None
            if node.get_single("DataTable"):
                step_argument_type = "dataTable"
                step_argument = node.get_single("DataTable")
            elif node.get_single("DocString"):
                step_argument_type = "docString"
                step_argument = node.get_single("DocString")
            elif node.get_single("EmbeddedBehavior"):
                step_argument_type = "embeddedBehavior"
                step_argument = node.get_single("EmbeddedBehavior")

            return self.reject_nones(
                {
                    "id": self.id_generator.get_next_id(),
                    "location": self.get_location(step_line),
                    "keyword": step_line.matched_keyword,
                    "keywordType": step_line.matched_keyword_type,
                    "text": step_line.matched_text,
                    step_argument_type: step_argument,
                },
            )

        if node.rule_type == "EmbeddedBehavior":
            tokens = node.get_tokens("EmbeddedBehaviorLine")
            start_line = tokens[0].location["line"]
            end_line = tokens[-1].location["line"]
            return {
                "location": self.get_location(tokens[0]),
                "startLine": start_line,
                "endLine": end_line,
            }

        if node.rule_type == "StochasticStepArg":
            return (
                node.get_single("DataTable")
                or node.get_single("DocString")
                or node.get_single("EmbeddedBehavior")
            )

        if node.rule_type == "StochasticScenarioDefinition":
            tags = self.get_tags(node)
            scenario_node = cast(AstNode, node.get_single("StochasticScenario"))
            scenario_line = scenario_node.get_token("StochasticScenarioLine")
            description = self.get_description(scenario_node)
            steps = cast(list[Step], scenario_node.get_items("StochasticStep"))

            return self.reject_nones(
                {
                    "id": self.id_generator.get_next_id(),
                    "tags": tags,
                    "location": self.get_location(scenario_line),
                    "keyword": scenario_line.matched_keyword,
                    "name": scenario_line.matched_text,
                    "description": description,
                    "steps": steps,
                },
            )

        if node.rule_type == "StochasticFeature":
            header = cast(
                Union[AstNode, None],
                node.get_single("StochasticFeatureHeader"),
            )
            if not header:
                return None

            tags = self.get_tags(header)
            feature_line = header.get_token("StochasticFeatureLine")
            if not feature_line:
                return None

            children = [
                {"stochasticScenario": i}
                for i in node.get_items("StochasticScenarioDefinition")
            ]
            description = self.get_description(header)
            language = feature_line.matched_gherkin_dialect

            return self.reject_nones(
                {
                    "tags": tags,
                    "location": self.get_location(feature_line),
                    "language": language,
                    "keyword": feature_line.matched_keyword,
                    "name": feature_line.matched_text,
                    "description": description,
                    "children": children,
                },
            )

        if node.rule_type == "StochasticGherkinDocument":
            feature = node.get_single("StochasticFeature")
            return self.reject_nones(
                {"stochasticFeature": feature, "comments": self.comments},
            )

        return super().transform_node(node)
