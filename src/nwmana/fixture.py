# Copyright (c) 2026 Martial Systems LLC
"""Synthetic 2025 window. AnA is delayed, biased USGS Q. CI needs no NOAA."""

from __future__ import annotations

from datetime import date

import numpy as np

from nwmana.config import GAGE_IDS, NORA_ID
from nwmana.pack import GagePack

FIXTURE_START = date(2025, 1, 1)
FIXTURE_END = date(2025, 3, 31)


def build_fixture(*, seed: int = 5) -> GagePack:
    rng = np.random.default_rng(seed)
    dates = np.arange(
        np.datetime64(FIXTURE_START.isoformat()),
        np.datetime64(FIXTURE_END.isoformat()) + np.timedelta64(1, "D"),
    )
    n = dates.shape[0]
    n_g = len(GAGE_IDS)
    y = dates.astype("datetime64[Y]")
    doy = (dates - y).astype("timedelta64[D]").astype(int) + 1
    seasonal = 900 + 350 * np.sin(2 * np.pi * (doy - 60) / 365.25)
    q = np.zeros((n, n_g), dtype=float)
    q[0] = seasonal[0] + np.array([180, 380, 650, 480], dtype=float)
    for t in range(1, n):
        rain = rng.gamma(0.4, 8.0)
        burst = 35.0 * rain if rng.random() < 0.08 else 0.0
        for g in range(n_g):
            rec = 0.82 - 0.04 * g
            q[t, g] = rec * q[t - 1, g] + (0.15 + 0.05 * g) * seasonal[t] + burst * (1.2 - 0.1 * g)
            q[t, g] = max(80.0, q[t, g] + rng.normal(0.0, 25.0))
    nwm = np.zeros_like(q)
    nwm[0] = q[0] * 1.16
    for t in range(1, n):
        nwm[t] = 1.16 * q[t - 1] + rng.normal(0.0, 40.0, size=n_g)
        nwm[t] = np.maximum(50.0, nwm[t])
    nwm[:, 1] *= 1.08
    return GagePack(
        dates=dates,
        usgs_cfs=q,
        nwm_cfs=nwm,
        gage_ids=GAGE_IDS,
        source="fixture",
        extra={"nora_id": NORA_ID, "nwm_bias": 1.16, "nwm_delay_days": 1},
    )
