# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import json, hashlib, re, difflib
from collections import Counter

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10010100003'
JP_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/hmn_10010100003_full'
WORK.mkdir(parents=True, exist_ok=True)

# Ordered by asset candidate records: title, message, messageTextUnder, messageTextCenter.
VI = [
    "Đó Là Kỵ Sĩ Đạo Của Tôi!",
    "Trong phòng chỉ huy‚ %user% và Alicia đang xử lý giấy tờ‚<br>còn Rosa thì đứng dõi theo hai người.<br> ",
    "Đây là tài liệu tiếp theo‚ xin Chỉ Huy kiểm tra giúp!<br> ",
    "Ư… say rượu quá nên đầu óc anh chẳng xoay nổi…<br>Việc này nhất định phải làm trong hôm nay sao…?<br> ",
    "Không được đâu ạ! Đã biết trước rồi mà còn uống rượu thì lỗi là ở Chỉ Huy đấy!<br> ",
    "Anh không cưỡng lại được mà… Ôi‚ rắc rối thật…<br> ",
    "Nếu Chỉ Huy đang gặp khó khăn thì tôi sẽ ra sức giúp! Nhưng… có<br>việc gì tôi làm được không ạ…?<br> ",
    "Tất nhiên là có! Hãy ký tên anh vào tài liệu này giúp anh!<br> ",
    "Xin đừng làm giả chữ ký ạ!<br> ",
    "Rosa‚ tiếc là những việc này toàn là thứ chỉ Chỉ Huy mới có thể<br>xử lý…<br> ",
    "Vậy nếu có việc lặt vặt nào‚ xin cứ gọi tôi bất cứ lúc nào!<br> ",
    "Rosa‚ cô không cần phải cất công ở lại đâu. Dù sao lỗi cũng là của<br>Chỉ Huy mà.<br> ",
    "Nhưng chính tôi là người đã hộ tống Chỉ Huy đến quán rượu.<br> ",
    "Không ngờ việc tôi làm lại dẫn đến chuyện này… Tôi phải chịu<br>trách nhiệm vì đã khiến Chỉ Huy lâm vào cảnh khó xử.<br> ",
    "Em đâu có làm gì sai‚ không cần phải chịu trách nhiệm đâu.<br>Thật ra anh còn vui vì Rosa đã đi cùng anh mà.<br> ",
    "Điều đó… vâng‚ nghe được tấm lòng của Chỉ Huy‚ tôi cũng thấy rất vui.<br> ",
    "Tôi giúp những người gặp khó khăn vì muốn mang niềm vui đến cho mọi người.<br> ",
    "…Giúp người gặp khó khăn đúng là điều chính đáng trong kỵ sĩ đạo‚<br>nhưng anh thấy Rosa có niềm tin đặc biệt mạnh mẽ về chuyện đó.<br> ",
    "Vâng‚ kỵ sĩ đạo của tôi có lẽ khác với người khác.<br> ",
    "Tôi đã gây phiền phức cho Chỉ Huy rồi… Chỉ Huy có thể nghe tôi<br>kể một chút về bản thân không ạ?<br> ",
    "Ồ‚ anh hứng thú đấy. Kể cho anh nghe để anh tỉnh rượu nào.<br> ",
    "Thật là‚ nghe hời hợt như vậy thì thất lễ lắm đấy ạ?<br> ",
    "Không sao đâu. Vì đây là chuyện rất riêng tư mà.<br> ",
    "Hồi còn nhỏ‚ tôi sống trong một ngôi làng quê nhỏ. Dân làng<br>không phải người xấu‚ nhưng suy nghĩ có phần thiên lệch…<br> ",
    "Nhiều người cho rằng nữ kỵ sĩ hay nữ binh sĩ không đáng tin‚<br>và chỉ khi đàn ông chiến đấu mới đúng.<br> ",
    "Đó đúng là tập tục cổ hủ.<br>Dưới quyền anh có rất nhiều cô gái mạnh mẽ cơ mà.<br> ",
    "Chỉ Huy đã nhìn thấy tôi chiến đấu và lập tức công nhận tôi.<br>Tôi thật sự rất vui.<br> ",
    "…Rồi một ngày nọ‚ ngôi làng ấy bị một băng cướp tấn công.<br> ",
    "Tất cả đàn ông có thể chiến đấu đều bị đánh gục‚ và chúng tôi bị<br>đe dọa phải chuẩn bị thật nhiều vàng trước lần chúng quay lại.<br> ",
    "Thật quá đáng…<br>Mọi người vẫn ổn chứ?<br> ",
    "Vâng.<br>Tình cờ thay‚ có một nữ kỵ sĩ ghé qua ngôi làng.<br> ",
    "Giữa lúc nhiều dân làng nói rằng điều đó là không thể‚ cô ấy đã<br>đánh bại băng cướp một cách xuất sắc.<br> ",
    "Có người kinh ngạc đến mức còn không chịu tin.<br>Nhưng cô ấy thậm chí chẳng tỏ vẻ tức giận.<br> ",
    "Cô ấy chỉ nói: 'Giờ mọi người có thể yên tâm rồi. Tôi mừng vì đã<br>giúp được'‚ rồi rời đi.<br> ",
    "Tôi ngưỡng mộ dáng vẻ cao quý và đầy kiêu hãnh ấy‚ nên cũng nuôi<br>ước mơ trở thành kỵ sĩ.<br> ",
    "Vì vậy nếu có người gặp khó khăn‚ dù trong lòng họ thế nào‚ tôi<br>vẫn muốn giúp họ.<br> ",
    "Đó chính là kỵ sĩ đạo của tôi.<br> ",
    "Tôi muốn giúp người gặp khó khăn dù họ không mong muốn.<br>Tôi biết đó là một kỵ sĩ đạo có phần thiên lệch.<br> ",
    "Nhưng… tôi chưa từng nghĩ rằng sau khi được giúp‚ chính người đó<br>lại lâm vào khó khăn. Phải chăng tôi đã sai…?<br> ",
    "Vì cũng có những người xấu lợi dụng thiện ý‚ như một vị<br>Chỉ Huy nào đó chẳng hạn nhỉ～?<br> ",
    "Đừng nói như thể đã quyết định anh là kẻ xấu vậy.<br>Anh đâu có làm gì sai.<br> ",
    "Dù Chỉ Huy đã lừa Rosa giúp mình đi uống rượu ư?<br> ",
    "Kết quả là bây giờ anh và Rosa đang có thể nói thật lòng với nhau<br>đấy thôi? Chúng ta đã có quan hệ đáng tin cậy hơn trước khi đến quán rượu rồi mà.<br> ",
    "Vâng‚ tôi cũng nghĩ vậy. Tôi không ngờ mình lại kể hết mọi điều<br>với Chỉ Huy như thế này.<br> ",
    "A… chẳng lẽ nào! Chỉ Huy đã nhắm tới chuyện này ngay từ đầu sao!?<br> ",
    "Cuối cùng em cũng hiểu rồi à. Tất cả đều đúng như anh tính toán.<br> ",
    "Tuyệt quá…! Chỉ Huy đã nhìn thấu đến mức này cơ đấy!<br> ",
    "Đừng để bị lừa đấy‚ Rosa! Chỉ Huy chỉ đang nói bừa thôi!<br> ",
    "Ơ!? Thật vậy sao ạ!?<br> ",
    "Đúng là anh muốn trêu Rosa để kéo gần khoảng cách. Và anh cũng<br>thật sự muốn uống rượu.<br> ",
    "Cả hai đều là thật sao…?<br> ",
    "Có những kẻ xấu làm việc thiện‚ cũng có người tốt cuối cùng lại<br>gây ra điều xấu. Không thể dễ dàng phán xét con người tốt hay xấu đâu.<br> ",
    "Bởi một người lúc được em giúp là người tốt‚ sau đó cũng có thể<br>đổi lòng mà trở thành kẻ xấu.<br> ",
    "…Thật sự khó quá. Tôi không nghĩ mình có thể nhìn thấu được.<br> ",
    "Liệu tôi có thể tiếp tục giúp người khác như từ trước đến nay‚<br>theo kỵ sĩ đạo mà tôi tin tưởng không…?<br> ",
    "Rosa…<br> ",
    "Vậy để anh nhìn thấu thay em. Anh sẽ phán đoán xem người đó có<br>xứng đáng để Rosa giúp hay không.<br> ",
    "Chỉ Huy sẽ thay tôi…!?<br> ",
    "Mục tiêu của anh với tư cách Chỉ Huy tiền tuyến là cứu thế giới. Anh là người em tuyệt đối có thể tin tưởng‚ đúng không?<br> ",
    "Ra là vậy…! Chắc chắn rồi! Đúng là Chỉ Huy!<br> ",
    "Vậy từ nay tôi chỉ cần tin tưởng Chỉ Huy và chiến đấu vì ngài<br>đúng không ạ!<br> ",
    "Đúng vậy. Từ nay anh vẫn sẽ trông cậy vào em đấy‚ Rosa.<br> ",
    "Vâng‚ thưa Chỉ Huy!<br> ",
    "Được rồi‚ anh cũng tỉnh rượu hơn rồi‚ quay lại làm việc thôi.<br> ",
    "…Hửm‚ thùng rác đầy lên rồi nhỉ‚ hay là anh đi đổ rác một chuyến.<br> ",
    "Thật là‚ Chỉ Huy! Bình thường toàn bắt tôi làm‚ vậy mà chỉ lúc<br>thế này mới chịu xung phong! Hãy tập trung làm việc đi ạ!<br> ",
    "À! Đúng rồi… Rosa! Hình như Chỉ Huy đang gặp khó vì thùng rác<br>đầy rồi đấy nhỉ?<br> ",
    "Vâng‚ tôi sẽ giúp Chỉ Huy! Tôi sẽ đi đổ ngay đây!<br> ",
    "Ơ‚ ơ kìa!? Em không cần làm vậy đâu‚ anh sẽ tự đi mà!<br> ",
    "Không‚ nếu đó là mệnh lệnh chắc chắn giúp ích cho người khác thì<br>tôi rất hoan nghênh! Xin cứ giao cho tôi!<br> ",
    "Rosa lao ra khỏi phòng chỉ huy với khí thế khủng khiếp.<br> ",
    "…À‚ cửa sổ hơi bẩn rồi. Anh thấy để tâm quá‚ nên lau qua một chút<br>rồi hẵng làm việc…<br> ",
    "Rosa quay lại với tốc độ dữ dội‚<br>hai tay ôm đầy dụng cụ dọn dẹp.<br> ",
    "Tôi đã nghĩ có thể sẽ như vậy‚ nên mang dụng cụ tới rồi! Những<br>chỗ Chỉ Huy thấy để tâm cứ giao cho tôi‚ còn ngài xin hãy làm việc!<br> ",
    "À‚ hình như cũng đến lúc anh bắt đầu thấy hơi đói rồi nhỉ?<br> ",
    "Tôi đã đặt món ở nhà ăn rồi!<br>Lát nữa tôi sẽ đi lấy‚ nên xin đừng lo!<br> ",
    "…Được rồi‚ anh làm việc đây.<br>Thiệt tình‚ Rosa giỏi quá nên anh cũng khổ.<br> ",
    "Tôi lại khiến Chỉ Huy khó xử nữa sao?<br>Xin lỗi vì tôi là một kỵ sĩ còn thiếu sót.<br> ",
    "Thôi thì anh sẽ tha cho em vậy.<br>Từ nay cứ tiếp tục cố gắng vì anh nhé.<br> ",
    "Vâng‚ tôi nhất định sẽ trở thành trợ lực cho Chỉ Huy.<br>Đó chính là kỵ sĩ đạo của tôi!<br> ",
]

