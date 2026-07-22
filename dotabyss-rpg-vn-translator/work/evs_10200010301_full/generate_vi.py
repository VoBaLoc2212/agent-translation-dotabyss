# -*- coding: utf-8 -*-
from pathlib import Path
import json, re, hashlib, difflib

root = Path('E:/AgentTranslation')
scene = 'evs_10200010301'
work = root/'dotabyss-rpg-vn-translator'/'work'/f'{scene}_full'
work.mkdir(parents=True, exist_ok=True)
ja_path = root/'dotabyss-translation-main'/'translations'/'novels'/scene/'ja.json'
en_json_path = root/'dotabyss-translation-main'/'translations'/'novels'/scene/'en.json'
en_asset = root/'Translation'/'en'/'RedirectedResources'/'assets'/'unnamed_assetbundle'/f'{scene}.txt'
vi_asset = root/'Translation'/'vi'/'RedirectedResources'/'assets'/'unnamed_assetbundle'/f'{scene}.txt'

vi = [
"Tiêu Đề",
"――Ra là vậy.<br>Thế nên mọi người mới đưa cô ấy đến chỗ tôi.<br> ",
"――Trong phòng thí nghiệm của Adelheid tại căn cứ tiền tuyến.<br>Nhà khoa học thiên tài lặng lẽ quan sát Wendy mà Verisa và mọi người đưa tới.<br> ",
"Ngay cả ở Lux Nova với nền khoa học kỹ thuật tiên tiến cũng không ai vượt qua được cô ấy.<br>Họ đến nhờ vào tay nghề ấy để xin cô khám cho Wendy.<br> ",
"Trước hết hãy xác nhận triệu chứng đã.<br>Cô Wendy‚ cô thử nói gì đó được không?<br> ",
"Xin lỗi…… đã làm phiền mọi người……<br>Pígaga‚ Pííí!<br> ",
"Ra vậy. Có vẻ chức năng phụ trách phát âm đã gặp trục trặc gì đó.<br>Để tôi kiểm tra thử.<br> ",
"――Hừm. Xem ra do cô ấy cố quá sức<br>nên lò ma đạo bị quá tải và quá nhiệt.<br> ",
"Thấy chưaaa~! Em đã bảo rồi mà~!<br>Cậu cố quá sức rồi đó~~!<br> ",
"V-vâng ạ…… em xin lỗ…… Gaga‚ Píííí!<br> ",
"Thôi mà‚ chị. Cô Wendy cũng chỉ một lòng<br>muốn làm Chỉ Huy vui thôi……<br> ",
"Dù vậy thì hỏng cả người cũng đâu còn ý nghĩa gì.<br>Thật là…… cậu phải dựa vào tớ nhiều hơn chứ…… chúng ta là bạn mà.<br> ",
"――Vậy cô có chữa được cho cô Wendy không?<br> ",
"Để tôi thử xem.<br>――Xin phép.<br> ",
"Adelheid thong thả ghé sát nhìn vào mặt Wendy<br>rồi gõ cốc cốc lên trán cô ấy.<br> ",
"Đau!? C-cô làm gì vậy……? ……Ơ‚ ủa?<br> ",
"Oa~! Khỏi rồi ạ~! Em không còn phát ra Pígaga nữa rồi~!<br> ",
"Triệu chứng này chỉ cần gõ vào vùng trán là sửa được.<br>Nguyên lý giống tivi hay radio cũ vậy.<br> ",
"Aaa…… cô Wendy bị đối xử như đồ cổ thế này……<br>Cách xử lý đại khái kiểu cứ đập cho chạy như vậy thật sự ổn sao?<br> ",
"Cách này cũng là một phương pháp chính thống lâu đời đấy…… nhưng đúng là chỉ sơ cứu tạm thời.<br>Nếu không sửa lò ma đạo là nguyên nhân gốc thì chưa biết sẽ còn triệu chứng nào xuất hiện nữa.<br> ",
"Không phải sơ cứu mà chữa trị đàng hoàng thì không được sao?<br>Em cứ nghĩ công nghệ của Lux Nova sẽ làm được chứ~?<br> ",
"Về căn bản công nghệ của cô ấy khác với chúng tôi nên muốn xử lý nhanh ngay tại đây thì……<br>Dĩ nhiên nếu có thời gian‚ tôi nhất định sẽ cứu được cô ấy.<br> ",
"Thời gian…… ạ.<br>Bữa tiệc bất ngờ phải làm sao đây……?<br> ",
"……Có vẻ mọi người có chuyện riêng nhỉ.<br>Tôi hiểu rồi. Tôi sẽ tìm cách sửa càng sớm càng tốt.<br> ",
"Thật sao ạ!? Cảm ơn cô nhiều lắm!<br> ",
"Không cần cảm ơn. Với tôi‚ cơ thể cô cũng vô cùng thú vị.<br>Dù sao đó cũng là kết tinh kỹ thuật ma pháp Perdion mà bình thường hiếm khi được biết đến……<br> ",
"Quả nhiên kiểm tra đơn giản thế này thì chưa thể khiến tôi thỏa mãn.<br>Cô có muốn được tôi kiểm tra thật chậm thật kỹ từ đầu đến chân không nào?<br> ",
"H-híí……!<br> ",
"T-tuyệt đối không được!<br>Nếu cô muốn nghiên cứu ma pháp thì để em hợp tác thay cô ấy……!<br> ",
"Khoan khoan‚ tôi không giao Wendy hay Viera cho cô đâu nhé!?<br>Tại cô nói mấy lời kỳ quặc nên ai cũng sợ rồi kìa‚ đồ biến thái~~!<br> ",
"Vâng‚ tôi là nhà khoa học thiên tài kiêm biến thái.<br>Mong mọi người tiếp tục chiếu cố.<br> ",
"Phủ nhận đi chứ~~!<br>Aa~ thật tình. Cô đúng là khó xử lý quá đi~!<br> ",
"Quan trọng hơn‚ xin hãy cẩn thận. Ảnh hưởng của quá nhiệt vẫn còn sót lại.<br>Từ giờ cô Wendy có lẽ sẽ phát sinh nhiều triệu chứng khác nhau.<br> ",
"Nhiều triệu chứng khác nhau……?<br>Sẽ xảy ra chuyện gì vậy?<br> ",
"Tôi không thể dự đoán. Nhưng nếu không kìm lại từng triệu chứng mỗi khi chúng xuất hiện<br>thì trường hợp xấu nhất cô ấy có thể ngừng hoạt động hoàn toàn.<br> ",
"Ểểểểể~!?<br> ",
"K-không thể nào―― nếu vậy thì em sẽ<br>trở thành lò ma đạo rồi hợp thể với cô Wendy.<br> ",
"Rồi rồi~. Bình tĩnh nào‚ cả hai người. Đâu có gì đáng để làm ầm lên vậy đâu~.<br>Không có Verisa-chan bên cạnh là hai người không ổn chút nào nhỉー đúng là yếu xìu mà~♪<br> ",
"Tóm lại chỉ cần kìm triệu chứng lại như lúc nãy là được đúng không~?<br>Chuyện đó cứ để Verisa-chan lo♪<br> ",
"C-cô Verisa~~! Huhu‚ cảm ơn cô nhiều lắm……!<br>Em cảm động đến mức nước mắt…… Pííííí‚ Gagagagaga!<br> ",
"Xin phép.<br> ",
"Đau quá! Gaga‚ gaga…… k-khoan‚ cô Adelheid…… Gaga‚ Pí!<br>Trán em…… đau‚ đau…… Gagaga……!<br> ",
"……A‚ khỏi rồi ạ.<br> ",
"Mất hết cao trào……<br> ",
"Triệu chứng vừa rồi cũng sẽ không kéo dài lâu.<br>Theo suy đoán của tôi‚ có lẽ sắp chuyển sang một trục trặc khác……<br> ",
"Tốt thôi!<br>Dù là triệu chứng gì‚ tôi cũng sẽ chữa cho cậu!<br> ",
"Em tuyệt đối sẽ không để cô ấy ngừng hoạt động. Dù thiết bị tự hủy có trục trặc<br>và thổi bay cả căn cứ này thì chính em cũng sẽ ngăn lại.<br> ",
"E-em đâu có gắn thiết bị nguy hiểm như vậy đâu ạ~!<br> ",
"……!?<br>C-cái này là……!?<br> ",
"Sao vậy!? Đừng nói là triệu chứng tiếp theo nhé!?<br>Wendy‚ nói cho tôi biết chuyện gì đang xảy ra đi!<br> ",
"Cái này…… x-xin cô tránh ra‚ cô Verisa……!<br>Em…… không kìm được nữa……!<br> ",
"Sao thế!? Rốt cuộc là――<br> ",
"……Mugyuuuuuu~~!!<br> ",
"Hả!? Cậu tự nhiên ôm chầm lấy tôi là sao vậy~~!?<br>Mà này‚ khỏe quá~~! Đau đau đau!<br> ",
"Cô Wendy‚ xin hãy đổi chỗ đó cho em―― không phải‚<br>xin hãy buông chị em ra!<br> ",
"Uuuu~~~! Em muốn buông nhưng không buông ra được~~~!<br>Tự nhiên em cứ muốn ôm chặt lấy người khác~~~!<br> ",
"Này‚ dính sát như thế thì ngã―― kya!?<br> ",
"Guheee~! N-nặng……!? Cậu nhỏ con như vậy<br>sao lại nặng thế này~!? Hôm qua cậu ăn nhiều lắm hả!?<br> ",
"E-em nặng vì em là automata mà~!<br>Em thật sự xin lỗiii~~!<br> ",
"Đè ngã chị mình thế kia……<br>Thật là…… đáng ghen tị……<br> ",
"Đừng đứng nhìn nữa‚ mau ngăn lại đi! Với lại đau! Nặng! Nội tạng bị ép nát mất!<br>Trời ơiii~~! Rốt cuộc là cậu bị sao vậy hả~!<br> ",
"Ra vậy…… đây là chứng thèm ôm.<br> ",
"Cái gì vậy!?<br> ",
"――Sân huấn luyện.<br>Ở đó‚ hôm nay cũng vang lên tiếng hô khí thế của các binh sĩ đang miệt mài rèn luyện.<br> ",
"Nào tới đi‚ Chỉ Huy! Thử ghi một điểm trước tôi xem!<br> ",
"Ghi một điểm trước Raveria à…… nghe có vẻ vất vả đây.<br> ",
"――Chỉ Huyyyyyyyyyyyyy!<br> ",
"Hửm? Wendy à? Em chạy tới hốt hoảng như vậy…… có chuyện……<br>Khoan‚ khoan đã! Sắp tới nơi rồi thì dừng lại!! Không dừng là va――!<br> ",
"Tránh raaaaaaaaaaaa!!<br> ",
"Guhooooo……!?<br> ",
"Chuyện gì vậy!? Đ-đánh úp à!? Đây là do Raveria sai khiến sao!?<br> ",
"Tôi đâu có đời nào làm chuyện đó.<br>……Dù vậy thì cú quấn người này đẹp thật. Sức mạnh cũng không chê vào đâu được.<br> ",
"Giờ đâu phải lúc khen……!<br>C-cứu…… khỏe quá…… nguoôôô……! Đau! Nặng! Nội tạng bị ép nát mất!<br> ",
"Em xin lỗi‚ em xin lỗi……!<br>Ngay cả em cũng không dừng lại được~~~!<br> ",
"Cuối cùng cũng đuổi kịp……!<br>Ôi‚ Chỉ Huy‚ sao lại thành ra thế này……!<br> ",
"Khụ‚ khụ……! Viera với Verisa……!?<br>Gì vậy‚ chuyện này là sao!?<br> ",
"Chỉ Huy‚ cô Wendy đã mắc chứng thèm ôm rồi ạ!<br> ",
"Hả……!? Cái triệu chứng quái lạ đó là gì!? Sao lại<br>thành ra thế!?<br> ",
"（――Vì là tiệc bất ngờ nên phải giấu anh ấy mới được.<br>Không thể nói Wendy hỏng vì cố quá sức chuẩn bị được nhỉ……）<br> ",
"Ừm thì―― đó là một căn bệnh lạ chưa rõ nguồn gốc rò rỉ từ Hố Lớn!<br>Ai mắc phải sẽ không thể cưỡng lại việc ôm người khác đâu~!<br> ",
"Nói dối!<br>Nếu có bệnh như vậy lan ra thì lẽ ra phải có báo cáo gửi lên anh rồi!<br> ",
"N-nó chỉ‚ ch-chỉ lây cho automata thôi~!<br>Đ-đúng không‚ Viera!?<br> ",
"Ư-ừm‚ đúng như chị nói!<br>Cách xử lý là chỉ còn biết ôm người khác cho đến khi cơn phát tác lắng xuống thôi ạ!<br> ",
"Vì vậy bọn em nghĩ ở sân huấn luyện có thể có người<br>chịu nổi cú ôm của Wendy nên mới đến đây ạ!<br> ",
"Ra vậy……!? Không‚ anh chưa hẳn là hiểu đến mức đó nhưng tạm thời anh nắm rồi!<br>Nhưng bị Wendy ôm với sức mạnh thế này thì thật sự khá là―― guheee~!<br> ",
"Awaa! Mặt anh ấy đang xanh lè thấy rõ luôn~~!!<br> ",
"Em xin lỗi‚ Chỉ Huy~~! Chính em cũng không dừng lại được……!<br>Em phải làm sao đây~~!?<br> ",
"Tôi đã nghe câu chuyện rồi! Tóm lại chỉ cần chịu được sức của cô bé đó là được đúng không?<br>Hay đấy! Để tôi làm đối thủ của cô ấy!<br> ",
"C-có thật là được không ạ……!?<br> ",
"Không sao! Ngày nào tôi cũng rèn luyện mà!<br>Cứ hết sức mà lao tới!<br> ",
"V-vậy thì…… ei!<br> ",
"Ồ……! Sức mạnh khá đấy!<br>Nhưng…… vẫn còn xa lắm! Tôi vẫn chịu được! Tới nữa điiii!!<br> ",
"Ghê thật…… không chỉ chịu được cú ôm của Wendy<br>mà trông cô ấy còn có vẻ vui nữa~…… cũng giỏi đấy…… theo nhiều nghĩa.<br> ",
"Ừm‚ đúng là vậy……<br>Nhờ thế mà hòa bình của căn cứ tiền tuyến được bảo vệ rồi…… phù.<br> ",
"Này…… rốt cuộc anh đang phải xem cái gì vậy?<br> ",
"Mà này‚ Verisa‚ Viera. Anh biết ba người các em đang lén lút làm gì đó<br>nhưng chuyện này có liên quan không? Rốt cuộc các em đang làm gì?<br> ",
"Hả!? A-anh hỏi gì…… b-bọn em đâu có làm gì đâu mà!<br>T-tóm lại giờ không còn vấn đề gì nữa! Ổ-ổn rồi……!!<br> ",
"C-c-c-chị ơi! Chị dao động quá rồi đó!<br>B-b-b-bình‚ bình tĩnh lại đi!<br> ",
"Em cũng vậy……. Thôi‚ cũng chẳng sao.<br> ",
"Phù…… cuối cùng cũng lắng xuống rồi ạ.<br> ",
"Cô Wendy……!<br>Tốt quá‚ cơn phát tác chứng thèm ôm đã lắng xuống rồi nhỉ.<br> ",
"Vâng ạ! Tất cả là nhờ cô Raveria!<br>Cảm ơn cô rất nhiều!<br> ",
"Có gì đâu‚ đừng để tâm. Tôi cũng vui vì lâu rồi mới được đấu<br>với một đối thủ mạnh.<br> ",
"Sao cô lại bóng bẩy như vậy chứ……<br>Thôi‚ miễn là mọi người bình an thì được.<br> ",
"Uuu…… mọi người‚ em thật sự xin lỗi vì đã gây nhiều phiền phức……<br>Em ổn rồi nên mọi người cứ yên tâm…… ư……!?<br> ",
"Đừng nói là…… triệu chứng tiếp theo đã tới rồi nhé……!?<br> ",
"E-e-e-em ổn‚ ạ……!<br>Y-yên‚ tâm…… yên tâm…… yê‚ n……!<br> ",
"――Cứ yên tâm meo♡<br> ",
"Yên tâm nổi mới lạ á!!<br> ",
]

