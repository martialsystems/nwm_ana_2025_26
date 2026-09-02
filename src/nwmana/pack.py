# Copyright (c) 2026 Martial Systems LLC
"""Daily Q at four gages: USGS and AnA, aligned."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class GagePack:
    """One row per day. Arrays are (n_days, n_gages) in GAGES order."""

    dates: np.ndarray
    usgs_cfs: np.ndarray
    nwm_cfs: np.ndarray
    gage_ids: tuple[str, ...]
    source: str = "fixture"
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def n_days(self) -> int:
        return int(self.dates.shape[0])

    @property
    def n_gages(self) -> int:
        return int(self.usgs_cfs.shape[1])

    def residual_cfs(self) -> np.ndarray:
        return np.asarray(self.nwm_cfs, dtype=float) - np.asarray(self.usgs_cfs, dtype=float)
