from __future__ import annotations

import os
from pathlib import Path


IMAGE_TOOL_PATH = Path.home() / ".hermes" / "hermes-agent" / "tools" / "image_generation_tool.py"
TELEGRAM_PATH = Path.home() / ".hermes" / "hermes-agent" / "gateway" / "platforms" / "telegram.py"


IMAGE_IMPORT_OLD = """import json
import logging
import os
import asyncio
import datetime
from typing import Dict, Any, Optional, Union
"""

IMAGE_IMPORT_NEW = """import base64
import json
import logging
import os
import asyncio
import datetime
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional, Union
"""

IMAGE_CONSTANTS_OLD = """VALID_OUTPUT_FORMATS = ["jpeg", "png"]
VALID_ACCELERATION_MODES = ["none", "regular", "high"]

_debug = DebugSession("image_tools", env_var="IMAGE_TOOLS_DEBUG")
"""

IMAGE_CONSTANTS_NEW = """VALID_OUTPUT_FORMATS = ["jpeg", "png"]
VALID_ACCELERATION_MODES = ["none", "regular", "high"]
OPENAI_IMAGE_MODEL = "gpt-image-1"
OPENAI_SIZE_MAP = {
    "landscape": "1536x1024",
    "square": "1024x1024",
    "portrait": "1024x1536",
}

_debug = DebugSession("image_tools", env_var="IMAGE_TOOLS_DEBUG")


def _save_generated_image(image_bytes: bytes, extension: str) -> str:
    cache_dir = Path(os.path.expanduser("~/.hermes/image_cache"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_{timestamp}_{os.getpid()}.{extension}"
    path = cache_dir / filename
    path.write_bytes(image_bytes)
    return str(path)


def _generate_with_openai(
    prompt: str,
    aspect_ratio: str,
    output_format: str,
) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    size = OPENAI_SIZE_MAP.get(aspect_ratio, OPENAI_SIZE_MAP[DEFAULT_ASPECT_RATIO])
    payload = {
        "model": OPENAI_IMAGE_MODEL,
        "prompt": prompt,
        "size": size,
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        body = json.loads(response.read().decode("utf-8"))

    data = body.get("data") or []
    if not data:
        raise ValueError("OpenAI image API returned no images")

    image_item = data[0]
    b64_image = image_item.get("b64_json")
    if not b64_image:
        raise ValueError("OpenAI image API returned no base64 image payload")

    image_bytes = base64.b64decode(b64_image)
    extension = "jpg" if output_format == "jpeg" else output_format
    local_path = _save_generated_image(image_bytes, extension)
    return {
        "path": local_path,
        "model": OPENAI_IMAGE_MODEL,
        "provider": "openai",
    }
"""

