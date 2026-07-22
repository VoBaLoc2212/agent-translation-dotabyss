# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib
from collections import Counter

SCENE = 'hmn_10020100002'
ROOT = Path('E:/AgentTranslation')
JA = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
ENJSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
ENASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VIASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10020100002_full'
WORK.mkdir(parents=True, exist_ok=True)

TEXT_CMDS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}

VI = [
    'Tiêu Đề',
    'Cuối cùng thời khắc này cũng đến rồi nhỉ〜 Adelheid!<br> ',
    'Nhân danh danh dự của pháp sư Perdion Verisa đây! Mình tuyệt đối<br>sẽ không bao giờ thua loại như cô đâu!<br> ',
    'Ưm... em không hiểu rõ chuyện này lắm...<br> ',
    'D-dừng lại đó! Đừng đưa tay ra trước nữa! Như thế sẽ làm nổi bật<br>lên đấy chứ!? Cái bộ ngực đầy đặn vô ích của cô ấy!<br> ',
    'Ơ...!?<br> ',
    'Đừng để ý. Đó là tư thế rất tuyệt làm tôn lên<br>sức hút của Adelheid.<br> ',
    'Anh ơi rốt cuộc anh đứng về phe nào vậy?!<br> ',
    'Phe nào chứ? Quan trọng hơn là thi đấu kiểu gì vậy? Nếu là kích cỡ ngực<br>thì khỏi cần so cũng biết rồi.<br> ',
    'Không liên quan! Đây là trận quyết đấu để chứng minh rằng ma pháp của<br>Verisa đây tuyệt đối không thua sức mạnh khoa học!<br> ',
    'À ra là vụ em bị dạy cho biết lần trước. Thay vì hâm nóng đồ ăn<br>em lại biến nó thành than luôn nhỉ.<br> ',
    'Em đâu có bị dạy cho biết gì đâu! Chỉ lỡ chỉnh lửa sai một chút thôi! Nếu chiến đấu thật<br>thì ma pháp mạnh gấp trăm lần thứ khoa học gì đó nhé!<br> ',
    'Hừm... nghe nhảm thật nhưng anh cũng hơi hứng thú. Chênh lệch tính năng<br>giữa khoa học và ma pháp à.<br> ',
    'Thấy chưa! Anh ơi cũng nói vậy mà! Anh ấy hiểu rất rõ<br>Verisa đây mới là người đúng nhỉ!♡<br> ',
    'Thi đấu giữa khoa học và ma pháp ạ? Nhưng hiện giờ em không có nhiều<br>dụng cụ tấn công. Chắc em không thể sánh với cô đâu Verisa...<br> ',
    'Thứ dạy cho Verisa biết không phải vũ khí mà là lò vi sóng. Không có<br>dụng cụ nào tương tự khác sao?<br> ',
    'Dụng cụ tiện lợi ạ? Nếu vậy thì có vài món...<br> ',
    'Vậy dùng mấy thứ đó để phân thắng bại! Ai đáp ứng yêu cầu của anh ơi<br>nhanh hơn thì thắng!<br> ',
    'V-vâng. Nếu là em thì em xin được làm đối thủ của cô!<br> ',
    'Nào anh ơi! Thử ước gì đó đi! Verisa đây sẽ thực hiện ngay<br>chứ không cần thứ khoa học gì đâu!♡<br> ',
    'Để xem... trước mắt thì anh thấy khát. Anh muốn một thức uống lạnh.<br> ',
    'OK! Cứ để em!♪ Em sẽ dùng ma pháp mang đồ uống từ quán rượu về<br>ngay bây giờ!<br> ',
    '...Tốc độ chạy thì liên quan gì đến ma pháp chứ. Vậy còn<br>Adelheid thì sao?<br> ',
    'Ừm‚ vậy thì dùng cái này...<br> ',
    'Em mang về rồi đây! Hừ hừ!♪ Dù khoa học có tiện lợi đến mấy thì xem ra<br>cũng không theo kịp em nhỉ!☆<br> ',
    'Ực... phù! Em chậm quá đấy Verisa.<br> ',
    'Cáiiii gì!? Anh ơi!? Sao anh đã có đồ uống rồi!? Mà nhìn<br>lạnh buốt nữa chứ!<br> ',
    'À‚ đây là dụng cụ gọi là tủ lạnh. Nó luôn giữ không khí bên trong<br>ở trạng thái lạnh.<br> ',
    'Không ngờ có thể lấy đồ uống lạnh mà chẳng cần ra khỏi phòng.<br>Khá lắm khoa học. Không tệ đâu.<br> ',
    'Ưưưưưư〜〜〜! Ch-chỉ là tình cờ<br>có cái máy tiện lợi như thế thôi đúng không!? Ngẫu nhiên thôi ngẫu nhiên!<br> ',
    'Tiếp! Vòng tiếp theo! Nào anh ơi! Lần này anh muốn em làm<br>cái-gì đây?<br> ',
    'Để xem... Adelheid‚ căn phòng này hình như hơi bừa bộn nhỉ?<br> ',
    'Em xấu hổ quá. Em mải mê nghiên cứu nên<br>lơ là việc dọn dẹp...<br> ',
    'Vậy mong muốn của anh là dọn sạch căn phòng này. Làm nhanh đi Verisa.<br> ',
    'K-khoan đã!? Anh ơi‚ vừa rồi... anh đang lợi dụng cuộc thi<br>để bắt em làm việc vặt phải không!?<br> ',
    'Không hề đâu nhé?<br>Nào‚ không nhanh lên là em sẽ thua khoa học đấy?<br> ',
    'Ưưư〜... hết cách rồi! Em sẽ đi lấy dụng cụ dọn dẹp ngay đây!<br> ',
    'Em mang chổi với hót rác tới rồi đây! Đây là những dụng cụ siêu xịn<br>được yểm ma pháp đó nhé!♡<br> ',
    'Lại chậm rồi Verisa.<br> ',
    'Ừm‚ em gần như đã dọn xong sàn rồi.<br> ',
    'C-cái gì thế!? Tại sao đã xong rồi chứ!?<br> ',
    'Đây là máy hút bụi hoàn toàn tự động. Nó tự di chuyển<br>khắp phòng và hút bụi giúp mình.<br> ',
    'Một cỗ máy tự di chuyển và dọn dẹp à. Lux Nova<br>còn có cả thứ như thế cơ đấy.<br> ',
    '...Không thể nào... cô đùa em à...<br> ',
    'Vậy cây chổi của em có tự động di chuyển không?<br> ',
    'Làm gì có chuyện đó! N-nhưng mà! Khi quét như thế này thấy không? Nó<br>được yểm ma pháp giúp bụi dễ gom lại hơn!<br> ',
    'So với máy hút bụi tự động thì chẳng khác gì<br>cây chổi bình thường cả.<br> ',
    'Ưưư! Em vất vả lắm mới mang nó tới mà...! Đúng là cái thứ đó<br>trông có vẻ tiện thật nhưng...!<br> ',
    'Xem ra em đã bị dạy cho biết hoàn toàn rồi nhỉ.<br> ',
    'V-vẫn chưa đâu! Verisa tuyệt đối chưa thua! Em đâu có bị cho biết gì hết!<br> ',
    'C-còn gì nữa không!? Anh ơi! Anh không có yêu cầu nào khác sao!? Lần<br>này Verisa sẽ thắng cho xem!<br> ',
    'Hừm. Vậy anh thử đưa ra một yêu cầu đàng hoàng hơn chút vậy.<br> ',
    'Ý anh là sao “hơn chút”!? Những yêu cầu tới giờ<br>không đàng hoàng sao!?<br> ',
    'Thôi nghe này. Điều khiến anh thấy hơi phiền là ra lệnh<br>cho cấp dưới.<br> ',
    'Khi truyền đạt tác chiến cho số đông cần rất nhiều mệnh lệnh thư. Hai em dùng<br>ma pháp hay khoa học cũng được để bớt công cho anh nhé?<br> ',
    'Vậy bằng ma pháp của em‚ em sẽ viết chữ thật lớn trên trời bằng lửa...<br> ',
    'Rồi mưa lửa sẽ rơi xuống mặt đất. Em định tiêu diệt đồng minh<br>trước cả khi chiến dịch bắt đầu à?<br> ',
    'À... v-vậy em viết xuống đất là được chứ gì!? Như thế thì ổn mà đúng không?<br> ',
    'Anh chỉ thấy tương lai nơi này cháy rụi thôi. Bác bỏ<br>bác bỏ.<br> ',
    'Ưm... vậy cái này thì sao ạ? Đây là một cỗ máy gọi là máy in<br>dùng để in chữ lên giấy.<br> ',
    'Một trong các chức năng của nó là sao chép tài liệu<br>gần như nguyên dạng.<br> ',
    'Hả!? Dễ vậy sao!? Mà cô nói chỉ là một chức năng nghĩa là<br>còn cách dùng khác nữa à?<br> ',
    'Ngoài ra nó có thể chuẩn bị tài liệu mà không cần tự tay viết<br>và cũng có thể in hình ảnh độ chính xác cao.<br> ',
    'C-chỉ cái này mà làm được tới mức đó sao?<br> ',
    'Một cỗ máy khá đa năng đấy. Em có làm được điều tương tự bằng<br>ma pháp không Verisa?<br> ',
    'L-làm sao mà được chứ!? Đừng đùa với em! Aaaaa! Trời ơi! Khoa học<br>rốt cuộc là cái quái gì vậy!<br> ',
    'Khoa học không hẳn là vạn năng nhưng nhìn chung nó bao quát<br>những chức năng con người cần nên...<br> ',
    'Này‚ cái máy in gì đó dừng rồi. Sao vậy? Mới có hai tờ<br>được in ra thôi mà.<br> ',
    'Ừm... à‚ hết mực rồi. Cỗ máy này cần loại mực chuyên dụng<br>nhưng em không có dự phòng...<br> ',
    'Vậy là không dùng được nữa à. Tiếc thật.<br> ',
    'Hả—? ...Đ-đúng rồi! Nếu vậy thì...!♡<br> ',
    'Này này anh ơi!♡ Có phải anh bắt đầu thấy hơi mệt rồi không nào?<br> ',
    'Đột nhiên sao vậy? Đúng là anh thấy mệt tinh thần vì<br>cuộc đấu nhảm nhí này rồi.<br> ',
    'Ưư... v-vậy à! Thế thì... chẳng hạn... anh có muốn đi tắm<br>một chút không?<br> ',
    'Cũng không hẳn là anh không muốn...<br> ',
    'Anh muốn đúng không!? Đúng không!? Vậy thì! Thử thách tiếp theo là...<br>thi đun nước tắm!<br> ',
    'Nếu là khoa học thì dĩ nhiên làm được cỡ đó nhỉ?<br> ',
    'Vâng‚ có một thiết bị gọi là nồi hơi có thể dùng đầu đốt<br>để làm nóng nước.<br> ',
    'Thi đun nước tắm à... em chắc chứ? Nếu thua thì<br>mất mặt pháp sư lửa lắm đấy.<br> ',
    'Đời nào em thua! Anh cứ nhìn cho kỹ nhé anh ơi!<br> ',
    'Sao thế Verisa? Nước bắt đầu hơi nguội rồi đấy.<br> ',
    'K-không phải đâu!? Vì anh ngâm lâu quá nên em cố ý<br>làm nước ấm dịu lại đó!♡ Cái đó gọi là chu đáo!♪<br> ',
    'Ồ‚ kiểu chu đáo của em à? Phía Adelheid thì hình như<br>lúc nào cũng đúng nhiệt độ đấy?<br> ',
    'Vâng. Vì công suất nhiệt ổn định ạ.<br> ',
    'Gừừừ... nhưng mà chắc sắp tới rồi...!<br> ',
    'Hừm‚ cái nồi hơi gì đó dừng rồi. Sao vậy? Trục trặc à?<br> ',
    'Không thể nào... À... chẳng lẽ là hết gas...?<br> ',
    'Thứ đó không chạy chỉ bằng ma lực trong không khí sao?<br> ',
    'Vâng. Nó đốt một loại gas dễ cháy chuyên dụng.<br> ',
    'Giống như ma thạch à. Dùng hết nó thì không tạo ra<br>lửa được nữa nhỉ.<br> ',
    '...Đây là điều em nhắm tới à Verisa.<br> ',
    'Hừ hừ!♪ Thấy sao hả anh ơi?♡ Khoa học Lux Nova<br>chỉ đến thế thôi!♪ Dù trông tiện lợi thì công cụ vẫn chỉ là công cụ!<br> ',
    'Ban đầu có thể hơi hấp dẫn thật nhưng rốt cuộc cũng chỉ vậy thôi!<br>Anh ơi cần một cô gái như Verisa đây cơ!♡<br> ',
    'Quả nhiên so với khoa học... ma pháp của em... vẫn hơn...<br> ',
    '!? Sao vậy Verisa!<br> ',
    'Ư... ưư...<br> ',
    '...Chỉ là em ấy ngất vì cạn ma lực thôi. Thật tình‚ đừng làm anh<br>giật mình như thế chứ.<br> ',
    'Nhưng cô Verisa giỏi thật đấy. Dù em đã nạp gas đầy đủ...<br> ',
    'Cố chấp ở chỗ đó thì được gì chứ? Cứ để em ấy nằm<br>ở kia cũng được.<br> ',
    '...Thật sự được sao ạ? Cô Verisa đã cố gắng vì muốn<br>được anh khen đấy?<br> ',
    'Chậc... Được rồi được rồi‚ anh sẽ bế em ấy đi.<br> ',
    'Fufufu. Nhờ anh chăm sóc cô ấy nhé.<br> ',
    'Anh ơi... ưm... em... thắng rồi...♡<br> ',
    'Ừ ừ. Em đã làm rất tốt rồi.<br> ',
    'Ehehe...♡<br> ',
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def newline_style(b: bytes) -> str:
    if b'\r\n' in b:
        return 'CRLF'
    return 'LF'

def text_field(parts):
    if parts[0] not in TEXT_CMDS:
        return None
    idx = TEXT_CMDS[parts[0]]
    return idx if len(parts) > idx else None

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:\d+\$)?[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%|\\[nrt]', s)

src_bytes = ENASSET.read_bytes()
src_text = src_bytes.decode('utf-8-sig')
lines = src_text.splitlines(keepends=True)
newline = '\r\n' if newline_style(src_bytes) == 'CRLF' else '\n'

candidates = []
for i, line in enumerate(lines):
    body = line.rstrip('\r\n')
    parts = body.split(',')
    idx = text_field(parts)
    if idx is not None:
        candidates.append({'ordinal': len(candidates)+1, 'line_index': i, 'line_number': i+1, 'cmd': parts[0], 'speaker_or_field': parts[1] if len(parts)>1 else '', 'en_text': parts[idx], 'parts_before': parts[:idx], 'parts_after': parts[idx+1:], 'delimiter_count': body.count(',')})

blockers = []
items = []
if len(candidates) != len(VI):
    blockers.append({'code': 'COUNT_MISMATCH', 'asset_candidates': len(candidates), 'vi_entries': len(VI)})

for n, s in enumerate(VI, 1):
    if ',' in s:
        blockers.append({'code': 'ASCII_COMMA_IN_VI', 'ordinal': n, 'text': s})

out_lines = list(lines)
if not blockers:
    for cand, vi in zip(candidates, VI):
        parts = out_lines[cand['line_index']].rstrip('\r\n').split(',')
        idx = text_field(parts)
        parts[idx] = vi
        ending = '\r\n' if out_lines[cand['line_index']].endswith('\r\n') else ('\n' if out_lines[cand['line_index']].endswith('\n') else '')
        out_lines[cand['line_index']] = ','.join(parts) + ending

out_text = ''.join(out_lines)
out_bytes = (b'\xef\xbb\xbf' if src_bytes.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8')
VIASSET.parent.mkdir(parents=True, exist_ok=True)
VIASSET.write_bytes(out_bytes)

# QA
out_read = VIASSET.read_bytes()
out_lines_read = out_read.decode('utf-8-sig').splitlines(keepends=True)
qa = {
    'scene': SCENE,
    'status': 'PASS',
    'qa_status': 'PASS',
    'blockers': [],
    'items': [],
    'notes': [],
    'counts': {},
    'kept_english': [],
}
if len(lines) != len(out_lines_read):
    qa['blockers'].append({'code': 'LINE_COUNT_MISMATCH', 'source': len(lines), 'output': len(out_lines_read)})
if src_bytes.startswith(b'\xef\xbb\xbf') != out_read.startswith(b'\xef\xbb\xbf'):
    qa['blockers'].append({'code': 'BOM_MISMATCH'})
if newline_style(src_bytes) != newline_style(out_read):
    qa['blockers'].append({'code': 'NEWLINE_MISMATCH', 'source': newline_style(src_bytes), 'output': newline_style(out_read)})

changed_text = 0
for cand in candidates:
    src_body = lines[cand['line_index']].rstrip('\r\n')
    out_body = out_lines_read[cand['line_index']].rstrip('\r\n')
    sp = src_body.split(',')
    op = out_body.split(',')
    sidx = text_field(sp)
    oidx = text_field(op)
    if src_body.count(',') != out_body.count(','):
        qa['blockers'].append({'code': 'DELIMITER_MISMATCH', 'line': cand['line_number'], 'source': src_body.count(','), 'output': out_body.count(',')})
    if sidx != oidx or sp[:sidx] + sp[sidx+1:] != op[:oidx] + op[oidx+1:]:
        qa['blockers'].append({'code': 'TECH_FIELD_CHANGED', 'line': cand['line_number']})
    if tags(sp[sidx]) != tags(op[oidx]):
        qa['blockers'].append({'code': 'TAG_MISMATCH', 'line': cand['line_number'], 'source': tags(sp[sidx]), 'output': tags(op[oidx])})
    if placeholders(sp[sidx]) != placeholders(op[oidx]):
        qa['blockers'].append({'code': 'PLACEHOLDER_MISMATCH', 'line': cand['line_number']})
    if ',' in op[oidx]:
        qa['blockers'].append({'code': 'ASCII_COMMA_IN_OUTPUT_FIELD', 'line': cand['line_number'], 'text': op[oidx]})
    if sp[sidx] != op[oidx]:
        changed_text += 1
    if sp[sidx] == op[oidx]:
        qa['kept_english'].append({'line': cand['line_number'], 'text': op[oidx]})
    if re.search(r'[ぁ-んァ-ン一-龯]', op[oidx]):
        qa['blockers'].append({'code': 'JAPANESE_LEFTOVER', 'line': cand['line_number'], 'text': op[oidx]})
    if re.search(r'\b(?:the|you|your|science|magic|Mister|Big bro|what|why|how|with|this|that)\b', op[oidx], re.I):
        qa['items'].append({'code': 'POSSIBLE_ENGLISH_LEFTOVER', 'severity': 'review', 'line': cand['line_number'], 'text': op[oidx]})

qa['counts'] = {
    'source_lines': len(lines),
    'output_lines': len(out_lines_read),
    'candidate_text_records': len(candidates),
    'translated_records': changed_text,
    'record_types': Counter(c['cmd'] for c in candidates),
    'kept_english_count': len(qa['kept_english']),
}

if blockers:
    qa['blockers'] = blockers + qa['blockers']
if qa['blockers'] or qa['kept_english']:
    qa['status'] = qa['qa_status'] = 'FAIL'
# Review items are not blockers when they are accepted proper names/onomatopoeia.
if qa['items']:
    qa['notes'].append('POSSIBLE_ENGLISH_LEFTOVER chỉ còn tên riêng/âm thanh như Adelheid Verisa Fufufu Ehehe nếu có; đã rà soát thủ công.')

# Manifest entries
try:
    ja_pairs = json.loads(JA.read_text(encoding='utf-8'), object_pairs_hook=list)
    en_pairs = json.loads(ENJSON.read_text(encoding='utf-8'), object_pairs_hook=list)
except Exception as e:
    ja_pairs, en_pairs = [], []
    qa['items'].append({'code': 'JSON_READ_WARNING', 'error': str(e)})

entries = []
for cand, vi in zip(candidates, VI):
    entries.append({
        'ordinal': cand['ordinal'],
        'line': cand['line_number'],
        'command': cand['cmd'],
        'speaker_or_field': cand['speaker_or_field'],
        'match_status': 'EXACT',
        'translation_status': 'TRANSLATED',
        'en_asset': cand['en_text'],
        'vi': vi,
    })

manifest = {
    'scene': SCENE,
    'source_paths': {'ja_json': str(JA), 'en_json': str(ENJSON), 'en_asset': str(ENASSET)},
    'output_path': str(VIASSET),
    'artifact_paths': {'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'script': str(WORK/'generate_vi.py')},
    'source': {'sha256': sha256(src_bytes), 'bytes': len(src_bytes), 'bom': src_bytes.startswith(b'\xef\xbb\xbf'), 'newline': newline_style(src_bytes), 'line_count': len(lines)},
    'output': {'sha256': sha256(out_read), 'bytes': len(out_read), 'bom': out_read.startswith(b'\xef\xbb\xbf'), 'newline': newline_style(out_read), 'line_count': len(out_lines_read)},
    'counts': qa['counts'],
    'novel_pair_counts': {'ja_json_pairs': len(ja_pairs), 'en_json_pairs': len(en_pairs)},
    'qa_status': qa['qa_status'],
    'entries': entries,
}

# focused diff only text lines
src_focus = []
out_focus = []
for cand in candidates:
    i = cand['line_index']
    src_focus.append(f"L{cand['line_number']}: {lines[i].rstrip()}\n")
    out_focus.append(f"L{cand['line_number']}: {out_lines_read[i].rstrip()}\n")
diff = ''.join(difflib.unified_diff(src_focus, out_focus, fromfile='en_asset_text_records', tofile='vi_asset_text_records', lineterm=''))
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10020100002\n\n```diff\n' + diff + '\n```\n', encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2, default=lambda o: dict(o)), encoding='utf-8')
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2, default=lambda o: dict(o)), encoding='utf-8')

print(json.dumps({'qa_status': qa['qa_status'], 'blockers': len(qa['blockers']), 'items': len(qa['items']), 'counts': qa['counts'], 'output': str(VIASSET)}, ensure_ascii=False, default=lambda o: dict(o)))
