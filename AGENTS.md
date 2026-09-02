# Agent notes: nwm_ana_2025_26

Public GitHub. MIT. Question: Does operational NWM analysis-assim beat yesterday's flow on the White River in 2025 to August 2026?

Same four gages as `fa2e315`. Window is 2025-01-01 to 2026-08-31. Fetch-or-stop per day. Persistence is the bar. Do not mix AnA RMSE into the v2.1 table. Do not restamp `fa2e315`. Do not start a 2021-2024 AnA fill. Do not open a Chicago HAND freeze. Calumet D stays finished.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

`vbd.runtime.json` runs `.venv/bin/python -m pytest` and `scripts/run_fixture.py`. Do not use stock `/usr/bin/python3 -m pytest`. Live `run_live.py` exits 2 on a missing AnA day.
