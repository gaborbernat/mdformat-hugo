from __future__ import annotations

from textwrap import dedent

import mdformat
import pytest


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("{{< ref page.md >}}\n", "{{< ref page.md >}}\n", id="simple"),
        pytest.param('{{< ref "page.md" >}}\n', '{{< ref "page.md" >}}\n', id="with_quotes"),
        pytest.param("{{% note %}}\n", "{{% note %}}\n", id="percent_style"),
        pytest.param(
            '{{< figure src="image.jpg" title="My Image" >}}\n',
            '{{< figure src="image.jpg" title="My Image" >}}\n',
            id="with_parameters",
        ),
        pytest.param("{{<  ref   page.md  >}}\n", "{{< ref page.md >}}\n", id="normalizes_whitespace"),
    ],
)
def test_shortcode_preservation(text: str, expected: str) -> None:
    outcome = mdformat.text(text, extensions=["hugo"])
    assert outcome == expected


def test_shortcode_in_paragraph() -> None:
    start = """\
        Some text {{< ref page.md >}} more text
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        Some text {{< ref page.md >}} more text
        """
    assert outcome == dedent(expected)


def test_multiple_shortcodes() -> None:
    start = """\
        {{< figure src="1.jpg" >}}

        {{< figure src="2.jpg" >}}
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        {{< figure src="1.jpg" >}}

        {{< figure src="2.jpg" >}}
        """
    assert outcome == dedent(expected)
