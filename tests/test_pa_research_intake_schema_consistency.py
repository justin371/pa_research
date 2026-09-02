import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import re
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


def _active_source_text(text: str) -> str:
    """Exclude inactive HTML comments while retaining fenced source metadata."""
    return re.sub(r"(?s)<!--.*?(?:-->|$)", "", text)


def _source_identity_is_bound(text: str, row: dict[str, str]) -> bool:
    active_text = _active_source_text(text)
    ticker = re.escape(row["symbol"])
    ticker_pattern = rf"(?<![A-Za-z0-9_])(?:US\.)?{ticker}(?![A-Za-z0-9_])"
    date_pattern = rf"(?<!\d){re.escape(row['decision_date'])}(?!\d)"
    h1_pattern = rf"(?im)^[ \t]*#(?!#)[ \t]+.*{ticker_pattern}"
    symbol_field_pattern = (
        rf"(?im)^[ \t]*(?:[-*][ \t]*)?(?:symbol|instrument|ticker|标的)"
        rf"[ \t]*[:：][ \t]*.*{ticker_pattern}"
    )
    return bool(
        re.search(date_pattern, active_text)
        and (
            re.search(h1_pattern, active_text)
            or re.search(symbol_field_pattern, active_text)
        )
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
                    self.assertEqual(source_path.suffix.casefold(), ".md", source_case)
                    self.assertTrue(
                        _source_identity_is_bound(source_path.read_text(encoding="utf-8"), row),
                        f"{filename}:{row_number} source_case identity is not bound",
                    )
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
                ignore=shutil.ignore_patterns(".git", ".venv", ".codex", "__pycache__", "*.pyc"),
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

    def test_validator_rejects_unbound_source_case_variants(self):
        unified_rows = _read_table(UNIFIED_FILE)[2]
        bop_rows = _read_table(BOP_FILE)[2]
        wrong_readme = unified_rows[0]
        wrong_date = unified_rows[1]
        comment_only = unified_rows[2]
        same_symbol_target = next(row for row in bop_rows if row["decision_date"] == "2025-03-04")
        same_symbol_source = next(
            row["source_case"]
            for row in bop_rows
            if row["symbol"] == same_symbol_target["symbol"]
            and row["decision_date"] != same_symbol_target["decision_date"]
            and same_symbol_target["decision_date"]
            not in (REPO_ROOT / row["source_case"]).read_text(encoding="utf-8")
        )

        with tempfile.TemporaryDirectory(prefix="pa-research-intake-source-binding-") as directory:
            fixture_root = Path(directory) / "repo"
            shutil.copytree(
                REPO_ROOT,
                fixture_root,
                ignore=shutil.ignore_patterns(".git", ".venv", ".codex", "__pycache__", "*.pyc"),
            )

            def rewrite(filename: str, intake_id: str, **updates: str) -> None:
                path = fixture_root / "research" / "backtesting" / filename
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    fieldnames = reader.fieldnames
                    rows = list(reader)
                self.assertIsNotNone(fieldnames)
                target = next(row for row in rows if row["intake_id"] == intake_id)
                target.update(updates)
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

            rewrite(UNIFIED_FILE, wrong_readme["intake_id"], source_case="research/README.md")
            rewrite(UNIFIED_FILE, wrong_date["intake_id"], decision_date="2099-01-01")
            rewrite(
                UNIFIED_FILE,
                comment_only["intake_id"],
                source_case=comment_only["source_case"],
            )
            (fixture_root / comment_only["source_case"]).write_text(
                f"<!-- # {comment_only['symbol']} {comment_only['decision_date']}\n"
                f"symbol: US.{comment_only['symbol']} -->\n",
                encoding="utf-8",
                newline="",
            )
            rewrite(
                BOP_FILE,
                same_symbol_target["intake_id"],
                source_case=same_symbol_source,
            )

            result = subprocess.run(
                [
                    "pwsh",
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
                f"ABC/BOP intake row source_case is missing ticker '{wrong_readme['symbol']}' in an active level-1 heading or explicit symbol field: {wrong_readme['intake_id']}",
                result.stdout,
            )
            self.assertIn(
                f"ABC/BOP intake row source_case is missing exact decision_date '2099-01-01': {wrong_date['intake_id']}",
                result.stdout,
            )
            self.assertIn(
                f"ABC/BOP intake row source_case is missing ticker '{comment_only['symbol']}' in an active level-1 heading or explicit symbol field: {comment_only['intake_id']}",
                result.stdout,
            )
            self.assertIn(
                f"BOP intake row source_case is missing exact decision_date '{same_symbol_target['decision_date']}': {same_symbol_target['intake_id']}",
                result.stdout,
            )

    def test_validator_ignores_commented_canonical_tokens_but_keeps_fenced_tokens(self):
        canonical_path = Path("docs/pa_research_output_schema_v0_1_CN.md")
        canonical_token = "chart_scope: full / partial / unavailable"
        with tempfile.TemporaryDirectory(prefix="pa-research-canonical-comment-") as directory:
            fixture_root = Path(directory) / "repo"
            shutil.copytree(
                REPO_ROOT,
                fixture_root,
                ignore=shutil.ignore_patterns(".git", ".venv", ".codex", "__pycache__", "*.pyc"),
            )
            schema_path = fixture_root / canonical_path
            original = schema_path.read_text(encoding="utf-8")
            self.assertEqual(original.count(canonical_token), 1)
            self.assertGreaterEqual(original.count("```"), 2)

            def run_validator():
                return subprocess.run(
                    [
                        "pwsh",
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

            positive = run_validator()
            self.assertEqual(positive.returncode, 0, positive.stdout)
            self.assertNotIn(
                f"missing canonical token '{canonical_token}': {canonical_path.as_posix()}",
                positive.stdout,
            )

            schema_path.write_text(
                original.replace(canonical_token, f"<!-- {canonical_token} -->"),
                encoding="utf-8",
                newline="",
            )
            negative = run_validator()
            self.assertNotEqual(negative.returncode, 0)
            self.assertIn(
                f"missing canonical token '{canonical_token}': {canonical_path.as_posix()}",
                negative.stdout,
            )


if __name__ == "__main__":
    unittest.main()