TEXT_RECS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}
TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r'(%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z0-9_]+\}|\$\{[A-Za-z0-9_]+\}|\\[nrt]|%%)')

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def props(p: Path):
    b = p.read_bytes()
    if b.startswith(b'\xef\xbb\xbf'):
        enc = 'utf-8-sig'; bom = True
    else:
        enc = 'utf-8'; bom = False
    nl = 'CRLF' if b.count(b'\r\n') else 'LF'
    text = b.decode(enc)
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'bom': bom, 'encoding': enc, 'newline': nl, 'line_count': len(text.splitlines()), 'trailing_newline': text.endswith(('\n','\r'))}

def load_pairs(p: Path):
    return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=list)

jp_pairs = load_pairs(JP_JSON)
en_pairs = load_pairs(EN_JSON)
source_props = {k: props(v) for k,v in {'ja_json': JP_JSON, 'en_json': EN_JSON, 'en_asset': EN_ASSET}.items()}
raw = EN_ASSET.read_bytes()
encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode(encoding)
lines = text.splitlines()
trailing = text.endswith(('\n','\r'))

candidates = []
for idx,line in enumerate(lines):
    rec = line.split(',',1)[0] if ',' in line else line
    if rec in TEXT_RECS and line.startswith(rec+','):
        parts = line.split(',')
        ti = TEXT_RECS[rec]
        if len(parts) <= ti:
            raise SystemExit(f'Malformed text record at line {idx+1}: {line}')
        candidates.append({'ordinal': len(candidates), 'line': idx+1, 'record': rec, 'speaker': '' if rec=='title' else parts[1], 'source_text': parts[ti], 'text_index': ti})

