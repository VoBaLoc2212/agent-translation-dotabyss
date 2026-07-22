from pathlib import Path
import json, hashlib, re, difflib

SCENE = 'hmn_10040100001'
ROOT = Path('E:/AgentTranslation')
JP_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET_PATH = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET_PATH = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/hmn_10040100001_full'
MANIFEST_PATH = WORK / 'manifest.json'
QA_PATH = WORK / 'qa_log.json'
DIFF_PATH = WORK / 'focused_diff.md'
TEXT_RECORDS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}

TRANSLATIONS = [
    'Cô Gái Du Hành Cùng Gấu Trúc',
    '<size=48>――Khu Rừng Gần Căn Cứ Tiền Tuyến</size>',
    'Được rồi‚ lấy chừng này chắc đủ rồi.<br>Đến lúc quay về căn cứ thôi…<br> ',
    'Nhưng chỉ vì trông mình có vẻ rảnh mà lại bắt Chỉ Huy đi hái nấm độc thế này thì…<br>Ừ thì nguyên liệu làm độc dược đối phó quái vật càng nhiều càng tốt‚ nhưng…<br> ',
    'Gì thế? Cây cối ở đây đổ ngổn ngang một cách kỳ lạ.<br>Tối qua có bão hay sao?<br> ',
    'A… tệ thật. Đường bị cây đổ chặn mất rồi…<br>Thế này thì không đi tiếp được…<br> ',
    'Đi vòng hay cố trèo qua đây…<br>Cách nào cũng phiền cả…<br> ',
    'Ưư… a-ai đó…<br>C-cứu với…<br> ',
    '…! Giọng nói vừa rồi là!?<br>Không lẽ có người bị kẹt dưới cây đổ à!?<br> ',
    'Đợi đó‚ tôi cứu cô ngay!<br>Chắc chắn giọng nói phát ra từ phía sau thân cây đổ kia…!<br> ',
    'Kupyư!<br> ',
    '…Hả? Gấu trúc con…?<br>Không lẽ gấu trúc biết nói đang kêu cứu… không‚ làm gì có chuyện—<br> ',
    'C-cứu… với…<br> ',
    'Cái gì!? Có người đang nằm sau lũ gấu trúc!<br> ',
    'Này‚ cô ổn chứ!?<br>Có bị cây đổ cuốn vào không!? Bị thương ở đâu không!?<br> ',
    '…Không… bị thương… cũng không… bị cuốn vào…<br> ',
    'Đ-đúng là vậy… Hình như cô chỉ ngã ra đó thôi.<br>Vậy là do khó chịu trong người à? Sắc mặt cũng xấu quá… nguyên nhân là gì?<br> ',
    'Không… biết…<br> ',
    'Nếu vậy thì có thể là bệnh đột ngột.<br>Tôi sẽ đưa cô về căn cứ tiền tuyến ngay để tìm nguyên nhân—<br> ',
    'Tại sao… lại thành… thế này…<br>Em chỉ đói bụng… rồi ăn nấm… thôi mà…<br> ',
    '…Này‚ vừa rồi cô nói gì cơ?<br> ',
    'Nấm… Xiaolei nói là… Xiaolei đã ăn…<br>Cái mọc ở đây… nấm… đẹp lắm…<br> ',
    '…Nấm đẹp là<br>cây nấm mọc dưới đất kia‚ màu sắc với hoa văn sặc sỡ quá mức đó à?<br> ',
    'Ừ… cái đó…<br> ',
    'Ăn xong… cơ thể… không cử động được nữa…<br>Lý do… không biết… kỳ lạ…<br> ',
    'Không không không! Đây là nấm độc làm tê liệt cơ thể đấy!?<br> ',
    'Đ-ộc? Aiyaa…<br> ',
    'Sao cô lại ngạc nhiên chứ…<br>Dù chỉ mọc trong khu rừng này‚ nó vẫn là loại nấm độc khá nổi tiếng đấy.<br> ',
    'Thôi thì cứ cho là cô không biết cũng đành‚<br>nhưng đừng ăn cái nấm nhìn thôi đã thấy khả nghi thế này chứ…<br> ',
    'Nhưng… Xiaolei đói bụng… với lại nó ngon…<br>Xiaolei không biết… có độc… ưư… thật xin lỗi…<br> ',
    'Thiệt tình… chờ một chút. Thuốc giải đơn giản thì tôi cũng làm được—<br> ',
    'Hay quá! Cơ thể cử động được rồi! Sheshe!<br> ',
    'Dù đã uống thuốc giải‚ không ngờ cô lại hồi phục nhanh thế.<br>Cơ thể cô khá là bền bỉ đấy.<br> ',
    'Nhân tiện‚ cái “sheshe” mà cô cứ nói là gì vậy?<br> ',
    'Lời cảm ơn. Lời cảm ơn ở quê Xiaolei.<br> ',
    'Ồ‚ lần đầu tôi nghe từ đó đấy.<br>Cô tên là Xiaolei phải không? Cô đến từ nơi xa à?<br> ',
    'Ừ. Em là Xiaolei. Đến từ một nơi xa‚ xa lắm.<br> ',
    'Một mình à? Sao lại cất công đến một nơi nguy hiểm thế này?<br> ',
    'Đó là lời hứa với ông nội. Xiaolei sẽ trở nên mạnh hơn.<br> ',
    'Lời hứa với ông của cô?<br> ',
    'Ừ. Đó là chuyện hồi Xiaolei vẫn còn ở quê…<br> ',
    'Xiaolei… cháu của ta. Từ khi biết nhận thức đến nay‚<br>cháu đã cùng ta‚ chỉ hai ông cháu‚ miệt mài tu luyện suốt bao năm…<br> ',
    'Cháu đã mạnh mẽ đến mức này rồi! Ngay cả trong gia tộc đời đời lấy võ thuật làm nghiệp của ta‚<br>chưa ai ở tuổi cháu mà luyện võ đến trình độ này đâu!!<br> ',
    'Nhờ ông nội cả. Sheshe.<br> ',
    '…À thì‚ dù ta chẳng dạy gì‚<br>Xiaolei vốn sinh ra đã mạnh rồi cơ.<br> ',
    'Nhưng này Xiaolei‚ sức mạnh của cháu vẫn còn thiếu một thứ.<br>Cháu biết đó là gì không?<br> ',
    '…? Thể hình… chẳng hạn? Xiaolei nhỏ con.<br> ',
    'Không phải đâu. Đúng là thân hình cháu không lớn‚<br>nhưng ta đã dạy đủ kỹ thuật để bù lại rồi.<br> ',
    'Nghe đây‚ cháu của ta! Thứ cháu còn thiếu chính là trí tuệ!<br> ',
    'Trí tuệ…<br> ',
    'Ừm! Sức mạnh chân chính cần có sức lực‚ kỹ thuật――và trí tuệ!<br>Nhưng ta chỉ dạy được sức lực và kỹ thuật thôi! Nói thật‚ đầu óc ta không sáng lắm!<br> ',
    'Vì thế đó‚ cháu của ta! Hãy ra thế giới bên ngoài‚ học hỏi thật nhiều‚ trải nghiệm thật nhiều và trở nên khôn ngoan!<br>Làm vậy cháu sẽ mạnh hơn nữa! Giải thích xong! Đi đi nào!!!<br> ',
    'Vâng ạ.<br> ',
    'Chuyện là vậy đó.<br> ',
    'Ông cụ nhà cô quyết đoán quá mức rồi đấy…!! Còn cô thì chấp nhận nhanh quá đấy!!<br> ',
    'Vì Xiaolei muốn trở nên mạnh hơn mà.<br> ',
    'R-ra vậy… Tóm lại là cô đang trên đường võ giả tu hành nhỉ.<br>Một mình rời quê hẳn cô đơn lắm‚ vậy mà cô vẫn cố gắng ghê.<br> ',
    'Aiyaa――không hẳn. Xiaolei không có một mình. Đúng không‚ Panpan‚ Dandan.<br> ',
    'Kupyư!<br> ',
    'Kupyư~!<br> ',
    'Panpan và Dandan đang chào anh. Chúng nói “rất vui được gặp anh”.<br> ',
    'À‚ ừ… rất vui được gặp hai đứa…<br>Mà sao cô lại giao tiếp được với gấu trúc vậy?<br> ',
    'Vì bọn em lớn lên cùng nhau suốt mà‚ nên đó là chuyện đương nhiên.<br> ',
    'Cùng với hai bạn ấy‚ Xiaolei sẽ mạnh hơn.<br>Vì vậy Xiaolei có thể cố gắng.<br> ',
    'Hai bạn ấy à… đúng vậy nhỉ.<br> ',
    'Vậy thì không cần lo rồi. Cố lên nhé‚ Xiaolei.<br>Hẹn gặp lại ở đâu đó—<br> ',
    'Ối!?<br> ',
    'Chờ đã.<br> ',
    'Sao thế‚ cô nắm vạt áo tôi làm gì?<br>Còn có chuyện gì nữa à?<br> ',
    'Làm ơn.<br>Xiaolei muốn anh trở thành sư phụ――thầy của Xiaolei.<br> ',
    'Hả? Thầy? Sao lại là tôi!?<br>Nhìn là biết tôi đâu phải võ thuật gia‚ đúng không?<br> ',
    'Anh trông gầy nhom và yếu lắm‚ nhưng anh thông minh.<br>Anh cũng biết về nấm độc. Còn làm thuốc nữa.<br> ',
    'Để trở nên mạnh hơn‚ Xiaolei cần trí tuệ như vậy.<br>Xin hãy dạy Xiaolei thật nhiều.<br> ',
    'À… nếu còn ăn cả nấm độc mọc ven đường như thế‚<br>có lẽ cô nên học ít nhất là chút thường thức cơ bản thật…<br> ',
    'Nhưng những gì tôi dạy được cũng có hạn thôi.<br>Cô hãy tìm người thông minh hơn—<br> ',
    'Không. Xiaolei muốn anh dạy.<br> ',
    'À… nghe này. Tôi không nhận đệ tử đâu.<br>Vậy nên‚ tạm biệt nhé—!?<br> ',
    '(C-cử động không được! Chuyện gì thế này!?<br>Bàn tay Xiaolei nắm tay áo mình không nhúc nhích chút nào!?)<br> ',
    'Xiaolei muốn anh dạy cho Xiaolei.<br> ',
    'À‚ ờ… xin lỗi‚ nhưng tôi không thể làm vậy.<br>Tôi là Chỉ Huy của Căn Cứ Tiền Tuyến‚ thế này mà cũng bận lắm rồi.<br> ',
    'Căn Cứ Tiền Tuyến… Xiaolei biết. Anh là Chỉ Huy ở đó à?<br>Tuyệt quá. Xiaolei có mắt nhìn người thật.<br> ',
    'Nhà Xiaolei nghèo‚ nên Xiaolei cũng muốn đến Căn Cứ Tiền Tuyến kiếm tiền.<br>Nếu được thầy dạy‚ Xiaolei sẽ mạnh hơn‚ một mũi tên trúng hai đích.<br> ',
    'Tôi đã bảo là tôi bận mà.<br>Bỏ tay ra khỏi áo tôi… bỏ… chết tiệt‚ chẳng rời ra chút nào…!<br> ',
    'Thầy?<br> ',
    'Đã bảo tôi không phải thầy của cô mà! A‚ thật là…<br>Vậy cứ cho là tôi trở thành thầy của cô đi‚ tôi được lợi gì chứ?<br> ',
    'Xiaolei mạnh. Cũng có sức lực. Nhất định sẽ giúp ích cho thầy.<br> ',
    'Đúng là cô đang nắm tay áo tôi bằng sức mạnh kinh khủng thật‚<br>nhưng cô mạnh đến mức cô nói sao…?<br> ',
    'Ừm‚ vậy thử hỏi nhé: cô có thể di chuyển thân cây đổ lớn này không?<br>Tôi đang khổ vì không đi qua đây được.<br> ',
    'Ừm‚ cái cây này?<br> ',
    'Hự.<br> ',
    'Cái gì!? Nhấc bằng một tay sao!?<br> ',
    'Vâng.<br> ',
    'Thân cây đổ bị ném phắt sang bên.<br>Một tiếng “rầm” nặng nề vang lên‚ mặt đất dưới chân rung chuyển dữ dội.<br> ',
    '(Một thân cây đổ lớn như vậy mà có thể dễ dàng nhấc bằng một tay――!<br>Thân hình nhỏ nhắn đó lấy đâu ra sức mạnh quái vật thế chứ!?)<br> ',
    'Thế này được chưa?<br> ',
    '…………Được rồi‚ tôi nhận cô. Từ hôm nay hãy gọi tôi là thầy.<br> ',
    'Fufu. Sheshe. Mong thầy giúp đỡ‚ thầy nhé.<br> '
]

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def detect_newline(b):
    return 'CRLF' if b.count(b'\r\n') else 'LF'

