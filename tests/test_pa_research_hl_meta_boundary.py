"""Regression checks for H/L META status, components, and authorization boundaries."""

import csv
from collections import Counter
from pathlib import Path
import unittest

from pa_research_backtest.engine import SUPPORTED_META_CONFLUENCE


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_meta_boundary_audit_2026-08-29_CN.md"

CONTRACT_FILES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)


def _rows_and_headers():
    rows = []
    headers = {}
    for filename in CONTRACT_FILES:
        with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers[filename] = set(reader.fieldnames or ())
            rows.extend((filename, row) for row in reader)
    return rows, headers


def _components(row):
    raw = row.get("meta_components", "")
    return [
        item.strip().lower()
        for item in raw.replace("|", ";").replace(",", ";").replace("+", ";").split(";")
        if item.strip()
    ]


class PaResearchHlMetaBoundaryTests(unittest.TestCase):
    def test_frozen_meta_states_and_present_requirements(self):
        rows, _ = _rows_and_headers()
        self.assertEqual(len(rows), 60)
        self.assertEqual(SUPPORTED_META_CONFLUENCE, {"present", "absent", "unknown"})
        self.assertNotIn("pending", SUPPORTED_META_CONFLUENCE)

        states = Counter(row["meta_confluence"].strip() for _, row in rows)
        self.assertEqual(states, Counter({"present": 49, "absent": 11}))

        present = [row for _, row in rows if row["meta_confluence"].strip() == "present"]
        self.assertEqual(sum(bool(row["meta_zone"].strip()) for row in present), 49)
        self.assertEqual(
            Counter(len(set(_components(row))) for row in present),
            Counter({3: 39, 2: 10}),
        )

        absent = [row for _, row in rows if row["meta_confluence"].strip() == "absent"]
        self.assertTrue(all(not row["meta_zone"].strip() for row in absent))
        self.assertTrue(all(not row["meta_components"].strip() for row in absent))

    def test_meta_does_not_override_ema_gate_or_space(self):
        rows, _ = _rows_and_headers()
        confluence_gate = Counter(
            (row["meta_confluence"].strip(), row["h_l_ema_slope_gate"].strip())
            for _, row in rows
        )
        self.assertEqual(
            confluence_gate,
            Counter(
                {
                    ("present", "long_pass"): 23,
                    ("present", "short_pass"): 21,
                    ("present", "fail_flat_or_opposite"): 5,
                    ("absent", "long_pass"): 4,
                    ("absent", "short_pass"): 7,
                }
            ),
        )

        confluence_space = Counter(
            (
                row["meta_confluence"].strip(),
                row.get("space_status", "").strip() or "<blank>",
            )
            for _, row in rows
        )
        self.assertEqual(
            confluence_space,
            Counter(
                {
                    ("present", "<blank>"): 45,
                    ("present", "strict_ge_1R"): 4,
                    ("absent", "<blank>"): 5,
                    ("absent", "strict_ge_1R"): 5,
                    ("absent", "borderline_ge_1R"): 1,
                }
            ),
        )

    def test_meta_components_have_no_obvious_direction_conflict(self):
        rows, headers = _rows_and_headers()
        self.assertTrue(
            all(
                not (
                    row["direction"] == "short"
                    and any("rising" in item or "upward" in item for item in _components(row))
                )
                for _, row in rows
            )
        )
        self.assertTrue(
            all(
                not (
                    row["direction"] == "long"
                    and any("falling" in item or "downward" in item for item in _components(row))
                )
                for _, row in rows
            )
        )
        self.assertTrue(all("b_leg_location" not in header for header in headers.values()))

    def test_audit_docs_and_reports_preserve_meta_boundaries(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "7 份 CSV 共 60 行",
            "`present` | 49",
            "`absent` | 11",
            "`unknown` | 0",
            "`pending` | 0",
            "fail_flat_or_opposite",
            "strict_ge_1R",
            "不能替代方向",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        schema = (REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md").read_text(encoding="utf-8")
        selection = (REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md").read_text(encoding="utf-8")
        visual = (REPO_ROOT / "docs" / "visual_pa_review_card_CN.md").read_text(encoding="utf-8")
        backtesting = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        meta_strategy = (REPO_ROOT / "strategy" / "meta_multiple_edge.md").read_text(encoding="utf-8")
        self.assertIn("canonical 枚举只有 `present / absent / unknown`", schema)
        self.assertIn("不能写 `pending`", schema)
        self.assertIn("meta_confluence` 只接受 `present / absent / unknown`", selection)
        self.assertIn("`pending` 属于整体视觉复核或触发状态", visual)
        self.assertIn("冻结合同枚举只有 `present`、`absent`、`unknown`", backtesting)
        self.assertIn("separate trade-geometry gate, not a META component", meta_strategy)

        reports = (
            BACKTEST_ROOT / "hl_large_selection_2026-08-27_CN.md",
            BACKTEST_ROOT / "hl_next4_selection_2026-08-27_CN.md",
            BACKTEST_ROOT / "hl_next4_replay_2026-08-27_CN.md",
            BACKTEST_ROOT / "hl_next5_replay_2026-08-27_CN.md",
        )
        for path in reports:
            with self.subTest(path=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertIn("META", content)
                self.assertTrue(
                    any(token in content for token in ("触发", "止损", "空间", "授权", "胜率"))
                )

        indexed = (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed:
            with self.subTest(path=path.as_posix(), index=True):
                self.assertIn(AUDIT_PATH.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
