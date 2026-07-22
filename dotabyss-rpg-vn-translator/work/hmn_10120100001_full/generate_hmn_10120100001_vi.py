# -*- coding: utf-8 -*-
import json, hashlib, re, difflib
from pathlib import Path
from datetime import datetime, timezone

scene = 'hmn_10120100001'
root = Path('E:/AgentTranslation')
work = root / 'dotabyss-rpg-vn-translator' / 'work' / f'{scene}_full'
work.mkdir(parents=True, exist_ok=True)
ja_path = root / 'dotabyss-translation-main' / 'translations' / 'novels' / scene / 'ja.json'
en_json_path = root / 'dotabyss-translation-main' / 'translations' / 'novels' / scene / 'en.json'
en_asset_path = root / 'Translation' / 'en' / 'RedirectedResources' / 'assets' / 'unnamed_assetbundle' / f'{scene}.txt'
vi_asset_path = root / 'Translation' / 'vi' / 'RedirectedResources' / 'assets' / 'unnamed_assetbundle' / f'{scene}.txt'

TEXT_COMMANDS = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

def read_bytes(p):
    return p.read_bytes()

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def detect_newline(b):
    if b'\r\n' in b:
        return '\\r\\n', '\r\n'
    return '\\n', '\n'

def has_bom(b):
    return b.startswith(b'\xef\xbb\xbf')

def text_index(parts):
    cmd = parts[0]
    if cmd == 'title': return 1
    if cmd in {'message', 'messageTextUnder', 'messageTextCenter'}: return 2
    return None

def split_line(line):
    return line.split(',')

tag_re = re.compile(r'<[^>]+>')
placeholder_re = re.compile(r'(%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\$\{[^}]+\}|%%)')

def tags(s): return tag_re.findall(s)
def placeholders(s): return placeholder_re.findall(s)

