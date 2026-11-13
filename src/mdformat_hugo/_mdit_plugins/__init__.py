"""Hugo markdown-it-py plugins."""

from __future__ import annotations

from .gfm_alerts import enable_gfm_alert_custom_titles
from .shortcodes import shortcode_plugin

__all__ = [
    "enable_gfm_alert_custom_titles",
    "shortcode_plugin",
]
