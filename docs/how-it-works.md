# How It Works

## Core Idea

Stylish Hermes does not try to redraw the same outfit the user already sent.

It does something more useful:

1. reads a reference image
2. understands the aesthetic behind it
3. translates that aesthetic into a different, more practical outfit
4. generates a new visual result that fits the user's context

In short:

**reference image in, transformed outfit out**

## Product Flow

### 1. Image Input

The user sends a fashion reference image in Telegram.

This can be:
- Pinterest inspiration
- editorial fashion
- anime-inspired styling
- runway looks
- AI-generated concept fashion

### 2. Style Interpretation

Hermes analyzes the reference and extracts:
- aesthetic direction
- color palette
- silhouette
- mood
- occasion fit
- what makes the look work

### 3. Transformation

Instead of copying the image, the system adapts it using constraints such as:
- everyday wear
- workwear
- different climate
- budget-friendly alternatives
- masculine or feminine reinterpretation
- toned-down real-life version

This is the real product value.

### 4. Visual Output

The transformed concept can then be turned into a realistic generated fashion image.

Image generation providers (in fallback order):
- FAL (FLUX 2 Pro + Clarity Upscaler)
- OpenAI (DALL-E 3)
- Gemini (gemini-2.0-flash-exp)

That creates a strong before-and-after moment:
- original inspiration
- transformed wearable version

## Why This Is Better Than Simple Outfit Recreation

Simple recreation is weak because the user already has the image.

Stylish Hermes is stronger because it answers:
- How do I actually wear this?
- How do I make this less costume-like?
- How do I adapt this for my life?
- How do I keep the vibe but change the outfit?

## Demoable Transformations

### Everyday adaptation

Take a dramatic or polished reference and make it wearable for normal city life.

### Constraint-based styling

Adapt the same vibe for:
- spring weather
- office use
- lower budget
- more casual settings

### Identity shift

Keep the energy of the original look, but redesign it for a different silhouette or styling direction.

## User Experience

The user does not need to know fashion terminology.

They can simply:
- send an image
- ask for a transformation
- get a result that feels useful

That makes the product accessible, fast, and easy to demo.

## Advanced Features

### Visual Transform (Reference -> New Outfit)

When `image_transform` is available (requires Gemini), the system can take the actual reference image and generate a transformed version directly. This creates a stronger visual connection between the original inspiration and the wearable result.

### Moodboard Analysis

Users can send multiple inspiration images. The system finds common threads across all images (shared palette, recurring silhouettes, consistent mood) and synthesizes a unified style direction.

### Shopping Guidance

After analyzing or transforming a look, the system can search for real products using `web_search` and provide specific shopping suggestions with approximate prices and store names.

### Color Palette Analysis

Deep color analysis including harmony type (complementary, analogous, monochromatic), undertone detection, seasonal color theory matching, and alternative palette suggestions.

### Try-On Visualization

Experimental feature using `image_transform` to overlay outfit concepts onto user photos. Results are approximations and noted as such.

### Automated Styling

Scheduled cron jobs for daily outfit recommendations (weather-aware), weekly wardrobe reports, and monthly seasonal checks.

## Stack Role Breakdown

- Hermes Agent: orchestration
- Telegram: user-facing interface
- GLM: reasoning and image understanding
- FAL: image generation (primary)
- OpenAI: image generation (fallback 1)
- Gemini: image generation (fallback 2) + image transformation
- Firecrawl: web search, weather, shopping links

## One-Sentence Summary

Stylish Hermes turns visual taste into actionable, transformed styling.
