from __future__ import annotations

from textwrap import dedent

import mdformat
import pytest


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("![alt](url)\n", id="image_without_title"),
        pytest.param("## \n", id="heading_empty_content"),
        pytest.param("![](url){.img}\n", id="image_empty_alt"),
    ],
)
def test_renderer_edge_cases(text: str) -> None:
    outcome = mdformat.text(text, extensions=["hugo"])
    assert outcome == text


def test_fence_backticks_preserved() -> None:
    start = """\
        ````python
        ```
        ````
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    assert outcome == dedent(start)


def test_fence_empty_info() -> None:
    start = """\
        ```
        code
        ```
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    assert outcome == dedent(start)
