from pathlib import Path
import json, hashlib, re, difflib

SCENE = 'evs_10200020701'
ROOT = Path('E:/AgentTranslation')
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/evs_10200020701_full'
WORK.mkdir(parents=True, exist_ok=True)

TEXT_TYPES = ('title','message','messageTextUnder','messageTextCenter')

TRANSLATIONS = [
"Tiêu Đề",
"Uốaaaaaaa!<br> ",
"Kíiiiiii——…!<br> ",
"Hê hê‚ thấy chưa! Đừng hòng tiến thêm một bước tới chỗ con người——!!<br> ",
"Tốt‚ lũ quái vật đang tụ lại vừa đẹp!<br>Tất cả mở đường bắn!<br> ",
"Ấy chết‚ thế này không ổn rồi! Tản ra‚ tản ra mau‚ anh em!<br> ",
"Shiraes‚ đến lúc rồi!<br> ",
"Nào‚ để tôi cho mọi người xem một màn pháo hoa thật hoành tráng!<br> ",
"Kít…!? Kíiiiiiiii——…!?<br> ",
"Ghê‚ ghê thật…! Hốt gọn một mẻ luôn…!<br>Đại tỷ Shiraes quả nhiên quá dữ!!<br> ",
"Chúng ta cũng không thể thua được! Cho chúng thấy khí phách của Quỷ tộc đi!<br> ",
"Ôôôôôôô~~~~~~~~~~~!!<br> ",
"(Tốt‚ sĩ khí đang lên rất đẹp. Quỷ tộc vốn dẻo dai‚<br>họ vẫn còn chiến đấu được lâu. Nhưng…)<br> ",
"Kíiiii~~~~~~~~!<br> ",
"(Dẻo dai đến mấy thì thể lực cũng có hạn. Họ sẽ<br>cầm cự được bao lâu trước làn sóng quái vật vô tận... đó mới là vấn đề.)<br> ",
"…Shiraes! Tình hình tinh thể thế nào rồi!?<br> ",
"Sức hút quái vật vẫn còn hoạt động. Năng lượng tích trữ trong nhiều ngày<br>đã bị nén lại nên không biết bao giờ nó mới cạn.<br> ",
"Ra vậy… nếu trận này kéo dài và chúng ta kiệt sức‚ cả bọn sẽ bị nghiền nát.<br>…Không còn cách nào khác.<br> ",
"Shiraes‚ tinh thể đó——phá hủy nó đi.<br> ",
"Quả là quyết đoán. Dù là mầm họa‚<br>nó vẫn là một bảo vật quý giá đấy.<br> ",
"Nếu không kiểm soát được thì với nhân loại nó chỉ là hiểm họa.<br>Mọi trách nhiệm để anh gánh. Làm đi.<br> ",
"Hì hì‚ đúng là Chỉ Huy mà tôi biết.<br>Anh không bao giờ nhìn nhầm điều quan trọng.<br> ",
"Tuy nhiên‚ tích đủ ma lực để phá hủy tinh thể sẽ mất thời gian.<br>Tôi phải rời khỏi tiền tuyến trong lúc đó — mọi người ổn chứ?<br> ",
"——Xin đừng lo! Chúng tôi sẽ cầm cự bao lâu cũng được!<br>Nhân danh niềm kiêu hãnh Quỷ tộc‚ tôi sẽ không để bất cứ con người nào bị thương!<br> ",
"Kureha… haha‚ em nói trước mất rồi.<br>Vậy đấy‚ Shiraes. Nhờ em cả.<br> ",
"Câu trả lời hay lắm. Vậy tôi giao lại cho mọi người.<br>Nhất định chúng ta sẽ cùng đón bình minh — tôi hứa.<br> ",
"Đã được nói như thế thì bên này cũng phải đáp lại kỳ vọng.<br>Đây là thời khắc quyết định! Tất cả‚ dốc hết sức đi!<br> ",
"Vâng! Trọng trách phu quân giao phó‚ em nhất định sẽ<br>hoàn thành!<br> ",
"Kí!<br> ",
"Gừ…! Chưa đâu!<br>Chừng đó còn lâu mới đánh bại được Quỷ tộc bọn ta!<br> ",
"Kíyaaaa…!<br> ",
"Cho tôi xem vết thương — chỗ này cần sơ cứu ngay!<br>Cô hãy lùi lại và đi chữa trị đi!<br> ",
"Tiểu thư Kureha… tôi thật mất mặt quá…!<br> ",
"(Không ổn rồi…! Đến cả Quỷ tộc cũng bắt đầu lộ rõ mệt mỏi.<br>Chưa có ai trọng thương‚ nhưng số người bị thương và phải rút lui đang tăng lên.)<br> ",
"Chuyện gì thế này...? Chẳng phải Quỷ tộc đang<br>lừa chúng ta rồi định giết chúng ta sao...?<br> ",
"Chiến đấu đến mức tả tơi như thế...<br>Khoan đã... họ đang bảo vệ chúng ta đúng không...? Chuyện này là sao?<br> ",
"Dáng vẻ chiến đấu tuyệt vọng của Quỷ tộc khiến dân làng bối rối.<br>Trông họ chẳng khác nào đang liều mình bảo vệ con người...<br> ",
"Quỷ tộc... thật sự là kẻ thù của chúng ta sao...?<br> ",
"(Dân làng cũng bắt đầu nhận ra rồi...<br>Đúng vậy. Hãy bỏ định kiến đi‚ tự nhìn bằng mắt mình và tự phán đoán.)<br> ",
"Nguy rồi...! Có một con lọt qua hướng đó!<br> ",
"Tiếng hét của Quỷ tộc vang lên — một con quái vật đã phá vòng vây.<br>Đôi mắt đỏ ngầu của nó đang nhắm vào... những dân làng co rúm sợ hãi.<br> ",
"Hí...!? Q-quái vật đang lao tới đây...!?<br> ",
"Chết tiệt...! Từ đây ta không kịp mất...!<br> ",
"(Nguy rồi...! Shiraes đang tập trung vào tinh thể...!<br>Dân làng đó...!)<br> ",
"Kíiiiiiii~~~~~~~!<br> ",
"Không‚ khôngggggggg...!!<br> ",
"Móng vuốt quái vật giáng xuống và máu bắn tung tóe.<br>Người dân làng bất lực đáng lẽ đã mặc nó xâu xé——nhưng không.<br> ",
"Ư...!? ............? H-hả...?<br>Sao mình... vẫn còn sống...? ...Gì cơ!?<br> ",
"A-anh... không sao chứ...?<br> ",
"——Thứ người dân làng nhìn thấy là Kureha‚ lấy chính thân mình<br>làm khiên để hứng móng vuốt quái vật.<br> ",
"Haaa!<br> ",
"Gyaaaa...!<br> ",
"C-cô... tại sao lại...?<br> ",
"Tại sao...? Hì hì‚ anh hỏi kỳ lạ thật đấy.<br>Bạn bè gặp nguy hiểm thì giúp là chuyện đương nhiên mà.<br> ",
"Bạn bè...? N-nhưng... chúng tôi thậm chí còn chưa từng tin<br>những điều các cô nói...! Sao cô lại làm đến mức đó...!<br> ",
"…Ngày xưa‚ từng có một người cứu tôi. Người ấy đã đứng lên<br>chống lại những kẻ làm tôi tổn thương dù chẳng có nghĩa vụ gì với tôi...<br> ",
"(Kureha…)<br> ",
"Vì vậy mọi người nghĩ gì về chúng tôi cũng không quan trọng.<br>Tôi... chúng tôi muốn bảo vệ mọi người!<br> ",
"Vì chúng tôi yêu con người! Đúng không nào!?<br> ",
"Ôôôôôôôôôôôôô!<br> ",
"Tiểu thư Kureha nói đúng! Anh em‚ dốc sức lên!<br>Mọi người có thể đang sợ‚ nhưng xin hãy cố chịu thêm một chút nữa!<br> ",
"Thấy chưa? Tất cả mọi người ở đây đều đang hết lòng muốn giúp mọi người.<br>Vì vậy... xin hãy để chúng tôi bảo vệ mọi người——!<br> ",
"Theo sau Tiểu thư Kureha——!<br> ",
"Dân làng lặng người nhìn Kureha lao trở lại<br>tiền tuyến.<br> ",
"(Hừ... Kureha lại lôi chuyện cũ ra nói.<br>Nhưng... xem ra cảm xúc của em ấy đã truyền tới họ rồi.)<br> ",
"Chúng ta... đã làm gì thế này...?<br> ",
"Rồi... một dân làng với tay lấy vũ khí từ kho dự bị.<br>Từng người rồi từng người khác cũng làm theo.<br> ",
"…Chúng ta cũng sẽ chiến đấu! Mọi người‚ cầm vũ khí lên!<br> ",
"Được! Chúng ta làm được... nhất định làm được! Ôôôôôôôôôôô!<br> ",
"Dân làng gom hết can đảm và gia nhập tiền tuyến. Quỷ tộc<br>tròn mắt nhìn con người chiến đấu kề vai sát cánh với họ.<br> ",
"N-này! Các người không cần phải làm vậy đâu!<br>Cứ giao nơi này cho bọn tôi rồi đến chỗ an toàn đi...!<br> ",
"Không‚ hãy để chúng tôi chiến đấu! Sức của chúng tôi có thể chẳng đáng là bao‚ nhưng...!<br> ",
"Để bạn bè chiến đấu một mình thì nhục đến tận đời con cháu!<br>Chúng tôi cũng muốn bảo vệ các cô!!<br> ",
"C-các người...!<br> ",
"Tấm lòng thẳng thắn và chân thành của Quỷ tộc cuối cùng cũng đã chạm tới họ——<br>Suy cho cùng‚ khác biệt giữa con người và Quỷ tộc chỉ là chuyện nhỏ...<br> ",
"Hỡi đồng bào! Con người đang chiến đấu cùng chúng ta!<br>Nếu không chứng tỏ khí phách lúc này thì còn gọi gì là Quỷ tộc!<br> ",
"Nào! Chỉ còn một chút nữa là hạ sạch lũ quái vật!<br>Đây chính là lúc phải gắng sức đấyyyy!!<br> ",
"Ôôôôôôôôôôôôô——!!<br> ",
"(...Nói thật thì bản thân sức chiến đấu của dân làng chẳng bổ sung được bao nhiêu.<br>Nhưng — một khi sĩ khí dâng cao‚ binh sĩ có thể hóa thành thứ hoàn toàn khác!)<br> ",
"Tốt lắm! Cứ tiếp tục cầm cự như thế!<br>Chỉ cần câu đủ thời gian‚ chắc chắn Shiraes sẽ——<br> ",
"——Để mọi người đợi lâu rồi.<br> ",
"Ngay lập tức‚ Shiraes giải phóng lượng ma lực khổng lồ đã tích tụ trong người.<br>Một luồng chớp nhuộm trắng bầu trời đêm và tiếng rít chói tai vang lên.<br> ",
"Tinh thể đã bị phá hủy. Sẽ không còn quân tiếp viện nữa.<br>Mọi người đã chiến đấu rất giỏi... ai cũng thật kiên cường. Tôi yêu mọi người.<br> ",
"Nào‚ quái vật chỉ còn lại vài con——cùng xốc lại tinh thần tiến lên chứ?<br>Trước hết... hãy thắp ngọn lửa phản công!<br> ",
"Kíyaaaaaa...!?<br> ",
"Đúng là Mẹ Shiraes!<br> ",
"Đại tỷ~~~~!<br> ",
"Được rồi! Lực lượng đã đủ! Sĩ khí cũng lên tới đỉnh!<br>Thế này thì chẳng có lý do gì để thua cả!<br> ",
"Đòn kết thúc đây! Vừa bảo vệ đồng đội bên cạnh vừa quét sạch chúng!<br>Toàn quân... tiến lên!!<br> ",
"Ôôôôôôô~~~!!!!<br> ",
]

