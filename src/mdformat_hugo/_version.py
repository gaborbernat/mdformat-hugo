"""Version of the installed mdformat-hugo package."""

from __future__ import annotations

from importlib.metadata import version
from typing import Final

#: The installed version of mdformat-hugo, read from the package metadata.
__version__: Final[str] = version("mdformat-hugo")

__all__ = [
    "__version__",
]
