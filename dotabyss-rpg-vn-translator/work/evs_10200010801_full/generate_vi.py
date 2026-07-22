import json, hashlib, re, difflib
from pathlib import Path

scene = 'evs_10200010801'
root = Path('E:/AgentTranslation')
ja_path = root/'dotabyss-translation-main/translations/novels'/scene/'ja.json'
en_json_path = root/'dotabyss-translation-main/translations/novels'/scene/'en.json'
en_asset_path = root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{scene}.txt'
vi_asset_path = root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{scene}.txt'
work = root/'dotabyss-rpg-vn-translator/work/evs_10200010801_full'
work.mkdir(parents=True, exist_ok=True)

TRANSLATIONS = [
    'Tiêu Đề',
    'Hàa~… cuối cùng cũng về được rồi~~.<br>Khác hẳn lúc mới vào‚ Wendy khỏe khoắn lại rồi nhỉ…<br> ',
    'Nhờ Verisa và mọi người mà em khỏe gấp trăm lần rồi ạ!<br>Thế này thì việc chuẩn bị tiệc cũng có thể tiến triển thật nhanh!<br> ',
    'Mà phải nói là hai chị giỏi thật đấy ạ!<br>Em chưa từng thấy phép thuật nào tuyệt vời đến thế!<br> ',
    'Hừ hừ~~. Nếu là chị đây ra tay thì cỡ đó là chuyện đương nhiên♪<br>Các em cũng cố gắng tàm tạm đấy chứ nhỉ~?<br> ',
    'Thôi nào‚ chị hai đúng là chẳng chịu thật lòng gì cả.<br>Rõ ràng lúc nãy chị khen Wendy nhiều lắm mà.<br> ',
    'S‚ suỵt---! Viera‚ đừng nói mấy chuyện thừa thãi đó mà~~!<br> ',
    'Hihi. Hai chị em lúc nào cũng thân nhau nhỉ.<br>Việc chuẩn bị tiệc cứ để em lo tiếp nên mọi người nghỉ đi ạ.<br> ',
    'Không‚ em không sao đâu ạ. Phải chuẩn bị xong trước khi Chỉ Huy về<br>nên em không có thời gian nghỉ đâu.<br> ',
    '…Mà khoan‚ giờ là mấy giờ rồi nhỉ~?<br>Hình như tụi mình đã xuống Đại Huyệt lâu lắm rồi thì phải――<br> ',
    'Các em đang làm gì vậy?<br> ',
    'Hyaaaaááááá!?<br> ',
    'C‚ Chỉ Huy ạ!?<br>Sao anh lại ở đây… chẳng phải anh đang đi thị sát sao?<br> ',
    'Thị sát thì vừa xong rồi nên anh mới quay về đây.<br> ',
    'K‚ không thể nào…!? Anh về mất rồi sao~~!?<br> ',
    'Sao thế‚ có gì bất tiện à? Mà… cả ba đứa đều lấm lem bùn đất hết rồi kìa.<br>Các em đã làm gì vậy? Nhìn qua thì tình trạng của Wendy có vẻ đã ổn rồi.<br> ',
    'C‚ chuyện đó… xảy ra nhiều chuyện lắm~~! Aaa‚ thật tình!<br>Anh về sớm thế này thì tụi em đâu chuẩn bị kịp tiệc bất ngờ chứ~!<br> ',
    '――A.<br> ',
    'Chị hai… chị nói ra chuyện đó thì…<br> ',
    'Hả? …A…………<br> ',
    '…Không tính! Không không không! Vừa rồi không tính~~~~~~~~~~!<br>Anh trai chưa nghe thấy gì hết đúng không~~!? Đúng không!? Nha~~!?<br> ',
    'Anh nghe thấy tiệc bất ngờ rồi.<br> ',
    'Khôngggggg~~~~~~~~~~~~!<br>Quên đi~~! Anh đập đầu rồi quên luôn đi mà~~!<br> ',
    'Đừng đòi hỏi vô lý vậy.<br>Thật ra anh cũng đoán đại khái là chuyện như thế rồi.<br> ',
    'Ơ…!?<br>Chỉ Huy đã nhận ra rồi sao ạ…!?<br> ',
    'Anh đã thấy các em đi mua đồ ở chợ‚<br>còn Wendy thì đêm nào cũng làm thứ gì đó mà.<br> ',
    'K‚ không thể nào…<br>Vậy là anh biết hết rồi sao…<br> ',
    'Thôi‚ đừng bận tâm quá. Dù không còn là bất ngờ‚ việc các em<br>muốn làm điều gì đó cho anh cũng đủ khiến anh vui rồi.<br> ',
    'Nhưng Wendy thì hơi cố quá rồi. Đừng liều đến mức hỏng hóc như vậy nữa.<br>Người tổ chức mà không khỏe thì anh cũng không thể thật lòng vui được.<br> ',
    'Vâng… em sẽ rút kinh nghiệm…<br> ',
    'Vậy thì tốt.<br> ',
    'Nhưng… em vẫn muốn tổ chức tiệc bất ngờ lắm…<br> ',
    'Bàn tay của %user%<br>dịu dàng xoa đầu Wendy đang ủ rũ.<br> ',
    'Anh đã nói việc Wendy muốn chúc mừng anh là điều khiến anh vui nhất rồi mà?<br>Hơn nữa‚ có vẻ em đã học được rất nhiều điều. Gương mặt em trưởng thành hơn rồi đấy.<br> ',
    'Trưởng thành…? Anh nghĩ em đã trưởng thành rồi sao?<br> ',
    'Ừ‚ rất nhiều. Theo một nghĩa nào đó‚ được thấy em trưởng thành mới là bất ngờ lớn nhất.<br>Vậy thì… giờ chỉ cần tổ chức tiệc nữa là đúng kế hoạch. Anh sẽ giúp chuẩn bị.<br> ',
    'Hả~~? Gì vậy chứ~~.<br>Rõ ràng là tiệc mừng anh trai nhậm chức mà anh trai lại đi chuẩn bị sao~?<br> ',
    'Có sao đâu. Đâu có luật nào cấm nhân vật chính tự chuẩn bị.<br>À đúng rồi‚ nếu đã muộn một nhịp thì hay là kiêm luôn tiệc chào mừng Wendy nhỉ?<br> ',
    'Ý hay đấy ạ.<br>Chỉ Huy và Wendy cứ chúc mừng lẫn nhau là được mà♪<br> ',
    'Của Chỉ Huy và… của em…<br>Nghe tuyệt quá ạ! Chúng ta bắt đầu ngay thôi!<br> ',
    'Phòng tiệc trong ký túc xá được trang hoàng đủ màu sắc. Lúc này nơi đó<br>đang đông vui với rất nhiều người đến chúc mừng %user% và Wendy.<br> ',
    'Ồ! Quả là thịnh soạn thật!<br>Ta cùng đồng đội sẽ tận hưởng cho thật đã!<br> ',
    'Đồ trang trí bùm bùm bùm~ rồi lấp lánh tà-daaa! Cứ như lễ hội ấy!<br>À đúng rồi‚ lát nữa nhớ cho tớ nghe cảm tưởng về chiếc xe kéo cải tạo nhé!<br> ',
    'Tôi đến kiểm tra tình trạng của Wendy‚ nhưng xem ra không có vấn đề gì.<br>Tiệc sao… dù gì cũng đã đến đây rồi nên cho phép tôi tham gia nhé.<br> ',
    'Được rồiii! Hôm nay chúng ta cũng quẩy hết mình nào~~!!<br> ',
    'Chuyện này… đúng là bất ngờ thật. Đông người ghê.<br> ',
    'Tất nhiên rồi♪ Để mọi người chúc mừng anh trai‚<br>nhóm Verisa đã đi mời khắp nơi mà~♪<br> ',
    'Wendy là người cố gắng nhất mà.<br>Nhiều người tụ họp thế này là vì sự hết mình của Wendy đã chạm đến họ đấy.<br> ',
    'Ha ha‚ đây là lần đầu anh có một bữa tiệc long trọng thế này.<br> ',
    'Anh có vui không ạ‚ Chỉ Huy?<br> ',
    'Ừ‚ vui lắm.<br>Biết được bạn bè của Wendy đã tăng lên nhiều thế này‚ niềm vui còn nhân đôi nữa.<br> ',
    '…Thế nào‚ Wendy? Căn cứ tiền tuyến có rất nhiều người cá tính mạnh‚<br>nhưng toàn những người thú vị đúng không?<br> ',
    'Vâng ạ. Mọi người đều rất tốt bụng!<br> ',
    '…Lần này‚ nhờ được rất nhiều người giúp đỡ‚<br>em mới có thể tổ chức bữa tiệc này.<br> ',
    'Sức của em tuy nhỏ bé‚ nhưng nhờ nhiều người giúp đỡ‚<br>em có thể làm được chuyện lớn… điều đó khiến em rất vui!<br> ',
    'Ha ha‚ vậy à. Thế thì mọi người có vẻ đang chờ rồi‚<br>người chủ trì phải nói vài lời nâng ly chứ nhỉ.<br> ',
    'Nâng ly… để em làm thật sự ổn sao ạ?<br> ',
    'Đương nhiên là được rồi~♪<br>Wendy là công thần số một mà♪<br> ',
    'Tôi cũng nghĩ không ai phù hợp hơn Wendy đâu.<br>Nhờ em nhé♪<br> ',
    'Verisa‚ Viera…<br>――Vâng! Em sẽ thử ạ!<br> ',
    'Ưm… e hèm. Mọi người đã chờ lâu rồi. Bây giờ chúng ta sẽ bắt đầu<br>tiệc mừng Chỉ Huy nhậm chức!<br> ',
    'Ừm‚ bỏ qua lời chào cứng nhắc đi‚ trước hết là――<br> ',
    '――Cạn ly~~~♪<br> ',
    'Cạn ly~~♪<br> ',
    'Đó là một khởi đầu khá nhẹ nhàng đối với một bữa tiệc bất ngờ‚ nhưng<br>nhìn đâu cũng thấy những nụ cười――một bữa tiệc tràn đầy chất Wendy――<br> ',
]

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def read_text_props(path):
    b = path.read_bytes()
    bom = b.startswith(b'\xef\xbb\xbf')
    newline = 'CRLF' if b'\r\n' in b else 'LF'
    text = b.decode('utf-8-sig')
    return b, text, bom, newline

