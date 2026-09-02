# Copyright (c) 2026 Martial Systems LLC
"""Locked AnA 2025 to August 2026 contract. Do not restamp fa2e315."""

from __future__ import annotations

from datetime import date
from pathlib import Path

QUESTION = (
    "Does operational NWM analysis-assim beat yesterday's flow on the White "
    "River in 2025 to August 2026?"
)
# Same four gages as fa2e315. Official NWIS names.
GAGES: tuple[dict[str, str | int], ...] = (
    {"id": "03348000", "name": "Anderson", "comid": 18474953, "nws": ""},
    {"id": "03351000", "name": "Nora", "comid": 18476353, "nws": "NORI3"},
    {"id": "03353000", "name": "Indianapolis", "comid": 18476879, "nws": "INDI3"},
    {"id": "03354000", "name": "Centerton", "comid": 18477453, "nws": ""},
)
NORA_ID = "03351000"
GAGE_IDS = tuple(str(g["id"]) for g in GAGES)
COMIDS = tuple(int(g["comid"]) for g in GAGES)
LOCKED_V21 = "fa2e315"
WINDOW_START = date(2025, 1, 1)
WINDOW_END = date(2026, 8, 31)
# Files exist on 2026-09-01; this tree still cuts at August 2026.
REFUSED_AFTER = date(2026, 9, 1)
REFUSED_BEFORE = date(2025, 1, 1)
MAX_FIGURES = 2
CMS_TO_CFS = 35.314666212661
USER_AGENT = "MartialSystemsResearch/nwm_ana_2025_26"
NWIS_DV_URL = (
    "https://waterservices.usgs.gov/nwis/dv/?format=json&sites={site}"
    "&startDT={start}&endDT={end}&parameterCd={code}&siteStatus=all"
)
ANA_BUCKET = "noaa-nwm-pds"
ANA_KEY = (
    "nwm.{yyyymmdd}/analysis_assim/nwm.t12z.analysis_assim.channel_rt.tm00.conus.nc"
)
ANA_HTTP = "https://noaa-nwm-pds.s3.amazonaws.com/" + ANA_KEY
ANA_S3 = "s3://noaa-nwm-pds/" + ANA_KEY
ANA_MIN_BYTES = 1_000_000
# v2.1 holdout RMSE must not appear in this tree's skill table.
V21_RMSE_TOKENS = (
    "1,243",
    "1,316",
    "1,450",
    "1,994",
    "1,795",
    "2,414",
    "676",
    "488",
)
INDEX_GIST = "https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3"
HYDRO_GIST = "https://gist.github.com/martialsystems/1104e5e47b8a04006ec694d289d43639"
PARENT_REPO = "https://github.com/martialsystems/white_river_nwm_error"
REPO_ROOT = Path(__file__).resolve().parents[2]
