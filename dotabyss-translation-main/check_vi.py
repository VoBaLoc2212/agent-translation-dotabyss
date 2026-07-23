import json

ja_path = r'E:\AgentTranslation\dotabyss-translation-main\translations\novels\hmn_10010100001\ja.json'
vi_path = r'E:\AgentTranslation\dotabyss-translation-main\translations\novels\hmn_10010100001\vi.json'

with open(ja_path, 'r', encoding='utf-8') as f:
    ja = json.load(f)

with open(vi_path, 'r', encoding='utf-8') as f:
    vi = json.load(f)

ja_keys = set(ja.keys())
vi_keys = set(vi.keys())

print(f'JA keys: {len(ja_keys)}')
print(f'VI keys: {len(vi_keys)}')
print(f'Keys match: {ja_keys == vi_keys}')

if ja_keys != vi_keys:
    print(f'Missing in VI: {ja_keys - vi_keys}')
    print(f'Extra in VI: {vi_keys - ja_keys}')

# Check for standard commas in VI values
bad_commas = [(k, v) for k, v in vi.items() if ',' in v]
print(f'Values with standard commas: {len(bad_commas)}')
for k, v in bad_commas[:5]:
    print(f'  KEY: {k[:50]}...')
    print(f'  VAL: {v[:80]}...')

# Check %user% preserved
user_count = sum(1 for v in vi.values() if '%user%' in v)
lt_user_count = sum(1 for v in vi.values() if '<user>' in v)
print(f'Values with %user%: {user_count}')
print(f'Values with <user> (legacy): {lt_user_count}')

# Check Chỉ Huy used
chihuy_count = sum(1 for v in vi.values() if 'Chỉ Huy' in v)
print(f"Values with 'Chỉ Huy': {chihuy_count}")

# Check fullwidth commas
fw_comma_count = sum(1 for v in vi.values() if '，' in v)
print(f'Values with fullwidth comma: {fw_comma_count}')

# Check <br> preserved
br_count = sum(1 for v in vi.values() if '<br>' in v)
print(f'Values with <br>: {br_count}')

print('OK')