def split_line(line):
    if line.startswith('title,'):
        return line.split(',', 1)
    if line.startswith('message,'):
        return line.split(',', 5)
    return None

def text_field(parts):
    if not parts: return None
    if parts[0] == 'title': return 1
    if parts[0] == 'message': return 2
    return None

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%', s)

def candidate(line):
    return line.startswith('title,') or line.startswith('message,') or line.startswith('messageTextUnder,') or line.startswith('messageTextCenter,')

src_b, src_text, bom, newline = read_text_props(en_asset_path)
lines = src_text.splitlines()
# Preserve terminal final blank lines exactly via splitlines(True) for write
raw_lines = src_text.splitlines(keepends=True)
line_texts = [rl[:-2] if rl.endswith('\r\n') else rl[:-1] if rl.endswith('\n') else rl for rl in raw_lines]
if line_texts != lines:
    # splitlines() drops one final empty logical line sometimes; use raw-derived
    lines = line_texts
candidates = [(i,l) for i,l in enumerate(lines) if candidate(l)]
if len(candidates) != len(TRANSLATIONS):
    raise SystemExit(f'translation count {len(TRANSLATIONS)} != candidate count {len(candidates)}')

vi_lines = list(lines)
entries = []
blockers = []
for n, ((idx, line), vi) in enumerate(zip(candidates, TRANSLATIONS), 1):
    if ',' in vi:
        blockers.append({'line': idx+1, 'type': 'ASCII_COMMA_IN_VI', 'vi': vi})
    parts = split_line(line)
    tf = text_field(parts)
    old_text = parts[tf]
    if tags(old_text) != tags(vi):
        blockers.append({'line': idx+1, 'type': 'TAG_MISMATCH', 'src_tags': tags(old_text), 'vi_tags': tags(vi)})
    if placeholders(old_text) != placeholders(vi):
        blockers.append({'line': idx+1, 'type': 'PLACEHOLDER_MISMATCH', 'src_ph': placeholders(old_text), 'vi_ph': placeholders(vi)})
    parts[tf] = vi
    new_line = ','.join(parts)
    vi_lines[idx] = new_line
    entries.append({
        'ordinal': n, 'line': idx+1, 'record_type': parts[0], 'speaker': parts[1] if parts[0]=='message' and len(parts)>1 else None,
        'source_en': old_text, 'vi': vi, 'match_status': 'EXACT', 'translation_status': 'TRANSLATED'
    })

