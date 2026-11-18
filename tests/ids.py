"""Helpers that keep automated tests and the written test cases (docs/test-cases) in sync."""

from __future__ import annotations


def tc_ids(base: str, count: int) -> list[str]:
    """IDs of a data-driven case: ``tc_ids("TC_FORM_06", 3)`` -> TC_FORM_06.1, TC_FORM_06.2, TC_FORM_06.3."""
    return [f"{base}.{n}" for n in range(1, count + 1)]