if len(VI) != len(candidates):
    raise SystemExit(f'VI count {len(VI)} != candidate count {len(candidates)}')

comma_errors = [i for i,s in enumerate(VI) if ',' in s]
if comma_errors:
    raise SystemExit(f'ASCII comma in VI strings: {comma_errors}')

new_lines = lines[:]
entries=[]
blockers=[]
for cand, vi in zip(candidates, VI):
    old = lines[cand['line']-1]
    parts = old.split(',')
    ti = cand['text_index']
    old_sig = parts[:ti] + parts[ti+1:]
    old_delims = old.count(',')
    parts[ti] = vi
    new = ','.join(parts)
    new_lines[cand['line']-1] = new
    new_parts = new.split(',')
    if new.count(',') != old_delims:
        blockers.append({'line': cand['line'], 'type':'DELIMITER_COUNT', 'old':old_delims, 'new':new.count(',')})
    if (new_parts[:ti] + new_parts[ti+1:]) != old_sig:
        blockers.append({'line': cand['line'], 'type':'TECH_FIELD_CHANGED'})
    if Counter(TAG_RE.findall(cand['source_text'])) != Counter(TAG_RE.findall(vi)):
        blockers.append({'line': cand['line'], 'type':'TAG_MISMATCH', 'source_tags':TAG_RE.findall(cand['source_text']), 'vi_tags':TAG_RE.findall(vi)})
    if Counter(PLACEHOLDER_RE.findall(cand['source_text'])) != Counter(PLACEHOLDER_RE.findall(vi)):
        blockers.append({'line': cand['line'], 'type':'PLACEHOLDER_MISMATCH', 'source_ph':PLACEHOLDER_RE.findall(cand['source_text']), 'vi_ph':PLACEHOLDER_RE.findall(vi)})
    status = 'TRANSLATED'
    kept_reason = None
    if vi.strip() == cand['source_text'].strip():
        status = 'UNCHANGED_REVIEW'
        kept_reason = 'identical_to_source_requires_review'
        blockers.append({'line': cand['line'], 'type':'UNCHANGED_EN_TEXT', 'text': vi})
    jp_source = jp_pairs[cand['ordinal']][0] if cand['ordinal'] < len(jp_pairs) else None
    en_ref = en_pairs[cand['ordinal']][1] if cand['ordinal'] < len(en_pairs) else None
    entries.append({**cand, 'jp_source': jp_source, 'en_json': en_ref, 'vi': vi, 'match_status': 'EXACT_ORDERED' if cand['ordinal'] < len(en_pairs) else 'ASSET_ONLY', 'translation_status': status, 'kept_reason': kept_reason})

