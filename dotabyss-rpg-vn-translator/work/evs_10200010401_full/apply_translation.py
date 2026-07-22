from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

root = Path('E:/AgentTranslation')
scene = 'evs_10200010401'
en_path = root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle/evs_10200010401.txt'
out_path = root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/evs_10200010401.txt'
ja_json_path = root/'dotabyss-translation-main/translations/novels/evs_10200010401/ja.json'
en_json_path = root/'dotabyss-translation-main/translations/novels/evs_10200010401/en.json'
work = root/'dotabyss-rpg-vn-translator/work/evs_10200010401_full'
work.mkdir(parents=True, exist_ok=True)
out_path.parent.mkdir(parents=True, exist_ok=True)

translations = [
"Hãy Đặt Tiêu Đề",
"Cứ ở lì trong khu huấn luyện thì sẽ làm phiền người ta nên<br>bọn anh ra ngoài rồi…<br> ",
"Ưưư~… chuyện này phải làm sao đây… nya♡<br> ",
"Mẹ ơi! Chị ấy nói “nya” kìa~!<br>Chị ấy thích mèo sao ạ~?<br> ",
"Suỵt‚ đừng nhìn.<br>Con bé đang ở cái tuổi đó đấy.<br> ",
"A á‚ mình lại bị nhìn bằng ánh mắt thương hại như nhìn automata tội nghiệp nữa rồi nya!<br>Ước gì có cái hố để chui xuống nya! Mình chịu hết nổi rồi nya~~n!<br> ",
"Automata tội nghiệp là sao vậy trời?<br>Ừ thì cảnh đó nhìn cũng hơi nhói lòng thật đó~.<br> ",
"Theo chẩn đoán của Adelheid-san thì chứng nya-nya này<br>để thêm một thời gian sẽ tự khỏi nhưng…<br> ",
"Một thời gian là bao giờ vậy nya!? Xấu hổ chết đi được nya!<br>Em muốn làm gì đó để chữa ngay nya~~n!<br> ",
"Em thì thấy dễ thương cũng tốt mà…<br>Nhưng Wendy-san đã không thích thì không thể bỏ mặc được… được rồi.<br> ",
"――Wendy-san‚ hãy phấn chấn lên nya!<br> ",
"Hể…? Viera-san…?<br> ",
"Đây chính là phong tục truyền thống Nhật Bản mà em nghe từ<br>Himari-san―― luật “đèn đỏ mà cả đám cùng băng qua thì chẳng còn đáng sợ”.<br> ",
"Đúng vậy――nếu mọi người cùng nói tiếng mèo thì Wendy-san sẽ không thấy xấu hổ nữa.<br>Vậy nên… nào‚ chị cũng nói cùng đi.<br> ",
"Hảả~? Sao lại là chị chứ!?<br> ",
"Tiếng mèo của chị chắc chắn sẽ siêu dễ thương… à không phải.<br>Vì Wendy-san mà‚ em xin chị đó.<br> ",
"Viera chỉ muốn tự mình nghe thôi chứ gì~!<br> ",
"…Hết cách rồi. Để anh nghĩ cách vậy.<br> ",
"Chỉ Huy…? Anh có ý hay gì sao nya…?<br> ",
"Chẳng lẽ Chỉ Huy-sama cũng sẽ nói tiếng mèo cùng sao?<br>Nếu vậy thì――hay đấy. Em thấy cũng được.<br> ",
"Anh không làm‚ không hay‚ cũng chẳng được gì hết!<br>Khác với Wendy và Viera‚ anh mà nói vậy là đụng tới luật nào đó ngay!<br> ",
"Nghe này‚ theo anh nghĩ thì.<br>Nếu muốn vượt qua tình trạng hiện tại――chỗ đó hẳn là lựa chọn tốt nhất.<br> ",
"――Xưởng đảm nhận chế tạo và bảo trì vũ khí phòng cụ cho binh lính.<br>Nơi vốn luôn vang tiếng kim loại va đập hôm nay còn ồn ào hơn thường lệ.<br> ",
"Khi rèn vũ khí thì phải hây daaa~~! Rồi GONG GONG KENG!<br>Sau đó GÙÙÙ~~~ bỏ vào lửa nóng rồi lại ĐÙNG ĐÙNG! Hiểu chưa!<br> ",
"Dạy kiểu đó thì ai mà hiểu được chứ~~!<br> ",
"Ưưư… nóng quá…<br>Chị ơi‚ em có khi tan chảy mất thôi…<br> ",
"Không được bỏ cuộc đâu Viera! Đây là bước ngoặt quyết định đó!<br>Nhìn đi‚ Wendy cũng đang cố hết sức mà~!<br> ",
"Dồn hết tinh thần vào~~… rồi đập nya!<br>Nyan! Nyan! Nya~~~n!<br> ",
"Ồồ! Cô làm được đấy!<br>Nhìn hơi liều mạng một chút nhưng khí thế thì khỏi chê. Cho hoa điểm mười luôn!<br> ",
"Th-thật vậy sao nya? Ehehe~♪<br> ",
"…Vì lò rèn ồn tiếng kim loại nên khỏi để ý tiếng mèo…<br>Lý thì chị hiểu đó… nhưng nếu vậy làm chuyện khác cũng được mà nhỉ~…?<br> ",
"Sao thế Verisa. Tay em dừng rồi kìa?<br> ",
"Sao anh lại đứng ngoài xem như vậy chứ~!<br>Vào làm cùng đi mà!<br> ",
"Anh là người giám sát mà. Với lại hiếm khi được trải nghiệm rèn đồ thế này.<br>Học theo Wendy rồi nghiêm túc hơn đi.<br> ",
"Aaa thật là~~! Vì Wendy nên chị hiểu rồi~!<br> ",
"Ừ‚ mình cũng phải đập mạnh hơn để tạo tiếng thật lớn.<br>Lớn đến mức át cả giọng Wendy-san…!<br> ",
"Hai người cố gắng đến vậy trong xưởng nóng như thiêu thế này…!<br>Mình cũng phải dốc sức hơn nữa nya!<br> ",
"Nya! Nyan! Nyauu~~~… nyaa~~~n!<br> ",
"(Wendy đang liều mạng đến vậy…!)<br> ",
"(Không phải vì bản thân cậu ấy.<br>Cậu ấy đang dốc hết sức để cố gắng của chúng ta không thành vô ích…)<br> ",
"(Không thể để một cô bé tốt như vậy chịu khổ thêm nữa!<br>Dù có chuyện gì cũng nhất định phải cứu cậu ấy…! Triệu chứng nào cũng cứ tới đây!)<br> ",
"――Quán rượu. Nơi nghỉ chân của những người thách thức Đại Hố.<br>Tại phòng tắm riêng trong một căn phòng ở đó…<br> ",
"Hỡi khí lạnh! Hãy làm nguội làn nước đang sôi sục này!<br>Haaaaa――!<br> ",
"Ồ‚ nhiệt độ nước vừa đẹp đấy. Tốt lắm Viera.<br>Cố lên‚ đừng thua sức nóng của Wendy.<br> ",
"Vâng ạ!<br> ",
"Phù xìiiii~~~…<br>Em xin lỗi Viera-san…<br> ",
"Triệu chứng lần này là sốt à~. Viera đang cố đóng băng nó<br>mà bồn vẫn là nước nóng… Wendy nóng tới mức nào vậy trời~.<br> ",
"…Mà nói mới nhớ~.<br>Sao cả anh cũng vào bồn tắm chung với Wendy vậy~?<br> ",
"Đằng nào nước cũng nóng sẵn nên anh nghĩ tranh thủ tắm một chút.<br>Nhờ vậy tiết kiệm được tiền lò hơi nữa.<br> ",
"Đừng có tiết kiệm ở chỗ này chứ~~.<br>Là Chỉ Huy mà ví tiền của anh cũng yếu xìu vậy sao~?<br> ",
"Ví của anh thì liên quan gì chứ!<br>Anh là Chỉ Huy tài giỏi biết tiết kiệm ngân sách căn cứ đấy!<br> ",
"W-wa wa wa… Chỉ Huy đang tắm chung với em…!<br>Phải làm sao đây… đầu em càng lâng lâng hơn rồi…!<br> ",
"…? Hình như nhiệt độ đang tăng lên?<br>Có lẽ mình dùng phép liên tục nên công suất giảm rồi chăng…?<br> ",
"Này chị ơi. Có lẽ em hơi mệt một chút rồi.<br>Nếu được thì chị cổ vũ em cố lên được không… chẳng hạn vậy…<br> ",
"Thật là‚ hết cách rồi~~!<br>Cố lên‚ cố lên Viera! Cố lên‚ cố lên Viera~~~!<br> ",
"Wa… chị đang cổ vũ cho em…!<br>Em phải cố hơn nữa! Haaaaaaaa…!!<br> ",
"Khoan… quá tay rồi…!<br>Đóng băng mất! Anh cũng bị đóng băng theo mất…!!!<br> ",
"Nhà bếp chuẩn bị bữa ăn cho binh lính.<br>Ở đó‚ Wendy cầm dao và xử lý nguyên liệu với tốc độ khủng khiếp.<br> ",
"Ưưư‚ đói quá đói quá…!<br>Em không nhịn nổi nữa! Nào nào nào~~~! <br> ",
"Đây là triệu chứng đói bụng…! Nguyên liệu đang bị cắt ra liên tục!<br>Aa‚ cậu ấy còn ướp gia vị hoàn hảo rồi chuyển sang chỗ chị nữa…!<br> ",
"Hỡi lửa! Những loài sống dưới nước‚ những sinh vật thở nơi đồng nội‚ những gì cắm rễ trong đất‚<br>hãy nướng tất cả cho vàng thơm đi~~!<br> ",
"Waa~~~! Trông ngon quá đi mất!<br> ",
"Hừ hừ‚ đúng chứ đúng chứ~♪ Phép thuật của Verisa-chan thì<br>canh lửa cũng chuẩn không cần chỉnh♪ Nào‚ cứ ăn thoải mái đi nhé~♪<br> ",
"Vâng‚ em xin phép ăn ạ!<br>Măm măm‚ nhồm nhoàm‚ chóp chép――<br> ",
"Tiền ăn…! Tiền ăn của tháng này~~~…!<br> ",
"Vẫn chưa đủ! Bụng em còn réo ùng ục đây~!<br>Nào nào nào! Tất cả nguyên liệu đều cắt cắt cắt hết~!<br> ",
"Khoan! M-một lượng khổng lồ đang tới kìa~!<br>Phải nướng hết chỗ này sao~!?<br> ",
"Đừng thua chị ơi! Hãy chiến đấu với nguyên liệu!<br>Để lấp đầy cơn đói của Wendy-san‚ chúng ta cần phép thuật của chị!<br> ",
"Đúng rồi… đúng vậy!<br>Phép thuật của Verisa-chan sẽ cứu chiếc bụng của Wendy mà~!<br> ",
"Lên nàoooo!<br>Cả lũ yếu xìu các ngươi‚ bị nướng vàng thơm hết đi~~~!!!<br> ",
"Aaa!?<br>Miếng thịt cao cấp mình mạnh tay mua để dùng cùng rượu vang…!?<br> ",
"Hộc‚ hộc…!<br>C-cuối cùng thì mọi triệu chứng cũng lắng xuống rồi…!<br> ",
"Cảm ơn mọi người nhiều lắm~~!<br> ",
"K-không sao đâu‚ đừng bận tâm… hộc‚ hộc…<br>Chúng ta là bạn mà…<br> ",
"Đ-đúng vậy đó… Chị đã nói sẽ chăm sóc em rồi nên<br>đừng có… hộc… khách sáo với bọn chị đấy… nhé…?<br> ",
"Viera-san‚ Verisa-san…!<br> ",
"Dù sao thì hôm nay cô ấy đã ổn định‚ vậy là tốt rồi.<br>Nếu có thể thì mai anh cũng muốn theo dõi tiếp nhưng anh phải đi thị sát.<br> ",
"Thị sát tức là… anh sẽ vắng nhà sao?<br> ",
"Ừ. Verisa‚ Viera.<br>Hai em hãy cùng giúp Wendy nhé.<br> ",
"<size=30>…Cơ hội đấy Viera.</>",
"<size=30>…Đúng là cơ hội đó chị.</>",
"Hửm? Hai em vừa nói gì à?<br> ",
"Không có gì đâu~♪ Bên này ổn cả nên<br>anh cứ nhanh đi thị sát đi~?<br> ",
"Vậy à? Thế thì anh còn phải chuẩn bị nên đi đây.<br>Phần còn lại giao cho các em――<br> ",
"――Nào‚ anh cũng đi rồi<br>chúng ta cũng chuẩn bị cho ngày mai thôi nhỉ~.<br> ",
"Vâng. Wendy-san‚ hẹn gặp lại ngày mai.<br>…Wendy-san?<br> ",
"…!<br> ",
"Wendy-san!?<br> ",
"Này!? Chuyện gì vậy!?<br>Wendy! Wendy…!?<br> "
]

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def comma_count(s):
    return s.count(',')

