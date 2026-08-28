import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "abc_bop_intake_schema_consistency_audit_2026-08-29_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"


UNIFIED_FILE = "abc_bop_contract_intake_2026-08-28.csv"
BOP_FILE = "bop_contract_intake_2026-08-28.csv"

UNIFIED_HEADERS = (
    "intake_id",
    "symbol",
    "source_case",
    "decision_date",
    "direction",
    "primary_pattern",
    "internal_label",
    "contract_branch",
    "intake_state",
    "contract_frozen",
    "event_state",
    "trigger_evidence",
    "structural_stop_evidence",
    "first_obstacle_evidence",
    "space_evidence",
    "lineage_evidence",
    "missing_fields",
    "freeze_recommendation",
)

BOP_HEADERS = (
    "intake_id",
    "symbol",
    "source_case",
    "decision_date",
    "direction",
    "classification",
    "bop_state",
    "old_boundary_evidence",
    "breakout_acceptance_evidence",
    "retest_class",
    "role_reversal_evidence",
    "order_branch",
    "intake_state",
    "contract_frozen",
    "event_state",
    "first_obstacle_evidence",
    "space_evidence",
    "lineage_evidence",
    "missing_fields",
    "freeze_recommendation",
)

EXPECTED_BOP_CLASSIFICATIONS = {
    "acceptance_candidate",
    "single_session_retest",
    "gap_boundary",
    "opening_reprice_boundary",
    "obstacle_boundary",
    "acceptance_without_retest",
    "not_bop_nested",
    "not_bop_hl",
    "range_edge_boundary",
    "not_bop_reversal",
    "not_bop_late_trend",
}

EXPECTED_BOP_STATE_BY_ID = {
    "BOP-TSLA-ACCEPT-20250911": "breakout_acceptance",
    "BOP-TSLA-RETEST-20250304": "breakout_pullback",
    "BOP-VRT-20260417": "gap_event",
    "BOP-NKE-20251028": "role_reversal_watch",
    "BOP-GOOGL-20240318": "gap_event",
    "BOP-WMT-20240626": "gap_event",
    "BOP-BKNG-20240614": "gap_event",
    "BOP-QCOM-20240724": "gap_event",
    "BOP-JPM-20250905": "failed_breakout_watch",
    "BOP-KLAC-20251024": "breakout_acceptance",
    "BOP-META-20241011": "not_bop",
    "BOP-TSLA-HL-20250905": "not_bop",
    "BOP-TSLA-RANGE-20250508": "range_edge",
    "BOP-TSLA-DEEP-20260520": "not_bop",
    "BOP-TSLA-LATE-20251212": "not_bop",
}


def _read_table(filename: str) -> tuple[tuple[str, ...], list[list[str]], list[dict[str, str]]]:
    with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = tuple(next(reader))
        raw_rows = list(reader)
    rows = [dict(zip(header, raw_row)) for raw_row in raw_rows]
    return header, raw_rows, rows