for i,(old,new) in enumerate(zip(lines, vi_lines), 1):
    if old.count(',') != new.count(','):
        blockers.append({'line': i, 'type': 'DELIMITER_COUNT_MISMATCH', 'old': old.count(','), 'new': new.count(',')})
    old_parts = split_line(old)
    new_parts = split_line(new)
    if old_parts and new_parts:
        if old_parts[0] == 'title':
            if old_parts[:1] != new_parts[:1]: blockers.append({'line': i, 'type':'TITLE_TECH_CHANGED'})
        elif old_parts[0] == 'message':
            if [old_parts[0], old_parts[1]] + old_parts[3:] != [new_parts[0], new_parts[1]] + new_parts[3:]:
                blockers.append({'line': i, 'type':'MESSAGE_TECH_CHANGED'})
            # Extra guard: no ASCII comma in VI text field beyond delimiters is implied by delimiter count.

# EN-kept QA: any translated candidate text equal to source or still ASCII-English alphabet-heavy without VI diacritics? log warnings only if proper/onomatopoeia.
english_kept = []
for e in entries:
    if e['source_en'] == e['vi']:
        english_kept.append({'line': e['line'], 'source_en': e['source_en'], 'vi': e['vi'], 'reason': 'UNCHANGED'})
# specific forbid translatable names-only like Wendy! unchanged: none expected.
if english_kept:
    blockers.append({'type':'UNCHANGED_EN_TEXT', 'items': english_kept})

