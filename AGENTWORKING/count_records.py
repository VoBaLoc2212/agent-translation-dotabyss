with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    content = f.read()

lines = content.splitlines(keepends=True)
text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
records = []
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
            records.append((i+1, cmd.rstrip(','), text))
            break

print(f'Total records: {len(records)}')
for r in records:
    print(f'  Line {r[0]}: {r[1]} | {repr(r[2][:80])}')