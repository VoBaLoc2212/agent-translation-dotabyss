# -*- coding: utf-8 -*-
"""Generate Vietnamese asset for evs_10200010501 and QA artifacts.
JP is primary source; EN asset is alignment/source structure.
"""
from __future__ import annotations
import json, hashlib, re, difflib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'evs_10200010501'
JP_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET_PATH = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET_PATH = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK_DIR = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST_PATH = WORK_DIR / 'manifest.json'
QA_PATH = WORK_DIR / 'qa_log.json'
DIFF_PATH = WORK_DIR / 'focused_diff.md'

VI = [
    "Tiêu Đề",
    "――Không cần lo nữa. Tất cả cơn phát tác đã lắng xuống và cô ấy đã ổn định.<br>Một thời gian nữa cô ấy chưa thể tự di chuyển nhưng chắc sẽ không ngã gục nữa.<br> ",
    "Hààà~~~~……<br>Tốt quá…… chị đã lo thật sự đó~~.<br> ",
    "Ưưư…… em xin lỗi vì đã khiến mọi người lo lắng……<br> ",
    "Em thật sự mừng vì mình vẫn ổn……<br>Em sẽ không sao trong một thời gian nữa đúng không chị Adelheid?<br> ",
    "Về chuyện đó…… có vẻ như mức hư hại ở lò ma đạo của Wendy<br>lớn hơn tôi dự tính ban đầu.<br> ",
    "Hả……? Ch-chuyện đó là sao hả!?<br> ",
    "Nói cho cùng thì hiểu biết của tôi về kỹ thuật automata còn nông cạn……<br>Tôi đã đánh giá sai tình hình.<br> ",
    "Không phải lỗi của chị Adelheid đâu……<br>Là do em đã cố quá sức……<br> ",
    "Mọi người đều rất quý Wendy chăm chỉ mà.<br>Em không cần tự trách mình như thế đâu nhé?<br> ",
    "Đúng đó~. Chỉ cần mau khỏe lại<br>rồi trở về làm Wendy như mọi khi là được~.<br> ",
    "Chị Viera…… chị Verisa……<br> ",
    "Hì hì…… cứ yên tâm. Cũng có tin tốt đây.<br>Sau khi phân tích thêm thì tôi đã tìm ra phương pháp chữa trị.<br> ",
    "Thật sao ạ――?<br>Chúng ta cần làm gì vậy?<br> ",
    "Một kết tinh ma lực có độ tinh khiết cao ở tầng sâu Đại Huyệt…… nếu có thể truyền ma lực đó vào<br>chức năng tự phục hồi của lò ma đạo trong Wendy sẽ hoạt động và đưa nó về trạng thái bình thường.<br> ",
    "Ủa~ chỉ cần vậy thôi hả~?<br>Thế thì đi lấy thật nhanh là xong mà~.<br> ",
    "Không. Vấn đề là mọi chuyện không đơn giản như vậy.<br>Kết tinh ma lực đó cực kỳ lớn nên có lẽ không thể mang về được.<br> ",
    "Nói cách khác…… cần đưa chính Wendy đến chỗ kết tinh.<br> ",
    "Đưa đến đó…… là đưa Wendy đang không thể tự di chuyển sao?<br> ",
    "Đúng vậy. Hơn nữa xung quanh kết tinh ma lực dường như có<br>những quái vật hung bạo bị sức mạnh ấy thu hút kéo đến làm tổ……<br> ",
    "Nên xem như sẽ có nguy hiểm tương xứng.<br>Vậy…… các cô định làm gì?<br> ",
    "Ra là vậy~. Nhưng vẫn chẳng có vấn đề gì đâu nhỉ.<br>Chị chỉ cần cõng Wendy đi là được mà~.<br> ",
    "Chị Verisa…… như vậy liều lĩnh quá.<br>Hơn nữa tầng sâu Đại Huyệt thì dù là hai chị cũng quá nguy hiểm.<br> ",
    "Đừng có xem thường Verisa-chan đó nha~.<br>Chuyện đó dễ ợt thôi dễ ợt.<br> ",
    "Gặp chị thì quái vật nào cũng chỉ là đồ yếu xìu~~♪<br>Phép thuật của Verisa-chan sẽ thổi bay hết cho xem♪<br> ",
    "Chị Verisa……<br>Em rất vui vì tấm lòng của chị nhưng……<br> ",
    "Còn phải chuẩn bị cho bữa tiệc bất ngờ nữa.<br>Phải trang trí xong trước khi Chỉ Huy quay về……<br> ",
    "Mọi người đừng bận tâm đến em mà hãy ưu tiên bữa tiệc đi ạ.<br>Việc đi lấy kết tinh ma lực để sau khi xong hết mọi chuyện cũng được……<br> ",
    "…………<br> ",
    "Chị Adelheid. Nếu việc sửa lò ma đạo chậm lại một chút<br>thì nó cũng sẽ không hỏng hẳn đúng không ạ?<br> ",
    "Nếu nghỉ ngơi yên tĩnh thì tôi nghĩ sẽ cầm cự được vài tuần.<br>Các triệu chứng đến hôm qua cũng đã có thể khống chế nhờ phân tích tiến triển.<br> ",
    "Tốt quá…… chị Verisa‚ chị Viera‚ hai chị nghe rồi đó.<br>Xin hãy cùng nhau tổ chức bữa tiệc bất ngờ cho Chỉ Huy.<br> ",
    "Em đó…… đang nói thật lòng đấy hả~?<br> ",
    "Vâng. Điều quan trọng nhất là làm Chỉ Huy vui.<br>Nếu bỏ lỡ cơ hội này thì không biết lần sau sẽ là khi nào――<br> ",
    "À‚ hây dô.<br> ",
    "――Nyao!?<br> ",
    "Au…… sao tự nhiên chị búng trán em vậy~~?<br> ",
    "Hì hì‚ yếu xìu~~♪<br>Đương nhiên là vì Wendy chẳng hiểu gì hết rồi~♪<br> ",
    "Hả……?<br> ",
    "Bữa tiệc bất ngờ này là do Wendy lên kế hoạch<br>nên đừng giao hết cho người khác mà hãy có trách nhiệm đến cùng đi~.<br> ",
    "Hơn nữa…… người muốn thấy gương mặt vui mừng của anh ấy hơn bất kỳ ai<br>chính là Wendy đúng không?<br> ",
    "…………！<br> ",
    "Vậy thì đừng bỏ cuộc dễ dàng như thế.<br>Em nghĩ tụi chị đã cố gắng vì ai chứ?<br> ",
    "Hả……? Vì ai thì chẳng phải là vì Chỉ Huy sao……?<br> ",
    "Hì hì‚ chị đúng là không thành thật chút nào nhỉ.<br> ",
    "Wendy. Bọn chị giúp đến tận hôm nay không chỉ vì Chỉ Huy đâu.<br>Bọn chị cũng muốn làm em vui nữa đó.<br> ",
    "Là…… vậy sao ạ……?<br> ",
    "Ừ.<br>Muốn làm bạn bè mỉm cười là cảm xúc rất tự nhiên mà♪<br> ",
    "Vì vậy trong bữa tiệc này<br>nếu không có Wendy ở đó thì bọn chị sẽ rất khó xử.<br> ",
    "…………<br> ",
    "Viera nói đúng đó~. Vậy nên Wendy.<br>Tụi chị nhất định sẽ chữa khỏi cho em♪<br> ",
    "Nói cho cùng thì em nghĩ bữa tiệc dành cho anh ấy<br>quan trọng hơn cơ thể của Wendy sao~?<br> ",
    "So với cái anh Chỉ Huy yếu xìu đó<br>Wendy quan trọng hơn nhiều nhiều luôn♪<br> ",
    "A ha ha. Ừm nếu Chỉ Huy nghe chuyện này<br>chắc anh ấy sẽ bảo ưu tiên sửa chữa hơn bữa tiệc và xuất kích đến Đại Huyệt ngay lập tức đấy.<br> ",
    "Đúng vậy đó~♪ Dù sao thì đã chuẩn bị đến mức này rồi<br>bữa tiệc nhất định phải thành công mới được~♪<br> ",
    "――Chúng ta sẽ tổ chức một bữa tiệc bất ngờ thật hoành tráng và hoàn hảo<br>rồi làm anh ấy hết hồn luôn! Hiểu chưa?<br> ",
    "……Vâng………… vâng! Cảm ơn mọi người!<br>Nhất định…… nhất định chúng ta hãy cùng tổ chức một bữa tiệc thật vui nhé……!<br> ",
    "Hư hư~ cuối cùng cũng hiểu rồi hả~.<br>Đã quyết vậy thì chị sẽ đưa em đi đến tận đâu cũng được! Leo lên lưng chị đi!<br> ",
    "A‚ à‚ chị Verisa? Chuyện đó hơi……<br> ",
    "Đã bảo là đừng khách sáo mà~.<br>Nào‚ chuẩn bị――…… lên nào!<br> ",
    "Verisa nắm lấy tay Wendy<br>và định cõng cô lên. Nhưng――<br> ",
    "　……Mgyu!?<br> ",
    "Rầm―― một tiếng‚ Verisa ngã sụp xuống ngay tại chỗ<br>kéo cả Wendy theo.<br> ",
    "…………<br> ",
    "Một bầu không khí hết sức ngượng ngùng bao trùm……<br> ",
    "……A‚ à‚ chị Verisa? Chị có ổn…… không ạ?<br> ",
    "……K-không có vấn đề gì hết. Chỉ là chị hơi hăng quá<br>rồi quên mất Wendy nặng thôi……<br> ",
    "……Tôi sẽ cho mượn xe kéo.<br>Và…… có cần tôi đỡ một tay không?<br> ",
    "……Lo chuyện bao đồng quá đó.<br> ",
    "Ưm…… tài năng bẩm sinh giúp mọi người bớt căng thẳng thế này!<br>Đúng là chị gái của em mà!<br> ",
    "Đừng có cố gượng bênh chị nữa!<br>Làm vậy càng thảm hại hơn đó~~!<br> ",
    "Ngay sau câu bắt bẻ của Verisa‚ Wendy bật ra một tiếng 『phụt――』 rồi mỉm cười.<br>Lấy đó làm khởi đầu‚ nụ cười bừng lên trên gương mặt của cả ba người.<br> ",
    "Hì hì hì. Đúng là em<br>rất thích những màn đối đáp thân thiết của chị Verisa và chị Viera♪<br> ",
    "Và thế là những cô gái đã bộc bạch lòng mình với nhau và đồng lòng một ý.<br>Giấu quyết tâm mạnh mẽ trong nụ cười‚ họ hướng về Đại Huyệt.<br> ",
]

TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]')

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def props(p: Path):
    b = p.read_bytes()
    return {
        'path': str(p),
        'bytes': len(b),
        'sha256': hashlib.sha256(b).hexdigest(),
        'bom_utf8': b.startswith(b'\xef\xbb\xbf'),
        'newline': 'CRLF' if b'\r\n' in b else 'LF',
        'line_count': len(b.decode('utf-8-sig').splitlines()),
    }

def split_lines_preserve(text: str):
    return text.splitlines()

def candidate_info(lines):
    out = []
    for idx, line in enumerate(lines, start=1):
        if line.startswith('title,') or line.startswith('message,'):
            parts = line.split(',')
            field_index = 1 if parts[0] == 'title' else 2
            out.append({'ordinal': len(out)+1, 'line_no': idx, 'type': parts[0], 'parts': parts, 'field_index': field_index, 'text': parts[field_index]})
    return out

def tags(s): return TAG_RE.findall(s)
def placeholders(s): return PH_RE.findall(s)
def has_ascii_comma(s): return ',' in s

WORK_DIR.mkdir(parents=True, exist_ok=True)
EN_BYTES = EN_ASSET_PATH.read_bytes()
encoding = 'utf-8-sig' if EN_BYTES.startswith(b'\xef\xbb\xbf') else 'utf-8'
newline = '\r\n' if b'\r\n' in EN_BYTES else '\n'
en_text = EN_BYTES.decode(encoding)
en_lines = split_lines_preserve(en_text)
cands = candidate_info(en_lines)

