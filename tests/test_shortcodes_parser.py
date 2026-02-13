from __future__ import annotations

from textwrap import dedent

import mdformat
import pytest


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("{{< ref page.md\n", id="incomplete"),
        pytest.param("{{% note\n", id="percent_incomplete"),
        pytest.param("{{< figure >}} and {{% note %}} together\n", id="mixed_types"),
        pytest.param("Text {{< ref page.md >}}\n", id="at_end_of_line"),
    ],
)
def test_shortcode_edge_cases(text: str) -> None:
    outcome = mdformat.text(text, extensions=["hugo"])
    assert outcome == text


def test_shortcode_too_short() -> None:
    start = "{{<\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "{{\\<\n"
    assert outcome == expected


def test_shortcode_not_multiline() -> None:
    start = """\
        Before {{< figure
        src="image.jpg"
        >}} after
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        Before {{< figure
        src="image.jpg"

        > }} after
        """
    assert outcome == dedent(expected)


def test_shortcode_in_list() -> None:
    start = """\
        - Item 1 {{< ref page1.md >}}
        - Item 2 {{< ref page2.md >}}
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    assert outcome == dedent(start)
