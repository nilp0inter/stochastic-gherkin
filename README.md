# Stochastic Gherkin

A superset of the [Gherkin](https://github.com/cucumber/gherkin) language for describing stochastic (probabilistic) behavior in BDD scenarios.

Stochastic Gherkin extends standard Gherkin with two new keywords -- `Stochastic Feature` and `Stochastic Scenario` -- and the ability to embed standard Gherkin scenarios directly inside a step, using indentation.

## Quick Start

```python
from gherkin import StochasticParser

parser = StochasticParser()
result = parser.parse("""\
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
```

The `When` step above contains an **embedded behavior** block: a set of standard Gherkin scenarios (with an optional Background) indented deeper than the step. The parser captures this block, delegates to the standard Gherkin parser, and attaches the result to the step's AST node as `embeddedBehavior`.

## How It Works

### New Keywords

| Keyword | Purpose |
|---|---|
| `Stochastic Feature:` | Top-level feature (replaces `Feature:`) |
| `Stochastic Scenario:` | A scenario whose steps may contain embedded behavior |

### Embedded Behavior

Any step inside a `Stochastic Scenario` can have an indented block of standard Gherkin beneath it. The block is delimited by indentation: lines indented deeper than the step are captured as embedded behavior; a line at the same indent or shallower ends the block.

The embedded block can contain:

- A `Background:` section
- One or more `Scenario:` or `Scenario Outline:` sections (with `Examples:`)
- Tags on any of the above

### AST Output

The parser produces a JSON-serializable AST. Steps with embedded behavior include an `embeddedBehavior` key:

```json
{
  "embeddedBehavior": {
    "location": {"line": 6, "column": 9},
    "background": {
      "keyword": "Background",
      "steps": [{"keyword": "Given ", "text": "a bet of 10 on red"}]
    },
    "scenarios": [
      {"keyword": "Scenario", "name": "Ball lands on red", "steps": [...]},
      {"keyword": "Scenario", "name": "Ball lands on black", "steps": [...]}
    ]
  }
}
```

Line numbers in the embedded AST refer back to the original source file.

## Architecture

Stochastic Gherkin uses the same toolchain as standard Gherkin:

```
stochastic.berp  ──►  berp + gherkin-python.razor  ──►  stochastic_parser_base.py (generated)
                                                                    │
                                                          StochasticParser (subclass)
                                                                    │
                                              ┌─────────────────────┼─────────────────────┐
                                              │                     │                     │
                                    StochasticTokenMatcher    StochasticAstBuilder    Post-processing
                                    (indentation-aware)       (stochastic rules)     (delegates to standard Parser)
```

- **`stochastic.berp`**: A minimal Berp grammar for the outer stochastic DSL
- **`gherkin-python.razor`**: The same Razor template used by the standard parser (reused, not forked)
- **`StochasticTokenMatcher`**: Extends `TokenMatcher` with indentation-aware matching for `EmbeddedBehaviorLine`
- **`StochasticAstBuilder`**: Extends `AstBuilder` with transform rules for stochastic node types
- **`StochasticParser`**: Hooks into the generated parser to track step indentation, then post-processes the AST to re-parse embedded blocks with the standard `Parser`

The standard Gherkin parser, scanner, and all other components remain **completely untouched**.

## Standard Gherkin

The standard Gherkin `Parser` and `Compiler` are still available and work exactly as in upstream:

```python
from gherkin import Parser, Compiler

doc = Parser().parse("Feature: ...")
doc["uri"] = "my.feature"
pickles = Compiler().compile(doc)
```

## Installation

```bash
pip install gherkin-official
```

## Development

```bash
# Run tests
cd python && uv run pytest

# Regenerate parsers (requires berp)
cd python && make generate

# Run standard Gherkin acceptance tests
cd python && make acceptance
```
