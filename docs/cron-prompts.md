# Cron Prompts

## Daily Outfit Recommendation

```python
schedule_cronjob(
    prompt="You are AI Personal Stylist. Read ~/.hermes/data/wardrobe.json. Use web_search to check today's weather for Istanbul. Read the user's short style summary from memory. Recommend one practical outfit for today. Keep the message concise and friendly.",
    schedule="0 7 * * *",
    name="daily-outfit-recommendation",
    deliver="telegram"
)
```

## Weekly Wardrobe Report

```python
schedule_cronjob(
    prompt="You are AI Personal Stylist. Read ~/.hermes/data/wardrobe.json. Summarize wardrobe counts, color distribution, style balance, season coverage, and obvious missing basics. Keep the report short and useful.",
    schedule="0 10 * * 0",
    name="weekly-wardrobe-report",
    deliver="telegram"
)
```

## Seasonal Check

```python
schedule_cronjob(
    prompt="You are AI Personal Stylist. Read ~/.hermes/data/wardrobe.json. Check whether the season is changing soon and recommend which wardrobe pieces should become more visible or which missing pieces should be added.",
    schedule="0 9 1 * *",
    name="seasonal-wardrobe-check",
    deliver="telegram"
)
```
