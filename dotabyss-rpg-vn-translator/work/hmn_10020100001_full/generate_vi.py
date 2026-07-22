# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10020100001'
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_OUT = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST = WORK / 'manifest.json'
QA_LOG = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'

translations = [
    "Tiêu Đề",
    "Nàyyy‚ anh đang làm gì vậy? Em mang bữa trưa tới cho anh mà anh không đến‚<br>nên nguội mất rồi nè!<br> ",
    "Berisa à.<br>À‚ đã đến giờ đó rồi sao.<br> ",
    "Em đã cất công mang tới cho anh rồi‚<br>nên nhớ biết ơn mà ăn cho hết đấy nhé?<br> ",
    "Ơ kìa~? Gì đây gì đây‚ núi giấy này là sao~?<br> ",
    "Chỉ là mấy việc vặt nhạt nhẽo thôi.<br>Kiểm tra giấy tờ rồi đem xử lý ấy mà.<br> ",
    "Hừm… khoan‚ chờ chút đã!? Đây là<br>báo cáo từ Ba Đại Quốc đúng không!? Toàn thứ siêu quan trọng mà~!?<br> ",
    "Cái gì vậy! Sao anh lại chất đống nhiều thế này hả~!?<br>Lỡ bị lộ ra ngoài thì anh tính sao đây~!<br> ",
    "Bọn chúng cứ việc lên mặt ra lệnh.<br>Anh chẳng có nghĩa vụ phải tuân theo quy tắc của chúng.",
    "Hay là gom lại đốt hết‚<br>rồi lấy lửa hâm nóng bữa trưa đã nguội cũng thú vị đấy.",
    "Dùng tài liệu quan trọng từ Ba Đại Quốc để hâm cơm ấy hả‚<br>cả thế giới rộng lớn này chắc chỉ có mình anh nghĩ ra thôi đó~? Phụt♪<br> ",
    "Chỉ mình anh trên đời à. Cũng không tệ.<br>Được‚ bắt đầu ngay thôi…<br> ",
    "…Chậc.<br>Phải rồi‚ hết mất rồi.",
    "Hửm~? Chẳng phải anh định đốt cái đó sao~? <br>…Ủa ủa~?<br> ",
    "Đừng nói là… anh quên ma thạch nhé~? Êê~!? <br>Anh không tự nhóm nổi lửa một mình luôn sao~?<br> ",
    "Quả nhiên không có ma pháp thì khổ ghê ha~♡<br>Đúng là yếu xìu yếu xịt mà~♪<br> ",
    "Cái giọng điệu nghe muốn nổi cáu đó là sao…<br> ",
    "Thôi được‚ em đến đúng lúc lắm.<br>Mừng đi‚ có việc cho pháp sư đây.",
    "Êê~? Em nên làm sao đây ta~?<br> ",
    "Anh mà không có ma pháp của bé Berisa thì<br>đến một ngọn lửa bé tí cũng không tạo ra nổi nhỉ~? Fufu♡<br> ",
    "Nhưng mà~ em lại mềm lòng với anh lắm~<br>nếu anh nhờ tử tế thì em làm cho cũng được đó?<br> ",
    "Nào nào~ nói thử xem? <br>『Anh muốn được bé Berisa chiều chuộng lắm♡』 ấy!<br> ",
    "…<br> ",
    "Ủa kìa? Anh ơi? <br>Nàyyy‚ anh đi đâu đó~?<br> ",
    "Ơ… không thể nào‚ anh ấy đi thật rồi!? <br>Đống giấy tờ quan trọng vẫn để nguyên ở đây mà…<br> ",
    "Trời ạ… nếu em lỡ xem thì anh tính sao đây~?<br>Anh đúng là tin bé Berisa quá mức rồi.",
    "Hay là vì anh đã ra chỉ thị rồi nên phần còn lại cứ để em đốt hết~? <br>Vừa rồi là mệnh lệnh‚ còn lại là công việc của bé Berisa~ hả?"]
