from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

SCENE = 'evs_10200010601'
ROOT = Path('E:/AgentTranslation')
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/evs_10200010601_full'
WORK.mkdir(parents=True, exist_ok=True)

translations = [
    'Tiêu Đề',
    'Verisa và Viera tiến sâu trong Đại Huyệt với Wendy nằm trên<br>xe kéo. Con đường hiểm trở‚ mồ hôi thấm trên trán cả hai.<br> ',
    'Hộc... hộc... hộc...!<br> ',
    'Verisa... cô có ổn không...?<br> ',
    'C-cỡ này thì dư sức với tôi mà~.<br>Wendy cứ nằm yên nghỉ đi‚ đừng bận tâm lung tung nữa~.<br> ',
    'Đúng vậy đó! Nếu em và chị gái<br>hợp sức bằng tình yêu chị em‚ thì mạnh cả triệu mã lực luôn...!<br> ',
    'Quan trọng hơn là còn lâu mới tới chỗ kết tinh‚<br>nên Wendy mới phải cố lên đó nha~?<br> ',
    '(Cả hai rõ ràng đâu có ổn...<br>Họ chỉ đang lo cho mình thôi...)<br> ',
    '(...Mình không thể cứ được mọi người động viên mãi.<br>Giá mà mình cũng làm được gì đó cho hai người họ...)<br> ',
    'Phù... Viera‚ giờ mình tới đâu rồi~?<br> ',
    'Theo bản đồ Adelheid đưa cho chúng ta... thì đã đi được khoảng một nửa rồi.<br> ',
    'Gì chứ‚ nhẹ hơn tôi tưởng đó♪<br>Wendy‚ chịu khó thêm chút nữa thôi nha~.<br> ',
    'Vâng... cảm ơn Verisa‚ Viera.<br>...Hai người thật sự không cần nghỉ một chút sao?<br> ',
    'Nếu được thì em cũng muốn vậy‚ nhưng ở độ sâu này chắc nguy hiểm sẽ càng nhiều hơn.<br>Có khi đi một mạch qua đây lại an toàn hơn.<br> ',
    'Ừ nhỉ~. Trong Đại Huyệt này chẳng biết thứ gì sẽ nhảy ra tấn công đâu...<br> ',
    'Đúng lúc đó‚ một âm thanh sột soạt khó chịu<br>rung lên bên tai cả ba người.<br> ',
    '--! Vừa nhắc đã tới rồi sao.<br>Hai người cẩn thận! Có thứ gì đang nấp trong bụi cây kia!<br> ',
    'Vâng‚ chị!<br>...Ơ? Bụi cây... ở nơi như thế này sao...?<br> ',
    'Chờ đã! Cơ thể em không cử động được‚ nhưng<br>nếu khởi động được cảm biến ma đạo thì...!<br> ',
    '--Cái này...!?<br>Hai người mau tránh xa nó ra!<br> ',
    'Hả... thứ này không phải đang nấp trong bụi cây mà là...<br> ',
    'Bản thân đám cây đang chuyển động!<br> ',
    'Ngay sau đó--vô số dây gai phóng ra từ bụi rậm‚<br>vươn dài như rắn và tấn công cả ba người!<br> ',
    'Mấy thứ này cứ để ngọn lửa của tôi thiêu sạch~~!<br>Haaaaaa!<br> ',
    'Ma pháp lửa của Verisa đánh thẳng vào những dây gai đang lao tới.<br>Chúng bốc cháy‚ mất đà rồi vụn ra thành tro.<br> ',
    'Lêu lêu~ yếu xìu~ cây cỏ phế vật~.<br>Hãy khắc sức mạnh của Verisa-chan vào mắt các ngươi... à mà‚ đâu có mắt nhỉ.<br> ',
    'Đây là loài thực vật bị biến đổi do ảnh hưởng của Đại Huyệt.<br>Theo dữ liệu của em‚ chúng có tập tính bắt con mồi rồi hút ma lực.<br> ',
    'Hừm~.<br>Nếu không phải quái vật mà chỉ là cây thôi‚ nghĩa là chúng yếu trước lửa hả?<br> ',
    'Vâng. Tuy nhiên chúng có vẻ kháng lạnh rất mạnh‚<br>nên có lẽ cần chú ý điểm đó...<br> ',
    'Ra vậy...!<br>Đúng là Wendy! Đáng tin cậy quá!<br> ',
    'Đúng là hỗ trợ viên xịn ghê~♪ Dù sao thì‚ chỉ cần thiên tài ma pháp<br>Verisa-chan ở đây‚ chặng đường phía trước cũng dễ như ăn bánh thôi♪<br> ',
    '(May quá... tuy cơ thể không thể cử động‚<br>nhưng mình vẫn có thể giúp ích cho họ. Cứ tiếp tục dò địch--)<br> ',
    'A...!<br>À‚ hai người... nhìn kìa...!<br> ',
    'Hửm~? Gì vậy‚ Wendy?<br>Nếu là cây ma nữa thì tôi sẽ thiêu rụi hết--<br> ',
    'Verisa và Viera nhìn theo hướng Wendy chỉ rồi trợn mắt kinh hãi.<br>Ở đó--hơn một trăm dây gai đang ngóc đầu như rắn chực tấn công.<br> ',
    'C-cái này thì đúng là hơi...<br> ',
    'V-Viera!! Dựng tường băng bảo vệ Wendy!!<br> ',
    'Vâng...!<br> ',
    'Những dây gai nhắm vào Wendy không thể cử động<br>bị bức tường băng do Viera tạo ra chặn lại.<br> ',
    'Tốt‚ cứ chặn chúng như vậy!<br>Phần còn lại để tôi... tôi sẽ thiêu sạch tất cả~~!!<br> ',
    'Hộc‚ hộc‚ hộc...! Rốt cuộc tụi này có bao nhiêu vậy hả~!?<br>Yếu xìu mà chỉ được cái đông thôi~~!<br> ',
    'Các dây gai lần lượt bị ma pháp của Verisa thiêu rụi‚ nhưng số lượng quá nhiều.<br>Vẻ mệt mỏi dần hiện rõ trên khuôn mặt Verisa.<br> ',
    'Bên này cũng đông quá‚ em không thể chống thêm nữa...!<br> ',
    'Viera cũng đáp trả bằng các bức tường băng‚<br>nhưng dường như cô đã hết sức chỉ để chặn những đợt gai tấn công từ mọi hướng.<br> ',
    '(Phải làm sao đây... cứ thế này thì hai người họ--!<br>Nếu mình gửi tín hiệu cầu cứu ai đó ở căn cứ tiền tuyến--!)<br> ',
    '(Nhưng gửi cho ai...? Chỉ Huy cũng không có ở đây...<br>Ngoài Verisa và Viera ra‚ mình đâu còn người bạn nào có thể dựa vào...)<br> ',
    'Ư‚ hết... theo‚ không kịp nữa...!<br>Cứ thế này ma lực của tôi sẽ...!<br> ',
    'Chị ơi!<br>Ư‚ đúng là băng không hiệu quả mấy...!<br> ',
    '--! Làm ơn...!<br>Ai đó...! Ai đó cứu hai người họ với--!<br> ',
    '--Để đó cho tôi!!<br> ',
    'Một giọng nói trong trẻo mà kiên định đáp lại lời cầu xin của Wendy. Ngay sau đó‚<br>ai đó lao vào nhanh như gió lốc‚ vung lưỡi kiếm chém gọn hàng loạt dây gai.<br> ',
    'Gì vậy!? Chuyện gì vừa xảy ra thế~~!?<br> ',
    'Suýt thì nguy rồi nhỉ.<br>Nhưng một khi tôi đã tới‚ thì không còn gì phải lo nữa!<br> ',
    'Raveria!? Sao cô lại...!?<br> ',
    'Tôi nghe tình hình từ Adelheid nên vội đuổi theo.<br>Dù sao Wendy cũng từng cùng tôi luyện tập mà.<br> ',
    '...Hả? Chỉ vì chuyện đó... mà cô tới cứu chúng tôi sao?<br> ',
    'Hừm. Nghe cô nói vậy thì‚ đúng là còn một lý do nữa.<br> ',
    'Tôi nghe nói cô đang cố gắng vì Chỉ Huy.<br>Một người như cô khiến tôi thấy rất thích. Lý do vậy là đủ rồi.<br> ',
    'R-Raveria...! Cảm ơn cô rất nhiều!!<br> ',
    'Thật là‚ làm màu dữ ha... sao lại canh đúng lúc thế không biết.<br>Nhưng đã tới rồi thì phải làm việc cho đàng hoàng đó nha~?<br> ',
    'Tất nhiên rồi.<br>Cứ để chỗ này cho chúng tôi‚ hai người nghỉ đi.<br> ',
    'Nghỉ á...? Cô định một mình xử lý ngần này dây gai sao?<br> ',
    'Hừ. Tôi đâu có nói--là một mình.<br> ',
    'Đượ~~c rồi! Cuối cùng cũng đuổi kịp!<br> ',
    'Ôi chà... vừa tới đã gặp tình huống căng thật đấy.<br> ',
    'Honoka!? Cả các binh sĩ nữa sao!?<br> ',
    'Bọn tôi nghe Wendy-chan đang gặp nguy!<br>Nên tới chi viện đây!<br> ',
    'Trả ơn người đã giúp mình là chuyện đương nhiên mà!<br>Honoka-chan‚ trong lúc bọn tôi cùng Raveria cầm chân dây gai!<br> ',
    'Cứ giao cho tôi! Nào‚ sửa nhanh thứ này thôi~~!<br> ',
    'Honoka cầm dụng cụ chạy tới bên xe kéo<br>và bắt đầu mày mò thứ gì đó.<br> ',
    'Honoka...? Cô đang làm gì vậy?<br> ',
    'Tôi đang cải tạo nó đó! Tôi sẽ làm cho chiếc xe kéo này trở nên vù vù~~~ rồi<br>vèo vèo~~~~ xong lại rầm rầm rầm~~~~!<br> ',
    'Tôi hoàn toàn không hiểu gì hết!<br>Ai đó làm ơn phiên dịch giúp với...!<br> ',
    'Ừm... hình như cô ấy đang giúp nó chạy nhanh hơn...?<br>Em rất biết ơn‚ nhưng... sao mọi người lại làm tới mức này?<br> ',
    'Hôm trước được rèn đồ cùng cô vui lắm! Ở cạnh nhau mà vui<br>thì là bạn bè! Bạn bè thì phải giúp đỡ lẫn nhau chứ~!<br> ',
    'Bạn bè...<br> ',
    'Tốt‚ bên này chúng tôi đã giảm bớt số lượng rồi!<br>Bây giờ có thể đột phá!<br> ',
    'Mọi người‚ lối này!<br>Có đường tắt!<br> ',
    'Ở chỗ này lại có đường nhánh sao... tôi không biết đấy.<br> ',
    'Đi qua đây là sẽ tới thẳng đích trong chớp mắt!<br>Bọn tôi sẽ tiếp tục cùng Raveria thu hút dây gai!<br> ',
    'Cảm ơn mọi người! Xin hãy bảo trọng!<br> ',
    'Các cô nhất định cũng phải tới dự tiệc đó nha~!<br> ',
    'Bên này cũng cải tạo xong rồi!<br>Nào nào‚ Verisa và Viera cũng lên xe đi! Chúng ta lao một mạch nào!<br> ',
    'Như thế này sao?<br> ',
    'Lên thì được thôi‚ nhưng rốt cuộc nó sẽ làm gì hả~?<br> ',
    'Đi nào~!<br>FIRE~~~~~~~~~~!<br> ',
    'Honoka kích hoạt cơ cấu trên chiếc xe kéo đã cải tạo. Ngay sau đó‚ chiếc ống gắn ở phía sau<br>phun ra cột lửa‚ khiến xe kéo tăng tốc dữ dội và lao vào đường nhánh--!<br> ',
    'A-ba-ba-ba-ba-ba-ba-ba...!<br>N-nếu nhanh tới mức này thì phải nói trước chứ~~~...!<br> ',
    'Ahaha... tốc độ này thì sẽ tới nơi trong nháy mắt thôi.<br> ',
    'Nói mới nhớ... Wendy thật sự được mọi người quý mến nhỉ.<br> ',
    'Ừ nhỉ~. Có vẻ bạn của cô không chỉ còn mỗi bọn tôi nữa rồi.<br>Fufu‚ nổi tiếng quá ha‚ Wendy♪<br> ',
    '...Vâng!<br>Mọi người đều là những người bạn tuyệt vời!<br> ',
]