translations = [
    "Em Vô Dụng Lắm!",
    "Được rồi‚ hôm nay khu chợ cũng yên bình.<br>Biến động giá cả có vẻ vẫn nằm trong dự tính…<br> ",
    "Chào anh bạn Chỉ Huy!<br>Hôm nay thịt rẻ lắm‚ mua một ít không?<br> ",
    "Tôi đến đây để thị sát đấy.<br>Đừng coi tôi như khách đi mua đồ chứ.<br> ",
    "Hửm? Miếng thịt này rẻ thật.<br>Từ trước đến giờ đây là giá thấp nhất đấy.<br> ",
    "Ông chủ‚ có chuyện gì à?<br>Hay ở đâu đó thú hoang xuất hiện hàng loạt?<br> ",
    "Không không‚ đây là thịt do Đội Săn Bắt săn về.<br>Hình như lần này họ được mùa lớn lắm.<br> ",
    "Đội Săn Bắt à… tôi nhớ mình đã cấp phép.<br>Đó là đội do các thợ săn tập trung ở Căn Cứ Tiền Tuyến lập ra để đi săn nhỉ.<br> ",
    "Ừ. Bình thường là thợ săn‚ khi có việc thì là lính đánh thuê lão luyện.<br>Tay nghề xẻ thịt cũng tốt‚ độ tươi thì khỏi chê nhé?<br> ",
    "Vậy nên mới mua được với giá rẻ thế này à…<br>Đội Săn Bắt thật sự giỏi đấy.<br> ",
    "…A‚ ừm…<br> ",
    "Dù còn phải đề phòng quái vật‚<br>vậy mà vẫn săn được bên ngoài thì quả là đáng nể.<br> ",
    "…Xin lỗi ạ…<br> ",
    "Ngay cả thú hoang không phải quái vật cũng có nhiều con hung dữ.<br>Những người không chiến đấu được đều biết ơn Đội Săn Bắt đấy.<br> ",
    "Thịt… cho em thịt…<br> ",
    "Tức là họ vừa đảm bảo lương thực vừa giữ an toàn. Khoan đã‚<br>nếu vừa là thợ săn vừa là lính đánh thuê thì cũng có thể kiêm trinh sát…<br> ",
    "Cho em thịt! Làm ơn ạ!<br> ",
    "Uoá!?<br> ",
    "Ối?<br>Xin lỗi‚ tôi cản đường à?<br> ",
    "A‚ không ạ… em xin lỗi vì đã lớn tiếng.<br>Vậy‚ ừm‚ phần thịt…<br> ",
    "À‚ Etia đấy à!<br>Vẫn như mọi khi nhỉ‚ chờ ta chút nhé.<br> ",
    "Cảm ơn… ạ.<br> ",
    "Etia cũng đến mua đồ à?<br> ",
    "V-vâng.<br>Em được nhờ bổ sung lương thực…<br> ",
    "Em chăm chỉ thật đấy.<br>Hôm nay thịt rẻ. Em đến mua là đúng lúc rồi.<br> ",
    "A… vậy sao ạ…<br> ",
    "Etia có nghe chưa?<br>Chuyện này hình như là nhờ công lao của Đội Săn Bắt đấy.<br> ",
    "Hả… a‚ v-vậy sao ạ!<br>G-giúp được nhiều quá nhỉ!<br> ",
    "Đúng vậy. Hoạt động ngoài vùng hoang dã nguy hiểm rồi mang về cả đống con mồi.<br>Không phải tay nghề tầm thường đâu.<br> ",
    "Đ-đ-đúng thật nhỉ ạ.<br> ",
    "Ngay cả thú hoang không phải quái vật‚ nếu lơ là cũng có thể bị thương.<br>Người trong phố cũng rất biết ơn vì chúng được xử lý.<br> ",
    "Mọi người cũng vui vì chuyện đó…<br>Thật là tuyệt quá ạ!<br> ",
    "Công lao của Đội Săn Bắt nên được đánh giá cao hơn.<br>Thành viên ưu tú đến mức tôi muốn có dưới quyền mình đấy.<br> ",
    "N-nhiều đến vậy sao ạ… ehehe…<br> ",
    "Rồi‚ để cháu chờ rồi Etia.<br>Ta gói toàn phần ngon nhất đấy‚ nhớ cảm ơn mấy người Đội Săn Bắt hộ ta nhé.<br> ",
    "V-vâng‚ cảm ơn ông ạ.<br>Em sẽ chuyển lời cho mọi người!<br> ",
    "Đội Săn Bắt? Gì vậy Etia‚ thấy em vui như thế‚<br>hóa ra em cũng có liên quan đến Đội Săn Bắt à.<br> ",
    "A… chuyện đó‚ nếu nói là liên quan thì có lẽ cũng có liên quan… chăng?<br>Kiểu như có không khí là vậy mà cũng không hẳn là vậy… ạ…<br> ",
    "Nói gì thế! Etia là một thành viên của Đội Săn Bắt mà!<br>Lần săn này con bé cũng đi cùng đấy!<br> ",
    "Hể!?<br> ",
    "Etia nhút nhát này mà…!?<br>Anh ngạc nhiên đấy‚ em đang cố gắng lắm mà.<br> ",
    "K-không đâu‚ em chẳng làm được gì cả…<br> ",
    "Không không‚ ta nghe rồi nhé?<br>Con mồi to nhất là do Etia săn được đúng không?<br> ",
    "Ồ‚ vậy là lập công lớn rồi!<br> ",
    "Chuyện đó chỉ là ngẫu nhiên‚ hay tình cờ thôi ạ…<br> ",
    "Thật sự em chỉ như người đi kèm trong Đội Săn Bắt thôi mà!<br> ",
    "Đâu phải công việc dễ đến mức tình cờ cũng săn được con lớn‚ đúng không?<br>Em làm tốt lắm mà‚ ngẩng cao đầu lên đi.<br> ",
    "Ưư…<br> ",
    "Với tư cách Chỉ Huy của căn cứ này‚<br>anh cũng nên cảm ơn Etia vì đã cố gắng trong Đội Săn Bắt nhỉ.<br> ",
    "Ồ‚ nghe được đấy!<br>Thỉnh thoảng cũng phải cho bọn tôi thấy anh bạn làm việc chứ!<br> ",
    "Bây giờ tôi cũng đang làm việc mà!<br>Nói thế người ta lại hiểu lầm là tôi chẳng làm gì mất!<br> ",
    "Biết rồi mà! Mọi người đều mong anh bạn đến đấy nhé?<br>Bọn tôi cũng đâu thể đi theo một Chỉ Huy còn chưa từng thấy mặt!<br> ",
    "Ông đúng là khéo nói thật.<br>Nếu vậy thì tỏ ra tôn trọng tôi thêm chút đi.<br> ",
    "（…Quả nhiên Chỉ Huy cũng được mọi người trong phố yêu mến…）<br> ",
    "Dù sao thì Etia cũng làm rất tốt.<br>Cảm ơn em‚ từ giờ cũng nhờ em nhé.<br> ",
    "Ư! Em không cần lời cảm ơn đâu ạ!<br>Em vô dụng hết thuốc chữa mà!<br> ",
    "Sao vậy‚ em đâu cần khiêm tốn đến thế.<br> ",
    "Vì em chẳng làm được gì<br>xứng đáng để Chỉ Huy khen cả…!<br> ",
    "Em xin lỗi em xin lỗi‚<br>em xin lỗi vì một người như em lại ở trong Đội Săn Bắt!<br> ",
    "X-x-xin phép ạ!!!<br> ",
    "…Em ấy chạy đi với tốc độ khủng khiếp luôn.<br>Một thợ săn lão luyện lập công trong Đội Săn Bắt mà rốt cuộc sợ gì vậy nhỉ.<br> ",
    "Nói vậy chứ‚ Etia ở tuổi đó mà đã sánh vai với người lớn<br>làm việc trong Đội Săn Bắt rồi sao.<br> ",
    "Vừa có năng lực vừa có tương lai à…<br>Đúng là nhân tài tôi muốn có làm cấp dưới trực tiếp…<br> ",
    "—Chuyện là như vậy.<br>Tôi đang nghĩ có nên chiêu mộ Etia từ Đội Săn Bắt không.<br> ",
    "Từ Đội Săn Bắt ạ?<br>Nhắc mới nhớ‚ Đội Săn Bắt vừa nộp một đơn xin mới đấy ạ.<br> ",
    "Ồ? Cho tôi xem chút.<br> ",
    "…Ra vậy‚ đơn xin hoạt động bên ngoài à.<br> ",
    "Vâng‚ họ muốn tiến hành một cuộc săn quy mô lớn hơn trước…<br> ",
    "Từ trước đến giờ họ vẫn cho ra kết quả vững chắc‚ không có lý do gì để không cho phép.<br>Hơn nữa… chuyện này lại vừa khéo.<br> ",
    "Vậy xử lý là đã phê duyệt có được không ạ?<br> ",
    "Như vậy cũng được.<br>Nhưng phải kèm điều kiện.<br> ",
    "Viễn chinh quy mô lớn có thể kích thích Đại Huyệt‚<br>nên ta sẽ giới hạn phạm vi hoạt động… chẳng hạn vậy ạ?<br> ",
    "Không‚ phần đó cứ để họ tự do.<br>Đội Săn Bắt có vẻ rất lão luyện‚ chắc họ cũng đã tính đến vài sự cố rồi.<br> ",
    "…Vậy điều kiện là gì ạ?<br> ",
    "Đơn giản thôi.<br>Tôi cũng sẽ đi cùng chuyến săn của Đội Săn Bắt!<br> ",
    "Chỉ Huy… quả nhiên anh ấy tuyệt thật…<br> ",
    "Lúc nào cũng tự tin‚ được mọi người công nhận‚ được yêu mến…<br> ",
    "Nếu mình cũng có thể trở nên giống Chỉ Huy…<br> ",
    "Ồ‚ Etia đấy à.<br>Nghe chưa‚ chuyến săn tiếp theo đã được cấp phép rồi.<br> ",
    "A… tốt quá rồi ạ!<br>Mọi người cố gắng nhé!<br> ",
    "Tất nhiên cô cũng đi cùng.<br>Lần sau tôi cũng kỳ vọng ở cô đấy!<br> ",
    "Hể!? <br>Rốt cuộc em cũng phải đi ạ…!?<br> ",
    "Tất nhiên rồi. À‚ lần này nghe nói đích thân Chỉ Huy sẽ đến thị sát‚<br>nên cả việc hộ vệ bên đó cũng nhờ cô nhé.<br> ",
    "H-hảảảảảảảả!?<br> ",
]

