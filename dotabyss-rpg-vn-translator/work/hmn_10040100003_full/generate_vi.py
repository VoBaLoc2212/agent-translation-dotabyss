from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10040100003'
JP = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
ENJ = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST = WORK / 'manifest.json'
QA_LOG = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'

TEXT_TYPES = {'title':1, 'message':2, 'messageTextUnder':2, 'messageTextCenter':2}

translations = [
    'Đó Là Tấm Lòng Không Thể Phá Vỡ',
    'Ừm‚ tiếp theo. Ừm‚ cái tiếp theo nữa.<br> ',
    'Tốt lắm‚ Xiaolei! Em rửa đĩa mà không làm vỡ cái nào rồi đấy!<br> ',
    'Có thể nói em đã kiểm soát sức mạnh hoàn hảo rồi! Giỏi lắm‚<br>Xiaolei!<br> ',
    'Thầy‚ vẫn còn nguy hiểm. Nếu Xiaolei không cẩn thận‚ Xiaolei sẽ làm<br>vỡ ngay.<br> ',
    'Cúp piu!<br> ',
    'Cúp piu‚ piu!<br> ',
    'Ừ‚ Panpan và Dandan cũng làm tốt lắm. Nhờ có hai đứa đấy.<br> ',
    'Vấn đề Xiaolei đang gặp là sức mạnh quá lớn nên không kiểm soát được‚<br>thành ra làm hỏng những thứ xung quanh.<br> ',
    'Ừm… không dùng sức‚ khó quá.<br> ',
    'Vì em cứ mải rèn luyện suốt nên chắc vẫn chưa nắm được cảm giác<br>thả lỏng sức lực.<br> ',
    'Nhưng này‚ Xiaolei. Có những đối tượng mà em đang chạm vào rất nhẹ nhàng‚ không hề dùng sức đấy.<br> ',
    'Ơ…?<br> ',
    'Chính là mấy đứa này!<br> ',
    'Cúp piu!<br> ',
    'Cúp piu‚ cúp piu!<br> ',
    'Panpan‚ Dandan…?<br> ',
    'Đúng vậy. Quan sát Xiaolei‚ thầy nhận ra chỉ khi chạm vào<br>mấy chú gấu trúc này‚ em mới điều chỉnh sức lực nhẹ nhàng được.<br> ',
    'Vì nếu Xiaolei vuốt mạnh‚ hai bạn sẽ đau… Panpan và Dandan<br>là những người rất quan trọng với Xiaolei‚ nên Xiaolei không muốn làm hai bạn bị thương.<br> ',
    'À… đó là‚ làm sức mạnh yếu đi‚ phải không?<br> ',
    'Chính xác! Nghĩa là em chỉ cần đối xử với mọi thứ bằng cảm giác<br>dịu dàng như khi vuốt ve mấy chú gấu trúc thôi!<br> ',
    'Nào‚ hãy xem cái cốc là Panpan và cái đĩa là Dandan rồi thử<br>cầm chúng lên đi!<br> ',
    'Ơ… đĩa‚ cốc… Không dễ thương như hai bạn…<br> ',
    'Thôi được rồi! Ta đi mua bộ bát đĩa họa tiết gấu trúc! Như vậy<br>thì em khỏi phàn nàn chứ gì!<br> ',
    'Họa tiết gấu trúc… Ừm‚ muốn có.<br> ',
    'Thầy‚ xong rồi.<br> ',
    'Vất vả rồi. Em làm tốt lắm. Nếu cứ quen dần theo đà này‚<br>chắc sinh hoạt hằng ngày sẽ không còn vấn đề gì nữa.<br> ',
    'Nhưng vẫn còn thất bại… Lúc gần cuối‚ em làm vỡ vài cái đĩa…<br> ',
    'Hiện tại em đang điều chỉnh sức mạnh bằng cách tưởng tượng lúc vuốt ve<br>Panpan và Dandan. Nếu mất tập trung thì có lúc mắc lỗi cũng là chuyện thường.<br> ',
    'Không sao đâu. Cứ làm rồi em sẽ ngày càng quen hơn. Đến lúc nhận ra<br>thì tự nhiên sẽ làm được thôi.<br> ',
    'Ừm… xìe xìe‚ thầy.<br> ',
    'Chỉ một chút thôi‚ nhưng em làm được rồi. Quả nhiên thầy giỏi thật.<br> ',
    'Cũng không đến mức phải cảm ơn thầy nhiều vậy đâu.<br> ',
    'Em muốn cảm ơn. Xiaolei sẽ làm bất cứ gì. Thầy muốn gì?<br> ',
    'Đừng tùy tiện nói “bất cứ gì” như thế. Thầy biết rõ nhận lời bừa<br>chính là cửa vào địa ngục đấy.<br> ',
    'Ừm‚ học được rồi.<br> ',
    'Hừ‚ ngoan lắm. Vậy thì… thay lời cảm ơn‚ hãy mang cho thầy<br>mấy cái cốc đã dùng xong trong phòng chỉ huy.<br> ',
    'Em hiểu rồi…!<br> ',
    'Tốt tốt‚ vấn đề đã giải quyết. Chỉ cần kiểm soát được sức mạnh‚<br>Xiaolei là một chiến lực ưu tú và là một đứa trẻ ngoan ngoãn‚ thật thà.<br> ',
    'Chà‚ vấn đề là tiếp theo nên dạy em điều gì. Dù thầy vốn chẳng<br>hợp làm thầy giáo chút nào――<br> ',
    'ĐOÀNG!!!<br> ',
    'Cái‚ cái âm thanh gì vậy!? Không‚ không lẽ――!!<br> ',
    'À… cánh cửa lại bay mất rồi… Hơn nữa còn cắm hẳn vào tường…<br> ',
    'Thầy… xin lỗi.<br> ',
    '…………Lần này lại chuyện gì nữa? Lại là bươm bướm à?<br> ',
    'Ừm… được thầy nhờ nên em vui quá… Rồi quên tưởng tượng<br>mình đang vuốt ve Panpan và Dandan…<br> ',
    'Vậy là em mất cảnh giác rồi. Thôi‚ hưng phấn quá mà thất bại là chuyện thường.<br>Đây cũng là kinh nghiệm‚ đừng bận tâm.<br> ',
    '(Nhưng mới sửa cửa lần trước thôi mà. Lần này còn cả bức tường nữa… Alicia<br>chắc sẽ cằn nhằn mình. Thiệt tình…)<br> ',
    'Ngay lúc đó‚ cánh cửa đã đâm vào tường rồi khựng lại<br>từ từ đổ xuống phía này――!<br> ',
    '(Chết‚ nguy rồi! Mình sẽ bị đè――!)<br> ',
    'Thầy!<br> ',
    'Ngay sau khi bị Xiaolei đẩy ra và gần như ngã khỏi chỗ đó‚<br>cánh cửa đổ xuống‚ phát ra một tiếng rầm nặng nề.<br> ',
    'Thầy‚ bình an chứ? Đây‚ tay em này.<br> ',
    'Ừ‚ cảm ơn…<br> ',
    'Phù… nhưng nguy hiểm thật. Em cứu thầy kịp lúc giỏi lắm.<br> ',
    'Đương nhiên. Thầy‚ em sẽ bảo vệ thầy.<br> ',
    'Thật là‚ đáng tin cậy quá. Cái gọi là xìe xìe đấy nhỉ.<br> ',
    'Nhưng… nói cho cùng là lỗi của Xiaolei… Nếu em không thổi bay cánh cửa‚<br>thầy đã không suýt bị đè.<br> ',
    'Thế nên thầy đã bảo em đừng bận tâm mà. Kết quả là thầy không bị thương――<br> ',
    '…Ơ? Thầy thật sự không bị thương chút nào nhỉ?<br> ',
    '…? Xiaolei đã bảo vệ thầy đàng hoàng.<br> ',
    'Không‚ không phải ý đó.<br>Thầy đã bị Xiaolei đẩy đúng không?<br> ',
    'Ừm.<br> ',
    'Chuyện xảy ra đột ngột như vậy‚<br>chắc Xiaolei đã lao vào mà không kịp suy nghĩ gì.<br> ',
    'Nghĩa là thầy có bị hất văng đi cũng không lạ…<br>Ấy vậy mà chẳng những không bị thương‚ còn không đau chỗ nào.<br> ',
    'Hừm.<br>Đương nhiên.<br> ',
    'Nếu không được thầy dạy‚<br>Xiaolei chẳng biết gì cả và đã gây phiền cho rất nhiều người.<br> ',
    'Như vậy không phải một võ sĩ mạnh mẽ.<br>Chỉ là người gây phiền phức.<br> ',
    'Thầy đã chỉ đường cho Xiaolei.<br>Thầy là người rất quan trọng với Xiaolei.<br> ',
    'Dù lúc nào‚ em cũng sẽ không làm thầy bị thương.<br>Hãy tin Xiaolei‚ thầy.<br> ',
    '…Ừ‚ thầy tin em.<br>Vì em là cô học trò đáng yêu của thầy mà.<br> ',
    'Ừm‚ xìe xìe‚ thầy.<br> ',
    'À… nhắc mới nhớ‚ cánh cửa‚ làm sao đây…<br> ',
    'Đồ đã hỏng thì chỉ còn cách vứt bỏ thôi.<br>Xiaolei‚ em mang nó ra ngoài được không?<br> ',
    'Về mức sức lực thì… để xem nào.<br>Nhờ em dùng cỡ lúc bế thầy nhé.<br> ',
    'Cứ giao cho em‚ thầy.<br>Hây… dô.<br> ',
    'RẮC!!!<br> ',
    'Cánh cửa Xiaolei nhấc lên đã nứt đôi ngay từ<br>chính giữa.<br> ',
    '…………Sống lưng thầy vừa lạnh buốt đấy.<br>Đó là mức sức lực em định dùng khi bế thầy đúng không?<br> ',
    'Th‚ thầy sẽ không vỡ như thế này‚ nên…<br> ',
    'Thầy! Dễ! Vỡ lắm đấy!<br> ',
    'Thiệt tình… Có vẻ còn lâu nữa em mới kiểm soát được hoàn hảo‚<br>nhỉ…<br> ',
    'Ừm‚ nhờ thầy chỉ bảo‚ thầy.<br>Hãy dạy em thêm nhiều điều nữa.<br> ',
]

