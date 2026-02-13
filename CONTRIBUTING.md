# Contributing to mdformat-hugo

Contributions are welcome and appreciated.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/gaborbernat/mdformat-hugo.git
cd mdformat-hugo
```

Create development environment:

```bash
tox -e dev
```

This creates a `.tox/dev` virtual environment with all dependencies installed in editable mode.

## Running Tests

Run all tests across Python versions:

```bash
tox -e 3.14,3.13,3.12,3.11
```

Run tests for a specific Python version:

```bash
tox -e 3.14
```

Run tests with coverage:

```bash
tox -e 3.14  # Coverage report shown in output
```

## Code Quality

Format and lint code:

```bash
tox -e fix
```

This runs:

- `ruff format` - Code formatting
- `ruff check --fix` - Linting with auto-fixes

Type check:

```bash
tox -e type
```

This runs `pyright` in strict mode.

## Code Style

- Use Python 3.11+ features (walrus operators, `TYPE_CHECKING` blocks)
- Follow existing code patterns
- All code must pass `ruff` strict linting
- All code must pass `pyright` strict type checking
- 100% test coverage required

## Writing Tests

Tests use snapshot-style testing with `textwrap.dedent`:

```python
from textwrap import dedent
import mdformat


def test_example() -> None:
    start = """\
        ## Heading {.class}
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        ## Heading {.class}
        """
    assert outcome == dedent(expected)
```

Test patterns:

- One test per behavior
- Clear test names describing what's being tested
- Use `dedent()` at usage point, not at variable assignment
- Test both valid input and edge cases

## Pull Request Process

1. Create a feature branch from `main`
1. Make your changes
1. Run `tox -e fix` to format and lint
1. Run `tox -e 3.14,3.13,3.12,3.11` to verify tests pass
1. Run `tox -e type` to verify type checking
1. Commit with a descriptive message following Commitizen format
1. Push and create a pull request

Pull request requirements:

- All tests must pass
- 100% code coverage maintained
- Type checking passes
- Linting passes
- Clear description of changes and motivation

## Project Structure

```
mdformat-hugo/
├── src/mdformat_hugo/
│   ├── __init__.py           # Entry point with version
│   ├── _plugin.py            # Plugin interface implementation
│   ├── _renderer.py          # Render functions
│   └── _mdit_plugins/        # Custom markdown-it-py plugins
│       ├── attrs.py          # Attribute parser (placeholder)
│       └── shortcodes.py     # Shortcode preservation
├── tests/                    # Test files
├── pyproject.toml           # Project configuration
└── tox.toml                 # Tox configuration
```

## Questions

For questions or discussions, open an issue on GitHub.