adult_uncertain_indices = []

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def read_bytes(path):
    return path.read_bytes()

def split_line(line):
    # raw line without newline
    return line.split(',')

def text_field_index(fields):
    if fields[0] == 'title':
        return 1
    if fields[0] == 'message':
        return 2
    return None

tag_re = re.compile(r'<[^>]+>')
placeholder_re = re.compile(r'%(?:\d+\$)?[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]|%%')

def tags(s): return tag_re.findall(s)
def placeholders(s): return placeholder_re.findall(s)

en_bytes = read_bytes(EN_ASSET)
source_hash = sha256_bytes(en_bytes)
has_bom = en_bytes.startswith(b'\xef\xbb\xbf')
text = en_bytes.decode('utf-8-sig')
newline = '\r\n' if '\r\n' in text else '\n'
ends_newline = text.endswith('\n')
lines = text.splitlines()

with JA_JSON.open('r', encoding='utf-8') as f: ja = json.load(f)
with EN_JSON.open('r', encoding='utf-8') as f: en = json.load(f)
ja_items = list(ja.items())
en_items = list(en.items())
assert len(ja_items) == len(en_items) == len(translations), (len(ja_items), len(en_items), len(translations))

candidate_positions = [i for i,l in enumerate(lines) if l.startswith('title,') or l.startswith('message,')]
assert len(candidate_positions) == len(translations), (len(candidate_positions), len(translations))

