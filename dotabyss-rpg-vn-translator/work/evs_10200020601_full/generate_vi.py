# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE = 'evs_10200020601'
ROOT = Path('E:/AgentTranslation')
SRC_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
OUT_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/evs_10200020601_full'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels/evs_10200020601/ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels/evs_10200020601/en.json'
TEXT_PREFIXES = ('title,','message,','messageTextUnder,','messageTextCenter,')

VI = [
'Tiêu Đề',
'Qua chén rượu trên bàn tiệc‚ những con người ghé thăm Đảo Quỷ đã hoàn toàn hòa hợp với tộc quỷ‚<br>bữa tiệc cũng náo nhiệt hẳn lên. Thế nhưng――<br> ',
'……!? V-vừa rồi là gì vậy ạ……?<br>Em cảm thấy có gì đó kỳ lạ…… như một làn sóng ma lực vừa lướt qua……?<br> ',
'……Shiraes. Cô cũng nhận ra rồi nhỉ?<br> ',
'Ừ. Vừa rồi là sức mạnh của viên pha lê. Xem ra viên pha lê đã được giải phóng<br>khỏi chiếc hộp mà cậu Adelheid làm cho chúng ta rồi.<br> ',
'Không thể nào!? Đáng lẽ em đã để nó trong phòng em rồi mà……<br>Không có ai trong tộc quỷ tự ý vào đó đâu……<br> ',
'Vậy thì…… có lẽ kẻ nào đó đã đột nhập vào Đảo Quỷ.<br>Nhưng…… nếu viên pha lê phát huy sức mạnh trong tình hình hiện tại thì rất tệ đấy.<br> ',
'C-cái gì vừa rồi vậy……!? Động đất à……!?<br> ',
'K-không‚ cảm giác còn lạ hơn thế nhiều……!<br> ',
'Có vẻ dân làng cũng cảm nhận được rồi.<br>Một dao động mạnh đến thế thì cũng không lạ.<br> ',
'M-mọi người‚ xin hãy bình tĩnh nào~.<br>Chúng tôi sẽ xác nhận tình hình ngay bây giờ――<br> ',
'Ngay lúc Kureha định trấn an dân làng‚<br>một gã đàn ông khả nghi bất ngờ phá cửa xông vào!<br> ',
'Chậc‚ bọn dai như đỉa……! Đây là…… phòng tiệc à?<br> ',
'Ngươi là…… tên trộm lúc đó!<br>Ra vậy‚ kẻ cướp viên pha lê chính là ngươi!<br> ',
'Ha ha‚ tưởng ai‚ hóa ra là Chỉ Huy ngu ngốc à!<br>Để đồ bị trộm thì tự trách mình đi! Viên pha lê này là của ta――!<br> ',
'Đứng lại đấyyyyy!! Mi đang làm cái quái gì vậyyyyy!!<br> ',
'Ưự……!? K-không thoát ra được……! Chết tiệt‚ sức mạnh quái vật gì thế này……!<br> ',
'C-cái gì vậy!? Rốt cuộc chuyện gì đang xảy ra……!?<br> ',
'Khi sự hỗn loạn lan rộng giữa dân làng‚<br>viên pha lê tuột khỏi tay tên trộm và lăn xuống đất.<br> ',
'Viên pha lê đang phát sáng…… nó đã kích hoạt hoàn toàn rồi.<br>Do ma lực tên trộm rót vào sao? Không…… phản ứng này mạnh quá mức.<br> ',
'Hừm…… đúng là phản ứng này kỳ lạ thật.<br>Nó vẫn đang liên tục phát ra sức mạnh thu hút quái vật.<br> ',
'Này cậu trộm kia. Ta muốn hỏi cậu một điều‚<br>chiếc hộp từng chứa viên pha lê này đâu rồi?<br> ',
'Này! Mau ngoan ngoãn trả lời câu hỏi của chị đại đi!<br> ',
'Hề‚ hê hê……! Thứ đó hả‚ ta đập nát rồi! Vướng víu quá mà!<br> ',
'Quả nhiên là vậy……. Chỉ Huy‚ chúng ta gặp chút rắc rối rồi đấy.<br> ',
'Viên pha lê vốn tự phát ra dao động thu hút quái vật<br>dù không ai rót ma lực vào‚ nhưng khi đặt trong hộp thì dao động ấy bị nhốt lại.<br> ',
'Cậu hiểu điều đó nghĩa là gì chứ?<br> ',
'……Ý cô là sức mạnh tích tụ khi bị nhốt trong chiếc hộp kín<br>đã được giải phóng trong một lần‚ rồi tiếp tục phát ra dao động―― phải không?<br> ',
'Chính xác. Nói cách khác―― nếu cứ thế này‚ quái vật sẽ không ngừng tràn đến Đảo Quỷ.<br>Hơn nữa còn là một lượng lớn chưa từng thấy từ trước đến nay.<br> ',
'K-không thể nào……!<br> ',
'……Này‚ tên trộm kia. Ngươi gây ra chuyện lớn thật đấy nhỉ?<br> ',
'Hê hê‚ liên quan gì đến ta.<br>Không phải có chuyện khác đáng lo hơn sao?<br> ',
'……Gì cơ?<br> ',
'Này‚ lũ chúng mày! Sắp có quái vật tràn vào đây đấy!<br>Lũ tộc quỷ đã gọi quái vật tới để giết sạch chúng mày!<br> ',
'Cái……!? Sao hắn dám nói bậy như vậy……!<br> ',
'Q-quái vật……? K-không‚ nhưng họ đã đối xử rất tử tế với chúng ta mà……<br> ',
'Tử tế để lừa chúng mày chứ còn gì nữa!<br>Chúng mời con người đến Đảo Quỷ là để tóm gọn cả mẻ đấy!<br> ',
'Ngươi đừng có ăn nói nhảm nhí nữa! Câm miệng một chút đi……!!<br> ',
'Guah……!?<br> ',
'Cô ta đánh hắn bất tỉnh rồi……?<br>Vì đó là chuyện không thể để lộ nên cô ta bịt miệng hắn sao……?<br> ',
'C-cái gì cơ!? Ta không hề có ý đó!<br>Chỉ là tên này nói mấy lời quá quắt nên ta mới……!<br> ',
'(Nguy rồi. Dân làng không biết tên trộm này là nguyên nhân.<br>Hơn nữa trong cảnh hỗn loạn này‚ họ cũng khó mà phán đoán bình tĩnh……!)<br> ',
'C-chúng ta sẽ bị giết……! Chúng ta bị lừa vào bẫy rồi!<br>Quả nhiên tộc quỷ là một bộ tộc đáng sợ……!<br> ',
'K-không phải vậy! Xin hãy nghe tôi nói!<br>Chúng tôi thật lòng muốn thân thiết với mọi người……!<br> ',
'L-làm sao tin chuyện đó được!<br> ',
'……!<br> ',
'Tình huống khẩn cấp! Một đàn quái vật đang áp sát!<br>Ai chiến đấu được thì vào vị trí!<br> ',
'Quái vật!? Vậy lời người đó nói là thật!<br>Tộc quỷ đúng là muốn giết chúng ta……!<br> ',
'Hả!? Sao các người lại nghĩ ra chuyện đó được!?<br>Bọn ta đang định bảo vệ các người mà……!<br> ',
'Đ-đừng hòng lừa bọn ta! V-vừa rồi ta nghe thấy tiếng quái vật!<br>Bị bao vây rồi……!? K-không chạy được nữa……!<br> ',
'Không ổn…… mọi người hỗn loạn thế này thì không thể sơ tán họ được……!<br>Rốt cuộc phải làm sao đây……?<br> ',
'<size=48>Khặc khặc khặc…… lũ con người ngu xuẩn‚ mắc bẫy ngon lành rồi nhỉ!!</>',
'Hả……!? P-phu quân!? Rốt cuộc anh đang làm gì vậy……!?<br> ',
'Đúng vậy! Bọn ta đã lừa các ngươi ngay từ đầu!<br>Kẻ nào chậm chân sẽ bị ăn trước! Uoooooooooooo!<br> ',
'H-hiiiiiiiii……!?<br> ',
'Bị %user% xua đuổi‚ dân làng bị dồn lại một chỗ.<br> ',
'Uoooooooooooo……!! ……Ừm‚ cỡ này chắc được rồi.<br> ',
'Làm tốt lắm. Ngoan đấy‚ Chỉ Huy.<br>Lát nữa ta sẽ xoa đầu thưởng cho cậu.<br> ',
'……! Ra là vậy! Để tập hợp dân làng vào một chỗ và bảo vệ họ‚<br>phu quân cố ý nói những lời hù dọa đó! Tuyệt quá! Đúng là phu quân!<br> ',
'Lời nói dối cũng có lúc cần thiết. Nếu họ chết thì sau này cũng không còn cơ hội giải thích hiểu lầm nữa.<br>Vì vậy…… bây giờ chúng ta phải dốc toàn lực bảo vệ dân làng!<br> ',
'Vâng! Mọi người tộc quỷ nghe thấy rồi chứ!?<br>Hãy làm theo chỉ thị của phu quân và bảo vệ mọi người bên phía con người!<br> ',
'Được! Ngài Chỉ Huy!<br>Cho bọn tôi thấy ngài xứng làm chú rể của tiểu thư Kureha đi!<br> ',
'Ai là chú rể chứ! Không‚ giờ không phải lúc nói chuyện đó!<br> ',
'Tộc quỷ hãy dựng thành bức tường để bảo vệ con người!<br> ',
'Rõ‚ cứ để bọn tôi! Làm tới luôn nàoーーー!<br> ',
'Kureha‚ dẫn vài người thiện chiến ra đánh du kích!<br>Tùy em phán đoán!<br> ',
'Đã rõ! Kureha này nhất định sẽ hoàn thành nhiệm vụ!<br> ',
'Shiraes! Tôi sẽ chỉ huy số tộc quỷ còn lại và dồn quái vật về một chỗ!<br>Khi tôi ra hiệu‚ dùng ma pháp mạnh nhất quét sạch chúng! Làm được chứ!?<br> ',
'Được thôi. Hiếm khi hôm nay có nhiều vị khách đến vậy.<br>Ta sẽ cho họ chiêm ngưỡng màn pháo hoa đặc biệt.<br> ',
'Tôi trông cậy vào cô đấy! Nào‚ mọi người‚ đây là giờ phút quyết định!<br>Hãy cho tôi thấy sức mạnh của tộc quỷ――!<br> ',
'Uoooooooooooooooooooooooooooooooo――!!!<br> ',
]


