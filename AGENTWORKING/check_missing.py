import re

# Read the 80 records from the EN asset
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

print(f"Total asset records: {len(asset_texts)}")

# Load VI dictionary
with open('E:/AgentTranslation/build_vi_complete.py', 'r', encoding='utf-8') as f:
    vi_content = f.read()

# Extract VI dict
start = vi_content.find('VI = {')
brace_count = 0
end = start
for i, ch in enumerate(vi_content[start:], start):
    if ch == '{':
        brace_count += 1
    elif ch == '}':
        brace_count -= 1
        if brace_count == 0:
            end = i + 1
            break

vi_text = vi_content[start:end]
vi_keys = re.findall(r'"([^"]+)"\s*:', vi_text)
vi_dict = {}
for k in vi_keys:
    # Find the value
    pattern = f'"{re.escape(k)}"\\s*:\\s*"([^"]*)"'
    m = re.search(pattern, vi_text)
    if m:
        vi_dict[k] = m.group(1)

print(f"VI dict has {len(vi_dict)} entries")

# Check which asset texts are missing
missing = []
for at in asset_texts:
    if at['text'] not in vi_dict:
        missing.append(at)

print(f"\nMissing {len(missing)} translations:")
for m in missing:
    print(f"  Line {m['line']} ({m['cmd']}): {repr(m['text'][:80])}")