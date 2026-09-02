# Copyright (c) 2026 Martial Systems LLC
"""Five refuse laws. Verify-before-done is the finish gate. Science 4fdedca."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from anaforge.graphs.fetch_or_stop import build_graph as fetch_or_stop
    from anaforge.graphs.no_mix_v21 import build_graph as no_mix_v21
    from anaforge.graphs.not_forecast import build_graph as not_forecast
    from anaforge.graphs.persistence_bar import build_graph as persistence_bar
    from anaforge.graphs.window import build_graph as window

    return [
        {
            "id": "ana.fetch_or_stop",
            "build": fetch_or_stop,
            "state": {"missing_day": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "ana.window",
            "build": window,
            "state": {"in_window": True, "outside_window": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "ana.no_mix_v21",
            "build": no_mix_v21,
            "state": {"mixed_v21_table": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "ana.persistence_bar",
            "build": persistence_bar,
            "state": {"persistence_is_bar": True},
            "allow_decisions": ["allow"],
        },
        {
            "id": "ana.not_forecast",
            "build": not_forecast,
            "state": {"captioned_as_forecast": False, "is_tm00_analysis": True},
            "allow_decisions": ["allow"],
        },
    ]