IMAGE_BLOCK_OLD = """        # Check API key availability
        if not os.getenv("FAL_KEY"):
            raise ValueError("FAL_KEY environment variable not set")
        
        # Validate other parameters
        validated_params = _validate_parameters(
            image_size, num_inference_steps, guidance_scale, num_images, output_format, "none"
        )
        
        # Prepare arguments for FAL.ai FLUX 2 Pro API
        arguments = {
            "prompt": prompt.strip(),
            "image_size": validated_params["image_size"],
            "num_inference_steps": validated_params["num_inference_steps"],
            "guidance_scale": validated_params["guidance_scale"],
            "num_images": validated_params["num_images"],
            "output_format": validated_params["output_format"],
            "enable_safety_checker": ENABLE_SAFETY_CHECKER,
            "safety_tolerance": SAFETY_TOLERANCE,
            "sync_mode": True  # Use sync mode for immediate results
        }
        
        # Add seed if provided
        if seed is not None and isinstance(seed, int):
            arguments["seed"] = seed
        
        logger.info("Submitting generation request to FAL.ai FLUX 2 Pro...")
        logger.info("  Model: %s", DEFAULT_MODEL)
        logger.info("  Aspect Ratio: %s -> %s", aspect_ratio_lower, image_size)
        logger.info("  Steps: %s", validated_params['num_inference_steps'])
        logger.info("  Guidance: %s", validated_params['guidance_scale'])
        
        # Submit request to FAL.ai
        handler = await fal_client.submit_async(
            DEFAULT_MODEL,
            arguments=arguments
        )
        
        # Get the result
        result = await handler.get()
        
        generation_time = (datetime.datetime.now() - start_time).total_seconds()
        
        # Process the response
        if not result or "images" not in result:
            raise ValueError("Invalid response from FAL.ai API - no images returned")
        
        images = result.get("images", [])
        if not images:
            raise ValueError("No images were generated")
        
        # Format image data and upscale images
        formatted_images = []
        for img in images:
            if isinstance(img, dict) and "url" in img:
                original_image = {
                    "url": img["url"],
                    "width": img.get("width", 0),
                    "height": img.get("height", 0)
                }
                
                # Attempt to upscale the image
                upscaled_image = await _upscale_image(img["url"], prompt.strip())
                
                if upscaled_image:
                    # Use upscaled image if successful
                    formatted_images.append(upscaled_image)
                else:
                    # Fall back to original image if upscaling fails
                    logger.warning("Using original image as fallback")
                    original_image["upscaled"] = False
                    formatted_images.append(original_image)
        
        if not formatted_images:
            raise ValueError("No valid image URLs returned from API")
        
        upscaled_count = sum(1 for img in formatted_images if img.get("upscaled", False))
        logger.info("Generated %s image(s) in %.1fs (%s upscaled)", len(formatted_images), generation_time, upscaled_count)
        
        # Prepare successful response - minimal format
        response_data = {
            "success": True,
            "image": formatted_images[0]["url"] if formatted_images else None
        }
        
        debug_call_data["success"] = True
        debug_call_data["images_generated"] = len(formatted_images)
        debug_call_data["generation_time"] = generation_time
"""

IMAGE_BLOCK_NEW = """        # Validate other parameters
        validated_params = _validate_parameters(
            image_size, num_inference_steps, guidance_scale, num_images, output_format, "none"
        )

        response_data = None

        if os.getenv("FAL_KEY"):
            try:
                arguments = {
                    "prompt": prompt.strip(),
                    "image_size": validated_params["image_size"],
                    "num_inference_steps": validated_params["num_inference_steps"],
                    "guidance_scale": validated_params["guidance_scale"],
                    "num_images": validated_params["num_images"],
                    "output_format": validated_params["output_format"],
                    "enable_safety_checker": ENABLE_SAFETY_CHECKER,
                    "safety_tolerance": SAFETY_TOLERANCE,
                    "sync_mode": True
                }

                if seed is not None and isinstance(seed, int):
                    arguments["seed"] = seed

                logger.info("Submitting generation request to FAL.ai FLUX 2 Pro...")
                logger.info("  Model: %s", DEFAULT_MODEL)
                logger.info("  Aspect Ratio: %s -> %s", aspect_ratio_lower, image_size)

                handler = await fal_client.submit_async(
                    DEFAULT_MODEL,
                    arguments=arguments
                )
                result = await handler.get()

                if not result or "images" not in result:
                    raise ValueError("Invalid response from FAL.ai API - no images returned")

                images = result.get("images", [])
                if not images:
                    raise ValueError("No images were generated")

                formatted_images = []
                for img in images:
                    if isinstance(img, dict) and "url" in img:
                        original_image = {
                            "url": img["url"],
                            "width": img.get("width", 0),
                            "height": img.get("height", 0)
                        }
                        upscaled_image = await _upscale_image(img["url"], prompt.strip())
                        if upscaled_image:
                            formatted_images.append(upscaled_image)
                        else:
                            logger.warning("Using original image as fallback")
                            original_image["upscaled"] = False
                            formatted_images.append(original_image)

                if formatted_images:
                    upscaled_count = sum(1 for img in formatted_images if img.get("upscaled", False))
                    logger.info("Generated %s image(s) with FAL (%s upscaled)", len(formatted_images), upscaled_count)
                    response_data = {
                        "success": True,
                        "image": formatted_images[0]["url"],
                    }
            except Exception as fal_error:
                logger.warning("FAL image generation failed, trying OpenAI fallback: %s", fal_error)

        if response_data is None:
            openai_result = await asyncio.to_thread(
                _generate_with_openai,
                prompt.strip(),
                aspect_ratio_lower,
                validated_params["output_format"],
            )
            logger.info("Generated image with OpenAI fallback: %s", openai_result["path"])
            response_data = {
                "success": True,
                "image": f"MEDIA:{openai_result['path']}",
            }

        generation_time = (datetime.datetime.now() - start_time).total_seconds()

        debug_call_data["success"] = True
        debug_call_data["images_generated"] = 1
        debug_call_data["generation_time"] = generation_time
"""

