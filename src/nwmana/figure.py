# Copyright (c) 2026 Martial Systems LLC
"""Two figures: Nora hydrograph, then four-gage residual strip."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from nwmana.claims import require_clean
from nwmana.config import GAGES, MAX_FIGURES, NORA_ID
from nwmana.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_hydrograph(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ho = fit["holdout"]
    dates = [datetime.strptime(str(x)[:10], "%Y-%m-%d") for x in ho["dates"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(dates, ho["usgs_cfs"], color="#222222", lw=1.4, label="USGS Q")
    ax.plot(dates, ho["persistence_cfs"], color="#7a7a7a", lw=1.0, ls="--", label="persistence")
    ax.plot(dates, ho["nwm_cfs"], color="#1b6ca8", lw=1.2, label="AnA Q")
    ax.set_ylabel("discharge (cfs)")
    ax.set_title(title, fontsize=10)
    ax.legend(loc="upper left", fontsize=7, frameon=False, ncol=3)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.12, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_residual_strip(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [str(g["name"]) for g in GAGES]
    bias = np.asarray(fit["mean_bias_cfs"], dtype=float)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    colors = ["#b36b00" if b > 0 else "#1b6ca8" for b in bias]
    ax.bar(range(len(names)), bias, color=colors)
    ax.axhline(0.0, color="#333333", lw=0.8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, fontsize=9)
    ax.set_ylabel("mean (AnA minus USGS) cfs")
    ax.set_title(title, fontsize=10)
    fig.text(0.5, 0.03, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.16, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any]) -> list[Path]:
    paths = [
        write_hydrograph(
            log_dir / "hydrograph.png",
            fit=fit,
            title=f"{NORA_ID} Nora: USGS, persistence, operational AnA",
            subtitle="2025 to August 2026. AnA is t12z tm00. Persistence is yesterday 00060. cfs, not feet.",
        ),
        write_residual_strip(
            log_dir / "residual_strip.png",
            fit=fit,
            title="AnA minus USGS, not water",
            subtitle="Same four gages as fa2e315. This strip is operational AnA, not v2.1 retro.",
        ),
    ]
    _cap(len(paths))
    return paths
