"""Hugo shortcode preservation parser plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_inline import StateInline


def shortcode_plugin(md: MarkdownIt) -> None:
    """Plugin to parse and format Hugo shortcodes uniformly."""
    md.inline.ruler.before("text", "hugo_shortcode", _shortcode_rule_wrapper)


def _shortcode_rule_wrapper(state: StateInline, silent: bool) -> bool:  # noqa: FBT001 - wrapper required by markdown-it-py API signature
    """Wrap shortcode rule to convert markdown-it-py boolean to named parameter."""
    return _shortcode_rule(state, should_skip_token_creation=silent)


def _shortcode_rule(state: StateInline, *, should_skip_token_creation: bool) -> bool:
    """Parse Hugo shortcodes: {{< shortcode >}} and {{% shortcode %}}."""
    pos = state.pos
    if pos + 3 >= state.posMax or state.src[pos : pos + 3] not in {"{{<", "{{%"}:
        return False

    is_percent = state.src[pos : pos + 3] == "{{%"
    close_marker = "%}}" if is_percent else ">}}"
    content_start = pos + 3

    pos = content_start
    while pos < state.posMax:
        if state.src[pos : pos + 3] == close_marker:
            if not should_skip_token_creation:  # pragma: no branch
                _create_shortcode_token(state, content_start, pos, is_percent=is_percent)
            state.pos = pos + 3
            return True
        pos += 1
    return False


def _create_shortcode_token(state: StateInline, content_start: int, pos: int, *, is_percent: bool) -> None:
    """Create a Hugo shortcode token."""
    token = state.push("hugo_shortcode", "", 0)
    token.content = state.src[content_start:pos].strip()
    token.markup = "{{%" if is_percent else "{{<"


__all__ = [
    "shortcode_plugin",
]
