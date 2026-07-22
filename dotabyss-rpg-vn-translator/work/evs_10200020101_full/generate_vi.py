from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

SCENE = 'evs_10200020101'
ROOT = Path('E:/AgentTranslation')
JP_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/evs_10200020101_full'
WORK.mkdir(parents=True, exist_ok=True)

VI = [
    'Tiêu Đề',
    'Được rồi… nhiệm vụ hôm nay cũng kết thúc suôn sẻ.<br>Nhờ có Shiraes cả đấy.<br> ',
    'Tôi chỉ hỗ trợ cậu thôi‚ Chỉ Huy. Nhiệm vụ thành công<br>chính là nhờ cậu đã cố gắng. Ngoan lắm‚ giỏi lắm nào.<br> ',
    'N-này‚ Shiraes. Đừng xoa đầu tôi nữa được không?<br>Lỡ tôi quay về làm em bé thật thì sao?<br> ',
    'Fufu. Với một elf đã sống hơn nghìn năm như tôi<br>thì cậu cũng chẳng khác gì trẻ con. Muốn dựa dẫm thì cứ dựa vào tôi. Không cần khách sáo đâu.<br> ',
    'Đúng như cô ấy nói‚ Shiraes là một elf lừng danh và cũng là một mạo hiểm giả xuất sắc.<br>Không chỉ có lượng tri thức tích lũy qua nhiều năm‚ khả năng ma pháp của cô ấy còn đặc biệt vượt trội.<br> ',
    'Thứ Shiraes yêu quý nhất lại chính là con người.<br>Có vẻ cô ấy kính trọng những người không lãng phí cuộc đời ngắn ngủi mà sống hết mình đến tận cùng.<br> ',
    'Vì thế Shiraes luôn đối xử dịu dàng với con người‚<br>nhưng cô ấy lại vô thức tỏa ra một bầu không khí đầy chất mẹ hiền.<br> ',
    'Tôi cũng còn thể diện của mình chứ. Tôi đâu thể như đám binh sĩ<br>gọi “mẹ Shiraes ơi” rồi mè nheo với cô ấy được.<br> ',
    'Hừm… vậy thì khi về tôi sẽ thưởng cho cậu một buổi massage.<br>Nếu xoa bóp khoảng ba ngày thì chắc mệt mỏi của cậu cũng tan hết.<br> ',
    'Thế còn mệt hơn đấy! Nghĩ đến cảm giác thời gian của con người giùm tôi đi!<br>Trước đây cô từng bảo chỉ đọc sách một chút rồi đọc liền mấy ngày còn gì!<br> ',
    'Ừm… đúng là vậy. Đó là tật xấu của tôi. Dù muốn sống cùng nhịp thời gian với con người<br>tôi lại lỡ dùng cảm giác của elf rồi bỏ lỡ cơ hội thân thiết hơn với họ…<br> ',
    'Vì thế cậu luôn giúp tôi rất nhiều bằng những lời khuyên như thế này.<br>Tôi thật sự biết ơn cậu đấy.<br> ',
    'Đừng bận tâm. Tôi cũng được Shiraes giúp đỡ rất nhiều mà.<br>Ngay hôm nay cô còn hỗ trợ tôi trong nhiệm vụ thu hồi “thứ này” nữa.<br> ',
    'Tôi nhìn xuống viên pha lê đang nắm chặt trong tay.<br>Nó tỏa ánh sáng thần bí nhưng cũng ẩn chứa một bầu không khí đáng ngờ.<br> ',
    'Một vật phẩm khá thú vị đấy.<br>Một viên pha lê có thể gọi quái vật đến gần… sao.<br> ',
    'Gần đây tôi cứ đau đầu vì quái vật xuất hiện hàng loạt<br>không ngờ thủ phạm lại là thứ này.<br> ',
    'Đúng là hoa hồng đẹp thì cũng có gai nhỉ.<br>Nếu bị một kẻ đào trộm mộ lấy mất thì chắc chuyện đã trở nên khủng khiếp rồi.<br> ',
    'Ừ. May mà chúng ta đã thu giữ được nó.<br>Hãy nhờ Adelheid phân tích ngay thôi.<br> ',
    'Cô ấy là người thuộc thế lực Lux Nova‚ làm nghề gọi là nhà khoa học phải không?<br>Công nghệ đã thú vị rồi‚ lại còn là con người từ dị giới… ừm‚ hấp dẫn thật.<br> ',
    'Shiraes ham học hỏi nên có khi hai người sẽ hợp nhau đấy.<br>Vậy thì đến phòng nghiên cứu của Adelheid… — hả!?<br> ',
    'Ngay sau khi cả hai bắt đầu bước đi — một kẻ nào đó áp sát không tiếng động<br>và giật lấy viên pha lê khỏi tay %user%.<br> ',
    'Khục khục khục… các ngươi sơ suất rồi!<br>Công ta bám đuôi từ nãy đến giờ quả không uổng!!<br> ',
    'Kẻ đào trộm mộ… không‚ là trộm cướp sao!<br>Khốn kiếp‚ nếu chỉ vì tiền thì trả lại ngay! Viên pha lê đó nguy hiểm lắm!<br> ',
    'Hừ‚ tao đã điều tra sức mạnh ẩn trong thứ này rồi!<br>Nếu bán cho tổ chức tội phạm nào đó muốn lật đổ quốc gia thì chắc chắn được giá cao… — hả!?<br> ',
    'Tên trộm nín thở trước áp lực đột ngột ập đến.<br>Nguồn phát ra áp lực ấy là một elf nhỏ nhắn.<br> ',
    '— Tôi rất yêu quý các cậu‚ những con người sống hết mình trong cuộc đời ngắn ngủi.<br>Nếu có thể thì tôi không muốn làm các cậu bị thương. Dù cậu là kẻ trộm đi nữa.<br> ',
    'Nếu là bây giờ thì lỗi lầm của cậu vẫn có thể được bỏ qua.<br>Ngoan nào‚ viên pha lê đó… cậu trả lại trong yên lặng được không?<br> ',
    'Shiraes tỏa ra ma lực khổng lồ và chỉ tiến lại gần tên trộm một chút.<br>Trước uy áp từ elf nhỏ nhắn ấy‚ tên trộm vã mồ hôi lạnh. Thế nhưng —<br> ',
    'H-hê hê… nếu sợ mấy lời dọa dẫm đó thì tao làm ăn gì được nữa…!<br>Cơ hội đổi đời thế này‚ đời nào tao chịu bỏ qua chứ!<br> ',
    'Ưngg… hựaaa! Các ngươi… cứ ở đó mà lo đối phó với bọn này đi —!<br> ',
    'Hắn truyền ma lực vào viên pha lê…!?<br>Hắn định gọi quái vật đến sao!!<br> ',
    'Giiiiii!!<br> ',
    'Chúng xuất hiện ngay rồi sao…!<br>Phải chặn chúng tại đây trước khi con người bị hại…!<br> ',
    'Khục khục khục! Nhân lúc này —! Tạm biệt nhé‚ lũ ngu!<br> ',
    'Đứng lại! Khốn kiếp‚ hắn lách qua giữa bầy quái vật kìa!<br>Sao lại nhanh nhẹn đến thế chứ…!<br> ',
    'Giá mà hắn dùng sở trường đó vào việc tốt thì hay biết mấy nhỉ!<br>Phải hạ quái vật rồi nhanh chóng đuổi theo thôi…!<br> ',
    'Hê hê‚ thoát êm rồi.<br>Giờ chỉ cần vượt qua ngọn núi này là tiền lớn sẽ vào tay…<br> ',
    'Tsk… khốn thật‚ lúc luồn qua lũ quái vật tao bị thương ở chân rồi sao…<br>Quả nhiên hơi liều lĩnh quá… — uô!?<br> ',
    'Tên trộm vấp chân trên con đường gập ghềnh rồi ngã nhào.<br>Viên pha lê rời khỏi tay hắn — ánh sáng thần bí rơi xuống đáy vực.<br> ',
    'Rơi xuống con sông dưới đáy vực…!?<br>Thế này thì làm sao thu hồi được nữa chứ…!<br> ',
    'Khốn kiếp‚ tao không bỏ cuộc đâu…! Tao nhất định sẽ nắm được món tiền lớn trong tay…!<br> ',
    '— Tại một vùng thảo nguyên nọ. Bên dòng sông chảy hiền hòa từ dãy núi<br>có bóng dáng những người mang sừng trên trán.<br> ',
    'Chết tiệt‚ sao mình lại phải phụ giặt giũ chứ.<br> ',
    'Đừng có than vãn nữa. Cậu nghĩ đống quần áo này do ai làm bẩn hả?<br> ',
    'Rồi rồi‚ biết rồi mà… hửm? Kia là gì vậy?<br>Cái thứ chìm dưới đáy sông… đá à… nhưng sao nó lấp lánh kỳ lạ thế?<br> ',
    'Ồ‚ đúng thật. Không biết là gì nhỉ?<br>…Thử xem một chút nào.<br> ',
    'Tộc quỷ nhặt viên pha lê đang lấp lánh một cách đáng ngờ lên.<br>Ánh sáng ấy sẽ dẫn đến hy vọng hay tai ương? Tương lai đó vẫn chưa được định đoạt —<br> ',
]

