from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

SCENE='hmn_10030100001'
ROOT=Path('E:/AgentTranslation')
JP_PATH=ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON_PATH=ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
EN_ASSET=ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET=ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK=ROOT/'dotabyss-rpg-vn-translator/work/hmn_10030100001_full'
WORK.mkdir(parents=True, exist_ok=True)

TRANSLATIONS = [
"Mở Phiên Đấu Giá!",
"Ở căn cứ này sắp tổ chức đấu giá… sao ạ?",
"Dự kiến vài ngày nữa sẽ diễn ra tại hội trường ngoại ô đang được chuẩn bị.<br>Nghe nói ngoài những ma đạo cụ quý hiếm‚ còn có cả các món giá mềm để người bình thường cũng có thể đấu giá.",
"Ôi‚ một sự kiện tuyệt vời quá.<br>Dòng máu thương nhân trong em đang sôi lên rồi đây.",
"Đây là catalogue các món được đem ra đấu giá nhỉ…<br>Oa‚ toàn những món tuyệt quá!",
"Vậy ông chủ muốn bàn với em chuyện gì nào?",
"Thật ra anh muốn nhờ Marina giúp trong buổi đấu giá.<br>Nhìn qua danh mục thì có cả vũ khí và ma thạch có thể giúp tăng cường chiến lực cho căn cứ.",
"Nhưng ngân sách mua sắm vật tư của chúng ta có hạn‚<br>nên tôi muốn mua được càng rẻ càng tốt…",
"Ra là vậy‚ chuyện là thế nhỉ.<br>Có món muốn lấy trong buổi đấu giá… ra vậy sao?",
"Sao hả Marina‚ anh nhờ em được không?",
"Việc ông chủ tin tưởng nhờ cậy em‚<br>em thật sự rất vui. Em không nói dối đâu nhé?",
"Nhưng em xin lỗi.<br>Hôm đó em có việc không thể bỏ được mất rồi～.",
"Vậy à. Thế thì đành chịu thôi.<br>Hiểu rồi‚ anh sẽ tự xoay xở vậy.",
"Nhờ anh nhé‚ Chỉ Huy.<br>Tôi sẽ cố gom thêm ngân sách dù chỉ một chút!",
"Vâng‚ cố lên nhé.<br>Em cũng sẽ ủng hộ anh mà.",
"Vậy thì em xin phép đi trước đây～.",
"Ừ‚ cảm ơn nhé‚ Marina.",
"Không có gì‚ khi nào cần cứ gọi em nhé♪<br>…Hì hì♪",
"<size=48>――Ngày Diễn Ra Đấu Giá</size>",
"Alicia đã cố hết sức‚ nhưng cũng chẳng gom được bao nhiêu ngân sách.<br>Đành phải liệu cơm gắp mắm thôi nhỉ.",
"Hm? Người ở đằng kia là…",
"Ôi‚ ông chủ.<br>Anh cũng tham gia đấu giá sao?",
"Marina‚ chẳng lẽ em cũng đến đấu giá!?<br>Em bảo hôm nay có việc còn gì!",
"Vâng‚ em có việc mà.<br>Một việc gọi là tham gia đấu giá đấy♪",
"Nhắc đến đấu giá là nhắc đến cơ hội làm ăn lớn.<br>Em đâu thể bỏ qua được.",
"Cô nàng này…!<br>Ra vậy‚ tức là em không định giúp anh chứ gì.",
"Tất nhiên em cũng thấy áy náy lắm‚<br>nhưng dù ông chủ có thắng đấu giá thì món đó cũng đâu thành hàng của em được.",
"Với tư cách thương nhân thì đó là lựa chọn đương nhiên nhỉ.<br>Hiểu rồi‚ anh không trách em đâu.",
"Quả không hổ danh‚ ông chủ hào phóng thật đấy.<br>Xem ai trong chúng ta giành được món mình muốn nhé♪",
"…Sao trông em có vẻ háo hức thế nhỉ.<br>Việc tranh hàng với anh vui đến vậy à?",
"Đã cùng tham gia một buổi đấu giá‚<br>thì dù là ông chủ cũng là đối thủ của em mà.",
"Được cạnh tranh với ông chủ với tư cách một thương nhân như thế này‚<br>Marina em không sao kìm được sự phấn khích♪",
"Anh đâu phải thương nhân.<br>Nhưng dù vậy‚ anh cũng không định thua đâu.",
"Chính vì ông chủ như vậy nên em mới thấy thú vị đấy.<br>Nào‚ chúng ta vào hội trường thôi～.",
"Sắp khai mạc rồi!<br>Những ai tham gia vui lòng nhận bảng số tại đây!",
"――Mọi người đã xem catalogue chưa?<br>Vì là nơi tiền tuyến nên có cả những món nguy hiểm được đem ra đấu giá đấy.",
"Họ còn bán cả sách cổ không ghi tiêu đề và những món kỳ lạ nữa nhỉ～?<br>Tôi lần đầu dự đấu giá nên háo hức quá～♪",
"Mục tiêu của tôi là 『Chiến Phủ Bộc Viêm』.<br>Chỗ dùng thì có hạn‚ nhưng nó sở hữu sức mạnh không món nào khác có được.",
"Cái gọi là 『Quả Cầu Cổ Đại』 này thật sự là món nổi bật sao?<br>Bên trong phong ấn một quái vật mạnh mẽ gì đó‚ nghe chỉ thấy nguy hiểm thôi mà?",
"Có thể dùng làm quân bài phô trương để uy hiếp‚ hoặc thả vào thế lực đối địch cũng được.<br>Dù không thể khống chế‚ sức mạnh lớn vẫn sinh ra rất nhiều lợi ích.",
"…Không khí náo nhiệt thật nhỉ.<br>Em mê cái bầu không khí ngay trước giờ khai mạc này lắm♪",
"Có vẻ ai cũng đã có món mình nhắm tới rồi…<br>Tất cả mọi người ở đây đều là đối thủ đấy‚ ông chủ～.",
"Ngân sách đã chẳng có bao nhiêu‚ rắc rối thật…<br>Nhân tiện‚ Marina nhắm món gì vậy?",
"Bất cứ thứ gì có vẻ bán được giá.<br>Tất cả đều là hàng hóa của em mà♪",
"À‚ tất nhiên em đâu có định mua sạch tất cả đâu nhé?",
"Marina đúng là thương nhân từ trong máu nhỉ…",
"Hì hì‚ đó là lời khen tuyệt nhất đấy♪<br>Ông chủ có món nào muốn lấy không?",
"Có vài món dụng cụ Alicia đã nhờ anh mua.<br>Với lại còn có một thứ anh thật sự muốn cho riêng mình…",
"Kính thưa quý vị đã có mặt!<br>Phiên đấu giá sắp bắt đầu!",
"Ôi‚ sắp bắt đầu rồi nhỉ.<br>Em thật sự mong chờ quá.",
"Vậy món đầu tiên đáng ghi nhớ là đây!　<br>Một tuyệt phẩm chúng tôi mang đến từ Eldrana‚ 『Ma Đạo Bộc Thạch』!",
"『Ma Đạo Bộc Thạch』…<br>Một đạo cụ đơn giản nhưng cực kỳ mạnh mẽ‚ có thể gây ra vụ nổ lớn khi sử dụng.",
"Ở căn cứ này chắc chắn nhu cầu sẽ rất cao.",
"Chậc‚ thứ đó mà cũng đem bán dễ dàng thế à.<br>Nếu kẻ kỳ quái nào thắng rồi làm nó nổ trong căn cứ thì tính sao đây?",
"Ôi chao. Vậy thì anh phải có trách nhiệm thắng đấu giá thôi nhỉ♪",
"Đúng là vậy.<br>Hơn nữa nó cũng có thể dùng trong thám hiểm Đại Hố mà.",
"Món này sẽ khởi điểm từ 10 nghìn!<br>Nào‚ có vị nào ra giá không!",
"Anh đấu giá!",
"<user> giơ bảng số trong tay lên.<br>Ánh mắt của người chủ trì hướng về phía này.",
"Vậy thì em cũng tham gia♪",
"Ngay bên cạnh‚ Marina cũng đã giơ bảng số lên.",
"Marina‚ em đúng là…!",
"Hì hì‚ vừa bắt đầu đã thành trận đấu rồi nhỉ‚ ông chủ♪",
"Khụ… đúng ý anh!",
"Quý cô bên kia ra 30 nghìn!<br>30 nghìn‚ còn ai nữa không!",
"Vẫn chưa đâu!<br>Anh không định rút lui ở chỗ này!",
"Đàn ông lắm đấy‚ ông chủ.<br>Vậy thì em cũng vậy♪",
"Quý ông bên kia‚ rồi lại đến quý cô thêm lần nữa‚ 50 nghìn!",
"Khụ… được lắm‚ Marina!",
"60 nghìn!",
"Bên này 70 nghìn!",
"Từ đây mới là lúc thật sự bắt đầu đấy.<br>Cùng tận hưởng nhé‚ ông chủ♪",
]

