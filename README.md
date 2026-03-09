# Stylish Hermes

Stylish Hermes is a Telegram-first AI stylist built on Hermes Agent.

The product is not a wardrobe tracker by default. It is an inspiration-to-outfit translator:

1. the user sends a reference image
2. the bot explains the aesthetic
3. the bot turns that vibe into a wearable real-life outfit
4. the bot can generate a polished inspired look image

## Hackathon Demo

This is the core demo loop:

1. Send an inspiration image through Telegram.
2. Get back a short style breakdown.
3. Ask for a wearable version.
4. Ask for a generated fashion image.

Use these docs during the presentation:

- [how-it-works.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/how-it-works.md)
- [hackathon-demo.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/hackathon-demo.md)
- [hackathon-pitch.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/hackathon-pitch.md)
- [prompts.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/prompts.md)

## What It Does

- Reads outfit inspiration from Telegram image uploads
- Identifies aesthetic, silhouette, palette, and occasion fit
- Transforms abstract fashion references into different practical real-life outfits
- Generates a new transformed version with FAL, OpenAI, or Gemini image generation (triple fallback)
- Keeps wardrobe tracking optional instead of forcing inventory collection

## Why It Feels Like A Product

- It starts where users already are: Telegram
- It accepts visual references instead of requiring fashion vocabulary
- It does transformation, not simple recreation
- It produces both explanation and visual payoff

## Stack

- Hermes Agent for orchestration
- Telegram as the user-facing interface
- GLM for chat and image understanding
- FAL as the default image generator
- OpenAI Images as the first fallback
- Google Gemini as the second fallback

## Quick Start

1. Install Hermes Agent in WSL2.
2. Copy [SKILL.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/skill/SKILL.md) to `~/.hermes/skills/lifestyle/ai-personal-stylist/SKILL.md`.
3. Add your API keys to `~/.hermes/.env`.
4. Run `hermes gateway setup`.
5. Start the bot with `hermes gateway`.
6. Test the Telegram flow before the demo.

## Required Secrets

```bash
GLM_API_KEY=...
GLM_BASE_URL=https://api.z.ai/api/coding/paas/v4
FAL_KEY=...                    # Image gen primary (optional)
OPENAI_API_KEY=...             # Image gen fallback 1 (optional)
GEMINI_API_KEY=...             # Image gen fallback 2 (optional)
TELEGRAM_BOT_TOKEN=...
AUXILIARY_VISION_PROVIDER=main
AUXILIARY_VISION_MODEL=glm-4.6v-flash
```

At least one image generation key (FAL_KEY, OPENAI_API_KEY, or GEMINI_API_KEY) is needed for visual output.

## Project Structure

```text
skill/SKILL.md
docs/prompts.md
docs/how-it-works.md
docs/hackathon-demo.md
docs/hackathon-pitch.md
docs/first-run-checklist.md
docs/cron-prompts.md
data/wardrobe.json
scripts/setup-wsl.sh
scripts/fix-hermes-max-tokens.py
scripts/enable-openai-image-fallback.py
scripts/enable-gemini-image-fallback.py
```

## Notes

- Demo Telegram, not the raw terminal.
- The default mode is inspiration analysis.
- The best demo is transformation, not recreation.
- Only use wardrobe mode if the user explicitly wants to track real clothes.
- Never commit real API keys or bot tokens.
- If FAL is locked or out of balance, run `python scripts/enable-openai-image-fallback.py` and use `OPENAI_API_KEY`.
- If OpenAI billing limit is hit, run `python scripts/enable-gemini-image-fallback.py` and use `GEMINI_API_KEY`.
- Fallback order: FAL -> OpenAI -> Gemini. At least one must be configured.
