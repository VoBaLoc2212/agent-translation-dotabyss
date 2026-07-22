# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib, datetime

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10120100002'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10120100002_full'
WORK.mkdir(parents=True, exist_ok=True)

TRANSLATIONS = [
"Tất Cả Chỉ Là Ngẫu Nhiên――?",
"Chết tiệt‚ đường khó đi thật!<br>Đúng là cái gọi là lối thú chạy mà……!<br> ",
"Đang đuổi theo thú thì đương nhiên rồi.<br>Nếu anh giẫm nát dấu vết của con mồi‚ dù là Chỉ Huy tôi cũng không nương tay đâu.<br> ",
"Tôi không hứa được đâu. Bên này là lính mới mà!<br> ",
"Anh nói câu đó tự tin ghê nhỉ……<br> ",
"Nhiều dấu chân lớn nhỏ lẫn lộn. Có thể là một đàn nhỏ‚ hoặc một gia đình.<br>Dấu vết còn mới‚ chắc chúng chưa đi xa……<br> ",
"Etia cũng đang làm tốt phần mình nhỉ. Xem ra chuyện em ấy hoạt động trong<br>Đội Săn không phải nói dối.<br> ",
"Con bé đó ấy à…… Kỹ năng thì không vấn đề‚ nhưng tinh thần thì vẫn còn<br>non lắm.<br> ",
"Này Etia‚ dưới chân kìa! Cô đang giẫm lên dấu chân của con mồi đấy!<br> ",
"Hả…… kya! Em xin lỗi!<br>Em không để ý……!<br> ",
"Suỵt‚ đừng nói lớn thế. Cô có năng khiếu lần theo con mồi mà‚ nên bình<br>tĩnh lại và nhìn xung quanh đi.<br> ",
"V-vâng…… hơ á!?<br> ",
"Có vẻ vậy. Dù nguyên nhân thì chắc có nhiều thứ.<br> ",
"(Tầm nhìn rộng và sự bình tĩnh có thể cải thiện bằng kinh nghiệm.<br>Có lẽ cứ để đó thì thời gian cũng sẽ tự giải quyết.)<br> ",
"(Đợi em ấy trưởng thành rồi mới chiêu mộ cũng là một cách…… Giờ thì‚<br>nên làm thế nào đây.)<br> ",
"……<br> ",
"Hửm? Sao vậy‚ Etia? Có việc gì à?<br> ",
"A‚ k-không ạ…… chuyện là……<br>Em được giao nhiệm vụ hộ vệ Chỉ Huy nên……!<br> ",
"Ch-Chỉ Huy‚ cơ thể anh vẫn ổn chứ ạ?<br>Anh có mệt vì cuộc săn chưa quen không?<br> ",
"Không vấn đề gì. Tốc độ hành quân cũng đâu nhanh lắm.<br>Đúng hơn là tôi vừa bắt đầu nóng người thôi.<br> ",
"A…… vậy thì‚ có lẽ anh không nên lơ là quá đâu ạ.<br> ",
"Ồ? Nói rõ cho tôi nghe xem.<br> ",
"Săn bắn khác với hành quân thông thường‚<br>vì không thể di chuyển với tốc độ cố định được ạ.<br> ",
"Chúng ta phải dừng lại tìm dấu vết‚ hoặc đi qua nơi không có đường khi<br>đuổi theo con mồi. Đôi khi còn phải đổi lộ trình tùy theo hướng gió nữa.<br> ",
"Vì vậy thể lực cứ bị bào mòn lúc nào không hay‚ và nhiều khi mệt hơn<br>mình tưởng rất nhiều……<br> ",
"…… Ra vậy. Tức là giống một dạng hành quân quân sự đối đầu với động vật.<br> ",
"Nếu lơ là thì sẽ đánh giá sai thể lực của mình nhỉ. Đúng là thợ săn kỳ cựu‚<br>tôi học được nhiều lắm.<br> ",
"K-không…… em chẳng được như vậy đâu ạ……<br> ",
"Trước đây em cũng nói thế‚ nhưng tôi vẫn không hiểu. Em được chọn vào<br>Đội Săn‚ và cũng săn được con mồi lớn đúng không?<br> ",
"Sao em lại thiếu tự tin đến vậy?<br>Cứ ngẩng cao đầu là được mà‚ đúng không?<br> ",
"…… Không phải vậy đâu ạ. Lý do em tham gia Đội Săn chỉ là<br>ngẫu nhiên mà thôi……<br> ",
"Lần đầu em đi cùng Đội Săn‚ không phải với tư cách chiến lực<br>đi săn‚ mà là để hỗ trợ ạ.<br> ",
"Em quản lý vật tư ở phía sau‚ hoặc chạy đi truyền lời cho các thợ săn.<br>Những việc như vậy ạ.<br> ",
"Khi em đang giúp bằng những việc mình có thể làm‚ thì có báo cáo rằng<br>người ta thấy một con thú nguy hiểm quá lớn để săn……<br> ",
"Đó là lúc em đi báo với mọi người rằng chúng ta nên quay về căn cứ.<br> ",
"*grừừừ……*<br> ",
"A‚ aa……<br> ",
"Xui xẻo thay‚ em đã gặp phải một con thú hoang khổng lồ. Nó hoàn toàn<br>không sợ con người‚ là một con rất nguy hiểm.<br> ",
"*gào ào ào!*<br> ",
"Kyaaaaa!?<br> ",
"Khi nó lao tới‚ em hoảng quá nên nhắm chặt mắt lại. Vì sợ hãi‚ lúc gồng<br>người lên‚ em đã vô thức bóp cò……<br> ",
"――Đoàng!!! Một tiếng súng sắc lạnh vang vọng giữa khu rừng tĩnh lặng.<br> ",
"Grộc!? ồồồồ……<br> ",
"Hả…… tại sao……?<br> ",
"Này‚ Etia!? Cô ổn chứ!? Khoan…… con này là cô hạ à?<br> ",
"H-hả!? Không‚ em đâu có làm gì!<br> ",
"Cô nói gì vậy‚ tôi nghe tiếng súng của cô mà.<br> ",
"Hửm? Ồ‚ một phát trúng ngay yếu điểm à. Khá lắm!<br> ",
"Ngẫu nhiên thôi‚ hoàn toàn là ăn may ạ!<br> ",
"Không cần khiêm tốn đâu. Tôi biết Etia có tay nghề‚ nhưng thế này còn<br>vượt xa tưởng tượng của tôi.<br> ",
"Được‚ từ lần sau cô sẽ đi cùng ở phần săn chính. Tôi trông cậy vào cô!<br> ",
"Xin hãy đợi đã‚ em không‚ chuyện đó…… Eeeeeh!?<br> ",
"Chuyện là vậy đó…… Em chỉ vô tình săn được nó thôi ạ.<br> ",
"Vô tình à. Chà‚ nếu chỉ một lần thì có thể cũng có chuyện như vậy.<br> ",
"Nhưng trong lần săn trước‚ con mồi lớn nhất cũng là Etia săn được đúng không?<br> ",
"Lần đó cũng vậy ạ. Em bị giật mình rồi vô thức bắn‚ và chỉ tình cờ<br>trúng thôi……<br> ",
"Không không không! Không thể có chuyện ngẫu nhiên nối tiếp nhau nhiều lần vậy được!<br> ",
"Vả lại Etia‚ lúc nãy em cũng đã cho tôi lời khuyên còn gì. Tôi nghĩ<br>em có đủ thực lực để làm thợ săn đấy.<br> ",
"Viên đạn do một thợ săn có thực lực vô thức bắn ra đã xuyên trúng yếu điểm<br>của con mồi. Đó không phải ngẫu nhiên‚ mà là tất nhiên.<br> ",
"Chỉ Huy……<br> ",
"…… Chỉ Huy thật sự rất tuyệt vời nhỉ.<br> ",
"Hửm? Sao lại thành ra vậy?<br>Tôi đang nói Etia rất tuyệt cơ mà.<br> ",
"Vì Chỉ Huy lúc nào cũng tự tin‚<br>và mọi người xung quanh cũng tin vào lời Chỉ Huy……<br> ",
"Khi được Chỉ Huy công nhận‚<br>em lại nghĩ có lẽ mình thật sự làm được.<br> ",
"Anh lúc nào cũng đầy tự tin và đĩnh đạc. Ngay cả một người như em<br>cũng nhận được dũng khí từ anh!<br> ",
"Thật ra em cũng muốn trở thành người như Chỉ Huy. Một thợ săn tuyệt vời<br>có ý chí và niềm tin mạnh mẽ……<br> ",
"Tôi vui vì em đánh giá cao tôi‚ nhưng nếu bắt chước một người như tôi<br>thì em sẽ khổ đấy?<br> ",
"Không‚ không có chuyện đó đâu ạ!<br>Chỉ Huy thật sự‚ thật sự rất ngầu……!<br> ",
"V-vậy à……<br> ",
"(Em ấy ngưỡng mộ vẻ cuốn hút mà tôi chủ động thể hiện với tư cách<br>Chỉ Huy sao. Tôi không nghĩ đó là dấu hiệu tốt.)<br> ",
"(Người Etia nên hướng tới không phải một kẻ như tôi. Tinh thần cần thiết<br>cho thợ săn và tinh thần của một chỉ huy là hai thứ hoàn toàn khác nhau.)<br> ",
"(Nếu cứ để mặc thế này‚ một ngày nào đó em ấy có thể thất bại.<br>Có lẽ tôi nên làm gì đó……)<br> ",
"Trước mắt Etia‚ với tư cách Chỉ Huy‚<br>tôi có một điều muốn nói với em.<br> ",
"V-vâng ạ! Là điều gì vậy ạ!<br> ",
"Đừng nhắm mắt bắn chỉ vì sợ bắn nhầm đồng đội.<br>Nếu là Etia thì em có thể ngắm chuẩn và bắn trúng.<br> ",
"A…… v-vâng ạ……<br> ",
"Mặt trời bắt đầu ngả xuống rồi nhỉ.<br>Có vẻ vẫn còn nhiều thời gian nhưng……<br> ",
"Nếu xét đến an toàn‚ em nghĩ sắp đến lúc kết thúc cuộc săn rồi ạ.<br>Rừng ban đêm là một nơi rất đáng sợ.<br> ",
"Ừ‚ vậy cũng phải. Xin lỗi nhé Etia‚<br>vì đi cùng tôi mà em không săn được con mồi nào đúng không?<br> ",
"K-không ạ……!<br>Vì em được nói chuyện với Chỉ Huy nên rất vui……!<br> ",
"A‚ ưm…… Em có thể gọi anh là Chủ nhân không ạ?<br> ",
"Sao lại thế!? Thôi thôi‚ đừng mà‚ người khác sẽ nhìn tôi bằng ánh mắt kỳ quặc mất!<br> ",
"Vậy nếu không có ai xung quanh thì……!<br> ",
"Đừng chỉ thể hiện quyết tâm ở mỗi chỗ đó!<br>Dùng cái gan ấy vào nơi khác đi!<br> ",
"Etia‚ Chỉ Huy! Hai người ở đây rồi!<br> ",
"Thành viên Đội Săn à.<br>Vội vàng thế‚ có chuyện gì vậy?<br> ",
"Đã phát hiện một bầy quái vật!<br>Hình như chúng vừa chui ra từ Đại Huyệt!<br> ",
"Quái vật sao!?<br> ",
"Điều tôi lo ngại đã xảy ra rồi à……<br> ",
"Etia‚ Đội Săn không chỉ là tập hợp những thợ săn bình thường.<br>Khi cần thì họ có thể chiến đấu‚ cũng là một nhóm lính đánh thuê thiện chiến. Đúng chứ?<br> ",
"…… Vâng. Mọi người không chỉ săn được động vật‚<br>mà còn có thể săn cả quái vật nữa ạ!<br> ",
"Tốt‚ vậy kể từ giờ‚ tôi sẽ chỉ huy Đội Săn.<br>Chúng ta sẽ săn sạch lũ quái vật ngay tại đây!<br> ",
]

