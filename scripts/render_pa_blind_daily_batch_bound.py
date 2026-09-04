#!/usr/bin/env python3
"""Source-bound CLI for the deterministic PA Research chart renderer."""

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pa_source_binding import load_source_module  # noqa: E402


RENDERER_SOURCE = REPO_ROOT / "scripts" / "render_pa_blind_daily_batch.py"


if __name__ == "__main__":
    renderer = load_source_module(
        RENDERER_SOURCE,
        "_pa_source_bound_blind_daily_renderer",
        "renderer source",
    )
    raise SystemExit(renderer.main())
