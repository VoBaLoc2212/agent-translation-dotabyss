import json

# Read ja.json (JP source)
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json', 'r', encoding='utf-8') as f:
    ja_novel = json.load(f)

# Read en.json (EN translation of JP)
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json', 'r', encoding='utf-8') as f:
    en_novel = json.load(f)

# Read EN asset text records
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    en_asset_lines = f.readlines()

text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

asset_texts = []
for i, line in enumerate(en_asset_lines):
    line = line.rstrip('\r\n')
    for cmd in text_cmds:
        if line.startswith(cmd):
            if cmd == 'title,':
                parts = line.split(',', 1)
                if len(parts) >= 2:
                    asset_texts.append((i+1, cmd, parts[1]))
            else:
                parts = line.split(',', 5)
                if len(parts) >= 3:
                    asset_texts.append((i+1, cmd, parts[2]))
            break

# Build reverse mapping: EN text (normalized) -> JP key
def norm(s):
    s = s.replace('，', ',').replace('、', ',')
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', '', s)
    return s

import re
en_to_jp = {}
for jp_key, en_val in en_novel.items():
    if en_val:
        en_to_jp[norm(en_val)] = jp_key

# Match each asset text to JP
print(f'EN novel entries with EN text: {len([v for v in en_novel.values() if v])}')
print(f'EN asset text records: {len(asset_texts)}')

matched = 0
unmatched = []
for line_num, cmd, asset_text in asset_texts:
    n = norm(asset_text)
    if n in en_to_jp:
        jp_key = en_to_jp[n]
        print(f'Line {line_num} ({cmd}): MATCHED -> JP: {jp_key[:50]}')
        matched += 1
    else:
        # Try partial match
        best = None
        for en_norm, jp_key in en_to_jp.items():
            if n in en_norm or en_norm in n:
                best = (jp_key, en_norm)
                break
        if best:
            print(f'Line {line_num} ({cmd}): PARTIAL -> JP: {best[0][:50]}')
            matched += 1
        else:
            print(f'Line {line_num} ({cmd}): UNMATCHED -> {asset_text[:80]}')
            unmatched.append((line_num, cmd, asset_text))

print(f'\nMatched: {matched}/{len(asset_texts)}')
print(f'Unmatched: {len(unmatched)}')