TEXT_TYPES={'title':1,'message':2,'messageTextUnder':2,'messageTextCenter':2}
TAG_RE=re.compile(r'<[^>]+>')
PLACEHOLDER_RE=re.compile(r'(%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]|%%|<user>)')

def sha(b): return hashlib.sha256(b).hexdigest()
def bom(b): return b.startswith(b'\xef\xbb\xbf')
def newline(b): return 'CRLF' if b'\r\n' in b else 'LF'
def split_lines_keep(s): return s.splitlines()
def text_field(parts, typ): return parts[TEXT_TYPES[typ]]
def tech_signature(parts, typ):
    ti=TEXT_TYPES[typ]
    return parts[:ti]+parts[ti+1:]

def load_pairs(path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=list)

src_b=EN_ASSET.read_bytes()
src_text=src_b.decode('utf-8-sig')
src_lines=src_text.splitlines()
line_sep='\r\n' if newline(src_b)=='CRLF' else '\n'

candidates=[]
for i,line in enumerate(src_lines,1):
    typ=line.split(',',1)[0] if ',' in line else ''
    if typ in TEXT_TYPES:
        parts=line.split(',')
        candidates.append({'ordinal':len(candidates)+1,'line':i,'type':typ,'speaker':parts[1] if len(parts)>1 else '', 'source_text':parts[TEXT_TYPES[typ]], 'delimiter_count':line.count(','), 'field_count':len(parts)})