out_text = newline.join(new_lines) + (newline if trailing else '')
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
VI_ASSET.write_bytes(out_text.encode(encoding))

# Independent-ish full file QA after writing
vi_raw = VI_ASSET.read_bytes(); vi_text = vi_raw.decode(encoding); vi_lines = vi_text.splitlines()
qa_blockers = blockers[:]
if len(vi_lines) != len(lines):
    qa_blockers.append({'type':'LINE_COUNT', 'source': len(lines), 'vi': len(vi_lines)})
if raw.startswith(b'\xef\xbb\xbf') != vi_raw.startswith(b'\xef\xbb\xbf'):
    qa_blockers.append({'type':'BOM_CHANGED'})
if (b'\r\n' in raw) != (b'\r\n' in vi_raw):
    qa_blockers.append({'type':'NEWLINE_STYLE_CHANGED'})
for i,(old,new) in enumerate(zip(lines,vi_lines),1):
    if old.count(',') != new.count(','):
        qa_blockers.append({'line': i, 'type':'DELIMITER_COUNT_FILE', 'old':old.count(','), 'new':new.count(',')})
    rec = old.split(',',1)[0] if ',' in old else old
    if rec in TEXT_RECS and old.startswith(rec+','):
        ti=TEXT_RECS[rec]
        op=old.split(','); np=new.split(',')
        if op[:ti]+op[ti+1:] != np[:ti]+np[ti+1:]:
            qa_blockers.append({'line': i, 'type':'TECH_FIELD_CHANGED_FILE'})