assert len(TRANSLATIONS) == 90, len(TRANSLATIONS)

# Guard: no ASCII comma in translated fields
for idx, s in enumerate(TRANSLATIONS):
    if ',' in s:
        raise SystemExit(f'ASCII comma in translation {idx+1}: {s}')

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()

def split_text_record(line):
    head = line.split(',', 1)[0]
    if head == 'title':
        parts = line.split(',', 1)
        return head, parts, 1
    if head in ('message','messageTextUnder','messageTextCenter'):
        parts = line.split(',', 5)
        if len(parts) < 3:
            return head, parts, None
        return head, parts, 2
    return head, None, None

def text_field(line):
    head, parts, idx = split_text_record(line)
    if parts is None or idx is None or len(parts) <= idx: return None
    return parts[idx]

def tags(s): return re.findall(r'<[^>]+>', s or '')
def placeholders(s): return re.findall(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]', s or '')

def norm(s):
    return s.replace('，', ',').replace('\r','').strip()

raw = EN_ASSET.read_bytes()
bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig')
newline = '\r\n' if '\r\n' in text else '\n'
ends_newline = text.endswith('\n')
lines = text.splitlines()
orig_lines = lines[:]

candidates = []
for i,line in enumerate(lines):
    if line.startswith(tuple(t+',' for t in TEXT_TYPES)):
        candidates.append((i,line))