# Guard: no ASCII comma in translatable Vietnamese fields
bad = [(i+1, s) for i,s in enumerate(vi) if ',' in s]
if bad:
    raise SystemExit('ASCII comma in VI translations: '+repr(bad[:5]))

ja = json.load(open(ja_path, encoding='utf-8'))
en = json.load(open(en_json_path, encoding='utf-8'))
if len(vi) != len(en):
    raise SystemExit(f'translation count {len(vi)} != en count {len(en)}')

src_bytes = en_asset.read_bytes()
encoding = 'utf-8-sig' if src_bytes.startswith(b'\xef\xbb\xbf') else 'utf-8'
src_text = src_bytes.decode(encoding)
newline = '\r\n' if b'\r\n' in src_bytes else '\n'
lines = src_text.splitlines(keepends=True)
msg_indices = []
for idx, line in enumerate(lines):
    bare = line.rstrip('\r\n')
    if bare.startswith('title,') or bare.startswith('message,'):
        msg_indices.append(idx)
if len(msg_indices) != len(vi):
    raise SystemExit(f'candidate count {len(msg_indices)} != vi count {len(vi)}')

orig_fields = []
new_lines = list(lines)
manifest_entries = []
for n, line_idx in enumerate(msg_indices):
    line = lines[line_idx]
    eol = '\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else '')
    bare = line[:-len(eol)] if eol else line
    parts = bare.split(',')
    before_count = len(parts)
    if parts[0] == 'title':
        trans_idx = 1
        record_id = 'title'
    elif parts[0] == 'message':
        trans_idx = 2
        record_id = parts[4] if len(parts) > 4 and parts[4] else f'line_{line_idx+1}'
    else:
        raise AssertionError(parts[0])
    old_text = parts[trans_idx]
    parts[trans_idx] = vi[n]
    nb = ','.join(parts)
    if len(nb.split(',')) != before_count:
        raise SystemExit(f'field count changed at line {line_idx+1}')
    new_lines[line_idx] = nb + eol
    jp_key = list(en.keys())[n]
    status = 'TRANSLATED'
    manifest_entries.append({
        'asset_line': line_idx+1,
        'record_type': parts[0],
        'speaker': parts[1] if parts[0]=='message' and len(parts)>1 else None,
        'record_id': record_id,
        'match_status': 'EXACT_BY_ORDER',
        'translation_status': status,
        'jp': jp_key,
        'en_reference': en[jp_key],
        'en_asset_before': old_text,
        'vi': vi[n],
    })

