"""
Gemini Image Generation Fallback for Hermes Agent
===================================================
Patches Hermes' image_generation_tool.py to add Google Gemini as a
fallback image provider (FAL -> OpenAI -> Gemini).

Usage:
    python scripts/enable-gemini-image-fallback.py

Prerequisites:
    pip install google-genai pillow

Environment:
    GEMINI_API_KEY=your-google-ai-studio-key

This script patches the installed Hermes image tool at:
    ~/.hermes/hermes-agent/tools/image_generation_tool.py
"""
from __future__ import annotations

import os
import shutil
import textwrap
from pathlib import Path


IMAGE_TOOL_PATH = Path.home() / ".hermes" / "hermes-agent" / "tools" / "image_generation_tool.py"
BACKUP_SUFFIX = ".bak-pre-gemini"


# ---------------------------------------------------------------------------
# Patch blocks
# ---------------------------------------------------------------------------

# 1. Add Gemini constants after OpenAI constants
AFTER_OPENAI_CONSTANTS = 'OPENAI_SIZE_MAP = {\n    "landscape": "1536x1024",\n    "square": "1024x1024",\n    "portrait": "1024x1536",\n}'

GEMINI_CONSTANTS = '''

# Gemini image generation config
GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"
GEMINI_ASPECT_RATIO_MAP = {
    "landscape": "16:9",
    "square": "1:1",
    "portrait": "9:16",
}'''


# 2. Add Gemini generation function after _generate_with_openai
AFTER_OPENAI_FUNCTION = '''    return {
        "path": local_path,
        "model": OPENAI_IMAGE_MODEL,
        "provider": "openai",
    }'''

GEMINI_FUNCTION = '''


def _generate_with_gemini(
    prompt: str,
    aspect_ratio: str,
    output_format: str,
) -> Dict[str, Any]:
    """Generate one image with Google Gemini and save it as a local file."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise ImportError(
            "google-genai package not installed. Run: pip install google-genai pillow"
        )

    client = genai.Client(api_key=api_key)
    gemini_aspect = GEMINI_ASPECT_RATIO_MAP.get(
        aspect_ratio, GEMINI_ASPECT_RATIO_MAP["square"]
    )

    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"],
        ),
    )

    # Extract image from response parts
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_bytes = part.inline_data.data
            extension = "png" if output_format == "png" else "jpg"
            local_path = _save_generated_image(image_bytes, extension)
            return {
                "path": local_path,
                "model": GEMINI_IMAGE_MODEL,
                "provider": "gemini",
            }

    raise ValueError("Gemini API returned no image in response")'''


# 3. Patch the fallback chain: after OpenAI fallback, add Gemini
OPENAI_FALLBACK_BLOCK = '''        if response_data is None:
            openai_result = await asyncio.to_thread(
                _generate_with_openai,
                prompt.strip(),
                aspect_ratio_lower,
                validated_params["output_format"],
            )
            logger.info("Generated image with OpenAI fallback: %s", openai_result["path"])
            response_data = {
                "success": True,
                "image": f"MEDIA:{openai_result[\'path\']}",
            }'''

FULL_FALLBACK_BLOCK = '''        if response_data is None and os.getenv("OPENAI_API_KEY"):
            try:
                openai_result = await asyncio.to_thread(
                    _generate_with_openai,
                    prompt.strip(),
                    aspect_ratio_lower,
                    validated_params["output_format"],
                )
                logger.info("Generated image with OpenAI fallback: %s", openai_result["path"])
                response_data = {
                    "success": True,
                    "image": f"MEDIA:{openai_result[\'path\']}",
                }
            except Exception as openai_error:
                logger.warning("OpenAI image generation failed, trying Gemini fallback: %s", openai_error)

        if response_data is None and os.getenv("GEMINI_API_KEY"):
            try:
                gemini_result = await asyncio.to_thread(
                    _generate_with_gemini,
                    prompt.strip(),
                    aspect_ratio_lower,
                    validated_params["output_format"],
                )
                logger.info("Generated image with Gemini fallback: %s", gemini_result["path"])
                response_data = {
                    "success": True,
                    "image": f"MEDIA:{gemini_result[\'path\']}",
                }
            except Exception as gemini_error:
                logger.warning("Gemini image generation also failed: %s", gemini_error)'''