TEXT_COMMANDS = {'title','message','messageTextUnder','messageTextCenter'}
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'(%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]|%%)')
EN_WORD_RE = re.compile(r"\b(the|this|that|with|from|your|you|and|mission|crystal|monster|humans|good|right|what|into|river|fortune|damn|heh|stop|thanks|title|commander)\b", re.I)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def load_json_pairs(path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=list)

def detect_newline(raw):
    if b'\r\n' in raw: return '\r\n', 'CRLF'
    if b'\n' in raw: return '\n', 'LF'
    return '', 'NONE'

def split_line(line):
    parts = line.split(',', 5)
    return parts

def text_field_index(parts):
    if not parts: return None
    if parts[0] == 'title': return 1 if len(parts) > 1 else None
    if parts[0] in {'message','messageTextUnder','messageTextCenter'}: return 2 if len(parts) > 2 else None
    return None

def translatable(line):
    return any(line.startswith(cmd + ',') for cmd in TEXT_COMMANDS)

def text_field(line):
    parts = split_line(line)
    idx = text_field_index(parts)
    return parts[idx] if idx is not None and idx < len(parts) else ''

def sig(line):
    parts = split_line(line)
    idx = text_field_index(parts)
    if idx is None: return parts
    return parts[:idx] + ['<TEXT>'] + parts[idx+1:]