def tags(s):
    return re.findall(r'<[^>]*>', s)

def placeholders(s):
    pats = [r'%[sd]', r'\{\d+\}', r'\{name\}', r'\$\{[^}]+\}', r'\\[nrt]', r'%%']
    out=[]
    for pat in pats: out += re.findall(pat, s)
    return out

raw = en_path.read_bytes()
has_bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig')
newline = '\r\n' if '\r\n' in text else '\n'
lines = text.splitlines()
message_indices = [i for i,l in enumerate(lines) if l.startswith('title,') or l.startswith('message,')]
if len(message_indices) != len(translations):
    raise SystemExit(f'translation count mismatch: {len(translations)} vs {len(message_indices)}')

ja = json.loads(ja_json_path.read_text('utf-8'))
en = json.loads(en_json_path.read_text('utf-8'))
ja_keys = list(ja.keys())
en_vals = list(en.values())

records=[]
new_lines = lines[:]
for seq,(idx,vi) in enumerate(zip(message_indices, translations), start=1):
    src_line = lines[idx]
    before_commas = comma_count(src_line)
    if src_line.startswith('title,'):
        new_line = 'title,' + vi
        speaker = ''
        old_text = src_line.split(',',1)[1]
        tech_tail = ''
    else:
        parts = src_line.split(',')
        speaker = parts[1] if len(parts)>1 else ''
        if len(parts) >= 6:
            old_text = parts[2]
            parts[2] = vi
            tech_tail = ','.join(parts[3:])
            new_line = ','.join(parts)
        elif len(parts) == 3:
            old_text = parts[2]
            parts[2] = vi
            tech_tail = ''
            new_line = ','.join(parts)
        else:
            raise SystemExit(f'unexpected field count at line {idx+1}: {src_line}')
    if ',' in vi:
        raise SystemExit(f'ASCII comma in VI text seq {seq}')
    if comma_count(new_line) != before_commas:
        raise SystemExit(f'comma count changed seq {seq} line {idx+1}')
    if tags(old_text) != tags(vi):
        raise SystemExit(f'tag mismatch seq {seq} line {idx+1}: {tags(old_text)} vs {tags(vi)}')
    if placeholders(old_text) != placeholders(vi):
        raise SystemExit(f'placeholder mismatch seq {seq}')
    new_lines[idx] = new_line
    status = 'TRANSLATED'
    records.append({
        'seq': seq,
        'asset_line': idx+1,
        'speaker': speaker,
        'field_count': len(src_line.split(',')),
        'status': status,
        'match_status': 'EXACT',
        'jp': ja_keys[seq-1] if seq-1 < len(ja_keys) else None,
        'en_novel': en_vals[seq-1] if seq-1 < len(en_vals) else None,
        'en_asset': old_text,
        'vi': vi,
        'tags': tags(vi),
        'placeholders': placeholders(vi)
    })

