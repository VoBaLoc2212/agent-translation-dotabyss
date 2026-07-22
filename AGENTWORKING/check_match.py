import json
import os

EN_ASSET = 'E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt'
EN_JSON = 'E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json'

with open(EN_JSON, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Build reverse map
en_to_jp = {}
for jp, en in en_data.items():
    if en and en.strip():
        en_to_jp[en.strip()] = jp

with open(EN_ASSET, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Check some message lines
for i, line in enumerate(lines[:50]):
    parts = line.split(',', 5)
    if len(parts) == 6 and parts[0] == 'message':
        text = parts[2].strip()
        norm = text.replace('<br> ', '').replace('<br>', '').strip()
        if norm in en_to_jp:
            print(f'MATCH line {i}: {text[:80]}')
        else:
            # Try to find close match
            found = False
            for en_key in en_to_jp:
                if en_key in norm or norm in en_key:
                    print(f'PARTIAL line {i}: {text[:80]}')
                    print(f'  -> EN key: {en_key[:80]}')
                    found = True
                    break
            if not found and text:
                print(f'NO MATCH line {i}: {text[:80]}')