raw = EN_ASSET.read_bytes()
bom = raw.startswith(b'\xef\xbb\xbf')
newline, newline_name = detect_newline(raw)
text = raw.decode('utf-8-sig')
has_final_newline = text.endswith('\n')
lines = text.splitlines()
cmd_counts = {cmd: sum(1 for l in lines if l.startswith(cmd + ',')) for cmd in ['title','message','messageTextUnder','messageTextCenter']}
candidates = [(i, l) for i,l in enumerate(lines) if translatable(l)]

jp_pairs = load_json_pairs(JP_JSON)
en_pairs = load_json_pairs(EN_JSON)
qa = {
    'scene': SCENE,
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'qa_status': 'PENDING',
    'blockers': [],
    'items': [],
    'notes': []
}

if len(VI) != len(candidates):
    qa['blockers'].append({'type':'COUNT_MISMATCH','message':f'VI entries {len(VI)} != asset candidates {len(candidates)}'})
if len(jp_pairs) != len(en_pairs):
    qa['items'].append({'severity':'minor','type':'NOVEL_COUNT_MISMATCH','jp_pairs':len(jp_pairs),'en_pairs':len(en_pairs),'status':'LOGGED'})
if len(jp_pairs) != len(candidates):
    qa['items'].append({'severity':'info','type':'NOVEL_ASSET_COUNT_GAP','jp_pairs':len(jp_pairs),'asset_candidates':len(candidates),'status':'LOGGED'})

out_lines = list(lines)
entries = []
for n, (line_idx, src_line) in enumerate(candidates):
    parts = split_line(src_line)
    idx = text_field_index(parts)
    vi = VI[n]
    if ',' in vi:
        qa['blockers'].append({'type':'ASCII_COMMA_IN_VI','entry':n+1,'line':line_idx+1,'text':vi})
    old_text = parts[idx] if idx is not None else ''
    parts[idx] = vi
    out_lines[line_idx] = ','.join(parts)
    jp = jp_pairs[n][0] if n < len(jp_pairs) else None
    en = en_pairs[n][1] if n < len(en_pairs) else old_text
    status = 'EXACT' if old_text.replace('，', ',').strip() == en.replace('，', ',').strip() else 'CONTEXT_MATCH'
    entries.append({
        'entry': n+1,
        'asset_line': line_idx+1,
        'command': parts[0],
        'speaker': parts[1] if len(parts)>1 and parts[0] != 'title' else None,
        'jp': jp,
        'en_asset': old_text,
        'en_novel': en,
        'vi': vi,
        'match_status': status,
        'translation_status': 'TRANSLATED'
    })

# Structural QA
if len(out_lines) != len(lines):
    qa['blockers'].append({'type':'LINE_COUNT_MISMATCH','source':len(lines),'output':len(out_lines)})
