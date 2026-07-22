import json

def translate_jp_to_vi(jp):
    """Translate Japanese text to Vietnamese"""
    # Placeholder - will be filled manually
    return f"[VI: {jp}]"

with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json', 'r', encoding='utf-8') as f:
    ja = json.load(f)

with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    content = f.read()

lines = content.splitlines(keepends=True)

text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
asset_texts = []

for i, line in enumerate(lines):
    for cmd in text_cmds:
        if line.startswith(cmd):
            raw = line.rstrip('\r\n')
            if cmd == 'title,':
                parts = raw.split(',', 2)
                text = parts[1] if len(parts) > 1 else ''
            else:
                parts = raw.split(',', 3)
                text = parts[2] if len(parts) > 2 else ''
            asset_texts.append({'line': i+1, 'cmd': cmd.rstrip(','), 'text': text})
            break

print(f"Total asset text records: {len(asset_texts)}")

# Build mapping: en.json value -> ja key
en_to_ja = {v: k for k, v in en.items() if v}

# Find matches
translations = {}
missing = []

for at in asset_texts:
    txt = at['text']
    found = False
    
    # Try exact match first
    if txt in en_to_ja:
        jp_key = en_to_ja[txt]
        translations[txt] = translate_jp_to_vi(jp_key)
        found = True
    else:
        # Try normalized match (strip <br> suffix)
        norm_txt = txt.strip().rstrip('<br>').strip()
        norm_txt = norm_txt.replace('，', ',').replace('…', '...')
        for en_val, jp_key in en_to_ja.items():
            norm_en = en_val.strip().rstrip('<br>').strip().replace('，', ',').replace('…', '...')
            if norm_txt == norm_en:
                translations[txt] = translate_jp_to_vi(jp_key)
                found = True
                break
    
    if not found:
        missing.append(at)

print(f"Mapped: {len(translations)}/{len(asset_texts)}")
print(f"Missing: {len(missing)}")
for m in missing:
    print(f"  MISSING line {m['line']}: {m['text'][:80]}...")

print("\n=== ALL MAPPINGS ===")
for at in asset_texts:
    txt = at['text']
    if txt in translations:
        print(f"'{txt}' -> '{translations[txt]}'")
    else:
        print(f"'{txt}' -> MISSING")