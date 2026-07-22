import json

# Load EN JSON and build EN->JP reverse mapping
with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json", 'r', encoding='utf-8') as f:
    en_json = json.load(f)

with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json", 'r', encoding='utf-8') as f:
    ja_json = json.load(f)

# Build EN -> JP mapping - need to normalize whitespace and special chars
en_to_jp = {}
for jp_key, en_val in en_json.items():
    if en_val and en_val.strip():
        # Normalize: replace fullwidth comma with regular comma, normalize whitespace
        normalized = en_val.strip()
        normalized = normalized.replace('，', ',').replace('　', ' ')
        en_to_jp[normalized] = jp_key
        # Also add the original
        en_to_jp[en_val.strip()] = jp_key

# Check some asset lines against this mapping
with open("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt", 'r', encoding='utf-8-sig') as f:
    asset_lines = f.readlines()

found = 0
not_found = 0
for i, line in enumerate(asset_lines):
    if line.startswith('message,'):
        parts = line.strip().split(',', 5)
        if len(parts) >= 3:
            en_text = parts[2].strip()
            # Normalize
            norm_text = en_text.replace('，', ',').replace('　', ' ')
            if en_text in en_to_jp or norm_text in en_to_jp:
                found += 1
            elif en_text:
                not_found += 1
                if not_found <= 10:
                    print(f"NOT FOUND: {repr(en_text[:100])}")
                    # Show what keys are close
                    for k in list(en_to_jp.keys())[:5]:
                        if k.startswith(en_text[:10].replace('，', ',')):
                            print(f"  CLOSE KEY: {repr(k[:100])}")

print(f"Found: {found}, Not found: {not_found}")