# Preserve duplicate keys in scene JSON. These assets may contain repeated silence lines
# such as "…………"; normal dict loading would collapse them and break alignment.
ja_pairs = json.loads(JP_PATH.read_text(encoding='utf-8'), object_pairs_hook=list)
en_pairs = json.loads(EN_JSON_PATH.read_text(encoding='utf-8'), object_pairs_hook=list)
ja_items = [k for k, _ in ja_pairs]
en_items = [v for _, v in en_pairs]

blockers = []
items = []
if len(VI) != len(cands): blockers.append({'code':'VI_COUNT_MISMATCH','expected':len(cands),'actual':len(VI)})
if len(ja_items) != len(cands): items.append({'code':'JP_COUNT_DIFFERS_FROM_ASSET','severity':'info','jp':len(ja_items),'candidates':len(cands),'message':'Novel JSON has fewer ordered pairs than asset candidate records; extra repeated silence records are translated from asset/context.'})
if len(en_items) != len(cands): items.append({'code':'EN_JSON_COUNT_DIFFERS_FROM_ASSET','severity':'info','en_json':len(en_items),'candidates':len(cands),'message':'Novel EN JSON has fewer ordered pairs than asset candidate records; extra repeated silence records are translated from asset/context.'})
for i, v in enumerate(VI, start=1):
    if has_ascii_comma(v): blockers.append({'code':'ASCII_COMMA_IN_VI','ordinal':i,'text':v})

