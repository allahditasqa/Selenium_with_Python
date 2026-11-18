"""HTTP status checker used for the 'Broken Links' practice section (no browser needed)."""

from __future__ import annotations

import requests

_HEADERS = {"User-Agent": "Mozilla/5.0 (selenium-python-framework link checker)"}


def status_code(url: str, timeout: int = 15) -> int:
    """Return the HTTP status of a URL, following redirects. Uses GET because many servers reject HEAD."""
    response = requests.get(url, headers=_HEADERS, timeout=timeout, allow_redirects=True, stream=True)
    response.close()
    return response.status_code