translations += [
    "…Có khi anh ấy giận rồi.<br>Chắc em hơi trêu quá đà một chút rồi chăng~…<br> ",
    "Thật ra em định ăn trưa cùng anh‚<br>nên còn mang cả phần của bé Berisa nữa mà~…<br> ",
    "Này‚ tránh ra khỏi đó.<br>Nguy hiểm đấy.",
    "Kyaa!? C-cái gì vậy‚ tự nhiên quá đi~!?<br>Làm em giật cả mình~!<br> ",
    "Ơ… anh ơi? Vừa rồi là… lửa à?<br>Anh mang ma thạch theo sao~?<br> ",
    "Không‚ anh không dùng ma pháp mà dùng thứ này.<br>Đám Lux Nova gọi nó là đèn khò gas thì phải.",
    "C-của Lux Nova á!? <br>S-sao anh lại dùng thứ đó chứ~!<br> ",
    "Anh nhớ ra có một dụng cụ dùng được‚<br>nên tiện thể thử thôi.",
    "Cũng đỡ tốn công cho em rồi còn gì‚<br>rốt cuộc em bất mãn điều gì?"]
translations += [
    "Nhưng mà nhưng mà~! Chỉ cần có ma pháp của bé Berisa thì đâu cần khoa học gì hết~!<br>Mấy dụng cụ như vậy chỉ là đồ trang trí vô dụng thôi mà!<br> ",
    "Em đã nói là để em làm rồi mà~<br>…em làm đàng hoàng được mà~…!<br> ",
    "Em là em‚ dụng cụ là dụng cụ.<br>Càng có nhiều lá bài dùng được càng tốt chứ sao.",
    "Hơn nữa‚ dù có kém hơn đôi chút‚<br>anh vẫn thích những dụng cụ không cần anh phải dỗ dành hơn.",
    "Ư… chỉ vì em trêu anh một chút‚<br>mà anh giận đến thế sao…?<br> ",
    "Nếu chỉ thế đã khiến anh khó chịu‚<br>anh đã đuổi em khỏi căn cứ này từ lâu rồi.",
    "Ơ… ra vậy‚ đúng rồi nhỉ♪ <br>Dù sao bé Berisa cũng là mỹ thiếu nữ ma pháp siêu thiên tài đáng tin cậy mà~♡<br> ",
    "So với mấy dụng cụ vô hồn đó‚ bé Berisa hữu dụng hơn nhiều~<br>Anh lẽ ra nên ngoan ngoãn nhờ em ngay từ đầu mới phải♪<br> ",
    "Ồ? Sao vậy Berisa‚ em muốn có ích cho anh à?<br>Em cũng có mặt dễ thương đấy chứ.",
    "C-chuyện đó… hoàn toàn không phải vậy đâu nhé!!<br> ",
    "Chỉ là…! Em chỉ bực vì ma pháp của em<br>trông như thua khoa học của Lux Nova thôi!<br> ",
    "Thấy chưa‚ nhìn đi này!<br>Vì anh phun lửa mạnh vô ích nên toàn bộ giấy tờ cháy đen thui hết rồi~!<br> ",
    "Hâm nóng bữa trưa á? Tuyệệệt đối không được!<br>Khoa học không tinh ý như bé Berisa đâu mà~!<br> ",
    "À‚ vậy thì vừa đúng lúc.<br>Thử luôn tính tiện dụng của thứ kia nào.",
    "Ơ? K-khoan đã~?<br>Anh định làm gì vậy~?<br> ",
    "Cho vào trong cái hộp này…<br>rồi… như vầy là được à.",
    "Ra vậy.<br>Có vẻ nó đang nóng lên đúng như lý thuyết.",
    "C-cái gì đây!? Không hề dùng lửa<br>mà thức ăn… lại ấm lên rồi~!?<br> ",
    "Đây là báo cáo của Adelheid.<br>Nhìn thử đi.",
    "Tên là lò vi sóng…? Nó biến điện thành vi ba…<br>rồi truyền nhiệt vào thức ăn bên trong~…?<br> ",
    "B-bộ chuyển đổi…? Thu gom ma lực trong không khí‚ biến thành điện…<br>rồi dùng thứ đó để chạy…!?<br> ",
    "Máy móc thì phô trương mà hiệu năng chỉ đủ hâm nóng đồ ăn.<br>Anh còn tưởng nó vô dụng‚ nhưng dùng thử thì cũng không tệ.",
    "Ư! Vô dụng vô dụng vô dụng! Như vậy siêu kém hiệu quả!!<br> ",
    "Cất công gom ma lực rồi biến thành điện hả? <br>Rồi lại chuyển nó thành thứ gì đó nữa~? Trời ơi‚ phiền phức quá đi!!<br> ",
    "Phải làm đến mức đó chỉ để ăn trưa sao…<br>Đúng là khoa học toàn một đống lãng phí~!<br> ",
    "Nếu là em thì chỉ cần vèo một cái♡<br>là dùng ma pháp hâm nóng xong rồi! Không có ma lực khổ ghê ha♪<br> ",
    "Anh thấy nó nhanh và dễ hơn dùng ma pháp của em nhiều.<br>Nếu muốn đắc thắng thì cứ tự nhiên.",
    "Ưưư~!! <br>Cái vẻ mặt chẳng quan tâm đó là thứ làm em bực nhất!!<br> ",
    "Dù sao thì đồ ăn hâm bằng cái máy như thế<br>chắc chắn không thể ngon được!<br> ",
    "Nếu em tò mò đến vậy thì tự ăn thử đi.<br>Nào‚ há miệng ra.",
    "C-chờ đã‚ đợi chút! Đừng đột ngột như vậy… ưm!?<br> ",
    "A… nó ấm thật… mà còn ngon nữa…<br> ",
    "Thấy chưa? Cũng không tệ đúng không?<br>Có cái máy này‚ có khi ta ăn được bữa nóng ngay trên chiến trường.",
    "L-lúc nào cũng có cơm nóng…<br> ",
    "Có vẻ cơ thể em đã hiểu đủ rõ<br>giá trị của cái máy này rồi nhỉ.",
    "H-hiểu bằng cơ thể…!? C-cách nói đó là sao chứ!<br> ",
    "Một dụng cụ chán ngắt thế này<br>làm sao khiến bé Berisa chịu hiểu được chứ!?<br> ",
    "Em tuyệệệệt đối sẽ không bao giờ thừa nhận đâu…!!<br> ",
    "Ừm‚ bên đó là bữa trưa của em à?<br>Anh hâm nóng luôn cho‚ đưa đây.",
    "K-không cần đâu! Em có ma pháp của mình rồi‚<br>nên chẳng cần món đồ chơi khoa học đó đâu!<br> ",
    "A… t-tất cả… cháy hết rồi…<br> ",
    "Nếu muốn khoe hỏa lực thì ra chiến trường mà khoe.<br>Lương thực là vật tư chiến lược đấy‚ đừng lãng phí.",
    "E-em xin lỗi…<br>Ưư~‚ bữa trưa hôm nay… em đã mong chờ lắm mà…<br> ",
    "…Được rồi được rồi.<br>Anh sẽ chia thêm phần của anh cho em.",
    "T-thật sao!? Trời ạ‚ anh đúng là yêu bé Berisa quá rồi đó~?♡<br> ",
    "Nếu em không chê cơm được hâm bằng khoa học thì vậy.",
    "…Ư‚ k-không‚ em không cần đâu!<br>Chỉ cần có ma pháp thì khoa học là thứ không cần thiết mà!<br> ",
    "À‚ em chắc chứ?"]