out_lines = list(lines)
entries = []
blockers = []
items = []
notes = []

for n, (pos, vi) in enumerate(zip(candidate_positions, translations)):
    line = lines[pos]
    fields = split_line(line)
    idx = text_field_index(fields)
    if idx is None:
        blockers.append({'line': pos+1, 'issue': 'candidate_without_text_field'})
        continue
    old_text = fields[idx]
    if ',' in vi:
        blockers.append({'line': pos+1, 'issue': 'ASCII comma in VI translation', 'vi': vi})
    # title no tag constraint; message preserve tag/placeholder counts exactly
    if tags(old_text) != tags(vi):
        blockers.append({'line': pos+1, 'issue': 'tag mismatch in translated field', 'source_tags': tags(old_text), 'vi_tags': tags(vi)})
    if placeholders(old_text) != placeholders(vi):
        blockers.append({'line': pos+1, 'issue': 'placeholder mismatch in translated field', 'source_placeholders': placeholders(old_text), 'vi_placeholders': placeholders(vi)})
    new_fields = list(fields)
    new_fields[idx] = vi
    out_lines[pos] = ','.join(new_fields)
    entries.append({
        'index': n,
        'asset_line': pos+1,
        'record_type': fields[0],
        'speaker': fields[1] if fields[0] == 'message' else None,
        'jp': ja_items[n][0],
        'en_novel': en_items[n][1],
        'en_asset': old_text,
        'vi': vi,
        'match_status': 'EXACT',
        'translation_status': 'TRANSLATED' if n not in adult_uncertain_indices else 'REVIEW',
    })

