# Copyright (c) 2026 Martial Systems LLC

from datetime import date

import pytest

from nwmana.ana import fetch_ana_daily, head_day
from nwmana.errors import FetchError


def test_head_404_is_stop() -> None:
    def boom(url: str) -> int:
        raise FetchError(f"GET empty or 404: {url}")

    with pytest.raises(FetchError, match="404"):
        head_day(date(2025, 1, 2), head_fn=boom)


def test_fetch_stops_on_first_missing_day() -> None:
    seen: list[date] = []

    def head_fn(url: str) -> int:
        if "20250103" in url:
            raise FetchError(f"GET empty or 404: {url}")
        return 12_000_000

    def extract_fn(day: date) -> dict[int, float]:
        seen.append(day)
        return {18474953: 1.0, 18476353: 2.0, 18476879: 3.0, 18477453: 4.0}

    with pytest.raises(FetchError, match="404"):
        fetch_ana_daily(
            start=date(2025, 1, 1),
            end=date(2025, 1, 5),
            head_fn=head_fn,
            extract_fn=extract_fn,
            workers=1,
        )
    assert seen == []