def raw_bytes(p): return p.read_bytes()
def sha(b): return hashlib.sha256(b).hexdigest()
def newline_style(b):
    if b'\r\n' in b: return 'CRLF'
    if b'\n' in b: return 'LF'
    return 'NONE'
def has_bom(b): return b.startswith(b'\xef\xbb\xbf')
def split_lines_keep(s): return s.splitlines(keepends=True)
def line_text_no_nl(line): return line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith('\n') else line
def eol_of(line): return '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
def tags(s): return re.findall(r'<[^>]+>', s)
def placeholders(s): return re.findall(r'(%user%|<user>|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%)', s)

def text_field(line):
    if line.startswith('title,'):
        return line.split(',',1)[1]
    if line.startswith(('message,','messageTextUnder,','messageTextCenter,')):
        parts=line.split(',',5)
        return parts[2] if len(parts)>2 else ''
    return None

def set_text_field(line, val):
    if line.startswith('title,'):
        return 'title,' + val
    parts=line.split(',',5)
    if len(parts) < 3: raise ValueError('bad message line')
    parts[2]=val
    return ','.join(parts)

def tech_signature(line):
    if line.startswith('title,'):
        return ['title']
    parts=line.split(',',5)
    return [parts[0],parts[1]] + (parts[3:] if len(parts)>3 else [])

