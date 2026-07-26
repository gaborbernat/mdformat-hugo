"""Force mdformat-gfm-alerts' custom_title option on, matching Hugo's own alert grammar."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markdown_it import MarkdownIt


def enable_gfm_alert_custom_titles(mdit: MarkdownIt) -> None:
    """Force an inline custom title on `[!TYPE]` alert lines. Not configurable."""
    mdit.options["mdformat"]["custom_title"] = True
