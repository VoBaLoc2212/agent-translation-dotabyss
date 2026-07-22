from pathlib import Path
import json, hashlib, re, difflib

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10160100003'
EN = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
WORK.mkdir(parents=True, exist_ok=True)
TEXT_CMDS = ('title,','message,','messageTextUnder,','messageTextCenter,')
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}')

translations = [
'Tiêu Đề',
'Khu trại được Wisteria dẫn tới đã có sẵn chỗ đốt lửa trại và lều<br>đủ rộng rãi để cắm trại.<br> ',
'Chào mừng Chỉ Huy. Cứ tự nhiên nhé.<br> ',
'Cảm ơn nhé. Chỗ này khá tuyệt đấy chứ.<br> ',
'Tôi sẽ nhóm lửa ngay. Cậu đợi một chút.<br> ',
'Wisteria nhanh nhẹn nhóm lửa rồi dẫn tôi ngồi xuống trước đống lửa.<br> ',
'Hơi ấm từ lửa trại thấm vào cơ thể đã mỏi mệt<br>vì đi tìm cô ấy.<br> ',
'Ồ‚ thế này tuyệt thật. Không khí khác hẳn những lần dã ngoại thường ngày.<br> ',
'Vậy… sao cậu lại đi tìm tôi? Có việc gì à?<br> ',
'Tôi nói rồi mà. Tôi chỉ muốn nói chuyện với Wisteria thôi.<br> ',
'Cậu tìm tôi chỉ để nói chuyện thôi sao? Sao lại làm vậy…?<br> ',
'Ban đầu chỉ là tò mò thôi. Tôi nghĩ hai lần gặp nhau<br>chắc cũng là có duyên gì đó.<br> ',
'Tôi cố đến tận đây cũng một nửa là vì hiếu thắng. Một Chỉ Huy<br>không tìm nổi một thuộc hạ thì thảm hại lắm đúng không?<br> ',
'Chỉ vì lý do đó… Cậu đúng là kẻ kỳ lạ thật.<br> ',
'Vậy mà trước giờ chưa từng có một ai muốn nói chuyện với tôi cả.<br> ',
'…Ý cô là sao? Wisteria‚ kể kỹ hơn cho tôi nghe được không?<br> ',
'Là cậu thì không sao. Dù tôi nghĩ đây không phải chuyện nghe vui vẻ gì đâu.<br> ',
'Wisteria đưa ra chiếc cốc cô đang hâm bên lửa<br>rồi chậm rãi bắt đầu kể—<br> ',
'Vốn dĩ tôi là cô nhi. Kiểu trẻ mồ côi vì chiến tranh ấy.<br> ',
'Ra là vậy…<br> ',
'Tôi mất cha mẹ và chỉ còn cách sống một mình. Dù gặp người<br>hay quái vật‚ hễ bị phát hiện là sẽ bị giết không thương tiếc.<br> ',
'Nếu bị áp sát từ phía sau thì chạy cũng không kịp. Tôi tuyệt đối không được<br>để ai nhắm vào điểm mù của mình.<br> ',
'Phải chạy‚ phải trốn‚ phải bảo vệ sau lưng. Tôi đã sống mãi<br>trong một môi trường như thế.<br> ',
'Không có ai bảo vệ cô sao…? Cô chưa từng gặp đồng đội<br>hay bạn bè à?<br> ',
'Có lẽ… ở đâu đó thì đã có thể gặp được.<br> ',
'Nhưng một kẻ luôn chạy trốn khỏi mọi người như tôi thì chẳng ai bắt chuyện cả.<br> ',
'Đến khi nhận ra thì tôi đã giỏi chạy trốn và ẩn nấp<br>rồi càng lúc càng không cần người khác nữa.<br> ',
'Và rồi—không còn ai cần tôi nữa.<br> ',
'Cái… làm gì có chuyện đó chứ!?<br> ',
'Không. Tôi đã sống một mình. Từ nay tôi cũng sẽ sống một mình.<br> ',
'Dù vậy‚ nghĩ đến việc có thêm những đứa trẻ như tôi vẫn khiến tôi khó chịu.<br> ',
'Nếu cứ bỏ mặc Đại Huyệt‚ chắc chắn sẽ có rất nhiều đứa trẻ bất hạnh được sinh ra.<br>Vì thế tôi mới chiến đấu tại căn cứ này.<br> ',
'…Quả nhiên chẳng phải câu chuyện thú vị gì. Xin lỗi‚ tôi không quen nói chuyện<br>với người khác.<br> ',
'Không‚ rất đáng nghe đấy. Và vì thế cho tôi nói một điều thôi.<br> ',
'Wisteria‚ cô không hề đơn độc. Từ nay tôi sẽ không để cô cô độc nữa đâu.<br> ',
'…Tôi không cần những lời đẹp đẽ đó.<br> ',
'Ngay lúc này tôi vẫn một mình. Chẳng có gì thay đổi cả.<br> ',
'Cô đang nói gì vậy? Cô nhìn cho kỹ đi. Tôi đang ở ngay đây<br>bên cạnh Wisteria mà!<br> ',
'Chuyện đó… vì cậu đã tìm ra tôi…<br> ',
'Đúng vậy! Tôi đã tìm ra Wisteria! Cô không còn đơn độc nữa!<br> ',
'Tôi là Chỉ Huy. Tôi có nghĩa vụ bảo vệ sau lưng cô. Tôi tuyệt đối không cho phép cô<br>một mình chiến đấu rồi một mình chết đâu!<br> ',
'Cậu sẽ bảo vệ sau lưng tôi…<br> ',
'…Cậu là người đầu tiên nói với tôi điều đó.<br> ',
'Chắc nếu là người khác nói thì tôi đã gạt đi<br>rằng mình không thể giao lưng cho ai rồi.<br> ',
'Nhưng nếu là cậu‚ người đã tìm ra tôi… có lẽ tôi có thể dựa vào cậu.<br> ',
'Đừng nói “có lẽ” chứ. Bên này đang liều mạng<br>để giành lấy lòng tin của thuộc hạ đấy.<br> ',
'Tôi đang rất cần một thuộc hạ mạnh mẽ‚ giỏi giang và xinh đẹp như cô.<br>Giờ đã thành bạn ngồi quanh lửa trại rồi thì tôi không để cô trốn nữa đâu.<br> ',
'Hưm hưm… cậu đúng là ghê gớm thật. Nghe cậu nói đến mức đó<br>khiến tôi cũng muốn thử tin cậu.<br> ',
'…Tôi nói hơi nhiều rồi. Vì trước giờ tôi chưa từng bộc bạch lòng mình<br>với ai như thế này…<br> ',
'Tôi cũng vậy. Ngồi nhìn lửa trại thế này tự nhiên lại dễ mở lời hơn.<br> ',
'Ừ‚ lửa là thứ thật tốt. Đặc biệt không phải ngọn lửa để vượt qua<br>đêm tối‚ mà là ngọn lửa để trải qua thời gian yên bình.<br> ',
'Nhưng giữ cho nó cháy mãi có vẻ tốn công thật. Đến lúc thêm<br>củi chưa nhỉ?<br> ',
'—Khoan đã‚ không được. Cho cành nhỏ như thế vào đống lửa đã cháy đủ<br>chỉ sinh thêm tro vô ích thôi.<br> ',
'Những cành nhỏ và bông mồi lửa đó chỉ được chuẩn bị để nhóm lửa ban đầu.<br> ',
'Nếu vì quản lửa khó mà cứ dùng toàn thứ dễ cháy<br>thì ngược lại sẽ làm lửa yếu đi đấy.<br> ',
'Đúng là dân lão luyện… Sau này chắc sẽ còn nhiều lần dã ngoại<br>nên tôi phải để Wisteria chỉ dạy rồi.<br> ',
'…Được thôi. Nếu chỉ mình cậu thì đến lúc nào cũng được.<br> ',
'Tôi chắc chắn sẽ chào đón cậu cùng ngọn lửa đỏ này.<br> ',
'Cảm ơn Wisteria.<br> ',
'Nhưng tiếc thật đấy. Chắc mọi người cũng muốn được<br>nói chuyện với Wisteria như thế này mà.<br> ',
'Không có chuyện đó đâu. Chỉ có cậu là đặc biệt thôi.<br> ',
'Những binh lính tôi hỏi chuyện đều quan tâm đến Wisteria đấy. Thôi<br>khi nào có hứng là được. Thử nói chuyện với họ cũng không tệ đâu.<br> ',
'…Nói chuyện với mọi người.<br> ',
'<size=48>—Căn Cứ Tiền Tuyến‚ Sân Tập Luyện</size>',
'Sáng sớm hôm sau tại sân tập luyện<br>Wisteria đang bảo dưỡng cây cung của mình.<br> ',
'(Chỉ Huy nói mình cứ nói chuyện với mọi người là được<br>nhưng làm gì có ai muốn nói chuyện với mình.)<br> ',
'(Cứ làm xong những việc cần làm như mọi khi rồi rời căn cứ thôi. Trước hết<br>bảo dưỡng cung rồi kiểm tra nhiệm vụ tiếp theo…)<br> ',
'Hửm…? Ồ‚ đó là Wisteria à? Hiếm thấy thật.<br> ',
'Chiến Thần đó…! Làm sao đây‚ mình bắt chuyện được không nhỉ…?<br> ',
'Biết sao được… nghe nói cô ấy khó gần lắm…<br> ',
'Cô ấy không nói chuyện với ai đúng không…? Mình làm phiền mất…<br> ',
'(…Họ muốn nói chuyện với mình…?)<br> ',
'Những binh lính khác chắc cũng nghĩ vậy đấy—ai cũng muốn nói chuyện<br>với cô mà.<br> ',
'…A‚ ờ. ………………Xin chào.<br> ',
'Hả…? L-Là tôi sao!?<br> ',
'Ừm… Chuyện là… Ờ… ưm…<br> ',
'…tim đập thình thịch.<br> ',
'Ch… ch…<br> ',
'Ch…?<br> ',
'…Ch-Chà…o… buổi sáng.<br> ',
'Ch-Chào buổi sáng ạ!<br> ',
'Ngập ngừng lâu vậy mà chỉ để chào thôi sao…!?<br> ',
'Tuyệt quá… mình thật sự chào hỏi Wisteria rồi…!<br> ',
'Sao cô lại vui vì chuyện đó chứ…?<br> ',
'Cô ấy đã cứu tôi trong trận trước mà! Tôi cực kỳ kính trọng cô ấy…!<br> ',
'…Ừ‚ đúng vậy. Chúng ta đã được cơn mưa lửa đó cứu.<br> ',
'Này‚ cô… Wisteria.<br> ',
'Hya…!?<br> ',
'Cây cung cô đang bảo dưỡng đó… là một cây cung tốt đấy. Bắn rất chuẩn.<br> ',
'…Đ-Đúng vậy. Ừm‚ là cái đó. T-Tức là… biết nói sao nhỉ… Aaaa‚ đó là<br>cộng sự của tôi.<br> ',
'Vậy à… Có cô và cây cung đó thì mạnh bằng cả trăm người. Từ giờ<br>cũng nhờ cô nhé.<br> ',
'…!<br> ',
'À‚ ừ… c-cứ giao cho tôi!!<br> ',
'Rời khỏi Wisteria đang tiếp tục bảo dưỡng cung<br>những binh lính lại thì thầm bàn tán với nhau.<br> ',
'Thật là…! Không chỉ cây cung mà kỹ năng của Wisteria mới đáng nể chứ!<br> ',
'T-Tôi biết mà…! Nhưng khác với lời đồn‚ cô ấy cũng nói chuyện được<br>đấy chứ…<br> ',
'…Cảm giác kỳ lạ thật. Nhưng cũng không khó chịu đâu.<br> ',
'<size=48>Đêm Hôm Đó Tại Căn Cứ Bí Mật Của Wisteria.</size>',
'Nghe này‚ khi nướng thịt tuyệt đối không được đưa quá gần lửa. Mặt ngoài<br>sẽ cháy khét và không ăn được nữa.<br> ',
'Vậy gặm từng chút từ phần mặt ngoài đã cháy thì sao?<br> ',
'…Cách đó được.<br> ',
'Được‚ lần sau làm thử nhé. Hôm nay cứ theo kiểu Wisteria nhỉ?<br> ',
'…Nhân tiện‚ tôi có thoáng thấy. Sáng nay cô nói chuyện<br>với các binh lính phải không?<br> ',
'Chuyện đó… vì Chỉ Huy bảo tôi thử nói chuyện…<br> ',
'Thế nào‚ cũng đâu tệ lắm phải không? Cô có thêm bạn rồi nhỉ?<br> ',
'Ừ… Tôi đã muốn bảo vệ đồng đội ở căn cứ này.<br> ',
'Nhưng quả nhiên vẫn khác với cậu. Tôi không nghĩ mình muốn họ bảo vệ sau lưng.<br> ',
'Chắc người duy nhất khiến tôi nghĩ có thể giao lưng<br>chỉ có cậu‚ Chỉ Huy đã tìm ra tôi.<br> ',
'…Trách nhiệm nặng nề thật. Thôi cứ giao cho vị Chỉ Huy đáng tin<br>này đi.<br> ',
'Ừ‚ tôi tin cậu đấy‚ Chỉ Huy.<br> ',
'Từ trước đến nay tôi luôn một mình‚ nhưng—từ nay<br>xin hãy để tôi được đi cùng cậu.<br> '
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_text_raw(path):
    data = path.read_bytes()
    bom = data.startswith(b'\xef\xbb\xbf')
    text = data.decode('utf-8-sig')
    newline = 'CRLF' if b'\r\n' in data else 'LF'
    return text, data, bom, newline

text, raw, bom, newline = read_text_raw(EN)
lines = text.splitlines(True)
records = []
for idx, line in enumerate(lines):
    clean = line.rstrip('\r\n')
    if clean.startswith(TEXT_CMDS):
        records.append((idx, clean))
if len(records) != len(translations):
    raise SystemExit(f'translation count {len(translations)} != records {len(records)}')

out_lines = list(lines)
qa_records = []
counts = {cmd[:-1]: 0 for cmd in TEXT_CMDS}
for n, ((idx, clean), vi) in enumerate(zip(records, translations), 1):
    old_line = out_lines[idx]
    nl = '\r\n' if old_line.endswith('\r\n') else ('\n' if old_line.endswith('\n') else '')
    if clean.startswith('title,'):
        new_clean = 'title,' + vi
        cmd = 'title'
        old_text = clean.split(',',1)[1]
    else:
        parts = clean.split(',', 5)
        cmd = parts[0]
        old_text = parts[2]
        parts[2] = vi
        new_clean = ','.join(parts)
    counts[cmd] += 1
    if ',' in vi:
        raise SystemExit(f'ASCII comma in VI record {n}: {vi}')
    if clean.count(',') != new_clean.count(','):
        raise SystemExit(f'comma count mismatch record {n}')
    if TAG_RE.findall(old_text) != TAG_RE.findall(vi):
        raise SystemExit(f'tag mismatch record {n}: {old_text} -> {vi}')
    if sorted(PH_RE.findall(old_text)) != sorted(PH_RE.findall(vi)):
        raise SystemExit(f'placeholder mismatch record {n}: {old_text} -> {vi}')
    out_lines[idx] = new_clean + nl
    qa_records.append({'record_index': n, 'line': idx+1, 'command': cmd, 'status': 'TRANSLATED', 'mapping_status': 'CONTEXT_MATCH' if n in (66, 101) else 'EXACT'})

VI.parent.mkdir(parents=True, exist_ok=True)
out_text = ''.join(out_lines)
encoded = out_text.encode('utf-8')
if bom:
    encoded = b'\xef\xbb\xbf' + encoded
VI.write_bytes(encoded)

vi_text, vi_raw, vi_bom, vi_newline = read_text_raw(VI)
issues = []
if len(text.splitlines(True)) != len(vi_text.splitlines(True)): issues.append('LINE_COUNT_MISMATCH')
if bom != vi_bom: issues.append('BOM_CHANGED')
if newline != vi_newline: issues.append('NEWLINE_CHANGED')
for i,(old,new) in enumerate(zip(text.splitlines(), vi_text.splitlines()),1):
    if old.count(',') != new.count(','):
        issues.append(f'DELIMITER_COUNT_LINE_{i}')
    if old.startswith(TEXT_CMDS):
        if old.startswith('title,'):
            old_field = old.split(',',1)[1]; new_field = new.split(',',1)[1]
        else:
            op = old.split(',',5); np = new.split(',',5)
            if op[:2] != np[:2] or op[3:] != np[3:]: issues.append(f'TECH_FIELD_CHANGED_LINE_{i}')
            old_field = op[2]; new_field = np[2]
        if TAG_RE.findall(old_field) != TAG_RE.findall(new_field): issues.append(f'TAG_MISMATCH_LINE_{i}')
        if sorted(PH_RE.findall(old_field)) != sorted(PH_RE.findall(new_field)): issues.append(f'PLACEHOLDER_MISMATCH_LINE_{i}')
        if ',' in new_field: issues.append(f'ASCII_COMMA_TEXT_LINE_{i}')
        if old == new: issues.append(f'UNCHANGED_TEXT_RECORD_LINE_{i}')

focused = ''.join(difflib.unified_diff(text.splitlines(True), vi_text.splitlines(True), fromfile=str(EN), tofile=str(VI), n=2))
(WORK/'focused_diff.md').write_text('```diff\n' + focused + '\n```\n', encoding='utf-8')
manifest = {
    'scene': SCENE,
    'status': 'PENDING_INDEPENDENT_VERIFY',
    'source_paths': {'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN)},
    'output_path': str(VI),
    'work_dir': str(WORK),
    'script': str(WORK/'translate_hmn_10160100003.py'),
    'focused_diff': str(WORK/'focused_diff.md'),
    'source_sha256': sha(EN),
    'output_sha256': sha(VI),
    'encoding': {'utf8_bom': bom, 'newline': newline, 'line_count': len(lines)},
    'candidate_counts': counts,
    'records': qa_records,
    'mapping_summary': {'EXACT': len([r for r in qa_records if r['mapping_status']=='EXACT']), 'CONTEXT_MATCH': len([r for r in qa_records if r['mapping_status']=='CONTEXT_MATCH']), 'UNMATCHED': 0, 'AMBIGUOUS': 0, 'TRANSLATED': len(qa_records)},
    'rules': {'jp_primary': True, 'en_alignment_only': True, 'commander': 'Chỉ Huy', 'ascii_comma_in_vi_text': 'forbidden; use U+201A ‚'},
    'self_qa': {'status': 'PASS' if not issues else 'FAIL', 'issues': issues, 'translated_records': len(records)}
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
qa = {
    'scene': SCENE,
    'qa_status': 'PENDING_INDEPENDENT_VERIFY',
    'structural_qa': manifest['self_qa'],
    'candidate_counts': counts,
    'translatable_records': len(records),
    'translated_records': len(records),
    'unmatched': [],
    'ambiguous': [],
    'notes': [
        'JP source used as primary; EN asset used for alignment and authoritative tag/field structure.',
        'Speaker names and charaload names preserved as source keys.',
        'Wisteria voice kept reserved and formal using tôi/cậu with Commander/Chỉ Huy where explicit.'
    ]
}
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'written': str(VI), 'records': len(records), 'counts': counts, 'self_qa': manifest['self_qa'], 'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json')}, ensure_ascii=False, indent=2))
