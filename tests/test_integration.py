from __future__ import annotations

from textwrap import dedent

import mdformat


def test_hugo_document_with_all_features() -> None:
    start = """\
        ## Heading {#intro .lead}

        Text with {{< ref "page.md" >}} shortcode.

        ![Image](img.jpg){.img-fluid width=600}

        ```python {.highlight}
        code
        ```
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        ## Heading {#intro .lead}

        Text with {{< ref "page.md" >}} shortcode.

        ![Image](img.jpg){.img-fluid width=600}

        ```python {.highlight}
        code
        ```
        """
    assert outcome == dedent(expected)


def test_paragraph_with_attrs() -> None:
    start = """\
        Regular paragraph.
        {.note}
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        Regular paragraph.
        {.note}
        """
    assert outcome == dedent(expected)


def test_shortcode_in_heading() -> None:
    start = "## Heading with {{< icon >}} shortcode\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading with {{< icon >}} shortcode\n"
    assert outcome == expected


def test_multiple_attrs_on_same_line() -> None:
    start = "## Heading {#id .class1 .class2 data-foo=bar}\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = "## Heading {#id .class1 .class2 data-foo=bar}\n"
    assert outcome == expected


def test_image_with_title_and_attrs() -> None:
    start = '![alt](url "title"){width=300}\n'
    outcome = mdformat.text(start, extensions=["hugo"])
    expected = '![alt](url "title"){width=300}\n'
    assert outcome == expected


def test_fence_without_lang() -> None:
    start = """\
        ```
        code
        ```
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        ```
        code
        ```
        """
    assert outcome == dedent(expected)


def test_alert_custom_title_preserved_by_default() -> None:
    start = "> [!TIP] Upgrade notes\n> Body.\n"
    outcome = mdformat.text(start, extensions=["hugo", "gfm_alerts"])
    assert outcome == "> [!TIP] Upgrade notes\n> Body.\n"


def test_alert_custom_title_preserved_regardless_of_extension_order() -> None:
    start = "> [!TIP] Upgrade notes\n> Body.\n"
    outcome = mdformat.text(start, extensions=["gfm_alerts", "hugo"])
    assert outcome == "> [!TIP] Upgrade notes\n> Body.\n"


def test_alert_custom_title_ignores_explicit_opt_out() -> None:
    start = "> [!TIP] Upgrade notes\n> Body.\n"
    outcome = mdformat.text(
        start,
        extensions=["hugo", "gfm_alerts"],
        options={"plugin": {"gfm_alerts": {"custom_title": False}}},
    )
    assert outcome == "> [!TIP] Upgrade notes\n> Body.\n"


def test_alert_without_gfm_alerts_extension_is_left_untouched() -> None:
    start = "> [!TIP] Upgrade notes\n> Body.\n"
    outcome = mdformat.text(start, extensions=["hugo"])
    assert outcome == start


def test_fence_with_backticks_in_code() -> None:
    start = """\
        ```python {.highlight}
        ```nested```
        ```
        """
    outcome = mdformat.text(dedent(start), extensions=["hugo"])
    expected = """\
        ````python {.highlight}
        ```nested```
        ````
        """
    assert outcome == dedent(expected)
