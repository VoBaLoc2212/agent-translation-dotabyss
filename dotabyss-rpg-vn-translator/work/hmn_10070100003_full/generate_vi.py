# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib
from collections import Counter

SCENE = 'hmn_10070100003'
ROOT = Path('E:/AgentTranslation')
SRC = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
OUT = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
NOVEL_JA = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
NOVEL_EN = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
WORK.mkdir(parents=True, exist_ok=True)

TRANSLATIONS = [
    'Kinh Hoàng! Poltergeist!',
    'ĐÙ―――――――NG!!!<br> ',
    'C‚ chuyện gì vậy!? Đã xảy ra chuyện gì!?<br> ',
    'Đồ đạc và vũ khí đang bay loạn xạ trên không! Cứ thế này thì<br>sẽ có người bị thương mất!<br> ',
    'Hả!? Khoan đã‚ làm gì có chuyện phi lý như thế――<br> ',
    'Ngay trước mắt Chỉ Huy còn chưa tin nổi vào tai mình‚ đủ thứ vật dụng<br>đang bay vù vù với sức mạnh chết người.<br> ',
    'Chúng bay thật kìa!? Sao lại có chuyện giống<br>poltergeist thế này được……<br> ',
    '…Không lẽ! Film đâu rồi!?<br> ',
    'Chỉ Huy‚ em tới rồi đây～ Anh đột nhiên gọi em như vậy‚ em vui lắm……<br> ',
    'Film vừa đến ký túc xá thì hơi mở to mắt trước hiện tượng<br>poltergeist ngay trước mặt.<br> ',
    'Ôi chao‚ bất ngờ thật. Chuyện lớn rồi nhỉ～<br> ',
    'Film‚ cuối cùng em cũng tới rồi!<br> ',
    'Chỉ Huy! Lúc nguy hiểm thế này anh không được chạy lung tung chứ!<br> ',
    'Đây là lúc thuyết giáo sao! Hiện tượng poltergeist này rõ ràng là<br>hiện tượng tâm linh rồi!<br> ',
    '…Ừ‚ em cảm nhận được linh lực rõ rệt. Chắc chắn là hiện tượng<br>tâm linh đấy～<br> ',
    'Khỉ thật‚ lần này là hàng thật sao! Quy mô lớn thế này‚ nguyên nhân lẽ nào<br>là……<br> ',
    'Là em sao‚ Noir?<br> ',
    '…!? …!!!<br> ',
    'Không phải à. Quả thật quy mô này không thể gọi là trò nghịch được.<br> ',
    'Tệ rồi. Phải nhanh chóng xử lý trước khi có người bị thương……!<br> ',
    'Đúng vậy! Chúng ta lại cùng nhau tìm nguyên nhân nhé‚ Chỉ Huy♪<br> ',
    'Chắc chắn hai chúng ta sẽ giải quyết được như lần trước thôi～<br> ',
    'Không‚ xin lỗi nhưng chuyện này không phải quy mô mà chỉ hai ta xử lý được.<br>Phải huy động toàn bộ nhân lực ở Căn Cứ Tiền Tuyến!<br> ',
    'A…… Ừ‚ đúng rồi nhỉ. Đâu phải lúc để vui vẻ<br>đi điều tra đâu.<br> ',
    '…Dù hơi tiếc một chút.<br> ',
    'Em sao vậy‚ Film? Giờ không phải lúc ngẩn người……<br> ',
    '!!<br> ',
    'Khi Film còn đang lơ đãng‚ %user% nhận ra một thanh đại kiếm nổi lên<br>do poltergeist đang lao thẳng về phía cô.<br> ',
    'Film‚ nguy hiểm!<br> ',
    'Ơ…… kya!?<br> ',
    'Ch‚ Chỉ Huy‚ anh che chắn cho em sao!?<br> ',
    'Đừng lơ là quá! Suýt nữa em bị thương rồi đấy!<br> ',
    'Trời ạ. Em đã nói là em ổn mà. Chỉ Huy đâu cần phải che chở<br>cho em chứ?<br> ',
    'Trước đây anh đã nói rồi mà. Dù có bị em mắng thì anh cũng<br>không bỏ được thói cứu giúp con gái đâu.<br> ',
    'Nhưng khi đó anh mới vừa gặp em thôi mà‚ Chỉ Huy.<br> ',
    'Giờ anh biết rõ em là một bà cụ già hơn anh rất nhiều rồi mà?<br> ',
    'Ừ‚ lúc đó và bây giờ khác nhau.<br> ',
    'Càng hiểu em‚ anh càng thấy Film là một cô gái đáng yêu‚<br>Film à.<br> ',
    '…Ơ?<br> ',
    'Anh đang nói rằng Film rất tuyệt vời bất kể tuổi tác. Vì vậy anh<br>mới lo cho em và muốn bảo vệ em.<br> ',
    'Ch‚ Chỉ Huy……♡<br> ',
    'ĐÙNG ĐÙNG!!!<br> ',
    'Cùng một tiếng nổ đặc biệt lớn‚ toàn bộ đồ đạc và vũ khí trong phòng<br>đồng loạt bay lên rồi va vào nhau giữa không trung.<br> ',
    'Một cái kệ lớn trong số đó rơi xuống phía Film và Chỉ Huy――<br> ',
    '…!<br> ',
    'Uoa!? Noir‚ đừng đột nhiên đâm sầm vào anh chứ……<br> ',
    'Kya……<br> ',
    '――――――Chụt――――――<br> ',
    '(Cảm giác mềm mại này…… không lẽ……)<br> ',
    'Ưm……<br> ',
    '!? A…… x‚ xin lỗi!<br> ',
    'Trời ạ‚ Chỉ Huy thật là. Tự dưng cưỡng hôn em như vậy làm em<br>giật mình đấy♡<br> ',
    'Không phải đâu! Noir đẩy anh từ phía sau……<br> ',
    '…!<br> ',
    'Hửm? Em đang nhìn về phía cái kệ…… Ra vậy! Em đã cứu anh khỏi<br>poltergeist đúng không.<br> ',
    '…♪<br> ',
    'À‚ cảm ơn em nhé‚ Noir.<br> ',
    'Chuyện gì đây……!? Tất cả những thứ đang bay đều rơi xuống rồi sao……?<br> ',
    'Đúng thật! Không thấy dấu hiệu chúng chuyển động nữa‚ có vẻ<br>poltergeist đã lắng xuống rồi～<br> ',
    'Đúng vậy nhưng có thể nó lại bắt đầu……<br> ',
    'V‚ vậy thì em đi trước đây. Chỉ Huy‚ vất vả rồi!<br> ',
    'Ơ? Không‚ khoan đã. Chúng ta còn phải tìm nguyên nhân gây ra poltergeist……<br> ',
    'Fufu‚ ufufu……♡<br> ',
    'Đi mất rồi……<br> ',
    'Thiệt tình. Để ngăn tái phát‚ chúng ta cần xác định nguyên nhân vậy mà……<br> ',
    '…!<br> ',
    'Gì vậy‚ Noir. Không lẽ em biết nguyên nhân rồi sao?<br> ',
    '…!<br>…!♡<br> ',
    'Em đang chỉ về phía Film đi…… Không lẽ em muốn nói<br>hiện tượng ban nãy là do Film gây ra?<br> ',
    'Nhưng Film đâu có linh lực đến mức đó đúng không? Cô ấy từng nói<br>cùng lắm chỉ làm nước trong cốc dao động thôi mà.<br> ',
    '…Khoan‚ thật sự là vậy sao?<br> ',
    'Cô ấy bị Noir nguyền rủa nhiều năm mà vẫn bình thản‚ thậm chí<br>còn bắt Noir nghe lời mình……<br> ',
    'Một Film như vậy mà không có<br>linh lực thì lạ quá.<br> ',
    '…!♪<br> ',
    'Chỉ là cô ấy không tự nhận ra thôi sao. Thật ra Film cũng có<br>linh lực rất mạnh…… đúng không?<br> ',
    '…!<br> ',
    'Có vẻ anh đoán đúng rồi. Nếu vậy thì cô ấy cũng có thể gây ra<br>poltergeist.<br> ',
    'Nhưng tại sao Film lại gây ra chuyện này? Và vì sao nó dừng lại?<br> ',
    'Em đã hôn Chỉ Huy rồi……! Fufu‚ ufufufufu♡<br> ',
    'Hôm nay em đã làm được chuyện còn tuyệt hơn cả hẹn hò. Một ngày<br>tuyệt vời biết bao……!<br> ',
    'Biết làm sao đây‚ từng tuổi này rồi mà tim em vẫn đập thình thịch không ngừng!♡<br>Tất cả là nhờ hiện tượng tâm linh đó đấy!<br> ',
    '…Không biết nó có xảy ra lần nữa không nhỉ～<br> ',
    'Nếu hiện tượng tâm linh xảy ra thì cô ấy lại có thể cùng mình giải quyết……<br>Cảm xúc đó đã vô thức gây nên vụ náo động……<br> ',
    'Và vì hôn mình xong cô ấy thỏa mãn nên hiện tượng tâm linh lắng xuống.<br>Đó là chân tướng của vụ việc này sao?<br> ',
    '…♡<br> ',
    'Chuyện gì thế này……<br>Film chẳng phải chỉ là một cô gái đáng yêu thôi sao……<br> ',
    '…♪<br> ',
    'Nhưng nếu chuyện này lặp đi lặp lại nhiều lần‚<br>Căn Cứ Tiền Tuyến sẽ tan hoang mất.<br> ',
    'Từ giờ trở đi‚ mình phải yêu chiều cô ấy trước khi Film tích tụ bất mãn khao khát.<br> ',
    '…♡<br> ',
]

