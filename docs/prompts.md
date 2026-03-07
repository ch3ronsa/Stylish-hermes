# Master Prompts

## 1. Initial Profile Setup

```text
Use the ai-personal-stylist skill. Ask me only the minimum questions needed to build a short personal style profile. Then write a short summary suitable for Hermes memory. Do not store my full wardrobe in memory.
```

## 2. Wardrobe File Initialization

```text
Use the ai-personal-stylist skill. Check whether ~/.hermes/data/wardrobe.json exists. If it does not exist, create it with this schema:
{"tops":[],"bottoms":[],"outerwear":[],"shoes":[],"accessories":[],"outfit_history":[]}
Then tell me you are ready for wardrobe intake.
```

## 3. First Clothing Photo Analysis

```text
Use the ai-personal-stylist skill. Analyze this clothing photo. Extract the clothing type, main color, visible pattern, likely fabric, style category, season suitability, and visible condition. Then add it to ~/.hermes/data/wardrobe.json in the correct category and suggest 2 outfit ideas using existing pieces if possible.
```

## 4. What Should I Wear Today

```text
Use the ai-personal-stylist skill. Read my wardrobe from ~/.hermes/data/wardrobe.json. Check the current weather for my city. If my city or occasion is unclear, ask a short clarification question first. Then recommend 3 outfit options and explain which one is best.
```

## 5. Wardrobe Report

```text
Use the ai-personal-stylist skill. Analyze ~/.hermes/data/wardrobe.json and give me a short report with category counts, color distribution, style balance, season coverage, and missing basics.
```

## 6. Shopping Decision

```text
Use the ai-personal-stylist skill. Analyze this item from its image or description and compare it with my existing wardrobe. Score wardrobe compatibility, color compatibility, style compatibility, and versatility. End with a clear verdict: buy, maybe, or skip.
```

## 7. Style Transition

```text
Use the ai-personal-stylist skill. Read my current wardrobe and build a 30-day transition plan toward [target style]. Split the advice into keep, restyle, and buy-later. Prioritize practical changes first.
```
