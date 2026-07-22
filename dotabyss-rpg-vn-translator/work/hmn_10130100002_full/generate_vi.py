from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE = 'hmn_10130100002'
ROOT = Path('E:/AgentTranslation')
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10130100002_full'

TRANSLATIONS = [
    'Tiêu Đề',
    'Đây là nhà của sư phụ đấy… hà.<br>Cuối cùng cũng tới nơi rồi… ',
    'Tâm trạng em lại tụt thêm nữa rồi nhỉ…<br> ',
    'Chỉ riêng việc tới được đây đã lằng nhằng đủ thứ rồi còn gì?<br>Thế nên tôi càng thấy ngán hơn đấy.<br> ',
    'Cứ cách một quãng lại phải nhỏ loại thuốc đặc biệt xuống đất<br>để tạm thời gỡ kết giới cản nhận thức thì mới thấy nơi này… à. Đúng là chỗ ẩn thân thật.<br> ',
    'Dù quân đội có kéo tới tấn công thì chắc cũng chẳng tìm ra căn nhà này đâu.<br> ',
    'Sư phụ của em là một pháp sư khá tài giỏi nhỉ.<br> ',
    'Ừ. Nếu chỉ nói về tay nghề ma thuật thì đúng là lão giỏi thật.<br>Còn mọi thứ khác thì tệ hết mức.<br> ',
    'Trông em ghét ra mặt đấy‚ không vào à?<br> ',
    'Đến tận trước cửa rồi mới…<br>bao ký ức đáng nguyền rủa lại… ưưư…!<br> ',
    'Nào‚ vậy thay vì gõ cửa‚<br>tôi ném thuốc nổ vào nhé♪<br> ',
    'Đừng gây cháy rừng chứ… Nào‚ đi thôi.<br> ',
    'Ưềềề… biết rồi‚ đi thì đi…<br> ',
    'Cộc cộc!<br> ',
    'Vào đi.<br> ',
    '…Quả nhiên ngay lúc gỡ kết giới<br>là lão biết bọn mình tới rồi.<br> ',
    'Xin phép làm phiền ạ…<br> ',
    'Ờm‚ sư phụ… lâu rồi không gặp—<br> ',
    'Những lúc thế này phải nói ""Con về rồi"" mới đúng chứ nhỉ.<br> ',
    'Ưẹ!?<br> ',
    'Lão vòng ra sau lưng Frederica từ lúc nào vậy…!?<br> ',
    'Là hiệu quả của thuốc xóa khí tức đấy‚ hô hô.<br> ',
    'Nhưng Frederica à‚ lâu lắm rồi mới gặp con. Da con vẫn trắng trẻo<br>mịn màng thật đẹp như xưa.<br> ',
    'Nào nào… liếm gáy một cái.<br> ',
    'Áaaaaaaaaaa!?<br> ',
    '…Ra vậy‚ là chuyện thế này à.<br> ',
    'Ừm ừm‚ càng lớn tuổi lại càng thêm hương vị‚ ọc…!?<br> ',
    'Đệ tử lâu ngày mới ghé mặt mà ông lập tức liếm cổ là sao hả?<br>Cái lão già dê biến thái này nghĩ gì trong đầu vậy!!<br> ',
    'Biết xấu hổ đi!! Này! Này!! Chết đi!!<br> ',
    'Ọc! Khụ!? Ưưư… cú đá khá đấy…!<br>Này‚ cậu trẻ kia. Nếu cậu sắp sửa ngăn con bé lại thì—<br> ',
    '……………………<br> ',
    'Gwooooo!? Ngươi cũng hùa vào sao… đúng là quỷ dữ mà‚<br>hô hô hô… đau‚ đau đau‚ á đau đau đau…!?<br> ',
    'Cảm ơn. Cùng tôi tiêu diệt con dâm thú này nào.<br> ',
    'Ôi‚ Frederica… từ khi nào con biết bày ra vẻ mặt tuyệt vời<br>như đang nhìn rác rưởi thế này‚ a đau đau đau đau!!<br> ',
    'Dai sức thật đấy…<br> ',
    'Này‚ à thì‚ ít nhất cũng tạm dừng một chút được không…!<br> ',
    '…Nào‚ hai người có chuyện muốn hỏi đúng không?<br>Ta sẽ nghe chuyện của ái đồ và ngài Chỉ Huy đây.<br> ',
    'Bị đánh bầm dập tới vậy<br>mà ông vẫn thản nhiên vào lại chủ đề được à…<br> ',
    '…Khoan‚ hả? Sao sư phụ biết người này là Chỉ Huy?<br>Bọn tôi còn chưa xưng danh mà…<br> ',
    'Chuyện về Căn Cứ Tiền Tuyến đã truyền tới cả vùng hẻo lánh này.<br>Và cả lời đồn về ngài Chỉ Huy trẻ tuổi tài giỏi nữa.<br> ',
    'Ngay lúc các ngươi bước vào rừng‚ ta đã nhìn thấy qua thủy tinh cầu này.<br>Nhìn phong thái trí tuệ ấy là ta đoán ra ngài là Chỉ Huy ngay.<br> ',
    'Ông quan sát chúng tôi qua thủy tinh cầu…?<br>Quả nhiên ông là một thuật sư rất tài giỏi.<br> ',
    'Nếu ngài đã công nhận ta tới mức đó<br>thì lúc đánh cũng nên nương tay hơn chút chứ…<br> ',
    'Nhân tiện‚ sư phụ. Đây là lần đầu tôi thấy thủy tinh cầu đó…<br>Chẳng lẽ ông dùng nó vào việc bất chính nào đấy chứ?<br> ',
    'Không có không có. …Không‚ thật sự là không mà?<br>Đừng dùng nụ cười ấy gây áp lực nữa‚ ái đồ của ta.<br> ',
    'Vậy vào chuyện chính thôi. Nội dung này khó nói với Frederica<br>nên để tôi giải thích. Thật ra—<br> ',
    '…Ra là vậy.<br> ',
    'Hừm… đúng là tình huống khá ngon… khá phiền phức nhỉ.<br> ',
    'Vừa rồi ông suýt nói ""ngon"" đấy à…?<br> ',
    'Frederica‚ muốn ra tay thì nghe lão nói xong đã.<br> ',
    'Tôi nghĩ… nguyên nhân là một loại ma pháp hay lời nguyền nào đó<br>mà ông đã đặt lên Frederica. Ông thấy sao?<br> ',
    'Hả! Thật vậy sao sư phụ!?<br> ',
    'Hô hô hô. Nào nào‚ chuyện thế nào nhỉ.<br> ',
    'Để xem‚ thuốc nổ mình mang theo chỉ có bấy nhiêu thôi à…<br> ',
    '…Nếu không nói thật thì mạng ta có vẻ nguy hiểm‚ nên ta thú nhận vậy.<br>Thật ra từng có lúc ta định dùng ma thuật dâm dục lên con bé.<br> ',
    'Quả nhiên nguyên nhân là sư phụ… khoan‚ hả?<br>""Định dùng"" là sao…?<br> ',
    'Tất cả ma thuật dâm dục đều bị bật ngược. Dù ta đã dùng nhiều lần vẫn thế.<br> ',
    'Đây vẫn chỉ là giả thuyết thôi… nhưng có lẽ Frederica<br>được một bí thuật dâm ma mạnh mẽ bảo vệ từ khi sinh ra.<br> ',
    'Ưeeee…? Tôi… bí thuật dâm ma…? Lại còn từ khi sinh ra…?<br> ',
    'C-chuyện vô lý như thế… làm gì có được! Ba mẹ tôi đều là con người mà!<br> ',
    'Em gọi là ba mẹ à. Dễ thương thật.<br> ',
    'I-i-im đi! Trọng điểm đâu phải chuyện đó!<br> ',
    'Tóm lại… sư phụ đang nói cái gì vậy!?<br> ',
    'Ta liên tục dùng ma pháp dâm dục với đủ cường độ lên con bé<br>và tất cả đều bị bật ngược nên mới suy đoán như vậy! Sao nào‚ thuyết phục chư—ọc!?<br> ',
    'Có quá nhiều chuyện gây sốc nên tôi lỡ nghe cho qua<br>nhưng ông vừa nói một chuyện không thể bỏ qua đấy!<br> ',
    'Ông nói đã nhiều lần dùng ma pháp dâm dục lên tôi là sao hảaaa!?<br> ',
    'Khụ‚ khặc‚ hộc!? H-hôm nay con hung hăng hơn thường lệ nhỉ‚<br>khụụụ!?<br> ',
    '(Bị bí thuật dâm ma bẩm sinh tác động… à.<br>Nếu vậy‚ nguyên nhân có thể nghĩ tới là…)<br> ',
    'Frederica. Mục đích đã đạt được rồi‚ chúng ta nên cáo lui thôi.<br> ',
    'Ừm… vậy à. Tôi vừa mới bắt đầu thấy việc đánh sư phụ cũng vui vui rồi…<br> ',
    'Ôi‚ ái đồ của ta sắp thức tỉnh một sở thích nguy hiểm rồi…<br>Nhưng… con thật sự đã trưởng thành rồi‚ Frederica à.<br> ',
    'Sư phụ…<br> ',
    'Nếu sự việc vẫn chưa giải quyết được thì hãy lại tới đây.<br>Ta sẽ nghĩ cách đối phó.<br> ',
    'N-nhưng mà ông chỉ tạo được mấy thứ dâm dục thôi mà…?<br> ',
    'Có gì đâu‚ ta chỉ cần chỉnh lại thành phần của chúng<br>để dùng được trong thực chiến là xong. Con nghĩ ta là ai chứ?<br> ',
    'Lão già dâm tặc biến thái siêu tàng hình…<br> ',
    'Ta sắp khóc tới nơi rồi… Đây chính là nghiệp ta phải gánh sao…<br> ',
    'Tôi nghĩ đó chỉ là hậu quả tích tụ<br>từ bao lần quấy rối tình dục của ông thôi…<br> ',
    'Nhưng… ra vậy‚ dù không giải quyết được vẫn có cách…<br>Chỉ cần nghĩ được như thế là tôi đã nhẹ nhõm hơn nhiều rồi.<br> ',
    'Cảm ơn sư phụ.<br> ',
    'Ôi‚ ái đồ của ta…!<br>Nào nào‚ trước lúc chia tay cho ta ôm thật chặt một cái…<br> ',
    'Cảm ơn sư phụ.<br> ',
    'Bụp.<br> ',
    'Vừa tung cú đấm vào bụng mà vẫn giữ nguyên nụ cười ấy…<br>khá lắm‚ ái đồ của ta…!<br> ',
]

