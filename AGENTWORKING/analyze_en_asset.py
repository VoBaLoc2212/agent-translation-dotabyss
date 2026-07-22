import re

with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

text_cmds = {'title': 0, 'message': 0, 'messageTextUnder': 0, 'messageTextCenter': 0}
text_lines = []

for i, line in enumerate(lines, 1):
    line = line.rstrip('\n\r')
    for cmd in text_cmds:
        if line.startswith(cmd + ','):
            text_cmds[cmd] += 1
            text_lines.append((i, cmd, line))
            break

print('Text command counts:')
for cmd, count in text_cmds.items():
    print(f'  {cmd}: {count}')
print(f'Total: {sum(text_cmds.values())}')
print()
print('First few text lines:')
for line_no, cmd, line in text_lines[:10]:
    print(f'  Line {line_no}: {cmd}, {line[:120]}')
print()
print('Last few text lines:')
for line_no, cmd, line in text_lines[-10:]:
    print(f'  Line {line_no}: {cmd}, {line[:120]}')