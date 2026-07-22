import json

# Load EN JSON and build EN->JP reverse mapping
with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json", 'r', encoding='utf-8') as f:
    en_json = json.load(f)

with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json", 'r', encoding='utf-8') as f:
    ja_json = json.load(f)

# Build EN -> JP mapping
en_to_jp = {}
for jp_key, en_val in en_json.items():
    if en_val and en_val.strip():
        en_to_jp[en_val.strip()] = jp_key

# Check some asset lines against this mapping
with open("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt", 'r', encoding='utf-8-sig') as f:
    asset_lines = f.readlines()

# Find message lines and check
found = 0
not_found = 0
for i, line in enumerate(asset_lines):
    if line.startswith('message,'):
        parts = line.strip().split(',', 5)
        if len(parts) >= 6:
            text_part = parts[5] if len(parts) > 5 else parts[2]
            # The text is in parts[2] for message lines
            if len(parts) > 2:
                en_text = parts[2].strip()
                if en_text and en_text in en_to_jp:
                    found += 1
                elif en_text:
                    not_found += 1
                    if not_found <= 10:
                        print(f"NOT FOUND: {repr(en_text[:100])}")

print(f"Found: {found}, Not found: {not_found}")

# Let's also check what the message lines look like in the asset
msg_lines = [l for l in asset_lines if l.startswith('message,')]
print(f"\nTotal message lines: {len(msg_lines)}")
for i, ml in enumerate(msg_lines[:5]):
    parts = ml.strip().split(',', 5)
    print(f"Line {i}: parts={len(parts)}")
    for j, p in enumerate(parts):
        print(f"  [{j}] {repr(p[:80])}")
    print()