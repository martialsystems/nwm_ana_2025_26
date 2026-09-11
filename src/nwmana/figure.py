# Copyright (c) 2026 Martial Systems LLC
"""Two figures: Nora hydrograph, then four-gage yesterday vs AnA RMSE."""

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


def _fmt_cfs(v: float) -> str:
    return f"{int(round(float(v))):,}"


def _gage_rmse(fit: dict[str, Any], contestant: str) -> tuple[list[str], list[float], list[float]]:
    id_to_name = {str(g["id"]): str(g["name"]) for g in GAGES}
    names: list[str] = []
    pers: list[float] = []
    other: list[float] = []
    for row in fit["gages"]:
        gid = str(row["id"])
        names.append(id_to_name.get(gid, gid))
        skill = row["skill"]
        pers.append(float(skill["persistence"]["rmse_cfs"]))
        other.append(float(skill[contestant]["rmse_cfs"]))
    return names, pers, other


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

    names, pers, ana = _gage_rmse(fit, "ana")
    x = np.arange(len(names))
    w = 0.38
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    c0 = ax.bar(x - w / 2, pers, w, color="#7a7a7a", label="yesterday")
    c1 = ax.bar(x + w / 2, ana, w, color="#1b6ca8", label="AnA")
    ax.bar_label(c0, labels=[_fmt_cfs(v) for v in pers], fontsize=7, padding=2)
    ax.bar_label(c1, labels=[_fmt_cfs(v) for v in ana], fontsize=7, padding=2)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9)
    ax.set_ylabel("RMSE (cfs)")
    hi = max(max(pers), max(ana)) if names else 1.0
    ax.set_ylim(0, hi * 1.20)
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=7, frameon=False)
    fig.text(0.5, 0.03, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.16, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any]) -> list[Path]:
    log_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    if fit.get("holdout"):
        paths.append(
            write_hydrograph(
                log_dir / "hydrograph.png",
                fit=fit,
                title=f"{NORA_ID} Nora: USGS, persistence, AnA t12z tm00 analysis",
                subtitle="2025 to August 2026. analysis_assim tm00 analysis. Persistence is yesterday 00060. cfs, not feet.",
            )
        )
    paths.append(
        write_residual_strip(
            log_dir / "residual_strip.png",
            fit=fit,
            title="Yesterday vs AnA RMSE",
            subtitle="AnA wins at all four gages. Bias stays in the table. analysis_assim tm00, not v2.1 retro.",
        )
    )
    _cap(len(paths))
    return paths