src_b=raw_bytes(SRC_ASSET)
enc='utf-8-sig' if has_bom(src_b) else 'utf-8'
src=src_b.decode(enc)
lines=split_lines_keep(src)
entries=[]
for idx,line in enumerate(lines,1):
    bare=line_text_no_nl(line)
    if bare.startswith(TEXT_PREFIXES):
        entries.append((idx,bare))

blockers=[]; notes=[]; kept=[]
if len(entries)!=len(VI):
    blockers.append({'type':'COUNT_MISMATCH','detail':f'asset candidates {len(entries)} vs VI {len(VI)}'})
for i,v in enumerate(VI):
    if ',' in v:
        blockers.append({'type':'ASCII_COMMA_IN_VI_TRANSLATION','entry':i+1,'text':v})

out_lines=lines[:]
if not blockers:
    for (n,bare),vi in zip(entries,VI):
        newbare=set_text_field(bare,vi)
        out_lines[n-1]=newbare+eol_of(lines[n-1])

OUT_ASSET.parent.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
out=''.join(out_lines)
OUT_ASSET.write_text(out, encoding=enc, newline='')
out_b=OUT_ASSET.read_bytes()

# QA
out_lines2=split_lines_keep(out_b.decode(enc))
if len(lines)!=len(out_lines2): blockers.append({'type':'LINE_COUNT_MISMATCH','src':len(lines),'out':len(out_lines2)})
translated=0
manifest_entries=[]
for pos,(n,bare) in enumerate(entries,1):
    obare=line_text_no_nl(out_lines2[n-1])
    src_tf=text_field(bare); out_tf=text_field(obare)
    errs=[]
    if bare.count(',') != obare.count(','): errs.append('DELIMITER_COUNT')
    if tech_signature(bare)!=tech_signature(obare): errs.append('TECH_FIELDS')
    if tags(src_tf)!=tags(out_tf): errs.append('TAG_MISMATCH')
    # compare placeholders except <user> speaker is outside, %user% in text must survive
    if placeholders(src_tf)!=placeholders(out_tf): errs.append('PLACEHOLDER_MISMATCH')
    if out_tf==src_tf:
        kept.append({'entry':pos,'line':n,'text':out_tf,'reason':'unintentional_unchanged_candidate'})
        errs.append('KEPT_EN')
    if ',' in out_tf: errs.append('ASCII_COMMA_IN_TEXT_FIELD')
    if errs:
        blockers.append({'type':'ENTRY_QA','entry':pos,'line':n,'errors':errs})
    else:
        translated += 1
    manifest_entries.append({'entry':pos,'line':n,'record':bare.split(',',1)[0],'speaker':bare.split(',',2)[1] if bare.startswith('message,') else None,'status':'TRANSLATED' if not errs else 'REVIEW','errors':errs,'source_text':src_tf,'vi_text':out_tf})

