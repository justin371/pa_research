import ast
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXECUTABLE_ROOTS = (REPO_ROOT / "pa_research_backtest", REPO_ROOT / "scripts")
BLOCKED_IMPORT_ROOTS = {
    "alpaca",
    "binance",
    "broker",
    "futu",
    "httpx",
    "ib",
    "ib_insync",
    "ibkr",
    "mcp",
    "moomoo",
    "requests",
    "socket",
    "urllib",
    "websocket",
}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


class PaResearchScopeBoundaryTests(unittest.TestCase):
    def test_executable_code_has_no_external_market_or_execution_imports(self):
        violations = {
            f"{path.relative_to(REPO_ROOT)}: {root}"
            for directory in EXECUTABLE_ROOTS
            for path in directory.rglob("*.py")
            for root in imported_roots(path) & BLOCKED_IMPORT_ROOTS
        }
        self.assertEqual(violations, set())

    def test_backtesting_dependencies_are_research_only_and_pinned(self):
        requirements = REPO_ROOT / "requirements-backtesting.txt"
        dependencies = [
            line.split("#", 1)[0].strip()
            for line in requirements.read_text(encoding="utf-8").splitlines()
            if line.split("#", 1)[0].strip()
        ]
        self.assertEqual(
            dependencies,
            ["backtesting==0.6.6", "matplotlib==3.10.9"],
        )


if __name__ == "__main__":
    unittest.main()
