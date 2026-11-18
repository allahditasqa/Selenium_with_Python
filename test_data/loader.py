"""Loads JSON test data so tests contain no hard-coded literals."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent


@cache
def load(name: str) -> dict[str, Any]:
    with (DATA_DIR / f"{name}.json").open(encoding="utf-8") as handle:
        return json.load(handle)
