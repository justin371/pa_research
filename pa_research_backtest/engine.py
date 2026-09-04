"""A small, auditable backtesting.py adapter for PA Research.

This module deliberately does not discover symbols or identify chart patterns.
It replays contracts that a human has already frozen from a chart review.  The
separation is important: a chart label such as H1 or strong A is evidence from
the research record, not a label inferred by this program.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import math
import os
import platform
import re
import sys
import warnings
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Iterable, Mapping

import backtesting
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

from pa_source_binding import require_source_snapshot, verify_source_snapshot


ENGINE_VERSION = "0.3.15"
SUPPORTED_DIRECTIONS = {"long", "short"}
SUPPORTED_PATTERNS = {"ABC_CONT", "BOP", "H1_L1", "H2_L2", "H3_L3", "RFB", "MTR", "other"}
SUPPORTED_LABELS = {"H1", "H2", "L1", "L2", "H3", "L3", "none", "pending"}
H_L_LABELS = {"H1", "H2", "L1", "L2"}
THIRD_PUSH_LABELS = {"H3", "L3"}
SUPPORTED_EMA_SLOPES = {"up", "flat", "down", "unknown"}
SUPPORTED_SPACE_STATUSES = {
    "strict_ge_1R",
    "borderline_ge_1R",
    "clearly_positive",
    "borderline",
    "blocked",
    "unknown",
}
SUPPORTED_H_L_EMA_GATES = {
    "long_pass",
    "short_pass",
    "fail_flat_or_opposite",
    "pending",
    "not_applicable",
}
SUPPORTED_META_CONFLUENCE = {"present", "absent", "unknown"}
SUPPORTED_ORDER_BRANCHES = {"stop_confirmation", "limit_retest", "market_close"}
SUPPORTED_GAP_POLICIES = {"accept_open", "skip", "flag_only", "not_applicable"}
TRADE_RESULTS = {"win", "loss", "scratch"}
COMPLETED_PATH_RESULTS = {"target-reached", "first-obstacle-reached", "invalidated", "time_exit"}

REQUIRED_CONTRACT_COLUMNS = {
    "sample_id",
    "symbol",
    "decision_date",
    "direction",
    "primary_pattern",
    "internal_label",
    "order_branch",
    "entry_trigger",
    "structural_stop",
    "first_obstacle",
    "target_price",
    "max_hold_bars",
    "gap_policy",
    "label_source",
    "daily_context_window",
    "major_high_low_review",
    "ema20_50_200_review",
    "event_context",
    "contract_frozen",
    "lineage_id",
}

PRICE_COLUMNS = {"Date", "Open", "High", "Low", "Close", "Volume", "Symbol"}
PRICE_COLUMN_ALIASES = {
    "date": "Date",
    "datetime": "Date",
    "timestamp": "Date",
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
    "symbol": "Symbol",
    "ticker": "Symbol",
}


class ContractValidationError(ValueError):
    """Raised when a manually frozen contract is not auditable."""


@dataclass(frozen=True)
class BacktestContract:
    """The minimum pre-outcome contract accepted by the replay engine."""

    sample_id: str
    symbol: str
    decision_date: pd.Timestamp
    direction: str
    primary_pattern: str
    internal_label: str
    order_branch: str
    entry_trigger: float | None
    structural_stop: float
    first_obstacle: float
    target_price: float
    max_hold_bars: int
    gap_policy: str
    label_source: str
    daily_context_window: str
    major_high_low_review: str
    ema20_50_200_review: str
    event_context: str
    contract_frozen: str
    lineage_id: str = ""
    market_context_id: str = ""
    daily_ema20_slope: str = ""
    daily_ema50_slope: str = ""
    h_l_ema_slope_gate: str = ""
    h_l_pullback_location: str = ""
    meta_confluence: str = ""
    meta_zone: str = ""
    meta_components: str = ""
    pre_entry_space_R: float | None = None
    space_status: str = ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "BacktestContract":
        raw_internal_label = _as_string(row.get("internal_label")).upper()
        internal_label = {"NONE": "none", "PENDING": "pending"}.get(raw_internal_label, raw_internal_label)
        raw_primary_pattern = _as_string(row.get("primary_pattern")).upper()
        primary_pattern = "other" if raw_primary_pattern == "OTHER" else raw_primary_pattern
        return cls(
            sample_id=_as_string(row.get("sample_id")),
            symbol=_normalise_symbol(row.get("symbol")),
            decision_date=_parse_date(row.get("decision_date"), "decision_date"),
            direction=_as_string(row.get("direction")).lower(),
            primary_pattern=primary_pattern,
            internal_label=internal_label,
            order_branch=_as_string(row.get("order_branch")).lower(),
            entry_trigger=_parse_optional_float(row.get("entry_trigger"), "entry_trigger"),
            structural_stop=_parse_float(row.get("structural_stop"), "structural_stop"),
            first_obstacle=_parse_float(row.get("first_obstacle"), "first_obstacle"),
            target_price=_parse_float(row.get("target_price"), "target_price"),
            max_hold_bars=_parse_int(row.get("max_hold_bars"), "max_hold_bars"),
            gap_policy=_as_string(row.get("gap_policy")).lower(),
            label_source=_as_string(row.get("label_source")).lower(),
            daily_context_window=_as_string(row.get("daily_context_window")).lower(),
            major_high_low_review=_as_string(row.get("major_high_low_review")).lower(),
            ema20_50_200_review=_as_string(row.get("ema20_50_200_review")).lower(),
            event_context=_as_string(row.get("event_context")).lower(),
            contract_frozen=_as_string(row.get("contract_frozen")).lower(),
            lineage_id=_as_string(row.get("lineage_id")),
            market_context_id=_as_string(row.get("market_context_id")),
            daily_ema20_slope=_as_string(row.get("daily_ema20_slope")).lower(),
            daily_ema50_slope=_as_string(row.get("daily_ema50_slope")).lower(),
            h_l_ema_slope_gate=_as_string(row.get("h_l_ema_slope_gate")).lower(),
            h_l_pullback_location=_as_string(row.get("h_l_pullback_location")),
            meta_confluence=_as_string(row.get("meta_confluence")).lower(),
            meta_zone=_as_string(row.get("meta_zone")),
            meta_components=_as_string(row.get("meta_components")),
            pre_entry_space_R=_parse_optional_float(row.get("pre_entry_space_R"), "pre_entry_space_R"),
            space_status=_normalise_space_status(row.get("space_status")),
        )

    def as_record(self) -> dict[str, Any]:
        record = asdict(self)
        record["decision_date"] = self.decision_date.strftime("%Y-%m-%d")
        return record


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    try:
        result = pd.isna(value)
    except (TypeError, ValueError):
        return False
    return bool(result) if isinstance(result, (bool, np.bool_)) else False


def _as_string(value: Any) -> str:
    return "" if _is_missing(value) else str(value).strip()


def _normalise_symbol(value: Any) -> str:
    return _as_string(value).upper()


def _is_finite_numeric(value: Any) -> bool:
    if isinstance(value, (bool, np.bool_)):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError, OverflowError):
        return False


def _parse_date(value: Any, field: str) -> pd.Timestamp:
    if _is_missing(value):
        raise ContractValidationError(f"{field} is required")
    try:
        timestamp = pd.Timestamp(value)
    except (TypeError, ValueError) as exc:
        raise ContractValidationError(f"{field} is not a valid date: {value!r}") from exc
    if timestamp.tzinfo is not None:
        timestamp = timestamp.tz_localize(None)
    return timestamp.normalize()


def _parse_float(value: Any, field: str) -> float:
    if _is_missing(value) or _as_string(value) == "":
        raise ContractValidationError(f"{field} is required")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ContractValidationError(f"{field} must be numeric: {value!r}") from exc
    if not math.isfinite(parsed):
        raise ContractValidationError(f"{field} must be finite: {value!r}")
    return parsed


def _parse_optional_float(value: Any, field: str) -> float | None:
    if _is_missing(value) or _as_string(value) == "":
        return None
    return _parse_float(value, field)


def _parse_int(value: Any, field: str) -> int:
    parsed = _parse_float(value, field)
    if parsed != int(parsed):
        raise ContractValidationError(f"{field} must be an integer: {value!r}")
    return int(parsed)


def _meta_component_names(value: str) -> list[str]:
    return [
        item.strip().lower()
        for item in re.split(r"[;,|+]", value)
        if item.strip()
    ]


def _event_bucket(event_context: str) -> str:
    """Classify raw event evidence conservatively for summary stratification."""

    context = _as_string(event_context).lower()
    # Non-event clearance is an explicit token, not a substring. In
    # particular, `earnings_filter_passed=false` must never grant clearance.
    tokens = {token.strip() for token in re.split(r"[;|]", context) if token.strip()}
    clearance_pattern = re.compile(
        r"(?:ordinary_non_event|earnings_filter_passed(?:_reaudit)?|"
        r"no_event_inside_a_b_or_10bar_horizon|outside_10bar_horizon|"
        r"outside_a_b_and_10bar_horizon|setup_window_no_known_event)(?:=true)?"
    )
    clearance_markers = (
        "ordinary_non_event", "earnings_filter_passed", "no_event_inside",
        "outside_10bar_horizon", "outside_a_b_and_10bar_horizon", "setup_window_no_known_event",
    )
    if any(
        any(marker in token for marker in clearance_markers)
        and clearance_pattern.fullmatch(token) is None
        for token in tokens
    ):
        return "event_unverified_or_pending"
    if re.search(
        r"historical_event_filter_not_verified|event_context_pending|"
        r"sector_context_pending|public_price_reaudit",
        context,
    ):
        return "event_unverified_or_pending"
    if re.search(r"event_driven|earnings[-_]driven|aftershock", context):
        return "event_driven"
    if "earnings_adjacent" in context:
        return "earnings_adjacent"
    if tokens.intersection({"ordinary_non_event", "ordinary_non_event=true"}) and "gap_reprice" not in context:
        return "ordinary_non_event"
    if any(clearance_pattern.fullmatch(token) and not token.startswith("ordinary_non_event") for token in tokens):
        return "event_reviewed_non_event"
    if context == "none":
        return "unknown"
    return "other_unclassified"


def _normalise_space_status(value: Any) -> str:
    raw = _as_string(value).lower()
    for status in SUPPORTED_SPACE_STATUSES:
        if status.lower() == raw:
            return status
    return raw


def _contract_space_bucket(space_status: str, pre_entry_space_r: float | None) -> str:
    """Return only the pre-entry space evidence explicitly frozen in the contract."""

    status = _as_string(space_status).lower()
    if status in {"strict_ge_1r", "clearly_positive"}:
        return "strict_ge_1R"
    if status in {"borderline_ge_1r", "borderline"}:
        return "borderline"
    if status == "blocked":
        return "blocked"
    if status == "unknown":
        return "unknown_contract_space"
    if pre_entry_space_r is not None and not _is_missing(pre_entry_space_r):
        return "numeric_only"
    return "unknown_contract_space"


def _contract_eligibility(contract: BacktestContract) -> str:
    """Return the research replay status implied by the frozen H/L gate."""

    if contract.internal_label == "pending":
        return "pending"
    if contract.internal_label not in H_L_LABELS:
        return "eligible"
    if contract.h_l_ema_slope_gate in {"long_pass", "short_pass"}:
        return "eligible"
    if contract.h_l_ema_slope_gate == "fail_flat_or_opposite":
        return "observation_only"
    return "pending"


def _result_contract_eligibility(internal_label: Any, ema_gate: Any) -> str:
    """Derive result eligibility from the pre-entry H/L gate, never from outcome fields."""

    label = _as_string(internal_label).upper()
    gate = _as_string(ema_gate).lower()
    if label == "PENDING":
        return "pending"
    if label not in H_L_LABELS:
        return "eligible"
    expected_gate = "long_pass" if label in {"H1", "H2"} else "short_pass"
    if gate == expected_gate:
        return "eligible"
    if gate == "fail_flat_or_opposite":
        return "observation_only"
    return "pending"


def _result_text_series(frame: pd.DataFrame, column: str) -> pd.Series:
    """Return a trimmed text column without treating missing evidence as valid."""

    if column not in frame:
        return pd.Series("", index=frame.index, dtype="object")
    return frame[column].fillna("").astype(str).str.strip()


def _pre_entry_provenance(frame: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Classify whether a result row still carries the required pre-entry evidence."""

    required_fields = (
        "sample_id",
        "symbol",
        "decision_date",
        "direction",
        "primary_pattern",
        "internal_label",
        "order_branch",
        "structural_stop",
        "first_obstacle",
        "target_price",
        "max_hold_bars",
        "gap_policy",
        "label_source",
        "daily_context_window",
        "major_high_low_review",
        "ema20_50_200_review",
        "event_context",
        "contract_frozen",
        "lineage_id",
    )
    missing_by_row: list[list[str]] = [[] for _ in range(len(frame))]

    def mark(field: str, condition: pd.Series) -> None:
        for position, flagged in enumerate(condition.tolist()):
            if bool(flagged) and field not in missing_by_row[position]:
                missing_by_row[position].append(field)

    for field in required_fields:
        mark(field, _result_text_series(frame, field).eq(""))
    mark("contract_frozen", _result_text_series(frame, "contract_frozen").str.lower().ne("yes"))
    order_branches = _result_text_series(frame, "order_branch").str.lower()
    mark(
        "planned_entry_trigger",
        order_branches.ne("market_close")
        & _result_text_series(frame, "planned_entry_trigger").eq(""),
    )

    labels = _result_text_series(frame, "internal_label").str.upper()
    directions = _result_text_series(frame, "direction").str.lower()
    h_l_rows = labels.isin(H_L_LABELS)
    mark("direction", h_l_rows & labels.isin({"H1", "H2"}) & directions.ne("long"))
    mark("direction", h_l_rows & labels.isin({"L1", "L2"}) & directions.ne("short"))

    for field in (
        "daily_ema20_slope",
        "daily_ema50_slope",
        "h_l_ema_slope_gate",
        "h_l_pullback_location",
        "meta_confluence",
    ):
        mark(field, h_l_rows & _result_text_series(frame, field).eq(""))
    for field in ("daily_ema20_slope", "daily_ema50_slope"):
        mark(
            field,
            h_l_rows
            & ~_result_text_series(frame, field).str.lower().isin(SUPPORTED_EMA_SLOPES),
        )
    ema_gate = _result_text_series(frame, "h_l_ema_slope_gate").str.lower()
    mark(
        "h_l_ema_slope_gate",
        h_l_rows & ~ema_gate.isin(SUPPORTED_H_L_EMA_GATES - {"not_applicable"}),
    )
    meta_confluence = _result_text_series(frame, "meta_confluence").str.lower()
    mark(
        "meta_confluence",
        h_l_rows & ~meta_confluence.isin(SUPPORTED_META_CONFLUENCE),
    )
    mark(
        "meta_zone",
        h_l_rows
        & meta_confluence.eq("present")
        & _result_text_series(frame, "meta_zone").eq(""),
    )
    mark(
        "meta_components",
        h_l_rows
        & meta_confluence.eq("present")
        & _result_text_series(frame, "meta_components").eq(""),
    )

    space_status = _result_text_series(frame, "space_status").str.lower()
    valid_space_statuses = {item.lower() for item in SUPPORTED_SPACE_STATUSES}
    mark("space_status", space_status.ne("") & ~space_status.isin(valid_space_statuses))
    space_value = pd.to_numeric(_result_text_series(frame, "pre_entry_space_R"), errors="coerce")
    strict_space = space_status.isin({"strict_ge_1r", "clearly_positive"})
    mark("pre_entry_space_R", strict_space & space_value.isna())
    mark("pre_entry_space_R", strict_space & space_value.notna() & space_value.lt(1))
    mark("pre_entry_space_R", space_status.eq("blocked") & space_value.isna())
    mark("pre_entry_space_R", space_status.eq("blocked") & space_value.gt(0))

    # Non-empty text is not proof of a valid frozen contract. Reuse the same
    # loader/contract rules for imported results (e.g. >=2y, complete visual
    # review, finite prices, and slope/pass agreement), rather than maintaining
    # a weaker second schema for statistics. Preserve specific missing-field
    # diagnostics already collected above.
    for position, record in enumerate(frame.to_dict(orient="records")):
        if missing_by_row[position]:
            continue
        contract_record = dict(record, entry_trigger=record.get("planned_entry_trigger"))
        try:
            contract = BacktestContract.from_row(contract_record)
            validate_contract(
                contract,
                entry_reference=contract.entry_trigger if contract.order_branch != "market_close" else None,
            )
            if record.get("fill_status") == "filled":
                actual_entry = record.get("entry_price")
                if isinstance(actual_entry, (bool, np.bool_)):
                    raise ValueError("entry price must be numeric, not boolean")
                validate_contract(contract, entry_reference=float(actual_entry))
        except (ContractValidationError, TypeError, ValueError, OverflowError):
            missing_by_row[position].append("invalid_frozen_contract")

    missing_fields = pd.Series(
        [";".join(fields) for fields in missing_by_row],
        index=frame.index,
        dtype="object",
    )
    status = missing_fields.map(lambda value: "incomplete" if value else "complete")
    return status, missing_fields


