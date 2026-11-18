from __future__ import annotations

from importlib.metadata import version

import mdformat_hugo


def test_version() -> None:
    assert mdformat_hugo.__version__ == version("mdformat-hugo")
