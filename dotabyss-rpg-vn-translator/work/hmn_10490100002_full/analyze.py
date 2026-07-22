#!/usr/bin/env python3
"""Analyze hmn_10490100002 EN asset structure."""
import json, re

EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"
JA_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10490100002/ja.json"
EN_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10490100002/en.json"

with open(JA_JSON, encoding='utf-8') as f:
    ja = json.load(f)
with open(EN_JSON, encoding='utf-8') as f:
    en_map = json.load(f)

with open(EN_PATH, 'rb') as f:
    raw = f.read()

has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.split('\n')

print(f"BOM: {has_bom}")
print(f"CRLF: {has_crlf}")
print(f"Total lines: {len(lines)}")

text_commands = []
for i, ln in enumerate(lines, 1):
    stripped = ln.strip()
    if any(stripped.startswith(cmd) for cmd in ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')):
        # Extract command and text field
        cmd = stripped.split(',', 1)[0]
        text_field = stripped[len(cmd)+1:]  # everything after "cmd,"
        # For message, the format is: cmd,speaker,text,... 
        # For title: title,text
        if cmd == 'title':
            text_val = text_field  # everything after "title,"
        elif cmd in ('messageTextUnder', 'messageTextCenter'):
            # cmd,text,... 
            parts = text_field.split(',', 1)
            text_val = parts[1] if len(parts) > 1 else ''
        else:
            # message,NAME,TEXT,...
            # split on first 2 commas
            parts = stripped.split(',', 2)
            text_val = parts[2] if len(parts) > 2 else ''
        
        text_commands.append({
            'line': i,
            'cmd': cmd,
            'text': text_val
        })

print(f"\nText commands: {len(text_commands)}")
print(f"  title: {sum(1 for t in text_commands if t['cmd'] == 'title')}")
print(f"  message: {sum(1 for t in text_commands if t['cmd'] == 'message')}")
print(f"  messageTextUnder: {sum(1 for t in text_commands if t['cmd'] == 'messageTextUnder')}")
print(f"  messageTextCenter: {sum(1 for t in text_commands if t['cmd'] == 'messageTextCenter')}")

print("\n\n=== DETAILED TEXT RECORDS ===")
for t in text_commands:
    br_count = t['text'].count('<br>')
    has_comma = ',' in t['text']
    # Check if text is JP or EN
    is_jp = bool(re.search(r'[\u3000-\u9fff]', t['text']))
    marker = "JP" if is_jp else "EN"
    print(f"  [{t['line']:3d}] {t['cmd']:25s} | br={br_count} | {marker} | {repr(t['text'][:80])}")

# Show total text record count + ja.json entries count for comparison
print(f"\n\nja.json entries: {len(ja)}")
print(f"en.json entries: {len(en_map)}")

# Check which ja.json entries have en.json counterparts
en_has_value = sum(1 for v in en_map.values() if v and v.strip())
print(f"en.json entries with values: {en_has_value}")

# Check if ja.json is identity map
is_identity = all(k == v for k, v in ja.items())
print(f"ja.json is identity map: {is_identity}")