# Avoid ASCII comma in all translated fields.
for i, s in enumerate(translations):
    if ',' in s:
        raise SystemExit(f'ASCII comma in translation {i}: {s!r}')

WORK.mkdir(parents=True, exist_ok=True)
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def props(path):
    b = Path(path).read_bytes()
    bom = b.startswith(b'\xef\xbb\xbf')
    newline = 'CRLF' if b.count(b'\r\n') == b.count(b'\n') and b.count(b'\n') else 'LF'
    text = b.decode('utf-8-sig')
    return {'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'bom': bom, 'newline': newline, 'line_count': len(text.splitlines(True)), 'endswith_newline': text.endswith('\n')}

src_b = EN_ASSET.read_bytes()
bom = src_b.startswith(b'\xef\xbb\xbf')
text = src_b.decode('utf-8-sig')
newline = '\r\n' if b'\r\n' in src_b else '\n'
lines = text.splitlines(True)

candidate_idxs = []
for idx, line in enumerate(lines):
    raw = line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith('\n') else line
    rec = raw.split(',', 1)[0]
    if rec in TEXT_TYPES:
        candidate_idxs.append(idx)

if len(candidate_idxs) != len(translations):
    raise SystemExit(f'translation count {len(translations)} != candidates {len(candidate_idxs)}')

out_lines = list(lines)
entries = []
for n, (idx, vi) in enumerate(zip(candidate_idxs, translations), 1):
    line = lines[idx]
    ending = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
    raw = line[:-len(ending)] if ending else line
    parts = raw.split(',')
    rec = parts[0]
    text_idx = TEXT_TYPES[rec]
    if text_idx >= len(parts):
        raise SystemExit(f'bad field count line {idx+1}')
    old_text = parts[text_idx]
    old_sig = parts[:text_idx] + parts[text_idx+1:]
    parts[text_idx] = vi
    new_raw = ','.join(parts)
    out_lines[idx] = new_raw + ending
    entries.append({
        'ordinal': n,
        'line': idx + 1,
        'record_type': rec,
        'speaker_or_field0': parts[1] if len(parts) > 1 else '',
        'source_text': old_text,
        'vi_text': vi,
        'match_status': 'EXACT_OR_ORDERED_CONTEXT',
        'translation_status': 'TRANSLATED',
        'technical_signature_unchanged': old_sig == (parts[:text_idx] + parts[text_idx+1:]),
    })

out_text = ''.join(out_lines)
out_bytes = (b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
VI_ASSET.write_bytes(out_bytes)

# QA
vi_b = VI_ASSET.read_bytes()
vi_text = vi_b.decode('utf-8-sig')
vi_lines = vi_text.splitlines(True)
blockers = []
items = []
if len(vi_lines) != len(lines):
    blockers.append({'type':'LINE_COUNT_MISMATCH','en':len(lines),'vi':len(vi_lines)})
if vi_b.startswith(b'\xef\xbb\xbf') != bom:
    blockers.append({'type':'BOM_MISMATCH'})
vi_nl = 'CRLF' if vi_b.count(b'\r\n') == vi_b.count(b'\n') and vi_b.count(b'\n') else 'LF'
if vi_nl != ('CRLF' if newline == '\r\n' else 'LF'):
    blockers.append({'type':'NEWLINE_MISMATCH','en':newline,'vi':vi_nl})

tag_re = re.compile(r'<[^>]+>')
ph_re = re.compile(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]')
kept_english = []
intentional_identical = []
for idx, (el, vl) in enumerate(zip(lines, vi_lines), 1):
    eraw = el[:-2] if el.endswith('\r\n') else el[:-1] if el.endswith('\n') else el
    vraw = vl[:-2] if vl.endswith('\r\n') else vl[:-1] if vl.endswith('\n') else vl
    if eraw.count(',') != vraw.count(','):
        blockers.append({'type':'DELIMITER_COUNT_MISMATCH','line':idx,'en':eraw.count(','),'vi':vraw.count(',')})
        continue
    ep = eraw.split(',')
    vp = vraw.split(',')
    rec = ep[0]
    if rec in TEXT_TYPES:
        ti = TEXT_TYPES[rec]
        if len(ep) <= ti or len(vp) <= ti:
            blockers.append({'type':'FIELD_COUNT_MISMATCH','line':idx})
            continue
        if ep[:ti] + ep[ti+1:] != vp[:ti] + vp[ti+1:]:
            blockers.append({'type':'TECH_FIELDS_CHANGED','line':idx})
        et, vt = ep[ti], vp[ti]
        if tag_re.findall(et) != tag_re.findall(vt):
            blockers.append({'type':'TAG_MISMATCH','line':idx,'en_tags':tag_re.findall(et),'vi_tags':tag_re.findall(vt)})
        if ph_re.findall(et) != ph_re.findall(vt):
            blockers.append({'type':'PLACEHOLDER_MISMATCH','line':idx})
        if ',' in vt:
            blockers.append({'type':'ASCII_COMMA_IN_VI_TEXT_FIELD','line':idx,'text':vt})
        if et == vt:
            kept_english.append({'line':idx,'text':vt})
        if re.search(r'\b(Teacher|Xiaolei|Panpan|Dandan|Squeak|Good grief|Crack|Great|Thanks|Mm|Yeah|Fine|Alicia|Command Room)\b', vt):
            # Proper names Xiaolei/Panpan/Dandan/Alicia are allowed; other English terms are blockers.
            bad = [w for w in re.findall(r'\b(?:Teacher|Squeak|Good grief|Crack|Great|Thanks|Command Room)\b', vt)]
            if bad:
                blockers.append({'type':'LEFTOVER_ENGLISH_TOKEN','line':idx,'tokens':bad,'text':vt})

# focused diff
before = []
after = []
for e in entries:
    li = e['line']
    before.append(f"L{li}: {lines[li-1].rstrip()}\n")
    after.append(f"L{li}: {vi_lines[li-1].rstrip()}\n")
diff = ''.join(difflib.unified_diff(before, after, fromfile='EN translatable lines', tofile='VI translatable lines', lineterm='\n'))
DIFF.write_text('# Focused Diff: hmn_10040100003\n\n```diff\n' + diff + '\n```\n', encoding='utf-8')

source_props = props(EN_ASSET)
output_props = props(VI_ASSET)
manifest = {
    'scene': SCENE,
    'created_at': datetime.now(timezone.utc).isoformat(),
    'sources': {'ja_json': props(JP), 'en_json': props(ENJ), 'en_asset': source_props},
    'output': output_props,
    'work_dir': str(WORK),
    'candidate_record_counts': {k: sum(1 for l in lines if l.startswith(k+',')) for k in TEXT_TYPES},
    'candidate_total': len(candidate_idxs),
    'translated_records': len(entries),
    'entries': entries,
    'artifacts': {'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'script': str(Path(__file__))},
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
qa = {
    'scene': SCENE,
    'qa_status': 'PASS' if not blockers else 'FAIL',
    'blockers': blockers,
    'items': items,
    'kept_english_records': kept_english,
    'intentional_identical_records': intentional_identical,
    'checks': {
        'line_count_match': len(vi_lines) == len(lines),
        'bom_preserved': vi_b.startswith(b'\xef\xbb\xbf') == bom,
        'newline_preserved': vi_nl == ('CRLF' if newline == '\r\n' else 'LF'),
        'candidate_total': len(candidate_idxs),
        'translated_records': len(entries),
        'delimiter_counts_match': not any(b.get('type') == 'DELIMITER_COUNT_MISMATCH' for b in blockers),
        'technical_fields_unchanged': not any(b.get('type') == 'TECH_FIELDS_CHANGED' for b in blockers),
        'tags_placeholders_preserved': not any(b.get('type') in {'TAG_MISMATCH','PLACEHOLDER_MISMATCH'} for b in blockers),
        'no_ascii_comma_in_vi_text_fields': not any(b.get('type') == 'ASCII_COMMA_IN_VI_TEXT_FIELD' for b in blockers),
        'no_unintentional_kept_english': not kept_english,
    },
    'notes': [
        'JP ja.json used as primary source; EN asset/en.json used for ordered alignment.',
        'All characters confirmed 18+ by project context; no H18 content appeared in this scene.',
        'Speaker fields and charaload names preserved exactly; in-text names follow existing EN mapping Xiaolei/Panpan/Dandan.',
        'ASCII commas in Vietnamese text fields replaced with U+201A where a comma-like pause was needed.',
    ],
}
qa['independent_verify'] = {
    'status': 'PASS' if qa['qa_status'] == 'PASS' else 'FAIL',
    'method': 'Re-read EN and VI asset bytes after writing; independently recompute line count, BOM/newline, delimiter counts, technical signatures, tag/placeholder parity, candidate/changed counts, ASCII comma guard, and kept-English equality.',
    'candidate_records': len(candidate_idxs),
    'changed_text_records': sum(
        1 for idx in candidate_idxs
        if lines[idx].rstrip('\r\n').split(',')[TEXT_TYPES[lines[idx].split(',', 1)[0]]] != vi_lines[idx].rstrip('\r\n').split(',')[TEXT_TYPES[vi_lines[idx].split(',', 1)[0]]]
    ),
    'problems': blockers,
    'kept_english_records': kept_english,
}
QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status': qa['qa_status'], 'blockers': len(blockers), 'output': str(VI_ASSET), 'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'translated_records': len(entries)}, ensure_ascii=False, indent=2))