# validate source availability
for p in [ja_path, en_json_path, en_asset_path]:
    if not p.exists():
        raise FileNotFoundError(p)

src_bytes = read_bytes(en_asset_path)
newline_label, newline = detect_newline(src_bytes)
encoding = 'utf-8-sig' if has_bom(src_bytes) else 'utf-8'
src_text = src_bytes.decode(encoding)
lines = src_text.splitlines(keepends=True)
line_bodies = [ln[:-len(newline)] if ln.endswith(newline) else ln for ln in lines]
final_has_newline = bool(lines and lines[-1].endswith(newline))

records = []
cmd_counts = {cmd: 0 for cmd in sorted(TEXT_COMMANDS)}
for i, body in enumerate(line_bodies, 1):
    parts = split_line(body)
    if parts and parts[0] in TEXT_COMMANDS:
        idx = text_index(parts)
        records.append({'line': i, 'cmd': parts[0], 'field_index': idx, 'source_text': parts[idx], 'delimiter_count': body.count(',')})
        cmd_counts[parts[0]] += 1

if len(translations) != len(records):
    raise SystemExit(f'translations {len(translations)} != records {len(records)}')

out_bodies = list(line_bodies)
qa_records = []
def normalize_br_count(vi, expected_count):
    # EN asset text field is authoritative for <br> count. If JP-shaped VI has
    # surplus line breaks, collapse earliest breaks to spaces while keeping the
    # final UI break(s). If a short VI line is missing a required trailing break,
    # add it at the end.
    current = vi.count('<br>')
    while current > expected_count:
        vi = vi.replace('<br>', ' ', 1)
        current -= 1
    while current < expected_count:
        if vi.endswith(' '):
            vi = vi[:-1] + '<br> '
        else:
            vi = vi + '<br>'
        current += 1
    return vi

