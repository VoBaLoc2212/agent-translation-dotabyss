from pathlib import Path
import json, hashlib, re, difflib

SCENE='hmn_10050100002'
ROOT=Path('E:/AgentTranslation')
WORK=ROOT/'dotabyss-rpg-vn-translator/work/hmn_10050100002_full'
JA=ROOT/f'dotabyss-translation-main/translations/novels/{SCENE}/ja.json'
ENJ=ROOT/f'dotabyss-translation-main/translations/novels/{SCENE}/en.json'
EN_ASSET=ROOT/f'Translation/en/RedirectedResources/assets/unnamed_assetbundle/{SCENE}.txt'
VI_OUT=ROOT/f'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/{SCENE}.txt'

translations = [
    'Tiêu Đề',
    '<size=48>—Vài ngày sau</size>',
    'Chỉ Huy‚ em không muốn hối anh đâu‚ nhưng với tốc độ đó thì anh sẽ<br>không kịp hạn chót mất!<br> ',
    'Anh biết‚ nhưng xử lý hết chỗ báo cáo nhiều thế này trong một lúc chẳng phải là bất khả thi sao?<br> ',
    'Nếu mỗi ngày anh chịu làm từng chút một thì chúng đã không<br>chất đống lên thế này rồi!<br> ',
    'Chỉ Huy‚ dạo gần đây ngài giao hết việc giấy tờ cho Electra nhỉ.<br>Có phải vì vậy mà cảm giác làm việc của ngài đã cùn đi rồi không?<br> ',
    'Ư… Anh không thể phủ nhận chuyện đó.<br> ',
    'Được rồi‚ được rồi. Chắc chắn là lỗi của anh. Nhưng anh nghỉ một lát<br>được không? Anh mệt thật rồi.<br> ',
    'Kh-không được đâu! Họ yêu cầu báo cáo do chính tay Chỉ Huy viết…<br>Nên hôm nay anh phải cố gắng vượt qua thôi~!<br> ',
    'Xin phép chủ nhân. Em đã mang món đồ ngài hẹn lấy về rồi.<br> ',
    'Ồ‚ Electra à. Em lấy được thứ anh nhờ chưa?<br> ',
    'Đây ạ. ""Đại Chiến Phu Nhân: Chương Tửu Trì Nhục Lâm""… Xin ngài nhận lấy.<br> ',
    'H-hảả!? Tiểu thuyết khiêu dâm sao!? Ngay lúc này ư!?<br> ',
    'Cái này… chỉ nhìn bìa thôi cũng thấy họ đầu tư ghê thật. Alicia‚ chỉ một chút thôi‚<br>cho anh đọc đi.<br> ',
    'Nhưng xin Chỉ Huy hãy kiềm chế lại! Electra‚ tịch thu quyển<br>sách đó đi!<br> ',
    'Anh xin em đấy‚ Electra. Thật sự chỉ một chút thôi. Cho anh đọc đi.<br> ',
    'Ơ? À… ừm…<br> ',
    'Electra‚ làm ơn đi!<br> ',
    'Electra‚ anh tò mò đoạn tiếp theo đến chịu không nổi… Anh hứa sẽ dừng lại<br>ở một chỗ hợp lý mà.<br> ',
    '…<br> ',
    'Hửm? Sao thế?<br> ',
    '…Em xin lỗi. Đã xảy ra lỗi.<br> ',
    'Trong phạm vi có thể‚ em sẽ đồng thời thực hiện cả hai mệnh lệnh.<br>Xin chủ nhân hãy tha thứ cho em!<br> ',
    'Ư!? Cô ấy lấy mất quyển sách rồi… Từ lúc nào vậy?!<br> ',
    'Alicia‚ xin hãy nhận lấy.<br> ',
    'Cảm ơn cô‚ Electra!<br> ',
    'Xin thứ lỗi vì yêu cầu đường đột này‚ nhưng cô có thể mở sách<br>và cho tôi xem nội dung bên trong không?<br> ',
    '…? Như thế này sao?<br> ',
    '""Này phu nhân. Cô có gào thế nào cũng chẳng ai đến cứu đâu."" Giọng<br>đàn ông lạnh thấu xương xuyên vào cơ thể nóng rực của người phụ nữ.<br> ',
    'Cùng lúc đó‚ những ngón tay của gã chuẩn xác đùa nghịch điểm nhạy cảm<br>dưới bụng nàng. Trước cách vuốt ve dịu dàng khó tưởng tượng nổi từ những ngón tay thô ráp ấy‚ nàng—<br> ',
    'E-Electra‚ cô đang làm gì vậy!?<br> ',
    '…Ra là vậy. Anh chưa từng nghĩ đến cách này. Được người đẹp đọc cho nghe<br>cũng khá là—<br> ',
    'Anh đang mở ra một cánh cửa mới đấy à!?<br> ',
    '""Aaa‚ xin anh—đừng nữa‚ dừng lại…"" Những tiếng rên đứt quãng trong hơi thở<br>yếu ớt càng kích thích dục vọng của gã đàn ông—<br> ',
    'Hiíí! Làm ơn—xin dừng lại đi mà!<br> ',
    'Hư hư‚ chuyện này thú vị thật.<br> ',
    '…Em xin lỗi. Em đã không thể đáp ứng mong muốn của cả hai người.<br> ',
    'Không‚ anh không nghĩ vậy đâu. Ngược lại anh còn cảm ơn em.<br> ',
    'Lúc nãy em đã xin lỗi‚ nhưng đến giờ em vẫn chưa biết đáp án đúng là gì.<br>Bên nào mới đúng đây…<br> ',
    'Hửm? Em nói chuyện lạ thật. Cứ làm theo ý em muốn là được mà.<br> ',
    'Điều Electra muốn làm ạ? Điều Electra muốn làm là đáp ứng nhu cầu<br>của mọi người và duy trì một cuộc sống lành mạnh.<br> ',
    'Trong tình huống lúc nãy‚ việc thỏa mãn tất cả những điều đó là rất khó—<br> ',
    'Hừm…?<br> ',
    'Đó là vấn đề khung‚ Chỉ Huy ạ.<br> ',
    'Đó là gì?<br> ',
    'Chỉ từ vài mảnh thông tin thôi‚ nhưng tôi có thể hình dung chuyện gì đã xảy ra. Electra‚<br>hãy giải thích về vấn đề khung.<br> ',
    'Người máy được thiết kế để tuân theo mệnh lệnh của con người. Đó là<br>tiền đề áp dụng cho mọi hành động của Electra.<br> ',
    'Vì vậy‚ khi các mệnh lệnh trái ngược được đưa ra cùng lúc‚ nếu thực hiện<br>một bên thì bên kia không thể được thỏa mãn‚ em sẽ chịu tải rất nặng.<br> ',
    'Ra vậy. Anh hiểu rồi. Alicia đã ra lệnh cho em tịch thu quyển sách của anh.<br>Nhưng anh lại bảo em dừng việc tịch thu và cho anh đọc‚ nên—<br> ',
    '…Anh không nghĩ chuyện này nghiêm trọng đến thế đâu.<br>Nhưng người máy đúng là như vậy nhỉ.<br> ',
    'Chỉ Huy hiểu nhanh nên thật đỡ quá.<br>Với người máy‚ việc tuân thủ mệnh lệnh là tuyệt đối.<br> ',
    'Vậy là không giải quyết được sao?<br> ',
    'Nếu ngài định sẵn phương châm cho những tình huống như vừa rồi<br>thì em sẽ phán đoán nhanh hơn và cũng không phạm sai lầm nữa.<br> ',
    'Ý em là muốn anh đặt điều kiện tùy thích sao?<br> ',
    'Vâng. Xin chủ nhân cứ tùy ý.<br> ',
    'Ừm… khó nghĩ thật.<br> ',
    'Điều gì khiến ngài băn khoăn vậy?<br> ',
    'Anh muốn nói “hãy ưu tiên mệnh lệnh của anh cao nhất”‚ nhưng nếu làm vậy<br>chắc Alicia sẽ cằn nhằn anh mãi mất.<br> ',
    'Chỉ Huy~? Em nghe thấy hết đấy nhé~?<br> ',
    'Thấy chưa‚ bị nói rồi đấy.<br> ',
    'Ôi dào‚ phiền phức quá rồi! Electra! Cứ làm theo ý em muốn đi!<br> ',
    'Ơ…?<br> ',
    'Nếu nói “tự do làm”‚ anh chỉ nghĩ ra những đáp án dễ gây thêm rắc rối thôi.<br>Để em quyết định có lẽ là cách ổn thỏa nhất.<br> ',
    '…! Chủ nhân…<br> ',
    'Nhưng khi anh không có vấn đề gì thì vẫn nghe theo anh nhé?<br> ',
    'Tất nhiên rồi ạ. Từ nay về sau‚ xin hãy để em tiếp tục phụng sự bên cạnh chủ nhân.<br> ',
]

