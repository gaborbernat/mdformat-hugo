"""Mdformat plugin for Hugo-flavored Markdown."""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("mdformat-hugo")

from ._plugin import CHANGES_AST, RENDERERS, update_mdit

__all__ = [
    "CHANGES_AST",
    "RENDERERS",
    "__version__",
    "update_mdit",
]
