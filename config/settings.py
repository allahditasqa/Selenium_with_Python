"""Central configuration. Values come from environment variables / .env, with safe defaults.

Command line options of pytest (--browser, --headless, --base-url) override these at runtime
(see conftest.py).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env(name: str, default: str) -> str:
    # Values may carry a trailing "# comment" when copied from .env.example
    return os.getenv(name, default).split("#")[0].strip()


@dataclass(frozen=True)
class Settings:
    base_url: str = "https://testautomationpractice.blogspot.com"
    browser: str = "chrome"
    headless: bool = True
    explicit_timeout: int = 15
    page_load_timeout: int = 60
    window_size: str = "1920,1080"
    remote_url: str | None = None
    screenshot_dir: Path = ROOT_DIR / "reports" / "screenshots"

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            base_url=_env("BASE_URL", cls.base_url).rstrip("/"),
            browser=_env("BROWSER", cls.browser).lower(),
            headless=_as_bool(_env("HEADLESS", "true"), cls.headless),
            explicit_timeout=int(_env("EXPLICIT_TIMEOUT", str(cls.explicit_timeout))),
            page_load_timeout=int(_env("PAGE_LOAD_TIMEOUT", str(cls.page_load_timeout))),
            window_size=_env("WINDOW_SIZE", cls.window_size),
            remote_url=_env("SELENIUM_REMOTE_URL", "") or None,
        )


settings = Settings.from_env()
