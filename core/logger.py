"""Small logging helper so every module logs in the same format."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"framework.{name}")