TEXT_CMDS = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%(?:\w+|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def props(data):
    return {
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'bom': data.startswith(b'\xef\xbb\xbf'),
        'newline': 'CRLF' if b'\r\n' in data and data.count(b'\r\n') == data.count(b'\n') else 'LF',
        'line_count': data.decode('utf-8-sig').count('\n'),
        'endswith_newline': data.endswith(b'\n'),
    }

def text_index(parts):
    return 1 if parts[0] == 'title' else 2

WORK.mkdir(parents=True, exist_ok=True)
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
en_data = EN_ASSET.read_bytes()
en_text = en_data.decode('utf-8-sig')
newline = '\r\n' if b'\r\n' in en_data and en_data.count(b'\r\n') == en_data.count(b'\n') else '\n'
lines = en_text.splitlines()
if len(TRANSLATIONS) != sum(1 for l in lines if l.split(',',1)[0] in TEXT_CMDS):
    raise SystemExit('translation count mismatch')
for idx, t in enumerate(TRANSLATIONS, 1):
    if ',' in t:
        raise SystemExit(f'ASCII comma in translation {idx}: {t}')

out_lines=[]
entries=[]
ti=0
for line_no, line in enumerate(lines,1):
    parts=line.split(',')
    if parts and parts[0] in TEXT_CMDS:
        typ=parts[0]
        idx=text_index(parts)
        old=parts[idx]
        vi=TRANSLATIONS[ti]
        ti += 1
        entries.append({'record_index': ti, 'line': line_no, 'type': typ, 'speaker': parts[1] if len(parts)>1 else '', 'source_text': old, 'vi_text': vi, 'status': 'TRANSLATED', 'match_status': 'EXACT'})
        parts[idx]=vi
        out_lines.append(','.join(parts))
    else:
        out_lines.append(line)
out_text = newline.join(out_lines) + (newline if en_text.endswith('\n') else '')
# Write UTF-8 BOM iff source has BOM.
VI_ASSET.write_bytes((b'\xef\xbb\xbf' if en_data.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8'))

vi_data = VI_ASSET.read_bytes()
vi_text = vi_data.decode('utf-8-sig')
vi_lines = vi_text.splitlines()
blockers=[]
notes=[]
if props(en_data)['line_count'] != props(vi_data)['line_count']:
    blockers.append({'type':'LINE_COUNT_MISMATCH','source':props(en_data)['line_count'],'output':props(vi_data)['line_count']})
for i,(a,b) in enumerate(zip(lines,vi_lines),1):
    if a.count(',') != b.count(','):
        blockers.append({'type':'DELIMITER_MISMATCH','line':i,'source_commas':a.count(','),'vi_commas':b.count(',')})
    ap=a.split(','); bp=b.split(',')
    if ap and ap[0] in TEXT_CMDS:
        idx=text_index(ap)
        if ap[:idx]+ap[idx+1:] != bp[:idx]+bp[idx+1:]:
            blockers.append({'type':'TECH_FIELD_MISMATCH','line':i})
        if TAG_RE.findall(ap[idx]) != TAG_RE.findall(bp[idx]):
            blockers.append({'type':'TAG_MISMATCH','line':i,'source':TAG_RE.findall(ap[idx]),'vi':TAG_RE.findall(bp[idx])})
        if PH_RE.findall(ap[idx]) != PH_RE.findall(bp[idx]):
            blockers.append({'type':'PLACEHOLDER_MISMATCH','line':i})
        if ap[idx] == bp[idx]:
            notes.append({'type':'UNCHANGED_TEXT_FIELD','line':i,'text':bp[idx],'intentional': bp[idx].strip() in ['……………………<br>']})

counts = {cmd: sum(1 for l in lines if l.startswith(cmd+',')) for cmd in TEXT_CMDS}
changed_text_records = sum(1 for e in entries if e['source_text'] != e['vi_text'])
qa = {
    'scene': SCENE,
    'status': 'PASS' if not blockers else 'FAIL',
    'qa_status': 'PASS' if not blockers else 'FAIL',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'candidate_record_counts': counts,
    'candidate_text_records': len(entries),
    'translated_records': len(entries),
    'changed_text_records': changed_text_records,
    'blockers': blockers,
    'notes': notes + [
        {'type':'SOURCE_ALIGNMENT','detail':'JP ja.json is primary; EN novel and EN asset used for ordered alignment. Asset candidate order matched 84 text commands.'},
        {'type':'CHARACTER_VOICE','detail':'Frederica kept casual blunt voice; 師匠 localized as old lecherous master using ta/con/ngươi/ngài as context; Commander/司令官 -> Chỉ Huy.'},
        {'type':'H18_RULE','detail':'Adult/H18-adjacent erotic magic references translated normally under confirmed all-18 project rule; source tone/consent preserved.'},
        {'type':'COMMA_RULE','detail':'No ASCII comma introduced in Vietnamese text fields; Vietnamese internal comma pauses use U+201A where needed.'},
    ],
    'source_props': props(en_data),
    'output_props': props(vi_data),
}
manifest = {
    'scene': SCENE,
    'status': qa['qa_status'],
    'created_at': qa['timestamp'],
    'paths': {'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN_ASSET), 'vi_asset': str(VI_ASSET), 'work_dir': str(WORK)},
    'source': qa['source_props'],
    'output': qa['output_props'],
    'candidate_record_counts': counts,
    'entries': entries,
    'qa_summary': {'qa_status': qa['qa_status'], 'blocker_count': len(blockers), 'translated_records': len(entries), 'changed_text_records': changed_text_records},
}
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
old_focus=[f"{e['line']}: {e['type']},{e['speaker']},{e['source_text']}" for e in entries]
new_focus=[f"{e['line']}: {e['type']},{e['speaker']},{e['vi_text']}" for e in entries]
diff='\n'.join(difflib.unified_diff(old_focus, new_focus, fromfile='EN asset text fields', tofile='VI asset text fields', lineterm=''))+'\n'
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10130100002\n\n```diff\n'+diff+'```\n', encoding='utf-8')
print(json.dumps({'scene':SCENE,'qa_status':qa['qa_status'],'candidate_text_records':len(entries),'translated_records':len(entries),'blockers':len(blockers),'output':str(VI_ASSET),'manifest':str(WORK/'manifest.json'),'qa_log':str(WORK/'qa_log.json'),'focused_diff':str(WORK/'focused_diff.md')}, ensure_ascii=False, indent=2))
