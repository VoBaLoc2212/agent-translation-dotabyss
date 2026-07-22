import json
import re

# Load ja.json with ordered pairs
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json', 'r', encoding='utf-8-sig') as f:
    ja_data = json.load(f, object_pairs_hook=list)

# Load en.json with ordered pairs
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json', 'r', encoding='utf-8-sig') as f:
    en_data = json.load(f, object_pairs_hook=list)

print("JA keys:", len(ja_data))
print("EN keys:", len(en_data))

# Extract JP texts in order
jp_texts = [v for k, v in ja_data]
print("JP texts:", len(jp_texts))

# First few
for i, (k, v) in enumerate(ja_data[:5]):
    print(f"  {i}: {k} = {v[:60]}...")

# Also extract EN texts
en_texts = [v for k, v in en_data]
print("EN texts:", len(en_texts))

# Print all JP texts with index
print("\n--- ALL JP TEXTS ---")
for i, (k, v) in enumerate(ja_data):
    print(f"{i}: {k} = {v}")