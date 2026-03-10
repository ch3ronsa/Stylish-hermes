"""
D2: Side-by-Side Image Patch
After a visual transform, automatically creates a comparison image
showing the original reference next to the transformed outfit.

Run from WSL:
    python3 scripts/enable-side-by-side.py
"""
from __future__ import annotations

from pathlib import Path


IMAGE_TOOL_PATH = Path.home() / ".hermes" / "hermes-agent" / "tools" / "image_generation_tool.py"


# --- Patch 1: Add PIL import and side-by-side helper ---

HELPER_MARKER = "def _save_generated_image("

SIDE_BY_SIDE_HELPER = '''def _create_side_by_side(
    left_path: str,
    right_path: str,
    left_label: str = "INSPIRATION",
    right_label: str = "TRANSFORMED",
) -> str:
    """Create a side-by-side comparison image from two local images.

    Returns the path to the combined image.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logger.warning("Pillow not installed, skipping side-by-side")
        return ""

    try:
        left = Image.open(left_path).convert("RGB")
        right = Image.open(right_path).convert("RGB")

        # Normalize heights
        target_h = max(left.height, right.height, 800)
        left = left.resize(
            (int(left.width * target_h / left.height), target_h),
            Image.LANCZOS,
        )
        right = right.resize(
            (int(right.width * target_h / right.height), target_h),
            Image.LANCZOS,
        )

        gap = 4
        label_h = 48
        total_w = left.width + gap + right.width
        total_h = target_h + label_h

        canvas = Image.new("RGB", (total_w, total_h), (18, 18, 26))
        canvas.paste(left, (0, label_h))
        canvas.paste(right, (left.width + gap, label_h))

        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        except (OSError, IOError):
            font = ImageFont.load_default()

        # Left label
        lx = left.width // 2
        draw.text((lx, label_h // 2), left_label, fill=(200, 200, 200), font=font, anchor="mm")

        # Right label
        rx = left.width + gap + right.width // 2
        draw.text((rx, label_h // 2), right_label, fill=(201, 165, 92), font=font, anchor="mm")

        # Arrow in the gap area
        arrow_y = label_h + target_h // 2
        draw.text(
            (left.width + gap // 2, arrow_y),
            "→",
            fill=(201, 165, 92),
            font=font,
            anchor="mm",
        )

        cache_dir = Path(os.path.expanduser("~/.hermes/image_cache"))
        cache_dir.mkdir(parents=True, exist_ok=True)
        import datetime as _dt
        fname = f"comparison_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        out_path = cache_dir / fname
        canvas.save(str(out_path), "JPEG", quality=92)
        logger.info("Created side-by-side comparison: %s", out_path)
        return str(out_path)

    except Exception as e:
        logger.warning("Failed to create side-by-side image: %s", e)
        return ""


'''


# --- Patch 2: Hook into image_transform to auto-generate comparison ---

TRANSFORM_RESULT_MARKER = '''            "provider": "gemini",'''

TRANSFORM_RESULT_NEW = '''            "provider": "gemini",'''

# We look for the return block of image_transform and add side-by-side generation
TRANSFORM_RETURN_OLD = '''            return json.dumps({
                "success": True,
                "image": f"MEDIA:{local_path}",
                "provider": "gemini",
            })'''

TRANSFORM_RETURN_NEW = '''            comparison_path = ""
            if reference_image and os.path.exists(reference_image):
                comparison_path = _create_side_by_side(reference_image, local_path)

            result_data = {
                "success": True,
                "image": f"MEDIA:{local_path}",
                "provider": "gemini",
            }
            if comparison_path:
                result_data["comparison"] = f"MEDIA:{comparison_path}"

            return json.dumps(result_data)'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text and new != old:
        print(f"  [skip] {label} already applied")
        return text
    if old not in text:
        print(f"  [warn] Could not find block for {label} - may need manual patching")
        return text
    return text.replace(old, new, 1)


def insert_before(text: str, marker: str, content: str, label: str) -> str:
    check_line = content.strip().split("\n")[0]
    if check_line in text:
        print(f"  [skip] {label} already applied")
        return text
    if marker not in text:
        print(f"  [warn] Could not find marker for {label}")
        return text
    return text.replace(marker, content + marker, 1)


def main() -> None:
    if not IMAGE_TOOL_PATH.exists():
        raise SystemExit(f"Missing file: {IMAGE_TOOL_PATH}")

    text = IMAGE_TOOL_PATH.read_text(encoding="utf-8")

    # Patch 1: Add side-by-side helper function
    text = insert_before(text, HELPER_MARKER, SIDE_BY_SIDE_HELPER, "side-by-side helper")

    # Patch 2: Hook into image_transform result
    text = replace_once(text, TRANSFORM_RETURN_OLD, TRANSFORM_RETURN_NEW, "transform return hook")

    IMAGE_TOOL_PATH.write_text(text, encoding="utf-8")
    print("Side-by-side comparison patch applied.")
    print("Make sure Pillow is installed: pip install Pillow")
    print("Restart Hermes gateway after this.")


if __name__ == "__main__":
    main()
