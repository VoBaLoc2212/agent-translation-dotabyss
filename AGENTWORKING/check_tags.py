import re
TAG_RE = re.compile(r'<[^>]+>')

mismatch_lines = [33, 84, 86, 97, 108, 162, 173, 192, 205, 227, 316, 331, 360, 398, 411]

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    vi_lines = f.readlines()

for line_no in mismatch_lines:
    if line_no <= len(en_lines):
        en_line = en_lines[line_no-1].rstrip('\r\n')
        vi_line = vi_lines[line_no-1].rstrip('\r\n')
        if en_line.startswith(('message,', 'messageTextCenter,', 'title,')):
            en_tags = TAG_RE.findall(en_line)
            vi_tags = TAG_RE.findall(vi_line)
            print(f'Line {line_no}:')
            print(f'  EN tags: {en_tags}')
            print(f'  VI tags: {vi_tags}')
            if en_line.startswith('title,'):
                en_text = en_line.split(',', 1)[1] if ',' in en_line else ''
                vi_text = vi_line.split(',', 1)[1] if ',' in vi_line else ''
            else:
                parts = en_line.split(',', 5)
                en_text = parts[2] if len(parts) >= 3 else ''
                parts_vi = vi_line.split(',', 5)
                vi_text = parts_vi[2] if len(parts_vi) >= 3 else ''
            print(f'  EN text: {repr(en_text)}')
            print(f'  VI text: {repr(vi_text)}')
            print()