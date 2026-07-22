from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE = 'hmn_10050100001'
EN_ASSET = Path('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10050100001.txt')
VI_ASSET = Path('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10050100001.txt')
JA_JSON = Path('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10050100001/ja.json')
EN_JSON = Path('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10050100001/en.json')
WORK = Path('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10050100001_full')
WORK.mkdir(parents=True, exist_ok=True)

TEXT_TYPES = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}
TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r'%(?:\d+\$)?[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]|%%')

vi = [
    'Tiêu Đề',
    'Ừm… có lẽ mình hơi vội thật chăng?<br> ',
    'Chỉ Huy‚ anh sao vậy?<br> ',
    'Hử? Em là người mà Adelheid đã giới thiệu… tên em là Electra‚<br>phải không?<br> ',
    'Vâng. Hoàn toàn chính xác. Anh có điều gì lo lắng sao?<br> ',
    'Ừ. Khu vực này đến vừa rồi vẫn còn quái vật nhưng chúng ta đã<br>trấn áp an toàn. Giờ thợ mỏ đang khai thác‚ nhưng—<br> ',
    'Anh đang hối hận vì có lẽ mình đã điều chủ lực sang hiện trường<br>khác hơi sớm.<br> ',
    'Em hiểu rồi. Sau khi ra lệnh‚ anh đã nhận ra nguy cơ quái vật<br>có thể tấn công lần nữa‚ đúng không?<br> ',
    'Xét theo tầng này thì khả năng đó thấp‚ nhưng anh vẫn lo nếu<br>mọi chuyện chuyển biến xấu.<br> ',
    'Em có hai điều muốn trình lên. Có được không ạ?<br> ',
    'Hử? Cứ nói đi.<br> ',
    'Thứ nhất: vì anh là Chỉ Huy‚ thái độ thận trọng ấy rất đáng hoan nghênh.<br>Suy nghĩ của anh chắc chắn sẽ kéo dài sinh mạng cho cấp dưới.<br> ',
    'Thứ hai: nỗi lo vừa rồi là không cần thiết. Bởi vì Electra đang<br>túc trực bên cạnh anh.<br> ',
    'Haha‚ em có vẻ tự tin ghê nhỉ.<br> ',
    'Em chỉ đang trình bày sự thật. Nhưng nếu đã khiến anh khó chịu thì<br>em xin lỗi.<br> ',
    '—Ngay sau khi Electra nói vậy‚ một tiếng động lớn vang vọng xung quanh.<br> ',
    'Có chuyện gì vậy?<br> ',
    'Chỉ Huy. Trên vách đá đã mở ra một lỗ hổng. Em cũng đã phát hiện<br>bóng dáng quái vật.<br> ',
    'Không ổn rồi… nỗi lo của anh thành sự thật mất rồi. Ngoài em ra‚<br>ở đây chỉ có thợ mỏ và công binh thôi!<br> ',
    'Không có vấn đề gì. Nguy hiểm sẽ do Electra loại bỏ. Chỉ Huy‚<br>xin hãy cho phép em xuất kích.<br> ',
    'Tất nhiên. Nhờ em đấy!<br> ',
    'Đã rõ‚ Chủ nhân. Xin hãy tận mắt chứng kiến toàn bộ năng lực của em.<br> ',
    'Electra lao đi‚ xông thẳng vào bầy quái vật.<br> ',
    '(…Nhanh quá!)<br> ',
    'Phát hiện bóng địch. Khóa mục tiêu. Bắt đầu tấn công.<br> ',
    'Gí!?<br> ',
    'Electra áp sát quái vật rồi bắn nát chân chúng ở cự ly gần‚<br>sau đó kết liễu chúng bằng loạt hỏa lực tập trung.<br> ',
    'Đã tiêu diệt một mục tiêu. Tiếp tục tấn công. Sẽ duy trì cho đến<br>khi hoàn tất quét sạch.<br> ',
    'Bầy quái vật lao vào Electra khi cô xông lên.<br>Nhưng không hề biến sắc‚ cô xả đạn và lũ quái vật lần lượt gục xuống.<br> ',
    'Hỏa lực cũng ở mức cao sao.<br>…Ra vậy. Thế thì em ấy tự tin cũng là phải.<br> ',
    'Số lượng kẻ địch không hề ít‚ nhưng sức mạnh của Electra áp đảo hoàn toàn. Bằng những động tác không chút thừa thãi‚ cô đã tiêu diệt sạch quái vật chỉ trong chớp mắt.',
    '—Vậy là không ai bị thương. Việc khai thác mạch quặng cũng hoàn tất an toàn.<br>Tất cả là nhờ Electra.<br> ',
    'Ra vậy! Cô ấy đã lập công lớn nhỉ!<br> ',
    'Em rất vinh dự khi được khen ngợi.<br> ',
    'Tôi đã nói rồi đúng không? Electra là một người máy hoàn hảo.<br>Cô ấy nhất định sẽ trở thành trợ lực.<br> ',
    'Hử? An…droid…?<br> ',
    'Anh quên rồi sao‚ Chỉ Huy? Trước đây tôi đã giải thích rồi mà…<br> ',
    'Electra. Hãy giải thích lại một lần nữa.<br> ',
    'Người máy dạng người là robot sở hữu năng lực xử lý và khả năng vận động cao.<br>Nói là búp bê máy móc thì anh có dễ hiểu hơn không ạ?<br> ',
    'Tức là không phải con người‚ đúng không.<br> ',
    'Electra không cần ăn uống hay ngủ nghỉ. Nếu được Adelheid bảo trì<br>định kỳ‚ em có thể tiếp tục hoạt động.<br> ',
    'Vì vậy‚ có thể kỳ vọng em phát huy trong các nhiệm vụ ở nơi con người<br>khó hoạt động hoặc môi trường khó tiếp tế.<br> ',
    'Hơn nữa‚ hiệu năng của Electra cao hơn người máy thông thường rất nhiều.<br>Do đó khó sản xuất hàng loạt‚ nhưng một mình cô ấy hẳn sẽ mang lại thành quả lớn.<br> ',
    'Tuyệt thật.<br>Dù là búp bê mà cách đối đáp khi trò chuyện hoàn toàn không gượng gạo…<br> ',
    'Đó hẳn là nhờ chương trình tư duy được cài trong Electra rất<br>ưu tú.<br> ',
    'Khác với con người‚ cô ấy không có trái tim nên sẽ ngoan ngoãn phục tùng Chỉ Huy.<br>Cô ấy sẽ trung thành tuân theo mệnh lệnh. Có thể gọi là người lính lý tưởng.<br> ',
    'Ồ. Đúng là một tồn tại tiện lợi nhỉ.<br> ',
    'Vâng‚ đúng vậy. Nhân tiện‚ người máy được trang bị chức năng thỏa mãn<br>dục vọng tình dục được gọi là sexaroid.<br> ',
    'Đó là cỗ máy như trong mơ có thể đáp ứng mọi yêu cầu‚ nhưng thật ra<br>Electra cũng—<br> ',
    'Cái… cũng có cách dùng đó nữa sao…!?<br>Nghĩa là nếu nhờ em ấy làm chuyện này chuyện kia thì cũng không bị ghét…?<br> ',
    'C-Chỉ Huy! Chuyện sexaroid xin hãy để hôm khác<br>nói với cô Adelheid ở nơi khác ạ!<br> ',
    'Không cần bận tâm đâu‚ cô Alicia.<br> ',
    'Nếu anh mong muốn‚ Electra sẽ làm bất cứ điều gì cho anh‚ Chủ nhân.<br> ',
    'Chủ nhân…!?<br> ',
    'Ra vậy… đúng là chạm vào tâm lý đàn ông. Một sexaroid tuyệt vời.<br> ',
    'Vả lại câu “sẽ làm bất cứ điều gì” thật là… ghê gớm.<br>Cụ thể thì Electra có thể làm những việc gì?<br> ',
    'Nếu liệt kê tất cả‚ chắc chắn em sẽ lấy mất vài ngày thời gian của Chỉ Huy‚<br>nên em xin tóm tắt từ một góc độ khác.<br> ',
    'Vai trò chính của Electra là duy trì cuộc sống lành mạnh cho chủ nhân—<br>lý tưởng là dùng hành động của mình để thỏa mãn cả thân lẫn tâm‚ làm phong phú cuộc đời chủ nhân.<br> ',
    'Vì mục đích đó‚ em có thể đáp ứng mọi mệnh lệnh.<br>Miễn là nội dung không quá mức.<br> ',
    'Quá mức là—những việc như thế nào?<br> ',
    'Ví dụ tiêu biểu là mệnh lệnh mà chỉ cần thực hiện cũng dễ hình dung rằng chủ nhân<br>sẽ mất nghiêm trọng sức quy tụ rồi đi đến hủy diệt.<br> ',
    'Nếu bị ra lệnh bằng mọi giá thì em sẽ thực hiện‚ nhưng—<br>khi rõ ràng không dẫn tới cuộc sống lành mạnh‚ em sẽ dâng lời khuyên.<br> ',
    'Tức là những mệnh lệnh kiểu công việc mà hầu gái hay cấp dưới làm<br>thì em sẽ nghe theo đúng không?<br> ',
    'Nếu không vượt khỏi lẽ thường‚ nhìn chung là<br>đúng như vậy.<br> ',
    'Ra vậy. Electra‚ anh muốn nhờ em một việc ngay bây giờ.<br> ',
    'Sổ sách đang tồn đọng‚ em xử lý thay anh được không?<br>Đây là sổ cái.<br> ',
    'Việc nhỏ thôi ạ.<br> ',
    '…………Đã hoàn tất.<br> ',
    'Nhanh thế!?<br> ',
    'Tuyệt quá! Em làm còn hơn cả mong đợi!<br> ',
    'X-Xin phép! Hàng hóa bị đổ trên phố chính!<br>Cứ thế này giao thông sẽ tắc nghẽn mất!<br> ',
    'Chủ nhân. Anh có thể giao việc này cho Electra không ạ?<br>Em sẽ dọn dẹp ngay lập tức.<br> ',
    '……<br> ',
    '……Đã hoàn tất.<br> ',
    'M-Mới đó thôi sao!?<br> ',
    'Chỉ Huy! Gia súc chạy thoát mất rồi…<br> ',
    'Xin cứ giao cho em‚ Chủ nhân.<br> ',
    '……Đã bắt giữ heo.<br> ',
    '……Đã bắt giữ bò.<br> ',
    '……Đã bắt giữ gà. Hoàn tất.<br> ',
    'T-Tuyệt quá! Cảm ơn rất nhiều!<br> ',
    'C-Cô thực sự xử lý xong ngay lập tức rồi nhỉ.<br> ',
    'Ừ‚ đúng là đáng nể.<br> ',
    'Cảm ơn anh.<br>Nếu anh có hy vọng hay yêu cầu gì‚ xin cứ sai bảo em bất cứ điều gì.<br> ',
    'Hử? Vậy thử tạo một dáng thật dễ thương xem nào.<br>Kiểu ưỡn khe ngực ra ấy‚ nhờ em.<br> ',
    'Như thế này… đúng không ạ?<br> ',
    '…Trông mềm mại thật.<br>Vả lại còn thơm nữa.<br> ',
    '…Nhân tiện‚ em có thể nói dễ thương hơn một chút không?<br> ',
    'Chủ nhân ơi! Electra thích Chủ nhân nhất đấy!<br>Xin hãy nhìn‚ chạm vào và cảm nhận em tùy thích nhé♡<br> ',
    '!?<br> ',
    'Như vậy đã được chưa ạ?<br> ',
    '…Tuyệt nhất rồi.<br>Lát nữa gối đùi cho anh nữa nhé.<br> ',
    'C-Chỉ Huy!<br>Xin đừng trêu đùa cô Electra nữa ạ!<br> ',
    'Không sao đâu.<br>Em đáp ứng mọi mệnh lệnh của con người.<br> ',
    'Nhưng mà…<br> ',
    'Electra‚ em có thể làm Alicia rung động không?<br>Anh muốn cô ấy hiểu cảm giác của anh.<br> ',
    'Rung động—cụ thể là như thế nào ạ?<br> ',
    'Hãy giả làm một mỹ nam rồi thử tán tỉnh Alicia xem.<br> ',
    'Đã rõ.<br> ',
    '…Này‚ mèo con. Đừng giận dữ thế chứ.<br>Phí mất vẻ đẹp của em đấy?<br> ',
    'Hyaa!? T-Tự nhiên cô làm gì vậy—<br> ',
    'Làm gì ư‚ đó là sự thật.<br>Mèo con của anh—nào‚ hãy lao vào vòng tay anh đi?<br> ',
    'Waa! Chỉ Huy! Thế này không được đâu! Xin hãy bảo cô ấy dừng lại đi mà!<br> ',
    'Nhưng Alicia. Ngoài xấu hổ ra còn cảm xúc khác nữa đúng không?<br>Em hiểu cảm giác của anh mà?<br> ',
    'Ư-ưư…<br> ',
    'Electra‚ em làm tốt lắm. Anh rất hài lòng.<br> ',
    '—Thật sao ạ?<br> ',
    'Ừ. Anh thấy tuyệt lắm. Nhờ em đến đây mà mọi chuyện sẽ lại vui hơn rồi.<br>Từ giờ mong em giúp đỡ nhé.<br> ',
    '…! …Cảm ơn anh‚ rất nhiều.<br> ',
    'Những lời ấy chính là lý do tồn tại của Electra.<br>Từ nay về sau xin hãy tiếp tục chiếu cố em‚ Chủ nhân—<br> ',
]

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def props(raw):
    bom = raw.startswith(b'\xef\xbb\xbf')
    if b'\r\n' in raw and raw.count(b'\r\n') == raw.count(b'\n'):
        nl = 'CRLF'
        newline = '\r\n'
    else:
        nl = 'LF'
        newline = '\n'
    return bom, nl, newline