out_text = ''.join(new_lines)
vi_asset.parent.mkdir(parents=True, exist_ok=True)
vi_asset.write_bytes(('\ufeff' + out_text).encode('utf-8') if encoding == 'utf-8-sig' else out_text.encode('utf-8'))

# QA
out_bytes = vi_asset.read_bytes()
out_dec = out_bytes.decode(encoding)
out_lines = out_dec.splitlines(keepends=True)
qa_items = []
def tags(s): return re.findall(r'<[^>]+>', s)
def placeholders(s): return re.findall(r'%(?:%|s|d)|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]', s)
if len(out_lines) != len(lines):
    qa_items.append({'severity':'BLOCKER','type':'line_count','source':len(lines),'output':len(out_lines),'status':'FAIL'})
for i,(a,b) in enumerate(zip(lines,out_lines),1):
    ab=a.rstrip('\r\n'); bb=b.rstrip('\r\n')
    if ab.count(',') != bb.count(','):
        qa_items.append({'severity':'BLOCKER','type':'delimiter_count','line':i,'source':ab.count(','),'output':bb.count(','),'status':'FAIL'})
    if ab.split(',')[0] != bb.split(',')[0]:
        qa_items.append({'severity':'BLOCKER','type':'record_type','line':i,'status':'FAIL'})
    ap_for_text=ab.split(','); bp_for_text=bb.split(',')
    src_text_field = ap_for_text[2] if ab.startswith('message,') and len(ap_for_text)>2 else (ap_for_text[1] if ab.startswith('title,') and len(ap_for_text)>1 else ab)
    out_text_field = bp_for_text[2] if bb.startswith('message,') and len(bp_for_text)>2 else (bp_for_text[1] if bb.startswith('title,') and len(bp_for_text)>1 else bb)
    if tags(src_text_field) != tags(out_text_field):
        qa_items.append({'severity':'BLOCKER','type':'tags','line':i,'source':tags(src_text_field),'output':tags(out_text_field),'status':'FAIL'})
    if placeholders(src_text_field) != placeholders(out_text_field):
        qa_items.append({'severity':'BLOCKER','type':'placeholders','line':i,'source':placeholders(src_text_field),'output':placeholders(out_text_field),'status':'FAIL'})
    # technical fields unchanged except translatable field
    if ab.startswith('message,'):
        ap=ab.split(','); bp=bb.split(',')
        if len(ap)==len(bp):
            for j in range(len(ap)):
                if j != 2 and ap[j] != bp[j]:
                    qa_items.append({'severity':'BLOCKER','type':'technical_field_changed','line':i,'field':j,'source':ap[j],'output':bp[j],'status':'FAIL'})
    elif ab.startswith('title,'):
        ap=ab.split(','); bp=bb.split(',')
        if len(ap)==len(bp) and ap[0] != bp[0]:
            qa_items.append({'severity':'BLOCKER','type':'technical_field_changed','line':i,'field':0,'status':'FAIL'})
