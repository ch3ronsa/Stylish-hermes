"""
C1: Config Validator
Checks all required and optional environment variables,
validates formats, and reports status clearly.

Run from WSL:
    python3 scripts/validate-config.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ENV_PATH = Path.home() / ".hermes" / ".env"

REQUIRED = {
    "TELEGRAM_BOT_TOKEN": {
        "desc": "Telegram bot authentication",
        "hint": "Get from @BotFather on Telegram",
    },
}

# At least one of these must be set for vision/chat
VISION_KEYS = {
    "GLM_API_KEY": "GLM-4 Vision (primary chat + vision model)",
    "OPENROUTER_API_KEY": "OpenRouter (alternative chat provider)",
}

# At least one of these must be set for image generation
IMAGE_KEYS = {
    "FAL_KEY": "FAL.ai FLUX 2 Pro (primary image gen)",
    "OPENAI_API_KEY": "OpenAI DALL-E 3 (fallback 1)",
    "GEMINI_API_KEY": "Google Gemini (fallback 2 + image transform)",
}

OPTIONAL = {
    "FIRECRAWL_API_KEY": "Web search & weather (for outfit recommendations)",
    "GLM_BASE_URL": "Custom GLM endpoint URL",
    "AUXILIARY_VISION_PROVIDER": "Auxiliary vision provider setting",
    "AUXILIARY_VISION_MODEL": "Auxiliary vision model name",
}


def load_env(path: Path) -> dict[str, str]:
    """Load .env file into a dict."""
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip()
    return env


def check_var(env: dict, key: str) -> bool:
    """Check if a key is set and not a placeholder."""
    val = env.get(key, os.environ.get(key, ""))
    if not val:
        return False
    placeholders = {"...", "sk-or-...", "fc-...", "your-key-here", ""}
    return val not in placeholders


def main() -> None:
    print("=" * 50)
    print("  Stylish Hermes - Config Validator")
    print("=" * 50)

    if not ENV_PATH.exists():
        print(f"\n  [ERROR] .env file not found at {ENV_PATH}")
        print("  Copy .env.example to ~/.hermes/.env and fill in your keys.")
        sys.exit(1)

    env = load_env(ENV_PATH)
    errors = []
    warnings = []

    print(f"\n  Reading: {ENV_PATH}\n")

    # Required keys
    print("--- REQUIRED ---")
    for key, info in REQUIRED.items():
        ok = check_var(env, key)
        status = "OK" if ok else "MISSING"
        icon = "+" if ok else "X"
        print(f"  [{icon}] {key}: {status}")
        if not ok:
            errors.append(f"{key} - {info['desc']} ({info['hint']})")

    # Vision keys (at least one)
    print("\n--- VISION/CHAT (need at least 1) ---")
    vision_ok = False
    for key, desc in VISION_KEYS.items():
        ok = check_var(env, key)
        vision_ok = vision_ok or ok
        icon = "+" if ok else "-"
        print(f"  [{icon}] {key}: {'OK' if ok else 'not set'}")
    if not vision_ok:
        errors.append("No vision/chat provider configured. Set GLM_API_KEY or OPENROUTER_API_KEY.")

    # Image generation keys (at least one)
    print("\n--- IMAGE GENERATION (need at least 1) ---")
    image_ok = False
    active_providers = []
    for key, desc in IMAGE_KEYS.items():
        ok = check_var(env, key)
        image_ok = image_ok or ok
        icon = "+" if ok else "-"
        print(f"  [{icon}] {key}: {'OK' if ok else 'not set'}")
        if ok:
            active_providers.append(desc)
    if not image_ok:
        errors.append("No image generation provider configured. Set FAL_KEY, OPENAI_API_KEY, or GEMINI_API_KEY.")
    else:
        print(f"  Fallback chain: {' -> '.join(active_providers)}")

    # Optional keys
    print("\n--- OPTIONAL ---")
    for key, desc in OPTIONAL.items():
        ok = check_var(env, key)
        icon = "+" if ok else "-"
        print(f"  [{icon}] {key}: {'OK' if ok else 'not set'} ({desc})")
        if not ok:
            warnings.append(f"{key} not set - {desc} will be unavailable")

    # Summary
    print("\n" + "=" * 50)
    if errors:
        print(f"  RESULT: {len(errors)} error(s) found\n")
        for e in errors:
            print(f"    [!] {e}")
        sys.exit(1)
    else:
        print("  RESULT: All good! Ready to run.\n")
        if warnings:
            for w in warnings:
                print(f"    [~] {w}")
        print()


if __name__ == "__main__":
    main()