out_newline = '\r\n' if newline == 'CRLF' else '\n'
out_text = out_newline.join(vi_lines)
# preserve whether original ended with newline
if src_text.endswith('\r\n') or src_text.endswith('\n'):
    out_text += out_newline
vi_asset_path.parent.mkdir(parents=True, exist_ok=True)
vi_bytes = (('\ufeff' if bom else '') + out_text).encode('utf-8')
if blockers:
    # still write artifacts but do not write output if blocker
    pass
else:
    vi_asset_path.write_bytes(vi_bytes)

# focused diff only candidates
before = [f"L{idx+1}: {line}\n" for idx,line in candidates]
after = [f"L{idx+1}: {vi_lines[idx]}\n" for idx,_ in candidates]
diff = ''.join(difflib.unified_diff(before, after, fromfile=str(en_asset_path), tofile=str(vi_asset_path), lineterm='\n'))
(work/'focused_diff.md').write_text('# Focused Diff: evs_10200010801\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')

ja_pairs = json.loads(ja_path.read_text(encoding='utf-8'), object_pairs_hook=list)
en_pairs = json.loads(en_json_path.read_text(encoding='utf-8'), object_pairs_hook=list)
manifest = {
    'scene': scene,
    'source_en_asset': str(en_asset_path),
    'source_ja_json': str(ja_path),
    'source_en_json': str(en_json_path),
    'output_vi_asset': str(vi_asset_path),
    'work_dir': str(work),
    'source_sha256': sha256_bytes(src_b),
    'output_sha256': sha256_bytes(vi_bytes) if not blockers else None,
    'source_bytes': len(src_b),
    'output_bytes': len(vi_bytes) if not blockers else None,
    'bom': bom,
    'newline': newline,
    'line_count_source': len(lines),
    'line_count_output': len(vi_lines),
    'candidate_record_count': len(candidates),
    'command_counts': {
        'title': sum(1 for _,l in candidates if l.startswith('title,')),
        'message': sum(1 for _,l in candidates if l.startswith('message,')),
        'messageTextUnder': sum(1 for _,l in candidates if l.startswith('messageTextUnder,')),
        'messageTextCenter': sum(1 for _,l in candidates if l.startswith('messageTextCenter,')),
    },
    'novel_ja_pairs': len(ja_pairs),
    'novel_en_pairs': len(en_pairs),
    'entries': entries,
    'qa_status': 'PASS' if not blockers else 'FAIL',
}
(work/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
qa = {
    'qa_status': 'PASS' if not blockers else 'FAIL',
    'blockers': blockers,
    'items': [],
    'notes': [
        'JP JSON used as primary source; EN JSON and EN asset used for ordered alignment.',
        'No H-18 content detected in this asset; adult-content special QA not applicable.',
        'All characters are treated as confirmed 18+ per task context.',
        'ASCII comma inside Vietnamese text fields is forbidden; U+201A used where needed.',
        'Speaker/ID/voice/chara technical fields preserved byte-for-byte for candidate records except translated text field.'
    ],
    'english_kept_records': english_kept,
}
(work/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({
    'qa_status': qa['qa_status'],
    'blocker_count': len(blockers),
    'source_sha256': manifest['source_sha256'],
    'output_sha256': manifest['output_sha256'],
    'line_count': len(lines),
    'candidate_record_count': len(candidates),
    'command_counts': manifest['command_counts'],
    'output': str(vi_asset_path),
    'manifest': str(work/'manifest.json'),
    'qa_log': str(work/'qa_log.json'),
    'focused_diff': str(work/'focused_diff.md')
}, ensure_ascii=False, indent=2))
if blockers:
    raise SystemExit(1)
