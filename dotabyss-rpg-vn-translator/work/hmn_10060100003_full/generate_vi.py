#!/usr/bin/env python
from __future__ import annotations
import hashlib, json, re, difflib
from pathlib import Path
from collections import Counter

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10060100003'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
TEXT_CMDS = {'title':1, 'message':2, 'messageTextUnder':2, 'messageTextCenter':2}
TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r"%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_asset(path: Path):
    data = path.read_bytes()
    return data, data.decode('utf-8-sig'), data.startswith(b'\xef\xbb\xbf')

def text_field(parts):
    return parts[TEXT_CMDS.get(parts[0], -999)]

# Plain VI strings aligned to asset text-command order. Do not include ASCII comma inside these strings.
VI = [
    'Một Ly Thì Chắc Là Không Sao',
    '<size=48>――Vài Ngày Sau</size>',
    'Còn nữa… thuốc cũng vơi đi một chút rồi nên mình phải nhờ bổ sung thêm.',
    'Phù‚ hôm nay ít người bị thương nên việc dọn dẹp cũng thuận lợi thật đấy~.',
    'Một giọng nói vang lên từ phía sau Noemi khi cô đang dọn dẹp một mình trong phòng điều trị.',
    'Dĩ nhiên là chẳng ai đến rồi. Bây giờ ở quán rượu đang giữa lúc tiệc mừng mà.',
    'A… Chỉ Huy.',
    'Tiệc mừng vì trận chiến đã tạm khép lại. Chắc mọi người không có tâm trí đến đây chữa trị đâu.',
    'Đ-đúng vậy! Đang lúc mọi người ăn mừng mà Chỉ Huy không tham gia thì có ổn không ạ~?',
    'Anh đã ghé qua rồi. Nhưng anh thấy hơi tiếc khi thiếu mất một trong những nhân vật chính.',
    'Nhân vật chính… là sao ạ…?',
    'Người đã lập công trong trận vừa rồi là Noemi mà. Mọi người đều đang chờ em đấy.',
    'N-nhưng chắc em sẽ làm hỏng bầu không khí mất. Em thì… chuyện rượu hơi…',
    'Vậy sao? Anh thấy em nói chuyện với Ludia nên cứ tưởng em hay đến quán rượu.',
    'A-anh thấy rồi ạ!? C-c-cái đó là…!',
    'Đúng là em thỉnh thoảng có đến quán rượu nhưng tuyệt đối không thường xuyên đâu‚ ừm…!',
    'Không sao đâu‚ đừng bận tâm. Không uống được rượu cũng chẳng có gì xấu cả.',
    'Chỉ Huy…',
    'Vậy thì anh sẽ uống ở đây.',
    'Ơơ!? Chỉ Huy hãy đến quán rượu đi ạ! Mọi người sẽ buồn lắm đó~!',
    'Không sao mà. Có anh là Chỉ Huy và Noemi là nhân vật chính ở đây thì nơi này chính là tiệc mừng rồi‚ đúng không?',
    'Chỉ Huy… cảm ơn anh rất nhiều.',
    'Thậm chí anh còn lời vì được giữ Noemi cho riêng mình ấy chứ. Bọn họ sẽ ghen tị lắm.',
    'Thôi mà~ không có chuyện đó đâu ạ~.',
    'Chỉ là… ừm… không phải em hoàn toàn không uống được rượu đâu…',
    'A‚ cô Noemi! Cả Chỉ Huy nữa! Hai người ở đây sao!',
    'Mọi người đang chờ đấy! Nào‚ ra quán rượu thôi!',
    'Mọi người!? Còn đến tận đây nữa…',
    'Ôi chà‚ tiệc riêng hiếm có bị phát hiện mất rồi. …Nào‚ em tính sao?',
    'Fufufu‚ vậy thì hết cách rồi. Đi cùng nhau nhé‚ Chỉ Huy.',
    'Mọi người ơi! Nhân vật chính xuất hiện rồi đây!',
    'Uoooo! Cô Noemi!',
    'Nữ thần của bọn tôi! Cuối cùng cô cũng đến rồi!',
    'Em đâu có làm gì đáng để được chào đón như vậy đâu ạ~!?',
    'Nhân vật chính mà nói gì vậy chứ! Nào nào‚ trước hết một ly đã!',
    'Bên này cũng có đây! Nào uống đi‚ Noemi!',
    'Khoan khoan‚ cái đó không được. Noemi với rượu thì…!',
    'Không sao đâu ạ. Em sẽ uống đàng hoàng mà.',
    'Ổn thật chứ? Em không cần phải cố chịu đâu.',
    'M-một ly thì chắc là không sao đâu ạ. Chắc em sẽ ổn mà…',
    'Em có vẻ quyết tâm kỳ lạ quá… Anh hơi có linh cảm chẳng lành.',
    'Em đã nói ổn là ổn mà! Em xin phép uống ạ!',
    'Noemi cầm lấy chiếc ly đã rót rượu rồi chậm rãi nhưng không hề dừng lại mà uống cạn.',
    'Ưm… hà… Cảm ơn vì ly rượu ạ~.',
    'N-này này này! Em uống hết thật à!? Đừng cố quá đấy!',
    'Không không‚ từng này thì em vẫn ổn. Vậy nên… thêm một ly… chỉ một ly nữa thôi…',
    'Noemi cầm ly tiếp theo lên và uống cạn còn nhanh hơn ly đầu tiên.',
    'Ực‚ ực… Haaa… tuyệt thật đấy…',
    'Đã hai ly rồi đấy? Mặt em cũng đỏ lên rồi‚ tốt hơn nên dừng ở đây thì…',
    'Em ổn mà~! Thêm chút nữa thôi‚ chỉ thêm một chút nữa…',
    'A‚ này!',
    'Noemi cầm lấy chiếc ly đặt trước mặt Chỉ Huy rồi ngửa cổ tu một hơi đầy khí thế.',
    'Ực ực ực… ưm~ ngon quá! Rượu mừng đúng là tuyệt nhất~!',
    'Này‚ cô Noemi uống nhiều quá rồi thì phải…?',
    'Có khi tửu lượng cô ấy mạnh ngoài dự đoán. Nhưng mà khí thế hơi…',
    'Thêm rượu‚ một ly nữa~! Không‚ dù sao em cũng uống hết thôi nên mang khoảng ba ly đến đây đi ạ~!',
    'Nhanh lên! Nha~nh lê~n nào!!!',
    'V-vẫn uống tiếp sao!? Cô ổn chứ‚ cô Noemi!?',
    'Em ổn mà! Đang tiệc mừng thì phải uống nhiều hơn nữa chứ!',
    'Dù vậy thì hơi…!',
    'Nào! Thêm nữa! Thêm nữa đi! Mang thêm rượu đến đây cho em với!!!',
    'Noemi vỗ bồm bộp lên bàn và bật cười vui vẻ. Nhìn thế nào đi nữa thì cô cũng chỉ là một con sâu rượu phiền phức.',
    'Chuyện này là sao vậy!?',
    'À‚ lại bắt đầu rồi nhỉ…',
    'Không lẽ Ludia‚ chuyện này xảy ra thường xuyên à?',
    'Ừ. Thật ra cô bé ấy là kiểu say vào sẽ quậy tưng bừng. Ban đầu thì ngại nên không uống nhưng một khi đã bắt đầu thì không dừng lại được đâu.',
    '…Ra là vậy. Cô ấy từ chối đến tiệc không phải vì không uống được mà vì hễ uống vào sẽ thành ra thế này.',
    'Lần nào tiền rượu cũng bị ghi nợ ấy mà. Ban ngày tôi phải lén đi thu lại đó.',
    'Hóa ra khi ấy hai người nói chuyện này. Bảo sao không thể nói to được.',
    'Dù vậy hôm nay cô ấy say khá nặng nhỉ. Không biết có phải đã dồn nén nhiều căng thẳng lắm không.',
    '…Vừa hay. Hãy để cô ấy nói hết ra ở đây đi.',
    'Noemi bị những người đàn ông vây quanh liền bật dậy và giơ cao ly rượu.',
    'Nghe đây chưa ạ‚ mọi người! Em ấy mà~! Đã chịu hết nổi rồi!',
    'Ồồ!?',
    'Sao vậy Noemi‚ nếu có chuyện gì làm cô khổ sở thì bọn tôi sẽ giúp!',
    'Điều làm em khổ sở là! Mọi người! Dù vẫn khỏe re! Lại cứ đến chữa trị đó ạ!',
    'Ặc… bị phát hiện rồi…! Chuyện là… tôi chỉ muốn được cô Noemi chữa trị bằng mọi giá nên…',
    'Xin lỗi vì đã khiến cô bận rộn quá…',
    'Em bận thì không sao hết ạ! Em lo cho mọi người cơ!',
    '…Cô lo cho bọn tôi?',
    'Nếu lúc nào cũng nói dối là bị thương rồi~ thì đến khi bị thương thật nặng sẽ không ai tin đâu!',
    'Rồi nếu bị xếp sau thì có thể chết mất đó! Em lo chuyện đó lắm đấy ạ!',
    'Bận rộn như vậy mà cô ấy vẫn nghĩ cho bọn mình chứ không phải cho bản thân…!?',
    'Nghe rõ chưa‚ các bé ngoan! Không được nói dối! Nào‚ nhắc lại!',
    'K-không được nói dối!',
    'Tốt lắm! Mọi người đều là bé ngoan hết đó ạ!',
    'Em cũng sẽ cố gắng hơn nữa với tư cách healer nên mọi người cũng cùng cố gắng nhé~!',
    'Cô Noemi…',
    '…Lũ say xỉn các cậu. Có nghe Noemi nói không?',
    'A‚ Chỉ Huy…!',
    'Người ta nói khi say sẽ lộ lòng thật nên đây hẳn là cảm xúc thật của Noemi. Giờ sao đây‚ từ nay các cậu vẫn định gây phiền cho Noemi à?',
    'Không… tôi sẽ chỉ dựa vào cô Noemi khi đã chiến đấu hết sức và bị thương thật thôi…',
    'Không thể gây phiền cho cô gái tốt bụng như vậy được. Hehe… cô ấy nói lo cho bọn mình kìa…',
    'Những người đàn ông vừa tự kiểm điểm vừa mỉm cười rồi thỏa mãn nghiêng ly uống.',
    'Vậy là có vẻ ổn rồi. Quả nhiên không ai thắng nổi sự dịu dàng của Noemi nhỉ.',
    'Chỉ Huy~!',
    'Uwaa!?',
    'Noemi ôm chặt lấy cánh tay Chỉ Huy. Cô cứ thế tựa vào vai anh rồi nói bằng giọng nũng nịu.',
    'Ehe~… Chỉ Huy‚ cảm ơn anh vì mọi chuyện~.',
    '…Người phải cảm ơn là anh mới đúng. Noemi‚ em say rồi đấy.',
    'Em hông say đâu~. Em thích anh lắm‚ Chỉ Huy~.',
    'Thiệt là. Câu đó hãy để lúc không say rồi nói lại cho anh nghe.',
    'Chuyện đó thì… em muốn anh chờ thêm chút nữa thôi… ehe~.',
    '…Ừ‚ anh mong chờ đấy.',
]