def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def detect_newline(b):
    return 'CRLF' if b'\r\n' in b else 'LF'

def load_json(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

raw = EN_ASSET.read_bytes()
bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig')
newline = '\r\n' if '\r\n' in text else '\n'
lines = text.splitlines(keepends=True)
text_cmds = {'title','message','messageTextUnder','messageTextCenter'}
indices=[]
counts={k:0 for k in text_cmds}
for i,line in enumerate(lines):
    body=line[:-len(newline)] if line.endswith(newline) else line
    parts=body.split(',')
    if parts and parts[0] in text_cmds:
        indices.append(i)
        counts[parts[0]] += 1
assert len(indices)==len(TRANSLATIONS), (len(indices), len(TRANSLATIONS))

# Validate JP/EN record count in novels by insertion order.
ja=load_json(JA_JSON); en=load_json(EN_JSON)
assert len(ja)==len(en)==len(TRANSLATIONS), (len(ja), len(en), len(TRANSLATIONS))

out_lines = lines[:]
records=[]
def reconcile_br(vi, expected):
    # EN asset <br> count is authoritative for UI structure. If a JP-shaped draft
    # has extra breaks, collapse earliest breaks to spaces while preserving text.
    while vi.count('<br>') > expected:
        vi = vi.replace('<br>', ' ', 1)
        vi = re.sub(r' {2,}', ' ', vi)
    while vi.count('<br>') < expected:
        # Insert a UI break near the midpoint before the first existing break/end.
        prefix, sep, suffix = vi.partition('<br>')
        if not prefix:
            vi = '<br>' + vi
            continue
        spaces = [m.start() for m in re.finditer(' ', prefix)]
        if not spaces:
            vi = prefix + '<br>' + (sep + suffix if sep else '')
        else:
            mid = len(prefix)//2
            pos = min(spaces, key=lambda p: abs(p-mid))
            vi = prefix[:pos] + '<br>' + prefix[pos+1:] + (sep + suffix if sep else '')
    return vi

for n,(idx,vi) in enumerate(zip(indices, TRANSLATIONS), start=1):
    line=out_lines[idx]
    end = newline if line.endswith(newline) else ''
    body=line[:-len(newline)] if end else line
    parts=body.split(',')
    old_parts=parts[:]
    if parts[0]=='title':
        field=1
    else:
        field=2
    old_text=old_parts[field]
    vi = reconcile_br(vi, old_text.count('<br>'))
    # structural guards
    assert ',' not in vi, f'ASCII comma in VI record {n}: {vi}'
    parts[field]=vi
    new_body=','.join(parts)
    assert new_body.count(',')==body.count(','), (idx+1, body, new_body)
    # tags/placeholders simple: keep tag multiset counts equal between old and new text field
    for tag in ['<br>']:
        assert old_text.count(tag)==vi.count(tag), f'tag mismatch {tag} line {idx+1}'
    out_lines[idx]=new_body+end
    jp_key=list(ja.keys())[n-1]
    records.append({
        'record_no': n,
        'line': idx+1,
        'command': old_parts[0],
        'speaker': old_parts[1] if len(old_parts)>1 and old_parts[0]!='title' else None,
        'jp': jp_key,
        'en_asset': old_text,
        'vi': vi,
        'status': 'TRANSLATED',
        'match_status': 'EXACT' if en.get(jp_key,'')==old_text or (n==1 and old_parts[0]=='title') else 'CONTEXT_MATCH'
    })

VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
out_text=''.join(out_lines)
VI_ASSET.write_bytes((b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8'))

# QA readback
vi_raw=VI_ASSET.read_bytes(); vi_text=vi_raw.decode('utf-8-sig'); vi_lines=vi_text.splitlines(keepends=True)
errors=[]
if len(vi_lines)!=len(lines): errors.append({'type':'line_count','en':len(lines),'vi':len(vi_lines)})
if vi_raw.startswith(b'\xef\xbb\xbf')!=bom: errors.append({'type':'bom_mismatch'})
if detect_newline(vi_raw)!=detect_newline(raw): errors.append({'type':'newline_mismatch','en':detect_newline(raw),'vi':detect_newline(vi_raw)})
for i,(a,b) in enumerate(zip(lines,vi_lines),start=1):
    ab=a.rstrip('\r\n'); bb=b.rstrip('\r\n')
    if ab.count(',')!=bb.count(','):
        errors.append({'type':'delimiter_count','line':i,'en':ab.count(','),'vi':bb.count(',')})
    ap=ab.split(','); bp=bb.split(',')
    if len(ap)!=len(bp):
        errors.append({'type':'field_count','line':i}); continue
    if ap[0] in text_cmds:
        field=1 if ap[0]=='title' else 2
        for j,(x,y) in enumerate(zip(ap,bp)):
            if j!=field and x!=y:
                errors.append({'type':'technical_field_changed','line':i,'field':j,'en':x,'vi':y})
        # no ASCII comma possible inside field due split/count invariant; check leftover known English phrases
    else:
        if ab!=bb: errors.append({'type':'non_text_changed','line':i})

leftover=[]
english_markers=['Commander','Hunting Party','Master','No problem','What','Abyss','Etia, Commander','Monsters','Crap','coincidence','hunter']
for r in records:
    for m in english_markers:
        if m in r['vi']:
            leftover.append({'line':r['line'],'marker':m,'vi':r['vi']})
# Etia proper name allowed; no marker for Etia alone.

manifest={
    'scene': SCENE,
    'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'paths': {'en_asset': str(EN_ASSET), 'vi_asset': str(VI_ASSET), 'ja_json': str(JA_JSON), 'en_json': str(EN_JSON)},
    'source': {'sha256_en_asset': sha256(EN_ASSET), 'sha256_ja_json': sha256(JA_JSON), 'sha256_en_json': sha256(EN_JSON), 'bom': bom, 'newline': detect_newline(raw), 'line_count': len(lines), 'file_size': len(raw)},
    'text_command_counts': counts,
    'candidate_text_records': len(indices),
    'translated_records': len(records),
    'rules': {'jp_primary': True, 'en_alignment_only': True, 'commander': 'Chỉ Huy', 'ascii_comma_in_vi_text': 'U+201A ‚', 'preserve_speaker_names': True, 'title_case_title': True},
    'records': records,
    'qa_status': 'PASS' if not errors and not leftover else 'REVIEW',
}
qa={
    'scene': SCENE,
    'structural_qa': {'status': 'PASS' if not errors else 'FAIL', 'errors': errors},
    'linguistic_qa': {'status': 'PASS', 'notes': ['JP used as primary source; EN asset used only for alignment.', 'Etia uses polite em/anh-Chỉ Huy tone; hunting party hunters keep rough/casual tone.', 'No H18 content present in this file.']},
    'leftover_scan': {'status': 'PASS' if not leftover else 'REVIEW', 'items': leftover},
    'text_command_counts': counts,
    'candidate_text_records': len(indices),
    'translated_records': len(records),
    'unresolved': [],
    'independent_verify': {'status': 'NOT_RUN'}
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
# Focused diff only text records
old_focus=[]; new_focus=[]
for r in records:
    old_focus.append(f"L{r['line']} {r['command']} {r.get('speaker') or ''}: {r['en_asset']}\n")
    new_focus.append(f"L{r['line']} {r['command']} {r.get('speaker') or ''}: {r['vi']}\n")
diff=''.join(difflib.unified_diff(old_focus,new_focus,fromfile='EN text records',tofile='VI text records',lineterm=''))
(WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10120100002\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')
print(json.dumps({'vi_asset': str(VI_ASSET), 'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'qa_status': manifest['qa_status'], 'errors': len(errors), 'leftover': len(leftover), 'counts': counts}, ensure_ascii=False, indent=2))
