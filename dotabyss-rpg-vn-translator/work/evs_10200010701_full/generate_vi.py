from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

SCENE = 'evs_10200010701'
ROOT = Path('E:/AgentTranslation')
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/evs_10200010701_full'

VI = [
    'Tiêu Đề',
    '...Thấy rồi~~!<br>Đó là kết tinh ma lực cần cho việc chữa trị của Wendy!<br> ',
    'Nhờ chiếc xe kéo cải tạo và lối tắt‚<br>cả nhóm đã tiến tới tận tầng sâu của Đại Huyệt.<br> ',
    'Em chưa từng thấy kết tinh ma lực nào lớn đến thế... nhưng...<br> ',
    'Ừm... chuyện này hơi rắc rối rồi đây~.<br> ',
    'Một bầy quái vật đang lảng vảng bên cạnh kết tinh ma lực.<br>Cứ như lính gác bảo vệ nó vậy.<br> ',
    'Có vẻ bọn chúng không định rời khỏi kết tinh ma lực đâu...<br>Cả khu vực này chắc là lãnh địa của chúng rồi nhỉ~.<br> ',
    'Có lẽ chúng đang hấp thụ ma lực rò rỉ từ kết tinh...<br>Nếu vậy thì nên xem chúng mạnh hơn cá thể bình thường.<br> ',
    'Quái vật tép riu... chắc lần này không gọi vậy được rồi~.<br> ',
    'Chỉ cần Wendy chạm được vào kết tinh ma lực là ổn‚<br>nhưng nhìn thế kia thì chắc chắn chúng sẽ cản đường rồi~.<br> ',
    'Mình làm sao đây‚ chị hai?<br> ',
    'Còn phải hỏi sao――xông thẳng qua thôi!<br>Đứa nào cản đường thì thổi bay hết～～!!<br> ',
    'Ểểể～～～!!?<br>L-làm như vậy thật sự ổn sao ạ!?<br> ',
    'Chỉ có đám tép riu mới bày trò vòng vo thôi♪<br>Hai chị em tụi này hợp sức là vô địch♪ Dư sức phá vòng vây luôn♪<br> ',
    'Đừng lo‚ Wendy.<br>Chị hai của em là một pháp sư cực kỳ lợi hại mà♪<br> ',
    '...Em hiểu rồi. Em tin hai người!<br>Đi thôi――!<br> ',
    'Bầy quái vật lấy vùng quanh kết tinh ma lực khổng lồ làm lãnh địa.<br>――Một vài con trong số đó nhận ra chấn động truyền qua mặt đất.<br> ',
    '...Gigi?<br> ',
    'Sự cảnh giác trước tình huống bất thường dần lan ra khắp bầy‚<br>từng con bắt đầu nhìn quanh. Và rồi――<br> ',
    'Tránh ra tránh ra～～～～～!!<br>Đứa nào không tránh thì bị hất văng đóーーーー!!<br> ',
    '――Chiếc xe kéo chở Verisa và mọi người lao tới<br>với tốc độ khủng khiếp!<br> ',
    'Hỡi lửa! Thiêu rụi kẻ cản đường――!!<br> ',
    'Hỡi băng! Hóa thành giáo xuyên thủng tà ác――!!<br> ',
    'Ma pháp hai chị em phóng ra thiêu cháy và xuyên thủng lũ quái vật.<br>Một phần những con thoát khỏi ma pháp bị xe kéo hất bay lên không trung.<br> ',
    'Gigigiiーーーー...!!?<br> ',
    'Awa!? Awawawawa~!?<br>Chuyện này hình như dữ dội quá rồi...!<br> ',
    'Không sao hết!<br>Cứ thế này lao thẳng tới kết tinh ma lực～～!!<br> ',
    'Em cũng muốn vậy lắm‚ chị hai...!<br>Nhưng cơ cấu cô Honoka gắn cho mình đang phát ra tiếng lạ...!!<br> ',
    'Hả――!?<br> ',
    'Ngay khoảnh khắc sau‚ ống gắn trên xe kéo phát nổ và phun khói.<br>Mất lực đẩy‚ chiếc xe lập tức giảm tốc rồi dừng lại giữa bầy quái vật.<br> ',
    'K-không‚ đùa chị chắc～～!?<br>Lại dừng đúng chỗ này sao～～!?<br> ',
    'Chị hai! Quái vật đang...!<br> ',
    'Đám quái vật vốn đứng xa cảnh giác‚<br>nhưng có lẽ thấy bên này không còn di chuyển được nên bắt đầu lừ lừ áp sát.<br> ',
    '(Cứ thế này sẽ bị bao vây mất...!<br>Nếu đã vậy thì ít nhất phải để hai người họ...!)<br> ',
    'Verisa‚ Viera! Mau chạy đi!<br>Đừng bận tâm đến em!<br> ',
    'Hả~? Em đang nói chuyện ngốc nghếch gì vậy～～?<br>――Verisa-chan đây sao có thể thua đám này được chứ!<br> ',
    'Cho nên――Wendy cũng không được bỏ cuộc!<br> ',
    'Chỉ còn một chút nữa là chạm tới kết tinh ma lực rồi!<br>Nhất định bọn em sẽ mở đường!<br> ',
    'Nhưng...! Nếu cố quá thì hai người sẽ chết mất!<br> ',
    'Không sao hết!<br>Vì bạn bè thì một hai mạng này em cũng cược cho xem――!!<br> ',
    '(――! Họ sẵn sàng đến mức đó vì mình...)<br> ',
    'Verisa và Viera dùng ma pháp nghênh chiến bầy quái vật.<br>Hai người chiến đấu rất tốt nhưng dần bị số lượng quái vật áp đảo.<br> ',
    'Gigii!!<br> ',
    'Kyaa!?<br> ',
    'Viera!?<br>Khốn kiếp! Dám làm vậy với em gái quý giá của ta sao!!<br> ',
    'Giiiiii...!?<br> ',
    'Đau... em xin lỗi‚ chị hai...<br>Em hơi bất cẩn...<br> ',
    'Đừng xin lỗi nữa! Được rồi‚ em lui ra sau đi!<br>Chị sẽ bảo vệ cả hai người!<br> ',
    'Viera‚ Verisa...!<br>Tại sao hai người lại làm đến mức đó...!<br> ',
    '(...Không. Chuyện đó mình đã hiểu từ lâu rồi...)<br> ',
    '(Vì là bạn bè... Viera và Verisa‚<br>chỉ vậy thôi cũng đủ để họ liều mạng chiến đấu...)<br> ',
    '(Có thể vượt quá giới hạn vì người kia... đó chính là bạn bè.<br>Nếu vậy thì――!)<br> ',
    'Nếu vậy... em cũng vậyyyyy――!!!<br> ',
    'Rầm――!! Wendy đạp vào xe kéo rồi bật nhảy.<br>Cô đáp xuống trước mặt Verisa và mọi người‚ chắn ngang lũ quái vật.<br> ',
    'Hả...!? Wendy!?<br>Không phải em không cử động được sao...!?<br> ',
    'Em cũng đã nghĩ vậy! Nhưng... kỳ lạ thật đấy.<br>Dù cơ thể rệu rã đến đâu... nếu là để bảo vệ bạn bè thì hình như em vẫn cử động được!<br> ',
    'Sức mạnh tình bạn là vô hạn...!<br>Powerーーーー!!!!<br> ',
    'Cơ thể vốn gần như không nghe lời bắt đầu chuyển động đáp lại ý chí của Wendy.<br>Nhưng đó không phải phép màu tiện lợi gì cả.<br> ',
    '(Cả người mình đang kêu răng rắc...! Cứ như sắp rã ra từng mảnh...!<br>――Nhưng mà!)<br> ',
    '...Lúc này chỉ cần chịu được tới kết tinh ma lực là đủ――!!<br> ',
    'Làm ơn... tránh raaaaaaa!<br> ',
    'Wendy bắt đầu chạy‚<br>hất văng những con quái vật chắn đường.<br> ',
    'Aha! Đúng là Wendy‚ sức mạnh ghê gớm thật đó~♪<br> ',
    'Bọn em sẽ mở đường!<br>Vì vậy cứ chạy tiếp‚ đừng quay đầu lại――<br> ',
    'Tiến lênnnnnnnnn――!!!<br> ',
    'Uwaaaaaaaaa～～～～～～!!<br> ',
    'Đòn tấn công của quái vật giáng xuống Wendy‚<br>nhưng cô vẫn chạy xuyên qua không dừng lại.<br> ',
    'Nhưng... cuộc tiến công ấy đột ngột kết thúc.<br> ',
    'A...!?<br> ',
    'Sự liều lĩnh không thể kéo dài. Chân Wendy mất lực‚ cô ngã nhào về phía trước.<br>Thế nhưng dù mặt lấm bùn‚ Wendy vẫn trừng mắt nhìn thẳng phía trước.<br> ',
    'Chỉ... một chút nữa thôi!<br>Em sẽ không bỏ cuộc... ở nơi này đâu!!<br> ',
    'Cô dùng sức cánh tay bò về phía kết tinh ma lực.<br>Hỏa lực yểm trợ của Verisa và mọi người quét ngã lũ quái vật lao vào sau lưng cô.<br> ',
    '(Làm ơn‚ cử động đi... cơ thể của mình!<br>Chỉ còn một chút nữa thôi...!)<br> ',
    'Verisa và Viera... những người bạn quý giá đã<br>liều mạng vì mình... giờ đến lượt mình...!!<br> ',
    'Bàn tay Wendy vươn tới kết tinh ma lực.<br> ',
    'Gigigigiiーーー!!<br> ',
    'Một số lượng quái vật mà ngay cả ma pháp của Verisa và mọi người cũng không xử lý kịp<br>đồng loạt lao vào lưng cô.<br> ',
    'Không được...! Không bắn hạ hết được...!<br> ',
    'Wendyyyyーーーー!<br> ',
    'Bóng dáng Wendy biến mất giữa lũ quái vật.<br>Trước sức mạnh số lượng áp đảo‚ cô gái Automata bị giẫm nát――<br> ',
    '――Tương lai tuyệt vọng ấy bị ánh sáng ma lực<br>chói lòa thổi bay.<br> ',
    '............<br> ',
    'Wendy!<br>Wendy!<br> ',
    'Verisa‚ Viera... em xin lỗi vì đã khiến hai người lo lắng.<br>Nhưng――giờ em ổn rồi! Không hiểu sao hiện tại em thấy mình sung sức tuyệt đỉnh!!<br> ',
    'Trước hết... phải phạt các bạn quái vật một chút nhỉ.<br>Quái vật dám bắt nạt những người bạn quý giá của em thì～～... thế này này!<br> ',
    'Wendy chộp hai con quái vật gần đó bằng hai tay‚<br>rồi bắt đầu vung chúng quay mòng mòng thật hoành tráng!<br> ',
    'Nhận lấyyyyyyyy～～～～～～～～!!<br> ',
    'Gigii～～～～～!?<br> ',
    'Wendy hóa thành một cơn lốc xoáy‚<br>quét sạch lũ quái vật hết con này đến con khác.<br> ',
    'Ahahaha! Em ấy quậy tưng bừng luôn kìa～～!<br>Viera‚ tụi mình cũng không thể thua được! Em còn chiến được chứ!?<br> ',
    'Vâng‚ chị hai!<br>Cho chúng thấy sức mạnh tiềm ẩn của hai chị em thân thiết mình nào!!<br> ',
    'Haaaaaaaaaaaaaaaaaaaa――!!<br> ',
    '――Ngày hôm đó‚ ma lực phình to ở tầng sâu Đại Huyệt mạnh đến mức bên ngoài huyệt cũng cảm nhận được‚<br>khiến Alicia suýt phái đội điều tra vì tưởng là sự cố bất thường.<br> ',
]

TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'(?:%[%sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nr t])')

def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def detect_newline(s):
    return 'CRLF' if '\r\n' in s else 'LF'

def text_field(line):
    if line.startswith('title,'):
        return line.split(',', 1)[1]
    if line.startswith('message,'):
        parts = line.split(',', 5)
        return parts[2]
    return None

def set_text_field(line, val):
    if line.startswith('title,'):
        return 'title,' + val
    parts = line.split(',', 5)
    parts[2] = val
    return ','.join(parts)

def tech_signature(line):
    if line.startswith('title,'):
        return ['title']
    parts = line.split(',', 5)
    return [parts[0], parts[1]] + parts[3:]

WORK.mkdir(parents=True, exist_ok=True)
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)

src_bytes = EN_ASSET.read_bytes()
bom = src_bytes.startswith(b'\xef\xbb\xbf')
text = src_bytes.decode('utf-8-sig')
newline = '\r\n' if '\r\n' in text else '\n'
lines = text.splitlines()
end_newline = text.endswith('\n')

records = [(i, line) for i, line in enumerate(lines) if line.startswith('title,') or line.startswith('message,')]
if len(records) != len(VI):
    raise SystemExit(f'VI entries {len(VI)} != records {len(records)}')
for idx, v in enumerate(VI):
    if ',' in v:
        raise SystemExit(f'ASCII comma in VI entry {idx}: {v!r}')

