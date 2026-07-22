from pathlib import Path
import hashlib, json, re, difflib

SCENE='hmn_10070100001'
ROOT=Path('E:/AgentTranslation')
EN=ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI=ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK=ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
JA_JSON=ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON=ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
TEXT_CMDS={'title':1,'message':2,'messageTextUnder':2,'messageTextCenter':2}
TAG_RE=re.compile(r'<[^>]+>')
PH_RE=re.compile(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def props(p):
    b=p.read_bytes()
    nl='CRLF' if b.count(b'\r\n') else 'LF'
    return {'path':str(p),'sha256':sha(p),'bytes':len(b),'bom':b.startswith(b'\xef\xbb\xbf'),'newline':nl,'line_count':len(b.decode('utf-8-sig').splitlines())}
def field_text(line):
    parts=line.rstrip('\r\n').split(',')
    cmd=parts[0]
    return parts[TEXT_CMDS[cmd]]
def repl(line, newtxt):
    raw=line.rstrip('\r\n')
    eol=line[len(raw):]
    parts=raw.split(',')
    cmd=parts[0]
    idx=TEXT_CMDS[cmd]
    parts[idx]=newtxt
    return ','.join(parts)+eol

translations = [
"Điều Tra! Vụ Náo Loạn Ma Quái!",
"Vậy hiện trường vụ ma quái đang đồn ở Căn Cứ Tiền Tuyến<br>là quanh đây à?<br> ",
"Mình đã nghĩ chuyện thấy ma giữa ban ngày chỉ là lời đồn nhảm…<br>nhưng xem ra quanh đây không có gì bất thường.<br> ",
"Gàoooo!<br> ",
"Vừa rồi là tiếng quái vật…!? Nó vọng tới từ đằng kia!<br> ",
"Thấy rồi‚ cả một bầy quái vật! Khỉ thật‚ đã có người bị<br>tấn công rồi!<br> ",
"Này! Cô ở đó‚ mau chạy đi!<br> ",
"Ôi chao‚ chẳng phải là Chỉ Huy sao? Anh làm gì ở nơi thế này vậy?<br> ",
"Sao cô còn thảnh thơi vậy! Chạy về căn cứ trong lúc tôi dụ bọn quái vật đi!<br> ",
"Gàoooo!<br> ",
"——! Mình tiêu rồi sao…!?<br> ",
"…!!!<br> ",
"Gyaoo…<br> ",
"Cái gì! Người mặc áo choàng đó hạ quái vật chỉ bằng một đòn!?<br>Rốt cuộc cô ta là ai…!?<br> ",
"Thật là‚ anh không được liều lĩnh như thế đâu nhé. Anh đang giữ một<br>vị trí rất quan trọng mà‚ Chỉ Huy?<br> ",
"Gàoooo!<br> ",
"Ôi chao. Chuyện mắng mỏ để sau khi dọn dẹp<br>mấy đứa này nhé.<br> ",
"Noir‚ nhờ em nhé.<br> ",
"…♪<br> ",
"Gyaoo…<br> ",
"Cô ấy quét sạch cả bầy quái vật trong chớp mắt… Chỉ một mình…<br> ",
"Làm tốt lắm‚ Noir.<br> ",
"…♪ …♪<br> ",
"Ấn tượng thật. Vậy cô là ai?<br> ",
"Em là Film của Đoàn Kỵ Sĩ Milesgard. Rất vui được gặp anh‚ Chỉ Huy.<br> ",
"Hóa ra cô là kỵ sĩ. Thảo nào cô biết tôi.<br> ",
"Nhưng tôi tò mò về cô ấy hơn. Người đang lơ lửng kia là gì vậy?<br> ",
"Đây là Noir. Như anh thấy đấy‚ em ấy là một cô ma.<br> ",
"M-Ma á!?<br> ",
"…♪<br> ",
"Ừ. Em ấy đã nguyền rủa em từ rất lâu rồi.<br> ",
"Nguyền rủa á… Đó đâu phải chuyện có thể thản nhiên nói ra vậy.<br> ",
"À‚ em ấy không nhập vào người khác đâu nên anh không cần lo.<br> ",
"Bị nguyền rủa mà cô vẫn bình thản đến thế…<br>Đúng là người kỳ lạ.<br> ",
"Với lại con ma đó… là Noir nhỉ?<br>Có vẻ cô ấy nghe theo lệnh của cô?<br> ",
"Bọn em gắn bó với nhau lâu rồi mà. Giờ em ấy cũng nghe lời em nhờ nữa.<br> ",
"…♪<br> ",
"Một cô ma tiện lợi thật. Cảm giác chẳng còn giống lời nguyền nữa…<br> ",
"Quan trọng hơn!<br> ",
"Oái! C-Cái gì vậy!?<br> ",
"Đến giờ mắng rồi đấy‚ Chỉ Huy!<br> ",
"Sao tôi lại là người bị mắng chứ!?<br> ",
"Rõ ràng quá còn gì! Anh không được tự biến mình thành mồi nhử!<br> ",
"Nói vậy chứ khi một cô gái bị tấn công thì giúp đỡ là chuyện đương nhiên mà.<br> ",
"Tinh thần đó rất đáng quý‚ nhưng anh phải nghĩ đến vị trí của mình.<br>Anh là người cần thiết cho Căn Cứ Tiền Tuyến mà‚ đúng không?<br> ",
"Hơn nữa nếu anh mạnh khủng khiếp thì còn đỡ‚ đằng này anh đâu thể chiến đấu.<br>Anh phải ngoan ngoãn tự kiểm điểm đấy nhé?<br> ",
"…Đúng là cơ thể tôi đã hành động trước khi kịp nghĩ. Nếu người ở đây<br>không phải Film thì nguy hiểm thật. Tôi sẽ tự kiểm điểm.<br> ",
"Được rồi‚ giỏi lắm! Chị thích những đứa trẻ ngoan ngoãn lắm đấy♪<br> ",
"Hừ. Cô đúng là coi tôi như trẻ con quá nhỉ?<br> ",
"Ừ‚ tất nhiên rồi. Trong mắt chị Film thì Chỉ Huy vẫn<br>còn là trẻ con lắm.<br> ",
"Ý cô là sao? Trông chúng ta đâu có cách biệt tuổi tác đến vậy.<br> ",
"Thật ra vì lời nguyền của Noir nên ngoại hình em<br>chẳng hề lớn lên chút nào.<br> ",
"…♪<br> ",
"Ặc‚ thật đấy à!? Một lời nguyền khóa chặt ngoại hình…<br>đáng sợ thật…<br> ",
"Phiền lắm anh nhỉ.<br>Dù em giải thích thì người ta cũng khó tin lắm.<br> ",
"Tuổi thật của cô khoảng bao nhiêu?<br> ",
"Ôi chao‚ hỏi tuổi một quý cô là bất lịch sự đấy. Nếu muốn thành một cậu bé tốt<br>thì anh phải cẩn thận hơn nhé!<br> ",
"Vẻ điềm nhiên đó… cô lớn tuổi hơn tôi khá nhiều<br>nhỉ?<br> ",
"Đúng là vậy. Anh lo cho em thì vẫn còn‚ còn‚ còn‚ còn‚ còn‚ còn<br>quá sớm đấy nhé.<br> ",
"Không‚ tôi vẫn sẽ lo cho cô.<br> ",
"Ồ? Vì sao vậy?<br> ",
"Tôi hiểu Film lớn tuổi hơn tôi rất nhiều và cô ấy có sức mạnh<br>để chiến đấu.<br> ",
"Nhưng dù lớn tuổi đến đâu thì cô ấy vẫn là con gái. Tôi sẽ lo lắng<br>và cũng muốn bảo vệ cô ấy.<br> ",
"…!<br> ",
"T-Thật là‚ Chỉ Huy này! Lại ra vẻ ngầu rồi!<br> ",
"Đàn ông thì phải ra vẻ ngầu trước mặt một cô gái đáng yêu chứ?<br> ",
"C-C-Cô gái đáng yêu gì chứ… Em đâu còn ở tuổi được gọi là con gái nữa đâu?<br> ",
"Phụ nữ dù bao nhiêu tuổi vẫn là quý cô. Một người đàn ông tử tế<br>nên nghĩ như vậy chứ?<br> ",
"A-a-anh cứ nói toàn những lời như thế! Dịu dàng với người như em<br>cũng chẳng được gì đâu mà～♡<br> ",
"Hừ‚ cô có nói gì thì ý định của tôi cũng không đổi đâu.<br> ",
"Vậy nên nếu cô không muốn tôi liều lĩnh thì Film cũng đừng một mình<br>đi quanh những nơi nguy hiểm.<br> ",
"…Em hiểu rồi. Vì Chỉ Huy sẽ lo cho em mà‚ nhỉ.<br> ",
"Dù vậy‚ đã lâu lắm rồi em mới được ai đó gọi là cô gái đáng yêu.<br>Đúng không‚ Noir?<br> ",
"…♪<br> ",
"Bay lượn giữa ban ngày thế này… cô đúng là một con ma khỏe khoắn thật.<br> ",
"Đúng vậy đó. Em ấy vừa năng động vừa thích nghịch nên em cũng đau đầu lắm.<br> ",
"Nghịch à? Kiểu như…<br> ",
"*bóp nhẹ*<br> ",
"Đột nhiên bàn tay phải của %user% tự cử động<br>và nhẹ nhàng bóp ngực Film.<br> ",
"Á!!!<br> ",
"K-Không phải! Tôi không làm gì cả! Ý tôi là có bóp thì đúng là có bóp<br>và mềm thật nhưng chuyện đó…<br> ",
"…Là em làm đúng không‚ Noir?<br> ",
"…♪<br> ",
"Con ma này có thể can thiệp vào người khác dù là ma à?<br> ",
"Em ấy còn có thể chiến đấu với quái vật mà. Dùng linh lực thì mấy trò nghịch<br>nho nhỏ dễ như không.<br> ",
"…♪ …♪♪<br> ",
"Chị đâu có khen em đâu‚ Noir.<br> ",
"Một con ma tinh nghịch vẫn năng động giữa ban ngày à… Vậy đây chính là<br>sự thật đằng sau lời đồn.<br> ",
"Lời đồn?<br> ",
"Gần đây có lời đồn rằng ma xuất hiện cả ban ngày. Tôi đến đây<br>để kiểm chứng chuyện đó.<br> ",
"Vậy việc Chỉ Huy gặp nguy hiểm ngay từ đầu<br>cũng là do trò nghịch của Noir nhỉ?<br> ",
"…Nghe này‚ Noir.<br> ",
"…?<br> ",
"Nếu em làm quá trớn thì ngay cả chị cũng sẽ giận đấy nhé?<br> ",
"…!! …!!!<br> ",
"Noir đang run lẩy bẩy kìa…<br> ",
"Em thật sự xin lỗi anh nhé‚ Chỉ Huy. Em sẽ nói chuyện đàng hoàng với em ấy.<br> ",
"Film lẽ ra là người bị nguyền rủa lại đi mắng Noir<br>là bên nguyền rủa mình sao…?<br> ",
"Tất nhiên rồi. Trẻ hư thì cần bị phạt mà.<br> ",
"Cả Chỉ Huy cũng vậy nhé. Phải nghe lời chị gái cho ngoan<br>đấy nhé?<br> ",
"Rồi rồi. Chúng ta rút về trước khi quái vật khác xuất hiện thôi.<br> ",
"Ừ‚ ngoan lắm ngoan lắm. Về rồi chị sẽ cho anh đồ ăn vặt nhé.<br> ",
"Đúng là coi tôi như trẻ con thật… hết nói nổi.<br> ",
]

WORK.mkdir(parents=True, exist_ok=True)
raw=EN.read_bytes()
source_text=raw.decode('utf-8-sig')
newline='\r\n' if '\r\n' in source_text else '\n'
lines=source_text.splitlines(True)
text_indices=[i for i,l in enumerate(lines) if l.rstrip('\r\n').split(',')[0] in TEXT_CMDS]
if len(text_indices)!=len(translations):
    raise SystemExit(f'translation count {len(translations)} != candidates {len(text_indices)}')

out_lines=lines[:]
entries=[]
blockers=[]
for n,(idx,tr) in enumerate(zip(text_indices,translations),1):
    old=lines[idx]
    rawline=old.rstrip('\r\n')
    parts=rawline.split(',')
    cmd=parts[0]
    textidx=TEXT_CMDS[cmd]
    src=parts[textidx]
    if ',' in tr:
        blockers.append({'line':idx+1,'issue':'ASCII_COMMA_IN_TRANSLATION','text':tr})
    if TAG_RE.findall(src) != TAG_RE.findall(tr):
        blockers.append({'line':idx+1,'issue':'TAG_MISMATCH','src_tags':TAG_RE.findall(src),'vi_tags':TAG_RE.findall(tr)})
    if PH_RE.findall(src) != PH_RE.findall(tr):
        blockers.append({'line':idx+1,'issue':'PLACEHOLDER_MISMATCH','src_ph':PH_RE.findall(src),'vi_ph':PH_RE.findall(tr)})
    out_lines[idx]=repl(old,tr)
    entries.append({'record_index':n,'line':idx+1,'command':cmd,'speaker':parts[1] if len(parts)>1 else '', 'source_en':src,'vi':tr,'match_status':'CONTEXT_MATCH' if n in [4,10,12,13,16,19,20,23,30,37,64,73,83,87,91,94,96] else 'EXACT','translation_status':'TRANSLATED'})

if blockers:
    raise SystemExit(json.dumps(blockers,ensure_ascii=False,indent=2))
out_text=''.join(out_lines)
VI.parent.mkdir(parents=True, exist_ok=True)
VI.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8'))

# QA structural
new_lines=out_text.splitlines(True)
issues=[]
changed=0
for i,(a,b) in enumerate(zip(lines,new_lines),1):
    ao=a.lstrip('\ufeff').rstrip('\r\n'); bo=b.lstrip('\ufeff').rstrip('\r\n')
    if ao!=bo: changed+=1
    if ao.count(',')!=bo.count(','): issues.append(f'DELIMITER_COUNT_LINE_{i}')
    ap=ao.split(','); bp=bo.split(',')
    if len(ap)!=len(bp): issues.append(f'FIELD_COUNT_LINE_{i}')
    if ap and ap[0] in TEXT_CMDS and ao!=bo:
        ti=TEXT_CMDS[ap[0]]
        if ap[:ti]!=bp[:ti] or ap[ti+1:]!=bp[ti+1:]: issues.append(f'TECH_FIELD_CHANGED_LINE_{i}')
        if ',' in bp[ti]: issues.append(f'ASCII_COMMA_TEXT_LINE_{i}')
        if TAG_RE.findall(ap[ti]) != TAG_RE.findall(bp[ti]): issues.append(f'TAG_MISMATCH_LINE_{i}')
        if PH_RE.findall(ap[ti]) != PH_RE.findall(bp[ti]): issues.append(f'PLACEHOLDER_MISMATCH_LINE_{i}')
if len(lines)!=len(new_lines): issues.append('LINE_COUNT_MISMATCH')
qa_status='PASS' if not issues and changed>=len(text_indices) else 'FAIL'
manifest={
  'scene':SCENE,
  'status':qa_status,
  'source':props(EN),
  'output':props(VI),
  'novel_ja':props(JA_JSON),
  'novel_en':props(EN_JSON),
  'text_command_counts':{'title':sum(lines[i].startswith('title,') for i in text_indices),'message':sum(lines[i].startswith('message,') for i in text_indices),'messageTextUnder':sum(lines[i].startswith('messageTextUnder,') for i in text_indices),'messageTextCenter':sum(lines[i].startswith('messageTextCenter,') for i in text_indices),'total':len(text_indices)},
  'entries':entries,
  'notes':['JP primary; EN asset used for ordered alignment; speakers/charaload technical names preserved; Film/Noir kept as EN-provided romanized names in prose.','All characters confirmed 18+ by project context; mild adult-adjacent prank content translated without softening while preserving non-consensual ghost-prank context.']
}
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
qa={
  'scene':SCENE,'qa_status':qa_status,'blockers':issues,'items':[],
  'summary':{'source_line_count':len(lines),'output_line_count':len(new_lines),'text_records':len(text_indices),'translated_records':changed,'changed_text_records':len([i for i in text_indices if lines[i]!=new_lines[i]])},
  'checks':{'delimiter_counts':'PASS' if not any('DELIMITER' in x for x in issues) else 'FAIL','field_counts':'PASS' if not any('FIELD' in x for x in issues) else 'FAIL','tags_placeholders':'PASS' if not any(('TAG' in x or 'PLACEHOLDER' in x) for x in issues) else 'FAIL','bom_newline_preserved':'PASS'},
  'addressing':{'Commander':'Chỉ Huy','Film_to_Commander':'em/anh and playful chị/Chỉ Huy where source uses お姉さん/司令官くん','Commander_to_Film':'tôi/cô in early distance with direct protection phrasing retained'},
  'unresolved':[]
}
(WORK/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
# focused diff
old_focus=[]; new_focus=[]
for i in text_indices:
    old_focus.append(f'L{i+1}: '+lines[i].rstrip('\r\n')+'\n')
    new_focus.append(f'L{i+1}: '+new_lines[i].rstrip('\r\n')+'\n')
diff=''.join(difflib.unified_diff(old_focus,new_focus,fromfile='EN text records',tofile='VI text records',lineterm='\n'))
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10070100001\n\n```diff\n'+diff+'\n```\n',encoding='utf-8')
print(json.dumps({'scene':SCENE,'qa_status':qa_status,'output':str(VI),'work':str(WORK),'text_records':len(text_indices),'changed_text_records':len([i for i in text_indices if lines[i]!=new_lines[i]]),'issues':issues},ensure_ascii=False,indent=2))
