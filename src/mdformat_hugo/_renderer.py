"""Renderers for Hugo markdown elements."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from mdformat.renderer import RenderContext, RenderTreeNode

_FENCE_ATTRS_PATTERN: Final[re.Pattern[str]] = re.compile(r"^(\S+)\s+\{([^}]+)\}$")
_INLINE_ATTRS_PATTERN: Final[re.Pattern[str]] = re.compile(r"^(.*?)\s*\{([^}]+)\}\s*$")
_ATTR_PATTERN: Final[re.Pattern[str]] = re.compile(r'\.([^\s{}=]+)|#([^\s{}=]+)|([^\s{}=]+)=(?:"([^"]*)"|([^\s{}]+))')


def render_hugo_shortcode(node: RenderTreeNode, _context: RenderContext) -> str:
    # Render Hugo shortcode with normalized formatting.
    content = " ".join(node.content.split())
    open_delim, close_delim = ("{{%", "%}}") if (node.markup == "{{%") else ("{{<", ">}}")
    return f"{open_delim} {content} {close_delim}"


def render_image(node: RenderTreeNode, _context: RenderContext) -> str:
    # Render image with optional title attribute.
    src, alt, title = node.attrs.get("src", ""), node.content, node.attrs.get("title", "")
    return f'![{alt}]({src} "{title}")' if title else f"![{alt}]({src})"


def render_heading(node: RenderTreeNode, context: RenderContext) -> str:
    markup = "#" * int(node.tag[1])
    children_text = node.children[0].render(context) if node.children else ""

    if match := _INLINE_ATTRS_PATTERN.match(children_text):
        return f"{markup} {match.group(1).strip()}{f' {_format_attrs(_parse_attrs_from_string(match.group(2)))}'}"

    return f"{markup} {children_text}"


def _format_attrs(attrs: dict[str, str]) -> str:
    # Format attributes dictionary with consistent ordering and sorted elements.
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
    # Parse attribute string into dictionary, preserving quoted values.
    attrs: dict[str, str] = {}
    for match in _ATTR_PATTERN.finditer(attr_str):
        if class_name := match.group(1):
            attrs["class"] = f"{attrs.get('class', '')} {class_name}".strip()
        elif id_value := match.group(2):
            attrs["id"] = id_value
        else:
            attrs[match.group(3)] = match.group(4) if match.group(4) is not None else match.group(5)
    return attrs


def render_fence(node: RenderTreeNode, _context: RenderContext) -> str:
    # Render code fence with optional attributes from info string.
    code_block = node.content
    fence_char = "`"
    fence = fence_char * max(3, _longest_consecutive_sequence(code_block, fence_char) + 1)

    info_str = node.info or ""

    if match := _FENCE_ATTRS_PATTERN.match(info_str):
        info_str = f"{match.group(1)} {_format_attrs(_parse_attrs_from_string(match.group(2)))}"

    return f"{fence}{info_str}\n{code_block}{fence}"


def _longest_consecutive_sequence(text: str, char: str) -> int:
    # Find longest consecutive sequence of char in text.
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