if len(candidates) != len(TRANSLATIONS):
    raise SystemExit(f'candidate count {len(candidates)} != translations {len(TRANSLATIONS)}')

entries = []
for n, ((line_idx,line), vi) in enumerate(zip(candidates, TRANSLATIONS), 1):
    head, parts, idx = split_text_record(line)
    old_text = parts[idx]
    parts[idx] = vi
    lines[line_idx] = ','.join(parts)
    entries.append({
        'seq': n, 'line': line_idx+1, 'record_type': head,
        'speaker': parts[1] if head != 'title' and len(parts)>1 else None,
        'source_text': old_text, 'vi_text': vi,
        'match_status': 'EXACT_OR_NORMALIZED',
        'translation_status': 'TRANSLATED'
    })

out_text = newline.join(lines) + (newline if ends_newline else '')
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
VI_ASSET.write_bytes((b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8'))

out_raw = VI_ASSET.read_bytes()
out_lines = out_raw.decode('utf-8-sig').splitlines()

blockers=[]; warnings=[]; kept=[]; delimiter_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; tech_mismatches=[]
for i,(a,b) in enumerate(zip(orig_lines,out_lines),1):
    if a.count(',') != b.count(','):
        delimiter_mismatches.append(i); blockers.append({'line':i,'type':'DELIMITER_COUNT_MISMATCH','source':a,'output':b})
    a_is = a.startswith(tuple(t+',' for t in TEXT_TYPES))
    if not a_is and a != b:
        tech_mismatches.append(i); blockers.append({'line':i,'type':'NON_TEXT_LINE_CHANGED','source':a,'output':b})
    if a_is:
        ah, ap, ai = split_text_record(a); bh, bp, bi = split_text_record(b)
        if ah != bh or ai != bi or len(ap) != len(bp):
            blockers.append({'line':i,'type':'FIELD_STRUCTURE_CHANGED','source':a,'output':b}); continue
        if ah == 'title':
            if ap[0] != bp[0]: blockers.append({'line':i,'type':'TITLE_TECH_CHANGED'})
        else:
            if [ap[0], ap[1]] + ap[3:] != [bp[0], bp[1]] + bp[3:]:
                blockers.append({'line':i,'type':'MESSAGE_TECH_FIELDS_CHANGED','source':a,'output':b})
        at, bt = text_field(a), text_field(b)
        if tags(at) != tags(bt):
            tag_mismatches.append(i); blockers.append({'line':i,'type':'TAG_MISMATCH','source_tags':tags(at),'output_tags':tags(bt)})
        if placeholders(at) != placeholders(bt):
            placeholder_mismatches.append(i); blockers.append({'line':i,'type':'PLACEHOLDER_MISMATCH','source_placeholders':placeholders(at),'output_placeholders':placeholders(bt)})
        if at == bt:
            kept.append(i); blockers.append({'line':i,'type':'UNCHANGED_TEXT_FIELD','text':bt})
        if ',' in bt:
            blockers.append({'line':i,'type':'ASCII_COMMA_IN_VI_FIELD','text':bt})

if len(orig_lines) != len(out_lines):
    blockers.append({'type':'LINE_COUNT_MISMATCH','source_lines':len(orig_lines),'output_lines':len(out_lines)})
if bom != out_raw.startswith(b'\xef\xbb\xbf'):
    blockers.append({'type':'BOM_CHANGED'})
if newline != ('\r\n' if '\r\n' in out_raw.decode('utf-8-sig') else '\n'):
    blockers.append({'type':'NEWLINE_CHANGED'})

# JSON pair reconciliation
ja_pairs = json.loads(JA_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)
en_pairs = json.loads(EN_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)
if len(ja_pairs) != len(en_pairs) or len(en_pairs) != len(candidates):
    warnings.append({'type':'NOVEL_ASSET_COUNT_RECONCILIATION','ja_pairs':len(ja_pairs),'en_pairs':len(en_pairs),'asset_candidates':len(candidates)})
for entry, jp_pair, en_pair in zip(entries, ja_pairs, en_pairs):
    entry['jp_source'] = jp_pair[0]
    entry['en_reference'] = en_pair[1]
    if norm(entry['source_text']) != norm(en_pair[1]):
        entry['match_status'] = 'CONTEXT_MATCH'

counts = {t:0 for t in TEXT_TYPES}
for _,line in candidates:
    counts[line.split(',',1)[0]] += 1

manifest = {
    'scene': SCENE,
    'status': 'PASS' if not blockers else 'FAIL',
    'source_asset': str(EN_ASSET),
    'output_asset': str(VI_ASSET),
    'ja_json': str(JA_JSON),
    'en_json': str(EN_JSON),
    'source_sha256': sha256_bytes(raw),
    'output_sha256': sha256_bytes(out_raw),
    'source_bytes': len(raw), 'output_bytes': len(out_raw),
    'bom_preserved': bom == out_raw.startswith(b'\xef\xbb\xbf'),
    'bom': 'utf-8-sig' if bom else 'utf-8',
    'newline': 'CRLF' if newline == '\r\n' else 'LF',
    'line_count_source': len(orig_lines), 'line_count_output': len(out_lines),
    'candidate_counts': counts,
    'translated_records': len(candidates),
    'kept_english_text_records': kept,
    'delimiter_mismatches': delimiter_mismatches,
    'tag_mismatches': tag_mismatches,
    'placeholder_mismatches': placeholder_mismatches,
    'technical_mismatches': tech_mismatches,
    'entries': entries,
}
qa = {
    'scene': SCENE,
    'qa_status': 'PASS' if not blockers else 'FAIL',
    'blockers': blockers,
    'warnings': warnings,
    'notes': [
        'JP source used as primary via ordered ja.json pairs; EN asset used for line/field alignment.',
        'All characters confirmed 18+ by project context; no H18 lines present in this file.',
        'Commander/司令官 translated as Chỉ Huy where applicable.',
        'ASCII commas inside VI fields are forbidden; Vietnamese separators use U+201A where needed.'
    ]
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

# focused diff only for translatable records
src_focus=[]; vi_focus=[]
for line_idx,_ in candidates:
    src_focus.append(f'{line_idx+1}: {orig_lines[line_idx]}\n')
    vi_focus.append(f'{line_idx+1}: {out_lines[line_idx]}\n')
diff = ''.join(difflib.unified_diff(src_focus, vi_focus, fromfile='EN translatable records', tofile='VI translatable records', lineterm='\n'))
(WORK/'focused_diff.md').write_text('```diff\n'+diff+'\n```\n', encoding='utf-8')
print(json.dumps({'status': manifest['status'], 'qa_status': qa['qa_status'], 'translated_records': len(candidates), 'blockers': len(blockers), 'output': str(VI_ASSET), 'work': str(WORK), 'output_sha256': manifest['output_sha256']}, ensure_ascii=False, indent=2))
