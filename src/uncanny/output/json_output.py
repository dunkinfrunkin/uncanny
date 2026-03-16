"""JSON output for scan results."""

from __future__ import annotations

import json

from uncanny.types import ScanResult


def render(result: ScanResult) -> str:
    """Render a scan result as JSON string."""
    return json.dumps(result.to_dict(), indent=2)
