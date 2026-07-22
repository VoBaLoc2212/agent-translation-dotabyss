from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE='hmn_10130100003'
root=Path('E:/AgentTranslation')
en_path=root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10130100003.txt'
vi_path=root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10130100003.txt'
ja_path=root/'dotabyss-translation-main/translations/novels/hmn_10130100003/ja.json'
en_json_path=root/'dotabyss-translation-main/translations/novels/hmn_10130100003/en.json'
work=root/'dotabyss-rpg-vn-translator/work/hmn_10130100003_full'
work.mkdir(parents=True, exist_ok=True)

translations = [
"Tiêu Đề",
"—Trên Đường Về Từ Nhà Của Sư Phụ.<br> ",
"Ra là bẩm sinh à... Ừm‚ từ giờ mình nên làm gì đây...<br> ",
"Về chuyện đó... hay là ta thử gặp cha mẹ em xem?<br> ",
"Uểểể!?<br> ",
"C-Chỉ Huy sao thế... tự nhiên anh chủ động<br>ghê nhỉ~.<br> ",
"Hình như em đang hiểu lầm thì phải... Ý anh là để hỏi nguyên nhân<br>vì sao em cứ tạo ra mấy thứ khiêu dâm ấy.<br> ",
"Ự. R-ra là ý đó à~. Ừm... ừm...<br> ",
"...Chuyện đó hơi... không‚ có khi tuyệt đối không được đâu.<br> ",
"Sao lại thế? Em thân với cha mẹ đến mức gọi họ là papa<br>và mama còn gì?<br> ",
"Đ-Đừng có lôi cách gọi ra nói chứーーー!!<br> ",
"...Nhưng thật ra thì mình rất yêu papa và ma... khụ! Mình yêu quý<br>và kính trọng cha mẹ lắm.<br> ",
"Nhưng... cả hai đều là giáo viên ở trường ma pháp.<br>Tính cách cũng cực kỳ nghiêm túc nữa...!<br> ",
"Thế thì... làm sao mình có thể hỏi họ<br>một chuyện kỳ quặc như vậy chứ...!?<br> ",
"Ra vậy... hóa ra là thế...<br> ",
"(Nếu không thể xác nhận với cha mẹ em ấy thì nước đi tiếp theo là—)<br> ",
"—Ra vậy. Vì thế ngài đến hỏi ý kiến tôi... đúng không ạ.<br> ",
"Ừ. Anh nghĩ nếu là em thì có thể dùng sức mạnh khoa học để làm rõ nguyên nhân.<br> ",
"Xin lỗi vì đã làm phiền... nhưng ít nhất mình cũng muốn<br>biết được nguyên nhân bằng cách nào đó...!<br> ",
"Tôi đã rõ. Vậy trước tiên...<br> ",
"Hãy bắt đầu bằng việc lấy mẫu dịch cơ thể của cô Frederica.<br> ",
"...Hả?<br> ",
"D-d-dịch cơ thể!? Tại sao!? Vì sao chứ!?<br> ",
"Khoa học phân tích triệt để cấu trúc của đối tượng.<br>Đó là cách tiếp cận giống mà khác với ma pháp.<br> ",
"Để phân tích thành phần cấu tạo cơ thể cô Frederica‚ tôi cần lấy<br>mẫu dịch cơ thể của cô.<br> ",
"L-lý do thì mình hiểu rồi... nhưng... nhưng mà...!<br> ",
"Sao vậy Frederica? Đâu phải chuyện cần do dự đến thế chứ?<br> ",
"Cả Chỉ Huy cũng vậy sao!? Ưư~... hai người bị sao thế...!<br> ",
"Nào‚ xin hãy cho dịch cơ thể của cô vào chiếc đĩa petri<br>này...<br> ",
"N-ngay tại đây!? Cô định lấy mẫu ngay tại đây sao!?<br> ",
"Phân tích nên được tiến hành càng sớm càng tốt mà‚ đúng không?<br> ",
"Đúng là vậy... đúng là vậy thật...! Ưưư~...!<br> ",
"L-làm sao mình làm chuyện khiêu dâm như thế được chứ~~~!!<br> ",
"...Hửm?<br> ",
"...Tôi định lấy mẫu nước bọt mà...? Chuyện đó khiếm nhã đến thế sao?<br> ",
"Hả?<br> ",
"...Đ-đúng vậy! Mình biết mà! Nước bọt chứ gì‚ nước bọt!<br> ",
"Hừm. Vậy có thể hiểu là em xem nước bọt như thứ dâm đãng à?<br> ",
"Không phảiーーー!!<br> ",
"Vậy thì là sao nhỉ... À. Ra vậy‚ cô Frederica không nghĩ tới<br>nước bọt mà là tinh d—?<br> ",
"Suỵt! Suỵt!! Đừng nói thêm nữa! Xin cô đấy!!<br> ",
"Vậy chúng ta lấy lại tinh thần nào... Nào cô Frederica.<br>Hãy thè lưỡi ra‚ lim dim mắt và để nước bọt chảy xuống thật nhớp nháp.<br> ",
"Yêu cầu kiểu gì thế!? Đâu cần phải làm đến mức đó chứ!?<br> ",
"Đúng vậy‚ tôi chỉ muốn xem khi cô Frederica tiến hành hành vi đó<br>thì sẽ có vẻ mặt như thế nào thôi.<br> ",
"Đừng tỉnh bơ nói chuyện động trời như thế!!<br> ",
"...Khoan‚ C-Chỉ Huy! Đừng nhìn em bằng ánh mắt dâm đãng như thế!<br> ",
"Đừng đánh đồng anh với sư phụ của em...<br> ",
"<size=48>—Vài Ngày Sau—</size>",
"Xin phép... Ồ? Cô Frederica đâu rồi ạ?<br> ",
"Anh đến một mình. Anh muốn nghe kết quả phân tích trước.<br> ",
"...Ra vậy. Quả thật tùy kết quả mà có khi không nên nói thẳng<br>với cô ấy. Một phán đoán rất tuyệt vời.<br> ",
"Vậy trước hết‚ xin nói thẳng kết luận... Cô Frederica có lẽ mang<br>dòng máu nữ quỷ mộng ma thượng cấp.<br> ",
"Nữ quỷ mộng ma... lại còn thượng cấp sao?<br> ",
"Nhiều nữ quỷ mộng ma sinh con với con người và dòng máu của họ<br>dần trở nên loãng đi.<br> ",
"Tuy nhiên‚ trong máu cô Frederica có những nhân tố di truyền<br>của nữ quỷ mộng ma mạnh đến mức qua nhiều đời vẫn không hề phai nhạt.<br> ",
"Ban nãy tôi chỉ nói là thượng cấp‚ nhưng với nồng độ này... có lẽ cô ấy<br>là hậu duệ của nữ quỷ mộng ma trong truyền thuyết.<br> ",
"Không ngờ gia tộc Frederica lại có liên hệ với nữ quỷ mộng ma...<br>Cảm ơn em‚ Adelheid. Cuối cùng bí ẩn cũng được giải đáp.<br> ",
"Ngài có muốn tôi nói chuyện này với cô Frederica không?<br> ",
"Không... vì thú vị nên cứ đừng cho em ấy biết.<br> ",
"Fufu... ngài vừa nghĩ ra một trò đùa tinh quái ghê gớm đấy.<br> ",
"Nhưng nếu bảo là không tìm ra gì thì uy tín của Lux Nova<br>sẽ giảm mất. Vậy nên sau đó anh sẽ—<br> ",
"Kết quả... thế nào rồi?<br> ",
"Xin nói ngắn gọn.<br>Cô Frederica. Cô bị—<br> ",
"Hội Chứng Dâm Đãng Cấp Tính.<br> ",
"Cá... i gì!? H-Hội Chứng Dâm Đãng Cấp Tính!?<br> ",
"Mình mới nghe lần đầu... nhưng chắc chắn là bệnh chẳng ra gì rồi!?<br> ",
"Vâng‚ đó là một căn bệnh hết sức tuyệt v... chẳng ra gì.<br> ",
"Khi triệu chứng tiến triển‚ cô Frederica sẽ tăng tốc biến thành<br>một sinh vật dâm đãng.<br> ",
"Vì bản thân cô bị sắc dục bao phủ nên đương nhiên ma lực cũng chịu ảnh hưởng.<br>Do đó dù cô có luyện thành thuật bao nhiêu lần thì cũng chỉ tạo ra những thứ cực kỳ dâm đãng.<br> ",
"T-triệu chứng đáng sợ quá...!<br> ",
"Anh từng đọc về căn bệnh này một lần trong sách.<br>Anh nhớ là nụ hôn của người mình yêu có thể làm dịu triệu chứng thì phải?<br> ",
"N-n-người mình yêu... h-h-hôn á!?<br> ",
"Đúng vậy. Cần một nụ hôn thật nồng nhiệt‚ cuốn lưỡi và nước bọt<br>vào nhau đến mức não như tan chảy.<br> ",
"Cuốn lưỡi và nước bọt vào nhau... một nụ hôn thật sâu...<br> ",
"...Hửm? Sao thế‚ cứ nhìn chằm chằm về phía anh vậy...?<br> ",
"Khụ khụ. À... Chỉ Huy. Nghĩ lại thì dạo gần đây<br>anh ngủ không đủ phải không?<br> ",
"Ừ... đúng là gần đây công việc dồn dập thật.<br> ",
"Ra vậy ra vậy. À... nhắc mới nhớ‚ mình từng nghe nói hôn<br>có tác dụng giúp ngủ ngon đấy.<br> ",
"Hửm...? N-này Frederica.<br>Hình như câu chuyện đang rẽ sang hướng kỳ lạ rồi đấy?<br> ",
"Anh nói gì thế. Đây là vì chúng ta mà! Nếu chúng ta h-hôn<br>nhau... Chỉ Huy sẽ ngủ ngon hơn‚ còn mình thì dịu triệu chứng đấy?<br> ",
"Vậy thì lúc này... chẳng phải nên làm một phát thật hoành tráng sao!?<br> ",
"Tự nhiên em nói cái gì vậy!?<br> ",
"Không‚ đâu cần giới hạn chỉ một lần.<br>Lặp lại hai lần ba lần chắc chắn sẽ có hiệu quả hơn.<br> ",
"Nào‚ Chỉ Huy... hà‚ hà... nào‚ nào!!<br> ",
"B-bình tĩnh! Adelheid‚ làm gì đó đi...!<br> ",
"Người nhớ ra phương pháp điều trị là Chỉ Huy mà.<br>Tôi sẽ chuyên tâm ghi chép cảnh điều trị.<br> ",
"Em vừa tỉnh bơ nói chuyện động trời đấy!?<br> ",
"Ưm hư~... Chỉ Huy~...♡<br> ",
"Vài ngày sau khi được nghe sự thật‚ Frederica một mình về quê. Cô giải thích với mẹ và được bà thổ lộ rằng bà là nữ quỷ mộng ma.",
"Có vẻ sức mạnh của bí thuật được truyền lại khác nhau theo từng đời‚ và Frederica hình như đã chịu một bí thuật khá mạnh.",
"Mẹ cô đã giúp kìm hãm hiệu lực của bí thuật‚ Frederica mừng rỡ vì từ nay có thể toàn tâm toàn ý dấn thân vào nghiên cứu... nhưng...",
"Bụp!<br> ",
"Funyaaaa!?<br> ",
"Hửm? Từ phòng thí nghiệm của Frederica... khói hồng!? Lại nữa sao...!<br> ",
"Frederica! Em ổn không!?<br> ",
"Ha hi...♡ k-không được... bị bế lên là... hya waaaa...♡<br> ",
"...Có vẻ em ấy lại tạo ra thuốc kích dục một cách ngoạn mục rồi.<br> ",
"Ưư~... đáng lẽ không phải thế này... cứ ba lần thì một lần... mình lại<br>tạo ra thứ siêu dâm đãng mất...♡<br> ",
"...Con đường phía trước còn dài lắm.<br> ",
"A‚ hya waa!♡ k-không được‚ chỉ cần được Chỉ Huy<br>bế thôi mà... hưn‚ hả‚ a‚ aaaa...♡<br> ",
"Funyaaaaaaaaa~~~~...♡<br> ",
]

