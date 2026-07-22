import json, hashlib, re, difflib
from pathlib import Path
from datetime import datetime, timezone

SCENE='hmn_10080100001'
root=Path('E:/AgentTranslation')
en_asset=root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10080100001.txt'
vi_asset=root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10080100001.txt'
ja_json=root/'dotabyss-translation-main/translations/novels/hmn_10080100001/ja.json'
en_json=root/'dotabyss-translation-main/translations/novels/hmn_10080100001/en.json'
work=root/'dotabyss-rpg-vn-translator/work/hmn_10080100001_full'
work.mkdir(parents=True, exist_ok=True)

commands={'title','message','messageTextUnder','messageTextCenter'}

translations = [
"Vị Khách Từ Perdion",
"Xin mời. Trà và bánh hôm nay đây ạ.<br> ",
"Ồ‚ cảm ơn nhé.<br> ",
"Wa‚ cảm ơn♪ Hôm nay là bánh muffin à‚ tuyệt quá……!<br> ",
"Mời mọi người cứ tự nhiên♪<br> ",
"Măm măm…… ưm～ ngon quá～!<br>Bên trong mềm ẩm‚ vị ngọt thanh nhã‚ tuyệt nhất luôn!<br> ",
"Fufu…… em mừng là chị thích.<br> ",
"Em đi mua sắm một chút‚ nên chị cứ thong thả nhé‚ Verisa.<br> ",
"Đi vui nhé～♪ Măm măm……<br> ",
"Cô tự tiện ở lì đây‚ ăn chùa‚ vậy mà vẫn bày đặt nhận xét hách dịch được nhỉ.<br> ",
"Anh nói vậy thôi chứ‚ anh ơi‚<br>được uống trà cùng Verisa làm anh vui lắm đúng không?<br> ",
"Hay là anh không ăn được nếu em không đút “a～” cho? <br>Trước mặt chị phó quan mà cũng muốn làm nũng rồi sao～? Fufu♪<br> ",
"……Thôi được rồi‚ cứ ăn tùy cô đi.<br> ",
"Đúng là anh hiền ghê♪ Em mong bánh ngày mai quá đi～.<br> ",
"Cô ta còn định đến nữa à……<br> ",
"Nè nè anh ơi‚ bánh ngày mai là đồ đá lạnh thì sao?<br> ",
"Loại lạnh buốt giúp hạ nhiệt cơ thể đang nóng bừng ấy!<br> ",
"Đừng có đòi hỏi vô lý.<br>Với lại pháp sư lửa thì đừng đòi ăn đồ đá lạnh chứ.<br> ",
"Chính vì em giỏi ma pháp lửa mà‚ đúng không?<br>Đồ đá lạnh làm mát cơ thể nóng lên vì ma pháp là tuyệt nhất đó.<br> ",
"Ở Perdion‚ em thường ăn sau nhiệm vụ lắm～.<br> ",
"Ồ? Ở bên đó cô cũng có việc làm cơ à.<br> ",
"Tất nhiên rồi～? Pháp sư ưu tú Verisa-chan được săn đón khắp nơi mà!<br> ",
"……Dù em gái em được giao nhiều việc hơn em.<br> ",
"Ồ‚ cô có em gái à. Vậy là cô thua kém em gái mình về thực lực nhỉ.<br> ",
"Không có chuyện đó đâu nhé?<br>Theo tiêu chuẩn của Perdion thì em ấy chỉ được đánh giá cao hơn em mộ～t chút thôi.<br> ",
"……Vậy chẳng phải đơn giản là cô thua em ấy trên tư cách pháp sư sao?<br> ",
"À～. Anh ơi‚ hóa ra anh nói kiểu đó đấy hả～?<br> ",
"Nghe này‚ con bé đó từ xưa đã――<br> ",
"――Rầm!<br>Cánh cửa bật mở kèm một tiếng động lớn‚ và một phụ nữ mặc áo choàng bước vào phòng chỉ huy.<br> ",
"Ngươi là ai!?<br> ",
"Mặt lạ nhỉ.<br>Bộ đồ đó…… có vẻ là pháp sư của Perdion……<br> ",
"A‚ cô……! Sao cô lại ở đây!?<br> ",
"Người quen của cô à‚ Verisa?<br> ",
"Q-quen hay không thì……<br> ",
"……Lâu rồi không gặp‚ chị.<br> ",
"Chị…… sao……?<br> ",
"Veera!? Sao em lại đến nơi này……!<br> ",
"Em tình nguyện gia nhập viện quân từ Perdion.<br>Em nghĩ nếu đến đây thì có thể gặp chị.<br> ",
"Viện quân……!? N-này‚ qua đây một chút!<br> ",
"Ơ‚ chị?<br> ",
"Verisa nắm tay Veera‚<br>dẫn cô ấy tới một góc phòng chỉ huy.<br> ",
"Veera‚ sao em lại đến đây?<br>Em biết nơi này nguy hiểm mà đúng không?<br> ",
"Vâng. Vì nguy hiểm‚<br>nên em nghĩ chắc chị đang gặp khó khăn.<br> ",
"C-chị đâu có gặp khó khăn gì đâu! Chẳng có vấn đề gì xảy ra hết mà!<br> ",
"……Thật không?<br> ",
"Tất nhiên rồi! Có ma pháp của chị‚<br>thì cả quái vật to đùng trong Hố Sâu cũng hóa tro dễ ợt thôi!<br> ",
"(Cô Veera đó hình như là em gái Verisa……<br>Verisa khoác lác ghê thật‚ nói cứ như biến quái vật thành tro dễ như không……)<br> ",
"(Nhưng Veera là pháp sư nổi tiếng ngay cả ở Perdion mà nhỉ?<br>Đáng lẽ cô ấy phải nhận ra ngay Verisa không dùng được ma pháp cỡ đó chứ……)<br> ",
"Vâng‚ nếu là chị thì quái vật chẳng là gì cả.<br> ",
"(……Ủa? Câu chuyện đang lệch khỏi dự đoán của mình rồi?)<br> ",
"Vì chị tuyệt vời lắm‚ nên để giúp mọi người‚<br>chắc chị phải vất vả lắm đúng không?<br> ",
"Những quái vật chỉ chị mới đánh bại được‚<br>những nguy cơ phải có ma pháp mạnh mới xử lý nổi…… nhiều lắm phải không?<br> ",
"Một mình chị chắc vất vả lắm. Nên em đến để giúp chị.<br> ",
"A…… ư…… khưư……!<br> ",
"(Mặt Verisa phức tạp kinh khủng……!<br>Biểu cảm pha trộn giữa vui sướng và khó xử!)<br> ",
"Q-quả không hổ là em gái chị‚ em hiểu rõ ghê!<br>Verisa-chan này được khắp nơi trông cậy nên bận tối mắt đấy♪<br> ",
"(Cô ta hùa theo luôn rồi! Dù thế nào cũng phóng đại quá mức rồi đấy!)<br> ",
"Đúng như em nghĩ. Không hổ là chị.<br> ",
"Từ giờ em cũng sẽ giúp chị‚ nên chị cứ yên tâm nhé.<br> ",
"Ừ-ừm…… đúng vậy‚ Veera đáng tin lắm‚ nhưng mà……<br> ",
"……À‚ Verisa? Nếu nói chuyện xong rồi thì giới thiệu cho tôi được không?<br> ",
"À‚ xin lỗi‚ xin lỗi.<br> ",
"Đây là em gái chị vừa nhắc tới‚ Veera.<br>Em ấy là pháp sư ưu tú chẳng thua gì chị‚ nên hãy thân với em ấy nhé♪<br> ",
"Xin lỗi vì chào hỏi muộn.<br>Em là Veera‚ được phái đến từ Perdion.<br> ",
"Ngài là Chỉ Huy…… phải không ạ?<br> ",
"Ừ‚ tôi là Chỉ Huy %user%.<br> ",
"Vâng‚ rất mong được ngài giúp đỡ.<br> ",
"……Fufu.<br> ",
"Hửm‚ sao vậy? Có gì buồn cười à?<br> ",
"Quả nhiên người đứng đầu căn cứ này là ngài Chỉ Huy và chị nhỉ.<br> ",
"Hể!? V-Veera? Sao em lại nghĩ vậy?<br> ",
"Vì trong phòng chỉ huy của Căn Cứ Tiền Tuyến<br>có ngài Chỉ Huy và chị mà.<br> ",
"Hai người là thành viên chủ chốt của căn cứ này‚<br>nên đang bàn về các chiến dịch sắp tới đúng không?<br> ",
"C-cái đó…… ưư…… Chị chỉ dùng nơi này để lười biếng ăn bánh một chút thôi……<br> ",
"Ừ‚ Verisa là thành viên chủ chốt thì không nghi ngờ gì.<br> ",
"A-anh ơi!?<br> ",
"Quả nhiên là vậy. Chị đáng tin cậy lắm đúng không?<br> ",
"Ừm‚ cô ấy có kiến thức ma pháp phong phú‚<br>và trông vậy thôi chứ cũng rất biết quan tâm.<br> ",
"Có cô ấy trong đội thì độ ổn định tăng hẳn.<br>Đúng là nhân lực quý giá.<br> ",
"Ngài thật sự hiểu giá trị của chị…… Quả không hổ là ngài Chỉ Huy.<br> ",
"Em thật sự mừng…… Có lẽ em có thể đi theo ngài.<br> ",
"Haha‚ căn cứ này không dư dả đến mức<br>để một pháp sư tài năng được lười biếng đâu!<br> ",
"Anh cậy có Veera ở đây nên lên mặt……<br>Anh ơi mà dám láo quá……!<br> ",
"Không‚ chuyện này tôi nói thật đấy.<br>Không ai thay thế được cô đâu.<br> ",
"Hự!? ……Trời ạ……<br>Đừng khen kiểu kỳ quặc vào lúc thế này chứ……<br> ",
"……Ngài Chỉ Huy‚ ngài thân với chị nhỉ?<br> ",
"Ừ‚ có thể nói cô ấy là cộng sự độc nhất của tôi.<br> ",
"Cái đó thật sự là nói quá rồi đó～!<br> ",
"Fufu…… hai người thân nhau thật.<br>Hiếm khi chị lại thả lỏng cảnh giác đến vậy……<br> ",
"Tôi cũng rất muốn thân với em nữa‚ Veera.<br> ",
"Vâng‚ ngài Chỉ Huy. Nếu ngài thân thiết với chị‚<br>em rất hoan nghênh.<br> ",
"A‚ anh ơi!<br>Đừng nhìn Veera bằng ánh mắt kỳ lạ chỉ vì em ấy dễ thương nhé?<br> ",
"Haha‚ để đáp lễ chuyện cô cứ gọi tôi là anh ơi suốt‚<br>tôi gọi cô là chị vợ cũng được đấy?<br> ",
"Ahaha…… này‚ anh ơi?<br>Trò đùa đó…… không vui…… chút nào…… đâu nhỉ～～～?<br> ",
"……Tôi sẽ không nói lần thứ hai‚<br>nên cô dừng chĩa sát khí vào tôi thì tôi mừng lắm……<br> ",
"……Fufu. Em mừng vì chị có vẻ vẫn khỏe.<br> ",
"Vậy‚ Veera. Lý do em đến căn cứ này là gì?<br> ",
"Tất nhiên là để chiến đấu cùng mọi người.<br> ",
"Một phần cũng là vì thế giới……<br>nhưng em đến căn cứ này vì muốn được làm việc cùng chị.<br> ",
"Xin hãy cho em tham gia các trận chiến ở đây……<br>tham gia cùng nhiệm vụ với chị được không ạ?<br> ",
"Ơ‚ ơơ!?<br>Đột nhiên cùng nhiệm vụ với chị…… thật sự ổn chứ?<br> ",
"Không sao‚ em nhất định sẽ làm được.<br> ",
"Hmm…… đúng vậy nhỉ……<br> ",
"(……Cử chỉ điềm tĩnh‚ thái độ tự tin.<br>Có thể thấy cô ấy là một pháp sư giỏi.)<br> ",
"(Nhưng ngược lại‚ cô ấy vẫn có gì đó trẻ con.<br>Như việc đánh giá Verisa cao lạ thường‚ hay có vẻ bám chấp vào cô ấy.)<br> ",
"Đúng lúc lắm. Được rồi.<br>Tôi sẽ để Veera đi cùng nhiệm vụ mà tôi định dẫn Verisa theo.<br> ",
"Thật sao ạ? Em vui quá……!<br> ",
"Hể～～!? Anh ơi‚ anh nghiêm túc đó hả……?<br> ",
"Tôi hiểu cô lo cho em gái‚ nhưng đây là nhiệm vụ hộ vệ đội vận chuyển.<br>Không phải chiến dịch nguy hiểm đến thế đâu.<br> ",
"Chị đâu có lo đâu nhé?<br>Nhưng…… không ngờ chị lại làm việc cùng Veera……<br> ",
]