def _normalise_date_index(index: Any) -> pd.Timestamp:
    timestamp = pd.Timestamp(index)
    if timestamp.tzinfo is not None:
        timestamp = timestamp.tz_localize(None)
    return timestamp.normalize()


def validate_contract(contract: BacktestContract, entry_reference: float | None = None) -> None:
    errors: list[str] = []
    if not contract.sample_id:
        errors.append("sample_id is required")
    if not contract.symbol:
        errors.append("symbol is required")
    if contract.direction not in SUPPORTED_DIRECTIONS:
        errors.append(f"direction must be one of {sorted(SUPPORTED_DIRECTIONS)}")
    if contract.primary_pattern not in SUPPORTED_PATTERNS:
        errors.append(f"primary_pattern must be one of {sorted(SUPPORTED_PATTERNS)}")
    if contract.internal_label not in SUPPORTED_LABELS:
        errors.append(f"internal_label must be one of {sorted(SUPPORTED_LABELS)}")
    if contract.internal_label == "pending":
        errors.append("frozen replay contracts cannot use internal_label=pending")
    if contract.order_branch not in SUPPORTED_ORDER_BRANCHES:
        errors.append(f"order_branch must be one of {sorted(SUPPORTED_ORDER_BRANCHES)}")
    if contract.order_branch != "market_close" and contract.entry_trigger is None:
        errors.append("entry_trigger is required for stop_confirmation and limit_retest")
    if contract.order_branch == "market_close" and contract.gap_policy != "not_applicable":
        errors.append("market_close requires gap_policy=not_applicable")
    if contract.order_branch != "market_close" and contract.gap_policy not in SUPPORTED_GAP_POLICIES - {"not_applicable"}:
        errors.append(f"gap_policy must be one of {sorted(SUPPORTED_GAP_POLICIES - {'not_applicable'})}")
    finite_numeric_fields: set[str] = set()
    for field_name, value in (
        ("structural_stop", contract.structural_stop),
        ("first_obstacle", contract.first_obstacle),
        ("target_price", contract.target_price),
    ):
        if _is_finite_numeric(value):
            finite_numeric_fields.add(field_name)
        else:
            errors.append(f"{field_name} must be finite")
    if contract.entry_trigger is not None:
        if _is_finite_numeric(contract.entry_trigger):
            finite_numeric_fields.add("entry_trigger")
        else:
            errors.append("entry_trigger must be finite")
    if contract.pre_entry_space_R is not None:
        if _is_finite_numeric(contract.pre_entry_space_R):
            finite_numeric_fields.add("pre_entry_space_R")
        else:
            errors.append("pre_entry_space_R must be finite")
    max_hold_bars_valid = isinstance(contract.max_hold_bars, (int, np.integer)) and not isinstance(
        contract.max_hold_bars, (bool, np.bool_)
    )
    if not max_hold_bars_valid:
        errors.append("max_hold_bars must be an integer")
    elif contract.max_hold_bars < 1:
        errors.append("max_hold_bars must be at least 1")
    if contract.label_source != "human_chart_review":
        errors.append("label_source must be human_chart_review")
    if contract.daily_context_window != ">=2y":
        errors.append("daily_context_window must be >=2y")
    if contract.major_high_low_review != "complete":
        errors.append("major_high_low_review must be complete")
    if contract.ema20_50_200_review != "complete":
        errors.append("ema20_50_200_review must be complete")
    if not contract.event_context:
        errors.append("event_context is required; use none when no event is known")
    if contract.contract_frozen != "yes":
        errors.append("contract_frozen must be yes")
    if not contract.lineage_id:
        errors.append("lineage_id is required for dependence control")
    space_status = _as_string(contract.space_status).lower()
    if space_status and space_status not in {item.lower() for item in SUPPORTED_SPACE_STATUSES}:
        errors.append(f"space_status must be one of {sorted(SUPPORTED_SPACE_STATUSES)}")
    if space_status in {"strict_ge_1r", "clearly_positive"}:
        if contract.pre_entry_space_R is None:
            errors.append("strict space_status requires pre_entry_space_R")
        elif "pre_entry_space_R" in finite_numeric_fields and contract.pre_entry_space_R < 1:
            errors.append("strict space_status requires pre_entry_space_R >= 1")
    if space_status == "blocked":
        if contract.pre_entry_space_R is None:
            errors.append("blocked space_status requires pre_entry_space_R")
        elif "pre_entry_space_R" in finite_numeric_fields and contract.pre_entry_space_R > 0:
            errors.append("blocked space_status requires pre_entry_space_R <= 0")

    if contract.internal_label == "H3_L3":
        errors.append("internal_label H3_L3 is ambiguous; use H3 or L3")
    if contract.internal_label == "H3" and contract.direction != "long":
        errors.append("H3 contracts must have direction=long")
    if contract.internal_label == "L3" and contract.direction != "short":
        errors.append("L3 contracts must have direction=short")
    if contract.internal_label in THIRD_PUSH_LABELS:
        if contract.primary_pattern != "H3_L3":
            errors.append("H3/L3 contracts must have primary_pattern=H3_L3")
        if contract.h_l_ema_slope_gate != "not_applicable":
            errors.append("H3/L3 contracts require h_l_ema_slope_gate=not_applicable")
    if contract.primary_pattern == "H3_L3" and contract.internal_label not in THIRD_PUSH_LABELS:
        errors.append("primary_pattern H3_L3 requires internal_label H3 or L3")
    if contract.primary_pattern == "H1_L1" and contract.internal_label not in {"H1", "L1"}:
        errors.append("primary_pattern H1_L1 requires internal_label H1 or L1")
    if contract.primary_pattern == "H2_L2" and contract.internal_label not in {"H2", "L2"}:
        errors.append("primary_pattern H2_L2 requires internal_label H2 or L2")
    if contract.primary_pattern == "BOP" and contract.internal_label in H_L_LABELS | THIRD_PUSH_LABELS:
        errors.append("BOP contracts cannot use H/L or H3/L3 as internal_label; keep them in secondary_context")

    for field_name, slope in (
        ("daily_ema20_slope", contract.daily_ema20_slope),
        ("daily_ema50_slope", contract.daily_ema50_slope),
    ):
        if slope and slope not in SUPPORTED_EMA_SLOPES:
            errors.append(f"{field_name} must be one of {sorted(SUPPORTED_EMA_SLOPES)}")
    if contract.h_l_ema_slope_gate and contract.h_l_ema_slope_gate not in SUPPORTED_H_L_EMA_GATES:
        errors.append(
            "h_l_ema_slope_gate must be one of "
            f"{sorted(SUPPORTED_H_L_EMA_GATES)}"
        )
    if contract.meta_confluence and contract.meta_confluence not in SUPPORTED_META_CONFLUENCE:
        errors.append(f"meta_confluence must be one of {sorted(SUPPORTED_META_CONFLUENCE)}")
    if contract.meta_confluence == "present":
        if not contract.meta_zone:
            errors.append("meta_zone is required when meta_confluence=present")
        if len(set(_meta_component_names(contract.meta_components))) < 2:
            errors.append(
                "meta_components must name at least two independent sources "
                "when meta_confluence=present"
            )

    if contract.internal_label in H_L_LABELS:
        if contract.internal_label in {"H1", "H2"} and contract.direction != "long":
            errors.append("H1/H2 contracts must have direction=long")
        if contract.internal_label in {"L1", "L2"} and contract.direction != "short":
            errors.append("L1/L2 contracts must have direction=short")
        if not contract.daily_ema20_slope:
            errors.append("daily_ema20_slope is required for H1/H2/L1/L2")
        if not contract.daily_ema50_slope:
            errors.append("daily_ema50_slope is required for H1/H2/L1/L2")
        if not contract.h_l_ema_slope_gate:
            errors.append("h_l_ema_slope_gate is required for H1/H2/L1/L2")
        if contract.h_l_ema_slope_gate == "not_applicable":
            errors.append("H1/H2/L1/L2 cannot use h_l_ema_slope_gate=not_applicable")
        if not contract.h_l_pullback_location:
            errors.append("h_l_pullback_location is required for H1/H2/L1/L2")
        if not contract.meta_confluence:
            errors.append("meta_confluence is required for H1/H2/L1/L2")

        long_label = contract.internal_label in {"H1", "H2"}
        expected_pass = "long_pass" if long_label else "short_pass"
        expected_slope = "up" if long_label else "down"
        if contract.h_l_ema_slope_gate in {"long_pass", "short_pass"}:
            if contract.h_l_ema_slope_gate != expected_pass:
                errors.append(f"{contract.internal_label} requires {expected_pass}")
        if contract.h_l_ema_slope_gate == expected_pass:
            if (
                contract.daily_ema20_slope != expected_slope
                or contract.daily_ema50_slope != expected_slope
            ):
                errors.append(
                    f"{expected_pass} requires both Daily EMA20 and EMA50 slope={expected_slope}"
                )
        elif contract.h_l_ema_slope_gate == "fail_flat_or_opposite":
            if "unknown" in {contract.daily_ema20_slope, contract.daily_ema50_slope}:
                errors.append(
                    "unknown EMA slope must use h_l_ema_slope_gate=pending, "
                    "not fail_flat_or_opposite"
                )
            if (
                contract.daily_ema20_slope == expected_slope
                and contract.daily_ema50_slope == expected_slope
            ):
                errors.append(
                    "fail_flat_or_opposite requires at least one EMA20/EMA50 slope "
                    "to be flat or opposite"
                )
        elif contract.h_l_ema_slope_gate not in {"pending", "long_pass", "short_pass"}:
            errors.append(
                f"{contract.internal_label} requires {expected_pass}, "
                "fail_flat_or_opposite, or pending"
            )
    elif contract.h_l_ema_slope_gate not in {"", "not_applicable"}:
        errors.append(
            "h_l_ema_slope_gate is only applicable to internal_label H1/H2/L1/L2 "
            "or must be not_applicable"
        )

    if entry_reference is not None and not _is_finite_numeric(entry_reference):
        errors.append("entry reference must be finite")
    if entry_reference is not None and _is_finite_numeric(entry_reference):
        if contract.direction == "long":
            if "structural_stop" in finite_numeric_fields and contract.structural_stop >= entry_reference:
                errors.append("long structural_stop must be below the entry reference")
            if "first_obstacle" in finite_numeric_fields and contract.first_obstacle <= entry_reference:
                errors.append("long first_obstacle must be above the entry reference")
            if "target_price" in finite_numeric_fields and contract.target_price <= entry_reference:
                errors.append("long target_price must be above the entry reference")
        elif contract.direction == "short":
            if "structural_stop" in finite_numeric_fields and contract.structural_stop <= entry_reference:
                errors.append("short structural_stop must be above the entry reference")
            if "first_obstacle" in finite_numeric_fields and contract.first_obstacle >= entry_reference:
                errors.append("short first_obstacle must be below the entry reference")
            if "target_price" in finite_numeric_fields and contract.target_price >= entry_reference:
                errors.append("short target_price must be below the entry reference")

    if errors:
        raise ContractValidationError(f"{contract.sample_id or '<unknown>'}: " + "; ".join(errors))