def split_for_br(text: str) -> str:
    """Insert one UI <br> near the middle for source fields with two <br> tags."""
    target = max(12, len(text) // 2)
    candidates = [m.start() for m in re.finditer(r'[.!?…。！？] ', text)]
    candidates += [m.start() for m in re.finditer(r' ', text)]
    if not candidates:
        return text
    pos = min(candidates, key=lambda p: abs(p - target))
    # If split at punctuation+space, keep punctuation before the break and drop the following space.
    if pos + 1 < len(text) and text[pos] in '.!?…。！？' and text[pos+1] == ' ':
        return text[:pos+1] + '<br>' + text[pos+2:]
    return text[:pos] + '<br>' + text[pos+1:]

def main():
    data, src_text, src_bom = read_asset(EN_ASSET)
    lines = src_text.splitlines(True)
    newline = '\r\n' if b'\r\n' in data else '\n'
    candidates = []
    for i, raw in enumerate(lines):
        s = raw.rstrip('\r\n')
        parts = s.split(',')
        if parts and parts[0] in TEXT_CMDS:
            idx = TEXT_CMDS[parts[0]]
            candidates.append((i, parts, idx))
    if len(candidates) != len(VI):
        raise SystemExit(f'VI count mismatch: {len(VI)} != {len(candidates)}')

    ja_pairs = json.loads(JA_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)
    en_pairs = json.loads(EN_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)

    out_lines = list(lines)
    entries = []
    blockers = []
    for n, ((i, parts, idx), vi) in enumerate(zip(candidates, VI), 1):
        original_text = parts[idx]
        # For ordinary asset text fields all text tags are <br>. Preserve exact source <br> count by appending UI breaks.
        if parts[0] != 'messageTextCenter':
            br_count = original_text.count('<br>')
            if '<' in vi or '>' in vi:
                blockers.append({'line': i+1, 'issue': 'unexpected_tag_in_vi_plain', 'text': vi})
            if br_count == 0:
                vi_field = vi
            elif br_count == 1:
                vi_field = vi + '<br> '
            else:
                vi_field = split_for_br(vi) + ''.join('<br>' for _ in range(br_count-2)) + '<br> '
        else:
            vi_field = vi
        if ',' in vi_field:
            blockers.append({'line': i+1, 'issue': 'ASCII_COMMA_IN_VI_FIELD', 'text': vi_field})
        new_parts = list(parts)
        new_parts[idx] = vi_field
        new_line = ','.join(new_parts)
        # Preserve original line ending
        ending = '\r\n' if lines[i].endswith('\r\n') else ('\n' if lines[i].endswith('\n') else '')
        out_lines[i] = new_line + ending
        src_tags = sorted(TAG_RE.findall(original_text))
        out_tags = sorted(TAG_RE.findall(vi_field))
        if src_tags != out_tags:
            blockers.append({'line': i+1, 'issue': 'TAG_MISMATCH_PREWRITE', 'src_tags': src_tags, 'vi_tags': out_tags, 'src': original_text, 'vi': vi_field})
        if sorted(PLACEHOLDER_RE.findall(original_text)) != sorted(PLACEHOLDER_RE.findall(vi_field)):
            blockers.append({'line': i+1, 'issue': 'PLACEHOLDER_MISMATCH_PREWRITE'})
        entries.append({
            'index': n,
            'line': i+1,
            'command': parts[0],
            'speaker': parts[1] if len(parts)>1 and parts[0] != 'title' else '',
            'source_text': original_text,
            'vi_text': vi_field,
            'match_status': 'EXACT_ORDERED',
            'translation_status': 'TRANSLATED',
            'ja_source': ja_pairs[n-1][0] if n-1 < len(ja_pairs) else None,
            'en_reference': en_pairs[n-1][1] if n-1 < len(en_pairs) else None,
        })
    if blockers:
        print(json.dumps({'blockers': blockers[:20], 'count': len(blockers)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    out_text = ''.join(out_lines)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    encoded = out_text.encode('utf-8')
    if src_bom:
        encoded = b'\xef\xbb\xbf' + encoded
    VI_ASSET.write_bytes(encoded)

    # QA structural checks
    vi_text = VI_ASSET.read_bytes().decode('utf-8-sig')
    vi_lines = vi_text.splitlines(True)
    issues = []
    for no,(a,b) in enumerate(zip(lines,vi_lines),1):
        aa=a.rstrip('\r\n'); bb=b.rstrip('\r\n')
        if aa.count(',') != bb.count(','):
            issues.append(f'DELIMITER_COUNT_LINE_{no}')
        pa=aa.split(','); pb=bb.split(',')
        if pa and pa[0] in TEXT_CMDS:
            idx=TEXT_CMDS[pa[0]]
            if pa[:idx] != pb[:idx] or pa[idx+1:] != pb[idx+1:]:
                issues.append(f'TECH_FIELDS_LINE_{no}')
            if ',' in pb[idx]:
                issues.append(f'ASCII_COMMA_TEXT_LINE_{no}')
            if sorted(TAG_RE.findall(pa[idx])) != sorted(TAG_RE.findall(pb[idx])):
                issues.append(f'TAG_MISMATCH_LINE_{no}')
    if len(lines) != len(vi_lines):
        issues.append('LINE_COUNT_MISMATCH')
    if src_bom != VI_ASSET.read_bytes().startswith(b'\xef\xbb\xbf'):
        issues.append('BOM_CHANGED')

    WORK.mkdir(parents=True, exist_ok=True)
    src_records = [f"L{e['line']} {e['command']}: {e['source_text']}" for e in entries]
    vi_records = [f"L{e['line']} {e['command']}: {e['vi_text']}" for e in entries]
    diff = '\n'.join(difflib.unified_diff(src_records, vi_records, fromfile='EN asset text fields', tofile='VI asset text fields', lineterm='')) + '\n'
    (WORK/'focused_diff.md').write_text('```diff\n'+diff+'```\n', encoding='utf-8')

    manifest = {
        'scene': SCENE,
        'status': 'PASS' if not issues else 'FAIL',
        'source_asset': str(EN_ASSET),
        'output_asset': str(VI_ASSET),
        'ja_json': str(JA_JSON),
        'en_json': str(EN_JSON),
        'source_sha256': sha(EN_ASSET),
        'output_sha256': sha(VI_ASSET),
        'source_bom': src_bom,
        'output_bom': VI_ASSET.read_bytes().startswith(b'\xef\xbb\xbf'),
        'newline': 'CRLF' if newline == '\r\n' else 'LF',
        'line_count': len(lines),
        'candidate_records': len(candidates),
        'command_counts': Counter(e['command'] for e in entries),
        'translated_records': len(entries),
        'issues': issues,
        'entries': entries,
    }
    # Counter not JSON serializable as desired unless cast
    manifest['command_counts'] = dict(manifest['command_counts'])
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    qa = {
        'scene': SCENE,
        'qa_status': 'PASS' if not issues else 'FAIL',
        'blockers': issues,
        'items': [],
        'notes': [
            'JP là nguồn chính; EN asset chỉ dùng để căn chỉnh thứ tự và trường văn bản.',
            'Noemi gọi 司令官さま là Chỉ Huy; khi thân mật dùng anh theo ngữ cảnh.',
            'Không có nội dung H18 trong cảnh này; không phát hiện vấn đề consent.',
            'Dấu phẩy ASCII trong field tiếng Việt đã được tránh hoặc đổi thành U+201A.',
        ],
        'counts': {'title':1, 'messageTextCenter':1, 'message':102, 'messageTextUnder':0, 'total':104},
        'paths': {'manifest': str(WORK/'manifest.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'output': str(VI_ASSET)}
    }
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': manifest['status'], 'issues': issues, 'output': str(VI_ASSET), 'qa_log': str(WORK/'qa_log.json')}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