# 4. Update requirements check to include Gemini
OLD_REQUIREMENTS = '''def check_image_generation_requirements() -> bool:
    """
    Check if all requirements for image generation tools are met.

    Returns:
        bool: True if requirements are met, False otherwise
    """
    try:
        if check_fal_api_key():
            import fal_client
            return True
        return bool(os.getenv("OPENAI_API_KEY"))

    except ImportError:
        return False'''

NEW_REQUIREMENTS = '''def check_image_generation_requirements() -> bool:
    """
    Check if all requirements for image generation tools are met.
    Supports FAL, OpenAI, or Gemini as providers.

    Returns:
        bool: True if at least one provider is available
    """
    try:
        if check_fal_api_key():
            import fal_client
            return True
    except ImportError:
        pass
    if os.getenv("OPENAI_API_KEY"):
        return True
    if os.getenv("GEMINI_API_KEY"):
        return True
    return False'''


# ---------------------------------------------------------------------------
# Patch logic
# ---------------------------------------------------------------------------

def replace_once(text: str, old: str, new: str, label: str) -> str:
    """Replace old with new exactly once. Skip if already patched."""
    if new in text:
        print(f"  [skip] {label} - already patched")
        return text
    if old not in text:
        raise SystemExit(f"  [FAIL] Could not find expected block for: {label}")
    result = text.replace(old, new, 1)
    print(f"  [ok]   {label}")
    return result


def insert_after(text: str, anchor: str, insertion: str, label: str) -> str:
    """Insert text after an anchor string. Skip if already present."""
    if insertion.strip() in text:
        print(f"  [skip] {label} - already patched")
        return text
    if anchor not in text:
        raise SystemExit(f"  [FAIL] Could not find anchor for: {label}")
    result = text.replace(anchor, anchor + insertion, 1)
    print(f"  [ok]   {label}")
    return result


def patch() -> None:
    if not IMAGE_TOOL_PATH.exists():
        raise SystemExit(f"Hermes image tool not found at: {IMAGE_TOOL_PATH}")

    # Create backup
    backup_path = IMAGE_TOOL_PATH.with_suffix(BACKUP_SUFFIX)
    if not backup_path.exists():
        shutil.copy2(IMAGE_TOOL_PATH, backup_path)
        print(f"Backup created: {backup_path}")

    text = IMAGE_TOOL_PATH.read_text(encoding="utf-8")

    print("\nApplying Gemini image fallback patches...")

    # 1. Add Gemini constants
    text = insert_after(text, AFTER_OPENAI_CONSTANTS, GEMINI_CONSTANTS, "Gemini constants")

    # 2. Add Gemini generation function
    text = insert_after(text, AFTER_OPENAI_FUNCTION, GEMINI_FUNCTION, "Gemini generation function")

    # 3. Patch fallback chain
    text = replace_once(text, OPENAI_FALLBACK_BLOCK, FULL_FALLBACK_BLOCK, "Fallback chain (FAL -> OpenAI -> Gemini)")

    # 4. Update requirements check
    text = replace_once(text, OLD_REQUIREMENTS, NEW_REQUIREMENTS, "Requirements check")

    IMAGE_TOOL_PATH.write_text(text, encoding="utf-8")
    print("\nGemini image fallback patch applied successfully!")
    print("\nNext steps:")
    print("  1. pip install google-genai pillow  (in WSL)")
    print("  2. Add GEMINI_API_KEY=... to ~/.hermes/.env")
    print("  3. Restart hermes gateway")
    print("\nFallback order: FAL -> OpenAI -> Gemini")


if __name__ == "__main__":
    patch()