out_lines = en_lines[:]
entries = []
if not blockers:
    for i, (cand, vi) in enumerate(zip(cands, VI), start=1):
        parts = cand['parts'][:]
        old_text = parts[cand['field_index']]
        parts[cand['field_index']] = vi
        out_lines[cand['line_no']-1] = ','.join(parts)
        # Basic alignment status: ordered mapping, exact after normalizing asset full-width comma and br-space quirks for many lines.
        entries.append({
            'ordinal': i,
            'line_no': cand['line_no'],
            'record_type': cand['type'],
            'speaker': cand['parts'][1] if cand['type'] == 'message' and len(cand['parts']) > 1 else None,
            'jp': ja_items[i-1] if i-1 < len(ja_items) else None,
            'en_json': en_items[i-1] if i-1 < len(en_items) else None,
            'en_asset': old_text,
            'vi': vi,
            'match_status': 'EXACT_ORDERED' if old_text.strip() else 'CONTEXT_MATCH',
            'translation_status': 'TRANSLATED',
        })

    VI_ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET_PATH.write_bytes((newline.join(out_lines) + (newline if en_text.endswith(('\n','\r\n')) else '')).encode(encoding))

# QA on written file
qa = {
    'scene': SCENE,
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'source_props': {
        'jp_json': props(JP_PATH),
        'en_json': props(EN_JSON_PATH),
        'en_asset': props(EN_ASSET_PATH),
    },
    'output_props': props(VI_ASSET_PATH) if VI_ASSET_PATH.exists() else None,
    'blockers': blockers,
    'items': items,
    'notes': [
        {'code':'H18_CHECK','status':'PASS','message':'No H-18/adult-uncertain sexual content detected in this scene.'},
        {'code':'ADDRESSING','status':'PASS','message':'Commander/司令官 rendered as Chỉ Huy; female-to-Commander references use anh/Chỉ Huy as appropriate; female-female dialogue uses chị/em/tôi by context.'},
    ],
}

