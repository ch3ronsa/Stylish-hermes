# Stylish Hermes

**AI stylist that lives in Telegram.** Send a fashion inspiration image, get a wearable real-life outfit back.

Built on [Hermes Agent](https://github.com/hermes-agent) for the Moltiverse Hackathon.

---

## The Problem

People save fashion inspiration everywhere - Pinterest, Instagram, anime, editorials - but still don't know how to actually **wear** it. Existing AI tools just label outfits ("old money", "streetwear") without telling you what to put on.

## The Solution

Stylish Hermes **translates** inspiration into action:

1. **Send** any reference image to the Telegram bot
2. **Analyze** - AI breaks down aesthetic, palette, silhouette, mood
3. **Transform** - converts the vibe into a wearable outfit for your context
4. **Generate** - creates a polished image of the transformed outfit

> This is transformation, not recreation. The bot doesn't copy the reference - it translates the aesthetic into something you can actually wear.

## Key Features

| Feature | Description |
|---------|-------------|
| Visual Transform | Reference image in, transformed outfit image out |
| Side-by-Side Compare | Original inspiration + transformed outfit in one image |
| Moodboard Analysis | Send multiple images, get a unified style direction |
| Shopping with Links | Real product suggestions with prices via web search |
| Color Palette Analysis | Harmony type, undertones, seasonal compatibility |
| Try-On Visualization | Experimental overlay of outfits on user photos |
| Inline Keyboard | One-tap style choices (Casual, Office, Bold) |
| Smart Fallbacks | Triple image gen: FAL -> OpenAI -> Gemini |
| Session Memory | Remembers previous images within a conversation |
| Auto Styling | Scheduled daily outfit recs with weather awareness |

## Tech Stack

- **Orchestration:** Hermes Agent
- **Interface:** Telegram Bot
- **Vision/Chat:** GLM-4 Vision
- **Image Generation:** FAL FLUX 2 Pro / OpenAI DALL-E / Google Gemini
- **Image Transform:** Gemini multimodal (reference + prompt -> new outfit)
- **Web Search:** Firecrawl API

## Quick Start

```bash
# 1. Install Hermes Agent in WSL2
bash scripts/setup-wsl.sh

# 2. Copy skill definition
cp skill/SKILL.md ~/.hermes/skills/lifestyle/ai-personal-stylist/SKILL.md

# 3. Configure environment
cp .env.example ~/.hermes/.env
# Edit ~/.hermes/.env with your API keys

# 4. Validate config
python3 scripts/validate-config.py

# 5. Apply patches (run the ones you need)
python3 scripts/fix-hermes-max-tokens.py
python3 scripts/enable-gemini-image-transform.py
python3 scripts/enable-openai-image-fallback.py
python3 scripts/enable-gemini-image-fallback.py
python3 scripts/enable-inline-keyboard.py
python3 scripts/enable-side-by-side.py
python3 scripts/enable-provider-logging.py
python3 scripts/enable-rate-limiting.py

# 6. Start the bot
hermes gateway setup
hermes gateway
```

## Required API Keys

```bash
TELEGRAM_BOT_TOKEN=...        # Required - get from @BotFather
GLM_API_KEY=...               # Required - vision + chat model
FAL_KEY=...                   # Image gen (primary)
OPENAI_API_KEY=...            # Image gen (fallback 1)
GEMINI_API_KEY=...            # Image gen (fallback 2) + visual transform
FIRECRAWL_API_KEY=...         # Optional - web search & weather
```

At least one image generation key is needed for visual output.

## Project Structure

```
skill/SKILL.md                         # Bot behavior definition (11 workflows)
demo/index.html                        # Interactive demo showcase page
demo/DEMO-SCRIPT.md                    # 90-second demo script
docs/
  prompts.md                           # 23 ready-to-use prompts
  how-it-works.md                      # Core concept explanation
  hackathon-demo.md                    # Demo flow guide
  hackathon-pitch.md                   # Pitch versions (15s/30s/60s)
scripts/
  setup-wsl.sh                         # WSL2 initial setup
  validate-config.py                   # Config validator
  fix-hermes-max-tokens.py             # Token limit patch
  enable-openai-image-fallback.py      # OpenAI fallback
  enable-gemini-image-fallback.py      # Gemini fallback
  enable-gemini-image-transform.py     # Visual transform feature
  apply-gemini-patches.py              # Meta Gemini patcher
  enable-inline-keyboard.py            # Telegram button UI
  enable-side-by-side.py               # Before/after comparison images
  enable-provider-logging.py           # Provider usage analytics
  enable-rate-limiting.py              # Anti-spam protection
  cleanup-image-cache.py               # Disk space management
  setup-cron-jobs.py                   # Automated scheduling
```

## Why It Wins

- **Visual in, visual out** - strong before-and-after demo moment
- **Zero friction** - no app to download, lives in Telegram
- **No fashion vocabulary needed** - send a photo, get an outfit
- **Real agent workflow** - not a GPT wrapper, actual agentic pipeline with fallbacks
- **Transformation, not recreation** - translates aesthetic into something wearable

## License

MIT
