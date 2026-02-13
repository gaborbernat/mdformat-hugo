from __future__ import annotations

from textwrap import dedent

import mdformat
import pytest


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("{.class}\n\nContent\n", "{.class}\n\nContent\n", id="at_start_of_document"),
        pytest.param("## Heading\n\n{}\n", "## Heading\n\n{}\n", id="empty_attrs_block"),
        pytest.param("## Heading\n\n{invalid\n", "## Heading\n\n{invalid\n", id="invalid_syntax"),
        pytest.param(
            '## Heading {data-value="foo=bar"}\n', '## Heading {data-value="foo=bar"}\n', id="quoted_value_with_equals"
        ),
        pytest.param('## Heading {title="Hello World"}\n', '## Heading {title="Hello World"}\n', id="space_in_value"),
        pytest.param(
            "## Heading {.class1 .class2 .class3}\n", "## Heading {.class1 .class2 .class3}\n", id="class_accumulation"
        ),
        pytest.param("## Heading {#custom-id}\n", "## Heading {#custom-id}\n", id="id_only"),
        pytest.param("## Heading {.class #id}\n", "## Heading {#id .class}\n", id="mixed_order_formatted"),
    ],
)
def test_attrs_edge_cases(text: str, expected: str) -> None:
    outcome = mdformat.text(text, extensions=["hugo"])
    assert outcome == expected


def test_attrs_on_paragraph() -> None:
    start = """\
        Some paragraph text.
        {.note}

        More text.
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    assert outcome == dedent(start)


def test_attrs_with_trailing_whitespace() -> None:
    start = "## Heading {.class  }\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading {.class}\n"
    assert outcome == expected


def test_attrs_invalid_key_without_equals() -> None:
    start = "## Heading {invalidkey}\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading {}\n"
    assert outcome == expected