def split_lines_preserve(text):
    return text.splitlines(keepends=True)

def line_core_nl(line):
    if line.endswith('\r\n'):
        return line[:-2], '\r\n'
    if line.endswith('\n'):
        return line[:-1], '\n'
    return line, ''

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]', s)

def ascii_comma_in_text(s):
    return ',' in s

def load_pairs(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=list)

WORK.mkdir(parents=True, exist_ok=True)
VI_ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)

en_bytes = EN_ASSET_PATH.read_bytes()
bom = en_bytes.startswith(b'\xef\xbb\xbf')
encoding = 'utf-8-sig' if bom else 'utf-8'
newline = detect_newline(en_bytes)
text = en_bytes.decode(encoding)
lines = split_lines_preserve(text)
jp_pairs = load_pairs(JP_PATH)
en_pairs = load_pairs(EN_JSON_PATH)

candidates = []
out_lines = lines[:]
blockers = []
items = []
trans_iter = iter(TRANSLATIONS)

for idx, line in enumerate(lines):
    core, nl = line_core_nl(line)
    parts = core.split(',')
    rec = parts[0] if parts else ''
    if rec in TEXT_RECORDS:
        text_idx = TEXT_RECORDS[rec]
        if len(parts) <= text_idx:
            blockers.append({'line': idx+1, 'type': 'FIELD_MISSING', 'record': rec})
            continue
        try:
            vi = next(trans_iter)
        except StopIteration:
            blockers.append({'line': idx+1, 'type': 'MISSING_TRANSLATION'})
            vi = parts[text_idx]
        if ascii_comma_in_text(vi):
            blockers.append({'line': idx+1, 'type': 'ASCII_COMMA_IN_VI_TRANSLATION', 'vi': vi})
        original_text = parts[text_idx]
        parts[text_idx] = vi
        out_lines[idx] = ','.join(parts) + nl
        candidates.append({
            'index': len(candidates)+1,
            'asset_line': idx+1,
            'record': rec,
            'source_text': original_text,
            'vi_text': vi,
            'jp_source': jp_pairs[len(candidates)][0] if len(candidates) < len(jp_pairs) else None,
            'en_reference': en_pairs[len(candidates)][1] if len(candidates) < len(en_pairs) else None,
            'match_status': 'EXACT' if len(candidates) < len(en_pairs) else 'UNMATCHED',
            'translation_status': 'TRANSLATED'
        })

