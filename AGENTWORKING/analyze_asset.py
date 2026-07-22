import re

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    content = f.read()

lines = content.splitlines(keepends=True)

text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
records = []
for i, line in enumerate(lines):
    for cmd in text_cmds:
        if line.startswith(cmd):
            if cmd == 'title,':
                parts = line.split(',', 2)
                text = parts[1] if len(parts) > 1 else ''
            else:
                parts = line.split(',', 3)
                text = parts[2] if len(parts) > 2 else ''
            records.append({
                'line_idx': i,
                'cmd': cmd.rstrip(','),
                'raw_line': line,
                'text': text,
                'speaker': parts[1] if cmd != 'title,' and len(parts) > 1 else ''
            })
            break

print(f'Total text records: {len(records)}')
for r in records:
    print(f"  Line {r['line_idx']+1}: {r['cmd']} | speaker={r['speaker']!r} | text={r['text'][:80]}...")