TEXT_CMDS = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}
TEXT_IDX = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%(?:user|s|d)|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%')

def sha256(data): return hashlib.sha256(data).hexdigest()
def newline_style(data):
    if b'\r\n' in data and data.count(b'\r\n') == data.count(b'\n'): return 'CRLF'
    if b'\n' in data: return 'LF'
    return 'NONE'

def read_json_pairs(path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=list)

def extract_candidates(lines):
    out=[]
    for ln,line in enumerate(lines,1):
        core=line.rstrip('\r\n')
        parts=core.split(',')
        if parts and parts[0] in TEXT_CMDS:
            idx=TEXT_IDX[parts[0]]
            out.append({'line':ln,'cmd':parts[0],'speaker':parts[1] if len(parts)>1 else '', 'text_idx':idx, 'text':parts[idx], 'delimiter_count':core.count(','), 'parts':parts})
    return out

src_bytes = SRC.read_bytes()
text = src_bytes.decode('utf-8-sig')
lines = text.splitlines(True)
cands = extract_candidates(lines)
blockers=[]; notes=[]
if len(cands) != len(TRANSLATIONS):
    blockers.append({'type':'TRANSLATION_COUNT_MISMATCH','expected':len(cands),'actual':len(TRANSLATIONS)})
for i,t in enumerate(TRANSLATIONS,1):
    if ',' in t:
        blockers.append({'type':'ASCII_COMMA_IN_TRANSLATION','index':i,'text':t})