translations += [
    "E-em chắc!!<br>Bé Berisa tuyệt đối sẽ không thừa nhận khoa học đâu!!<br> ",
    "Ưưưư~…<br> ",
    "Thật tình‚ rốt cuộc em không thích điểm nào chứ…"
]

TEXT_TYPES = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def newline_style(b):
    return 'CRLF' if b'\r\n' in b else 'LF'

def split_lines_keep(text):
    return text.splitlines(keepends=True)

def line_ending(line):
    if line.endswith('\r\n'): return '\r\n'
    if line.endswith('\n'): return '\n'
    return ''

def strip_eol(line):
    return line[:-2] if line.endswith('\r\n') else (line[:-1] if line.endswith('\n') else line)

def load_pairs(path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=list)

def text_index(kind):
    return 1 if kind == 'title' else 2

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:\d+\$)?[sd]|\{[^{}]+\}|\$\{[^{}]+\}|\\[nrt]|%%', s)

def has_japanese(s):
    return re.search(r'[\u3040-\u30ff\u3400-\u9fff]', s) is not None

WORK.mkdir(parents=True, exist_ok=True)
VI_OUT.parent.mkdir(parents=True, exist_ok=True)

en_bytes = EN_ASSET.read_bytes()
had_bom = en_bytes.startswith(b'\xef\xbb\xbf')
encoding = 'utf-8-sig' if had_bom else 'utf-8'
source_text = en_bytes.decode(encoding)
lines = split_lines_keep(source_text)

candidates = []
for idx, line in enumerate(lines, 1):
    body = strip_eol(line)
    parts = body.split(',')
    if parts and parts[0] in TEXT_TYPES:
        ti = text_index(parts[0])
        if len(parts) <= ti:
            raise SystemExit(f'bad candidate line {idx}')
        candidates.append({'line': idx, 'kind': parts[0], 'speaker': parts[1] if len(parts)>1 else '', 'text': parts[ti], 'delims': body.count(',')})