for rec, vi in zip(records, translations):
    vi = normalize_br_count(vi, rec['source_text'].count('<br>'))
    # no ASCII comma in translated text fields
    if ',' in vi:
        raise SystemExit(f'ASCII comma in VI translation for line {rec["line"]}: {vi}')
    if tags(vi) != tags(rec['source_text']):
        raise SystemExit(f'tag mismatch at line {rec["line"]}: {tags(rec["source_text"])} != {tags(vi)}')
    if placeholders(vi) != placeholders(rec['source_text']):
        raise SystemExit(f'placeholder mismatch at line {rec["line"]}')
    parts = split_line(out_bodies[rec['line']-1])
    parts[rec['field_index']] = vi
    new_body = ','.join(parts)
    if new_body.count(',') != rec['delimiter_count']:
        raise SystemExit(f'delimiter mismatch at line {rec["line"]}')
    out_bodies[rec['line']-1] = new_body
    qa_records.append({
        'line': rec['line'], 'cmd': rec['cmd'], 'status': 'TRANSLATED',
        'source_text': rec['source_text'], 'vi_text': vi,
        'tags_preserved': tags(vi) == tags(rec['source_text']),
        'placeholders_preserved': placeholders(vi) == placeholders(rec['source_text']),
        'delimiter_count': rec['delimiter_count']
    })

out_text = newline.join(out_bodies)
if final_has_newline:
    out_text += newline
vi_asset_path.parent.mkdir(parents=True, exist_ok=True)
vi_asset_path.write_bytes((('\ufeff' if has_bom(src_bytes) else '') + out_text).encode('utf-8'))