kept = []
for e in entries:
    vi_field = vi_lines[e['line']-1].split(',')[e['text_index']]
    if vi_field.strip() == e['source_text'].strip():
        kept.append({'line': e['line'], 'text': vi_field, 'reason': e.get('kept_reason')})

jp_leftover=[]
for e in entries:
    field=vi_lines[e['line']-1].split(',')[e['text_index']]
    if re.search(r'[\u3040-\u30ff\u3400-\u9fff]', field):
        jp_leftover.append({'line':e['line'],'text':field})
        qa_blockers.append({'line':e['line'],'type':'JP_LEFTOVER','text':field})

honorific_leftover=[]
for e in entries:
    field=vi_lines[e['line']-1].split(',')[e['text_index']]
    if re.search(r'-(san|sama|kun|chan)\b', field, re.I):
        honorific_leftover.append({'line':e['line'],'text':field})
        qa_blockers.append({'line':e['line'],'type':'HONORIFIC_LEFTOVER','text':field})

counts = Counter(e['record'] for e in entries)
qa_status = 'PASS' if not qa_blockers and not kept else 'FAIL'
# kept already creates blockers above, but keep explicit.
manifest = {
    'scene': SCENE,
    'status': qa_status,
    'source_props': source_props,
    'output_props': props(VI_ASSET),
    'candidate_text_records': len(candidates),
    'candidate_counts': dict(counts),
    'translated_records': sum(1 for e in entries if e['translation_status']=='TRANSLATED'),
    'jp_json_pairs': len(jp_pairs),
    'en_json_pairs': len(en_pairs),
    'entries': entries,
    'artifacts': {'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'script': str(WORK/'generate_vi.py'), 'output': str(VI_ASSET)},
}
qa_log = {
    'scene': SCENE,
    'qa_status': qa_status,
    'blockers': qa_blockers,
    'kept_english_records': kept,
    'intentional_unchanged_records': [],
    'jp_leftover': jp_leftover,
    'honorific_leftover': honorific_leftover,
    'checks': {
        'line_count_match': len(vi_lines)==len(lines),
        'bom_preserved': raw.startswith(b'\xef\xbb\xbf') == vi_raw.startswith(b'\xef\xbb\xbf'),
        'newline_preserved': (b'\r\n' in raw) == (b'\r\n' in vi_raw),
        'delimiter_mismatches': [b for b in qa_blockers if b.get('type') in ('DELIMITER_COUNT','DELIMITER_COUNT_FILE')],
        'technical_fields_unchanged': not any(b.get('type') in ('TECH_FIELD_CHANGED','TECH_FIELD_CHANGED_FILE') for b in qa_blockers),
        'tags_placeholders_preserved': not any(b.get('type') in ('TAG_MISMATCH','PLACEHOLDER_MISMATCH') for b in qa_blockers),
        'candidate_record_coverage': {'expected': len(candidates), 'vi_entries': len(VI), 'counts': dict(counts)},
        'no_unintentional_kept_english': not kept,
    },
    'notes': [
        'JP was used as primary source; EN asset/en.json used for ordered alignment.',
        'All characters are confirmed 18+ by project context; this file contained no explicit H18 scene.',
        'Speaker/technical asset fields and charaload names were preserved.',
        'ASCII comma was forbidden in VI text fields; U+201A was used where needed.',
    ],
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')
# focused diff only translatable lines
before=[]; after=[]
for e in entries:
    ln=e['line']
    before.append(f"{ln}:"+lines[ln-1])
    after.append(f"{ln}:"+vi_lines[ln-1])
diff = '\n'.join(difflib.unified_diff(before, after, fromfile='EN asset text records', tofile='VI asset text records', lineterm='')) + '\n'
(WORK/'focused_diff.md').write_text(diff, encoding='utf-8')
print(json.dumps({'qa_status': qa_status, 'blocker_count': len(qa_blockers), 'kept_english_count': len(kept), 'output': str(VI_ASSET), 'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'candidate_counts': dict(counts), 'output_sha256': props(VI_ASSET)['sha256']}, ensure_ascii=False, indent=2))
if qa_status != 'PASS':
    raise SystemExit(1)
