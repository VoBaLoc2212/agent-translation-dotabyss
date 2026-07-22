with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Check field counts for message lines
for i, line in enumerate(lines):
    if line.startswith('message,'):
        parts = line.split(',')
        if len(parts) != 6:
            print(f'Line {i}: {len(parts)} fields: {line[:100]}')