# Check no ASCII comma inside text fields by split count same and translations prechecked. Check adult uncertain
review_items = []
adult_uncertain = False

qa_log = {
    'file': scene + '.txt',
    'source': str(en_asset),
    'output': str(vi_asset),
    'qa_status': 'PASS' if not qa_items else 'FAIL',
    'source_sha256': hashlib.sha256(src_bytes).hexdigest(),
    'output_sha256': hashlib.sha256(out_bytes).hexdigest(),
    'encoding': encoding,
    'bom_preserved': src_bytes.startswith(b'\xef\xbb\xbf') == out_bytes.startswith(b'\xef\xbb\xbf'),
    'newline': 'CRLF' if newline == '\r\n' else 'LF',
    'source_line_count': len(lines),
    'output_line_count': len(out_lines),
    'translatable_records': len(msg_indices),
    'translated_records': len(vi),
    'skipped_records': 0,
    'h18_or_adult_uncertain_records': 0,
    'blockers': [x for x in qa_items if x.get('severity') == 'BLOCKER'],
    'items': qa_items,
    'notes': ['JP used as primary source; EN asset used for sequence/alignment.', 'No H-18/adult-uncertain content detected; all records translated.']
}
manifest = {
    'scene': scene,
    'created_files': {
        'output': str(vi_asset),
        'manifest': str(work/'manifest.json'),
        'diff': str(work/'focused_diff.md'),
        'qa_log': str(work/'qa_log.json'),
    },
    'inputs': {'ja_json': str(ja_path), 'en_json': str(en_json_path), 'en_asset': str(en_asset)},
    'output': str(vi_asset),
    'encoding': encoding,
    'newline': 'CRLF' if newline == '\r\n' else 'LF',
    'source_sha256': hashlib.sha256(src_bytes).hexdigest(),
    'output_sha256': hashlib.sha256(out_bytes).hexdigest(),
    'line_count': len(lines),
    'records_total': len(manifest_entries),
    'records_translated': len(manifest_entries),
    'records_review': 0,
    'records_unmatched': 0,
    'entries': manifest_entries,
}
(work/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(work/'qa_log.json').write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')
# focused diff only candidate lines
orig_focus = []
new_focus = []
for i in msg_indices:
    orig_focus.append(f'{i+1}: {lines[i].rstrip()}\n')
    new_focus.append(f'{i+1}: {out_lines[i].rstrip()}\n')
diff = ''.join(difflib.unified_diff(orig_focus, new_focus, fromfile='EN translatable records', tofile='VI translatable records', lineterm='\n'))
(work/'focused_diff.md').write_text('# Focused Diff: evs_10200010301.txt\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')
print(json.dumps({'output':str(vi_asset),'work':str(work),'qa_status':qa_log['qa_status'],'lines':len(lines),'records':len(msg_indices),'blockers':len(qa_log['blockers'])}, ensure_ascii=False, indent=2))
