#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Live AnA 2025 to August 2026. Fetch-or-stop per day. Exit 2 on 404."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from nwmana.errors import FetchError  # noqa: E402
from nwmana.pipeline import run_live  # noqa: E402


def main() -> int:
    log_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "logs" / "live"
    try:
        report = run_live(log_dir)
    except FetchError as exc:
        print(str(exc))
        return 2
    for g in report["gages"]:
        pers = g["skill"]["persistence"]["rmse_cfs"]
        ana = g["skill"]["ana"]["rmse_cfs"]
        print(f"{g['id']} persistence {pers:.0f} AnA {ana:.0f} bias {g['bias_cfs']:.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
