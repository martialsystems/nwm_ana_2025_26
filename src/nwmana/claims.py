# Copyright (c) 2026 Martial Systems LLC
"""Fail closed: AnA is not v2.1 retro, residual is not water."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from nwmana.config import V21_RMSE_TOKENS
from nwmana.errors import ClaimBanError, MixRetroError

_BANS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("casualty", re.compile(r"\b(deaths?|fatalit(?:y|ies)|casualt(?:y|ies)|killed)\b", re.I)),
    ("climate", re.compile(r"\b(cmip\d*|downscal(?:e|ed|ing)|gcm)\b", re.I)),
    ("par", re.compile(r"\b(lives|people|population)\s+at\s+risk\b", re.I)),
    ("p100", re.compile(r"\b100-year\s+exceedance\b", re.I)),
    ("forecast", re.compile(r"\bP\(sfha\s*\|\s*hydro\)\s+is\s+(?:a\s+)?(?:flood\s+)?forecast\b", re.I)),
    ("hand_firm", re.compile(r"\bHAND (?:mask|wet(?: area)?|bathtub) is (?:a |the )?FIRM\b", re.I)),
    ("resid_wet", re.compile(r"\bresidual (?:strip|map|layer) is (?:a |the )?(?:wet mask|inundation)\b", re.I)),
    ("flood_warning", re.compile(r"\bflood warning\b|\bemergency forecast\b", re.I)),
    ("flood_ai", re.compile(r"\bflood AI\b", re.I)),
    ("mix_column", re.compile(r"\bmix(?:ed|ing)? AnA with v2\.1\b", re.I)),
)


def scan_text(text: str) -> list[str]:
    hits = [name for name, pat in _BANS if pat.search(text or "")]
    if "\u2014" in (text or ""):
        hits.append("em_dash")
    return hits


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")


def require_ana_table_not_v21(text: str, *, source: str) -> None:
    """The AnA skill table must not reuse the locked v2.1 RMSE cells."""
    start = text.find("| Gage |")
    if start < 0:
        return
    end = text.find("\n## ", start)
    block = text[start : end if end > 0 else start + 2000]
    for tok in V21_RMSE_TOKENS:
        if tok in block:
            raise MixRetroError(f"{source}: AnA table contains v2.1 RMSE token {tok}")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
