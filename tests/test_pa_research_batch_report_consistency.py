import csv
from collections import Counter
from pathlib import Path
import re
import unittest

from pa_research_backtest.engine import _contract_space_bucket, _event_bucket


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "batch_report_numeric_consistency_audit_2026-08-29_CN.md"


BATCHES = (
    {
        "name": "首批",
        "contracts": "hl_contracts_2026-08-26.csv",
        "selection": "hl_contract_batch_replay_2026-08-26_CN.md",
        "replay": "hl_contract_batch_replay_2026-08-26_CN.md",
        "replay_facts": (
            "contract_count=5",
            "eligible_contract_count=4",
            "filled_count=3",
            "completed_trade_count=3",
            "win_rate_pct=33.33%",
        ),
        "outcome_facts": ("33.33%", "-0.9414R", "1/3"),
    },
    {
        "name": "第二批",
        "contracts": "hl_contracts_batch2_2026-08-26.csv",
        "selection": "hl_contract_batch2_replay_2026-08-26_CN.md",
        "replay": "hl_contract_batch2_replay_2026-08-26_CN.md",
        "replay_facts": (
            "contract_count=3",
            "eligible=3",
            "filled=3",
            "completed=3",
            "3/3 wins = 100.00%",
        ),
        "outcome_facts": ("100.00%", "+4.8743R", "3/3"),
    },
    {
        "name": "大样本",
        "contracts": "hl_large_contracts_2026-08-27.csv",
        "selection": "hl_large_selection_2026-08-27_CN.md",
        "replay": "hl_large_replay_2026-08-27_CN.md",
        "replay_facts": (
            "| 冻结合同 | 37 |",
            "| 实际成交 | 17 |",
            "| 完成且可比 | 17 |",
            "| 胜 / 负 | 13 / 4 |",
            "76.47%",
        ),
        "outcome_facts": ("76.47%", "+1.9652R", "13/4"),
    },
    {
        "name": "下一批",
        "contracts": "hl_next_contracts_2026-08-27.csv",
        "selection": "hl_next_selection_2026-08-27_CN.md",
        "replay": "hl_next_replay_2026-08-27_CN.md",
        "replay_facts": (
            "| 全部 | 5 | 2 | 2 | 1 / 1",
            "50.00%",
        ),
        "outcome_facts": ("50.00%", "+1.4063R", "1/1"),
    },
    {
        "name": "下一批（二）",
        "contracts": "hl_next2_contracts_2026-08-27.csv",
        "selection": "hl_next2_selection_2026-08-27_CN.md",
        "replay": "hl_next2_replay_2026-08-27_CN.md",
        "replay_facts": (
            "| 全部 | 2 | 2 | 2 | 2 / 0",
            "100.00%",
        ),
        "outcome_facts": ("100.00%", "+2.5925R", "2/0"),
    },
    {
        "name": "下一批（四）",
        "contracts": "hl_next4_contracts_2026-08-27.csv",
        "selection": "hl_next4_selection_2026-08-27_CN.md",
        "replay": "hl_next4_replay_2026-08-27_CN.md",
        "replay_facts": (
            "| 全部 | 2 | 2 | 2 | 0 / 2",
            "0.00%",
        ),
        "outcome_facts": ("0.00%", "-1.5090R", "0/2"),
    },
    {
        "name": "下一批（五）",
        "contracts": "hl_next5_contracts_2026-08-27.csv",
        "selection": "hl_next5_selection_2026-08-27_CN.md",
        "replay": "hl_next5_replay_2026-08-27_CN.md",
        "replay_facts": (
            "本批回放 6 条",
            "| 全部合同 | 6 | 5 | 3 / 2",
            "60.00%",
        ),
        "outcome_facts": ("60.00%", "+3.4812R", "3/2"),
    },
)


def _read_contract_rows(filename: str) -> list[dict[str, str]]:
    with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _geometry_space(row: dict[str, str]) -> float:
    entry = float(row["entry_trigger"])
    stop = float(row["structural_stop"])
    obstacle = float(row["first_obstacle"])
    risk = abs(entry - stop)
    if row["direction"] == "long":
        return (obstacle - entry) / risk
    return (entry - obstacle) / risk


def _fact_counts(rows: list[dict[str, str]]) -> dict[str, Counter | int]:
    spaces = Counter(
        _contract_space_bucket(
            row.get("space_status", ""),
            float(row["pre_entry_space_R"]) if row.get("pre_entry_space_R") else None,
        )
        for row in rows
    )
    geometry = Counter("ge_1R" if _geometry_space(row) >= 1.0 else "lt_1R" for row in rows)
    gates = Counter(row["h_l_ema_slope_gate"] for row in rows)
    gates["observation_only"] = gates.get("fail_flat_or_opposite", 0)
    return {
        "directions": Counter(row["direction"] for row in rows),
        "labels": Counter(row["internal_label"] for row in rows),
        "gates": gates,
        "events": Counter(_event_bucket(row["event_context"]) for row in rows),
        "spaces": spaces,
        "geometry": geometry,
        "lineages": len({row["lineage_id"].strip().casefold() for row in rows}),
    }


