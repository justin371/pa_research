"""Source-bound entry point for the PA Research-only replay adapter."""

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pa_source_binding import load_source_module  # noqa: E402


ENGINE_SOURCE = REPO_ROOT / "pa_research_backtest" / "engine.py"


if __name__ == "__main__":
    engine = load_source_module(
        ENGINE_SOURCE,
        "pa_research_backtest._source_bound_engine",
        "engine source",
    )
    raise SystemExit(engine.main())