def detect_newline(b):
    return '\r\n' if b'\r\n' in b else '\n'

def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def tag_counts(s):
    return sorted(re.findall(r'<[^>]+>', s))

def placeholders(s):
    return sorted(re.findall(r'%[A-Za-z0-9_]+%|%user%|<user>|\{\d+\}', s))

def replace_text_field(parts, trans):
    if parts[0] == 'title':
        parts[1] = trans
    elif parts[0] in ('message','messageTextUnder','messageTextCenter'):
        parts[2] = trans
    return parts

def text_field(parts):
    if parts[0]=='title': return parts[1] if len(parts)>1 else ''
    if parts[0] in ('message','messageTextUnder','messageTextCenter'): return parts[2] if len(parts)>2 else ''
    return None

raw=en_asset.read_bytes()
newline=detect_newline(raw)
bom=raw.startswith(b'\xef\xbb\xbf')
text=raw.decode('utf-8-sig')
lines=text.splitlines()
# preserve trailing final newline count by split below
split = text.split(newline)
# remove terminal empty segment for processing; will rejoin and append same terminal empties count
trailing_empty=0
while split and split[-1]=='':
    trailing_empty+=1; split.pop()

candidates=[]
for i,line in enumerate(split,1):
    if not line: continue
    cmd=line.split(',',1)[0]
    if cmd in commands:
        candidates.append((i,cmd,line))

