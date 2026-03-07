# Stylish Hermes

AI Personal Stylist MVP built for Hermes Agent.

## What This Does

- Analyzes inspiration images, moodboards, editorials, anime references, and outfit photos
- Explains style aesthetics, silhouettes, and color palettes
- Translates inspiration looks into wearable real-life outfits
- Suggests outfits based on weather and occasion
- Optionally stores wardrobe inventory locally only when the user explicitly wants wardrobe tracking

## Project Structure

```text
skill/SKILL.md
data/wardrobe.json
docs/prompts.md
docs/first-run-checklist.md
docs/cron-prompts.md
docs/hackathon-demo.md
docs/hackathon-pitch.md
scripts/setup-wsl.sh
scripts/fix-hermes-max-tokens.py
```

## Quick Start

1. Install Hermes Agent in WSL2.
2. Copy `skill/SKILL.md` to `~/.hermes/skills/lifestyle/ai-personal-stylist/SKILL.md`.
3. Copy `data/wardrobe.json` to `~/.hermes/data/wardrobe.json`.
4. Add your API keys to `~/.hermes/.env`.
5. Run `hermes gateway setup`.
6. Test the skill manually before adding cron jobs.

## Hackathon Focus

For the demo, stay on the core loop:

1. give Hermes an inspiration image
2. get back the aesthetic, palette, occasion, and wearable version

Use [docs/hackathon-demo.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/hackathon-demo.md) for the demo flow and [docs/hackathon-pitch.md](/c:/Users/cheo/Desktop/projeler/nous/Stylish-hermes/docs/hackathon-pitch.md) for the short pitch.

## Required Environment Variables

```bash
OPENROUTER_API_KEY=sk-or-...
FAL_KEY=...
FIRECRAWL_API_KEY=fc-...
TELEGRAM_BOT_TOKEN=...
```

## Security

- Never commit real API keys or bot tokens.
- Keep secrets only in `~/.hermes/.env` on your machine.
- This repository should contain only templates and example files.
- `.env` files are ignored by git in this repo.

## Notes

- The default mode is inspiration analysis, not wardrobe tracking.
- Do not store the full wardrobe in Hermes memory.
- Use Hermes memory only for short user profile summaries.
- Use `wardrobe.json` only if you explicitly want to track real owned clothing.
- `ffmpeg` is optional unless you want voice-heavy TTS flows.

## Low-Credit Fix

If Hermes keeps failing with an OpenRouter `402` error mentioning `65536 tokens`, run:

```bash
python3 /mnt/c/Users/cheo/Desktop/projeler/nous/Stylish-hermes/scripts/fix-hermes-max-tokens.py
```

This patches the local Hermes CLI to honor `agent.max_tokens` from `~/.hermes/config.yaml`
and sets that limit to `4096`.
