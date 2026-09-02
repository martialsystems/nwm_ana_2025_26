# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from anaforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from anaforge.gate import require_bar, require_caption, require_fetch, require_mix, require_window
from anaforge.product_laws import laws


def test_fetch_and_window() -> None:
    require_fetch(missing_day=False, thread_id="t.f.ok")
    with pytest.raises(LawBlockedError):
        require_fetch(thread_id="t.f.default")
    require_window(in_window=True, outside_window=False, thread_id="t.w.ok")
    with pytest.raises(LawBlockedError):
        require_window(in_window=True, outside_window=True, thread_id="t.w.out")


def test_mix_and_bar() -> None:
    require_mix(mixed_v21_table=False, thread_id="t.m.ok")
    with pytest.raises(LawBlockedError):
        require_mix(thread_id="t.m.default")
    require_bar(persistence_is_bar=True, thread_id="t.b.ok")
    with pytest.raises(LawBlockedError):
        require_bar(thread_id="t.b.default")


def test_caption_blocks_forecast() -> None:
    require_caption(captioned_as_forecast=False, is_tm00_analysis=True, thread_id="t.c.ok")
    with pytest.raises(LawBlockedError):
        require_caption(thread_id="t.c.default")
    with pytest.raises(LawBlockedError):
        require_caption(
            captioned_as_forecast=True, is_tm00_analysis=True, thread_id="t.c.fcst"
        )


def test_five_laws_registry() -> None:
    ids = {row["id"] for row in laws()}
    assert ids == {
        "ana.fetch_or_stop",
        "ana.window",
        "ana.no_mix_v21",
        "ana.persistence_bar",
        "ana.not_forecast",
    }