if len(translations) != len(candidates):
    raise SystemExit(f'translation count {len(translations)} != candidates {len(candidates)}')

# Preserve the asset text field's exact <br> count. EN asset wrapping is authoritative
# for UI tags even when JP line breaks differ.
def reconcile_br_count(vi, src):
    src_n = src.count('<br>')
    vi_n = vi.count('<br>')
    if vi_n > src_n:
        # Remove excess tags from left to right by turning them into spaces.
        excess = vi_n - src_n
        out = vi
        while excess:
            out = out.replace('<br>', ' ', 1)
            excess -= 1
        return out
    if vi_n < src_n:
        missing = src_n - vi_n
        m = re.search(r'\s*$', vi)
        trail = m.group(0) if m else ''
        core = vi[:len(vi)-len(trail)] if trail else vi
        return core + ('<br>' * missing) + trail
    return vi

translations = [reconcile_br_count(t, c['text']) for t, c in zip(translations, candidates)]

comma_errors = [(i, t) for i, t in enumerate(translations) if ',' in t]
if comma_errors:
    raise SystemExit(f'ASCII comma in translations: {comma_errors[:5]}')

out_lines = list(lines)
entries = []
for n, (cand, vi) in enumerate(zip(candidates, translations)):
    li = cand['line'] - 1
    eol = line_ending(out_lines[li])
    body = strip_eol(out_lines[li])
    parts = body.split(',')
    ti = text_index(parts[0])
    old_parts = parts[:]
    parts[ti] = vi
    out_lines[li] = ','.join(parts) + eol
    entries.append({
        'index': n,
        'line': cand['line'],
        'kind': cand['kind'],
        'speaker': cand['speaker'],
        'asset_en': cand['text'],
        'vi': vi,
        'match_status': 'EXACT_ORDERED',
        'translation_status': 'TRANSLATED',
        'unchanged_text': cand['text'] == vi,
    })

out_text = ''.join(out_lines)
VI_OUT.write_bytes((('\ufeff' if had_bom else '') + out_text).encode('utf-8'))

# QA
vi_bytes = VI_OUT.read_bytes()
vi_text = vi_bytes.decode(encoding)
vi_lines = split_lines_keep(vi_text)
blockers = []
items = []
if len(lines) != len(vi_lines):
    blockers.append({'type': 'LINE_COUNT_MISMATCH', 'en': len(lines), 'vi': len(vi_lines)})
if had_bom != vi_bytes.startswith(b'\xef\xbb\xbf'):
    blockers.append({'type': 'BOM_MISMATCH', 'en_bom': had_bom, 'vi_bom': vi_bytes.startswith(b'\xef\xbb\xbf')})
if newline_style(en_bytes) != newline_style(vi_bytes):
    blockers.append({'type': 'NEWLINE_MISMATCH', 'en': newline_style(en_bytes), 'vi': newline_style(vi_bytes)})

changed_text_records = 0
kept_en = []
for i, (en_line, vi_line) in enumerate(zip(lines, vi_lines), 1):
    en_body = strip_eol(en_line); vi_body = strip_eol(vi_line)
    if en_body.count(',') != vi_body.count(','):
        blockers.append({'type':'DELIMITER_COUNT_MISMATCH','line':i,'en':en_body.count(','),'vi':vi_body.count(',')})
        continue
    en_parts = en_body.split(','); vi_parts = vi_body.split(',')
    if en_parts and en_parts[0] in TEXT_TYPES:
        ti = text_index(en_parts[0])
        if len(en_parts) != len(vi_parts):
            blockers.append({'type':'FIELD_COUNT_MISMATCH','line':i,'en':len(en_parts),'vi':len(vi_parts)})
            continue
        if en_parts[:ti] + en_parts[ti+1:] != vi_parts[:ti] + vi_parts[ti+1:]:
            blockers.append({'type':'TECH_FIELD_CHANGED','line':i})
        if en_parts[ti] != vi_parts[ti]:
            changed_text_records += 1
        else:
            kept_en.append({'line':i,'kind':en_parts[0],'text':vi_parts[ti]})
        if ',' in vi_parts[ti]:
            blockers.append({'type':'ASCII_COMMA_IN_TEXT_FIELD','line':i,'text':vi_parts[ti]})
        if tags(en_parts[ti]) != tags(vi_parts[ti]):
            blockers.append({'type':'TAG_MISMATCH','line':i,'en':tags(en_parts[ti]),'vi':tags(vi_parts[ti])})
        if placeholders(en_parts[ti]) != placeholders(vi_parts[ti]):
            blockers.append({'type':'PLACEHOLDER_MISMATCH','line':i,'en':placeholders(en_parts[ti]),'vi':placeholders(vi_parts[ti])})
        if has_japanese(vi_parts[ti]):
            blockers.append({'type':'JAPANESE_LEFTOVER_IN_TEXT','line':i,'text':vi_parts[ti]})
        if re.search(r'\b(?:what|where|science|magic|lunch|Mister|Big Bro|Verisa|Title)\b', vi_parts[ti], re.I):
            blockers.append({'type':'ENGLISH_LEFTOVER_SUSPECT','line':i,'text':vi_parts[ti]})
    else:
        if en_body != vi_body:
            blockers.append({'type':'NON_TEXT_LINE_CHANGED','line':i})

