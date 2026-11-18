"""Hugo markdown-it-py plugins."""

from __future__ import annotations

__lazy_modules__ = [
    f"{__spec__.parent}.gfm_alerts",  # ty: ignore[missing-union-attribute]  # imported modules have a spec
    f"{__spec__.parent}.shortcodes",  # ty: ignore[missing-union-attribute]  # imported modules have a spec
]

from .gfm_alerts import enable_gfm_alert_custom_titles
from .shortcodes import shortcode_plugin

__all__ = [
    "enable_gfm_alert_custom_titles",
    "shortcode_plugin",
]
