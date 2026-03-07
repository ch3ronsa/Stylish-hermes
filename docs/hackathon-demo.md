# Hackathon Demo

## Scope

This MVP is not a wardrobe tracker-first app.
It is an inspiration-first AI stylist built on Hermes Agent.

Core promise:
- analyze a style image
- explain the aesthetic
- extract the color palette and occasion fit
- turn the reference into a wearable real-life version

## Demo Flow

Use one clean inspiration image and one short prompt.

Prompt:

```text
Use the ai-personal-stylist skill. Inspiration mode only. Do not add anything to wardrobe. Analyze this image briefly: aesthetic, color palette, occasion, and one simple real-life version of the look.
```

If Hermes asks for a path, use a WSL path like:

```text
/mnt/c/Users/cheo/Downloads/example.png
```

## What To Say While Demoing

1. This is an inspiration-first stylist, not a closet logger.
2. I can give it anime, Pinterest, editorial, or lookbook references.
3. It identifies the vibe, explains why it works, and converts it into a wearable version.
4. The same system can later extend into shopping, weather styling, and optional wardrobe mode.

## Judge-Friendly Points

- Clear user value: style inspiration becomes actionable
- Works with ambiguous or aesthetic-heavy references
- Practical output, not just labels
- Built on Hermes tools and skills, not a static prompt dump

## Safe Backup Prompt

If the first prompt is too broad, use:

```text
Use the ai-personal-stylist skill. Inspiration mode only. Do not add anything to wardrobe. Tell me the aesthetic, key colors, best occasion, and a simpler everyday version.
```

## Do Not Demo

- wardrobe tracking
- cron jobs
- Telegram setup
- image generation
- long multi-step flows

These are extras. The demo should stay on the core loop.
