# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib
from collections import Counter

SCENE = 'hmn_10050100003'
ROOT = Path('E:/AgentTranslation')
JA_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET_PATH = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET_PATH = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK_DIR = ROOT / 'dotabyss-rpg-vn-translator/work/hmn_10050100003_full'
MANIFEST_PATH = WORK_DIR / 'manifest.json'
QA_PATH = WORK_DIR / 'qa_log.json'
DIFF_PATH = WORK_DIR / 'focused_diff.md'
TEXT_TYPES = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

VI_TRANSLATIONS = [
    'Tiêu Đề',
    '<size=48>――Vài Ngày Sau</size>',
    'Khụ khụ khụ!<br>…Xem ra mình bị cảm thật rồi.<br> ',
    'Chủ nhân‚ ngài thật sự không sao chứ?<br>Trông ngài rất khổ sở…<br> ',
    'Ta đã nằm liệt giường khoảng hai ngày rồi.<br>Nhưng chỉ là cảm lạnh thôi. Chẳng mấy chốc sẽ khá hơn.<br> ',
    'Khăn lau mồ hôi‚ túi chườm đá‚ cả gối đùi――<br>tất cả đã chuẩn bị xong. Xin cứ sai bảo bất cứ điều gì ngài cần.<br> ',
    'Còn chuẩn bị đọc tiểu thuyết khiêu gợi thì sao?<br> ',
    'Hoàn hảo ạ.<br>…Nhưng nếu ngài chưa khá hơn một chút thì thần không thể khuyến nghị――<br> ',
    'Ta biết mà.<br>…Nếu được chăm sóc chu đáo thế này thì thỉnh thoảng bị cảm cũng không tệ.<br> ',
    'Đúng vậy. Nếu không có lúc như thế này<br>chủ nhân hiếm khi chịu nghỉ ngơi.<br> ',
    'À… khụ.<br> ',
    '…? Chủ nhân?<br>Sắc mặt ngài không được ổn――<br> ',
    '…!? Chủ nhân!? Ngài sốt cao quá đấy!?<br>Rốt cuộc từ lúc nào mà!?<br> ',
    '…Ta cũng nghĩ từ nãy đến giờ người chẳng có sức<br>quả nhiên là vậy.<br> ',
    'Thần sẽ mang thuốc tới. Bữa ăn cũng sẽ đổi sang món có tác dụng<br>hạ sốt. Thần chuẩn bị ngay đây‚ xin ngài hãy nghỉ ngơi.<br> ',
    '――Cạch!<br> ',
    'C-Chỉ Huy! Nguy rồi! Một bầy quái vật đã xuất hiện trong Đại Hố!<br>Đội khảo sát đang gặp nguy hiểm!<br> ',
    'Khốn… đúng lúc này…<br> ',
    '…Hiểu rồi. Ta sẽ đi ngay.<br> ',
    'Không được đâu‚ thưa chủ nhân.<br>Ngài đâu đang trong tình trạng có thể chỉ huy?<br> ',
    'Ơ!? V-vậy sao ạ!?<br> ',
    'Đừng nói nhảm. Chỉ cỡ này thì chẳng――khụ!<br> ',
    'Ngay khoảnh khắc %user% định rời khỏi giường để đứng dậy<br>anh loạng choạng dữ dội.<br> ',
    'Như cô thấy đấy‚ cô Alicia.<br>Ngài ấy sốt cao đến mức không thể cử động được.<br> ',
    'Tôi hiểu rồi. Chỉ Huy‚ chúng tôi sẽ xoay xở. Xin ngài hãy nghỉ ngơi.<br> ',
    'Không được! Ta là Chỉ Huy đấy! Đồng đội đang lâm nguy mà sao ta có thể nằm yên!<br>Ta sẽ chỉ huy đội cứu viện!<br> ',
    'N-nhưng… ngài nên nghỉ thì hơn…<br> ',
    'Đừng hoảng. Electra‚ mau mang đồ thay cho ta.<br> ',
    '…<br> ',
    '…Chủ nhân‚ thần vô cùng xin lỗi. Xin thất lễ.<br> ',
    'Này‚ cô làm gì vậy!?<br> ',
    'Electra đè %user% xuống giường<br>rồi nhanh chóng trói anh lại bằng dây thừng.<br> ',
    'Electra‚ cởi dây ra! Đây là chống lệnh đấy!<br> ',
    '…Thần biết. Nhưng để bảo vệ sức khỏe của chủ nhân<br>thần phán đoán đây là cách tốt nhất.<br> ',
    'Cô Alicia‚ thần xin được kiến nghị. Chủ nhân đang không khỏe.<br>Xin hãy ra lệnh cho Electra thay ngài ấy cứu đội khảo sát.<br> ',
    'Đừng tự ý quyết định!<br>Trong căn cứ này không ai có thể thay thế ta!<br> ',
    'Thần hiểu. Electra không thể nào thay thế chủ nhân.<br>Dù vậy‚ thần vẫn muốn trở thành sức mạnh của ngài.<br> ',
    'Nguy hiểm cũng đã nằm trong dự tính. Dẫu vậy‚ xin hãy để thần đi.<br>Thần nhất định sẽ bảo vệ đội khảo sát.<br> ',
    '(…Phải. Cho dù Electra có phải hy sinh.)<br> ',
    'Electra. Cô đang nghĩ gì vậy?<br> ',
    'Thần đang dự đoán suy nghĩ của chủ nhân. Một chủ nhân sáng suốt như ngài hẳn đã nhìn ra rằng<br>ra lệnh cho Electra sẽ có tỷ lệ thành công cao hơn tự mình đi trong tình trạng hiện tại.<br> ',
    'Ư…<br> ',
    'Chủ nhân‚ xin hãy ban lệnh――<br> ',
    '…<br> ',
    'Chủ nhân?<br> ',
    '…Ngài ấy ngủ rồi. Tôi nghĩ ngài ấy đã tới giới hạn.<br>Vậy mà trong tình trạng này ngài ấy còn định ra tiền tuyến…<br> ',
    'Electra. Đây là lời thỉnh cầu của tôi. Xin hãy xuất kích thay Chỉ Huy!<br>Tôi cũng sẽ hỗ trợ!<br> ',
    'Xin nhờ cô.<br> ',
    '…Chủ nhân. Về việc chống lệnh‚ thần sẽ chấp nhận bất kỳ hình phạt nào.<br> ',
    '(Nhưng trước hết‚ phải cứu đội khảo sát――<br>và đem chiến thắng về cho đơn vị của chủ nhân!)<br> ',
    '<size=48>――Vài Giờ Sau</size>',
    'Electra cùng đơn vị do cô chỉ huy đã có mặt trong Đại Hố.<br> ',
    'Tìm thấy rồi! Đội khảo sát kìa!<br>Họ đang bị quái vật bao vây!<br> ',
    'Electra sẽ mở đường!<br>Đã bắt mục tiêu! Bắt đầu tấn công!<br> ',
    'Electra nã đạn vào bầy quái vật đang tạo thành vòng vây.<br>Những con quái vật trúng đạn gào thét rồi ngã gục.<br> ',
    'Tuyệt quá…<br>Cô ấy mở được đường rút chỉ trong chớp mắt!?<br> ',
    'Hãy khẩn trương cứu người!<br>Không thể ở lâu khi Chỉ Huy vắng mặt!<br> ',
    'Electra xông vào trong vòng vây――<br>và dẫn các thành viên đội khảo sát cần cứu hộ ra tuyến rút lui đã được bảo đảm.',
    'Electra‚ nguy hiểm!<br>Phía sau!<br> ',
    'Đã bắt được mục tiêu!<br> ',
    'Kíí!?<br> ',
    '――Bịch.<br> ',
    'Nào‚ hãy đi đi! Electra sẽ chặn địch ở cuối đội hình!<br> ',
    'Electra đảm nhiệm vai trò đoạn hậu và tiếp tục hạ gục quái vật. Trong lúc đó‚ đội cứu viện lại bị chặn bước tiến.',
    'K-không ổn rồi‚ Electra!<br>Phía đầu đội đang bị một con quái vật khổng lồ tấn công nên không thể tiến lên!<br> ',
    'Electra nheo mắt nhìn về phía xa.<br> ',
    'Phát hiện bóng địch. Cự ly 120… khai hỏa!<br> ',
    'Viên đạn Electra bắn ra trúng vào đầu con quái vật đang nổi loạn ở phía xa.<br>Bị bắn xuyên điểm yếu‚ nó mất sức và đổ gục ngay tại chỗ.<br> ',
    'K-kinh thật… bắn trúng một con ở xa đến vậy!<br> ',
    'Hãy truyền lời bảo họ nhanh lên!<br>Số lượng địch quá đông! Không cầm cự được lâu đâu!<br> ',
    'Gàooooo!!<br> ',
    'Khụ…<br> ',
    'Tiếp tục… tấn công!<br> ',
    'Electra đẩy lùi quái vật và tiếp tục làm ngọn giáo cùng tấm khiên của mọi người. Vượt qua hết trận tử chiến này đến trận tử chiến khác‚ đội khảo sát cuối cùng cũng được cứu――',
    '<size=48>――Vài Ngày Sau</size>',
    'Chủ nhân. Tình trạng sức khỏe của ngài thế nào rồi?<br> ',
    'Hoàn toàn ổn rồi. Ta đã bị trói trên giường suốt mấy ngày mà.<br>Đến cả ta cũng chỉ còn cách ngủ thôi.<br> ',
    '…Chủ nhân đang giận Electra‚ đúng không ạ?<br> ',
    'Đương nhiên. Ta không thể bỏ qua chuyện chống lệnh.<br> ',
    'Vâng. Thần sẽ chấp nhận bất kỳ hình phạt nào.<br> ',
    '(Cho dù đó là bị tiêu hủy đi nữa――)<br> ',
    'Được. Vậy ta sẽ tuyên án phạt.<br> ',
    'Hình phạt là búng tay vào cổ tay và búng trán.<br> ',
    '…Ơ?<br> ',
    'Không phục à?<br> ',
    'À‚ không――chỉ là‚ thưa chủ nhân. Hình phạt đó là thứ bình thường đối với ngài sao?<br> ',
    'Làm gì có chuyện một hình phạt đùa cợt như thế lại bình thường.<br> ',
    '…Nghe tin Electra có thể bị phạt vì chống lệnh<br>đội khảo sát và đội cứu viện đã gửi đơn thỉnh cầu xin ta tha thứ cho cô.<br> ',
    'Tuy nhiên‚ nếu bỏ qua chuyện chống lệnh thì sau này sẽ ảnh hưởng tới quyền chỉ huy.<br>Không thể xóa bỏ hình phạt nên mới thành ra thế này.<br> ',
    '…Ý ngài là ngài sẽ tha thứ cho Electra ạ?<br> ',
    'Ừ thì. Dù bây giờ nghĩ lại ta vẫn hơi bực<br>nhưng cô đã làm theo lệnh của ta‚ đúng không?<br> ',
    'Khi lệnh của ta và Alicia xung đột<br>ta đã nói hãy làm điều cô muốn làm.<br> ',
    'Ở tình huống đó cô phán đoán trói ta vào giường là phương án tốt nhất.<br>Đúng vậy chứ?<br> ',
    'Vâng. Quá trình dẫn đến phán đoán đó không hề sai lệch.<br> ',
    'Vậy thì không cần nghiêm phạt. Búng tay vào cổ tay và búng trán<br>là thỏa đáng rồi nhỉ?<br> ',
    'Việc cô làm theo mệnh lệnh "hãy làm điều cô muốn"<br>ta đánh giá rất cao. Cô làm tốt lắm.<br> ',
    '…! Ngài sẽ khen thần sao?<br> ',
    'Ừ. Có cô ở bên khiến ta rất yên tâm. Từ giờ cũng nhờ cô tiếp tục như vậy.<br> ',
    '…Tức là ngài vẫn sẽ tiếp tục tôn trọng phán đoán của Electra?<br> ',
    'À‚ nhưng không có nghĩa là ta cho phép cô lại trói ta vào giường đâu nhé?<br> ',
    '…<br> ',
    'Sao lại đứng hình vậy? Lại là vấn đề khung gì đó à?<br> ',
    'Không‚ không phải ạ.<br> ',
    'Vậy là cô đang cảm động trước lòng khoan dung của ta sao?<br> ',
    'Cũng không phải vậy‚ thưa chủ nhân.<br>Electra không có cảm xúc. Cũng không có trái tim.<br> ',
    'Thứ tồn tại bên trong Electra là chương trình tư duy dùng để kiểm chứng và phán đoán<br>điều gì là tốt nhất cho chủ nhân và điều gì là đúng đắn.<br> ',
    'Chương trình đó vừa đưa ra câu trả lời.<br>Rằng Electra đang được ở bên cạnh người đúng đắn mà mình nên phụng sự.<br> ',
    'Chừng nào ngài còn mong muốn‚ Electra sẽ tiếp tục phụng sự bên cạnh ngài.<br>Electra sẽ tiếp tục tồn tại để có ích cho ngài.<br> ',
    '…Nếu chỉ nghe lời cô nói<br>thì nghe kiểu gì cũng giống như cô đang cảm kích và hạnh phúc ấy nhỉ.<br> ',
    'Nói như vậy sẽ khiến chủ nhân thấy vui hơn sao?<br> ',
    'Tất nhiên rồi. Đó là vinh dự lớn nhất của một Chỉ Huy.<br>Cả với tư cách đàn ông nữa.<br> ',
    'Vậy thần xin nói lại.<br> ',
    'Electra rất hạnh phúc khi được phụng sự chủ nhân.<br> ',
    'Ha ha. Quả nhiên nói vậy nghe hay hơn.<br> ',
]

