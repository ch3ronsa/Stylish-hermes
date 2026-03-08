# Hackathon Demo

## Product Story

Stylish Hermes helps people turn saved fashion inspiration into something wearable.

Instead of asking users to manually build a wardrobe database first, the product starts with the way people already behave:

- they save looks
- they send references to friends
- they want to know how to recreate the vibe

This demo shows that loop inside Telegram.

## Demo Goal

By the end of the demo, the judges should understand one simple thing:

**This bot can look at a reference image, understand the style, and transform it into a different wearable outfit.**

## Happy Path

### Step 1

Open Telegram and send one strong reference image.

Best choices:
- editorial fashion photo
- Pinterest outfit collage
- anime-inspired fashion look
- runway or lookbook image
- AI-generated fashion concept image

### Step 2

Send this:

```text
Analyze this image briefly: aesthetic, colors, occasion, wearable version.
```

### Step 3

After the analysis lands, send this:

```text
Transform this look into a smart-casual everyday outfit for Istanbul spring. Keep the vibe, but make it practical, wearable, and visually different from the original.
```

### Step 4

After the transformation lands, send this:

```text
Generate the transformed version as a realistic fashion image.
```

### Step 5

Show the generated result and explain that the bot is not recreating the reference. It is translating the aesthetic into a new, usable outfit.

## What To Say During The Demo

Use short lines. Do not over-explain.

Suggested narration:

1. "Most people already collect inspiration images, but they do not know how to turn them into something wearable."
2. "Our bot lives in Telegram, where users already share taste and references."
3. "First it interprets the style. Then it transforms that vibe into a different outfit for a real context."
4. "And instead of stopping at text, it can generate the transformed result."

## Why This Is A Good Hackathon Demo

- The input is visual.
- The output is visual.
- The interface is familiar.
- The value is obvious in under a minute.
- It feels like a product, not a terminal experiment.

## Backup Lines For Judges

- "This is taste-to-execution."
- "We convert inspiration into actionable styling."
- "We do transformation, not simple recreation."
- "The user does not need fashion vocabulary to get value."

## Backup Prompt

If the main prompt feels too long, use this:

```text
Transform this into a practical everyday look while keeping the same vibe.
```

## Backup Plan

If generation fails:

1. Show the analysis output.
2. Explain that the generation step is optional enhancement.
3. Emphasize that the core product value is interpretation plus translation.
