"""
Apply all Gemini patches to Hermes image_generation_tool.py
This is a one-time fix script that applies constants, function,
fallback chain, and requirements check updates.
"""
import re
from pathlib import Path

p = Path.home() / ".hermes" / "hermes-agent" / "tools" / "image_generation_tool.py"
if not p.exists():
    raise SystemExit(f"File not found: {p}")

text = p.read_text(encoding="utf-8")
changes = 0

# ── 1. Add GEMINI constants ──
if "GEMINI_IMAGE_MODEL" not in text:
    anchor = 'OPENAI_SIZE_MAP = {\n    "landscape": "1536x1024",\n    "square": "1024x1024",\n    "portrait": "1024x1536",\n}'
    addition = '''

# Gemini image generation config
GEMINI_IMAGE_MODEL = "gemini-2.0-flash-exp"
GEMINI_ASPECT_RATIO_MAP = {
    "landscape": "16:9",
    "square": "1:1",
    "portrait": "9:16",
}'''
    if anchor in text:
        text = text.replace(anchor, anchor + addition, 1)
        changes += 1
        print("[ok] Gemini constants")
    else:
        print("[FAIL] Cannot find OPENAI_SIZE_MAP anchor")
else:
    print("[skip] Gemini constants already present")


# ── 2. Add _generate_with_gemini function ──
if "def _generate_with_gemini" not in text:
    anchor = '    return {\n        "path": local_path,\n        "model": OPENAI_IMAGE_MODEL,\n        "provider": "openai",\n    }'
    func = '''


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

    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"],
        ),
    )

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

    if anchor in text:
        text = text.replace(anchor, anchor + func, 1)
        changes += 1
        print("[ok] _generate_with_gemini function")
    else:
        print("[FAIL] Cannot find _generate_with_openai return anchor")
else:
    print("[skip] _generate_with_gemini already present")


# ── 3. Patch fallback chain ──
if "gemini_result" not in text:
    pattern = re.compile(
        r"( {8}if response_data is None:\s*\n"
        r" {12}openai_result = await asyncio\.to_thread\(\s*\n"
        r" {16}_generate_with_openai,\s*\n"
        r" {16}prompt\.strip\(\),\s*\n"
        r" {16}aspect_ratio_lower,\s*\n"
        r" {16}validated_params\[\"output_format\"\],\s*\n"
        r" {12}\)\s*\n"
        r" {12}logger\.info\(\"Generated image with OpenAI fallback.*?\n"
        r" {12}response_data = \{\s*\n"
        r" {16}\"success\": True,\s*\n"
        r" {16}\"image\":.*?openai_result.*?\n"
        r" {12}\})",
        re.DOTALL,
    )
    m = pattern.search(text)
    if m:
        new_block = (
            '        if response_data is None and os.getenv("OPENAI_API_KEY"):\n'
            '            try:\n'
            '                openai_result = await asyncio.to_thread(\n'
            '                    _generate_with_openai,\n'
            '                    prompt.strip(),\n'
            '                    aspect_ratio_lower,\n'
            '                    validated_params["output_format"],\n'
            '                )\n'
            '                logger.info("Generated image with OpenAI fallback: %s", openai_result["path"])\n'
            '                response_data = {\n'
            '                    "success": True,\n'
            "                    \"image\": f\"MEDIA:{openai_result['path']}\",\n"
            '                }\n'
            '            except Exception as openai_error:\n'
            '                logger.warning("OpenAI fallback failed, trying Gemini: %s", openai_error)\n'
            '\n'
            '        if response_data is None and os.getenv("GEMINI_API_KEY"):\n'
            '            try:\n'
            '                gemini_result = await asyncio.to_thread(\n'
            '                    _generate_with_gemini,\n'
            '                    prompt.strip(),\n'
            '                    aspect_ratio_lower,\n'
            '                    validated_params["output_format"],\n'
            '                )\n'
            '                logger.info("Generated image with Gemini fallback: %s", gemini_result["path"])\n'
            '                response_data = {\n'
            '                    "success": True,\n'
            "                    \"image\": f\"MEDIA:{gemini_result['path']}\",\n"
            '                }\n'
            '            except Exception as gemini_error:\n'
            '                logger.warning("Gemini fallback also failed: %s", gemini_error)'
        )
        text = text[: m.start()] + new_block + text[m.end() :]
        changes += 1
        print("[ok] Fallback chain (FAL -> OpenAI -> Gemini)")
    else:
        print("[FAIL] Cannot find OpenAI fallback block (regex mismatch)")
else:
    print("[skip] Gemini fallback chain already present")


# ── 4. Requirements check (already patched if script ran before) ──
if 'os.getenv("GEMINI_API_KEY")' not in text:
    old_req = re.compile(
        r"def check_image_generation_requirements\(\) -> bool:.*?except ImportError:\s*\n\s*return False",
        re.DOTALL,
    )
    new_req = '''def check_image_generation_requirements() -> bool:
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
    result = old_req.sub(new_req, text, count=1)
    if result != text:
        text = result
        changes += 1
        print("[ok] Requirements check")
    else:
        print("[FAIL] Cannot find requirements check block")
else:
    print("[skip] Requirements check already patched")


# ── Write ──
if changes > 0:
    p.write_text(text, encoding="utf-8")
    print(f"\nDone! {changes} patch(es) applied and saved.")
else:
    print("\nNo changes needed - all patches already applied.")
