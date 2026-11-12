"""Renderers for Hugo markdown elements."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from mdformat.renderer import RenderContext, RenderTreeNode

_FENCE_ATTRS_PATTERN: Final[re.Pattern[str]] = re.compile(r"^(?P<language>\S+)\s+\{(?P<attrs>[^}]+)\}$")
_INLINE_ATTRS_PATTERN: Final[re.Pattern[str]] = re.compile(r"^(?P<text>.*?)\s*\{(?P<attrs>[^}]+)\}\s*$")
_ATTR_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""
    \.(?P<class_name>[^\s{}=]+)  # class shorthand
    | \#(?P<id>[^\s{}=]+)  # ID shorthand
    | (?P<key>[^\s{}=]+)=(?:"(?P<quoted_value>[^"]*)"|(?P<value>[^\s{}]+))  # key and value
    """,
    re.VERBOSE,
)


def render_hugo_shortcode(node: RenderTreeNode, _context: RenderContext) -> str:
    content = " ".join(node.content.split())
    open_delim, close_delim = ("{{%", "%}}") if node.markup == "{{%" else ("{{<", ">}}")
    return f"{open_delim} {content} {close_delim}"


def render_image(node: RenderTreeNode, _context: RenderContext) -> str:
    src, alt, title = node.attrs.get("src", ""), node.content, node.attrs.get("title", "")
    return f'![{alt}]({src} "{title}")' if title else f"![{alt}]({src})"


def render_heading(node: RenderTreeNode, context: RenderContext) -> str:
    markup = "#" * int(node.tag[1])
    children_text = node.children[0].render(context) if node.children else ""

    if match := _INLINE_ATTRS_PATTERN.match(children_text):
        return f"{markup} {match['text'].strip()} {_format_attrs(_parse_attrs_from_string(match['attrs']))}"

    return f"{markup} {children_text}"


def _format_attrs(attrs: dict[str, str]) -> str:
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
    attrs: dict[str, str] = {}
    for match in _ATTR_PATTERN.finditer(attr_str):
        if class_name := match["class_name"]:
            attrs["class"] = f"{attrs.get('class', '')} {class_name}".strip()
        elif id_value := match["id"]:
            attrs["id"] = id_value
        else:
            attrs[match["key"]] = match["quoted_value"] if match["quoted_value"] is not None else match["value"]
    return attrs


def render_fence(node: RenderTreeNode, _context: RenderContext) -> str:
    code_block = node.content
    fence_char = "`"
    fence = fence_char * max(3, _longest_consecutive_sequence(code_block, fence_char) + 1)

    info_str = node.info or ""

    if match := _FENCE_ATTRS_PATTERN.match(info_str):
        info_str = f"{match['language']} {_format_attrs(_parse_attrs_from_string(match['attrs']))}"

    return f"{fence}{info_str}\n{code_block}{fence}"


def _longest_consecutive_sequence(text: str, char: str) -> int:
    longest = current = 0
    for symbol in text:
        current = current + 1 if symbol == char else 0
        longest = max(longest, current)
    return longest


__all__ = [
    "render_fence",
    "render_heading",
    "render_hugo_shortcode",
    "render_image",
]