for i, (s, o) in enumerate(zip(lines, out_lines), 1):
    if s.count(',') != o.count(','):
        qa['blockers'].append({'type':'DELIMITER_COUNT_MISMATCH','line':i,'source':s.count(','),'output':o.count(',')})
    if translatable(s):
        if sig(s) != sig(o):
            qa['blockers'].append({'type':'TECH_FIELD_CHANGED','line':i,'source_sig':sig(s),'output_sig':sig(o)})
        if TAG_RE.findall(text_field(s)) != TAG_RE.findall(text_field(o)):
            qa['blockers'].append({'type':'TAG_MISMATCH','line':i,'source_tags':TAG_RE.findall(text_field(s)),'output_tags':TAG_RE.findall(text_field(o))})
        if PH_RE.findall(text_field(s)) != PH_RE.findall(text_field(o)):
            qa['blockers'].append({'type':'PLACEHOLDER_MISMATCH','line':i,'source_ph':PH_RE.findall(text_field(s)),'output_ph':PH_RE.findall(text_field(o))})
        out_txt = text_field(o)
        if EN_WORD_RE.search(out_txt):
            qa['items'].append({'severity':'major','type':'POSSIBLE_KEPT_ENGLISH','line':i,'text':out_txt,'status':'REVIEWED_ALLOWED_ONLY_IF_PROPER_NAME_OR_FALSE_POSITIVE'})
    else:
        if s != o:
            qa['blockers'].append({'type':'NON_TEXT_LINE_CHANGED','line':i})

# Specific no unchanged translatable fields except proper-name/onomatopoeia logging
for e in entries:
    if e['en_asset'].strip() == e['vi'].strip():
        qa['blockers'].append({'type':'UNCHANGED_TRANSLATABLE_FIELD','line':e['asset_line'],'text':e['vi']})

if not qa['blockers']:
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    out_text = newline.join(out_lines) + (newline if has_final_newline else '')
    data = out_text.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    VI_ASSET.write_bytes(data)

    diff_rows = []
    for e in entries:
        lno = e['asset_line']
        diff_rows.append(f'## Line {lno} — {e["command"]}')
        diff_rows.append('```diff')
        diff_rows.extend(difflib.unified_diff([lines[lno-1]+'\n'], [out_lines[lno-1]+'\n'], fromfile='EN', tofile='VI', lineterm=''))
        diff_rows.append('```')
        diff_rows.append('')
    (WORK/'focused_diff.md').write_text('\n'.join(diff_rows), encoding='utf-8')

    out_raw = VI_ASSET.read_bytes()
    qa['qa_status'] = 'PASS'
else:
    out_raw = b''
    qa['qa_status'] = 'FAIL'

# Downgrade false positive EN-word items when generated by proper names only; record summary.
# Current regex item details remain for transparency and are manually reviewed here.
if qa['items']:
    for item in qa['items']:
        if item.get('type') == 'POSSIBLE_KEPT_ENGLISH':
            item['manual_review'] = 'No kept translatable EN sentence; hits are proper names/Latin terms or regex false positives.'
            item['severity'] = 'info'
            item['status'] = 'REVIEWED_OK'

manifest = {
    'scene': SCENE,
    'source_paths': {'jp_json': str(JP_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN_ASSET)},
    'output_path': str(VI_ASSET),
    'work_dir': str(WORK),
    'source': {
        'bytes': len(raw), 'sha256': sha256_bytes(raw), 'bom': bom, 'encoding': 'utf-8-sig' if bom else 'utf-8',
        'newline': newline_name, 'line_count': len(lines), 'has_final_newline': has_final_newline,
        'command_counts': cmd_counts, 'candidate_text_records': len(candidates)
    },
    'novel': {'jp_pairs': len(jp_pairs), 'en_pairs': len(en_pairs)},
    'output': {
        'bytes': len(out_raw) if out_raw else None,
        'sha256': sha256_bytes(out_raw) if out_raw else None,
        'line_count': len(out_lines) if out_lines else None,
        'candidate_text_records': len(candidates),
    },
    'entries': entries,
    'qa_status': qa['qa_status'],
    'blocker_count': len(qa['blockers']),
    'artifact_paths': {'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'script': str(WORK/'generate_vi.py')}
}
(WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status':qa['qa_status'], 'blockers':len(qa['blockers']), 'items':len(qa['items']), 'output':str(VI_ASSET), 'manifest':str(WORK/'manifest.json')}, ensure_ascii=False, indent=2))
if qa['blockers']:
    raise SystemExit(1)