def _semantic_report_lines(text: str) -> list[str]:
    """Return report lines that are rendered content, not examples or comments."""
    lines: list[str] = []
    in_fence = False
    text = re.sub(r"(?s)<!--.*?(?:-->|$)", "", text)
    for raw_line in text.splitlines():
        line = raw_line
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if not in_fence and line.strip():
            lines.append(line)
    return lines


def _active_report_text(*texts: str) -> str:
    """Preserve fenced contract blocks while excluding commented-out claims."""
    return "\n".join(re.sub(r"(?s)<!--.*?(?:-->|$)", "", text) for text in texts)


def _structured_identity_lines(text: str, row: dict[str, str]) -> list[str]:
    symbol = re.escape(row["symbol"])
    decision_date = re.escape(row["decision_date"])
    label = re.escape(row["internal_label"])
    date_token = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
    expected_date = re.compile(rf"(?<!\d){decision_date}(?!\d)")
    expected_label = re.compile(rf"(?<![A-Za-z0-9_]){label}(?![A-Za-z0-9_])")
    identity_rows: list[str] = []
    for line in _semantic_report_lines(text):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2 or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if not re.search(rf"(?<![A-Za-z0-9_]){symbol}(?![A-Za-z0-9_])", stripped):
            continue
        date_matches = list(date_token.finditer(stripped))
        for index, date_match in enumerate(date_matches):
            if not expected_date.fullmatch(date_match.group()):
                continue
            if len(date_matches) == 1:
                date_label_segment = stripped
            else:
                next_date = date_matches[index + 1].start() if index + 1 < len(date_matches) else len(stripped)
                date_label_segment = stripped[date_match.start() : next_date]
            if expected_label.search(date_label_segment):
                identity_rows.append(line)
                break
    return identity_rows


def _assert_report_facts(testcase: unittest.TestCase, selection: str, replay: str, batch: dict[str, object]) -> None:
    report_text = _active_report_text(selection, replay)
    for direction in sorted({row["direction"] for row in _read_contract_rows(batch["contracts"]) }):
        testcase.assertIn(direction, report_text)
    for label in sorted({row["internal_label"] for row in _read_contract_rows(batch["contracts"]) }):
        testcase.assertIn(label, report_text)
    for fact in batch["replay_facts"]:
        testcase.assertIn(fact, _active_report_text(replay))
    for fact in batch["outcome_facts"]:
        if "/" in fact and all(part.isdigit() for part in fact.split("/")):
            left, right = fact.split("/")
            testcase.assertRegex(
                _active_report_text(replay),
                rf"(?<!\d){re.escape(left)}\s*/\s*{re.escape(right)}(?!\d)",
            )
        else:
            testcase.assertIn(fact, _active_report_text(replay))
    testcase.assertIn("no-new-positive", _active_report_text(replay))
    testcase.assertIn("validated win-rate: not-computable", _active_report_text(replay))