def text_idx(parts):
    if not parts: return None
    return TEXT_TYPES.get(parts[0])

raw = EN_ASSET.read_bytes()
bom, nl_name, newline = props(raw)
text = raw.decode('utf-8-sig' if bom else 'utf-8')
lines = text.splitlines(True)
candidates = []
for idx, line in enumerate(lines):
    body = line[:-2] if line.endswith('\r\n') else (line[:-1] if line.endswith('\n') else line)
    parts = body.split(',')
    ti = text_idx(parts)
    if ti is not None:
        candidates.append((idx, parts, ti, body))

blockers=[]; warnings=[]; entries=[]
if len(vi) != len(candidates):
    blockers.append({'code':'TRANSLATION_COUNT_MISMATCH','expected':len(candidates),'actual':len(vi)})

out_lines = lines[:]
for n, (idx, parts, ti, body) in enumerate(candidates):
    old_text = parts[ti]
    new_text = vi[n] if n < len(vi) else old_text
    if ',' in new_text:
        blockers.append({'code':'ASCII_COMMA_IN_VI_TEXT','candidate_index':n+1,'line':idx+1,'text':new_text})
    if TAG_RE.findall(old_text) != TAG_RE.findall(new_text):
        blockers.append({'code':'TAG_MISMATCH','candidate_index':n+1,'line':idx+1,'source':TAG_RE.findall(old_text),'vi':TAG_RE.findall(new_text)})
    if PLACEHOLDER_RE.findall(old_text) != PLACEHOLDER_RE.findall(new_text):
        blockers.append({'code':'PLACEHOLDER_MISMATCH','candidate_index':n+1,'line':idx+1})
    old_sig = parts[:ti] + parts[ti+1:]
    parts2 = parts[:]
    parts2[ti] = new_text
    new_body = ','.join(parts2)
    new_sig = parts2[:ti] + parts2[ti+1:]
    if old_sig != new_sig:
        blockers.append({'code':'TECH_FIELDS_CHANGED','candidate_index':n+1,'line':idx+1})
    if body.count(',') != new_body.count(','):
        blockers.append({'code':'DELIMITER_COUNT_CHANGED','candidate_index':n+1,'line':idx+1,'source_commas':body.count(','),'vi_commas':new_body.count(',')})
    ending = '\r\n' if lines[idx].endswith('\r\n') else ('\n' if lines[idx].endswith('\n') else '')
    out_lines[idx] = new_body + ending
    entries.append({'candidate_index': n+1, 'line': idx+1, 'record_type': parts[0], 'speaker': parts[1] if len(parts)>1 else '', 'source_text': old_text, 'vi_text': new_text, 'match_status':'CONTEXT_MATCH' if n==1 or n==31 else 'EXACT', 'translation_status':'TRANSLATED', 'intentionally_identical': old_text == new_text})

