"""Mdformat plugin for Hugo-flavored Markdown."""

from __future__ import annotations

__lazy_modules__ = [
    f"{__spec__.parent}._plugin",  # ty: ignore[missing-union-attribute]  # imported modules have a spec
    f"{__spec__.parent}._version",  # ty: ignore[missing-union-attribute]  # imported modules have a spec
]

from ._plugin import CHANGES_AST, RENDERERS, update_mdit
from ._version import __version__

__all__ = [
    "CHANGES_AST",
    "RENDERERS",
    "__version__",
    "update_mdit",
]
