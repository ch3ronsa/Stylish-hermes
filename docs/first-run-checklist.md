# First Run Checklist

## Before You Start

- WSL2 is installed
- Hermes is installed
- API keys are present in `~/.hermes/.env`
- `SKILL.md` exists at `~/.hermes/skills/lifestyle/ai-personal-stylist/SKILL.md`
- `wardrobe.json` exists at `~/.hermes/data/wardrobe.json`

## First Manual Test Flow

### Test 1: Profile Setup

```text
Use the ai-personal-stylist skill. Ask me only the minimum questions needed to build a short personal style profile. Then write a short summary suitable for Hermes memory. Do not store my full wardrobe in memory.
```

### Test 2: Wardrobe Intake

```text
Use the ai-personal-stylist skill. Analyze this clothing photo. Extract the clothing type, main color, visible pattern, likely fabric, style category, season suitability, and visible condition. Then add it to ~/.hermes/data/wardrobe.json in the correct category and suggest 2 outfit ideas using existing pieces if possible.
```

### Test 3: Outfit Recommendation

```text
Use the ai-personal-stylist skill. Read my wardrobe from ~/.hermes/data/wardrobe.json. Check the current weather for my city. If my city or occasion is unclear, ask a short clarification question first. Then recommend 3 outfit options and explain which one is best.
```

### Test 4: Wardrobe Report

```text
Use the ai-personal-stylist skill. Analyze ~/.hermes/data/wardrobe.json and give me a short report with category counts, color distribution, style balance, season coverage, and missing basics.
```