IMAGE_REQUIREMENTS_OLD = """def check_image_generation_requirements() -> bool:
    \"\"\"
    Check if all requirements for image generation tools are met.
    
    Returns:
        bool: True if requirements are met, False otherwise
    \"\"\"
    try:
        # Check API key
        if not check_fal_api_key():
            return False
        
        # Check if fal_client is available
        import fal_client
        return True
        
    except ImportError:
        return False
"""

IMAGE_REQUIREMENTS_NEW = """def check_image_generation_requirements() -> bool:
    \"\"\"
    Check if all requirements for image generation tools are met.
    
    Returns:
        bool: True if requirements are met, False otherwise
    \"\"\"
    try:
        if check_fal_api_key():
            import fal_client
            return True
        return bool(os.getenv("OPENAI_API_KEY"))
        
    except ImportError:
        return False
"""

TELEGRAM_INSERT_AFTER = """        except Exception as e:
            print(f"[{self.name}] Failed to send photo, falling back to URL: {e}")
            # Fallback: send as text link
            return await super().send_image(chat_id, image_url, caption, reply_to)
"""

TELEGRAM_INSERT = """
    async def send_image_file(
        self,
        chat_id: str,
        image_path: str,
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> SendResult:
        \"\"\"Send a local image file natively as a Telegram photo.\"\"\"
        if not self._bot:
            return SendResult(success=False, error="Not connected")

        try:
            if not os.path.exists(image_path):
                return SendResult(success=False, error=f"Image file not found: {image_path}")

            with open(image_path, "rb") as image_file:
                msg = await self._bot.send_photo(
                    chat_id=int(chat_id),
                    photo=image_file,
                    caption=caption[:1024] if caption else None,
                    reply_to_message_id=int(reply_to) if reply_to else None,
                )
            return SendResult(success=True, message_id=str(msg.message_id))
        except Exception as e:
            print(f"[{self.name}] Failed to send local image, falling back to text: {e}")
            return await super().send_image_file(chat_id, image_path, caption, reply_to)
"""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Could not find expected block for {label}")
    return text.replace(old, new, 1)


def patch_image_tool() -> None:
    text = IMAGE_TOOL_PATH.read_text(encoding="utf-8")
    text = replace_once(text, IMAGE_IMPORT_OLD, IMAGE_IMPORT_NEW, "image imports")
    text = replace_once(text, IMAGE_CONSTANTS_OLD, IMAGE_CONSTANTS_NEW, "image constants")
    text = replace_once(text, IMAGE_BLOCK_OLD, IMAGE_BLOCK_NEW, "image generation logic")
    text = replace_once(text, IMAGE_REQUIREMENTS_OLD, IMAGE_REQUIREMENTS_NEW, "image requirements")
    IMAGE_TOOL_PATH.write_text(text, encoding="utf-8")


def patch_telegram() -> None:
    text = TELEGRAM_PATH.read_text(encoding="utf-8")
    if "async def send_image_file(" in text:
        return
    if TELEGRAM_INSERT_AFTER not in text:
        raise SystemExit("Could not find Telegram image send block")
    text = text.replace(TELEGRAM_INSERT_AFTER, TELEGRAM_INSERT_AFTER + TELEGRAM_INSERT, 1)
    TELEGRAM_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    if not IMAGE_TOOL_PATH.exists():
        raise SystemExit(f"Missing file: {IMAGE_TOOL_PATH}")
    if not TELEGRAM_PATH.exists():
        raise SystemExit(f"Missing file: {TELEGRAM_PATH}")

    patch_image_tool()
    patch_telegram()
    print("OpenAI image fallback patch applied.")
    print("Restart Hermes gateway after this.")


if __name__ == "__main__":
    main()