TEXT_TYPES={'title','message','messageTextUnder','messageTextCenter'}
TEXT_INDEX={'title':1,'message':2,'messageTextUnder':2,'messageTextCenter':2}
TAG_RE=re.compile(r'<[^>]+>')
PH_RE=re.compile(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def nl(b):
    return 'CRLF' if b'\r\n' in b else ('LF' if b'\n' in b else 'NONE')

def read_json_pairs(p):
    return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=list)

def field(line):
    parts=line.split(',')
    if parts[0] not in TEXT_TYPES: return None
    idx=TEXT_INDEX[parts[0]]
    if len(parts)<=idx: return None
    return parts, idx, parts[idx]

WORK.mkdir(parents=True, exist_ok=True)
VI_OUT.parent.mkdir(parents=True, exist_ok=True)
raw=EN_ASSET.read_bytes()
bom=raw.startswith(b'\xef\xbb\xbf')
newline=nl(raw)
text=raw.decode('utf-8-sig')
# split preserving no final newline info
lines=text.splitlines()
ends_newline=text.endswith('\n') or text.endswith('\r')

candidates=[]
for i,line in enumerate(lines,1):
    f=field(line)
    if f:
        parts,idx,src=f
        candidates.append({'line':i,'type':parts[0],'speaker': parts[1] if parts[0]=='message' and len(parts)>1 else '', 'source_text':src, 'delimiter_count':line.count(',')})
