# Copyright (c) 2026 Martial Systems LLC
"""Refuse 2021-2024 AnA and dates after 2026-08-31."""

from __future__ import annotations

from typing import Any

from anaforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not bool(state.get("in_window")):
        violations.append("ana_window_not_pinned")
    if bool(state.get("outside_window")):
        violations.append("ana_date_outside_2025_aug2026")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="ana.window",
        evaluate=_evaluate,
        extra=[("in_window", False), ("outside_window", True)],
    )
