# Stylish Hermes — Live Demo (90 seconds)

## Setup Before Demo
- Have 2-3 good fashion images ready (Pinterest editorial, street style, runway)
- Bot running in Telegram
- Phone screen mirrored to projector

---

## THE SHOW

### [0:00 - 0:10] HOOK

**Say:** "Everyone saves fashion inspiration. No one knows how to wear it. This bot fixes that."

**Action:** Open Telegram, type `/start`

**Show:** Bot greets with personality + inline buttons appear

---

### [0:10 - 0:30] INSPIRATION ANALYSIS

**Say:** "Send any image — Pinterest, anime, runway, anything."

**Action:** Send a strong editorial/runway image (no text, just the image)

**Show:** Bot automatically analyzes:
- Style aesthetic
- Color palette
- Silhouette breakdown
- 3 wearability levels (easier / wearable / bolder)

**Key moment:** Bot talks like a stylish friend, not a robot.

---

### [0:30 - 0:55] VISUAL TRANSFORM — THE MONEY SHOT

**Say:** "Now watch this. I'll ask it to make this wearable for me."

**Action:** Type: `Turn this into a casual spring outfit for Istanbul`

**Show:** Bot generates a brand new outfit image inspired by the reference.

**Say:** "It didn't copy the outfit. It translated the *vibe* into something I can actually wear tomorrow."

**Key moment:** Side-by-side comparison — original vs. transformed.

---

### [0:55 - 1:10] CELEBRITY MATCH

**Say:** "Let's have some fun."

**Action:** Type: `Who dresses like this?`

**Show:** Bot returns top 3 celebrity matches with percentages and reasoning.

**Say:** "Shareable, fun, drives engagement."

---

### [1:10 - 1:25] STYLE DNA

**Say:** "After a few images, the bot builds your style identity."

**Action:** Type: `What's my Style DNA?`

**Show:** Style DNA card with categories, signature colors, power piece, celebrity twin + generated mood image.

---

### [1:25 - 1:30] CLOSE

**Say:** "Vision in, outfit out. No app to download. No fashion vocabulary needed. Just Telegram."

---

## IF SOMETHING FAILS

- **Image generation down?** → "The bot has 3 fallback providers — FAL, OpenAI, Gemini. Even if all fail, it gives you a detailed text outfit so you're never stuck."
- **Slow response?** → "It's running vision analysis + image generation — two AI models back to back. That's the pipeline working, not lag."

## BACKUP: JUDGE Q&A

| Question | Answer |
|----------|--------|
| "How is this different from ChatGPT?" | "ChatGPT describes outfits. We generate them. And we use the reference image as actual input to the generation — it's not text-to-image, it's image-to-image translation." |
| "What's the tech?" | "Hermes Agent for orchestration, GLM-4 for vision, Gemini for image transform, triple fallback chain for reliability." |
| "Can it scale?" | "It's a Telegram bot — zero friction deployment. The pipeline is stateless per-session. Each user gets their own context." |
| "What's the business model?" | "Premium features: unlimited transforms, saved style profiles, brand partnerships for shopping recs." |

## KEY PHRASES
- **"Inspiration to execution"**
- **"Transformation, not recreation"**
- **"No fashion vocabulary needed"**
- **"Lives where users already are"**
