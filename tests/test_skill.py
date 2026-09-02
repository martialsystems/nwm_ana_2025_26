# Copyright (c) 2026 Martial Systems LLC

from nwmana.config import LOCKED_V21, NORA_ID
from nwmana.fixture import build_fixture
from nwmana.skill import score_pack


def test_persistence_is_the_bar_on_fixture() -> None:
    fit = score_pack(build_fixture())
    assert fit["v21_citation"] == LOCKED_V21
    assert fit["mixed_v21_table"] is False
    assert fit["source"] == "fixture"
    nora = next(g for g in fit["gages"] if g["id"] == NORA_ID)
    assert nora["skill"]["persistence"]["rmse_cfs"] < nora["skill"]["ana"]["rmse_cfs"]
    for g in fit["gages"]:
        assert "nwm_v21" not in g["skill"]
        assert "ana" in g["skill"]
        assert "persistence" in g["skill"]
