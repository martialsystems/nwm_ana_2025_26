# Copyright (c) 2026 Martial Systems LLC
"""NWIS daily 00060 at the four White River gages."""

from __future__ import annotations

from datetime import date
from typing import Any

import numpy as np

from nwmana.config import GAGE_IDS, NWIS_DV_URL
from nwmana.errors import FetchError
from nwmana.http import get_json


def _time_series(doc: dict[str, Any]) -> list[dict[str, Any]]:
    blob = doc.get("value") if isinstance(doc.get("value"), dict) else doc
    return list((blob or {}).get("timeSeries") or [])


def parse_dv_q(doc: dict[str, Any]) -> dict[np.datetime64, float]:
    out: dict[np.datetime64, float] = {}
    for ts in _time_series(doc):
        var = ((ts.get("variable") or {}).get("variableCode") or [{}])[0]
        if str(var.get("value") or "") != "00060":
            continue
        rows = ((ts.get("values") or [{}])[0]).get("value") or []
        for rec in rows:
            stamp = str(rec.get("dateTime") or "")[:10]
            try:
                val = float(rec.get("value"))
            except (TypeError, ValueError):
                continue
            if stamp and np.isfinite(val):
                out[np.datetime64(stamp)] = val
    return out


def fetch_usgs_q(
    *,
    start: date,
    end: date,
    sites: tuple[str, ...] = GAGE_IDS,
    get_json_fn=None,
) -> dict[str, dict[np.datetime64, float]]:
    getter = get_json_fn or get_json
    out: dict[str, dict[np.datetime64, float]] = {}
    for site in sites:
        doc = getter(
            NWIS_DV_URL.format(
                site=site, start=start.isoformat(), end=end.isoformat(), code="00060"
            )
        )
        series = parse_dv_q(doc)
        if not series:
            raise FetchError(f"NWIS daily 00060 is empty for {site}")
        out[site] = series
    return out
