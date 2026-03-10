"""
C6: Provider Usage Logging
Patches image_generation_tool.py to log every provider call
(success/failure, latency, provider name) to a JSON log file.

Run from WSL:
    python3 scripts/enable-provider-logging.py
"""
from __future__ import annotations

from pathlib import Path


IMAGE_TOOL_PATH = Path.home() / ".hermes" / "hermes-agent" / "tools" / "image_generation_tool.py"


# --- Patch 1: Add the logging helper function ---

HELPER_MARKER = "def _save_generated_image("

LOG_HELPER = '''def _log_provider_usage(
    provider: str,
    action: str,
    success: bool,
    latency_s: float,
    error: str = "",
) -> None:
    """Append a provider usage entry to the log file."""
    import datetime as _dt

    log_dir = Path(os.path.expanduser("~/.hermes/logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "provider_usage.jsonl"

    entry = {
        "timestamp": _dt.datetime.now().isoformat(),
        "provider": provider,
        "action": action,
        "success": success,
        "latency_s": round(latency_s, 2),
    }
    if error:
        entry["error"] = str(error)[:200]

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\\n")
    except Exception:
        pass  # never break the main flow for logging


'''


# --- Patch 2: Add logging calls in the fallback chain ---
# We patch the FAL success log line to also log provider usage

FAL_LOG_OLD = '                    logger.info("Generated %s image(s) with FAL (%s upscaled)", len(formatted_images), upscaled_count)'

FAL_LOG_NEW = '''                    logger.info("Generated %s image(s) with FAL (%s upscaled)", len(formatted_images), upscaled_count)
                    _log_provider_usage("fal", "image_generate", True, (datetime.datetime.now() - start_time).total_seconds())'''


FAL_FAIL_OLD = '                logger.warning("FAL image generation failed, trying OpenAI fallback: %s", fal_error)'

FAL_FAIL_NEW = '''                logger.warning("FAL image generation failed, trying OpenAI fallback: %s", fal_error)
                _log_provider_usage("fal", "image_generate", False, (datetime.datetime.now() - start_time).total_seconds(), str(fal_error))'''


OPENAI_LOG_OLD = '            logger.info("Generated image with OpenAI fallback: %s", openai_result["path"])'

OPENAI_LOG_NEW = '''            logger.info("Generated image with OpenAI fallback: %s", openai_result["path"])
            _log_provider_usage("openai", "image_generate", True, (datetime.datetime.now() - start_time).total_seconds())'''


def insert_before(text: str, marker: str, content: str, label: str) -> str:
    check_line = content.strip().split("\n")[0]
    if check_line in text:
        print(f"  [skip] {label} already applied")
        return text
    if marker not in text:
        print(f"  [warn] Could not find marker for {label}")
        return text
    return text.replace(marker, content + marker, 1)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        print(f"  [skip] {label} already applied")
        return text
    if old not in text:
        print(f"  [warn] Could not find block for {label}")
        return text
    return text.replace(old, new, 1)


def main() -> None:
    if not IMAGE_TOOL_PATH.exists():
        raise SystemExit(f"Missing file: {IMAGE_TOOL_PATH}")

    text = IMAGE_TOOL_PATH.read_text(encoding="utf-8")

    # Patch 1: Add logging helper
    text = insert_before(text, HELPER_MARKER, LOG_HELPER, "provider logging helper")

    # Patch 2: Add logging calls
    text = replace_once(text, FAL_LOG_OLD, FAL_LOG_NEW, "FAL success log")
    text = replace_once(text, FAL_FAIL_OLD, FAL_FAIL_NEW, "FAL failure log")
    text = replace_once(text, OPENAI_LOG_OLD, OPENAI_LOG_NEW, "OpenAI success log")

    IMAGE_TOOL_PATH.write_text(text, encoding="utf-8")
    print("Provider usage logging patch applied.")
    print("Logs will be written to ~/.hermes/logs/provider_usage.jsonl")
    print("Restart Hermes gateway after this.")


if __name__ == "__main__":
    main()
