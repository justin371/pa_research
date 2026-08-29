import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "research" / "unified_output_state_axis_audit_2026-08-29_CN.md"


HISTORICAL_SUMMARY_GATES = {
    "research/qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md": "observation_only",
    "research/tsla_abc_h1_h2_comparison_matrix.md": "observation_only",
    "research/tsla_bearish_abc_candidate_screen_2026-08-22.md": "pending",
    "research/tsla_bearish_abc_comparison_matrix.md": "observation_only",
    "research/tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md": "pending",
    "research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md": "observation_only",
}


def first_contract_block(text):
    for match in re.finditer(r"```(?:text)?\r?\n(.*?)```", text, re.DOTALL):
        block = match.group(1)
        if "contract_scope:" in block and "direction:" in block:
            return block
    raise AssertionError("no contract block found")


def field(block, name):
    match = re.search(rf"(?m)^{re.escape(name)}:\s*([^\r\n]*)$", block)
    if not match:
        raise AssertionError(f"missing {name}")
    return match.group(1).strip()


class UnifiedOutputStateAxisTests(unittest.TestCase):
    def test_document_maturity_is_separate_from_case_research_state(self):
        markdown_files = sorted(REPO_ROOT.rglob("*.md"))
        invalid = []
        header_count = 0
        for path in markdown_files:
            text = path.read_text(encoding="utf-8")
            if re.search(r"research_state\s*[=:]\s*(?:provisional|research_only)\b", text, re.IGNORECASE):
                invalid.append(path.relative_to(REPO_ROOT).as_posix())
            first_lines = "\n".join(text.splitlines()[:6])
            if "document_status=" in first_lines and "document_maturity=provisional" in first_lines:
                header_count += 1
        self.assertEqual(invalid, [])
        self.assertGreaterEqual(header_count, 49)

        report = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("document_maturity: provisional", report)
        self.assertIn("案例状态轴", report)

    def test_historical_summary_blocks_have_gate_result(self):
        allowed_gates = {"pass", "conditional", "observation_only", "valid_no_trade", "pending"}
        for relative_path, expected_gate in HISTORICAL_SUMMARY_GATES.items():
            block = first_contract_block((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
            self.assertIn(field(block, "direction"), {"long", "short", "no_valid_direction"}, relative_path)
            self.assertIn(field(block, "research_state"), {
                "pattern_like", "research_candidate", "research_positive_conditional",
                "observation_only", "valid_no_trade", "failed_thesis", "pending",
            }, relative_path)
            self.assertEqual(field(block, "trade_state"), "not_authorized", relative_path)
            self.assertEqual(field(block, "gate_result"), expected_gate, relative_path)
            self.assertEqual(field(block, "handoff_status"), "research_only", relative_path)
            self.assertIn(expected_gate, allowed_gates)

    def test_h3_l3_attempt_direction_does_not_replace_canonical_direction(self):
        path = REPO_ROOT / "patterns" / "08_three_push_h3_l3" / "README.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("attempt_direction: bullish_attempts / bearish_attempts", text)
        self.assertIsNone(re.search(r"(?m)^direction:\s*bullish_attempts\s*/\s*bearish_attempts\s*$", text))
        self.assertIn("canonical `direction`", text)
        for token in (
            "timeframes_seen:",
            "daily_context_window:",
            "lineage_status: same_lineage / reset / unclear / pending",
            "event_bucket:",
            "space_status:",
            "trade_state:",
            "gate_result:",
            "handoff_status:",
        ):
            self.assertIn(token, text, token)

    def test_shared_hl_lineage_ledger_uses_canonical_state_names(self):
        text = (REPO_ROOT / "research" / "h_l_lineage_visual_boundary_audit_2026-08-24_CN.md").read_text(encoding="utf-8")
        self.assertIn("parent_state: open_trend / trading_range / range_edge / transition / climax / unclear", text)
        self.assertIn("lineage_status: same_lineage / reset / unclear / pending", text)
        self.assertIn("lineage_id:", text)
        self.assertNotIn("lineage_status: same-lineage / reset / unclear", text)

    def test_bop_protocol_uses_current_primary_pattern_and_state_axes(self):
        path = REPO_ROOT / "research" / "bop_multiday_pullback_candidate_audit_2026-08-24_CN.md"
        block = first_contract_block(path.read_text(encoding="utf-8"))
        self.assertEqual(field(block, "primary_pattern"), "BOP / other")
        self.assertIn("candidate_class:", block)
        self.assertIn("parent_state:", block)
        self.assertIn("timeframes_seen:", block)
        self.assertIn("lineage_status:", block)
        self.assertIn("event_bucket:", block)
        self.assertIn("space_status:", block)
        self.assertIn("research_state:", block)
        self.assertIn("gate_result:", block)
        self.assertIn("handoff_status:", block)

    def test_index_validator_and_audit_preserve_scope_and_pre_entry_boundaries(self):
        readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(encoding="utf-8")
        report = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("unified_output_state_axis_audit_2026-08-29_CN.md", readme)
        self.assertIn("unified_output_state_axis_audit_2026-08-29_CN.md", validator)
        for token in (
            "document_maturity",
            "Daily",
            "4H",
            "15m",
            "lineage_id",
            "event_bucket",
            "space_status",
            "no-new-positive",
            "validated win-rate: not-computable",
            "不修改 Codex Trading",
            "不创建量化扫描器",
            "不连接 Execution Agent",
        ):
            self.assertIn(token, report, token)


if __name__ == "__main__":
    unittest.main()