class PaResearchBatchReportConsistencyTests(unittest.TestCase):
    def test_current_contract_facts_match_machine_audit(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")

        for batch in BATCHES:
            with self.subTest(batch=batch["name"]):
                rows = _read_contract_rows(batch["contracts"])
                facts = _fact_counts(rows)
                directions = facts["directions"]
                labels = facts["labels"]
                gates = facts["gates"]
                events = facts["events"]
                spaces = facts["spaces"]
                geometry = facts["geometry"]

                self.assertIn(
                    f"| {batch['name']} | `{batch['contracts']}` | {len(rows)} | "
                    f"{directions['long']}/{directions['short']} | "
                    f"{labels['H1']}/{labels['H2']}/{labels['L1']}/{labels['L2']} | "
                    f"{gates['long_pass']}/{gates['short_pass']}/{gates['observation_only']} |",
                    audit,
                )
                self.assertIn(
                    f"event_reviewed_non_event={events['event_reviewed_non_event']}; "
                    f"event_driven={events['event_driven']}; "
                    f"event_unverified_or_pending={events['event_unverified_or_pending']}; "
                    f"ordinary_non_event={events['ordinary_non_event']}; "
                    f"earnings_adjacent={events['earnings_adjacent']}; "
                    f"unknown={events['unknown']}",
                    audit,
                )
                audit_row = next(
                    line for line in audit.splitlines() if line.startswith(f"| {batch['name']} |")
                )
                self.assertIn(
                    f"explicit={spaces['strict_ge_1R']}/{spaces['borderline']}/"
                    f"{spaces['unknown_contract_space']} |",
                    audit_row,
                )
                self.assertIn(
                    f"geometry={geometry['ge_1R']}/{geometry['lt_1R']} |",
                    audit_row,
                )
                self.assertTrue(audit_row.rstrip().endswith(f"| lineages={facts['lineages']} |"))

    def test_selection_and_replay_reports_preserve_contract_identity_and_facts(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")

        for batch in BATCHES:
            with self.subTest(batch=batch["name"]):
                rows = _read_contract_rows(batch["contracts"])
                selection = (BACKTEST_ROOT / batch["selection"]).read_text(encoding="utf-8")
                replay = (BACKTEST_ROOT / batch["replay"]).read_text(encoding="utf-8")

                for row in rows:
                    identity_lines = _structured_identity_lines(selection, row)
                    self.assertTrue(
                        identity_lines,
                        f"missing {row['symbol']} {row['decision_date']} in selection report",
                    )
                _assert_report_facts(self, selection, replay, batch)

                self.assertIn(f"| {batch['name']} |", audit)

    def test_identity_rows_ignore_comments_and_fenced_examples(self):
        positive_batch = BATCHES[3]
        positive_selection = (BACKTEST_ROOT / positive_batch["selection"]).read_text(encoding="utf-8")
        positive_row = _read_contract_rows(positive_batch["contracts"])[0]
        self.assertTrue(_structured_identity_lines(positive_selection, positive_row))

        comment_only = (
            "<!-- | {symbol} {date} | {label} | -->\n"
            "```markdown\n"
            "| {symbol} {date} | {label} | example |\n"
            "```\n"
        ).format(
            symbol=positive_row["symbol"],
            date=positive_row["decision_date"],
            label=positive_row["internal_label"],
        )
        self.assertEqual([], _structured_identity_lines(comment_only, positive_row))

        crossed_pair = (
            f"| {positive_row['symbol']} | {positive_row['decision_date']} L1; "
            f"2025-12-31 {positive_row['internal_label']} |\n"
        )
        self.assertEqual([], _structured_identity_lines(crossed_pair, positive_row))

        facts_only_in_comment = (
            f"| {positive_row['symbol']} {positive_row['decision_date']} | "
            f"{positive_row['internal_label']} |\n"
            "<!-- "
            + " ".join(
                (
                    *positive_batch["replay_facts"],
                    *positive_batch["outcome_facts"],
                    "no-new-positive",
                    "validated win-rate: not-computable",
                )
            )
            + " -->\n"
        )
        self.assertTrue(_structured_identity_lines(facts_only_in_comment, positive_row))
        with self.assertRaises(AssertionError):
            _assert_report_facts(self, facts_only_in_comment, facts_only_in_comment, positive_batch)

    def test_intake_total_and_pattern_split_are_not_frozen_contracts(self):
        unified = _read_contract_rows("abc_bop_contract_intake_2026-08-28.csv")
        bop = _read_contract_rows("bop_contract_intake_2026-08-28.csv")
        all_rows = unified + bop
        self.assertEqual(len(unified), 10)
        self.assertEqual(Counter(row["primary_pattern"] for row in unified), Counter({"ABC_CONT": 6, "BOP": 4}))
        self.assertEqual(len(bop), 15)
        self.assertEqual(len(all_rows), 25)
        self.assertTrue(all(row["contract_frozen"].casefold() == "no" for row in all_rows))
        self.assertTrue(all("sample_id" not in row for row in all_rows))

        audit = AUDIT_PATH.read_text(encoding="utf-8")
        unified_row = next(line for line in audit.splitlines() if line.startswith("| 统一 ABC/BOP intake |"))
        bop_row = next(line for line in audit.splitlines() if line.startswith("| BOP 专项 intake |"))
        total_row = next(line for line in audit.splitlines() if line.startswith("| 全部 intake |"))
        self.assertIn("| 10 | `ABC_CONT` 6、`BOP` 4 |", unified_row)
        self.assertIn("| 15 |", bop_row)
        self.assertIn("| 25 |", total_row)

    def test_audit_is_indexed_and_validator_required(self):
        relative = "batch_report_numeric_consistency_audit_2026-08-29_CN.md"
        research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        backtesting_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(encoding="utf-8")
        self.assertIn(relative, research_readme)
        self.assertIn(relative, backtesting_readme)
        self.assertIn(f"research/backtesting/{relative}", validator)


if __name__ == "__main__":
    unittest.main()
