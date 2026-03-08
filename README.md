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

- [hackathon-demo.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/hackathon-demo.md)
- [hackathon-pitch.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/hackathon-pitch.md)
- [prompts.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/prompts.md)

## What It Does

- Reads outfit inspiration from Telegram image uploads
- Identifies aesthetic, silhouette, palette, and occasion fit
- Translates abstract fashion references into practical real-life styling
- Generates a realistic inspired version with FAL
- Keeps wardrobe tracking optional instead of forcing inventory collection

## Stack

- Hermes Agent for orchestration
- Telegram as the user-facing interface
- GLM for chat and image understanding
- FAL for image generation

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
FAL_KEY=...
TELEGRAM_BOT_TOKEN=...
AUXILIARY_VISION_PROVIDER=main
AUXILIARY_VISION_MODEL=glm-4.6v-flash
```

## Project Structure

```text
skill/SKILL.md
docs/prompts.md
docs/hackathon-demo.md
docs/hackathon-pitch.md
docs/first-run-checklist.md
docs/cron-prompts.md
data/wardrobe.json
scripts/setup-wsl.sh
scripts/fix-hermes-max-tokens.py
```

## Notes

- Demo Telegram, not the raw terminal.
- The default mode is inspiration analysis.
- Only use wardrobe mode if the user explicitly wants to track real clothes.
- Never commit real API keys or bot tokens.
