# White River NWM AnA 2025 to 2026

Does operational NWM analysis-assim beat yesterday's flow on the White River in 2025 to August 2026?

Operational NWM AnA (2025-01-01 to 2026-08-31, t12z tm00) beats yesterday's USGS Q at Anderson, Nora, Indy, and Centerton. That is not the v2.1 retrospective, which only beat yesterday at Anderson. Science `4fdedca`.

What was scored is `analysis_assim` tm00: a cycling analysis that has seen recent observations. Nora 301 vs 1,179 yesterday. Anderson 252 vs 813. Indianapolis 559 vs 1,472. Centerton 622 vs 1,770. Bias is small (-6, +7, -17, +67 cfs). Fetch-or-stop covered 608 noon-UTC files. Beating yesterday with small bias is what an analysis is for. It does not reverse `fa2e315`.

Gages, upstream to downstream: **03348000 Anderson**, **03351000 Nora**, **03353000 Indianapolis**, **03354000 Centerton**. Residual is AnA minus USGS, in cfs. Noon UTC tm00 versus daily mean 00060. 2021-2024 AnA still 404.

Parent: [![white_river_nwm_error](https://img.shields.io/badge/white__river__nwm__error-2e7d32?style=for-the-badge)](https://github.com/martialsystems/white_river_nwm_error) (`fa2e315`). Do not restamp it.

![Figure 1. Nora AnA hydrograph](logs/live/hydrograph.png)

Figure 1. Live window at Nora: USGS Q, persistence, operational AnA `t12z` `tm00` analysis. Persistence RMSE 1,179 cfs; AnA 301 cfs.

![Figure 2. Residual strip](logs/live/residual_strip.png)

Figure 2. AnA minus USGS, not water. Anderson to Centerton. This is analysis_assim tm00 analysis, not v2.1 retro. Bias stays near zero except Centerton +67 cfs.

## Live skill (2025-01-01 to 2026-08-31)

608 AnA days fetched. Comparable days after lag-1 and USGS gaps: 604 / 603 / 604 / 607.

| Gage | Persistence RMSE | AnA RMSE | Bias (AnA minus USGS) |
|------|-----------------:|---------:|----------------------:|
| Anderson 03348000 | 813 | 252 | -6 |
| Nora 03351000 | 1,179 | 301 | +7 |
| Indianapolis 03353000 | 1,472 | 559 | -17 |
| Centerton 03354000 | 1,770 | 622 | +67 |

AnA analysis wins all four on RMSE and MAE. Noon UTC `tm00` versus daily mean 00060. cfs, not feet. 2021-2024 AnA still 404.

## Stage 0

Synthetic 2025 window so CI runs without S3.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/live
```

Do not use stock `/usr/bin/python3 -m pytest`. Live `run_live.py` exits 2 on a missing AnA day. Two figures max.

| File | Role |
|------|------|
| [METHODOLOGY.md](METHODOLOGY.md) | Locked contract |
| [AGENTS.md](AGENTS.md) | Agent rules |
| [CHECKLIST.md](CHECKLIST.md) | Operator list |
| `src/nwmana/` | NWIS, AnA t12z tm00, skill, figures |
| `anaforge/` | GraphForge pin: five refuse laws |

Write-up: [![White River Q](https://img.shields.io/badge/White_River_Q-2e7d32?style=for-the-badge)](https://gist.github.com/martialsystems/1104e5e47b8a04006ec694d289d43639)

[![Open the research console](https://img.shields.io/badge/Open_the_research_console-2e7d32?style=for-the-badge)](https://martialsystems.github.io/indiana_wx_pages/)