blockers=[]
items=[]
notes=[]
if len(TRANSLATIONS)!=len(candidates):
    blockers.append({'code':'TRANSLATION_COUNT_MISMATCH','expected':len(candidates),'actual':len(TRANSLATIONS)})
for n,t in enumerate(TRANSLATIONS,1):
    if ',' in t:
        blockers.append({'code':'ASCII_COMMA_IN_TRANSLATION','ordinal':n,'text':t})

out_lines=list(src_lines)
entries=[]
if not blockers:
    for cand,vi in zip(candidates,TRANSLATIONS):
        parts=out_lines[cand['line']-1].split(',')
        parts[TEXT_TYPES[cand['type']]]=vi
        out_lines[cand['line']-1]=','.join(parts)
        status='TRANSLATED'
        # log intentional proper-name/numeric-ish unchanged only; none expected except impossible
        entries.append({**cand,'vi_text':vi,'match_status':'CONTEXT_ORDER_MATCH','translation_status':status})

out_text=line_sep.join(out_lines)
# Preserve final newline if source had one
if src_text.endswith('\n') or src_text.endswith('\r\n'):
    out_text += line_sep
out_b=(b'\xef\xbb\xbf' if bom(src_b) else b'') + out_text.encode('utf-8')
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
if not blockers:
    VI_ASSET.write_bytes(out_b)

