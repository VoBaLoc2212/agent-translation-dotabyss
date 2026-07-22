import json
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)
print('EN keys count:', len(en_data))
for k, v in list(en_data.items())[:5]:
    print(f'JP: {repr(k[:50])}')
    print(f'EN: {repr(v[:50])}')
    print()