out_text = ''.join(out_lines)
out_raw = (b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')

# Whole-file structural QA
out_decoded = out_raw.decode('utf-8-sig' if bom else 'utf-8')
out_lines_check = out_decoded.splitlines(True)
if len(out_lines_check) != len(lines):
    blockers.append({'code':'LINE_COUNT_MISMATCH','source':len(lines),'vi':len(out_lines_check)})
for i,(a,b) in enumerate(zip(lines,out_lines_check),1):
    abody = a[:-2] if a.endswith('\r\n') else (a[:-1] if a.endswith('\n') else a)
    bbody = b[:-2] if b.endswith('\r\n') else (b[:-1] if b.endswith('\n') else b)
    if abody.count(',') != bbody.count(','):
        blockers.append({'code':'LINE_DELIMITER_MISMATCH','line':i})
    ap = abody.split(','); bp = bbody.split(',')
    ti = text_idx(ap)
    if ti is not None and len(ap) == len(bp):
        if ap[:ti] + ap[ti+1:] != bp[:ti] + bp[ti+1:]:
            blockers.append({'code':'LINE_TECH_SIGNATURE_MISMATCH','line':i})
        if TAG_RE.findall(ap[ti]) != TAG_RE.findall(bp[ti]):
            blockers.append({'code':'LINE_TAG_MISMATCH','line':i})
        if PLACEHOLDER_RE.findall(ap[ti]) != PLACEHOLDER_RE.findall(bp[ti]):
            blockers.append({'code':'LINE_PLACEHOLDER_MISMATCH','line':i})

# Kept EN unchanged: none should remain except symbols logged.
unchanged = [e for e in entries if e['source_text'] == e['vi_text']]
allowed_unchanged = []
for e in unchanged:
    if e['source_text'].strip() in {'!?<br>'}:
        e['intentionally_identical'] = True
        e['intentional_reason'] = 'symbolic punctuation identical in JP/EN/VI'
        allowed_unchanged.append(e['candidate_index'])
    else:
        blockers.append({'code':'UNINTENTIONAL_KEPT_EN','line':e['line'],'text':e['source_text']})

# Targeted English leftovers likely not proper names / terms.
leftover_patterns = ['Commander','Master','Android','android','Sexaroid','sexaroid','Already','Amazing','Electra,','Adelheid,','Alicia,','Waaah','Eeek','Hey','kitten','whimper']
leftovers=[]
for e in entries:
    t=e['vi_text']
    for pat in leftover_patterns:
        if pat in t:
            # Sexaroid lowercase is an accepted coined term in VI; Electra/Adelheid/Alicia names allowed but ASCII comma prohibited catches punctuation
            if pat in {'sexaroid'}:
                continue
            leftovers.append({'line':e['line'],'pattern':pat,'text':t})
if leftovers:
    blockers.append({'code':'TARGETED_EN_LEFTOVER','items':leftovers[:20],'count':len(leftovers)})

if blockers:
    qa_status = 'FAIL'
else:
    qa_status = 'PASS'
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_raw)