# QA after write
qa={
 'scene':SCENE,
 'status':'PASS',
 'generated_at':datetime.now(timezone.utc).isoformat(),
 'blockers':[],
 'items':items,
 'notes':notes,
 'intentional_kept_text_records':[],
 'counts':{},
 'independent_verify':{}
}

def count_types(lines):
    d={k:0 for k in TEXT_TYPES}
    for l in lines:
        typ=l.split(',',1)[0] if ',' in l else ''
        if typ in d: d[typ]+=1
    d['total']=sum(d.values())
    return d

src_props={'path':str(EN_ASSET),'bytes':len(src_b),'sha256':sha(src_b),'bom':bom(src_b),'newline':newline(src_b),'line_count':len(src_lines),'text_record_counts':count_types(src_lines)}
vi_b=VI_ASSET.read_bytes() if VI_ASSET.exists() else b''
vi_text=vi_b.decode('utf-8-sig') if vi_b else ''
vi_lines=vi_text.splitlines() if vi_b else []
vi_props={'path':str(VI_ASSET),'bytes':len(vi_b),'sha256':sha(vi_b) if vi_b else None,'bom':bom(vi_b) if vi_b else None,'newline':newline(vi_b) if vi_b else None,'line_count':len(vi_lines),'text_record_counts':count_types(vi_lines) if vi_lines else {}}

if blockers:
    qa['blockers'].extend(blockers)
else:
    if len(src_lines)!=len(vi_lines): qa['blockers'].append({'code':'LINE_COUNT_MISMATCH','src':len(src_lines),'vi':len(vi_lines)})
    delimiter_mismatches=[]; tech_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; ascii_comma_issues=[]; unchanged=[]
    changed_records=0
    for cand in candidates:
        i=cand['line']-1
        sp=src_lines[i].split(','); vp=vi_lines[i].split(',')
        typ=cand['type']; ti=TEXT_TYPES[typ]
        if src_lines[i].count(',')!=vi_lines[i].count(','):
            delimiter_mismatches.append(cand['line'])
        if len(sp)!=len(vp) or tech_signature(sp,typ)!=tech_signature(vp,typ):
            tech_mismatches.append(cand['line'])
        if TAG_RE.findall(sp[ti])!=TAG_RE.findall(vp[ti]):
            tag_mismatches.append({'line':cand['line'],'src':TAG_RE.findall(sp[ti]),'vi':TAG_RE.findall(vp[ti])})
        if PLACEHOLDER_RE.findall(sp[ti])!=PLACEHOLDER_RE.findall(vp[ti]):
            placeholder_mismatches.append({'line':cand['line'],'src':PLACEHOLDER_RE.findall(sp[ti]),'vi':PLACEHOLDER_RE.findall(vp[ti])})
        if ',' in vp[ti]: ascii_comma_issues.append(cand['line'])
        if sp[ti] != vp[ti]: changed_records+=1
        else: unchanged.append({'line':cand['line'],'text':vp[ti]})
    if delimiter_mismatches: qa['blockers'].append({'code':'DELIMITER_MISMATCH','lines':delimiter_mismatches})
    if tech_mismatches: qa['blockers'].append({'code':'TECH_FIELD_MISMATCH','lines':tech_mismatches})
    if tag_mismatches: qa['blockers'].append({'code':'TAG_MISMATCH','items':tag_mismatches})
    if placeholder_mismatches: qa['blockers'].append({'code':'PLACEHOLDER_MISMATCH','items':placeholder_mismatches})
    if ascii_comma_issues: qa['blockers'].append({'code':'ASCII_COMMA_IN_VI_TEXT_FIELD','lines':ascii_comma_issues})
    if unchanged: qa['blockers'].append({'code':'UNINTENTIONAL_UNCHANGED_TEXT_RECORDS','items':unchanged})
    # Leftover targeted JP/EN/honorific scan in VI fields
    jp_left=[]; honorific=[]; en_markers=[]
    for cand in candidates:
        p=vi_lines[cand['line']-1].split(','); txt=p[TEXT_TYPES[cand['type']]]
        if re.search(r'[ぁ-んァ-ン一-龯]', txt): jp_left.append({'line':cand['line'],'text':txt})
        if re.search(r'-(kun|sama|san|chan)\b', txt, re.I): honorific.append({'line':cand['line'],'text':txt})
        if re.search(r'\b(Ugh|Ah|Oh|Geez|What|Yes|No|Lord Commander|Commander)\b', txt): en_markers.append({'line':cand['line'],'text':txt})
    if jp_left: qa['blockers'].append({'code':'LEFTOVER_JAPANESE_IN_VI','items':jp_left})
    if honorific: qa['blockers'].append({'code':'LEFTOVER_HONORIFIC','items':honorific})
    if en_markers: qa['blockers'].append({'code':'LEFTOVER_ENGLISH_MARKER','items':en_markers})
    qa['counts']={'candidate_text_records':len(candidates),'translated_records':changed_records,'by_type':count_types(src_lines),'delimiter_mismatch_count':len(delimiter_mismatches),'unchanged_text_records':len(unchanged)}
    qa['independent_verify']={'line_count_match':len(src_lines)==len(vi_lines),'bom_match':bom(src_b)==bom(vi_b),'newline_match':newline(src_b)==newline(vi_b),'delimiter_mismatches':delimiter_mismatches,'technical_field_mismatches':tech_mismatches,'tag_mismatches':tag_mismatches,'placeholder_mismatches':placeholder_mismatches,'ascii_comma_issues':ascii_comma_issues,'unchanged_text_records':unchanged,'leftover_japanese':jp_left,'leftover_honorific':honorific,'leftover_english_markers':en_markers}

