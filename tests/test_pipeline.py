# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from nwmana.config import LOCKED_V21, QUESTION
from nwmana.pipeline import stage0_fixture


def test_fixture_stage0(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["v21_citation"] == LOCKED_V21
    assert report["mixed_v21_table"] is False
    assert report["captioned_as_forecast"] is False
    assert report["is_tm00_analysis"] is True
    assert report["source"] == "fixture"
    assert (tmp_path / "hydrograph.png").is_file()
    assert (tmp_path / "residual_strip.png").is_file()
    assert (tmp_path / "stage0_report.json").is_file()
    assert all(g["skill"]["ana"]["rmse_cfs"] != 1316 for g in report["gages"])