# Diff only text records
before=[]; after=[]
for e in entries:
    line_no=e['line']
    before.append(f"L{line_no}: {e['source_text']}\n")
    after.append(f"L{line_no}: {e['vi_text']}\n")
diff=''.join(difflib.unified_diff(before, after, fromfile='EN text fields', tofile='VI text fields', lineterm='\n'))
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10050100001\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')

manifest = {
    'scene':SCENE,
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'source_paths': {'en_asset': str(EN_ASSET), 'ja_json': str(JA_JSON), 'en_json': str(EN_JSON)},
    'output_path': str(VI_ASSET),
    'artifact_paths': {'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'script': str(WORK/'generate_vi.py')},
    'source': {'bytes': len(raw), 'sha256': sha256(raw), 'bom': bom, 'newline': nl_name, 'line_count': len(lines)},
    'output': {'written': qa_status=='PASS', 'sha256': sha256(out_raw) if qa_status=='PASS' else None, 'bom': bom, 'newline': nl_name, 'line_count': len(out_lines_check)},
    'counts': {'title': sum(1 for _,p,_,__ in candidates if p[0]=='title'), 'message': sum(1 for _,p,_,__ in candidates if p[0]=='message'), 'messageTextUnder': sum(1 for _,p,_,__ in candidates if p[0]=='messageTextUnder'), 'messageTextCenter': sum(1 for _,p,_,__ in candidates if p[0]=='messageTextCenter'), 'candidate_text_records': len(candidates), 'translated_records': len(entries), 'unchanged_intentional_records': allowed_unchanged},
    'qa_status': qa_status,
    'entries': entries,
}
qa = {
    'scene':SCENE,
    'qa_status': qa_status,
    'blockers': blockers,
    'warnings': warnings,
    'notes': [
        'JP ja.json used as primary source; EN asset/en.json used for alignment and field preservation.',
        'All characters confirmed 18+ by project rule; adult/sexaroid-related lines translated normally while preserving tone and consent.',
        'Electra uses formal servant/android voice; Commander/司令官 translated as Chỉ Huy; ご主人様 translated as Chủ nhân.',
        'ASCII comma is forbidden inside VI text fields; U+201A used where a comma-like pause is needed.',
    ],
    'independent_verify': {
        'line_count_match': len(out_lines_check)==len(lines),
        'bom_preserved': out_raw.startswith(b'\xef\xbb\xbf') == bom,
        'newline_preserved': props(out_raw)[1] == nl_name,
        'delimiter_mismatches': [b for b in blockers if 'DELIMITER' in b.get('code','')],
        'technical_field_mismatches': [b for b in blockers if 'TECH' in b.get('code','')],
        'tag_mismatches': [b for b in blockers if 'TAG' in b.get('code','')],
        'placeholder_mismatches': [b for b in blockers if 'PLACEHOLDER' in b.get('code','')],
        'candidate_text_records': len(candidates),
        'translated_records': len(entries),
        'unintentional_kept_en_records': [b for b in blockers if b.get('code')=='UNINTENTIONAL_KEPT_EN'],
    }
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status':qa_status,'blockers':len(blockers),'candidates':len(candidates),'output_written':qa_status=='PASS','output':str(VI_ASSET)}, ensure_ascii=False, indent=2))
if blockers:
    print(json.dumps(blockers[:5], ensure_ascii=False, indent=2))
    raise SystemExit(1)
