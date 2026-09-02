# Copyright (c) 2026 Martial Systems LLC
"""Refuse a silent skip when an AnA day 404s."""

from __future__ import annotations

from typing import Any

from anaforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations = ["missing_ana_day"] if state.get("missing_day") else []
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="ana.fetch_or_stop",
        evaluate=_evaluate,
        extra=[("missing_day", True)],
    )