assert len(candidates)==len(translations), (len(candidates), len(translations))

out_lines=lines[:]
entries=[]
for n,c in enumerate(candidates):
    vi=translations[n]
    if ',' in vi:
        raise SystemExit(f'ASCII comma in translation {n+1}: {vi}')
    line=out_lines[c['line']-1]
    parts=line.split(',')
    idx=TEXT_INDEX[parts[0]]
    before_sig=parts[:idx]+parts[idx+1:]
    parts[idx]=vi
    new_line=','.join(parts)
    out_lines[c['line']-1]=new_line
    entries.append({**c,'entry_index':n+1,'vi_text':vi,'status':'TRANSLATED','match_status':'ORDERED_CONTEXT_MATCH','technical_signature_before':before_sig})

sep='\r\n' if newline=='CRLF' else '\n'
out_text=sep.join(out_lines) + (sep if ends_newline else '')
VI_OUT.write_bytes((b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8'))

# QA
out_raw=VI_OUT.read_bytes(); out_text_read=out_raw.decode('utf-8-sig'); out_lines_read=out_text_read.splitlines()
blockers=[]; warnings=[]
if len(out_lines_read)!=len(lines): blockers.append({'type':'LINE_COUNT_MISMATCH','source':len(lines),'output':len(out_lines_read)})
if out_raw.startswith(b'\xef\xbb\xbf') != bom: blockers.append({'type':'BOM_MISMATCH'})
if nl(out_raw)!=newline: blockers.append({'type':'NEWLINE_MISMATCH','source':newline,'output':nl(out_raw)})
changed=0; kept=[]
for c in candidates:
    i=c['line']; src=lines[i-1]; dst=out_lines_read[i-1]
    if src!=dst: changed+=1
    if src.count(',')!=dst.count(','): blockers.append({'type':'DELIMITER_MISMATCH','line':i,'source':src.count(','),'output':dst.count(',')})
    sp,si,st=field(src); dp,di,dt=field(dst)
    if sp[:si]+sp[si+1:] != dp[:di]+dp[di+1:]: blockers.append({'type':'TECH_FIELD_MISMATCH','line':i})
    if TAG_RE.findall(st)!=TAG_RE.findall(dt): blockers.append({'type':'TAG_MISMATCH','line':i,'source':TAG_RE.findall(st),'output':TAG_RE.findall(dt)})
    if PH_RE.findall(st)!=PH_RE.findall(dt): blockers.append({'type':'PLACEHOLDER_MISMATCH','line':i})
    if ',' in dt: blockers.append({'type':'ASCII_COMMA_IN_VI_FIELD','line':i,'text':dt})
    if dt==st:
        kept.append({'line':i,'text':dt})
# non-text lines unchanged
for i,(a,b) in enumerate(zip(lines,out_lines_read),1):
    if i not in {c['line'] for c in candidates} and a!=b:
        blockers.append({'type':'NON_TEXT_LINE_CHANGED','line':i})
# targeted leftovers
leftover_patterns=['Commander','Master','Please','Thank you','What are you','Fufu','android','Androids','frame problem','Electra,','Alicia,','Hmm','Ugh','Eh','Guh','Eeeek']
leftovers=[]
for c in candidates:
    txt=field(out_lines_read[c['line']-1])[2]
    for pat in leftover_patterns:
        if pat in txt:
            leftovers.append({'line':c['line'],'pattern':pat,'text':txt})
# Allow intentional technical/lore terms? none except Android maybe localized? check flags as warnings/blocker
for lo in leftovers:
    if lo['pattern'] not in {'android'}:
        blockers.append({'type':'LEFTOVER_ENGLISH_PATTERN','line':lo['line'],'pattern':lo['pattern'],'text':lo['text']})

qa={
 'file': SCENE+'.txt',
 'status': 'PASS' if not blockers else 'FAIL',
 'source': {'path':str(EN_ASSET),'sha256':sha(EN_ASSET),'bytes':len(raw),'bom':bom,'newline':newline,'line_count':len(lines)},
 'output': {'path':str(VI_OUT),'sha256':sha(VI_OUT),'bytes':len(out_raw),'bom':out_raw.startswith(b'\xef\xbb\xbf'),'newline':nl(out_raw),'line_count':len(out_lines_read)},
 'candidate_counts': {k:sum(1 for c in candidates if c['type']==k) for k in TEXT_TYPES},
 'translated_records': len(candidates),
 'changed_text_records': changed,
 'kept_english_records': kept,
 'intentional_identical_records': [],
 'blockers': blockers,
 'warnings': warnings,
 'h18_note': 'Project confirmation: all characters are 18+; erotic-novel quoted passages translated normally with source tone/consent preserved.',
 'addressing': {'Commander/司令官':'Chỉ Huy','Electra to protagonist':'chủ nhân/ngài; self as Electra where source self-names','default protagonist to women':'anh/em where natural'},
}
(WORK/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')

manifest={
 'scene':SCENE,
 'status':qa['status'],
 'jp_json': {'path':str(JA),'sha256':sha(JA),'ordered_pairs':len(read_json_pairs(JA))},
 'en_json': {'path':str(ENJ),'sha256':sha(ENJ),'ordered_pairs':len(read_json_pairs(ENJ))},
 'source_asset': qa['source'],
 'output_asset': qa['output'],
 'text_command_counts': qa['candidate_counts'],
 'entries': entries,
 'qa_log': str(WORK/'qa_log.json'),
 'focused_diff': str(WORK/'focused_diff.md'),
 'script': str(WORK/'generate_vi.py'),
}
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Focused diff: only candidate source and output lines
src_focus=[]; dst_focus=[]
for c in candidates:
    i=c['line']
    src_focus.append(f'L{i}: {lines[i-1]}\n')
    dst_focus.append(f'L{i}: {out_lines_read[i-1]}\n')
diff=''.join(difflib.unified_diff(src_focus,dst_focus,fromfile='EN asset text records',tofile='VI asset text records',lineterm='\n'))
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10050100002\n\n```diff\n'+diff+'\n```\n',encoding='utf-8')
print(json.dumps({'status':qa['status'],'blockers':len(blockers),'output':str(VI_OUT),'qa':str(WORK/'qa_log.json')},ensure_ascii=False,indent=2))