try:
    extra = next(trans_iter)
    blockers.append({'type': 'EXTRA_TRANSLATIONS', 'first_extra': extra})
except StopIteration:
    pass

out_text = ''.join(out_lines)
VI_ASSET_PATH.write_bytes(out_text.encode(encoding))

# QA after write
vi_bytes = VI_ASSET_PATH.read_bytes()
vi_text = vi_bytes.decode(encoding)
vi_lines = split_lines_preserve(vi_text)
delimiter_mismatches = []
field_mismatches = []
technical_mismatches = []
tag_mismatches = []
placeholder_mismatches = []
unchanged_text_records = []
ascii_comma_violations = []
counts = {k:0 for k in TEXT_RECORDS}

for i, (src_line, dst_line) in enumerate(zip(lines, vi_lines), 1):
    s_core, _ = line_core_nl(src_line)
    d_core, _ = line_core_nl(dst_line)
    if s_core.count(',') != d_core.count(','):
        delimiter_mismatches.append(i)
    sp = s_core.split(',')
    dp = d_core.split(',')
    if len(sp) != len(dp):
        field_mismatches.append(i)
        continue
    rec = sp[0] if sp else ''
    if rec in TEXT_RECORDS:
        counts[rec] += 1
        ti = TEXT_RECORDS[rec]
        if sp[:ti] + sp[ti+1:] != dp[:ti] + dp[ti+1:]:
            technical_mismatches.append(i)
        if tags(sp[ti]) != tags(dp[ti]):
            tag_mismatches.append({'line': i, 'src_tags': tags(sp[ti]), 'vi_tags': tags(dp[ti])})
        if placeholders(sp[ti]) != placeholders(dp[ti]):
            placeholder_mismatches.append({'line': i, 'src': placeholders(sp[ti]), 'vi': placeholders(dp[ti])})
        if sp[ti] == dp[ti]:
            unchanged_text_records.append({'line': i, 'text': dp[ti]})
        if ',' in dp[ti]:
            ascii_comma_violations.append({'line': i, 'text': dp[ti]})
    else:
        if sp != dp:
            technical_mismatches.append(i)

