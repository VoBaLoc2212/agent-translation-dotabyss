import json

with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json', 'r', encoding='utf-8') as f:
    ja = json.load(f)

with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

# Print all mappings
for k, v in ja.items():
    en_val = en.get(k, '')
    print(f'JA: {repr(k)}')
    print(f'EN: {repr(en_val)}')
    print('---')