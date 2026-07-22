import json
import re

# Load JP source (ja.json) and EN novel translation (en.json)
with open('dotabyss-translation-main/translations/novels/hmn_10440100001/ja.json', 'r', encoding='utf-8') as f:
    ja_data = json.load(f)

with open('dotabyss-translation-main/translations/novels/hmn_10440100001/en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Load EN asset lines
with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'r', encoding='utf-8-sig') as f:
    en_asset_lines = [line.rstrip('\n\r') for line in f]

TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
en_asset_texts = []  # (line_idx, cmd, speaker, text_field)
for i, line in enumerate(en_asset_lines):
    for cmd in TEXT_CMDS:
        if line.startswith(cmd):
            parts = line.split(',', 5)
            speaker = parts[1] if len(parts) > 1 else ''
            text_field = parts[2] if len(parts) > 2 else ''
            en_asset_texts.append((i, cmd, speaker, text_field))
            break

print(f"EN asset text records: {len(en_asset_texts)}")

# Build map from EN asset text -> VI translation
# First, create reverse lookup: EN novel text -> JP key
en_to_jp = {}
for jp_key, en_val in en_data.items():
    if en_val:  # Only non-empty EN translations
        # Normalize for matching: strip trailing <br> and whitespace
        norm_en = en_val.rstrip().rstrip('<br>').rstrip()
        en_to_jp[norm_en] = jp_key

print(f"EN novel entries with translations: {len(en_to_jp)}")

# Also check title in ja.json (which is identity map)
ja_title_keys = [k for k in ja_data.keys() if not k.startswith('<size')]
print(f"JA title-like keys: {len(ja_title_keys)}")

# Build VI translations keyed by EN asset text field (normalized)
VI_MAP = {}

# First, handle title - it's still JP in the asset
# Line 20: title,これから大雨が降りますから！,
title_line_idx = None
for i, line in enumerate(en_asset_lines):
    if line.startswith('title,'):
        title_line_idx = i
        parts = line.split(',', 5)
        jp_title = parts[1]
        print(f"Title JP: {jp_title}")
        if jp_title in ja_data:
            # We need to translate this JP title to VI
            pass
        break

# For each EN asset text record, find corresponding JP and translate
for idx, cmd, speaker, text_field in en_asset_texts:
    # Normalize EN asset text field for matching
    norm_text = text_field.rstrip().rstrip('<br>').rstrip()
    
    # Try to match with EN novel translation
    jp_key = None
    if norm_text in en_to_jp:
        jp_key = en_to_jp[norm_text]
    else:
        # Try fuzzy matching - the EN asset may have slight differences
        for en_novel, jp in en_to_jp.items():
            # Compare without tags and normalized whitespace
            en_clean = re.sub(r'<[^>]+>', '', en_novel).replace('，', ',').replace('\u201a', ',').strip()
            asset_clean = re.sub(r'<[^>]+>', '', norm_text).replace('，', ',').replace('\u201a', ',').strip()
            if en_clean == asset_clean:
                jp_key = jp
                break
    
    if jp_key:
        # Now translate JP to VI
        jp_text = jp_key
        # Build VI translation
        vi_text = translate_jp_to_vi(jp_text, cmd, speaker)
        VI_MAP[text_field] = vi_text
    else:
        print(f"NO MATCH Line {idx} ({cmd}): speaker={speaker} text={text_field[:80]}")

print(f"\nBuilt VI_MAP with {len(VI_MAP)} entries")

def translate_jp_to_vi(jp_text, cmd, speaker):
    """Translate Japanese text to Vietnamese based on context"""
    # This is a simplified version - in reality we'd use the full translation map
    # For now, return the text as-is to identify unmatched
    return f"[VI:{jp_text[:40]}]"

# Print first few mappings
for k, v in list(VI_MAP.items())[:5]:
    print(f"  EN: {k[:60]}")
    print(f"  VI: {v[:60]}")