def _normalise_price_columns(frame: pd.DataFrame) -> pd.DataFrame:
    rename: dict[str, str] = {}
    for column in frame.columns:
        key = str(column).strip().lower().replace(" ", "_")
        canonical = PRICE_COLUMN_ALIASES.get(key)
        if canonical:
            rename[column] = canonical
    frame = frame.rename(columns=rename)
    duplicates = [column for column in PRICE_COLUMNS if list(frame.columns).count(column) > 1]
    if duplicates:
        raise ValueError(f"duplicate price columns after normalization: {sorted(set(duplicates))}")
    return frame


def load_prices(path: str | Path, default_symbol: str | None = None) -> pd.DataFrame:
    """Load a combined or single-symbol OHLCV CSV for the replay engine."""

    try:
        frame = _normalise_price_columns(pd.read_csv(path))
    except pd.errors.EmptyDataError as exc:
        raise ValueError("price CSV contains no rows or columns") from exc
    required = {"Date", "Open", "High", "Low", "Close"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"price CSV is missing required columns: {missing}")
    if "Symbol" not in frame.columns:
        if not default_symbol:
            raise ValueError("price CSV has no Symbol column; pass --symbol for a single-symbol file")
        frame["Symbol"] = _normalise_symbol(default_symbol)
    else:
        frame["Symbol"] = frame["Symbol"].map(_normalise_symbol)
    if frame["Symbol"].eq("").any():
        raise ValueError("price CSV contains an empty Symbol")

    try:
        frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
        if frame["Date"].dt.tz is not None:
            frame["Date"] = frame["Date"].dt.tz_localize(None)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("price CSV contains invalid or mixed-timezone Date values") from exc
    if frame["Date"].isna().any():
        raise ValueError("price CSV contains an invalid Date")
    for column in ("Open", "High", "Low", "Close"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if "Volume" not in frame.columns:
        frame["Volume"] = 0.0
    else:
        # Only an absent optional column gets the neutral default. A present
        # malformed/missing observation must fail the finite-data check below.
        frame["Volume"] = pd.to_numeric(frame["Volume"], errors="coerce")

    if frame[["Open", "High", "Low", "Close"]].isna().any().any():
        raise ValueError("price CSV contains a missing or non-numeric OHLC value")
    if not np.isfinite(frame[["Open", "High", "Low", "Close", "Volume"]].to_numpy(dtype=float)).all():
        raise ValueError("price CSV contains a non-finite OHLCV value")
    invalid_ohlc = (
        (frame[["Open", "High", "Low", "Close"]] <= 0).any(axis=1)
        | (frame["High"] < frame[["Open", "Close", "Low"]].max(axis=1))
        | (frame["Low"] > frame[["Open", "Close", "High"]].min(axis=1))
        | (frame["High"] < frame["Low"])
        | (frame["Volume"] < 0)
    )
    if invalid_ohlc.any():
        bad_rows = frame.index[invalid_ohlc].tolist()[:5]
        raise ValueError(f"price CSV contains invalid OHLCV rows at source rows {bad_rows}")

    frame["Date"] = frame["Date"].dt.normalize()
    duplicate_mask = frame.duplicated(subset=["Symbol", "Date"], keep=False)
    if duplicate_mask.any():
        raise ValueError("price CSV contains duplicate Symbol/Date rows")
    return frame.sort_values(["Symbol", "Date"]).set_index("Date")


def load_contracts(path: str | Path) -> list[BacktestContract]:
    """Load and validate the pre-outcome contract CSV."""

    try:
        frame = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ContractValidationError("contract CSV contains no rows or columns") from exc
    frame.columns = [str(column).strip() for column in frame.columns]
    missing = sorted(REQUIRED_CONTRACT_COLUMNS - set(frame.columns))
    if missing:
        raise ContractValidationError(f"contract CSV is missing required columns: {missing}")
    contracts: list[BacktestContract] = []
    seen_ids: set[str] = set()
    seen_contract_families: set[tuple[str, str, str, str, str, str]] = set()
    for row_number, row in enumerate(frame.to_dict(orient="records"), start=2):
        try:
            contract = BacktestContract.from_row(row)
            validate_contract(contract)
        except ContractValidationError as exc:
            raise ContractValidationError(f"contract CSV row {row_number}: {exc}") from exc
        sample_identity = contract.sample_id.casefold()
        if sample_identity in seen_ids:
            raise ContractValidationError(f"duplicate sample_id: {contract.sample_id}")
        contract_family = (
            contract.symbol,
            contract.decision_date.strftime("%Y-%m-%d"),
            contract.direction,
            contract.primary_pattern,
            contract.internal_label,
            contract.lineage_id.casefold(),
        )
        if contract_family in seen_contract_families:
            raise ContractValidationError(
                "duplicate contract family (same symbol/date/direction/pattern/label/lineage); "
                "choose one order branch before replay: "
                f"{contract.symbol}/{contract.decision_date.strftime('%Y-%m-%d')}/"
                f"{contract.primary_pattern}/{contract.internal_label}/{contract.lineage_id}"
            )
        seen_ids.add(sample_identity)
        seen_contract_families.add(contract_family)
        contracts.append(contract)
    if not contracts:
        raise ContractValidationError("contract CSV contains no rows")
    return contracts


def _first_entry_opportunity(prices: pd.DataFrame, contract: BacktestContract) -> dict[str, Any] | None:
    if contract.order_branch == "market_close":
        return {"date": contract.decision_date, "gap_through": False}
    assert contract.entry_trigger is not None
    future = prices.loc[prices.index > contract.decision_date]
    for date, row in future.iterrows():
        trigger = contract.entry_trigger
        if contract.order_branch == "stop_confirmation":
            touched = row["High"] >= trigger if contract.direction == "long" else row["Low"] <= trigger
            gap_through = row["Open"] > trigger if contract.direction == "long" else row["Open"] < trigger
        else:
            touched = row["Low"] <= trigger if contract.direction == "long" else row["High"] >= trigger
            gap_through = row["Open"] < trigger if contract.direction == "long" else row["Open"] > trigger
        if touched:
            return {"date": _normalise_date_index(date), "gap_through": bool(gap_through)}
    return None


def _base_result(contract: BacktestContract, *, fill_status: str, reason: str) -> dict[str, Any]:
    eligibility = _contract_eligibility(contract)
    if eligibility == "observation_only":
        evidence_status = "observation_only"
    elif fill_status == "unproven":
        evidence_status = "excluded"
    else:
        evidence_status = "not-a-trade"
    return {
        "engine_version": ENGINE_VERSION,
        "backtesting_version": getattr(backtesting, "__version__", "unknown"),
        "sample_id": contract.sample_id,
        "symbol": contract.symbol,
        "decision_date": contract.decision_date.strftime("%Y-%m-%d"),
        "direction": contract.direction,
        "primary_pattern": contract.primary_pattern,
        "internal_label": contract.internal_label,
        "lineage_id": contract.lineage_id,
        "daily_ema20_slope": contract.daily_ema20_slope,
        "daily_ema50_slope": contract.daily_ema50_slope,
        "h_l_ema_slope_gate": contract.h_l_ema_slope_gate,
        "h_l_pullback_location": contract.h_l_pullback_location,
        "meta_confluence": contract.meta_confluence,
        "meta_zone": contract.meta_zone,
        "meta_components": contract.meta_components,
        "pre_entry_space_R": contract.pre_entry_space_R,
        "space_status": contract.space_status,
        "contract_space_bucket": _contract_space_bucket(contract.space_status, contract.pre_entry_space_R),
        "event_bucket": _event_bucket(contract.event_context),
        "contract_eligibility": eligibility,
        "pre_entry_provenance_status": "complete",
        "pre_entry_provenance_missing_fields": "",
        "order_branch": contract.order_branch,
        "event_context": contract.event_context,
        "label_source": contract.label_source,
        "daily_context_window": contract.daily_context_window,
        "major_high_low_review": contract.major_high_low_review,
        "ema20_50_200_review": contract.ema20_50_200_review,
        "contract_frozen": contract.contract_frozen,
        "market_context_id": contract.market_context_id,
        "planned_entry_trigger": contract.entry_trigger,
        "structural_stop": contract.structural_stop,
        "first_obstacle": contract.first_obstacle,
        "target_price": contract.target_price,
        "max_hold_bars": contract.max_hold_bars,
        "gap_policy": contract.gap_policy,
        "fill_status": fill_status,
        "gap_through": None,
        "gap_adjustment": "not_applicable",
        "entry_date": None,
        "entry_price": None,
        "exit_date": None,
        "exit_price": None,
        "exit_reason": reason,
        "path_result": reason,
        "trade_result": "not-applicable",
        "evidence_status": evidence_status,
        "win_rate_eligible": "no",
        "ambiguous_intrabar": "no",
        "ambiguous_bar": None,
        "first_obstacle_hit": "unknown",
        "space_to_first_obstacle_R": None,
        "space_gate": "unknown",
        "risk_per_unit": None,
        "gross_pnl": None,
        "net_pnl": None,
        "commission_paid": None,
        "realized_R": None,
        "bars_held": None,
        "engine_warnings": "",
    }


def _find_ambiguous_bar(
    prices: pd.DataFrame,
    direction: str,
    structural_stop: float,
    target_price: float,
    entry_bar: int,
    exit_bar: int,
    *,
    include_entry: bool = False,
) -> pd.Timestamp | None:
    # A close entry has no exposure to the preceding intraday range; a
    # stop/limit entry does. Never silently discard its SL/TP conflict.
    start_bar = entry_bar if include_entry else entry_bar + 1
    for bar_number in range(start_bar, min(exit_bar, len(prices) - 1) + 1):
        row = prices.iloc[bar_number]
        if direction == "long":
            stop_hit = row["Low"] <= structural_stop
            target_hit = row["High"] >= target_price
        else:
            stop_hit = row["High"] >= structural_stop
            target_hit = row["Low"] <= target_price
        if stop_hit and target_hit:
            return _normalise_date_index(prices.index[bar_number])
    return None


def _first_obstacle_hit(
    prices: pd.DataFrame,
    direction: str,
    first_obstacle: float,
    entry_bar: int,
    exit_bar: int,
) -> bool:
    for bar_number in range(entry_bar + 1, min(exit_bar, len(prices) - 1) + 1):
        row = prices.iloc[bar_number]
        if direction == "long" and row["High"] >= first_obstacle:
            return True
        if direction == "short" and row["Low"] <= first_obstacle:
            return True
    return False


def _space_gate(space_r: float | None) -> str:
    if space_r is None or not math.isfinite(space_r):
        return "unknown"
    if space_r <= 0:
        return "blocked"
    if space_r < 1:
        return "borderline"
    return "positive"


def _classify_protective_exit(contract: BacktestContract, exit_price: float) -> str:
    """Classify a non-time exit even when the exit bar gaps through a level.

    backtesting.py fills a stop/limit protective order at the opening price
    when the opening bar gaps through that order.  Comparing the reported
    exit price for exact equality therefore mislabels valid target/stop exits
    as ``data_end``.  Same-bar stop/target conflicts are handled separately by
    ``_find_ambiguous_bar`` before this helper is called.
    """

    tolerance = 1e-9
    if contract.direction == "long":
        if exit_price >= contract.target_price - tolerance:
            return "target"
        if exit_price <= contract.structural_stop + tolerance:
            return "stop"
    else:
        if exit_price <= contract.target_price + tolerance:
            return "target"
        if exit_price >= contract.structural_stop - tolerance:
            return "stop"
    return "data_end"


def _entry_bar_protective_exit(contract: BacktestContract, row: pd.Series) -> str | None:
    """Prove a single protective hit after entry under continuous OHLC paths.

    Both-level bars remain ambiguous. A limit stop (or stop-entry target)
    lies beyond the entry in the same crossing direction. The other single
    level is provable only for an opening fill or a close beyond that level.
    """

    if contract.order_branch == "market_close":
        return None
    long = contract.direction == "long"
    stop_hit = row["Low"] <= contract.structural_stop if long else row["High"] >= contract.structural_stop
    target_hit = row["High"] >= contract.target_price if long else row["Low"] <= contract.target_price
    if bool(stop_hit) == bool(target_hit):
        return None
    limit = contract.order_branch == "limit_retest"
    at_open = (row["Open"] <= contract.entry_trigger if long else row["Open"] >= contract.entry_trigger) if limit else (
        row["Open"] >= contract.entry_trigger if long else row["Open"] <= contract.entry_trigger
    )
    reason = "stop" if stop_hit else "target"
    close_proves_hit = (
        (row["Close"] <= contract.structural_stop if long else row["Close"] >= contract.structural_stop)
        if stop_hit else (row["Close"] >= contract.target_price if long else row["Close"] <= contract.target_price)
    )
    if at_open or close_proves_hit or (limit and stop_hit) or (not limit and target_hit):
        return reason
    return None


def run_contract(
    contract: BacktestContract,
    prices: pd.DataFrame,
    *,
    commission: float = 0.0,
    spread: float = 0.0,
    cash: float = 1_000_000.0,
) -> dict[str, Any]:
    """Replay one frozen contract and return one auditable result row."""

    if (
        not _is_finite_numeric(commission)
        or not _is_finite_numeric(spread)
        or not _is_finite_numeric(cash)
        or float(commission) < 0
        or float(spread) < 0
        or float(cash) <= 0
    ):
        raise ValueError("commission and spread must be finite and non-negative; cash must be finite and positive")
    validate_contract(contract)
    eligibility = _contract_eligibility(contract)
    if eligibility == "observation_only":
        return _base_result(
            contract,
            fill_status="not-traded",
            reason="h-l-ema-slope-gate-failed",
        )
    if eligibility == "pending":
        return _base_result(
            contract,
            fill_status="unproven",
            reason="h-l-ema-slope-gate-pending",
        )
    symbol_prices = prices.loc[prices["Symbol"] == contract.symbol].copy()
    if symbol_prices.empty:
        return _base_result(contract, fill_status="unproven", reason="symbol-data-missing")
    symbol_prices = symbol_prices.drop(columns=["Symbol"])
    symbol_prices = symbol_prices.sort_index()
    if contract.decision_date not in symbol_prices.index:
        return _base_result(contract, fill_status="unproven", reason="decision-date-missing")
    decision_position = symbol_prices.index.get_indexer([contract.decision_date])[0]
    if decision_position <= 0:
        return _base_result(contract, fill_status="unproven", reason="decision-date-needs-prior-bar")

    entry_reference = (
        float(symbol_prices.loc[contract.decision_date, "Close"])
        if contract.order_branch == "market_close"
        else contract.entry_trigger
    )
    validate_contract(contract, entry_reference=entry_reference)
    opportunity = _first_entry_opportunity(symbol_prices, contract)
    if opportunity is None:
        return _base_result(contract, fill_status="no-fill", reason="no-entry-trigger")
    if opportunity["gap_through"] and contract.gap_policy == "skip":
        result = _base_result(contract, fill_status="opening-skip", reason="opening-gap-skipped")
        result["gap_through"] = True
        result["gap_adjustment"] = "skipped"
        return result
    if opportunity["gap_through"]:
        gap_open = float(symbol_prices.loc[opportunity["date"], "Open"])
        try:
            # A gap changes the actual entry and therefore the structural
            # risk/target geometry.  If the old contract no longer makes
            # directional sense at the open, require a separately frozen
            # gap-reprice contract instead of silently reusing old levels.
            validate_contract(contract, entry_reference=gap_open)
            gap_risk = abs(gap_open - contract.structural_stop)
            gap_space = abs(contract.first_obstacle - gap_open) / gap_risk
            if _normalise_space_status(contract.space_status) in {"strict_ge_1R", "clearly_positive", "borderline_ge_1R"} and gap_space < 1.0 - 1e-12:
                raise ContractValidationError(
                    "actual gap-open space is below the frozen >=1R requirement"
                )
        except ContractValidationError as exc:
            result = _base_result(contract, fill_status="unproven", reason="gap-reprice-required")
            result["gap_through"] = True
            result["gap_adjustment"] = "reprice_required"
            result["engine_warnings"] = str(exc)
            return result

    class ContractStrategy(Strategy):
        def init(self) -> None:
            self._order_submitted = False
            self._entry_bar: int | None = None
            self._time_exit_submitted = False
            self._time_exit_request_bar: int | None = None

        def next(self) -> None:
            current_date = _normalise_date_index(self.data.index[-1])
            current_bar = len(self.data) - 1
            if not self._order_submitted and current_date == contract.decision_date:
                protective = {"sl": contract.structural_stop, "tp": contract.target_price}
                if contract.order_branch == "market_close":
                    if contract.direction == "long":
                        self.buy(size=1, tag=contract.sample_id, **protective)
                    else:
                        self.sell(size=1, tag=contract.sample_id, **protective)
                elif contract.order_branch == "stop_confirmation":
                    if contract.direction == "long":
                        self.buy(stop=contract.entry_trigger, size=1, tag=contract.sample_id, **protective)
                    else:
                        self.sell(stop=contract.entry_trigger, size=1, tag=contract.sample_id, **protective)
                elif contract.order_branch == "limit_retest":
                    if contract.direction == "long":
                        self.buy(limit=contract.entry_trigger, size=1, tag=contract.sample_id, **protective)
                    else:
                        self.sell(limit=contract.entry_trigger, size=1, tag=contract.sample_id, **protective)
                self._order_submitted = True
                return

            if self.position:
                if self._entry_bar is None:
                    active_trades = list(self.trades)
                    if not active_trades:
                        return
                    # Use backtesting.py's actual entry bar.  With
                    # trade_on_close=True a market-close order becomes visible
                    # one strategy iteration after the trade's entry bar.
                    self._entry_bar = min(int(trade.entry_bar) for trade in active_trades)
                    # SL/TP are attached to the parent order, not one bar late.
                    # Upstream deferred entry-bar fills are excluded below.
                if (
                    not self._time_exit_submitted
                    and current_bar - self._entry_bar >= contract.max_hold_bars
                ):
                    self.position.close()
                    self._time_exit_submitted = True
                    self._time_exit_request_bar = current_bar

    trade_on_close = contract.order_branch == "market_close"
    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.simplefilter("always")
        stats = Backtest(
            symbol_prices,
            ContractStrategy,
            cash=cash,
            commission=commission,
            spread=spread,
            exclusive_orders=True,
            finalize_trades=True,
            trade_on_close=trade_on_close,
        ).run()

    trades = stats["_trades"]
    if trades.empty:
        # Pinned backtesting.py emits this warning for a rejected absolute
        # one-unit order. Do not confuse a buying-power failure with absence
        # of a market trigger (nor infer rejection from a generic cash warning).
        cash_rejected = any(
            "Broker canceled the order due to insufficient margin" in str(item.message)
            for item in captured_warnings
        )
        result = _base_result(
            contract, fill_status="unproven" if cash_rejected else "no-fill",
            reason="configuration-error-insufficient-cash" if cash_rejected else "no-entry-fill",
        )
        result["gap_through"] = bool(opportunity["gap_through"])
        if opportunity["gap_through"]:
            result["gap_adjustment"] = "accepted_open" if contract.gap_policy == "accept_open" else "flag_only"
        result["engine_warnings"] = " | ".join(str(item.message) for item in captured_warnings)
        return result
    if len(trades) != 1:
        raise RuntimeError(f"{contract.sample_id}: expected one trade, got {len(trades)}")

    trade = trades.iloc[0].copy()
    entry_bar = int(trade["EntryBar"])
    resolved_entry_exit = _entry_bar_protective_exit(contract, symbol_prices.iloc[entry_bar])
    if resolved_entry_exit is not None:
        # Replace only a proven same-bar exit, never a guessed intrabar order.
        # Downstream dates, fees, path horizon and R all use this same fill.
        resolved_price = contract.structural_stop if resolved_entry_exit == "stop" else contract.target_price
        trade["ExitBar"] = entry_bar
        trade["ExitTime"] = symbol_prices.index[entry_bar]
        trade["ExitPrice"] = resolved_price
        trade["Commission"] = commission * (abs(float(trade["EntryPrice"])) + abs(resolved_price))
        trade["PnL"] = (resolved_price - float(trade["EntryPrice"])) * (1 if contract.direction == "long" else -1) - trade["Commission"]
    exit_bar = int(trade["ExitBar"])
    entry_price = float(trade["EntryPrice"])
    exit_price = float(trade["ExitPrice"])
    risk_per_unit = abs(entry_price - contract.structural_stop)
    if risk_per_unit <= 0:
        raise ContractValidationError(f"{contract.sample_id}: realized risk is zero")
    strategy_state = stats["_strategy"]
    time_exit_submitted = resolved_entry_exit is None and bool(getattr(strategy_state, "_time_exit_submitted", False))
    time_exit_request_bar = getattr(strategy_state, "_time_exit_request_bar", None)
    expected_time_exit_bar = None
    if time_exit_submitted and time_exit_request_bar is not None:
        # backtesting.py market orders fill on the next open, except that
        # trade_on_close=True assigns a market-close order to the current bar.
        expected_time_exit_bar = (
            time_exit_request_bar
            if contract.order_branch == "market_close"
            else time_exit_request_bar + 1
        )
    time_exit_executed = (
        time_exit_submitted
        and expected_time_exit_bar is not None
        and exit_bar == expected_time_exit_bar
    )
    protective_exit_reason = _classify_protective_exit(contract, exit_price)
    # A non-market-close time-exit close order fills at the opening of
    # exit_bar.  Price action later in that bar occurred after the position
    # was closed and must not manufacture an ambiguous path or a first-
    # obstacle hit.  A market-close time exit is indexed to the closing bar,
    # so that bar remains part of the held path.  The same conservative
    # boundary applies to backtesting.py's forced final close when the
    # horizon is incomplete.
    time_exit_path_end_bar = (
        exit_bar
        if contract.order_branch == "market_close" and time_exit_executed
        else max(entry_bar, exit_bar - 1)
    )
    path_end_bar = (
        time_exit_path_end_bar
        if time_exit_executed
        else max(entry_bar, exit_bar - 1)
        if protective_exit_reason == "data_end"
        else exit_bar
    )
    exit_open = float(symbol_prices.iloc[exit_bar]["Open"])
    stop_gap_at_exit_open = (
        exit_bar > entry_bar
        and protective_exit_reason == "stop"
        and math.isclose(exit_price, exit_open, rel_tol=1e-12, abs_tol=1e-12)
        and (exit_open <= contract.structural_stop if contract.direction == "long"
             else exit_open >= contract.structural_stop)
    )
    if stop_gap_at_exit_open:
        # The protective stop was filled at the open. Later extremes in this
        # bar cannot create a stop/target conflict or a first-obstacle hit.
        path_end_bar = exit_bar - 1
    ambiguous_date = _find_ambiguous_bar(
        symbol_prices,
        contract.direction,
        contract.structural_stop,
        contract.target_price,
        entry_bar,
        path_end_bar,
        include_entry=contract.order_branch != "market_close",
    )
    entry_row = symbol_prices.iloc[entry_bar]
    entry_stop_hit = (
        entry_row["Low"] <= contract.structural_stop
        if contract.direction == "long" else entry_row["High"] >= contract.structural_stop
    )
    entry_target_hit = (
        entry_row["High"] >= contract.target_price
        if contract.direction == "long" else entry_row["Low"] <= contract.target_price
    )
    # backtesting.py may defer a contingent order on its parent stop/limit
    # candle. Its later synthetic fill is not evidence of the original path.
    # After the topology resolver, a remaining single touched level can still
    # predate entry. Do not present a later backend fill as its resolution.
    entry_fill_unresolved = (
        contract.order_branch != "market_close"
        and (entry_stop_hit or entry_target_hit)
        and exit_bar != entry_bar
    )
    obstacle_hit = _first_obstacle_hit(
        symbol_prices,
        contract.direction,
        contract.first_obstacle,
        entry_bar,
        path_end_bar,
    )
    entry_obstacle_unknown = False
    if contract.order_branch != "market_close":
        long = contract.direction == "long"
        touched = (entry_row["High"] >= contract.first_obstacle if long
                   else entry_row["Low"] <= contract.first_obstacle)
        if touched:
            # A stop and an obstacle lie in the same price direction, hence
            # the obstacle cannot precede the stop entry. For a limit entry
            # a favorable extreme may predate entry unless it was marketable
            # at the open or the closing price itself establishes the hit.
            entry_at_open = (entry_row["Open"] <= contract.entry_trigger if long
                             else entry_row["Open"] >= contract.entry_trigger)
            close_beyond_obstacle = (entry_row["Close"] >= contract.first_obstacle if long
                                    else entry_row["Close"] <= contract.first_obstacle)
            if contract.order_branch == "stop_confirmation" or entry_at_open or close_beyond_obstacle:
                obstacle_hit = True
            elif not obstacle_hit:
                entry_obstacle_unknown = True
            if resolved_entry_exit == "stop":
                # The favorable extreme may occur after the proven stop.
                entry_obstacle_unknown = True
    if ambiguous_date is not None:
        exit_reason = "ambiguous_intrabar_stop_target"
        trade_result = "pending"
        path_result = "ambiguous"
        realized_r: float | None = None
        evidence_status = "excluded_ambiguous"
    elif entry_fill_unresolved:
        exit_reason = "unresolved_entry_bar_protective_fill"
        trade_result = "pending"
        path_result = "unresolved-entry-bar-protective-fill"
        realized_r = None
        evidence_status = "excluded_entry_bar_fill"
    elif time_exit_executed:
        exit_reason = "time_exit"
        path_result = "time_exit"
        net_pnl = float(trade["PnL"])
        realized_r = net_pnl / risk_per_unit
        tolerance = 1e-12
        if realized_r > tolerance:
            trade_result = "win"
        elif realized_r < -tolerance:
            trade_result = "loss"
        else:
            trade_result = "scratch"
        evidence_status = "comparable"
    elif time_exit_submitted:
        # A close request made on the final available bar is executed only by
        # backtesting.py's synthetic finalization, not at the expected next
        # market time.  It is an incomplete horizon, not a completed time exit.
        exit_reason = "data_end"
        path_result = "incomplete-horizon"
        trade_result = "pending"
        realized_r = None
        evidence_status = "excluded_incomplete_horizon"
    else:
        exit_reason = protective_exit_reason
        if exit_reason == "data_end":
            path_result = "incomplete-horizon"
            trade_result = "pending"
            realized_r = None
            evidence_status = "excluded_incomplete_horizon"
        else:
            path_result = "target-reached" if exit_reason == "target" else (
                "first-obstacle-reached" if obstacle_hit and not entry_obstacle_unknown else (
                    "invalidated" if exit_reason == "stop" else exit_reason
                )
            )
            net_pnl = float(trade["PnL"])
            realized_r = net_pnl / risk_per_unit
            tolerance = 1e-12
            if realized_r > tolerance:
                trade_result = "win"
            elif realized_r < -tolerance:
                trade_result = "loss"
            else:
                trade_result = "scratch"
            evidence_status = "comparable"

    commission_paid = float(trade["Commission"])
    net_pnl = float(trade["PnL"])
    gross_pnl = net_pnl + commission_paid
    if contract.direction == "long":
        space_r = (contract.first_obstacle - entry_price) / risk_per_unit
    else:
        space_r = (entry_price - contract.first_obstacle) / risk_per_unit

    # Preserve the pre-entry bucket for provenance, but never let spread or
    # an actual fill reprice a frozen >=1R contract into the completed group.
    if _normalise_space_status(contract.space_status) in {"strict_ge_1R", "clearly_positive", "borderline_ge_1R"} and space_r < 1.0 - 1e-12:
        trade_result = "pending"
        realized_r = None
        evidence_status = "excluded_actual_space"
        exit_reason = "actual-fill-space-below-frozen-minimum"
        path_result = "reprice-required"

    result = _base_result(contract, fill_status="filled", reason=exit_reason)
    result.update(
        {
            "gap_through": bool(opportunity["gap_through"]),
            "gap_adjustment": (
                "accepted_open" if opportunity["gap_through"] and contract.gap_policy == "accept_open"
                else "flag_only" if opportunity["gap_through"] else "none"
            ),
            "entry_date": _normalise_date_index(trade["EntryTime"]).strftime("%Y-%m-%d"),
            "entry_price": entry_price,
            "exit_date": _normalise_date_index(trade["ExitTime"]).strftime("%Y-%m-%d"),
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "path_result": path_result,
            "trade_result": trade_result,
            "evidence_status": evidence_status,
            "win_rate_eligible": "yes" if trade_result in TRADE_RESULTS else "no",
            "ambiguous_intrabar": "yes" if ambiguous_date is not None else "no",
            "ambiguous_bar": ambiguous_date.strftime("%Y-%m-%d") if ambiguous_date is not None else None,
            # If the stop/target sequence is ambiguous, an obstacle reached
            # only on that unresolved path cannot be claimed as reached while
            # the position was still open.  Keep it out of the win/loss logic
            # and expose the uncertainty in the process field.
            "first_obstacle_hit": (
                "unknown"
                if ((ambiguous_date is not None or entry_fill_unresolved) and obstacle_hit)
                or entry_obstacle_unknown
                else "yes"
                if obstacle_hit
                else "no"
            ),
            "space_to_first_obstacle_R": space_r,
            "space_gate": _space_gate(space_r),
            "risk_per_unit": risk_per_unit,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "commission_paid": commission_paid,
            "realized_R": realized_r,
            "bars_held": exit_bar - entry_bar,
            "engine_warnings": " | ".join(str(item.message) for item in captured_warnings),
        }
    )
    return result


def run_contracts(
    contracts: Iterable[BacktestContract],
    prices: pd.DataFrame,
    *,
    commission: float = 0.0,
    spread: float = 0.0,
    cash: float = 1_000_000.0,
) -> list[dict[str, Any]]:
    return [
        run_contract(contract, prices, commission=commission, spread=spread, cash=cash)
        for contract in contracts
    ]


def _safe_mean(values: pd.Series) -> float | None:
    values = pd.to_numeric(values, errors="coerce").dropna()
    return float(values.mean()) if not values.empty else None


def _safe_median(values: pd.Series) -> float | None:
    values = pd.to_numeric(values, errors="coerce").dropna()
    return float(values.median()) if not values.empty else None


def _canonical_text_series(frame: pd.DataFrame, column: str) -> pd.Series:
    """Return a case-insensitive identity series without changing display values."""

    if column not in frame:
        return pd.Series("", index=frame.index, dtype="object")
    return frame[column].fillna("").astype(str).str.strip().str.casefold()


def _canonical_date_series(frame: pd.DataFrame, column: str) -> pd.Series:
    raw = _canonical_text_series(frame, column)
    parsed = pd.to_datetime(raw.replace("", np.nan), errors="coerce")
    normalised = raw.copy()
    valid = parsed.notna()
    normalised.loc[valid] = parsed.loc[valid].dt.strftime("%Y-%m-%d")
    return normalised


def _identity_key(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    parts = [
        _canonical_date_series(frame, column) if column == "decision_date" else _canonical_text_series(frame, column)
        for column in columns
    ]
    key = parts[0].copy()
    complete = parts[0].ne("")
    for part in parts[1:]:
        key = key + "|" + part
        complete &= part.ne("")
    return key.where(complete, "")


def _duplicate_identity_mask(values: pd.Series) -> tuple[pd.Series, int, int, int]:
    """Return duplicate rows and group/row/extra counts for a canonical identity."""

    nonempty = values[values != ""]
    counts = nonempty.value_counts()
    duplicate_counts = counts[counts > 1]
    mask = values.ne("") & values.isin(duplicate_counts.index)
    row_count = int(duplicate_counts.sum()) if not duplicate_counts.empty else 0
    group_count = int(len(duplicate_counts))
    extra_count = int((duplicate_counts - 1).sum()) if not duplicate_counts.empty else 0
    return mask, group_count, row_count, extra_count


def _exposure_overlap_stats(frame: pd.DataFrame) -> tuple[pd.Series, int, int]:
    """Find overlapping held intervals for non-duplicate filled result rows.

    This is a dependence diagnostic, not a claim that all common market dates
    are the same price-action setup.  Missing entry/exit dates remain unknown.
    """

    overlap = pd.Series(False, index=frame.index, dtype="bool")
    candidate = frame.loc[
        frame["fill_status"].eq("filled")
        & ~frame["_duplicate_result_row"]
        & frame["_symbol_key"].ne("")
    ].copy()
    if candidate.empty:
        return overlap, 0, 0
    candidate["_entry_ts"] = pd.to_datetime(candidate["entry_date"], errors="coerce")
    candidate["_exit_ts"] = pd.to_datetime(candidate["exit_date"], errors="coerce")
    candidate = candidate.loc[
        candidate["_entry_ts"].notna()
        & candidate["_exit_ts"].notna()
        & (candidate["_exit_ts"] >= candidate["_entry_ts"])
    ]
    if candidate.empty:
        return overlap, 0, 0

    group_count = 0
    for _, symbol_group in candidate.groupby("_symbol_key", sort=False):
        ordered = symbol_group.sort_values(["_entry_ts", "_exit_ts"])
        component_indices: list[Any] = []
        component_end: pd.Timestamp | None = None

        def flush_component() -> None:
            nonlocal group_count
            if len(component_indices) > 1:
                overlap.loc[component_indices] = True
                group_count += 1

        for index, row in ordered.iterrows():
            entry = row["_entry_ts"]
            exit_ = row["_exit_ts"]
            if component_end is None or entry > component_end:
                flush_component()
                component_indices = [index]
                component_end = exit_
            else:
                component_indices.append(index)
                if exit_ > component_end:
                    component_end = exit_
        flush_component()
    return overlap, group_count, int(overlap.sum())


def _prepare_result_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize result fields before any denominator or group calculation."""

    has_ema_gate_provenance = "h_l_ema_slope_gate" in frame.columns

    for column in (
        "sample_id",
        "symbol",
        "decision_date",
        "direction",
        "primary_pattern",
        "internal_label",
        "order_branch",
        "planned_entry_trigger",
        "lineage_id",
        "market_context_id",
        "structural_stop",
        "first_obstacle",
        "target_price",
        "max_hold_bars",
        "gap_policy",
        "label_source",
        "daily_context_window",
        "major_high_low_review",
        "ema20_50_200_review",
        "event_context",
        "contract_frozen",
        "daily_ema20_slope",
        "daily_ema50_slope",
        "h_l_ema_slope_gate",
        "h_l_pullback_location",
        "meta_confluence",
        "meta_zone",
        "meta_components",
        "pre_entry_space_R",
        "space_status",
        "entry_date",
        "exit_date",
    ):
        if column not in frame:
            frame[column] = ""
    frame["lineage_id"] = frame["lineage_id"].fillna("").astype(str).str.strip()
    frame["market_context_id"] = frame["market_context_id"].fillna("").astype(str).str.strip()
    frame["_sample_id_key"] = _canonical_text_series(frame, "sample_id")
    frame["_symbol_key"] = _canonical_text_series(frame, "symbol")
    frame["_lineage_key"] = _canonical_text_series(frame, "lineage_id")
    frame["_market_context_key"] = _canonical_text_series(frame, "market_context_id")
    frame["_contract_family_key"] = _identity_key(
        frame,
        [
            "symbol",
            "decision_date",
            "direction",
            "primary_pattern",
            "internal_label",
            "lineage_id",
        ],
    )
    sample_duplicate, sample_group_count, sample_row_count, sample_extra_count = _duplicate_identity_mask(
        frame["_sample_id_key"]
    )
    family_duplicate, family_group_count, family_row_count, family_extra_count = _duplicate_identity_mask(
        frame["_contract_family_key"]
    )
    frame["_duplicate_result_row"] = sample_duplicate | family_duplicate
    frame["_missing_result_identity"] = frame["_sample_id_key"].eq("") & frame["_contract_family_key"].eq("")
    frame.attrs["sample_id_group_count"] = sample_group_count
    frame.attrs["sample_id_row_count"] = sample_row_count
    frame.attrs["sample_id_extra_count"] = sample_extra_count
    frame.attrs["contract_family_group_count"] = family_group_count
    frame.attrs["contract_family_row_count"] = family_row_count
    frame.attrs["contract_family_extra_count"] = family_extra_count

    if "trade_result" not in frame:
        frame["trade_result"] = ""
    frame["trade_result"] = frame["trade_result"].fillna("").astype(str).str.strip().str.lower()
    if "win_rate_eligible" not in frame:
        frame["win_rate_eligible"] = "no"
    frame["win_rate_eligible"] = (
        frame["win_rate_eligible"].fillna("").astype(str).str.strip().str.lower()
    )
    if "evidence_status" not in frame:
        frame["evidence_status"] = "unknown"
    frame["evidence_status"] = frame["evidence_status"].fillna("").astype(str).str.strip().str.lower()
    if "fill_status" not in frame:
        frame["fill_status"] = "unknown"
    frame["fill_status"] = frame["fill_status"].fillna("").astype(str).str.strip().str.lower()
    if "ambiguous_intrabar" not in frame:
        frame["ambiguous_intrabar"] = "unknown"
    frame["ambiguous_intrabar"] = (
        frame["ambiguous_intrabar"].fillna("unknown").astype(str).str.strip().str.lower()
    )
    if "path_result" not in frame:
        frame["path_result"] = ""
    frame["path_result"] = frame["path_result"].fillna("").astype(str).str.strip().str.lower()
    if "realized_R" not in frame:
        frame["realized_R"] = None
    pre_entry_status, pre_entry_missing_fields = _pre_entry_provenance(frame)
    frame["pre_entry_provenance_status"] = pre_entry_status
    frame["pre_entry_provenance_missing_fields"] = pre_entry_missing_fields
    frame.attrs["pre_entry_provenance_incomplete_count"] = int(
        pre_entry_status.eq("incomplete").sum()
    )
    if "contract_eligibility" not in frame:
        frame["contract_eligibility"] = ""
    declared_contract_eligibility = (
        frame["contract_eligibility"].fillna("").astype(str).str.strip().str.lower()
    )
    if has_ema_gate_provenance:
        derived_contract_eligibility = pd.Series(
            [
                _result_contract_eligibility(label, gate)
                for label, gate in zip(frame["internal_label"], frame["h_l_ema_slope_gate"])
            ],
            index=frame.index,
            dtype="object",
        )
        mismatch = declared_contract_eligibility.ne("") & declared_contract_eligibility.ne(
            derived_contract_eligibility
        )
        frame["contract_eligibility"] = derived_contract_eligibility
        frame["_contract_eligibility_guard"] = True
        frame["_contract_eligibility_mismatch"] = mismatch
        frame.attrs["contract_eligibility_mismatch_count"] = int(mismatch.sum())
    else:
        frame["_contract_eligibility_guard"] = False
        frame["_contract_eligibility_mismatch"] = False
        frame.attrs["contract_eligibility_mismatch_count"] = 0
    overlap, overlap_group_count, overlap_row_count = _exposure_overlap_stats(frame)
    frame["_exposure_overlap_row"] = overlap
    frame.attrs["exposure_overlap_group_count"] = overlap_group_count
    frame.attrs["exposure_overlap_row_count"] = overlap_row_count
    return frame


def _result_economics_valid(frame: pd.DataFrame) -> pd.Series:
    """Check one-unit filled-result accounting independently of claimed R."""

    valid = pd.Series(True, index=frame.index, dtype="bool")
    values: dict[str, pd.Series] = {}
    for field in ("entry_price", "exit_price", "structural_stop", "risk_per_unit",
                  "gross_pnl", "net_pnl", "commission_paid", "realized_R"):
        raw = frame.get(field, pd.Series(None, index=frame.index, dtype="object"))
        valid &= raw.map(_is_finite_numeric)
        values[field] = pd.to_numeric(raw, errors="coerce")
    entry, exit_price = values["entry_price"], values["exit_price"]
    risk, net = values["risk_per_unit"], values["net_pnl"]
    expected_risk = (entry - values["structural_stop"]).abs()
    sign = np.where(_result_text_series(frame, "direction").str.lower().eq("long"), 1, -1)
    expected_gross = (exit_price - entry) * sign
    valid &= entry.gt(0) & exit_price.gt(0) & risk.gt(0) & values["commission_paid"].ge(0)
    for actual, expected in (
        (risk, expected_risk),
        (values["gross_pnl"], expected_gross),
        (net, expected_gross - values["commission_paid"]),
        (values["realized_R"], net / risk.where(risk.gt(0))),
    ):
        valid &= np.isclose(actual, expected, rtol=1e-9, atol=1e-12, equal_nan=False)
    return valid


def _completed_trade_mask(frame: pd.DataFrame) -> pd.Series:
    """Return the strict, auditable win-rate denominator mask."""

    realized_r = pd.to_numeric(frame["realized_R"], errors="coerce")
    # Match the same net-R tolerance used when replay labels a trade. A
    # contradictory imported label must not inflate wins or losses; retain the
    # source row and expose it through the existing guard-exclusion counters.
    result_sign_consistent = (
        (frame["trade_result"].eq("win") & realized_r.gt(1e-12))
        | (frame["trade_result"].eq("loss") & realized_r.lt(-1e-12))
        | (frame["trade_result"].eq("scratch") & realized_r.abs().le(1e-12))
    )
    duplicate_rows = frame.get(
        "_duplicate_result_row",
        pd.Series(False, index=frame.index, dtype="bool"),
    )
    contract_eligibility_guard = frame.get(
        "_contract_eligibility_guard",
        pd.Series(False, index=frame.index, dtype="bool"),
    )
    contract_eligibility = frame.get(
        "contract_eligibility",
        pd.Series("", index=frame.index, dtype="object"),
    )
    eligibility_mismatch = frame.get(
        "_contract_eligibility_mismatch",
        pd.Series(False, index=frame.index, dtype="bool"),
    )
    pre_entry_provenance_status = frame.get(
        "pre_entry_provenance_status",
        pd.Series("incomplete", index=frame.index, dtype="object"),
    )
    return (
        frame["trade_result"].isin(TRADE_RESULTS)
        & frame["win_rate_eligible"].eq("yes")
        & frame["evidence_status"].eq("comparable")
        & frame["fill_status"].eq("filled")
        & frame["ambiguous_intrabar"].eq("no")
        & frame["path_result"].isin(COMPLETED_PATH_RESULTS)
        & ~duplicate_rows
        & (~contract_eligibility_guard | contract_eligibility.eq("eligible"))
        & ~eligibility_mismatch
        & pre_entry_provenance_status.eq("complete")
        & realized_r.notna()
        & np.isfinite(realized_r)
        & result_sign_consistent
        & _result_economics_valid(frame)
    )


def _outcome_bucket_series(frame: pd.DataFrame, completed: pd.Series) -> pd.Series:
    """Give every row one mutually exclusive outcome/exclusion bucket."""

    buckets = pd.Series("other_excluded", index=frame.index, dtype="object")
    buckets.loc[completed] = "completed_win_loss_scratch"
    flag_mismatch = (~completed) & (
        frame["trade_result"].isin(TRADE_RESULTS) != frame["win_rate_eligible"].eq("yes")
    )
    buckets.loc[flag_mismatch] = "eligibility_flag_mismatch"
    guard_excluded = (~completed) & frame["win_rate_eligible"].eq("yes")
    buckets.loc[guard_excluded] = "eligibility_guard_excluded"
    ambiguous = (~completed) & (
        frame["ambiguous_intrabar"].eq("yes") | frame["path_result"].eq("ambiguous")
    )
    buckets.loc[ambiguous] = "ambiguous_intrabar"
    incomplete = (~completed) & frame["path_result"].eq("incomplete-horizon")
    buckets.loc[incomplete] = "incomplete_horizon"
    missing_path = (~completed) & frame["path_result"].eq("")
    buckets.loc[missing_path] = "missing_path_result"
    opening_skip = (~completed) & frame["fill_status"].eq("opening-skip")
    buckets.loc[opening_skip] = "opening_skip"
    no_fill = (~completed) & frame["fill_status"].eq("no-fill")
    buckets.loc[no_fill] = "no_fill"
    unproven = (~completed) & frame["fill_status"].eq("unproven")
    buckets.loc[unproven] = "unproven"
    configuration_error = (~completed) & frame["path_result"].eq("configuration-error-insufficient-cash")
    buckets.loc[configuration_error] = "configuration_error"
    observation_only = (~completed) & (
        frame["fill_status"].eq("not-traded") | frame["evidence_status"].eq("observation_only")
    )
    buckets.loc[observation_only] = "observation_only"
    provenance_incomplete = (~completed) & frame["pre_entry_provenance_status"].eq("incomplete")
    buckets.loc[provenance_incomplete] = "pre_entry_provenance_incomplete"
    duplicate_rows = frame.get(
        "_duplicate_result_row",
        pd.Series(False, index=frame.index, dtype="bool"),
    )
    buckets.loc[duplicate_rows] = "duplicate_result"
    return buckets


def _aggregate_group(group: pd.DataFrame) -> dict[str, Any]:
    completed = group[_completed_trade_mask(group)]
    r_values = pd.to_numeric(completed["realized_R"], errors="coerce").dropna()
    wins = int((completed["trade_result"] == "win").sum())
    losses = int((completed["trade_result"] == "loss").sum())
    scratches = int((completed["trade_result"] == "scratch").sum())
    gross_wins = float(r_values[r_values > 0].sum()) if not r_values.empty else 0.0
    gross_losses = float(r_values[r_values < 0].sum()) if not r_values.empty else 0.0
    profit_factor = gross_wins / abs(gross_losses) if gross_losses < 0 else None
    event_context_values = sorted(
        {
            str(value)
            for value in group["event_context"].dropna().tolist()
            if str(value).strip()
        }
    )
    return {
        "primary_pattern": group["primary_pattern"].iloc[0],
        "internal_label": group["internal_label"].iloc[0],
        "direction": group["direction"].iloc[0],
        "pre_entry_provenance_status": group["pre_entry_provenance_status"].iloc[0],
        "lineage_id": group["lineage_id"].iloc[0],
        "market_context_id": group["market_context_id"].iloc[0],
        "daily_ema20_slope": group["daily_ema20_slope"].iloc[0],
        "daily_ema50_slope": group["daily_ema50_slope"].iloc[0],
        "h_l_ema_slope_gate": group["h_l_ema_slope_gate"].iloc[0],
        "meta_confluence": group["meta_confluence"].iloc[0],
        "event_bucket": group["event_bucket"].iloc[0],
        "contract_space_bucket": group["contract_space_bucket"].iloc[0],
        "contract_eligibility": group["contract_eligibility"].iloc[0],
        "order_branch": group["order_branch"].iloc[0],
        "event_context": event_context_values[0] if len(event_context_values) == 1 else "multiple",
        "event_context_values": event_context_values,
        "sample_count": int(len(group)),
        "filled_count": int((group["fill_status"] == "filled").sum()),
        "duplicate_result_count": int(group["_duplicate_result_row"].sum()),
        "win_rate_eligible_count": int((group["win_rate_eligible"] == "yes").sum()),
        "win_rate_eligibility_mismatch_count": int(
            (group["trade_result"].isin(TRADE_RESULTS) != group["win_rate_eligible"].eq("yes")).sum()
        ),
        "win_rate_guard_exclusion_count": int(
            ((group["win_rate_eligible"] == "yes") & ~_completed_trade_mask(group)).sum()
        ),
        "completed_trade_count": int(len(completed)),
        "wins": wins,
        "losses": losses,
        "scratches": scratches,
        "ambiguous_count": int((group["ambiguous_intrabar"] == "yes").sum()),
        "win_rate_pct": float(wins / len(completed) * 100) if len(completed) else None,
        "avg_realized_R": _safe_mean(completed["realized_R"]),
        "median_realized_R": _safe_median(completed["realized_R"]),
        "total_realized_R": float(r_values.sum()) if not r_values.empty else None,
        "profit_factor": profit_factor,
        "statistics_status": "descriptive_only",
    }


def build_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Build descriptive results without promoting them to validated evidence."""

    frame = pd.DataFrame(results)
    if frame.empty:
        return {
            "engine_version": ENGINE_VERSION,
            "backtesting_version": getattr(backtesting, "__version__", "unknown"),
            "study_status": "research_only / no-results",
            "contract_count": 0,
            "filled_count": 0,
            "eligible_contract_count": 0,
            "observation_only_count": 0,
            "pending_contract_count": 0,
            "completed_trade_count": 0,
            "win_rate_eligible_count": 0,
            "win_rate_eligibility_mismatch_count": 0,
            "win_rate_guard_exclusion_count": 0,
            "unique_sample_id_count": 0,
            "missing_sample_id_count": 0,
            "duplicate_sample_id_group_count": 0,
            "duplicate_sample_id_row_count": 0,
            "duplicate_sample_id_extra_row_count": 0,
            "duplicate_contract_family_group_count": 0,
            "duplicate_contract_family_row_count": 0,
            "duplicate_contract_family_extra_row_count": 0,
            "duplicate_result_row_count": 0,
            "pre_entry_provenance_complete_count": 0,
            "pre_entry_provenance_incomplete_count": 0,
            "pre_entry_provenance_status_counts": {},
            "contract_eligibility_mismatch_count": 0,
            "event_bucket_mismatch_count": 0,
            "contract_space_bucket_mismatch_count": 0,
            "event_bucket_contract_counts": {},
            "contract_space_bucket_counts": {},
            "outcome_bucket_counts": {},
            "ordinary_non_event_completed_trade_count": 0,
            "ordinary_non_event_win_rate_pct": None,
            "ordinary_non_event_strict_space_completed_trade_count": 0,
            "ordinary_non_event_strict_space_win_rate_pct": None,
            "ordinary_non_event_strict_space_statistics_status": "not-computable_no-results",
            "ambiguous_count": 0,
            "unique_lineage_count": 0,
            "missing_lineage_count": 0,
            "shared_lineage_group_count": 0,
            "shared_lineage_row_count": 0,
            "cross_pattern_lineage_group_count": 0,
            "unique_market_context_count": 0,
            "missing_market_context_count": 0,
            "shared_market_context_group_count": 0,
            "shared_market_context_row_count": 0,
            "exposure_overlap_group_count": 0,
            "exposure_overlap_row_count": 0,
            "independence_status": "no-results",
            "independence_adjusted_win_rate_pct": None,
            "independence_statistics_status": "not-computable_no-results",
            "win_rate_pct": None,
            "realized_R_distribution": None,
            "limitations": [
                "no results; win rate is not computable",
                "empty summary is descriptive only and does not create a denominator",
            ],
            "groups": [],
        }

    frame = _prepare_result_frame(frame)
    stratification_columns = [
        "lineage_id",
        "daily_ema20_slope",
        "daily_ema50_slope",
        "h_l_ema_slope_gate",
        "meta_confluence",
        "contract_eligibility",
        "pre_entry_provenance_status",
    ]
    for column in stratification_columns:
        if column not in frame:
            frame[column] = ""
    if "event_context" not in frame:
        frame["event_context"] = ""
    derived_event_bucket = frame["event_context"].fillna("").map(_event_bucket)
    if "event_bucket" in frame:
        declared_event_bucket = frame["event_bucket"].fillna("").astype(str).str.strip().str.casefold()
        event_bucket_mismatch = declared_event_bucket.ne("") & declared_event_bucket.ne(
            derived_event_bucket.str.casefold()
        )
    else:
        event_bucket_mismatch = pd.Series(False, index=frame.index, dtype="bool")
    frame["event_bucket"] = derived_event_bucket
    frame.attrs["event_bucket_mismatch_count"] = int(event_bucket_mismatch.sum())
    if "space_status" not in frame:
        frame["space_status"] = ""
    if "pre_entry_space_R" not in frame:
        frame["pre_entry_space_R"] = None
    frame["pre_entry_space_R"] = pd.to_numeric(frame["pre_entry_space_R"], errors="coerce")
    derived_space_bucket = pd.Series(
        [
            _contract_space_bucket(status, space_r)
            for status, space_r in zip(frame["space_status"], frame["pre_entry_space_R"])
        ],
        index=frame.index,
        dtype="object",
    )
    if "contract_space_bucket" in frame:
        declared_space_bucket = frame["contract_space_bucket"].fillna("").astype(str).str.strip().str.casefold()
        space_bucket_mismatch = declared_space_bucket.ne("") & declared_space_bucket.ne(
            derived_space_bucket.str.casefold()
        )
    else:
        space_bucket_mismatch = pd.Series(False, index=frame.index, dtype="bool")
    frame["contract_space_bucket"] = derived_space_bucket
    frame.attrs["contract_space_bucket_mismatch_count"] = int(space_bucket_mismatch.sum())

    completed_mask = _completed_trade_mask(frame)
    completed = frame[completed_mask]
    r_values = pd.to_numeric(completed["realized_R"], errors="coerce").dropna()
    wins = int((completed["trade_result"] == "win").sum())
    lineage_values = frame["_lineage_key"]
    nonempty_lineages = lineage_values[lineage_values != ""]
    lineage_counts = nonempty_lineages.value_counts()
    shared_lineages = lineage_counts[lineage_counts > 1]
    lineage_frame = frame.assign(_lineage=lineage_values)
    lineage_frame = lineage_frame[lineage_frame["_lineage"] != ""]
    pattern_counts = (
        lineage_frame.groupby("_lineage")["primary_pattern"].nunique()
        if not lineage_frame.empty
        else pd.Series(dtype="int64")
    )
    cross_pattern_lineages = pattern_counts[pattern_counts > 1]
    missing_lineage_count = int((lineage_values == "").sum())
    unique_lineage_count = int(nonempty_lineages.nunique())
    shared_lineage_group_count = int(len(shared_lineages))
    shared_lineage_row_count = int(shared_lineages.sum()) if shared_lineages.size else 0
    sample_id_values = frame["_sample_id_key"]
    unique_sample_id_count = int(sample_id_values[sample_id_values != ""].nunique())
    missing_sample_id_count = int((sample_id_values == "").sum())
    duplicate_sample_id_group_count = int(frame.attrs.get("sample_id_group_count", 0))
    duplicate_sample_id_row_count = int(frame.attrs.get("sample_id_row_count", 0))
    duplicate_sample_id_extra_row_count = int(frame.attrs.get("sample_id_extra_count", 0))
    duplicate_contract_family_group_count = int(frame.attrs.get("contract_family_group_count", 0))
    duplicate_contract_family_row_count = int(frame.attrs.get("contract_family_row_count", 0))
    duplicate_contract_family_extra_row_count = int(frame.attrs.get("contract_family_extra_count", 0))
    duplicate_result_row_count = int(frame["_duplicate_result_row"].sum())

    market_context_values = frame["_market_context_key"]
    nonempty_market_contexts = market_context_values[market_context_values != ""]
    market_context_counts = nonempty_market_contexts.value_counts()
    shared_market_contexts = market_context_counts[market_context_counts > 1]
    unique_market_context_count = int(nonempty_market_contexts.nunique())
    missing_market_context_count = int((market_context_values == "").sum())
    shared_market_context_group_count = int(len(shared_market_contexts))
    shared_market_context_row_count = int(shared_market_contexts.sum()) if shared_market_contexts.size else 0
    exposure_overlap_group_count = int(frame.attrs.get("exposure_overlap_group_count", 0))
    exposure_overlap_row_count = int(frame.attrs.get("exposure_overlap_row_count", 0))
    pre_entry_provenance_status_counts = {
        str(key): int(value)
        for key, value in frame["pre_entry_provenance_status"].value_counts(dropna=False).items()
    }

    if duplicate_result_row_count:
        independence_status = "duplicate_result_rows_present"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_duplicate_result_rows"
    elif missing_lineage_count:
        independence_status = "missing_lineage"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_missing_lineage"
    elif shared_lineage_group_count:
        independence_status = "dependent_lineage_rows_present"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_shared_lineage"
    elif missing_sample_id_count:
        independence_status = "missing_sample_identity"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_missing_sample_identity"
    elif missing_market_context_count:
        independence_status = "missing_market_context"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_missing_market_context"
    elif shared_market_context_group_count:
        independence_status = "shared_market_context_rows_present"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_shared_market_context"
    elif exposure_overlap_group_count:
        independence_status = "overlapping_symbol_exposure"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_overlapping_exposure"
    else:
        independence_status = "unique_lineage_only"
        independence_adjusted_win_rate = float(wins / len(completed) * 100) if len(completed) else None
        independence_statistics_status = "descriptive_unique_lineage_only"
    event_bucket_contract_counts = {
        str(key): int(value) for key, value in frame["event_bucket"].value_counts(dropna=False).items()
    }
    contract_space_bucket_counts = {
        str(key): int(value) for key, value in frame["contract_space_bucket"].value_counts(dropna=False).items()
    }
    ordinary_rows_mask = frame["event_bucket"].eq("ordinary_non_event")
    ordinary_completed = frame[ordinary_rows_mask & completed_mask]
    ordinary_strict_rows_mask = ordinary_rows_mask & frame["contract_space_bucket"].eq("strict_ge_1R")
    ordinary_strict_completed = frame[ordinary_strict_rows_mask & completed_mask]
    ordinary_wins = int((ordinary_completed["trade_result"] == "win").sum())
    ordinary_strict_wins = int((ordinary_strict_completed["trade_result"] == "win").sum())
    ordinary_strict_status = (
        "descriptive_only" if len(ordinary_strict_completed) else "not-computable_no-completed-trades"
    )
    summary: dict[str, Any] = {
        "engine_version": ENGINE_VERSION,
        "backtesting_version": getattr(backtesting, "__version__", "unknown"),
        "study_status": "research_only / descriptive_only / not-validated",
        "contract_count": int(len(frame)),
        "filled_count": int((frame["fill_status"] == "filled").sum()),
        "eligible_contract_count": int((frame["contract_eligibility"] == "eligible").sum()),
        "observation_only_count": int((frame["contract_eligibility"] == "observation_only").sum()),
        "pending_contract_count": int((frame["contract_eligibility"] == "pending").sum()),
        "completed_trade_count": int(len(completed)),
        "win_rate_eligible_count": int((frame["win_rate_eligible"] == "yes").sum()),
        "win_rate_eligibility_mismatch_count": int(
            (frame["trade_result"].isin(TRADE_RESULTS) != frame["win_rate_eligible"].eq("yes")).sum()
        ),
        "win_rate_guard_exclusion_count": int(
            ((frame["win_rate_eligible"] == "yes") & ~completed_mask).sum()
        ),
        "unique_sample_id_count": unique_sample_id_count,
        "missing_sample_id_count": missing_sample_id_count,
        "duplicate_sample_id_group_count": duplicate_sample_id_group_count,
        "duplicate_sample_id_row_count": duplicate_sample_id_row_count,
        "duplicate_sample_id_extra_row_count": duplicate_sample_id_extra_row_count,
        "duplicate_contract_family_group_count": duplicate_contract_family_group_count,
        "duplicate_contract_family_row_count": duplicate_contract_family_row_count,
        "duplicate_contract_family_extra_row_count": duplicate_contract_family_extra_row_count,
        "duplicate_result_row_count": duplicate_result_row_count,
        "pre_entry_provenance_complete_count": int(
            (frame["pre_entry_provenance_status"] == "complete").sum()
        ),
        "pre_entry_provenance_incomplete_count": int(
            (frame["pre_entry_provenance_status"] == "incomplete").sum()
        ),
        "pre_entry_provenance_status_counts": pre_entry_provenance_status_counts,
        "contract_eligibility_mismatch_count": int(
            frame.attrs.get("contract_eligibility_mismatch_count", 0)
        ),
        "event_bucket_mismatch_count": int(frame.attrs.get("event_bucket_mismatch_count", 0)),
        "contract_space_bucket_mismatch_count": int(
            frame.attrs.get("contract_space_bucket_mismatch_count", 0)
        ),
        "event_bucket_contract_counts": event_bucket_contract_counts,
        "contract_space_bucket_counts": contract_space_bucket_counts,
        "outcome_bucket_counts": {
            str(key): int(value)
            for key, value in _outcome_bucket_series(frame, completed_mask).value_counts(dropna=False).items()
        },
        "ordinary_non_event_completed_trade_count": int(len(ordinary_completed)),
        "ordinary_non_event_win_rate_pct": (
            float(ordinary_wins / len(ordinary_completed) * 100) if len(ordinary_completed) else None
        ),
        "ordinary_non_event_strict_space_completed_trade_count": int(len(ordinary_strict_completed)),
        "ordinary_non_event_strict_space_win_rate_pct": (
            float(ordinary_strict_wins / len(ordinary_strict_completed) * 100)
            if len(ordinary_strict_completed)
            else None
        ),
        "ordinary_non_event_strict_space_statistics_status": ordinary_strict_status,
        "unique_lineage_count": unique_lineage_count,
        "missing_lineage_count": missing_lineage_count,
        "shared_lineage_group_count": shared_lineage_group_count,
        "shared_lineage_row_count": shared_lineage_row_count,
        "cross_pattern_lineage_group_count": int(len(cross_pattern_lineages)),
        "unique_market_context_count": unique_market_context_count,
        "missing_market_context_count": missing_market_context_count,
        "shared_market_context_group_count": shared_market_context_group_count,
        "shared_market_context_row_count": shared_market_context_row_count,
        "exposure_overlap_group_count": exposure_overlap_group_count,
        "exposure_overlap_row_count": exposure_overlap_row_count,
        "independence_status": independence_status,
        "independence_adjusted_win_rate_pct": independence_adjusted_win_rate,
        "independence_statistics_status": independence_statistics_status,
        "ambiguous_count": int((frame["ambiguous_intrabar"] == "yes").sum()),
        "win_rate_pct": float(wins / len(completed) * 100) if len(completed) else None,
        "realized_R_distribution": {
            "mean": float(r_values.mean()),
            "median": float(r_values.median()),
            "min": float(r_values.min()),
            "max": float(r_values.max()),
        } if not r_values.empty else None,
        "groups": [],
        "limitations": [
            "manual_chart_review labels only; no pattern recognition or symbol discovery",
            "results are descriptive and do not establish a validated win rate",
            "the win-rate denominator requires win_rate_eligible=yes, filled, comparable evidence, no ambiguity or incomplete horizon, a win/loss/scratch result, and finite realized_R",
            "same-bar stop/target ambiguity is excluded from the win-rate denominator",
            "each contract must be frozen before its outcome and must carry >=2y Daily context evidence",
            "lineage_id is preserved for dependence control; contracts sharing a lineage are not independent samples",
            "same sample_id or contract-family duplicates are excluded from the completed denominator; all copies remain visible in duplicate counters",
            "market_context_id is optional manual dependence evidence; missing or shared market context withholds the independence-adjusted rate",
            "overlapping same-symbol held intervals are a dependence diagnostic and withhold the independence-adjusted rate",
            "win_rate_pct is row-based descriptive output; an independence-adjusted rate is withheld when identity, lineage, market context or exposure independence is unresolved",
            "event_bucket is conservative; event-unverified, pending, unknown and unclassified contexts are never upgraded to ordinary_non_event",
            "ordinary_non_event_strict_space statistics use only explicit pre-entry space evidence; blank legacy space fields remain unknown",
            "H1/H2/L1/L2 require the matching Daily EMA20/EMA50 slope gate; failed gates remain observation_only and are excluded",
            "event_bucket and contract_space_bucket are recomputed from raw pre-entry fields; supplied derived values are diagnostic only",
            "when H/L EMA gate provenance is present, contract eligibility is recomputed from that gate and mismatches are excluded from the completed denominator",
            "completed trades also require complete pre-entry provenance; missing contract/event/planned-trigger/H-L evidence is descriptive only and is bucketed as pre_entry_provenance_incomplete",
            "META is recorded and stratified as a confluence field; it is not an entry trigger or authorization",
        ],
    }
    grouping_columns = stratification_columns
    group_columns = [
        "primary_pattern",
        "internal_label",
        "direction",
        *grouping_columns,
        "market_context_id",
        "event_bucket",
        "contract_space_bucket",
        "order_branch",
    ]
    for _, group in frame.groupby(group_columns, dropna=False, sort=True):
        summary["groups"].append(_aggregate_group(group))
    return summary


def _json_default(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    raise TypeError(f"not JSON serializable: {type(value).__name__}")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _result_set_sha256(results: list[dict[str, Any]]) -> str:
    serialised = pd.DataFrame(results).to_csv(index=False, lineterminator="\n")
    return hashlib.sha256(serialised.encode("utf-8")).hexdigest()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay manually frozen PA Research contracts with backtesting.py."
    )
    parser.add_argument("--prices", required=True, help="OHLCV CSV with Date, Open, High, Low, Close and optional Symbol/Volume")
    parser.add_argument("--contracts", required=True, help="Human-frozen contract CSV; see research/backtesting/README.md")
    parser.add_argument("--output-dir", required=True, help="Directory for results.csv, summary.json and run_metadata.json")
    parser.add_argument("--symbol", help="Required only when the price CSV has no Symbol column")
    parser.add_argument("--commission", type=float, default=0.0, help="Per-side commission rate passed to backtesting.py")
    parser.add_argument("--spread", type=float, default=0.0, help="Spread rate passed to backtesting.py")
    parser.add_argument("--cash", type=float, default=1_000_000.0, help="Synthetic cash for one-unit research trades")
    parser.add_argument("--data-source", default="user_supplied_historical_csv")
    parser.add_argument("--data-status", default="historical", choices=["historical", "delayed", "live_confirmed", "incomplete"])
    parser.add_argument("--as-of-time", default=None, help="Optional source timestamp to preserve in run metadata")
    return parser


def _check_output_paths(inputs: list[Path], outputs: list[Path]) -> None:
    """Reject path, symlink and hard-link aliases before touching outputs."""

    for index, output in enumerate(outputs):
        for other in inputs + outputs[:index]:
            if output.resolve() == other.resolve() or (
                output.exists() and other.exists() and output.samefile(other)
            ):
                raise ValueError(f"input/output paths overlap: {output} and {other}")


def _publish_directory_no_replace(staging_root: Path, output_dir: Path) -> None:
    """Atomically publish a complete artifact directory without replacement."""

    source = str(staging_root)
    destination = str(output_dir)
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        move_file = kernel32.MoveFileW
        move_file.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
        move_file.restype = ctypes.c_int
        if not move_file(source, destination):
            error = ctypes.get_last_error()
            if error in {80, 183}:
                raise FileExistsError(error, ctypes.FormatError(error), destination)
            raise OSError(error, ctypes.FormatError(error), destination)
        return
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform.startswith("linux"):
        rename_no_replace = getattr(libc, "renameat2", None)
        if rename_no_replace is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace directory publication is unavailable")
        rename_no_replace.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        rename_no_replace.restype = ctypes.c_int
        result = rename_no_replace(-100, os.fsencode(source), -100, os.fsencode(destination), 1)
    elif sys.platform == "darwin":
        rename_no_replace = getattr(libc, "renamex_np", None)
        if rename_no_replace is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace directory publication is unavailable")
        rename_no_replace.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        rename_no_replace.restype = ctypes.c_int
        result = rename_no_replace(os.fsencode(source), os.fsencode(destination), 0x00000004)
    else:
        raise OSError(errno.ENOTSUP, "atomic no-replace directory publication is unavailable")
    if result != 0:
        error = ctypes.get_errno()
        if error in {errno.EEXIST, errno.ENOTEMPTY}:
            raise FileExistsError(error, os.strerror(error), destination)
        raise OSError(error, os.strerror(error), destination)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if (
        not _is_finite_numeric(args.commission)
        or not _is_finite_numeric(args.spread)
        or not _is_finite_numeric(args.cash)
        or args.commission < 0
        or args.spread < 0
        or args.cash <= 0
    ):
        raise SystemExit("commission/spread must be finite and non-negative; cash must be finite and positive")
    price_path = Path(args.prices).resolve()
    contract_path = Path(args.contracts).resolve()
    engine_source_path = Path(__file__).resolve(strict=True)
    engine_source_snapshot = require_source_snapshot(
        sys.modules.get(__name__),
        globals(),
        engine_source_path,
        "engine source",
    )
    verify_source_snapshot(engine_source_snapshot, "engine source")
    engine_source_sha256 = engine_source_snapshot.sha256
    output_dir = Path(args.output_dir).resolve()
    outputs = [output_dir / name for name in ("results.csv", "summary.json", "run_metadata.json")]
    _check_output_paths([price_path, contract_path, engine_source_path], outputs)
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError(f"refusing to reuse output directory: {output_dir}; use a new output directory")
    # Hash exactly the immutable bytes consumed by the loaders, before any
    # output write. A later input edit must not acquire the run's provenance.
    price_bytes = price_path.read_bytes()
    contract_bytes = contract_path.read_bytes()
    price_hash = hashlib.sha256(price_bytes).hexdigest()
    contract_hash = hashlib.sha256(contract_bytes).hexdigest()
    prices = load_prices(BytesIO(price_bytes), default_symbol=args.symbol)
    contracts = load_contracts(BytesIO(contract_bytes))
    results = run_contracts(
        contracts,
        prices,
        commission=args.commission,
        spread=args.spread,
        cash=args.cash,
    )
    summary = build_summary(results)
    verify_source_snapshot(engine_source_snapshot, "engine source")
    _check_output_paths([price_path, contract_path, engine_source_path], outputs)
    results_path = output_dir / "results.csv"
    result_set_sha256 = _result_set_sha256(results)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".pa-backtest-artifact-", dir=output_dir.parent) as staging_directory:
        staging_root = Path(staging_directory)
        staged_results = staging_root / "results.csv"
        pd.DataFrame(results).to_csv(staged_results, index=False)
        results_file_sha256 = _sha256_file(staged_results)
        summary["result_set_sha256"] = result_set_sha256
        summary["results_file_sha256"] = results_file_sha256
        summary["engine_source_sha256"] = engine_source_sha256
        summary_provenance = {
            "result_columns": list(pd.DataFrame(results).columns),
            "pre_entry_provenance_complete_count": summary["pre_entry_provenance_complete_count"],
            "pre_entry_provenance_incomplete_count": summary["pre_entry_provenance_incomplete_count"],
            "pre_entry_provenance_status_counts": dict(summary["pre_entry_provenance_status_counts"]),
            "contract_eligibility_mismatch_count": summary["contract_eligibility_mismatch_count"],
            "event_bucket_mismatch_count": summary["event_bucket_mismatch_count"],
            "contract_space_bucket_mismatch_count": summary["contract_space_bucket_mismatch_count"],
            "win_rate_eligibility_mismatch_count": summary["win_rate_eligibility_mismatch_count"],
            "win_rate_guard_exclusion_count": summary["win_rate_guard_exclusion_count"],
            "completed_trade_count": summary["completed_trade_count"],
            "outcome_bucket_counts": dict(summary["outcome_bucket_counts"]),
        }
        summary["run_metadata"] = {
            "engine_version": ENGINE_VERSION,
            "backtesting_version": getattr(backtesting, "__version__", "unknown"),
            "python_version": platform.python_version(),
            "pandas_version": pd.__version__,
            "numpy_version": np.__version__,
            "engine_source": str(engine_source_path),
            "engine_source_sha256": engine_source_sha256,
            "data_source": args.data_source,
            "data_status": args.data_status,
            "as_of_time": args.as_of_time,
            "price_file": str(price_path),
            "price_file_sha256": price_hash,
            "contract_file": str(contract_path),
            "contract_file_sha256": contract_hash,
            "result_set_sha256": result_set_sha256,
            "results_file": str(results_path),
            "results_file_sha256": results_file_sha256,
            "result_row_count": len(results),
            "summary_provenance": summary_provenance,
            "commission": args.commission,
            "spread": args.spread,
            "cash": args.cash,
            "scope": "PA Research only; no scanner; no Execution Agent; no Codex Trading changes",
        }
        summary_text = json.dumps(summary, ensure_ascii=False, indent=2, default=_json_default)
        metadata_text = json.dumps(summary["run_metadata"], ensure_ascii=False, indent=2, default=_json_default)
        (staging_root / "summary.json").write_text(summary_text + "\n", encoding="utf-8")
        (staging_root / "run_metadata.json").write_text(metadata_text + "\n", encoding="utf-8")
        verify_source_snapshot(engine_source_snapshot, "engine source")
        _publish_directory_no_replace(staging_root, output_dir)
    print(summary_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
