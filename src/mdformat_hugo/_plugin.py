"""Mdformat plugin interface for Hugo markdown."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Mapping

    from markdown_it import MarkdownIt
    from mdformat.renderer.typing import Render

from ._mdit_plugins.shortcodes import shortcode_plugin
from ._renderer import render_fence, render_heading, render_hugo_shortcode, render_image

CHANGES_AST: Final = True
RENDERERS: Final[Mapping[str, Render]] = {
    "hugo_shortcode": render_hugo_shortcode,
    "heading": render_heading,
    "image": render_image,
    "fence": render_fence,
}


def update_mdit(mdit: MarkdownIt) -> None:
    """Add Hugo-specific markdown-it-py plugins."""
    mdit.use(shortcode_plugin)


__all__ = [
    "CHANGES_AST",
    "RENDERERS",
    "update_mdit",
]
