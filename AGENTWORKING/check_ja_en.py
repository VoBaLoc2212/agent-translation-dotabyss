import json
import re
from pathlib import Path

# Load ja.json (JP primary source)
with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json", "r", encoding="utf-8-sig") as f:
    ja_data = json.load(f)

# Load en.json (for cross-reference if needed)
with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json", "r", encoding="utf-8-sig") as f:
    en_data = json.load(f)

# Print all keys in order
print(f"ja.json entries: {len(ja_data)}")
print(f"en.json entries: {len(en_data)}")

for i, (k, v) in enumerate(ja_data.items()):
    print(f"{i+1}: JP='{k}' -> EN='{en_data.get(k, 'MISSING')}'")

print("\n\n---\nChecking EN asset text records match ja.json...")