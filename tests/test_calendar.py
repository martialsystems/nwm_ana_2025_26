# Copyright (c) 2026 Martial Systems LLC

from datetime import date

import pytest

from nwmana.calendar import require_in_window, window_days
from nwmana.errors import FetchError


def test_window_is_2025_through_august_2026() -> None:
    days = window_days()
    assert days[0] == date(2025, 1, 1)
    assert days[-1] == date(2026, 8, 31)
    assert len(days) == 608
    with pytest.raises(FetchError):
        require_in_window(date(2024, 12, 31))
    with pytest.raises(FetchError):
        require_in_window(date(2021, 6, 15))
    with pytest.raises(FetchError):
        require_in_window(date(2026, 9, 1))
    with pytest.raises(FetchError):
        window_days(start=date(2024, 1, 1), end=date(2025, 1, 31))
