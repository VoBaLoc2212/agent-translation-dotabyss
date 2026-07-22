import json

with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json", 'r', encoding='utf-8') as f:
    en_json = json.load(f)

test_keys = ["ん？　……なんだ、司令官さんか。", "そんなことですかい。<br>それより今月分の給料、ちと少なくないですかね？"]
for k in test_keys:
    v = en_json.get(k)
    if v:
        print(f"JP: {repr(k)}")
        print(f"EN: {repr(v)}")
        print()