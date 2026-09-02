# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 fixture. Live fetch-or-stop per day. Two figures max."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwmana.ana import align_pack, fetch_ana_daily
from nwmana.calendar import window_days
from nwmana.claims import require_ana_table_not_v21, require_clean, require_paths_clean
from nwmana.config import (
    GAGE_IDS,
    LOCKED_V21,
    NORA_ID,
    QUESTION,
    WINDOW_END,
    WINDOW_START,
)
from nwmana.figure import write_two
from nwmana.fixture import build_fixture
from nwmana.nwis import fetch_usgs_q
from nwmana.skill import score_pack

from anaforge.gate import require_bar, require_caption, require_fetch, require_mix, require_window


def _jsonable(report: dict[str, Any]) -> dict[str, Any]:
    skip = {"holdout", "mean_bias_cfs"}
    return {k: v for k, v in report.items() if k not in skip}


def _run(log_dir: Path, *, pack, fixture: bool, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    require_clean(QUESTION, source="question")
    require_fetch(missing_day=False, thread_id="run.fetch")
    require_window(in_window=True, outside_window=False, thread_id="run.window")
    require_mix(mixed_v21_table=False, thread_id="run.mix")
    require_bar(persistence_is_bar=True, thread_id="run.bar")
    require_caption(
        captioned_as_forecast=False, is_tm00_analysis=True, thread_id="run.caption"
    )
    fit = score_pack(pack)
    paths = write_two(log_dir, fit=fit)
    log_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "stage": "0" if fixture else "C",
        "fixture": fixture,
        "question": QUESTION,
        "gage_ids": list(GAGE_IDS),
        "nora_id": NORA_ID,
        "n_days": pack.n_days,
        "source": pack.source,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "v21_citation": LOCKED_V21,
        "mixed_v21_table": False,
        "captioned_as_forecast": False,
        "is_tm00_analysis": True,
        "gages": fit["gages"],
        "figures": [p.name for p in paths],
        "holdout": fit["holdout"],
    }
    if extra:
        report.update({k: v for k, v in extra.items() if k != "holdout"})
    name = "stage0_report.json" if fixture else "stage_c_report.json"
    payload = _jsonable(report)
    text = json.dumps(payload, indent=2, default=str) + "\n"
    (log_dir / name).write_text(text)
    require_paths_clean([log_dir / name])
    require_ana_table_not_v21(text, source=name)
    return report


def stage0_fixture(log_dir: Path) -> dict[str, Any]:
    return _run(log_dir, pack=build_fixture(), fixture=True)


def run_live(log_dir: Path, *, cache_dir: Path | None = None) -> dict[str, Any]:
    days = window_days()
    usgs = fetch_usgs_q(start=WINDOW_START, end=WINDOW_END)
    ana = fetch_ana_daily(start=WINDOW_START, end=WINDOW_END, cache_dir=cache_dir)
    pack = align_pack(dates=days, usgs=usgs, ana=ana)
    return _run(
        log_dir,
        pack=pack,
        fixture=False,
        extra={"n_head_days": len(days), "fetch_or_stop": True},
    )
