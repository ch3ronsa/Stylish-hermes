# Stylish Hermes

**AI stylist that lives in Telegram.** Send a fashion inspiration image — get a wearable real-life outfit back.

Built on [Hermes Agent](https://github.com/hermes-agent) for the Moltiverse Hackathon.

---

## The Problem

People save fashion inspiration everywhere — Pinterest, Instagram, anime, editorials — but still don't know how to actually **wear** it. Existing AI tools just label outfits ("old money", "streetwear") without telling you what to put on.

## The Solution

Stylish Hermes **translates** inspiration into action:

```
Reference Image  →  Vision Analysis  →  Style Transform  →  New Outfit Image
```

> This is transformation, not recreation. The bot doesn't copy the reference — it translates the aesthetic into something you can actually wear.

## Features

| Feature | What It Does |
|---------|-------------|
| **Inspiration Analysis** | Break down any image: aesthetic, palette, silhouette, mood, wearability |
| **Visual Transform** | Send a reference image + context → get a new wearable outfit image |
| **Moodboard Analysis** | Send multiple images → get a unified style direction |
| **Color Palette Analysis** | Analyze color harmony, undertones, seasonal compatibility |
| **Celebrity Style Match** | "Who dresses like this?" → top 3 celebrity matches with % |
| **Style DNA Card** | Your unique style identity: categories, signature colors, power piece |

### Supporting Features

| Feature | What It Does |
|---------|-------------|
| Session Memory | Bot remembers all images within a conversation |
| Inline Keyboard | One-tap style buttons in Telegram (Casual, Office, Bold) |
| Smart Fallbacks | Triple image generation chain: FAL → OpenAI → Gemini |
| Side-by-Side | Original inspiration + transformed outfit in one image |
| Rate Limiting | Anti-spam protection (5 msgs / 30s per user) |

## How It Works — Technical Deep Dive

### The Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Telegram    │────▶│  Hermes      │────▶│  Vision Engine   │────▶│  Transform   │
│  Interface   │     │  Agent Core  │     │  (GLM-4 Vision)  │     │  Engine      │
└─────────────┘     └──────────────┘     └─────────────────┘     └──────────────┘
                           │                      │                       │
                    Skill Router            Aesthetic              Image Gen with
                    + Session Mgmt          Extraction             Reference Context
                                                                         │
                                                                  ┌──────▼──────┐
                                                                  │  Fallback   │
                                                                  │  Chain      │
                                                                  │             │
                                                                  │ FAL FLUX 2  │
                                                                  │     ↓       │
                                                                  │ OpenAI      │
                                                                  │ DALL-E 3    │
                                                                  │     ↓       │
                                                                  │ Gemini      │
                                                                  │ Imagen      │
                                                                  └─────────────┘
```

### What Makes This Different From a GPT Wrapper

Most "AI fashion" tools are a single LLM call with a system prompt. Stylish Hermes is an **agentic pipeline**:

1. **Skill-Based Routing** — Hermes Agent reads the SKILL.md spec at boot and routes user messages to the correct workflow. No hardcoded if/else chains.

2. **Vision → Transform Loop** — The bot first *understands* the reference image (extracting 6 aesthetic dimensions), then uses that understanding to *generate* a new image. The transform prompt is built from the analysis, not from the user's raw text.

3. **Resilient Image Generation** — Three independent providers with automatic failover. If FAL is down, OpenAI picks up. If OpenAI quota runs out, Gemini takes over. The user never sees an error.

4. **Session Context** — Within a conversation, the bot tracks every image and analysis. "Make the first one more casual" works because the bot knows what "the first one" is.

5. **Reference-Aware Generation** — Unlike text-to-image, the transform pipeline passes the original image as a reference to the generation model (via Gemini multimodal). The output inherits the *vibe* of the reference, not just keywords.

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | Hermes Agent (skill-based LLM agent framework) |
| Interface | Telegram Bot API |
| Vision Model | GLM-4 Vision (aesthetic analysis) |
| Image Generation | FAL FLUX 2 Pro → OpenAI DALL-E 3 → Google Gemini Imagen |
| Image Transform | Gemini multimodal (reference image + prompt → new image) |

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

# 5. Apply patches
python3 scripts/fix-hermes-max-tokens.py
python3 scripts/enable-gemini-image-transform.py
python3 scripts/enable-openai-image-fallback.py
python3 scripts/enable-gemini-image-fallback.py
python3 scripts/enable-inline-keyboard.py
python3 scripts/enable-side-by-side.py

# 6. Start the bot
hermes gateway setup
hermes gateway
```

### Required API Keys

| Key | Purpose | Required |
|-----|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot interface | Yes |
| `GLM_API_KEY` | Vision + chat model | Yes |
| `FAL_KEY` | Image generation (primary) | At least one |
| `OPENAI_API_KEY` | Image generation (fallback 1) | At least one |
| `GEMINI_API_KEY` | Image generation (fallback 2) + visual transform | At least one |

## Project Structure

```
skill/SKILL.md                         # Bot brain — 6 workflows, personality, rules
scripts/
  setup-wsl.sh                         # WSL2 initial setup
  validate-config.py                   # Config validator
  fix-hermes-max-tokens.py             # Token limit patch
  enable-openai-image-fallback.py      # OpenAI fallback
  enable-gemini-image-fallback.py      # Gemini fallback
  enable-gemini-image-transform.py     # Visual transform feature
  apply-gemini-patches.py              # Meta Gemini patcher
  enable-inline-keyboard.py            # Telegram button UI
  enable-side-by-side.py               # Before/after comparison
  enable-provider-logging.py           # Provider usage analytics
  enable-rate-limiting.py              # Anti-spam protection
  cleanup-image-cache.py               # Disk space management
demo/
  index.html                           # Interactive showcase page
  DEMO-SCRIPT.md                       # Live demo walkthrough
```

## Roadmap

These features are designed and specced but not yet wired up:

- **Wardrobe Tracking** — Save real clothing items, get outfit combos from your own closet
- **Shopping with Links** — Real product suggestions with prices via web search (needs Firecrawl API)
- **Try-On Visualization** — See outfits on your own body using image transform
- **Weather-Aware Recs** — Daily outfit suggestions based on local weather
- **Multi-Language** — Full Turkish + English support with auto-detection

## License

MIT
