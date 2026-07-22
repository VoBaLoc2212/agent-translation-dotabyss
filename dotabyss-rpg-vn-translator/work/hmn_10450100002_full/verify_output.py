"""Verify VI output for hmn_10450100002."""
en = open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt', 'rb').read()
vi = open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt', 'rb').read()

bom = b'\xef\xbb\xbf'
print(f'EN BOM: {en[:3] == bom}')
print(f'VI BOM: {vi[:3] == bom}')
print(f'EN ends: {en[-20:]}')
print(f'VI ends: {vi[-20:]}')

en_crlf = en.count(b'\r\n')
vi_crlf = vi.count(b'\r\n')
print(f'EN CRLF: {en_crlf}, VI CRLF: {vi_crlf}')

en_lines = en.split(b'\r\n')
vi_lines = vi.split(b'\r\n')
print(f'EN lines (CRLF split): {len(en_lines)}')
print(f'VI lines (CRLF split): {len(vi_lines)}')

# Spot check
en_text = en.decode('utf-8-sig').splitlines(True)
vi_text = vi.decode('utf-8-sig').splitlines(True)

# Check message line indices (0-indexed)
check_lines = [76, 78, 89, 91, 93, 166, 195]
for idx in check_lines:
    if idx < len(en_text):
        print(f'\nL{idx+1} EN: {en_text[idx].rstrip()[:90]}')
        print(f'L{idx+1} VI: {vi_text[idx].rstrip()[:90]}')

# BOM stripping check
en_no_bom = en[3:] if en[:3] == bom else en
vi_no_bom = vi[3:] if vi[:3] == bom else vi
print(f'\nEN size with BOM: {len(en)}, without: {len(en_no_bom)}')
print(f'VI size with BOM: {len(vi)}, without: {len(vi_no_bom)}')
print('DONE.')
