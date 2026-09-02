# Copyright (c) 2026 Martial Systems LLC
"""Refuse putting AnA RMSE in the v2.1 column."""

from __future__ import annotations

from typing import Any

from anaforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations = ["mixed_v21_table"] if state.get("mixed_v21_table") else []
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="ana.no_mix_v21",
        evaluate=_evaluate,
        extra=[("mixed_v21_table", True)],
    )
