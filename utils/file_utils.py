"""File helpers used by upload / download tests."""

from __future__ import annotations

import time
from pathlib import Path


def wait_for_download(directory: Path, suffix: str, timeout: float = 20) -> Path:
    """Wait until a finished download with the given suffix (e.g. '.txt') exists, and return its path."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        finished = [
            p for p in directory.glob(f"*{suffix}") if not p.name.endswith((".crdownload", ".part", ".tmp"))
        ]
        if finished:
            return finished[0]
        time.sleep(0.25)
    raise TimeoutError(f"No '{suffix}' file appeared in {directory} within {timeout}s")


def create_text_file(directory: Path, name: str, content: str = "sample content") -> Path:
    path = directory / name
    path.write_text(content, encoding="utf-8")
    return path