out_text = newline.join(out_lines) + (newline if ends_newline else '')
out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
VI_ASSET.write_bytes(out_bytes)

# Structural QA
out_read = VI_ASSET.read_bytes()
out_text2 = out_read.decode('utf-8-sig')
out_lines2 = out_text2.splitlines()
if len(out_lines2) != len(lines):
    blockers.append({'issue': 'line_count_mismatch', 'source': len(lines), 'output': len(out_lines2)})
if out_read.startswith(b'\xef\xbb\xbf') != has_bom:
    blockers.append({'issue': 'bom_mismatch'})
if ('\r\n' if '\r\n' in out_text2 else '\n') != newline:
    blockers.append({'issue': 'newline_mismatch'})

for i, (src, out) in enumerate(zip(lines, out_lines2), start=1):
    if src.count(',') != out.count(','):
        blockers.append({'line': i, 'issue': 'delimiter_count_mismatch', 'source': src.count(','), 'output': out.count(',')})
    sf, of = split_line(src), split_line(out)
    if len(sf) != len(of):
        blockers.append({'line': i, 'issue': 'field_count_mismatch', 'source': len(sf), 'output': len(of)})
        continue
    if sf and sf[0] in ('title','message'):
        idx = text_field_index(sf)
        for j, (a,b) in enumerate(zip(sf, of)):
            if j != idx and a != b:
                blockers.append({'line': i, 'issue': 'technical_field_changed', 'field': j, 'source': a, 'output': b})
        if ',' in of[idx]:
            blockers.append({'line': i, 'issue': 'ASCII comma inside translated text field'})
        if tags(sf[idx]) != tags(of[idx]):
            blockers.append({'line': i, 'issue': 'tag_mismatch_postwrite', 'source_tags': tags(sf[idx]), 'output_tags': tags(of[idx])})
        if placeholders(sf[idx]) != placeholders(of[idx]):
            blockers.append({'line': i, 'issue': 'placeholder_mismatch_postwrite', 'source_placeholders': placeholders(sf[idx]), 'output_placeholders': placeholders(of[idx])})
    elif src != out:
        blockers.append({'line': i, 'issue': 'non_translatable_line_changed'})

