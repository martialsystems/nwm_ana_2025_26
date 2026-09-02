# Copyright (c) 2026 Martial Systems LLC
"""Pinned AnA window. 2021-2024 and post-August 2026 are refused."""

from __future__ import annotations

from datetime import date, timedelta

from nwmana.config import REFUSED_AFTER, REFUSED_BEFORE, WINDOW_END, WINDOW_START
from nwmana.errors import FetchError


def window_days(
    *,
    start: date = WINDOW_START,
    end: date = WINDOW_END,
) -> list[date]:
    if start < REFUSED_BEFORE:
        raise FetchError(f"{start.isoformat()} is before the AnA window {WINDOW_START}")
    if end >= REFUSED_AFTER:
        raise FetchError(f"{end.isoformat()} is after August 2026")
    if end < start:
        raise FetchError("empty AnA window")
    out: list[date] = []
    d = start
    while d <= end:
        out.append(d)
        d += timedelta(days=1)
    return out


def require_in_window(day: date) -> date:
    if day < WINDOW_START or day > WINDOW_END:
        raise FetchError(
            f"{day.isoformat()} is outside 2025-01-01 to 2026-08-31. "
            "Do not mix 2021-2024 AnA or restamp fa2e315."
        )
    return day
