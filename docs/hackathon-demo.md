# Hackathon Demo

## Scope

This MVP is not a wardrobe tracker-first app.
It is an inspiration-first AI stylist built on Hermes Agent.

Core promise:
- user sends an inspiration image in Telegram
- Hermes explains the aesthetic and occasion fit
- Hermes turns the reference into a wearable real-life version
- Hermes can generate a polished inspired look image with FAL

## Demo Flow

Use Telegram as the front door.
Do not demo the raw terminal unless something breaks.

### Step 1: Send an inspiration image in Telegram

Use one strong image: editorial, Pinterest, anime, runway, or a Gemini-generated fashion image.

### Step 2: Ask for analysis

Prompt:

```text
Use the ai-personal-stylist skill. Inspiration mode only. Do not add anything to wardrobe. Analyze this image briefly: aesthetic, color palette, occasion, and one simple real-life version of the look.
```

### Step 3: Ask for the wow moment

Prompt:

```text
Use the ai-personal-stylist skill. Inspiration mode only. Do not add anything to wardrobe. Generate one polished, wearable inspired version of this look as a realistic fashion image. Keep the core vibe, but make it believable for real life.
```

## What To Say While Demoing

1. This is a stylist that starts from taste, not inventory.
2. Users already collect inspiration in chats and social apps, so Telegram is the natural interface.
3. The product does two things: interpret the reference, then translate it into something wearable.
4. The FAL-generated output makes the recommendation feel like a product, not just a text answer.

## Judge-Friendly Points

- Clear user value: style inspiration becomes actionable
- Works with ambiguous or aesthetic-heavy references
- Practical output, not just labels
- Messaging-first experience instead of a developer-facing interface
- Visual output creates a stronger demo moment
- Built on Hermes tools and skills, not a static prompt dump

## Telegram Setup Before Demo

1. `hermes gateway setup`
2. Connect the Telegram bot token
3. Start the gateway
4. Message the bot from Telegram

## FAL Setup Before Demo

1. Put `FAL_KEY=...` in `~/.hermes/.env`
2. Restart Hermes or the gateway
3. Use the generation prompt only after analysis succeeds

## Safe Backup Prompt

```text
Use the ai-personal-stylist skill. Inspiration mode only. Do not add anything to wardrobe. Tell me the aesthetic, key colors, best occasion, and a simpler everyday version.
```

## If Telegram Fails

Fallback order:

1. Hermes CLI with the same prompt
2. analysis only
3. skip generation only if FAL is unavailable