# focused diff for translatable records only
src_focus = [f'{i+1}: {lines[i]}' for i in candidate_positions]
out_focus = [f'{i+1}: {out_lines2[i]}' for i in candidate_positions]
diff = '\n'.join(difflib.unified_diff(src_focus, out_focus, fromfile=str(EN_ASSET), tofile=str(VI_ASSET), lineterm='')) + '\n'
(WORK/'focused_diff.md').write_text('# Focused diff: translatable records only\n\n```diff\n' + diff + '```\n', encoding='utf-8')

qa_status = 'PASS' if not blockers else 'FAIL'
qa_log = {
    'scene': SCENE,
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'qa_status': qa_status,
    'blockers': blockers,
    'items': items,
    'notes': notes + ['No H-18/adult-uncertain content detected in this file.', 'JP used as primary source; EN asset used for alignment/reference.', 'ASCII comma is forbidden inside translated title/message fields; U+201A used where needed.'],
    'checks': {
        'line_count_match': len(out_lines2) == len(lines),
        'field_counts_match': not any(b.get('issue') == 'field_count_mismatch' for b in blockers),
        'delimiter_counts_match': not any(b.get('issue') == 'delimiter_count_mismatch' for b in blockers),
        'technical_fields_unchanged': not any(b.get('issue') == 'technical_field_changed' for b in blockers),
        'tags_preserved': not any('tag' in b.get('issue','') for b in blockers),
        'placeholders_preserved': not any('placeholder' in b.get('issue','') for b in blockers),
        'ascii_comma_absent_in_translated_fields': not any('ASCII comma' in b.get('issue','') for b in blockers),
        'bom_preserved': out_read.startswith(b'\xef\xbb\xbf') == has_bom,
        'newline_preserved': ('\r\n' if '\r\n' in out_text2 else '\n') == newline,
    }
}
(WORK/'qa_log.json').write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')

manifest = {
    'scene': SCENE,
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'paths': {
        'ja_json': str(JA_JSON),
        'en_json': str(EN_JSON),
        'en_asset': str(EN_ASSET),
        'vi_asset': str(VI_ASSET),
        'work_dir': str(WORK),
        'focused_diff': str(WORK/'focused_diff.md'),
        'qa_log': str(WORK/'qa_log.json'),
        'script': str(WORK/'generate_vi.py'),
    },
    'source': {
        'sha256': source_hash,
        'bytes': len(en_bytes),
        'bom': has_bom,
        'newline': 'CRLF' if newline == '\r\n' else 'LF',
        'line_count': len(lines),
        'candidate_records': len(candidate_positions),
    },
    'output': {
        'sha256': sha256_bytes(out_read),
        'bytes': len(out_read),
        'bom': out_read.startswith(b'\xef\xbb\xbf'),
        'line_count': len(out_lines2),
        'candidate_records': len([l for l in out_lines2 if l.startswith('title,') or l.startswith('message,')]),
    },
    'entries': entries,
    'qa_status': qa_status,
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status': qa_status, 'blocker_count': len(blockers), 'output': str(VI_ASSET), 'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'output_sha256': sha256_bytes(out_read)}, ensure_ascii=False, indent=2))
if blockers:
    raise SystemExit(1)
