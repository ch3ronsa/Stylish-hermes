"""
Setup Cron Jobs for AI Personal Stylist
========================================
Registers daily, weekly, and monthly automated styling tasks
with Hermes Agent's cron system.

Usage:
    python scripts/setup-cron-jobs.py [--city CITY]

Default city: Istanbul
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


CRON_JOBS = [
    {
        "name": "daily-outfit-recommendation",
        "schedule": "0 7 * * *",
        "description": "Daily outfit recommendation based on weather",
        "prompt": (
            "You are AI Personal Stylist. "
            "Read ~/.hermes/data/wardrobe.json. "
            "Use web_search to check today's weather for {city}. "
            "Read the user's short style summary from memory. "
            "Recommend one practical outfit for today. "
            "Keep the message concise and friendly. "
            "If image generation is available, generate a quick outfit visual."
        ),
    },
    {
        "name": "weekly-wardrobe-report",
        "schedule": "0 10 * * 0",
        "description": "Weekly wardrobe analysis report (Sundays 10 AM)",
        "prompt": (
            "You are AI Personal Stylist. "
            "Read ~/.hermes/data/wardrobe.json. "
            "Summarize wardrobe counts, color distribution, style balance, "
            "season coverage, and obvious missing basics. "
            "Keep the report short and useful."
        ),
    },
    {
        "name": "seasonal-wardrobe-check",
        "schedule": "0 9 1 * *",
        "description": "Monthly seasonal wardrobe check (1st of each month)",
        "prompt": (
            "You are AI Personal Stylist. "
            "Read ~/.hermes/data/wardrobe.json. "
            "Check whether the season is changing soon and recommend "
            "which wardrobe pieces should become more visible or which "
            "missing pieces should be added. "
            "Use web_search to check upcoming weather trends for {city}."
        ),
    },
]


def setup_cron_jobs(city: str = "Istanbul") -> None:
    """Print cron job configurations for manual setup."""
    print(f"AI Personal Stylist - Cron Job Setup (City: {city})")
    print("=" * 60)
    print()
    print("Add these to your Hermes cron configuration:")
    print()

    for job in CRON_JOBS:
        prompt = job["prompt"].format(city=city)
        print(f"## {job['description']}")
        print(f"Name: {job['name']}")
        print(f"Schedule: {job['schedule']}")
        print(f"Prompt: {prompt}")
        print()

    print("=" * 60)
    print()
    print("To add via Hermes CLI:")
    print()
    for job in CRON_JOBS:
        prompt = job["prompt"].format(city=city)
        safe_prompt = prompt.replace('"', '\\"')
        print(f'hermes cron add --name "{job["name"]}" \\')
        print(f'  --schedule "{job["schedule"]}" \\')
        print(f'  --deliver telegram \\')
        print(f'  --prompt "{safe_prompt}"')
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Setup AI Stylist cron jobs")
    parser.add_argument("--city", default="Istanbul", help="City for weather (default: Istanbul)")
    args = parser.parse_args()
    setup_cron_jobs(args.city)


if __name__ == "__main__":
    main()