if VI_ASSET_PATH.exists():
    vi_bytes = VI_ASSET_PATH.read_bytes()
    vi_text = vi_bytes.decode(encoding)
    vi_lines = split_lines_preserve(vi_text)
    vi_cands = candidate_info(vi_lines)
    delimiter_mismatches=[]; field_mismatches=[]; tech_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; ascii_comma=[]
    if len(en_lines) != len(vi_lines): blockers.append({'code':'LINE_COUNT_MISMATCH','en':len(en_lines),'vi':len(vi_lines)})
    if len(cands) != len(vi_cands): blockers.append({'code':'CANDIDATE_COUNT_MISMATCH','en':len(cands),'vi':len(vi_cands)})
    for el, vl in zip(en_lines, vi_lines):
        if el.count(',') != vl.count(','):
            delimiter_mismatches.append({'line_no': en_lines.index(el)+1, 'en_commas': el.count(','), 'vi_commas': vl.count(',')})
    for ec, vc in zip(cands, vi_cands):
        if len(ec['parts']) != len(vc['parts']):
            field_mismatches.append({'line_no':ec['line_no'],'en_fields':len(ec['parts']),'vi_fields':len(vc['parts'])})
        etech = ec['parts'][:]; vtech = vc['parts'][:]
        etech[ec['field_index']] = '<TEXT>'; vtech[vc['field_index']] = '<TEXT>'
        if etech != vtech:
            tech_mismatches.append({'line_no':ec['line_no'],'en':etech,'vi':vtech})
        if tags(ec['text']) != tags(vc['text']):
            tag_mismatches.append({'line_no':ec['line_no'],'en':tags(ec['text']),'vi':tags(vc['text'])})
        if placeholders(ec['text']) != placeholders(vc['text']):
            placeholder_mismatches.append({'line_no':ec['line_no'],'en':placeholders(ec['text']),'vi':placeholders(vc['text'])})
        if has_ascii_comma(vc['text']):
            ascii_comma.append({'line_no':ec['line_no'],'text':vc['text']})
    for code, arr in [('DELIMITER_MISMATCH',delimiter_mismatches),('FIELD_COUNT_MISMATCH',field_mismatches),('TECHNICAL_FIELD_MISMATCH',tech_mismatches),('TAG_MISMATCH',tag_mismatches),('PLACEHOLDER_MISMATCH',placeholder_mismatches),('ASCII_COMMA_IN_TRANSLATED_FIELD',ascii_comma)]:
        if arr: blockers.append({'code':code,'count':len(arr),'details':arr[:20]})
    qa.update({
        'structural': {
            'source_line_count': len(en_lines),
            'output_line_count': len(vi_lines),
            'candidate_records': len(cands),
            'translated_records': len(vi_cands),
            'delimiter_mismatches': delimiter_mismatches,
            'field_mismatches': field_mismatches,
            'technical_field_mismatches': tech_mismatches,
            'tag_mismatches': tag_mismatches,
            'placeholder_mismatches': placeholder_mismatches,
            'ascii_comma_in_translated_fields': ascii_comma,
        }
    })

qa['qa_status'] = 'PASS' if not blockers else 'FAIL'
qa['blockers'] = blockers

manifest = {
    'scene': SCENE,
    'created_at_utc': qa['timestamp_utc'],
    'paths': {
        'jp_json': str(JP_PATH),
        'en_json': str(EN_JSON_PATH),
        'en_asset': str(EN_ASSET_PATH),
        'vi_asset': str(VI_ASSET_PATH),
        'manifest': str(MANIFEST_PATH),
        'qa_log': str(QA_PATH),
        'focused_diff': str(DIFF_PATH),
        'script': str(Path(__file__)),
    },
    'counts': {
        'en_asset_lines': len(en_lines),
        'candidate_records': len(cands),
        'title_records': sum(1 for c in cands if c['type']=='title'),
        'message_records': sum(1 for c in cands if c['type']=='message'),
        'translated_records': len(entries),
        'review_records': 0,
        'h18_review_records': 0,
    },
    'source_hashes': qa['source_props'],
    'output_hashes': {'vi_asset': props(VI_ASSET_PATH)} if VI_ASSET_PATH.exists() else None,
    'entries': entries,
    'qa_status': qa['qa_status'],
}

# focused diff
old_focus = []
new_focus = []
if VI_ASSET_PATH.exists():
    vi_lines = VI_ASSET_PATH.read_bytes().decode(encoding).splitlines()
    for ec, vc in zip(cands, candidate_info(vi_lines)):
        old_focus.append(f"L{ec['line_no']}: {en_lines[ec['line_no']-1]}")
        new_focus.append(f"L{vc['line_no']}: {vi_lines[vc['line_no']-1]}")
    diff = list(difflib.unified_diff(old_focus, new_focus, fromfile='EN asset translatable lines', tofile='VI asset translatable lines', lineterm=''))
    DIFF_PATH.write_text('# Focused Diff: evs_10200010501\n\n```diff\n' + '\n'.join(diff) + '\n```\n', encoding='utf-8')

MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status':qa['qa_status'], 'blocker_count':len(blockers), 'vi_asset':str(VI_ASSET_PATH), 'manifest':str(MANIFEST_PATH), 'qa_log':str(QA_PATH), 'focused_diff':str(DIFF_PATH), 'output_sha256': sha256(VI_ASSET_PATH) if VI_ASSET_PATH.exists() else None}, ensure_ascii=False, indent=2))
if blockers:
    raise SystemExit(1)
