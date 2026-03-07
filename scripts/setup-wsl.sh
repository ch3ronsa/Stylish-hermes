#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

echo "[1/4] Creating Hermes directories"
mkdir -p ~/.hermes/skills/lifestyle/ai-personal-stylist
mkdir -p ~/.hermes/data

echo "[2/4] Copying skill"
cp "$(dirname "$0")/../skill/SKILL.md" ~/.hermes/skills/lifestyle/ai-personal-stylist/SKILL.md

echo "[3/4] Creating wardrobe file if missing"
if [ ! -f ~/.hermes/data/wardrobe.json ]; then
  cp "$(dirname "$0")/../data/wardrobe.json" ~/.hermes/data/wardrobe.json
fi

echo "[4/4] Next steps"
cat <<'EOF'
1. Run: hermes setup
2. Fill ~/.hermes/.env with:
   OPENROUTER_API_KEY=...
   FAL_KEY=...
   FIRECRAWL_API_KEY=...
   TELEGRAM_BOT_TOKEN=...
3. Run: hermes gateway setup
4. Test: /ai-personal-stylist
EOF
