"""
Gemini Image Transform Tool for Hermes Agent
==============================================
Patches Hermes to add a new `image_transform` tool that takes a reference
image + text prompt and generates a transformed outfit image using Gemini's
multimodal capabilities (image+text in, image out).

This is the core "reference image -> transformed outfit" feature.

Usage:
    python scripts/enable-gemini-image-transform.py

Prerequisites:
    pip install google-genai pillow

Environment:
    GEMINI_API_KEY=your-google-ai-studio-key

This script patches:
    ~/.hermes/hermes-agent/tools/image_generation_tool.py
"""
from __future__ import annotations

import shutil
from pathlib import Path


IMAGE_TOOL_PATH = Path.home() / ".hermes" / "hermes-agent" / "tools" / "image_generation_tool.py"
BACKUP_SUFFIX = ".bak-pre-transform"


# ---------------------------------------------------------------------------
# New function: transform image with Gemini
# ---------------------------------------------------------------------------

TRANSFORM_FUNCTION = '''

def _transform_with_gemini(
    image_path: str,
    prompt: str,
    output_format: str = "png",
) -> Dict[str, Any]:
    """Transform a reference image using Gemini multimodal (image+text -> image).

    Sends the reference image along with a transformation prompt to Gemini,
    which generates a new image based on the reference aesthetic but adapted
    to the prompt constraints.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    try:
        from google import genai
        from google.genai import types
        from PIL import Image as PILImage
    except ImportError:
        raise ImportError(
            "google-genai and pillow packages required. Run: pip install google-genai pillow"
        )

    # Load the reference image
    ref_path = image_path.replace("MEDIA:", "")
    if not os.path.exists(ref_path):
        raise FileNotFoundError(f"Reference image not found: {ref_path}")

    ref_image = PILImage.open(ref_path)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[
            prompt,
            ref_image,
        ],
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"],
        ),
    )

    # Extract generated image from response
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_bytes = part.inline_data.data
            extension = "png" if output_format == "png" else "jpg"
            local_path = _save_generated_image(image_bytes, extension)
            return {
                "path": local_path,
                "model": GEMINI_IMAGE_MODEL,
                "provider": "gemini-transform",
            }

    raise ValueError("Gemini transform returned no image in response")


async def image_transform_tool(
    reference_image: str,
    prompt: str,
    output_format: str = "png",
) -> str:
    """Transform a reference image into a new outfit based on the prompt.

    Uses Gemini multimodal to understand the reference aesthetic and generate
    a transformed version that matches the prompt constraints.

    Args:
        reference_image (str): Path to the reference image (local path or MEDIA: prefixed)
        prompt (str): Transformation instructions (e.g. "Transform this into a casual everyday outfit for spring")
        output_format (str): Output format "jpeg" or "png" (default: "png")

    Returns:
        str: JSON string with {"success": bool, "image": str_path_or_null}
    """
    start_time = datetime.datetime.now()
    try:
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt is required")
        if not reference_image:
            raise ValueError("Reference image path is required")

        result = await asyncio.to_thread(
            _transform_with_gemini,
            reference_image,
            prompt.strip(),
            output_format,
        )

        generation_time = (datetime.datetime.now() - start_time).total_seconds()
        logger.info("Transformed image with Gemini in %.1fs: %s", generation_time, result["path"])

        return json.dumps({
            "success": True,
            "image": f"MEDIA:{result['path']}",
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("Image transform failed: %s", e)
        return json.dumps({
            "success": False,
            "image": None,
            "error": str(e),
        }, indent=2, ensure_ascii=False)

'''


# ---------------------------------------------------------------------------
# Tool registration block
# ---------------------------------------------------------------------------

TRANSFORM_REGISTRY = '''

IMAGE_TRANSFORM_SCHEMA = {
    "name": "image_transform",
    "description": "Transform a reference fashion image into a new outfit. Takes a reference image and a text prompt describing the desired transformation (e.g. casual version, office version, budget-friendly). Uses AI to understand the reference aesthetic and generate a completely new outfit image. Returns a local image path.",
    "parameters": {
        "type": "object",
        "properties": {
            "reference_image": {
                "type": "string",
                "description": "Path to the reference image to transform. Use the image path from the user's uploaded photo."
            },
            "prompt": {
                "type": "string",
                "description": "Transformation instructions describing how to adapt the reference look. Be specific about context, constraints, and desired changes."
            }
        },
        "required": ["reference_image", "prompt"]
    }
}


def _handle_image_transform(args, **kw):
    reference_image = args.get("reference_image", "")
    prompt = args.get("prompt", "")
    if not reference_image or not prompt:
        return json.dumps({"error": "reference_image and prompt are required"})
    return image_transform_tool(
        reference_image=reference_image,
        prompt=prompt,
        output_format="png",
    )


def check_image_transform_requirements() -> bool:
    """Check if image transform requirements are met (needs Gemini)."""
    return bool(os.getenv("GEMINI_API_KEY"))


registry.register(
    name="image_transform",
    toolset="image_gen",
    schema=IMAGE_TRANSFORM_SCHEMA,
    handler=_handle_image_transform,
    check_fn=check_image_transform_requirements,
    requires_env=["GEMINI_API_KEY"],
    is_async=True,
)
'''


# ---------------------------------------------------------------------------
# Patch logic
# ---------------------------------------------------------------------------

def insert_after(text: str, anchor: str, insertion: str, label: str) -> str:
    if insertion.strip()[:60] in text:
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

    backup_path = IMAGE_TOOL_PATH.with_suffix(BACKUP_SUFFIX)
    if not backup_path.exists():
        shutil.copy2(IMAGE_TOOL_PATH, backup_path)
        print(f"Backup created: {backup_path}")

    text = IMAGE_TOOL_PATH.read_text(encoding="utf-8")

    print("\nApplying Gemini image transform patches...")

    # 1. Add transform function (after _generate_with_gemini or _generate_with_openai)
    # Find the best anchor - look for the Gemini function end or OpenAI function end
    if "_generate_with_gemini" in text:
        anchor = '    raise ValueError("Gemini API returned no image in response")'
    else:
        anchor = '''    return {
        "path": local_path,
        "model": OPENAI_IMAGE_MODEL,
        "provider": "openai",
    }'''
    text = insert_after(text, anchor, TRANSFORM_FUNCTION, "Image transform function")

    # 2. Add tool registration (at the end of the file, after existing registry)
    registry_anchor = "    is_async=True,\n)"
    # Find the LAST occurrence
    last_idx = text.rfind(registry_anchor)
    if last_idx == -1:
        raise SystemExit("  [FAIL] Could not find registry anchor")
    if "image_transform" not in text:
        text = text[:last_idx + len(registry_anchor)] + TRANSFORM_REGISTRY + text[last_idx + len(registry_anchor):]
        print("  [ok]   Image transform tool registration")
    else:
        print("  [skip] Image transform tool registration - already patched")

    IMAGE_TOOL_PATH.write_text(text, encoding="utf-8")
    print("\nGemini image transform patch applied successfully!")
    print("\nNew tool available: image_transform(reference_image, prompt)")
    print("This enables: reference image IN -> transformed outfit OUT")


if __name__ == "__main__":
    patch()
