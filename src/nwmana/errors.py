# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class FetchError(GateError):
    """AnA, NWIS, or a calendar day 404/empty."""


class FigureCapError(GateError):
    """This tree stops at two figures."""


class MixRetroError(GateError):
    """AnA skill table mixed with v2.1 retrospective RMSE."""