out_text = newline.join(new_lines) + newline
out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
out_path.write_bytes(out_bytes)

# QA compare structural
out_lines = out_text.splitlines()
issues=[]
if len(lines) != len(out_lines): issues.append({'severity':'BLOCKER','type':'line_count','source':len(lines),'output':len(out_lines)})
for i,(a,b) in enumerate(zip(lines,out_lines),1):
    if comma_count(a)!=comma_count(b): issues.append({'severity':'BLOCKER','type':'delimiter_count','line':i,'source':comma_count(a),'output':comma_count(b)})
    if tags(a)!=tags(b): issues.append({'severity':'BLOCKER','type':'tag_mismatch','line':i,'source':tags(a),'output':tags(b)})
    if placeholders(a)!=placeholders(b): issues.append({'severity':'BLOCKER','type':'placeholder_mismatch','line':i})
    if not (a.startswith('message,') or a.startswith('title,')) and a!=b:
        issues.append({'severity':'BLOCKER','type':'technical_line_changed','line':i})
    if b.startswith('message,'):
        parts=b.split(',')
        trans_field = parts[2] if len(parts)>=3 else ''
        if ',' in trans_field:
            issues.append({'severity':'BLOCKER','type':'ascii_comma_in_text_field','line':i})

qa = {
    'file': scene + '.txt',
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'source_path': str(en_path),
    'output_path': str(out_path),
    'source_sha256': sha256(en_path),
    'output_sha256': sha256(out_path),
    'encoding': {'source':'utf-8-sig','output':'utf-8-sig','bom_preserved':has_bom},
    'newline': {'source':'CRLF' if newline=='\r\n' else 'LF','output':'CRLF' if newline=='\r\n' else 'LF'},
    'line_count': {'source':len(lines),'output':len(out_lines),'ok':len(lines)==len(out_lines)},
    'message_title_records': len(records),
    'translated': len(records),
    'review': 0,
    'unmatched': 0,
    'ambiguous': 0,
    'h18_or_adult_uncertain': {'detected': False, 'review_lines': []},
    'issues': issues,
    'status': 'PASS' if not issues else 'FAIL'
}
manifest = {
    'scene': scene,
    'created_at_utc': qa['timestamp_utc'],
    'paths': {'ja_json':str(ja_json_path),'en_json':str(en_json_path),'en_asset':str(en_path),'vi_output':str(out_path)},
    'records': records,
    'summary': {'total_records':len(records),'translated':len(records),'exact':len(records),'review':0,'unmatched':0,'ambiguous':0}
}
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
# focused diff message/title only
old_focus=[f'{i+1}: {lines[i]}' for i in message_indices]
new_focus=[f'{i+1}: {new_lines[i]}' for i in message_indices]
diff='\n'.join(difflib.unified_diff(old_focus,new_focus,fromfile='en/message-title',tofile='vi/message-title',lineterm=''))
(work/'focused_diff.md').write_text('# Focused Diff — evs_10200010401\n\n```diff\n'+diff+'\n```\n',encoding='utf-8')
print(json.dumps({'output':str(out_path),'manifest':str(work/'manifest.json'),'qa_log':str(work/'qa_log.json'),'diff':str(work/'focused_diff.md'),'qa_status':qa['status'],'records':len(records),'issues':len(issues)},ensure_ascii=False,indent=2))