# JSON ordered pair counts
try:
    ja_pairs=json.loads(JA_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)
    en_pairs=json.loads(EN_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)
    notes.append({'type':'NOVEL_PAIR_COUNT','ja_pairs':len(ja_pairs),'en_pairs':len(en_pairs),'asset_candidates':len(entries)})
except Exception as e:
    notes.append({'type':'NOVEL_JSON_READ_ERROR','error':str(e)})

# focused diff only candidates
src_focus=[f'L{n}: {bare}\n' for n,bare in entries]
out_focus=[f'L{n}: {line_text_no_nl(out_lines2[n-1])}\n' for n,_ in entries]
diff=''.join(difflib.unified_diff(src_focus,out_focus,fromfile=str(SRC_ASSET),tofile=str(OUT_ASSET),lineterm=''))
(WORK/'focused_diff.md').write_text('```diff\n'+diff+'\n```\n',encoding='utf-8')
qa_status='PASS' if not blockers else 'FAIL'
manifest={
 'scene':SCENE,
 'generated_at':datetime.now(timezone.utc).isoformat(),
 'source_asset':str(SRC_ASSET), 'output_asset':str(OUT_ASSET),
 'ja_json':str(JA_JSON), 'en_json':str(EN_JSON),
 'source_sha256':sha(src_b), 'output_sha256':sha(out_b),
 'source_bytes':len(src_b), 'output_bytes':len(out_b),
 'source_bom':has_bom(src_b), 'output_bom':has_bom(out_b),
 'source_newline':newline_style(src_b), 'output_newline':newline_style(out_b),
 'source_line_count':len(lines), 'output_line_count':len(out_lines2),
 'candidate_record_count':len(entries), 'translated_record_count':translated,
 'text_command_counts':{k:sum(1 for _,b in entries if b.startswith(k+',')) for k in ['title','message','messageTextUnder','messageTextCenter']},
 'entries':manifest_entries,
 'qa_status':qa_status,
}
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
qa={'qa_status':qa_status,'blockers':blockers,'kept_english':kept,'notes':notes,'checks':{
 'line_count_match':len(lines)==len(out_lines2), 'bom_preserved':has_bom(src_b)==has_bom(out_b), 'newline_preserved':newline_style(src_b)==newline_style(out_b), 'candidate_count':len(entries), 'translated_count':translated,
}}
(WORK/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'qa_status':qa_status,'blockers':len(blockers),'translated':translated,'candidates':len(entries),'manifest':str(WORK/'manifest.json'),'qa_log':str(WORK/'qa_log.json'),'diff':str(WORK/'focused_diff.md'),'output':str(OUT_ASSET)},ensure_ascii=False,indent=2))
if blockers:
    raise SystemExit(1)
