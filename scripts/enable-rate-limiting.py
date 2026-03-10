"""
C4: Rate Limiting Patch for Telegram
Adds per-user rate limiting to prevent spam and excessive API usage.
Default: 5 messages per 30 seconds per user.

Run from WSL:
    python3 scripts/enable-rate-limiting.py
"""
from __future__ import annotations

from pathlib import Path


TELEGRAM_PATH = Path.home() / ".hermes" / "hermes-agent" / "gateway" / "platforms" / "telegram.py"


# --- Patch 1: Add rate limiter class after imports ---

IMPORT_MARKER = "from telegram import"

RATE_LIMITER = '''
import time as _time
from collections import defaultdict as _defaultdict

class _RateLimiter:
    """Simple per-user rate limiter."""

    def __init__(self, max_requests: int = 5, window_seconds: int = 30):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[str, list[float]] = _defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = _time.time()
        window_start = now - self.window
        # Clean old entries
        self._requests[user_id] = [
            t for t in self._requests[user_id] if t > window_start
        ]
        if len(self._requests[user_id]) >= self.max_requests:
            return False
        self._requests[user_id].append(now)
        return True

    def time_until_allowed(self, user_id: str) -> float:
        if not self._requests[user_id]:
            return 0
        oldest = min(self._requests[user_id])
        return max(0, self.window - (_time.time() - oldest))

_rate_limiter = _RateLimiter()

'''


# --- Patch 2: Add rate check in message handler ---

HANDLE_MSG_OLD = "    async def _handle_message(self, update: Update, context) -> None:"

HANDLE_MSG_NEW = '''    async def _handle_message(self, update: Update, context) -> None:
        # Rate limiting check
        if update.effective_user:
            _uid = str(update.effective_user.id)
            if not _rate_limiter.is_allowed(_uid):
                _wait = _rate_limiter.time_until_allowed(_uid)
                try:
                    await update.message.reply_text(
                        f"Slow down! Please wait {_wait:.0f} seconds before sending another message."
                    )
                except Exception:
                    pass
                return
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        print(f"  [skip] {label} already applied")
        return text
    if old not in text:
        raise SystemExit(f"Could not find expected block for {label}")
    return text.replace(old, new, 1)


def insert_before(text: str, marker: str, content: str, label: str) -> str:
    if "_RateLimiter" in text:
        print(f"  [skip] {label} already applied")
        return text
    if marker not in text:
        raise SystemExit(f"Could not find marker for {label}")
    idx = text.index(marker)
    return text[:idx] + content + text[idx:]


def main() -> None:
    if not TELEGRAM_PATH.exists():
        raise SystemExit(f"Missing file: {TELEGRAM_PATH}")

    text = TELEGRAM_PATH.read_text(encoding="utf-8")

    # Patch 1: Add rate limiter class
    text = insert_before(text, IMPORT_MARKER, RATE_LIMITER, "rate limiter class")

    # Patch 2: Add rate check in handler
    text = replace_once(text, HANDLE_MSG_OLD, HANDLE_MSG_NEW, "rate limiting check")

    TELEGRAM_PATH.write_text(text, encoding="utf-8")
    print("Rate limiting patch applied (5 msgs / 30 sec per user).")
    print("Restart Hermes gateway after this.")


if __name__ == "__main__":
    main()