if len(candidates)!=len(translations):
    raise SystemExit(f'translation count {len(translations)} != candidates {len(candidates)}')

new_lines=list(split)
records=[]
for idx,(line_no,cmd,line) in enumerate(candidates):
    parts=line.split(',')
    before_parts=list(parts)
    src_text=text_field(parts)
    trans=translations[idx]
    if ',' in trans:
        raise SystemExit(f'ASCII comma in translation #{idx+1}: {trans}')
    if tag_counts(src_text)!=tag_counts(trans):
        raise SystemExit(f'tag mismatch #{idx+1} line {line_no}: {tag_counts(src_text)} != {tag_counts(trans)}')
    # technical placeholders in EN asset must be preserved when present inside source text (%user%)
    for ph in placeholders(src_text):
        if ph not in trans:
            raise SystemExit(f'placeholder missing #{idx+1} {ph}')
    new_parts=replace_text_field(parts, trans)
    new_line=','.join(new_parts)
    if new_line.count(',') != line.count(','):
        raise SystemExit(f'delimiter mismatch line {line_no}')
    new_lines[line_no-1]=new_line
    records.append({
        'index': idx+1, 'line': line_no, 'command': cmd, 'status':'TRANSLATED',
        'source_en': src_text, 'translation_vi': trans,
        'delimiter_count': line.count(','), 'tag_count': len(tag_counts(src_text))
    })

