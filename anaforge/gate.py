# Copyright (c) 2026 Martial Systems LLC
"""Call sites for the five refuse laws."""

from __future__ import annotations

from typing import Any

from anaforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from anaforge.graphs.fetch_or_stop import build_graph as build_fetch
from anaforge.graphs.no_mix_v21 import build_graph as build_mix
from anaforge.graphs.not_forecast import build_graph as build_caption
from anaforge.graphs.persistence_bar import build_graph as build_bar
from anaforge.graphs.window import build_graph as build_window


def _run(build, law_id: str, state: dict[str, Any], thread_id: str) -> None:
    require_law(
        build(),
        state,
        allow_decisions=["allow"],
        law_id=law_id,
        thread_id=thread_id,
        raise_error=True,
    )


def require_fetch(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ana_fetch"))
    state = {"missing_day": True}
    state.update(flags)
    _run(build_fetch, "ana.fetch_or_stop", state, thread_id)


def require_window(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ana_window"))
    state = {"in_window": False, "outside_window": True}
    state.update(flags)
    _run(build_window, "ana.window", state, thread_id)


def require_mix(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ana_mix"))
    state = {"mixed_v21_table": True}
    state.update(flags)
    _run(build_mix, "ana.no_mix_v21", state, thread_id)


def require_bar(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ana_bar"))
    state = {"persistence_is_bar": False}
    state.update(flags)
    _run(build_bar, "ana.persistence_bar", state, thread_id)


def require_caption(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ana_caption"))
    state = {"captioned_as_forecast": True, "is_tm00_analysis": False}
    state.update(flags)
    _run(build_caption, "ana.not_forecast", state, thread_id)