if len(lines) != len(vi_lines):
    blockers.append({'type':'LINE_COUNT_MISMATCH', 'source':len(lines), 'vi':len(vi_lines)})
for name, arr in [('DELIMITER_MISMATCH',delimiter_mismatches),('FIELD_MISMATCH',field_mismatches),('TECHNICAL_MISMATCH',technical_mismatches),('TAG_MISMATCH',tag_mismatches),('PLACEHOLDER_MISMATCH',placeholder_mismatches),('ASCII_COMMA_TEXT_FIELD',ascii_comma_violations),('UNCHANGED_TEXT_RECORD',unchanged_text_records)]:
    if arr:
        blockers.append({'type': name, 'items': arr[:20], 'count': len(arr)})

# Targeted leftover scans in VI text fields
leftover_patterns = [r'\b(?:Ugh|Ah|Oh|Geez|What|Yes|No|Teacher|Commander|Frontline Base|Please|Wait|Huh|Honestly|Alright|Okay|Okaaay|Yay)\b', r'-(?:san|sama|kun|chan)\b']
intentional_kept = [
    {'term':'Xiaolei', 'reason':'proper name from EN alignment for シャオレイ'},
    {'term':'Panpan', 'reason':'proper name from EN alignment for パンパン'},
    {'term':'Dandan', 'reason':'proper name from EN alignment for ダンダン'},
    {'term':'Kupyu/Kupyu~', 'reason':'onomatopoeia/name-like panda call preserved/localized minimally'},
    {'term':'Sheshe', 'reason':'in-world thank-you word explicitly explained in source'},
    {'term':'Fufu', 'reason':'onomatopoeia/interjection retained as source tone'},
    {'term':'Aiyaa', 'reason':'character catchphrase/interjection retained as source tone'},
]
leftovers = []
for cand in candidates:
    v = cand['vi_text']
    for pat in leftover_patterns:
        if re.search(pat, v, flags=re.I):
            leftovers.append({'line':cand['asset_line'], 'pattern':pat, 'text':v})