cmds=('title','message','messageTextUnder','messageTextCenter')
raw=en_path.read_bytes()
bom=raw.startswith(b'\xef\xbb\xbf')
newline='CRLF' if b'\r\n' in raw else 'LF'
text=raw.decode('utf-8-sig')
lines=text.splitlines(True)
records=[]
out_lines=[]
idx=0
for line_no,line in enumerate(lines,1):
    stripped=line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith('\n') else line
    if any(stripped.startswith(c+',') for c in cmds):
        parts=stripped.split(',')
        typ=parts[0]
        field_index=1 if typ=='title' else 2
        old=parts[field_index]
        new=translations[idx]
        if ',' in new:
            raise ValueError(f'ASCII comma in translation {idx}: {new!r}')
        # Structural tag count must match EN asset field.
        tag_re=re.compile(r'<[^>]+>')
        if tag_re.findall(old) != tag_re.findall(new):
            raise ValueError(f'tag mismatch idx {idx}: {tag_re.findall(old)} vs {tag_re.findall(new)}')
        parts[field_index]=new
        new_stripped=','.join(parts)
        records.append({'index':idx,'line':line_no,'type':typ,'speaker':parts[1] if typ!='title' else None,'source_text':old,'vi_text':new,'status':'TRANSLATED'})
        idx += 1
        ending='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
        out_lines.append(new_stripped+ending)
    else:
        out_lines.append(line)
