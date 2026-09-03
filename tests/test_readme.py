# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from nwmana.claims import require_ana_table_not_v21, scan_text
from nwmana.config import HYDRO_GIST, LOCKED_V21, QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert "Operational NWM AnA (2025-01-01 to 2026-08-31, t12z tm00) beats yesterday's USGS Q" in text
    assert "That is not the v2.1 retrospective, which only beat yesterday at Anderson." in text
    assert "analysis_assim" in text
    assert "NWM now wins" not in text
    assert "1,316" not in text
    assert "03351000" in text
    assert "Anderson" in text
    assert "Centerton" in text
    assert LOCKED_V21 in text
    assert "252" in text
    assert "301" in text
    assert "559" in text
    assert "622" in text
    assert "1,179" in text
    assert "608" in text
    assert "Open_the_research_console-2e7d32" in text
    assert "martialsystems.github.io/indiana_wx_pages" in text
    assert "NWM v2.1 vs yesterday" in text
    assert "white__river__nwm__error" not in text
    assert "Parent: [![" not in text
    assert any(
        "[![White River Q]" in line and "[![Open the research console]" in line
        for line in text.splitlines()
    )
    assert HYDRO_GIST.split("/")[-1] in text
    assert scan_text(text) == []
    assert "\u2014" not in text
    assert "What it is not" not in text
    require_ana_table_not_v21(text, source="README.md")
    for name in ("METHODOLOGY.md", "AGENTS.md", "CHECKLIST.md"):
        other = (REPO / name).read_text(encoding="utf-8")
        assert "\u2014" not in other
        assert "What it is not" not in other