if qa['blockers']:
    qa['status']='FAIL'

jp_pairs=load_pairs(JP_PATH); en_pairs=load_pairs(EN_JSON_PATH)
manifest={
 'scene':SCENE,
 'status':'PASS' if qa['status']=='PASS' else 'FAIL',
 'created_at':datetime.now(timezone.utc).isoformat(),
 'sources':{'jp_json':{'path':str(JP_PATH),'sha256':sha(JP_PATH.read_bytes()),'pair_count':len(jp_pairs)},'en_json':{'path':str(EN_JSON_PATH),'sha256':sha(EN_JSON_PATH.read_bytes()),'pair_count':len(en_pairs)},'en_asset':src_props},
 'output':vi_props,
 'format':{'delimiter':',','text_field_indices':TEXT_TYPES,'preserved_bom':src_props['bom'],'preserved_newline':src_props['newline']},
 'translation_policy':{'jp_primary':True,'en_alignment_only':True,'commander':'Chỉ Huy','ascii_comma_in_vi_text':'U+201A ‚','title_case':True,'adult_content':'confirmed_18_plus_translate_normally'},
 'entries':entries,
 'qa_status':qa['status'],
 'qa_log':str(WORK/'qa_log.json'),
 'diff':str(WORK/'focused_diff.md')
}

(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

# Focused diff only candidate lines
src_focus=[]; vi_focus=[]
for cand in candidates:
    src_focus.append(f"L{cand['line']:04d}: {src_lines[cand['line']-1]}\n")
    if vi_lines:
        vi_focus.append(f"L{cand['line']:04d}: {vi_lines[cand['line']-1]}\n")
    else:
        vi_focus.append(f"L{cand['line']:04d}: <NO OUTPUT>\n")
diff_lines = [line.rstrip('\n') for line in difflib.unified_diff(src_focus, vi_focus, fromfile='EN/JP asset text records', tofile='VI asset text records', lineterm='')]
diff='\n'.join(diff_lines)
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10030100001\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')
print(json.dumps({'qa_status':qa['status'],'blockers':qa['blockers'],'output':str(VI_ASSET),'manifest':str(WORK/'manifest.json'),'qa_log':str(WORK/'qa_log.json'),'diff':str(WORK/'focused_diff.md'),'counts':qa.get('counts')}, ensure_ascii=False, indent=2))