if idx != len(translations):
    raise ValueError(f'translation count mismatch used {idx} of {len(translations)}')
out_text=''.join(out_lines)
out_bytes=(b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
vi_path.parent.mkdir(parents=True, exist_ok=True)
vi_path.write_bytes(out_bytes)

# QA structural checks
vi_raw=vi_path.read_bytes()
vi_text=vi_raw.decode('utf-8-sig')
en_lines=text.splitlines()
vi_lines=vi_text.splitlines()
issues=[]
if len(en_lines)!=len(vi_lines): issues.append({'severity':'blocker','type':'line_count','en':len(en_lines),'vi':len(vi_lines)})
for n,(a,b) in enumerate(zip(en_lines,vi_lines),1):
    if a.count(',') != b.count(','):
        issues.append({'severity':'blocker','type':'delimiter_count','line':n,'en':a.count(','),'vi':b.count(',')})
    # check non-translatable commands byte-ish same (by line text) unless text command
    if not any(a.startswith(c+',') for c in cmds) and a != b:
        issues.append({'severity':'blocker','type':'non_text_changed','line':n})

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
counts={c:0 for c in cmds}
for r in records: counts[r['type']]+=1
qa={
 'scene':SCENE,
 'status':'PASS' if not issues else 'FAIL',
 'timestamp':datetime.now(timezone.utc).isoformat(),
 'source': {'en_asset':str(en_path),'ja_json':str(ja_path),'en_json':str(en_json_path), 'sha256_en_asset':sha256(en_path),'bom':bom,'newline':newline,'line_count':len(en_lines)},
 'output': {'vi_asset':str(vi_path),'sha256_vi_asset':sha256(vi_path),'bom':vi_raw.startswith(b'\xef\xbb\xbf'),'newline':'CRLF' if b'\r\n' in vi_raw else 'LF','line_count':len(vi_lines)},
 'text_record_counts': counts,
 'total_text_records': len(records),
 'translated_records': len(records),
 'h18_policy': 'User context confirms all characters 18+; adult/H18-adjacent content translated faithfully without softening or intensifying.',
 'addressing': {'Commander':'Chỉ Huy','Frederica_to_Commander':'mình/anh or Chỉ Huy by source tone','Commander_to_Frederica':'anh/em','Adelheid':'formal tôi/ngài/Chỉ Huy'},
 'structural_qa': {'line_count_match':len(en_lines)==len(vi_lines),'delimiter_count_match':not any(i.get('type')=='delimiter_count' for i in issues),'non_text_unchanged':not any(i.get('type')=='non_text_changed' for i in issues),'bom_preserved':bom==vi_raw.startswith(b'\xef\xbb\xbf'),'newline_preserved':newline==('CRLF' if b'\r\n' in vi_raw else 'LF')},
 'issues':issues,
 'records':records,
}
(work/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={
 'scene':SCENE,'status':qa['status'],'created_at':qa['timestamp'],
 'paths':{'en_asset':str(en_path),'vi_asset':str(vi_path),'ja_json':str(ja_path),'en_json':str(en_json_path),'work_dir':str(work)},
 'hashes':{'en_asset':sha256(en_path),'vi_asset':sha256(vi_path),'ja_json':sha256(ja_path),'en_json':sha256(en_json_path)},
 'encoding':{'bom_preserved':qa['structural_qa']['bom_preserved'],'newline_preserved':qa['structural_qa']['newline_preserved']},
 'counts':{'source_lines':len(en_lines),'output_lines':len(vi_lines),'text_records':counts,'total_text_records':len(records),'translated_records':len(records)},
 'mapping_status_summary':{'TRANSLATED':len(records),'UNMATCHED':0,'AMBIGUOUS':0,'REVIEW':0},
 'qa_status':qa['status'],
}
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# focused diff with only text lines context
udiff=''.join(difflib.unified_diff(text.splitlines(True), vi_text.splitlines(True), fromfile=str(en_path), tofile=str(vi_path), n=1))
(work/'focused_diff.md').write_text('# Focused Diff: hmn_10130100003\n\n```diff\n'+udiff+'\n```\n',encoding='utf-8')
print(json.dumps({'status':qa['status'],'records':len(records),'counts':counts,'issues':len(issues),'vi_path':str(vi_path)},ensure_ascii=False,indent=2))