out_bytes = read_bytes(vi_asset_path)
# structural QA
out_lines = out_text.splitlines(keepends=True)
structural_errors = []
if len(out_lines) != len(lines): structural_errors.append('line_count_mismatch')
for idx, (src_body, out_body) in enumerate(zip(line_bodies, out_bodies), 1):
    if src_body.count(',') != out_body.count(','):
        structural_errors.append(f'comma_delimiter_count_mismatch_line_{idx}')
    sp = split_line(src_body); op = split_line(out_body)
    if len(sp) != len(op):
        structural_errors.append(f'field_count_mismatch_line_{idx}')
    if sp and sp[0] in TEXT_COMMANDS:
        ti = text_index(sp)
        for fi, (a, b) in enumerate(zip(sp, op)):
            if fi != ti and a != b:
                structural_errors.append(f'non_text_field_changed_line_{idx}_field_{fi}')
    elif src_body != out_body:
        structural_errors.append(f'non_text_line_changed_{idx}')

# focused diff only text records
focus_src = [f"{r['line']}:{r['cmd']}:{r['source_text']}" for r in records]
focus_out = [f"{r['line']}:{r['cmd']}:{r['vi_text']}" for r in qa_records]
diff = '\n'.join(difflib.unified_diff(focus_src, focus_out, fromfile='EN asset text fields', tofile='VI asset text fields', lineterm='')) + '\n'
(work / 'focused_diff.md').write_text('# Focused Diff: hmn_10120100001\n\n```diff\n' + diff + '```\n', encoding='utf-8')

manifest = {
    'scene': scene,
    'created_at': datetime.now(timezone.utc).isoformat(),
    'source_paths': {'ja_json': str(ja_path), 'en_json': str(en_json_path), 'en_asset': str(en_asset_path)},
    'output_path': str(vi_asset_path),
    'workdir': str(work),
    'source_hashes': {'ja_json_sha256': sha256(read_bytes(ja_path)), 'en_json_sha256': sha256(read_bytes(en_json_path)), 'en_asset_sha256': sha256(src_bytes)},
    'output_hashes': {'vi_asset_sha256': sha256(out_bytes)},
    'format': {'encoding': encoding, 'bom': has_bom(src_bytes), 'newline': newline_label, 'line_count': len(lines), 'final_newline': final_has_newline, 'delimiter': ','},
    'text_commands': cmd_counts,
    'text_record_count': len(records),
    'translated_record_count': len(qa_records),
    'mapping_status_counts': {'TRANSLATED': len(qa_records), 'UNMATCHED': 0, 'AMBIGUOUS': 0, 'REVIEW': 0},
    'structural_errors': structural_errors,
    'status': 'PASS' if not structural_errors else 'FAIL',
    'notes': ['JP primary; EN asset used for alignment.', 'Speaker names and charaload names preserved.', 'ASCII commas avoided inside Vietnamese text fields.']
}
qa_log = {
    'scene': scene,
    'qa_status': manifest['status'],
    'structural_qa': {
        'line_count_equal': len(out_lines) == len(lines),
        'delimiter_counts_equal': not any('delimiter' in e for e in structural_errors),
        'field_counts_equal': not any('field_count' in e for e in structural_errors),
        'non_text_fields_preserved': not any('non_text' in e for e in structural_errors),
        'tag_placeholder_preserved': True,
        'bom_preserved': has_bom(src_bytes) == has_bom(out_bytes),
        'newline_preserved': detect_newline(out_bytes)[0] == newline_label,
        'errors': structural_errors,
    },
    'linguistic_qa': {
        'title_case_title': translations[0],
        'commander_term': 'Commander/司令官 translated as Chỉ Huy where used as title; pronouns localized by context.',
        'character_voice': 'Etia timid/self-effacing; merchant casual; Alicia formal assistant; female hunter direct.',
        'h18': 'No H18 content in this scene.'
    },
    'records': qa_records,
    'issues': []
}
(work / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(work / 'qa_log.json').write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': manifest['status'], 'records': len(records), 'cmd_counts': cmd_counts, 'output': str(vi_asset_path), 'workdir': str(work)}, ensure_ascii=False, indent=2))
