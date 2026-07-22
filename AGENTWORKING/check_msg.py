with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

msg_lines = [l for l in lines if l.startswith('message,')]
print(f'Total message lines: {len(msg_lines)}')

# Check unique text parts
texts = set()
for l in msg_lines:
    parts = l.strip().split(',', 5)
    if len(parts) >= 3:
        texts.add(parts[2].strip())
print(f'Unique message texts: {len(texts)}')