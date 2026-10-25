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
tox -e 3.15,3.14,3.13,3.12,3.11
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

This runs the `ty` type checker.

## Code Style

- Use Python 3.11+ features (walrus operators, `TYPE_CHECKING` blocks)
- Follow existing code patterns
- All code must pass `ruff` strict linting
- All code must pass `ty` type checking
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

## Release notes

Add a `changelog.d/+short-name.<type>.md` fragment when a pull request changes what package users can use or observe.
Use one fragment per user-facing change; the name can describe the change before a pull request number exists. The
release workflow links each fragment to its merged squash pull request.

| Type          | Changelog section | Use for                                                    |
| ------------- | ----------------- | ---------------------------------------------------------- |
| `feature`     | Added             | New capabilities and Python support additions or removals  |
| `change`      | Changes           | Changed behavior that remains available                    |
| `bugfix`      | Fixed             | Corrected behavior                                         |
| `doc`         | Documentation     | Documentation changes users need to know about             |
| `breaking`    | Breaking changes  | Changes that require users to update code or configuration |
| `security`    | Security          | Security fixes users need to act on                        |
| `performance` | Performance       | User-visible speed or resource improvements                |
| `deprecation` | Deprecated        | Supported behavior scheduled for removal                   |
| `removal`     | Removed           | Removed user-facing capabilities other than Python support |
| `packaging`   | Packaging         | Install, wheel, or distribution changes                    |

Use `skip news` for a pull request with no user-facing change. The label can be applied after the pull request opens. A
fragment still has to be valid when the label is present. Dependabot, pre-commit.ci, and repository automation receive
the label when their pull request has no fragment.

Do not write credits into a fragment. The changelog credits the authors and `Co-authored-by` co-authors of the commits
that added it, and the prepare workflow runs `release-creator contributors` to list first-time contributors.

## Pull Request Process

1. Create a feature branch from `main`
1. Make your changes
1. Add a changelog fragment for a user-facing change, or apply `skip news` for internal maintenance
1. Run `tox -e fix` to format and lint
1. Run `tox -e 3.15,3.14,3.13,3.12,3.11` to verify tests pass
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
