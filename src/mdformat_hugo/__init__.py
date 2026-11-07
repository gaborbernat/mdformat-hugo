"""Mdformat plugin for Hugo-flavored Markdown."""

from __future__ import annotations

from ._plugin import CHANGES_AST, RENDERERS, update_mdit
from ._version import __version__

__all__ = [
    "CHANGES_AST",
    "RENDERERS",
    "__version__",
    "update_mdit",
]
