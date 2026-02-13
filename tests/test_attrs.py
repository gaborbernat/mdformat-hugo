from __future__ import annotations

from textwrap import dedent

import mdformat
import pytest


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("## Heading {.class}\n", id="with_class"),
        pytest.param("## Heading {#custom-id}\n", id="with_id"),
        pytest.param("## Heading {.c1 .c2 .c3}\n", id="multiple_classes"),
        pytest.param("## Heading {#id .c1 .c2}\n", id="id_and_classes"),
        pytest.param("## Heading {data-foo=bar}\n", id="custom_attrs"),
        pytest.param('## Heading {data-foo="bar baz"}\n', id="quoted_attr_value"),
        pytest.param("## Heading {#id .class key=value}\n", id="mixed_attrs"),
    ],
)
def test_heading_attrs(text: str) -> None:
    outcome = mdformat.text(text, extensions=["hugo"])
    assert outcome == text


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("![alt](url){width=300}\n", id="with_attrs"),
        pytest.param("![alt](url){.img-fluid}\n", id="with_class"),
    ],
)
def test_image_attrs(text: str) -> None:
    outcome = mdformat.text(text, extensions=["hugo"])
    assert outcome == text


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            """\
        ```python {linenos=table}
        code
        ```
        """,
            id="with_attrs",
        ),
        pytest.param(
            """\
        ```python {.highlight}
        code
        ```
        """,
            id="with_class",
        ),
        pytest.param(
            """\
        ```python {#mycode}
        code
        ```
        """,
            id="with_id",
        ),
        pytest.param(
            """\
        ```python {#mycode .highlight}
        code
        ```
        """,
            id="id_and_class",
        ),
    ],
)
def test_fence_attrs(text: str) -> None:
    outcome = mdformat.text(dedent(text), extensions=["hugo"])
    assert outcome == dedent(text)


def test_attrs_without_element() -> None:
    start = "{.class}\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    assert outcome == start


def test_multiple_elements_with_attrs() -> None:
    start = """\
        ## Heading 1 {.h1}

        ## Heading 2 {.h2}
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    assert outcome == dedent(start)


def test_attrs_sorted_classes() -> None:
    start = "## Heading {.zebra .apple .middle}\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading {.apple .middle .zebra}\n"
    assert outcome == expected


def test_attrs_sorted_custom_attrs() -> None:
    start = "## Heading {zebra=1 apple=2 middle=3}\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading {apple=2 middle=3 zebra=1}\n"
    assert outcome == expected


def test_attrs_id_classes_custom_sorted() -> None:
    start = "## Heading {.zebra #myid zebra=1 .apple alpha=2}\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading {#myid .apple .zebra alpha=2 zebra=1}\n"
    assert outcome == expected