class PaResearchIntakeSchemaConsistencyTests(unittest.TestCase):
    def test_each_intake_has_exact_schema_complete_values_and_resolvable_source(self):
        specs = (
            (UNIFIED_FILE, UNIFIED_HEADERS, 10),
            (BOP_FILE, BOP_HEADERS, 15),
        )
        all_ids = []
        for filename, expected_headers, expected_rows in specs:
            with self.subTest(filename=filename):
                headers, raw_rows, rows = _read_table(filename)
                self.assertEqual(headers, expected_headers)
                self.assertEqual(len(raw_rows), expected_rows)
                self.assertNotIn("sample_id", headers)
                self.assertEqual(len({row["intake_id"] for row in rows}), len(rows))
                for row_number, (raw_row, row) in enumerate(zip(raw_rows, rows), start=2):
                    self.assertEqual(
                        len(raw_row),
                        len(headers),
                        f"{filename}:{row_number} has malformed CSV width",
                    )
                    for field in headers:
                        self.assertTrue(
                            row[field].strip(),
                            f"{filename}:{row_number} has empty {field}",
                        )
                    self.assertIn(row["direction"], {"long", "short"})
                    date.fromisoformat(row["decision_date"])
                    self.assertEqual(row["contract_frozen"].casefold(), "no")
                    source_case = row["source_case"]
                    self.assertFalse(Path(source_case).is_absolute())
                    self.assertNotIn("..", Path(source_case).parts)
                    source_path = REPO_ROOT / source_case
                    self.assertTrue(source_path.is_file(), source_case)
                    self.assertIn(row["symbol"], source_path.read_text(encoding="utf-8"))
                    all_ids.append(row["intake_id"])

        self.assertEqual(len(all_ids), 25)
        self.assertEqual(len(set(all_ids)), 25)

    def test_unified_intake_pattern_direction_and_label_partitions(self):
        _, _, rows = _read_table(UNIFIED_FILE)
        self.assertEqual(Counter(row["direction"] for row in rows), Counter({"long": 6, "short": 4}))
        self.assertEqual(
            Counter(row["primary_pattern"] for row in rows),
            Counter({"ABC_CONT": 6, "BOP": 4}),
        )
        self.assertEqual(
            Counter(row["internal_label"] for row in rows),
            Counter({"H2": 4, "L1": 2, "none": 4}),
        )
        for row in rows:
            if row["primary_pattern"] == "BOP":
                self.assertEqual(row["internal_label"], "none", row["intake_id"])
            else:
                self.assertIn(row["internal_label"], {"H1", "H2", "L1", "L2", "H3", "L3"})

        tsla_acceptance = next(row for row in rows if row["intake_id"] == "BOP-TSLA-20250911")
        self.assertEqual(tsla_acceptance["direction"], "long")
        self.assertEqual(tsla_acceptance["primary_pattern"], "BOP")

    def test_bop_intake_state_and_retest_boundaries(self):
        _, _, rows = _read_table(BOP_FILE)
        self.assertEqual(
            Counter(row["direction"] for row in rows),
            Counter({"long": 12, "short": 3}),
        )
        self.assertEqual(
            Counter(row["retest_class"] for row in rows),
            Counter({"not-occurred": 10, "intraday-only": 3, "single-session": 2}),
        )
        self.assertEqual(set(row["classification"] for row in rows), EXPECTED_BOP_CLASSIFICATIONS)
        self.assertEqual({row["intake_id"] for row in rows}, set(EXPECTED_BOP_STATE_BY_ID))
        for row in rows:
            self.assertEqual(row["bop_state"], EXPECTED_BOP_STATE_BY_ID[row["intake_id"]])
            self.assertNotEqual(row["retest_class"], "multi-day")
            self.assertTrue(row["freeze_recommendation"].startswith("do_not_replay"))
            if row["retest_class"] == "intraday-only":
                self.assertTrue(
                    "multi_day" in row["missing_fields"]
                    or "multi_day" in row["freeze_recommendation"].lower()
                )
            else:
                self.assertIn("multi_day_retest", row["missing_fields"])

    def test_cross_schema_aliases_are_explicit_and_directionally_consistent(self):
        all_rows = []
        for filename in (UNIFIED_FILE, BOP_FILE):
            _, _, rows = _read_table(filename)
            all_rows.extend((filename, row) for row in rows)

        by_case = defaultdict(list)
        for filename, row in all_rows:
            key = (row["symbol"], row["decision_date"], row["source_case"])
            by_case[key].append((filename, row))

        aliases = {key: group for key, group in by_case.items() if len(group) > 1}
        self.assertEqual(len(by_case), 22)
        self.assertEqual(len(aliases), 3)
        expected_aliases = {
            ("TSLA", "2025-03-04", "research/tsla_abc_playbook_2025-03-04_284_retest.md"),
            ("TSLA", "2025-09-11", "research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md"),
            ("NKE", "2025-10-28", "research/nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md"),
        }
        self.assertEqual(set(aliases), expected_aliases)
        for key, group in aliases.items():
            self.assertEqual({row["direction"] for _, row in group}, {group[0][1]["direction"]}, key)
            self.assertEqual(len({row["intake_id"] for _, row in group}), len(group), key)

    def test_current_intake_audit_indexes_schema_and_boundary_fixes(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        backtesting_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        validator = VALIDATOR_PATH.read_text(encoding="utf-8")
        for text in (research_readme, backtesting_readme, validator):
            self.assertIn("abc_bop_intake_schema_consistency_audit_2026-08-29_CN.md", text)
        for token in (
            "18",
            "20",
            "22 个底层案例键",
            "3 个案例同时出现在两种 intake 视图中",
            "BOP-UNIFIED-NKE-20251028",
            "TSLA 2025-09-11 为 `long`",
            "no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, audit)

    def test_validator_rejects_missing_intake_freeze_recommendation(self):
        with tempfile.TemporaryDirectory(prefix="pa-research-intake-schema-") as directory:
            fixture_root = Path(directory) / "repo"
            shutil.copytree(
                REPO_ROOT,
                fixture_root,
                ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc"),
            )
            intake_path = fixture_root / "research" / "backtesting" / UNIFIED_FILE
            lines = intake_path.read_text(encoding="utf-8").splitlines()
            target_index = next(
                index for index, line in enumerate(lines) if line.startswith("BOP-UNIFIED-NKE-20251028,")
            )
            lines[target_index] = lines[target_index].rsplit(",", 1)[0]
            intake_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(fixture_root / "scripts" / "validate_pa_research_docs.ps1"),
                    "-RepoRoot",
                    str(fixture_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "ABC/BOP intake row missing required value 'freeze_recommendation': BOP-UNIFIED-NKE-20251028",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
