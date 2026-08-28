"""A small, auditable backtesting.py adapter for PA Research.

This module deliberately does not discover symbols or identify chart patterns.
It replays contracts that a human has already frozen from a chart review.  The
separation is important: a chart label such as H1 or strong A is evidence from
the research record, not a label inferred by this program.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import backtesting
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy


ENGINE_VERSION = "0.3.3"
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
    if "ordinary_non_event" in context and "gap_reprice" not in context:
        return "ordinary_non_event"
    if re.search(
        r"earnings_filter_passed|no_event_inside|outside_10bar_horizon|"
        r"outside_a_b_and_10bar_horizon|setup_window_no_known_event",
        context,
    ):
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

    if contract.internal_label not in H_L_LABELS:
        return "eligible"
    if contract.h_l_ema_slope_gate in {"long_pass", "short_pass"}:
        return "eligible"
    if contract.h_l_ema_slope_gate == "fail_flat_or_opposite":
        return "observation_only"
    return "pending"


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
    if contract.order_branch not in SUPPORTED_ORDER_BRANCHES:
        errors.append(f"order_branch must be one of {sorted(SUPPORTED_ORDER_BRANCHES)}")
    if contract.order_branch != "market_close" and contract.entry_trigger is None:
        errors.append("entry_trigger is required for stop_confirmation and limit_retest")
    if contract.order_branch == "market_close" and contract.gap_policy != "not_applicable":
        errors.append("market_close requires gap_policy=not_applicable")
    if contract.order_branch != "market_close" and contract.gap_policy not in SUPPORTED_GAP_POLICIES - {"not_applicable"}:
        errors.append(f"gap_policy must be one of {sorted(SUPPORTED_GAP_POLICIES - {'not_applicable'})}")
    if contract.max_hold_bars < 1:
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
    if space_status in {"strict_ge_1r", "clearly_positive"} and contract.pre_entry_space_R is not None:
        if contract.pre_entry_space_R < 1:
            errors.append("strict space_status requires pre_entry_space_R >= 1")
    if space_status == "blocked" and contract.pre_entry_space_R is not None:
        if contract.pre_entry_space_R > 0:
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

    if entry_reference is not None:
        if contract.direction == "long":
            if contract.structural_stop >= entry_reference:
                errors.append("long structural_stop must be below the entry reference")
            if contract.first_obstacle <= entry_reference:
                errors.append("long first_obstacle must be above the entry reference")
            if contract.target_price <= entry_reference:
                errors.append("long target_price must be above the entry reference")
        elif contract.direction == "short":
            if contract.structural_stop <= entry_reference:
                errors.append("short structural_stop must be above the entry reference")
            if contract.first_obstacle >= entry_reference:
                errors.append("short first_obstacle must be below the entry reference")
            if contract.target_price >= entry_reference:
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

    frame = _normalise_price_columns(pd.read_csv(path))
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

    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    if frame["Date"].isna().any():
        raise ValueError("price CSV contains an invalid Date")
    if frame["Date"].dt.tz is not None:
        frame["Date"] = frame["Date"].dt.tz_localize(None)
    for column in ("Open", "High", "Low", "Close"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if "Volume" not in frame.columns:
        frame["Volume"] = 0.0
    else:
        frame["Volume"] = pd.to_numeric(frame["Volume"], errors="coerce").fillna(0.0)

    if frame[["Open", "High", "Low", "Close"]].isna().any().any():
        raise ValueError("price CSV contains a missing or non-numeric OHLC value")
    invalid_ohlc = (
        (frame["High"] < frame[["Open", "Close", "Low"]].max(axis=1))
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

    frame = pd.read_csv(path)
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
        if contract.sample_id in seen_ids:
            raise ContractValidationError(f"duplicate sample_id: {contract.sample_id}")
        contract_family = (
            contract.symbol,
            contract.decision_date.strftime("%Y-%m-%d"),
            contract.direction,
            contract.primary_pattern,
            contract.internal_label,
            contract.lineage_id,
        )
        if contract_family in seen_contract_families:
            raise ContractValidationError(
                "duplicate contract family (same symbol/date/direction/pattern/label/lineage); "
                "choose one order branch before replay: "
                f"{contract.symbol}/{contract.decision_date.strftime('%Y-%m-%d')}/"
                f"{contract.primary_pattern}/{contract.internal_label}/{contract.lineage_id}"
            )
        seen_ids.add(contract.sample_id)
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
        "order_branch": contract.order_branch,
        "event_context": contract.event_context,
        "label_source": contract.label_source,
        "daily_context_window": contract.daily_context_window,
        "major_high_low_review": contract.major_high_low_review,
        "ema20_50_200_review": contract.ema20_50_200_review,
        "contract_frozen": contract.contract_frozen,
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
) -> pd.Timestamp | None:
    # Protective orders are attached after the entry bar is observed.  The
    # entry bar is therefore intentionally excluded from this check.
    for bar_number in range(entry_bar + 1, min(exit_bar, len(prices) - 1) + 1):
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


def run_contract(
    contract: BacktestContract,
    prices: pd.DataFrame,
    *,
    commission: float = 0.0,
    spread: float = 0.0,
    cash: float = 1_000_000.0,
) -> dict[str, Any]:
    """Replay one frozen contract and return one auditable result row."""

    if commission < 0 or spread < 0:
        raise ValueError("commission and spread must be non-negative")
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
                if contract.order_branch == "market_close":
                    if contract.direction == "long":
                        self.buy(size=1, tag=contract.sample_id)
                    else:
                        self.sell(size=1, tag=contract.sample_id)
                elif contract.order_branch == "stop_confirmation":
                    if contract.direction == "long":
                        self.buy(stop=contract.entry_trigger, size=1, tag=contract.sample_id)
                    else:
                        self.sell(stop=contract.entry_trigger, size=1, tag=contract.sample_id)
                elif contract.order_branch == "limit_retest":
                    if contract.direction == "long":
                        self.buy(limit=contract.entry_trigger, size=1, tag=contract.sample_id)
                    else:
                        self.sell(limit=contract.entry_trigger, size=1, tag=contract.sample_id)
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
                    for trade in active_trades:
                        # Attach exits only after the entry bar has completed.
                        # This avoids backtesting.py's documented ambiguity when
                        # a contingent SL/TP is hit in the parent entry candle.
                        trade.sl = contract.structural_stop
                        trade.tp = contract.target_price
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
        result = _base_result(contract, fill_status="no-fill", reason="no-entry-fill")
        result["gap_through"] = bool(opportunity["gap_through"])
        if opportunity["gap_through"]:
            result["gap_adjustment"] = "accepted_open" if contract.gap_policy == "accept_open" else "flag_only"
        result["engine_warnings"] = " | ".join(str(item.message) for item in captured_warnings)
        return result
    if len(trades) != 1:
        raise RuntimeError(f"{contract.sample_id}: expected one trade, got {len(trades)}")

    trade = trades.iloc[0]
    entry_bar = int(trade["EntryBar"])
    exit_bar = int(trade["ExitBar"])
    entry_price = float(trade["EntryPrice"])
    exit_price = float(trade["ExitPrice"])
    risk_per_unit = abs(entry_price - contract.structural_stop)
    if risk_per_unit <= 0:
        raise ContractValidationError(f"{contract.sample_id}: realized risk is zero")
    strategy_state = stats["_strategy"]
    time_exit_submitted = bool(getattr(strategy_state, "_time_exit_submitted", False))
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
    ambiguous_date = _find_ambiguous_bar(
        symbol_prices,
        contract.direction,
        contract.structural_stop,
        contract.target_price,
        entry_bar,
        path_end_bar,
    )
    obstacle_hit = _first_obstacle_hit(
        symbol_prices,
        contract.direction,
        contract.first_obstacle,
        entry_bar,
        path_end_bar,
    )
    if ambiguous_date is not None:
        exit_reason = "ambiguous_intrabar_stop_target"
        trade_result = "pending"
        path_result = "ambiguous"
        realized_r: float | None = None
        evidence_status = "excluded_ambiguous"
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
                "first-obstacle-reached" if obstacle_hit else (
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
                if ambiguous_date is not None and obstacle_hit
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


def _prepare_result_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize result fields before any denominator or group calculation."""

    if "trade_result" not in frame:
        frame["trade_result"] = ""
    frame["trade_result"] = frame["trade_result"].fillna("").astype(str).str.strip().str.lower()
    result_labels = frame["trade_result"].isin(TRADE_RESULTS)

    if "win_rate_eligible" not in frame:
        frame["win_rate_eligible"] = np.where(result_labels, "yes", "no")
    frame["win_rate_eligible"] = (
        frame["win_rate_eligible"].fillna("").astype(str).str.strip().str.lower()
    )
    eligible_flags = frame["win_rate_eligible"].eq("yes")

    if "evidence_status" not in frame:
        frame["evidence_status"] = np.where(
            result_labels & eligible_flags,
            "comparable",
            "excluded",
        )
    frame["evidence_status"] = frame["evidence_status"].fillna("").astype(str).str.strip().str.lower()
    if "fill_status" not in frame:
        frame["fill_status"] = np.where(
            result_labels & eligible_flags,
            "filled",
            "unknown",
        )
    frame["fill_status"] = frame["fill_status"].fillna("").astype(str).str.strip().str.lower()
    if "ambiguous_intrabar" not in frame:
        frame["ambiguous_intrabar"] = "no"
    frame["ambiguous_intrabar"] = (
        frame["ambiguous_intrabar"].fillna("no").astype(str).str.strip().str.lower()
    )
    if "path_result" not in frame:
        frame["path_result"] = ""
    frame["path_result"] = frame["path_result"].fillna("").astype(str).str.strip().str.lower()
    if "realized_R" not in frame:
        frame["realized_R"] = None
    return frame


