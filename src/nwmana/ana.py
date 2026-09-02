# Copyright (c) 2026 Martial Systems LLC
"""Operational AnA t12z tm00 at four COMIDs. Fetch-or-stop per day."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import numpy as np

from nwmana.calendar import require_in_window, window_days
from nwmana.config import (
    ANA_HTTP,
    ANA_MIN_BYTES,
    ANA_S3,
    CMS_TO_CFS,
    COMIDS,
    GAGES,
    REPO_ROOT,
)
from nwmana.errors import FetchError
from nwmana.http import head_bytes

NWM_MISSING = -999900
NWM_SCALE = 0.009999999776482582


def ana_http(day: date) -> str:
    require_in_window(day)
    return ANA_HTTP.format(yyyymmdd=f"{day:%Y%m%d}")


def ana_s3(day: date) -> str:
    require_in_window(day)
    return ANA_S3.format(yyyymmdd=f"{day:%Y%m%d}")


def head_day(day: date, *, head_fn=None) -> int:
    fn = head_fn or head_bytes
    n = int(fn(ana_http(day)))
    if n < ANA_MIN_BYTES:
        raise FetchError(f"AnA file too small ({n} bytes) for {day.isoformat()}")
    return n


def _extract_raw(day: date, *, comids: tuple[int, ...] = COMIDS) -> dict[int, float]:
    import fsspec
    import h5netcdf

    url = ana_s3(day)
    fs = fsspec.filesystem("s3", anon=True)
    try:
        with fs.open(url, "rb") as fh:
            with h5netcdf.File(fh, "r") as ds:
                if "streamflow" not in ds.variables or "feature_id" not in ds.variables:
                    raise FetchError(f"AnA file missing streamflow/feature_id: {url}")
                feat = np.asarray(ds["feature_id"][:], dtype=np.int64)
                sf = ds["streamflow"]
                scale = float(sf.attrs.get("scale_factor", NWM_SCALE))
                out: dict[int, float] = {}
                for c in comids:
                    hits = np.where(feat == int(c))[0]
                    if hits.size == 0:
                        raise FetchError(f"AnA has no feature_id {c} on {day.isoformat()}")
                    raw = int(np.asarray(sf[int(hits[0])]))
                    if raw == NWM_MISSING:
                        raise FetchError(f"AnA streamflow missing for {c} on {day.isoformat()}")
                    out[int(c)] = float(raw) * scale * CMS_TO_CFS
                return out
    except FetchError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise FetchError(f"AnA extract failed {day.isoformat()}: {exc}") from exc


def _cache_path(day: date, cache_dir: Path) -> Path:
    return cache_dir / f"{day:%Y%m%d}.json"


def extract_day(
    day: date,
    *,
    cache_dir: Path | None = None,
    head_fn=None,
    skip_head: bool = False,
) -> dict[int, float]:
    require_in_window(day)
    if not skip_head:
        head_day(day, head_fn=head_fn)
    dest_dir = cache_dir if cache_dir is not None else REPO_ROOT / "data" / "interim" / "ana"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = _cache_path(day, dest_dir)
    if dest.is_file():
        blob = json.loads(dest.read_text(encoding="utf-8"))
        return {int(k): float(v) for k, v in blob.items()}
    raw = _extract_raw(day)
    dest.write_text(json.dumps({str(k): v for k, v in raw.items()}) + "\n", encoding="utf-8")
    return raw


def fetch_ana_daily(
    *,
    start: date,
    end: date,
    cache_dir: Path | None = None,
    head_fn=None,
    extract_fn=None,
    workers: int = 8,
) -> dict[int, dict[np.datetime64, float]]:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    days = window_days(start=start, end=end)
    with ThreadPoolExecutor(max_workers=max(1, int(workers))) as pool:
        futs = [pool.submit(head_day, day, head_fn=head_fn) for day in days]
        for fut in futs:
            fut.result()
    getter = extract_fn or (
        lambda d: extract_day(d, cache_dir=cache_dir, head_fn=head_fn, skip_head=True)
    )
    by_day: dict[date, dict[int, float]] = {}
    with ThreadPoolExecutor(max_workers=max(1, int(workers))) as pool:
        futs = {pool.submit(getter, day): day for day in days}
        done = 0
        for fut in as_completed(futs):
            day = futs[fut]
            rec = fut.result()
            by_day[day] = rec
            done += 1
            if done == 1 or done % 50 == 0 or done == len(days):
                print(f"AnA {done}/{len(days)} {day.isoformat()}", flush=True)
    out: dict[int, dict[np.datetime64, float]] = {int(c): {} for c in COMIDS}
    for day in days:
        rec = by_day[day]
        stamp = np.datetime64(day.isoformat())
        for c in COMIDS:
            if int(c) not in rec:
                raise FetchError(f"AnA day {day.isoformat()} missing COMID {c}")
            out[int(c)][stamp] = float(rec[int(c)])
    if any(len(v) == 0 for v in out.values()):
        raise FetchError("AnA window is empty at the four COMIDs")
    return out


def align_pack(
    *,
    dates: list[date],
    usgs: dict[str, dict[np.datetime64, float]],
    ana: dict[int, dict[np.datetime64, float]],
):
    from nwmana.pack import GagePack
    from nwmana.config import GAGE_IDS

    stamps = [np.datetime64(d.isoformat()) for d in dates]
    n = len(stamps)
    q = np.full((n, len(GAGE_IDS)), np.nan, dtype=float)
    nwm = np.full((n, len(GAGE_IDS)), np.nan, dtype=float)
    for g, gage in enumerate(GAGES):
        gid = str(gage["id"])
        cid = int(gage["comid"])
        for i, stamp in enumerate(stamps):
            if stamp in usgs.get(gid, {}):
                q[i, g] = usgs[gid][stamp]
            if stamp in ana.get(cid, {}):
                nwm[i, g] = ana[cid][stamp]
    return GagePack(
        dates=np.asarray(stamps),
        usgs_cfs=q,
        nwm_cfs=nwm,
        gage_ids=GAGE_IDS,
        source="ana_2025_26",
    )
