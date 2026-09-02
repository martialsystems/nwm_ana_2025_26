# Copyright (c) 2026 Martial Systems LLC

import pytest

from nwmana.claims import require_ana_table_not_v21, require_clean, scan_text
from nwmana.errors import ClaimBanError, MixRetroError


def test_allowed_and_banned() -> None:
    assert scan_text("AnA versus yesterday 00060 at Nora") == []
    assert "forecast" in scan_text("P(sfha | hydro) is a forecast")
    assert "nwm_now_wins" in scan_text("NWM now wins on the White River")
    assert "ana_as_forecast" in scan_text("AnA is a forecast")
    assert "ana_vs_v21_nora" in scan_text("Nora 301 vs 1,316 means NWM improved")
    with pytest.raises(ClaimBanError):
        require_clean("flood warning", source="t")


def test_ana_table_cannot_reuse_v21_rmse() -> None:
    good = "| Gage | Yesterday | AnA |\n| Nora | 900 | 1100 |\n"
    require_ana_table_not_v21(good, source="t")
    bad = "| Gage | Yesterday | AnA |\n| Nora | 1,243 | 1,316 |\n"
    with pytest.raises(MixRetroError):
        require_ana_table_not_v21(bad, source="t")