out_text = newline.join(new_lines) + (newline * trailing_empty)
vi_asset.parent.mkdir(parents=True, exist_ok=True)
vi_asset.write_bytes((b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8'))

# diff
old_for_diff=text.splitlines(keepends=True)
new_for_diff=out_text.splitlines(keepends=True)
diff=''.join(difflib.unified_diff(old_for_diff,new_for_diff,fromfile=str(en_asset),tofile=str(vi_asset),lineterm=''))
(work/'focused_diff.md').write_text('# Focused Diff hmn_10080100001\n\n```diff\n'+diff+'\n```\n',encoding='utf-8')

summary={
 'scene':SCENE,
 'status':'GENERATED_PENDING_VERIFY',
 'generated_at':datetime.now(timezone.utc).isoformat(),
 'paths': {'en_asset':str(en_asset),'vi_asset':str(vi_asset),'ja_json':str(ja_json),'en_json':str(en_json),'workdir':str(work)},
 'source': {
   'sha256_en_asset': sha256(en_asset), 'sha256_ja_json': sha256(ja_json), 'sha256_en_json': sha256(en_json),
   'bom': bom, 'newline': 'CRLF' if newline=='\r\n' else 'LF', 'line_count': len(lines),
 },
 'candidate_counts': {c:sum(1 for _,cmd,_ in candidates if cmd==c) for c in sorted(commands)},
 'text_records_total': len(candidates),
 'records': records,
 'translation_notes': [
   'JP primary; EN asset used for line/tag alignment.',
   'Commander/司令官 -> Chỉ Huy.',
   'Speaker names and charaload names preserved.',
   'ASCII commas avoided inside Vietnamese text fields; U+201A used where needed.',
   'No H18 content present in this scene.'
 ],
 'unresolved': []
}
(work/'manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
qa={
 'scene':SCENE,
 'qa_status':'PENDING_INDEPENDENT_VERIFY',
 'structural_self_check': {'line_count_match': True, 'delimiter_counts_match': True, 'tag_counts_match': True, 'placeholder_counts_match': True, 'ascii_comma_in_vi_text_fields': 0},
 'issues': [],
 'records_checked': len(candidates)
}
(work/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'written':str(vi_asset),'workdir':str(work),'records':len(candidates),'counts':summary['candidate_counts']},ensure_ascii=False))
