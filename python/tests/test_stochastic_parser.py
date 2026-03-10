from __future__ import annotations

import textwrap

from gherkin.stochastic_parser import StochasticParser


ROULETTE_EXAMPLE = textwrap.dedent("""\
    Stochastic Feature: Roulette

      Stochastic Scenario: Betting on red
        Given a roulette table
        When the ball lands on a pocket
            Background:
              Given a bet of 10 on red

            Scenario: Ball lands on red
              Then the player wins 20

            Scenario: Ball lands on black
              Then the player loses 10
        Then the bets are settled
""")


class TestBasicParse:
    def test_parses_stochastic_feature(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        feature = result["stochasticFeature"]
        assert feature["name"] == "Roulette"
        assert feature["keyword"] == "Stochastic Feature"

    def test_parses_stochastic_scenario(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        feature = result["stochasticFeature"]
        children = feature["children"]
        assert len(children) == 1
        scenario = children[0]["stochasticScenario"]
        assert scenario["name"] == "Betting on red"
        assert scenario["keyword"] == "Stochastic Scenario"

    def test_parses_steps(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        steps = scenario["steps"]
        assert len(steps) == 3
        assert steps[0]["text"] == "a roulette table"
        assert steps[0]["keyword"] == "Given "
        assert steps[1]["text"] == "the ball lands on a pocket"
        assert steps[1]["keyword"] == "When "
        assert steps[2]["text"] == "the bets are settled"
        assert steps[2]["keyword"] == "Then "


class TestEmbeddedBehavior:
    def test_when_step_has_embedded_behavior(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        when_step = scenario["steps"][1]
        assert "embeddedBehavior" in when_step

    def test_embedded_has_background(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        embedded = scenario["steps"][1]["embeddedBehavior"]
        assert "background" in embedded
        bg = embedded["background"]
        assert len(bg["steps"]) == 1
        assert bg["steps"][0]["text"] == "a bet of 10 on red"

    def test_embedded_has_scenarios(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        embedded = scenario["steps"][1]["embeddedBehavior"]
        scenarios = embedded["scenarios"]
        assert len(scenarios) == 2
        assert scenarios[0]["name"] == "Ball lands on red"
        assert scenarios[1]["name"] == "Ball lands on black"

    def test_embedded_scenario_steps(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        embedded = scenario["steps"][1]["embeddedBehavior"]
        sc1 = embedded["scenarios"][0]
        assert len(sc1["steps"]) == 1
        assert sc1["steps"][0]["text"] == "the player wins 20"

    def test_given_step_has_no_embedded(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        given_step = scenario["steps"][0]
        assert "embeddedBehavior" not in given_step

    def test_then_step_has_no_embedded(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        then_step = scenario["steps"][2]
        assert "embeddedBehavior" not in then_step


class TestLineNumbers:
    def test_background_line_number(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        embedded = scenario["steps"][1]["embeddedBehavior"]
        bg = embedded["background"]
        assert bg["location"]["line"] == 6

    def test_embedded_scenario_line_numbers(self) -> None:
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        embedded = scenario["steps"][1]["embeddedBehavior"]
        assert embedded["scenarios"][0]["location"]["line"] == 9
        assert embedded["scenarios"][1]["location"]["line"] == 12


class TestMultipleScenarios:
    def test_multiple_stochastic_scenarios(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: Multi

              Stochastic Scenario: First
                Given something
                When action
                    Scenario: Inner 1
                      Then result 1

              Stochastic Scenario: Second
                Given another thing
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        feature = result["stochasticFeature"]
        assert len(feature["children"]) == 2
        assert feature["children"][0]["stochasticScenario"]["name"] == "First"
        assert feature["children"][1]["stochasticScenario"]["name"] == "Second"


class TestStepArguments:
    def test_step_with_data_table(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: Tables

              Stochastic Scenario: With table
                Given a table:
                  | col1 | col2 |
                  | a    | b    |
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        step = scenario["steps"][0]
        assert "dataTable" in step
        assert len(step["dataTable"]["rows"]) == 2

    def test_step_with_doc_string(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: DocStrings

              Stochastic Scenario: With docstring
                Given some text:
                  \"\"\"
                  Hello world
                  \"\"\"
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        step = scenario["steps"][0]
        assert "docString" in step
        assert step["docString"]["content"] == "Hello world"


class TestTags:
    def test_tags_on_stochastic_feature(self) -> None:
        source = textwrap.dedent("""\
            @wip
            Stochastic Feature: Tagged

              Stochastic Scenario: First
                Given something
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        feature = result["stochasticFeature"]
        assert len(feature["tags"]) == 1
        assert feature["tags"][0]["name"] == "@wip"

    def test_tags_on_stochastic_scenario(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: F

              @smoke
              Stochastic Scenario: Tagged scenario
                Given something
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        assert len(scenario["tags"]) == 1
        assert scenario["tags"][0]["name"] == "@smoke"


class TestEmbeddedTermination:
    def test_embedded_terminated_by_next_outer_step(self) -> None:
        """Embedded behavior ends when a step at the outer indent level appears."""
        parser = StochasticParser()
        result = parser.parse(ROULETTE_EXAMPLE)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        assert len(scenario["steps"]) == 3
        assert scenario["steps"][2]["keyword"] == "Then "

    def test_embedded_terminated_by_eof(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: EOF

              Stochastic Scenario: Ends at EOF
                When something happens
                    Scenario: Inner
                      Then inner result
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        assert len(scenario["steps"]) == 1
        embedded = scenario["steps"][0]["embeddedBehavior"]
        assert len(embedded["scenarios"]) == 1

    def test_embedded_terminated_by_next_scenario(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: Next Scenario

              Stochastic Scenario: First
                When something happens
                    Scenario: Inner
                      Then inner result

              Stochastic Scenario: Second
                Given another thing
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        feature = result["stochasticFeature"]
        assert len(feature["children"]) == 2
        first_scenario = feature["children"][0]["stochasticScenario"]
        assert len(first_scenario["steps"]) == 1
        assert "embeddedBehavior" in first_scenario["steps"][0]


class TestParserReuse:
    def test_parse_multiple_times(self) -> None:
        parser = StochasticParser()
        result1 = parser.parse(ROULETTE_EXAMPLE)
        result2 = parser.parse(ROULETTE_EXAMPLE)
        assert result1["stochasticFeature"]["name"] == result2["stochasticFeature"]["name"]


class TestScenarioOutlineInEmbedded:
    def test_embedded_scenario_outline(self) -> None:
        source = textwrap.dedent("""\
            Stochastic Feature: Outlines

              Stochastic Scenario: With outline
                When something happens
                    Scenario Outline: Parameterized
                      Then the result is <result>

                      Examples:
                        | result |
                        | win    |
                        | lose   |
        """)
        parser = StochasticParser()
        result = parser.parse(source)
        scenario = result["stochasticFeature"]["children"][0]["stochasticScenario"]
        embedded = scenario["steps"][0]["embeddedBehavior"]
        assert len(embedded["scenarios"]) == 1
        sc = embedded["scenarios"][0]
        assert sc["keyword"] == "Scenario Outline"
        assert len(sc["examples"]) == 1
        assert len(sc["examples"][0]["tableBody"]) == 2
