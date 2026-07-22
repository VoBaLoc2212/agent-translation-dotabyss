import json
with open('dotabyss-translation-main/translations/novels/hmn_10440100001/ja.json', 'r', encoding='utf-8') as f:
    ja = json.load(f)
print('JA keys:', len(ja))
for i, k in enumerate(ja.keys()):
    print(f'  {i}: {k[:80]}')