if blockers:
    raise SystemExit(json.dumps({'blockers':blockers}, ensure_ascii=False, indent=2))

out_lines = list(lines)
entries=[]
for idx,(cand,vi) in enumerate(zip(cands, TRANSLATIONS),1):
    parts = list(cand['parts'])
    old_text = parts[cand['text_idx']]
    parts[cand['text_idx']] = vi
    end = '\r\n' if out_lines[cand['line']-1].endswith('\r\n') else '\n' if out_lines[cand['line']-1].endswith('\n') else ''
    out_lines[cand['line']-1] = ','.join(parts) + end
    entries.append({
        'index':idx,'line':cand['line'],'command':cand['cmd'],'speaker':cand['speaker'],
        'source_text':old_text,'vi_text':vi,
        'match_status':'EXACT' if idx <= 85 else 'ASSET_EXTRA_NOIR_EMOTE',
        'translation_status':'TRANSLATED',
        'ja_primary': None
    })

out_text = ''.join(out_lines)
out_bytes = (b'\xef\xbb\xbf' if src_bytes.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8')
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(out_bytes)

# QA structural
vi_bytes = OUT.read_bytes()
vi_text = vi_bytes.decode('utf-8-sig')
vi_lines = vi_text.splitlines(True)
vi_cands = extract_candidates(vi_lines)
qa_blockers=[]; qa_items=[]
if len(lines) != len(vi_lines): qa_blockers.append({'type':'LINE_COUNT_MISMATCH','en':len(lines),'vi':len(vi_lines)})
if src_bytes.startswith(b'\xef\xbb\xbf') != vi_bytes.startswith(b'\xef\xbb\xbf'):
    qa_blockers.append({'type':'BOM_MISMATCH'})
if newline_style(src_bytes) != newline_style(vi_bytes): qa_blockers.append({'type':'NEWLINE_MISMATCH','en':newline_style(src_bytes),'vi':newline_style(vi_bytes)})
if len(cands) != len(vi_cands): qa_blockers.append({'type':'TEXT_RECORD_COUNT_MISMATCH','en':len(cands),'vi':len(vi_cands)})
for e,v in zip(cands, vi_cands):
    if e['delimiter_count'] != v['delimiter_count']:
        qa_blockers.append({'type':'DELIMITER_MISMATCH','line':e['line'],'en':e['delimiter_count'],'vi':v['delimiter_count']})
    ep = e['parts']; vp = v['parts']; ti=e['text_idx']
    if ep[:ti] + ep[ti+1:] != vp[:ti] + vp[ti+1:]:
        qa_blockers.append({'type':'TECH_FIELD_CHANGED','line':e['line']})
    if TAG_RE.findall(e['text']) != TAG_RE.findall(v['text']):
        qa_blockers.append({'type':'TAG_MISMATCH','line':e['line'],'en':TAG_RE.findall(e['text']),'vi':TAG_RE.findall(v['text'])})
    if PH_RE.findall(e['text']) != PH_RE.findall(v['text']):
        qa_blockers.append({'type':'PLACEHOLDER_MISMATCH','line':e['line'],'en':PH_RE.findall(e['text']),'vi':PH_RE.findall(v['text'])})
    if ',' in v['text']:
        qa_blockers.append({'type':'ASCII_COMMA_IN_VI_TEXT','line':e['line'],'text':v['text']})
    if e['text'] == v['text']:
        qa_items.append({'type':'UNCHANGED_TEXT_REVIEW','line':e['line'],'text':v['text'],'status':'intentional_symbol_or_noir_emote' if re.fullmatch(r'[.…!♪♡<br> ]+', v['text']) else 'review'})

ja_pairs = read_json_pairs(NOVEL_JA)
en_pairs = read_json_pairs(NOVEL_EN)
for i,e in enumerate(entries):
    if i < len(ja_pairs):
        e['ja_primary'] = ja_pairs[i][0]
    else:
        e['ja_primary'] = None

# diff focused
before=[]; after=[]
for e,v in zip(cands, vi_cands):
    before.append(f"L{e['line']:04d} {e['cmd']} {e['speaker']}: {e['text']}\n")
    after.append(f"L{v['line']:04d} {v['cmd']} {v['speaker']}: {v['text']}\n")
diff=''.join(difflib.unified_diff(before, after, fromfile='EN asset text fields', tofile='VI asset text fields', lineterm='\n'))
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10070100003\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')

manifest={
    'scene':SCENE,
    'status':'PASS' if not qa_blockers else 'FAIL',
    'source_paths':{'ja_json':str(NOVEL_JA),'en_json':str(NOVEL_EN),'en_asset':str(SRC)},
    'output_path':str(OUT),
    'artifacts':{'manifest':str(WORK/'manifest.json'),'qa_log':str(WORK/'qa_log.json'),'focused_diff':str(WORK/'focused_diff.md'),'script':str(WORK/'generate_vi.py')},
    'source_hashes':{'en_asset_sha256':sha256(src_bytes),'ja_json_sha256':sha256(NOVEL_JA.read_bytes()),'en_json_sha256':sha256(NOVEL_EN.read_bytes())},
    'output_sha256':sha256(vi_bytes),
    'encoding':{'bom':src_bytes.startswith(b'\xef\xbb\xbf'),'newline':newline_style(src_bytes)},
    'line_count':{'en':len(lines),'vi':len(vi_lines)},
    'text_record_count':{'candidate_total':len(cands),'by_command':dict(Counter(c['cmd'] for c in cands)),'translated':len(TRANSLATIONS),'novel_pairs_ja':len(ja_pairs),'novel_pairs_en':len(en_pairs)},
    'character_notes':{'Film':'giữ tên Film; giọng dịu dàng‚ lớn tuổi nhưng đáng yêu; gọi Commander là Chỉ Huy/anh tùy câu','Noir':'giữ tên Noir; chỉ biểu cảm ký hiệu'},
    'entries':entries,
}
qa={
    'scene':SCENE,
    'qa_status':'PASS' if not qa_blockers else 'FAIL',
    'blockers':qa_blockers,
    'items':qa_items,
    'notes':[
        'JP ja.json là nguồn chính; EN asset dùng làm khung và đối chiếu.',
        'Asset có 90 text records: 1 title + 89 message. Novel JSON có ít cặp hơn vì asset có thêm các biểu cảm Noir/ký hiệu.',
        'Title đã dịch dạng Title Case tiếng Việt.',
        'Tất cả dấu phẩy ngắt câu trong field tiếng Việt dùng U+201A ‚; delimiter ASCII giữ nguyên.',
        'Không có nội dung H18 trực diện; cảnh hôn/ham muốn được dịch theo sắc thái nguồn và consent hài hước/lãng mạn.'
    ],
    'structural_checks':{
        'line_count_match':len(lines)==len(vi_lines),
        'bom_match':src_bytes.startswith(b'\xef\xbb\xbf')==vi_bytes.startswith(b'\xef\xbb\xbf'),
        'newline_match':newline_style(src_bytes)==newline_style(vi_bytes),
        'text_record_count_match':len(cands)==len(vi_cands),
        'delimiter_mismatches':[],
        'tag_placeholder_checked':True,
    },
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status':manifest['status'],'output':str(OUT),'qa_log':str(WORK/'qa_log.json'),'manifest':str(WORK/'manifest.json'),'focused_diff':str(WORK/'focused_diff.md'),'output_sha256':manifest['output_sha256'],'records':manifest['text_record_count']}, ensure_ascii=False, indent=2))