assert len(VI_TRANSLATIONS) == 114, len(VI_TRANSLATIONS)

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def detect_newline(b: bytes):
    crlf = b.count(b'\r\n')
    lf = b.count(b'\n')
    return 'CRLF' if crlf == lf and lf else 'LF' if lf else 'NONE'

def get_text_index(parts):
    typ = parts[0]
    if typ == 'title': return 1
    if typ in ('message', 'messageTextUnder', 'messageTextCenter'): return 2
    return None

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%user%|<user>|%s|%d|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%', s)

def text_records(lines):
    out=[]
    for idx,line in enumerate(lines):
        body=line.rstrip('\r\n')
        if not body:
            continue
        typ=body.split(',',1)[0]
        if typ in TEXT_TYPES:
            parts=body.split(',')
            ti=get_text_index(parts)
            out.append({'seq': len(out)+1, 'line_no': idx+1, 'type': typ, 'parts': parts, 'text_idx': ti, 'text': parts[ti]})
    return out

def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    src_b = EN_ASSET_PATH.read_bytes()
    encoding = 'utf-8-sig' if src_b.startswith(b'\xef\xbb\xbf') else 'utf-8'
    newline = detect_newline(src_b)
    src_text = src_b.decode(encoding)
    lines = src_text.splitlines(keepends=True)
    recs = text_records(lines)
    blockers=[]; items=[]; kept=[]
    if len(recs) != len(VI_TRANSLATIONS):
        blockers.append({'code':'COUNT_MISMATCH','source_candidates':len(recs),'vi_entries':len(VI_TRANSLATIONS)})
    new_lines = list(lines)
    entries=[]
    for rec, vi in zip(recs, VI_TRANSLATIONS):
        if ',' in vi:
            blockers.append({'code':'ASCII_COMMA_IN_VI','seq':rec['seq'],'line':rec['line_no'],'text':vi})
        body = lines[rec['line_no']-1].rstrip('\r\n')
        ending = lines[rec['line_no']-1][len(body):]
        parts = body.split(',')
        ti = rec['text_idx']
        before_sig = parts[:ti] + parts[ti+1:]
        parts[ti] = vi
        new_body = ','.join(parts)
        new_lines[rec['line_no']-1] = new_body + ending
        entries.append({
            'seq': rec['seq'], 'line_no': rec['line_no'], 'type': rec['type'],
            'speaker': rec['parts'][1] if rec['type'] != 'title' else None,
            'en_text': rec['text'], 'vi_text': vi,
            'match_status': 'CONTEXT_MATCH' if rec['seq'] in {58,64,74} else 'EXACT',
            'translation_status': 'TRANSLATED',
            'technical_signature': before_sig,
        })
        if vi == rec['text']:
            kept.append({'seq':rec['seq'],'line':rec['line_no'],'text':vi,'reason':'identical punctuation/proper-name only if reviewed'})
    out_text=''.join(new_lines)
    VI_ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET_PATH.write_bytes((b'\xef\xbb\xbf' if encoding == 'utf-8-sig' else b'') + out_text.encode('utf-8'))
    out_b = VI_ASSET_PATH.read_bytes()
    out_dec = out_b.decode(encoding)
    out_lines = out_dec.splitlines(keepends=True)
    out_recs = text_records(out_lines)
    # independent structural QA
    delimiter_mismatches=[]; technical_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; comma_violations=[]; unchanged=[]
    if len(lines) != len(out_lines):
        blockers.append({'code':'LINE_COUNT_MISMATCH','en_lines':len(lines),'vi_lines':len(out_lines)})
    if detect_newline(out_b) != newline:
        blockers.append({'code':'NEWLINE_MISMATCH','en_newline':newline,'vi_newline':detect_newline(out_b)})
    if out_b.startswith(b'\xef\xbb\xbf') != src_b.startswith(b'\xef\xbb\xbf'):
        blockers.append({'code':'BOM_MISMATCH'})
    if len(out_recs) != len(recs):
        blockers.append({'code':'TEXT_RECORD_COUNT_MISMATCH','en':len(recs),'vi':len(out_recs)})
    for i,(a,b) in enumerate(zip(lines,out_lines),1):
        if a.count(',') != b.count(','):
            delimiter_mismatches.append({'line':i,'en_commas':a.count(','),'vi_commas':b.count(',')})
    for en_rec, vi_rec in zip(recs, out_recs):
        ti=en_rec['text_idx']
        en_parts=en_rec['parts']; vi_parts=vi_rec['parts']
        if en_parts[:ti] + en_parts[ti+1:] != vi_parts[:ti] + vi_parts[ti+1:]:
            technical_mismatches.append({'seq':en_rec['seq'],'line':en_rec['line_no']})
        if tags(en_rec['text']) != tags(vi_rec['text']):
            tag_mismatches.append({'seq':en_rec['seq'],'line':en_rec['line_no'],'en_tags':tags(en_rec['text']),'vi_tags':tags(vi_rec['text'])})
        if placeholders(en_rec['text']) != placeholders(vi_rec['text']):
            placeholder_mismatches.append({'seq':en_rec['seq'],'line':en_rec['line_no'],'en_ph':placeholders(en_rec['text']),'vi_ph':placeholders(vi_rec['text'])})
        if ',' in vi_rec['text']:
            comma_violations.append({'seq':en_rec['seq'],'line':en_rec['line_no'],'text':vi_rec['text']})
        if vi_rec['text'] == en_rec['text']:
            unchanged.append({'seq':en_rec['seq'],'line':en_rec['line_no'],'text':vi_rec['text']})
    for name,lst in [('DELIMITER_MISMATCH',delimiter_mismatches),('TECHNICAL_FIELD_MISMATCH',technical_mismatches),('TAG_MISMATCH',tag_mismatches),('PLACEHOLDER_MISMATCH',placeholder_mismatches),('ASCII_COMMA_IN_TRANSLATED_FIELD',comma_violations),('UNCHANGED_EN_TEXT',unchanged)]:
        if lst:
            blockers.append({'code':name,'items':lst[:20],'count':len(lst)})
    suspicious_patterns = [r'\bMaster\b', r'\bCommander\b', r'\bSurvey Team\b', r'\bAbyss\b', r'\bElectra is very happy\b', r'\bPlease\b', r'\bWhat\b', r'\bYes\b', r'\bNo\b', r'\bUgh\b', r'\bNgh\b']
    leftovers=[]
    for rec in out_recs:
        for pat in suspicious_patterns:
            if re.search(pat, rec['text']):
                # Allow proper names Electra/Alicia only; targeted terms above should be translated.
                leftovers.append({'seq':rec['seq'],'line':rec['line_no'],'pattern':pat,'text':rec['text']})
    if leftovers:
        blockers.append({'code':'TARGETED_EN_LEFTOVER','count':len(leftovers),'items':leftovers[:20]})
    # focused diff
    before=[]; after=[]
    for rec in recs:
        before.append(f"L{rec['line_no']:04d} {lines[rec['line_no']-1].rstrip()}\n")
    for rec in out_recs:
        after.append(f"L{rec['line_no']:04d} {out_lines[rec['line_no']-1].rstrip()}\n")
    diff=''.join(difflib.unified_diff(before, after, fromfile='EN asset text records', tofile='VI asset text records', lineterm=''))
    DIFF_PATH.write_text(diff, encoding='utf-8')
    counts = Counter(r['type'] for r in entries)
    qa_status = 'PASS' if not blockers else 'FAIL'
    qa = {
        'scene': SCENE,
        'qa_status': qa_status,
        'blockers': blockers,
        'items': items,
        'notes': [
            'JP is primary source; EN asset used for exact ordered field replacement.',
            'All Dot Abyss characters in this project confirmed 18+ by user; no H18 blocker encountered in this file.',
            'Names in technical speaker/charaload fields were preserved; in prose Electra/Alicia kept per EN mapping.',
            'Commander/司令官 translated as Chỉ Huy; ご主人様 translated as chủ nhân for Electra master-servant voice.',
            'ASCII comma inside Vietnamese text fields forbidden; Vietnamese internal commas use U+201A if needed.'
        ],
        'kept_en_records': kept,
        'independent_verify': {
            'line_count_match': len(lines) == len(out_lines),
            'bom_preserved': out_b.startswith(b'\xef\xbb\xbf') == src_b.startswith(b'\xef\xbb\xbf'),
            'newline_preserved': detect_newline(out_b) == newline,
            'candidate_counts': dict(Counter(x['type'] for x in out_recs)),
            'candidate_total': len(out_recs),
            'translated_records': len(out_recs) - len(unchanged),
            'delimiter_mismatches': delimiter_mismatches,
            'technical_mismatches': technical_mismatches,
            'tag_mismatches': tag_mismatches,
            'placeholder_mismatches': placeholder_mismatches,
            'ascii_comma_violations': comma_violations,
            'unchanged_en_records': unchanged,
            'targeted_en_leftovers': leftovers,
        }
    }
    QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    manifest = {
        'scene': SCENE,
        'status': qa_status,
        'source_paths': {'ja_json': str(JA_PATH), 'en_json': str(EN_JSON_PATH), 'en_asset': str(EN_ASSET_PATH)},
        'output_path': str(VI_ASSET_PATH),
        'artifact_paths': {'manifest': str(MANIFEST_PATH), 'qa_log': str(QA_PATH), 'focused_diff': str(DIFF_PATH), 'script': str(WORK_DIR / 'generate_vi.py')},
        'source': {'sha256': sha256(src_b), 'bytes': len(src_b), 'bom': src_b.startswith(b'\xef\xbb\xbf'), 'newline': newline, 'line_count': len(lines), 'candidate_counts': dict(Counter(x['type'] for x in recs)), 'candidate_total': len(recs)},
        'output': {'sha256': sha256(out_b), 'bytes': len(out_b), 'bom': out_b.startswith(b'\xef\xbb\xbf'), 'newline': detect_newline(out_b), 'line_count': len(out_lines), 'candidate_counts': dict(Counter(x['type'] for x in out_recs)), 'candidate_total': len(out_recs)},
        'entries': entries,
        'qa_summary': {'qa_status': qa_status, 'blocker_count': len(blockers), 'translated_records': len(out_recs) - len(unchanged), 'kept_en_records': len(unchanged)}
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest['qa_summary'], ensure_ascii=False))

if __name__ == '__main__':
    main()
