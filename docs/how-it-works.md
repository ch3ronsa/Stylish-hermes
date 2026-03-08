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

The transformed concept can then be turned into a realistic generated fashion image using FAL.

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

## Stack Role Breakdown

- Hermes Agent: orchestration
- Telegram: user-facing interface
- GLM: reasoning and image understanding
- FAL: transformed outfit image generation

## One-Sentence Summary

Stylish Hermes turns visual taste into actionable, transformed styling.
