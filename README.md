# Stylish Hermes

AI Personal Stylist MVP built for Hermes Agent.

## What This Does

- Analyzes clothing photos
- Stores wardrobe inventory locally in `~/.hermes/data/wardrobe.json`
- Suggests outfits based on weather and occasion
- Generates optional outfit visuals
- Supports Telegram and cron-based reminders through Hermes

## Project Structure

```text
skill/SKILL.md
data/wardrobe.json
docs/prompts.md
docs/first-run-checklist.md
docs/cron-prompts.md
scripts/setup-wsl.sh
```

## Quick Start

1. Install Hermes Agent in WSL2.
2. Copy `skill/SKILL.md` to `~/.hermes/skills/lifestyle/ai-personal-stylist/SKILL.md`.
3. Copy `data/wardrobe.json` to `~/.hermes/data/wardrobe.json`.
4. Add your API keys to `~/.hermes/.env`.
5. Run `hermes gateway setup`.
6. Test the skill manually before adding cron jobs.

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

- Do not store the full wardrobe in Hermes memory.
- Use Hermes memory only for short user profile summaries.
- Store the full wardrobe in `wardrobe.json`.
- `ffmpeg` is optional unless you want voice-heavy TTS flows.
