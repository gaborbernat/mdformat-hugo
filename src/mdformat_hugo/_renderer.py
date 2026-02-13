"""Renderers for Hugo markdown elements."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from mdformat.renderer import RenderContext, RenderTreeNode

FENCE_ATTRS_PATTERN: Final = re.compile(r"^(\S+)\s+\{([^}]+)\}$")
INLINE_ATTRS_PATTERN: Final = re.compile(r"^(.*?)\s*\{([^}]+)\}\s*$")
ATTR_PATTERN: Final = re.compile(r'\.([^\s{}=]+)|#([^\s{}=]+)|([^\s{}=]+)=(?:"([^"]*)"|([^\s{}]+))')


def render_hugo_shortcode(node: RenderTreeNode, _context: RenderContext) -> str:
    """Render Hugo shortcode with normalized formatting."""
    content = " ".join(node.content.split())
    is_percent = node.markup == "{{%"
    open_delim, close_delim = ("{{%", "%}}") if is_percent else ("{{<", ">}}")
    return f"{open_delim} {content} {close_delim}"


def render_image(node: RenderTreeNode, _context: RenderContext) -> str:
    """Render image with optional title attribute."""
    src, alt, title = node.attrs.get("src", ""), node.content, node.attrs.get("title", "")
    return f'![{alt}]({src} "{title}")' if title else f"![{alt}]({src})"


def render_heading(node: RenderTreeNode, context: RenderContext) -> str:
    """Render heading with optional attributes."""
    markup = "#" * int(node.tag[1])
    children_text = node.children[0].render(context) if node.children else ""

    if match := INLINE_ATTRS_PATTERN.match(children_text):
        text_part = match.group(1).strip()
        attrs = _parse_attrs_from_string(match.group(2))
        attrs_str = f" {_format_attrs(attrs)}"
        return f"{markup} {text_part}{attrs_str}"

    return f"{markup} {children_text}"


def render_fence(node: RenderTreeNode, _context: RenderContext) -> str:
    """Render code fence with optional attributes from info string."""
    code_block = node.content
    fence_char = "`"
    fence_len = max(3, _longest_consecutive_sequence(code_block, fence_char) + 1)
    fence = fence_char * fence_len

    info_str = node.info or ""

    if match := FENCE_ATTRS_PATTERN.match(info_str):
        lang = match.group(1)
        attrs = _parse_attrs_from_string(match.group(2))
        info_str = f"{lang} {_format_attrs(attrs)}"

    return f"{fence}{info_str}\n{code_block}{fence}"


def _format_attrs(attrs: dict[str, str]) -> str:
    """Format attributes dictionary with consistent ordering and sorted elements."""
    parts = (
        ([f"#{attrs['id']}"] if "id" in attrs else [])
        + [f".{c}" for c in sorted(attrs.get("class", "").split()) if c]
        + [
            f'{k}="{v}"' if " " in v or "=" in v else f"{k}={v}"
            for k, v in sorted(attrs.items())
            if k not in {"id", "class"}
        ]
    )
    return f"{{{' '.join(parts)}}}"


def _parse_attrs_from_string(attr_str: str) -> dict[str, str]:
    """Parse attribute string into dictionary, preserving quoted values."""
    attrs: dict[str, str] = {}
    for match in ATTR_PATTERN.finditer(attr_str):
        if class_name := match.group(1):
            attrs["class"] = f"{attrs.get('class', '')} {class_name}".strip()
        elif id_value := match.group(2):
            attrs["id"] = id_value
        else:
            key = match.group(3)
            value = match.group(4) if match.group(4) is not None else match.group(5)
            attrs[key] = value
    return attrs


def _longest_consecutive_sequence(text: str, char: str) -> int:
    """Find longest consecutive sequence of char in text."""
    longest = current = 0
    for c in text:
        current = current + 1 if c == char else 0
        longest = max(longest, current)
    return longest


__all__ = [
    "render_fence",
    "render_heading",
    "render_hugo_shortcode",
    "render_image",
]
