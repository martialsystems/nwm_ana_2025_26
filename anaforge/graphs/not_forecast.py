# Copyright (c) 2026 Martial Systems LLC
"""Refuse captioning tm00 analysis as a forecast or medium-range run."""

from __future__ import annotations

from typing import Any

from anaforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if bool(state.get("captioned_as_forecast")):
        violations.append("ana_captioned_as_forecast")
    if not bool(state.get("is_tm00_analysis")):
        violations.append("ana_not_tm00_analysis")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="ana.not_forecast",
        evaluate=_evaluate,
        extra=[("captioned_as_forecast", True), ("is_tm00_analysis", False)],
    )
