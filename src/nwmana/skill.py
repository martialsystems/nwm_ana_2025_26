# Copyright (c) 2026 Martial Systems LLC
"""AnA versus lag-1 00060. Persistence is the bar. No v2.1 mix-in."""

from __future__ import annotations

from typing import Any

import numpy as np

from nwmana.config import GAGE_IDS, LOCKED_V21, NORA_ID
from nwmana.pack import GagePack


def rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    err = np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float)
    ok = np.isfinite(err)
    if not ok.any():
        return float("nan")
    e = err[ok]
    return float(np.sqrt(np.mean(e * e)))


def mae(y: np.ndarray, yhat: np.ndarray) -> float:
    err = np.abs(np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float))
    ok = np.isfinite(err)
    if not ok.any():
        return float("nan")
    return float(np.mean(err[ok]))


def _skill(y: np.ndarray, yhat: np.ndarray) -> dict[str, float]:
    return {"rmse_cfs": rmse(y, yhat), "mae_cfs": mae(y, yhat)}


def _lag1(arr: np.ndarray) -> np.ndarray:
    out = np.full(arr.shape, np.nan, dtype=float)
    out[1:] = np.asarray(arr, dtype=float)[:-1]
    return out


def score_pack(pack: GagePack) -> dict[str, Any]:
    usgs = np.asarray(pack.usgs_cfs, dtype=float)
    nwm = np.asarray(pack.nwm_cfs, dtype=float)
    pers = _lag1(usgs)
    ok = np.isfinite(usgs) & np.isfinite(nwm) & np.isfinite(pers)
    per_gage: list[dict[str, Any]] = []
    mean_bias = np.full(pack.n_gages, np.nan)
    for g, gid in enumerate(GAGE_IDS):
        ho = ok[:, g]
        if int(ho.sum()) < 2:
            raise ValueError(f"no comparable AnA/USGS rows for {gid}")
        y_ho, nwm_ho, pers_ho = usgs[ho, g], nwm[ho, g], pers[ho, g]
        per_gage.append(
            {
                "id": gid,
                "n_days": int(ho.sum()),
                "skill": {
                    "persistence": _skill(y_ho, pers_ho),
                    "ana": _skill(y_ho, nwm_ho),
                },
                "bias_cfs": float(np.nanmean(nwm_ho - y_ho)),
                "ana_beats_persistence": bool(
                    _skill(y_ho, nwm_ho)["rmse_cfs"] < _skill(y_ho, pers_ho)["rmse_cfs"]
                ),
            }
        )
        mean_bias[g] = per_gage[-1]["bias_cfs"]
    nora = GAGE_IDS.index(NORA_ID)
    ho = ok[:, nora]
    return {
        "gages": per_gage,
        "mean_bias_cfs": mean_bias,
        "source": pack.source,
        "v21_citation": LOCKED_V21,
        "mixed_v21_table": False,
        "holdout": {
            "dates": pack.dates[ho],
            "usgs_cfs": usgs[ho, nora],
            "nwm_cfs": nwm[ho, nora],
            "persistence_cfs": pers[ho, nora],
        },
    }
