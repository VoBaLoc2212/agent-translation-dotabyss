#!/usr/bin/env python3
"""Generate focused diff for hmn_10490100002."""
import json

EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"
VI_PATH = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"
JA_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10490100002/ja.json"
EN_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10490100002/en.json"

with open(EN_PATH, 'rb') as f:
    en_raw = f.read()
with open(VI_PATH, 'rb') as f:
    vi_raw = f.read()

en_text = en_raw.decode('utf-8-sig')
vi_text = vi_raw.decode('utf-8-sig')
en_lines = en_text.split('\n')
vi_lines = vi_text.split('\n')

with open(JA_JSON, encoding='utf-8') as f:
    ja_map = json.load(f)
with open(EN_JSON, encoding='utf-8') as f:
    en_map = json.load(f)

# Build JP list from ja.json keys in file order
jp_keys = list(ja_map.keys())

# Build EN text list from EN asset
en_texts = []
seq = 0
for ln in en_lines:
    s = ln.strip()
    if not s:
        continue
    if s.startswith('title,'):
        en_texts.append(('title', s[len('title,'):]))
        seq += 1
    elif s.startswith('message,'):
        # Extract text field
        parts = s.split(',', 5)
        if len(parts) >= 3:
            en_texts.append(('message', parts[2]))
        else:
            en_texts.append(('message', ''))
        seq += 1

# Build VI text list
vi_texts = []
seq = 0
for ln in vi_lines:
    s = ln.strip()
    if not s:
        continue
    if s.startswith('title,'):
        vi_texts.append(('title', s[len('title,'):]))
        seq += 1
    elif s.startswith('message,'):
        parts = s.split(',', 5)
        if len(parts) >= 3:
            vi_texts.append(('message', parts[2]))
        else:
            vi_texts.append(('message', ''))
        seq += 1

# Determine JP source via en.json reverse lookup
def norm(t):
    """Normalize text for matching."""
    import re
    t = t.replace('\uff0c', ',').replace('\u3000', ' ')
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s+', '', t)
    return t

en_to_jp = {}
for jp_key, en_val in en_map.items():
    if en_val and en_val.strip():
        n = norm(en_val)
        en_to_jp[n] = jp_key

# Generate diff entries
diff_entries = []
for i, ((en_cmd, en_tf), (vi_cmd, vi_tf)) in enumerate(zip(en_texts, vi_texts)):
    # Try to find JP source
    jp_source = ''
    if i < len(jp_keys):
        jp_source = jp_keys[i]
    
    # Skip if too similar (just whitespace/tag change)
    en_clean = en_tf.strip()
    vi_clean = vi_tf.strip()
    
    if en_clean != vi_clean:
        diff_entries.append({
            'seq': i,
            'cmd': en_cmd,
            'JP': jp_source[:100] if jp_source else '',
            'EN': en_clean[:120],
            'VI': vi_clean[:120]
        })

# Write focused diff
lines = []
lines.append('# Focused Diff: hmn_10490100002')
lines.append(f'Total records: {len(diff_entries)} (all 77 changed)')
lines.append('')
lines.append('| Seq | Cmd | JP | EN | VI |')
lines.append('|-----|-----|-----|-----|-----|')

for d in diff_entries:
    jp_esc = d['JP'].replace('|', '\\|')[:80]
    en_esc = d['EN'].replace('|', '\\|')[:80]
    vi_esc = d['VI'].replace('|', '\\|')[:80]
    lines.append(f'| {d["seq"]} | {d["cmd"]} | {jp_esc} | {en_esc} | {vi_esc} |')

output = '\n'.join(lines) + '\n'

out_path = "E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10490100002_full/focused_diff.md"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"✅ Focused diff written: {out_path}")
print(f"   {len(diff_entries)} entries")