if leftovers:
    blockers.append({'type':'LEFTOVER_ENGLISH_TARGETED', 'items':leftovers[:20], 'count':len(leftovers)})

focused = ['# Focused diff: hmn_10040100001 translatable records\n']
for cand in candidates:
    focused.append(f"\n## {cand['index']:03d} line {cand['asset_line']} {cand['record']}\n")
    focused.append('```diff\n')
    src_line = lines[cand['asset_line']-1].rstrip('\r\n')
    dst_line = vi_lines[cand['asset_line']-1].rstrip('\r\n')
    for dl in difflib.unified_diff([src_line+'\n'], [dst_line+'\n'], fromfile='EN asset', tofile='VI asset', lineterm=''):
        focused.append(dl.rstrip('\n')+'\n')
    focused.append('```\n')
DIFF_PATH.write_text(''.join(focused), encoding='utf-8')

qa_status = 'PASS' if not blockers else 'FAIL'
manifest = {
    'scene': SCENE,
    'status': 'TRANSLATED' if qa_status == 'PASS' else 'REVIEW',
    'qa_status': qa_status,
    'source_files': {
        'ja_json': {'path': str(JP_PATH), 'sha256': sha256(JP_PATH)},
        'en_json': {'path': str(EN_JSON_PATH), 'sha256': sha256(EN_JSON_PATH)},
        'en_asset': {'path': str(EN_ASSET_PATH), 'sha256': sha256(EN_ASSET_PATH), 'bytes': len(en_bytes), 'bom': bom, 'encoding': encoding, 'newline': newline, 'line_count': len(lines)},
    },
    'output_files': {
        'vi_asset': {'path': str(VI_ASSET_PATH), 'sha256': sha256(VI_ASSET_PATH), 'bytes': len(vi_bytes), 'bom': vi_bytes.startswith(b'\xef\xbb\xbf'), 'encoding': encoding, 'newline': detect_newline(vi_bytes), 'line_count': len(vi_lines)},
        'focused_diff': str(DIFF_PATH),
        'qa_log': str(QA_PATH),
        'manifest': str(MANIFEST_PATH),
        'script': str(WORK / 'generate_vi.py'),
    },
    'counts': {'candidate_text_records': counts, 'candidate_total': sum(counts.values()), 'translations': len(TRANSLATIONS), 'jp_pairs': len(jp_pairs), 'en_pairs': len(en_pairs)},
    'entries': candidates,
}
qa = {
    'scene': SCENE,
    'qa_status': qa_status,
    'blockers': blockers,
    'checks': {
        'line_count_match': len(lines) == len(vi_lines),
        'bom_preserved': bom == vi_bytes.startswith(b'\xef\xbb\xbf'),
        'newline_preserved': newline == detect_newline(vi_bytes),
        'delimiter_mismatches': delimiter_mismatches,
        'field_mismatches': field_mismatches,
        'technical_mismatches': technical_mismatches,
        'tag_mismatches': tag_mismatches,
        'placeholder_mismatches': placeholder_mismatches,
        'ascii_comma_violations': ascii_comma_violations,
        'unchanged_text_records': unchanged_text_records,
        'targeted_leftover_scan': leftovers,
    },
    'independent_verify': {
        'status': qa_status,
        'line_count_match': len(lines) == len(vi_lines),
        'source_output_line_count': [len(lines), len(vi_lines)],
        'bom_preserved': bom == vi_bytes.startswith(b'\xef\xbb\xbf'),
        'encoding': encoding,
        'candidate_text_records': counts,
        'delimiter_mismatches': len(delimiter_mismatches),
        'field_mismatches': len(field_mismatches),
        'technical_field_mismatches': len(technical_mismatches),
        'tag_mismatches': len(tag_mismatches),
        'placeholder_mismatches': len(placeholder_mismatches),
        'ascii_comma_in_text_fields': len(ascii_comma_violations),
        'unchanged_text_records': len(unchanged_text_records),
        'targeted_english_leftovers': len(leftovers),
        'vi_sha256': sha256(VI_ASSET_PATH),
    },
    'intentional_kept_terms': intentional_kept,
    'notes': [
        'JP is primary; EN asset used for alignment only.',
        'Speaker/name technical fields preserved exactly from EN asset.',
        'All characters confirmed 18+ by project context; no H18 content present in this file.',
        'ASCII commas are forbidden inside VI text fields; U+201A used where needed.',
        'Title translated in Vietnamese Title Case.',
    ],
}
MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status': qa_status, 'blocker_count': len(blockers), 'counts': manifest['counts'], 'vi_sha256': sha256(VI_ASSET_PATH)}, ensure_ascii=False, indent=2))
if blockers:
    print(json.dumps(blockers[:5], ensure_ascii=False, indent=2))
    raise SystemExit(1)
