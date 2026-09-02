# Copyright (c) 2026 Martial Systems LLC
"""HEAD/GET with 404 as fetch-or-stop. Retry IncompleteRead and 5xx."""

from __future__ import annotations

import json
import time
from http.client import IncompleteRead
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from nwmana.config import USER_AGENT
from nwmana.errors import FetchError


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, IncompleteRead):
        return True
    if isinstance(exc, HTTPError):
        return int(getattr(exc, "code", 0) or 0) >= 500
    return isinstance(exc, (URLError, TimeoutError, ConnectionResetError, ConnectionError))


def _open(url: str, *, method: str, timeout: int, attempts: int):
    req = Request(url, headers={"User-Agent": USER_AGENT}, method=method)
    last: BaseException | None = None
    for i in range(attempts):
        try:
            return urlopen(req, timeout=timeout)
        except HTTPError as exc:
            last = exc
            code = int(getattr(exc, "code", 0) or 0)
            if code == 404:
                raise FetchError(f"GET empty or 404: {url}") from exc
            if not _is_retryable(exc) or i == attempts - 1:
                raise FetchError(f"GET failed: {url}: {exc}") from exc
            time.sleep(min(2**i, 16))
        except (URLError, TimeoutError, ConnectionResetError, ConnectionError, IncompleteRead) as exc:
            last = exc
            if not _is_retryable(exc) or i == attempts - 1:
                raise FetchError(f"GET failed: {url}: {exc}") from exc
            time.sleep(min(2**i, 16))
    raise FetchError(f"GET failed: {url}: {last}") from last


def head_bytes(url: str, *, timeout: int = 30, attempts: int = 4) -> int:
    with _open(url, method="HEAD", timeout=timeout, attempts=attempts) as resp:
        length = int(resp.headers.get("Content-Length") or 0)
        code = int(getattr(resp, "status", 200) or 200)
    if code == 404 or length <= 0:
        raise FetchError(f"GET empty or 404: {url}")
    return length


def get_bytes(url: str, *, timeout: int = 90, attempts: int = 6) -> bytes:
    with _open(url, method="GET", timeout=timeout, attempts=attempts) as resp:
        body = resp.read()
    if not body:
        raise FetchError(f"GET empty or 404: {url}")
    return body


def get_json(url: str, *, timeout: int = 90) -> dict[str, Any]:
    raw = get_bytes(url, timeout=timeout)
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FetchError(f"not JSON: {url}") from exc
    if not isinstance(doc, dict):
        raise FetchError(f"JSON object required: {url}")
    return doc