def _completed_trade_mask(frame: pd.DataFrame) -> pd.Series:
    """Return the strict, auditable win-rate denominator mask."""

    realized_r = pd.to_numeric(frame["realized_R"], errors="coerce")
    return (
        frame["trade_result"].isin(TRADE_RESULTS)
        & frame["win_rate_eligible"].eq("yes")
        & frame["evidence_status"].eq("comparable")
        & frame["fill_status"].eq("filled")
        & frame["ambiguous_intrabar"].ne("yes")
        & frame["path_result"].ne("ambiguous")
        & frame["path_result"].ne("incomplete-horizon")
        & realized_r.notna()
        & np.isfinite(realized_r)
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
    opening_skip = (~completed) & frame["fill_status"].eq("opening-skip")
    buckets.loc[opening_skip] = "opening_skip"
    no_fill = (~completed) & frame["fill_status"].eq("no-fill")
    buckets.loc[no_fill] = "no_fill"
    unproven = (~completed) & frame["fill_status"].eq("unproven")
    buckets.loc[unproven] = "unproven"
    observation_only = (~completed) & (
        frame["fill_status"].eq("not-traded") | frame["evidence_status"].eq("observation_only")
    )
    buckets.loc[observation_only] = "observation_only"
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
        "lineage_id": group["lineage_id"].iloc[0],
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
    ]
    for column in stratification_columns:
        if column not in frame:
            frame[column] = ""
    if "event_context" not in frame:
        frame["event_context"] = ""
    if "event_bucket" not in frame:
        frame["event_bucket"] = frame["event_context"].fillna("").map(_event_bucket)
    else:
        missing_event_bucket = frame["event_bucket"].fillna("").astype(str).str.strip() == ""
        frame.loc[missing_event_bucket, "event_bucket"] = (
            frame.loc[missing_event_bucket, "event_context"].fillna("").map(_event_bucket)
        )
    if "space_status" not in frame:
        frame["space_status"] = ""
    if "pre_entry_space_R" not in frame:
        frame["pre_entry_space_R"] = None
    if "contract_space_bucket" not in frame:
        frame["contract_space_bucket"] = [
            _contract_space_bucket(status, space_r)
            for status, space_r in zip(frame["space_status"], frame["pre_entry_space_R"])
        ]
    else:
        missing_space_bucket = frame["contract_space_bucket"].fillna("").astype(str).str.strip() == ""
        frame.loc[missing_space_bucket, "contract_space_bucket"] = [
            _contract_space_bucket(status, space_r)
            for status, space_r in zip(
                frame.loc[missing_space_bucket, "space_status"],
                frame.loc[missing_space_bucket, "pre_entry_space_R"],
            )
        ]

    completed_mask = _completed_trade_mask(frame)
    completed = frame[completed_mask]
    r_values = pd.to_numeric(completed["realized_R"], errors="coerce").dropna()
    wins = int((completed["trade_result"] == "win").sum())
    lineage_values = frame["lineage_id"].fillna("").astype(str).str.strip()
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
    if missing_lineage_count:
        independence_status = "missing_lineage"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_missing_lineage"
    elif shared_lineage_group_count:
        independence_status = "dependent_lineage_rows_present"
        independence_adjusted_win_rate = None
        independence_statistics_status = "not-computable_shared_lineage"
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
            "win_rate_pct is row-based descriptive output; an independence-adjusted rate is withheld when lineages are shared or missing",
            "event_bucket is conservative; event-unverified, pending, unknown and unclassified contexts are never upgraded to ordinary_non_event",
            "ordinary_non_event_strict_space statistics use only explicit pre-entry space evidence; blank legacy space fields remain unknown",
            "H1/H2/L1/L2 require the matching Daily EMA20/EMA50 slope gate; failed gates remain observation_only and are excluded",
            "META is recorded and stratified as a confluence field; it is not an entry trigger or authorization",
        ],
    }
    grouping_columns = stratification_columns
    group_columns = [
        "primary_pattern",
        "internal_label",
        "direction",
        *grouping_columns,
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


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.commission < 0 or args.spread < 0 or args.cash <= 0:
        raise SystemExit("commission/spread must be non-negative and cash must be positive")
    prices = load_prices(args.prices, default_symbol=args.symbol)
    contracts = load_contracts(args.contracts)
    results = run_contracts(
        contracts,
        prices,
        commission=args.commission,
        spread=args.spread,
        cash=args.cash,
    )
    summary = build_summary(results)
    summary["run_metadata"] = {
        "data_source": args.data_source,
        "data_status": args.data_status,
        "as_of_time": args.as_of_time,
        "price_file": str(Path(args.prices).resolve()),
        "contract_file": str(Path(args.contracts).resolve()),
        "commission": args.commission,
        "spread": args.spread,
        "cash": args.cash,
        "scope": "PA Research only; no scanner; no Execution Agent; no Codex Trading changes",
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(results).to_csv(output_dir / "results.csv", index=False)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=_json_default) + "\n",
        encoding="utf-8",
    )
    (output_dir / "run_metadata.json").write_text(
        json.dumps(summary["run_metadata"], ensure_ascii=False, indent=2, default=_json_default) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=_json_default))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
