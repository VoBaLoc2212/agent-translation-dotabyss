with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Check first 100 lines for issues
for i, line in enumerate(lines[:100]):
    if line.startswith('message,'):
        parts = line.split(',')
        print(f'Line {i}: {len(parts)} fields: {line[:120]}')