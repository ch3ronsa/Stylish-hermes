"""
D1: Inline Keyboard Patch for Telegram
Adds inline keyboard support so the bot can offer style choices
(Casual, Office, Bold, etc.) as clickable buttons instead of text.

Run from WSL:
    python3 scripts/enable-inline-keyboard.py
"""
from __future__ import annotations

import os
from pathlib import Path


TELEGRAM_PATH = Path.home() / ".hermes" / "hermes-agent" / "gateway" / "platforms" / "telegram.py"


# --- Patch 1: Add InlineKeyboardButton/Markup imports ---

IMPORT_OLD = "from telegram import Update"

IMPORT_NEW = "from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update"


# --- Patch 2: Add send_inline_keyboard method ---
# We insert after the send_image_file method (or send_image fallback if that doesn't exist)

INSERT_MARKER = "    async def send_image("

KEYBOARD_METHOD = '''
    async def send_inline_keyboard(
        self,
        chat_id: str,
        text: str,
        buttons: list[list[dict]],
        reply_to: str | None = None,
    ) -> "SendResult":
        """Send a message with inline keyboard buttons.

        Args:
            chat_id: Telegram chat ID.
            text: Message text above the buttons.
            buttons: 2D list of button dicts, each with 'text' and 'callback_data'.
                     Example: [[{"text": "Casual", "callback_data": "style_casual"}]]
        """
        if not self._bot:
            return SendResult(success=False, error="Not connected")

        try:
            keyboard = []
            for row in buttons:
                keyboard.append([
                    InlineKeyboardButton(
                        text=btn.get("text", ""),
                        callback_data=btn.get("callback_data", btn.get("text", "")),
                    )
                    for btn in row
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)
            msg = await self._bot.send_message(
                chat_id=int(chat_id),
                text=text,
                reply_markup=reply_markup,
                reply_to_message_id=int(reply_to) if reply_to else None,
            )
            return SendResult(success=True, message_id=str(msg.message_id))
        except Exception as e:
            print(f"[{self.name}] Failed to send inline keyboard: {e}")
            return SendResult(success=False, error=str(e))

'''


# --- Patch 3: Add callback query handler in the start/setup method ---

HANDLER_MARKER = "application.add_handler(MessageHandler("

CALLBACK_HANDLER = """application.add_handler(CallbackQueryHandler(self._handle_callback_query))
        """

CALLBACK_IMPORT_OLD = "from telegram.ext import ApplicationBuilder, MessageHandler"
CALLBACK_IMPORT_NEW = "from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler"


# --- Patch 4: Add the callback query handler method ---

CALLBACK_METHOD_MARKER = "    async def _handle_message("

CALLBACK_METHOD = '''    async def _handle_callback_query(self, update: Update, context) -> None:
        """Handle inline keyboard button presses."""
        query = update.callback_query
        if query is None:
            return
        await query.answer()  # acknowledge the button press
        # Treat the callback data as a user message
        chat_id = str(query.message.chat_id)
        user_text = query.data or ""
        print(f"[{self.name}] Callback query from {chat_id}: {user_text}")
        # Process like a normal message
        await self._process_user_input(chat_id, user_text, None)

'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        print(f"  [skip] {label} already applied")
        return text
    if old not in text:
        raise SystemExit(f"Could not find expected block for {label}")
    return text.replace(old, new, 1)


def insert_before(text: str, marker: str, content: str, label: str) -> str:
    if content.strip().split("\n")[1] in text:
        print(f"  [skip] {label} already applied")
        return text
    if marker not in text:
        raise SystemExit(f"Could not find marker for {label}")
    return text.replace(marker, content + marker, 1)


def insert_after(text: str, marker: str, content: str, label: str) -> str:
    if content.strip().split("\n")[1] in text:
        print(f"  [skip] {label} already applied")
        return text
    if marker not in text:
        raise SystemExit(f"Could not find marker for {label}")
    return text.replace(marker, marker + "\n        " + content, 1)


def main() -> None:
    if not TELEGRAM_PATH.exists():
        raise SystemExit(f"Missing file: {TELEGRAM_PATH}")

    text = TELEGRAM_PATH.read_text(encoding="utf-8")

    # Patch 1: InlineKeyboard imports
    text = replace_once(text, IMPORT_OLD, IMPORT_NEW, "InlineKeyboard imports")

    # Patch 2: CallbackQueryHandler import
    text = replace_once(text, CALLBACK_IMPORT_OLD, CALLBACK_IMPORT_NEW, "CallbackQueryHandler import")

    # Patch 3: Add send_inline_keyboard method
    text = insert_before(text, INSERT_MARKER, KEYBOARD_METHOD, "send_inline_keyboard method")

    # Patch 4: Add callback query handler registration
    text = insert_after(text, HANDLER_MARKER, CALLBACK_HANDLER, "callback handler registration")

    # Patch 5: Add callback query handler method
    text = insert_before(text, CALLBACK_METHOD_MARKER, CALLBACK_METHOD, "callback query handler method")

    TELEGRAM_PATH.write_text(text, encoding="utf-8")
    print("Inline keyboard patch applied successfully.")
    print("Restart Hermes gateway after this.")


if __name__ == "__main__":
    main()
