# Copyright (c) 2026 Martial Systems LLC
"""Refuse scoring AnA without yesterday 00060 as the bar."""

from __future__ import annotations

from typing import Any

from anaforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations = [] if state.get("persistence_is_bar") else ["persistence_not_the_bar"]
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="ana.persistence_bar",
        evaluate=_evaluate,
        extra=[("persistence_is_bar", False)],
    )