if kept_en:
    blockers.append({'type':'UNINTENTIONAL_KEPT_EN_TEXT', 'records': kept_en})

ja_pairs = load_pairs(JA_JSON)
en_pairs = load_pairs(EN_JSON)
counts = {k: sum(1 for c in candidates if c['kind']==k) for k in sorted(TEXT_TYPES)}
manifest = {
    'scene': SCENE,
    'status': 'PASS' if not blockers else 'FAIL',
    'source_paths': {'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN_ASSET)},
    'output_path': str(VI_OUT),
    'artifact_paths': {'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'script': str(Path(__file__))},
    'source': {
        'en_asset_sha256': sha256(EN_ASSET), 'en_asset_bytes': len(en_bytes), 'bom': had_bom,
        'newline': newline_style(en_bytes), 'line_count': len(lines),
        'candidate_text_records': len(candidates), 'candidate_counts': counts,
        'ja_pairs': len(ja_pairs), 'en_pairs': len(en_pairs)
    },
    'output': {'vi_sha256': sha256(VI_OUT), 'bytes': len(vi_bytes), 'line_count': len(vi_lines), 'changed_text_records': changed_text_records},
    'entries': entries,
    'notes': [
        'JP is primary; EN asset used for authoritative field order/alignment.',
        'All H18/adult content rule acknowledged for project; this scene contains no explicit H18 content.',
        'Speaker names and technical charaload/ID fields preserved. Internal ベリサちゃん localized as bé Berisa; おにーさん localized as anh/anh ơi by context.',
        'ASCII commas inside Vietnamese text fields replaced with U+201A where needed.'
    ]
}
qa = {
    'scene': SCENE,
    'qa_status': 'PASS' if not blockers else 'FAIL',
    'blockers': blockers,
    'items': items,
    'kept_english_records': [],
    'intentional_identical_records': [],
    'structural_qa': {
        'line_count_match': len(lines)==len(vi_lines),
        'bom_match': had_bom == vi_bytes.startswith(b'\xef\xbb\xbf'),
        'newline_match': newline_style(en_bytes)==newline_style(vi_bytes),
        'delimiter_mismatches': [b for b in blockers if b.get('type')=='DELIMITER_COUNT_MISMATCH'],
        'field_or_tech_mismatches': [b for b in blockers if b.get('type') in ('FIELD_COUNT_MISMATCH','TECH_FIELD_CHANGED','NON_TEXT_LINE_CHANGED')],
        'tag_placeholder_mismatches': [b for b in blockers if b.get('type') in ('TAG_MISMATCH','PLACEHOLDER_MISMATCH')]
    },
    'linguistic_qa': {
        'commander_term': 'No Commander/司令官 line in this scene; <user> translated as male MC anh where appropriate.',
        'character_names': 'Technical speaker names kept unchanged; Berisa used consistently in Vietnamese text for ベリサちゃん.',
        'h18': 'No explicit H18 content detected in this file; project adult rule noted.'
    },
    'counts': manifest['source'] | manifest['output']
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

# focused diff: only candidate lines
before = [f"L{c['line']}: {strip_eol(lines[c['line']-1])}\n" for c in candidates]
after = [f"L{c['line']}: {strip_eol(vi_lines[c['line']-1])}\n" for c in candidates]
diff = difflib.unified_diff(before, after, fromfile='EN text records', tofile='VI text records', lineterm='\n')
DIFF.write_text(''.join(diff), encoding='utf-8')
print(json.dumps({'qa_status': qa['qa_status'], 'blockers': len(blockers), 'output': str(VI_OUT), 'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'changed_text_records': changed_text_records, 'candidate_text_records': len(candidates)}, ensure_ascii=False, indent=2))
if blockers:
    raise SystemExit(1)