out_lines = list(lines)
entries = []
for n, ((line_idx, old_line), vi) in enumerate(zip(records, VI)):
    out_lines[line_idx] = set_text_field(old_line, vi)
    entries.append({
        'record_index': n,
        'asset_line': line_idx + 1,
        'record_type': old_line.split(',', 1)[0],
        'speaker': old_line.split(',', 5)[1] if old_line.startswith('message,') else None,
        'source_text_field': text_field(old_line),
        'vi_text_field': vi,
        'match_status': 'EXACT',
        'translation_status': 'TRANSLATED',
    })

out_text = newline.join(out_lines) + (newline if end_newline else '')
VI_ASSET.write_bytes((b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8'))

# QA
out_read = VI_ASSET.read_bytes().decode('utf-8-sig')
out_lines2 = out_read.splitlines()
blockers = []
items = []
if len(out_lines2) != len(lines):
    blockers.append({'type': 'LINE_COUNT', 'source': len(lines), 'output': len(out_lines2)})
if detect_newline(out_read) != detect_newline(text):
    blockers.append({'type': 'NEWLINE', 'source': detect_newline(text), 'output': detect_newline(out_read)})
if VI_ASSET.read_bytes().startswith(b'\xef\xbb\xbf') != bom:
    blockers.append({'type': 'BOM', 'source': bom, 'output': VI_ASSET.read_bytes().startswith(b'\xef\xbb\xbf')})

delimiter_mismatches = []
field_mismatches = []
technical_mismatches = []
tag_mismatches = []
placeholder_mismatches = []
ascii_comma_text = []
for i, (a, b) in enumerate(zip(lines, out_lines2), 1):
    if a.count(',') != b.count(','):
        delimiter_mismatches.append(i)
    if len(a.split(',')) != len(b.split(',')):
        field_mismatches.append(i)
    if (a.startswith('title,') or a.startswith('message,')):
        if tech_signature(a) != tech_signature(b):
            technical_mismatches.append(i)
        ta, tb = text_field(a), text_field(b)
        if TAG_RE.findall(ta) != TAG_RE.findall(tb):
            tag_mismatches.append(i)
        if PH_RE.findall(ta) != PH_RE.findall(tb):
            placeholder_mismatches.append(i)
        if ',' in tb:
            ascii_comma_text.append(i)

for name, vals in [
    ('DELIMITER_COUNT', delimiter_mismatches),
    ('FIELD_COUNT', field_mismatches),
    ('TECHNICAL_FIELDS', technical_mismatches),
    ('TAG_MISMATCH', tag_mismatches),
    ('PLACEHOLDER_MISMATCH', placeholder_mismatches),
    ('ASCII_COMMA_IN_TRANSLATED_TEXT', ascii_comma_text),
]:
    if vals:
        blockers.append({'type': name, 'lines': vals[:50], 'count': len(vals)})

qa = {
    'scene': SCENE,
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'qa_status': 'PASS' if not blockers else 'FAIL',
    'blockers': blockers,
    'items': items,
    'notes': [
        'JP was used as primary source; EN asset was used for ordered alignment/reference.',
        'No H-18/adult-uncertain content detected in this asset.',
        'No UNMATCHED or AMBIGUOUS records; all candidate title/message records translated.',
        'ASCII comma is forbidden inside translated text fields; Vietnamese internal commas use U+201A where needed.'
    ],
    'checks': {
        'source_line_count': len(lines),
        'output_line_count': len(out_lines2),
        'candidate_records': len(records),
        'translated_records': len(VI),
        'delimiter_mismatch_count': len(delimiter_mismatches),
        'field_mismatch_count': len(field_mismatches),
        'technical_mismatch_count': len(technical_mismatches),
        'tag_mismatch_count': len(tag_mismatches),
        'placeholder_mismatch_count': len(placeholder_mismatches),
        'ascii_comma_text_count': len(ascii_comma_text),
    }
}

manifest = {
    'scene': SCENE,
    'timestamp_utc': qa['timestamp_utc'],
    'sources': {
        'ja_json': str(JA_JSON),
        'en_json': str(EN_JSON),
        'en_asset': str(EN_ASSET),
        'vi_asset': str(VI_ASSET),
    },
    'source_properties': {
        'en_asset_bytes': len(src_bytes),
        'en_asset_sha256': hashlib.sha256(src_bytes).hexdigest(),
        'bom_utf8': bom,
        'newline': detect_newline(text),
        'line_count': len(lines),
        'candidate_records': len(records),
        'title_records': sum(1 for _, l in records if l.startswith('title,')),
        'message_records': sum(1 for _, l in records if l.startswith('message,')),
    },
    'output_properties': {
        'vi_asset_bytes': VI_ASSET.stat().st_size,
        'vi_asset_sha256': sha256(VI_ASSET),
        'line_count': len(out_lines2),
    },
    'entries': entries,
    'qa_status': qa['qa_status'],
}

(WORK / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK / 'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

old_focus = [f'{i+1}: {line}\n' for i, line in records]
new_focus = [f'{i+1}: {out_lines[i]}\n' for i, _ in records]
diff = difflib.unified_diff(old_focus, new_focus, fromfile='en_asset_translatable_records', tofile='vi_asset_translatable_records', lineterm='')
(WORK / 'focused_diff.md').write_text('# Focused Diff: evs_10200010701 translatable records\n\n```diff\n' + '\n'.join(diff) + '\n```\n', encoding='utf-8')

print(json.dumps({
    'qa_status': qa['qa_status'],
    'blockers': blockers,
    'vi_asset': str(VI_ASSET),
    'manifest': str(WORK / 'manifest.json'),
    'qa_log': str(WORK / 'qa_log.json'),
    'focused_diff': str(WORK / 'focused_diff.md'),
    'translated_records': len(VI),
    'line_count': len(out_lines2),
    'sha256': sha256(VI_ASSET),
}, ensure_ascii=False, indent=2))
if blockers:
    raise SystemExit(2)
