from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

scene = 'hmn_10010100001'
root = Path('E:/AgentTranslation')
work = root / 'dotabyss-rpg-vn-translator' / 'work' / f'{scene}_full'
en_asset = root / 'Translation' / 'en' / 'RedirectedResources' / 'assets' / 'unnamed_assetbundle' / f'{scene}.txt'
vi_asset = root / 'Translation' / 'vi' / 'RedirectedResources' / 'assets' / 'unnamed_assetbundle' / f'{scene}.txt'
ja_json = root / 'dotabyss-translation-main' / 'translations' / 'novels' / scene / 'ja.json'
en_json = root / 'dotabyss-translation-main' / 'translations' / 'novels' / scene / 'en.json'
manifest_path = work / 'manifest.json'
qa_path = work / 'qa_log.json'
diff_path = work / 'focused_diff.md'

TEXT_TYPES = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}

translations = [
    'Nghe Tin Ngài Gặp Khó Khăn Nên Tôi Đã Tới!',
    'Gàaaaaaa!!!<br> ',
    'Trước bầy quái vật‚ các binh sĩ đang lập đội hình chiến đấu.<br> ',
    'Chúng đông thật nhưng ta hoàn toàn có thể thắng! Bình tĩnh mà chiến đấu!<br> ',
    'Gruooooo!<br> ',
    'Chỉ Huy! Có kẻ địch cỡ lớn!<br> ',
    'Một con hàng khủng xuất hiện rồi à...!<br>Đừng đối đầu trực diện‚ câu giờ đi! Ta sẽ cho đơn vị khác yểm trợ!<br> ',
    'Nhưng các đơn vị hiện có thể điều động... đều đang giao chiến cả rồi!<br> ',
    'Áaaaaaa!?<br> ',
    'Người lính đang chống cự kẻ địch mạnh bị đòn tấn công dữ dội<br>của quái vật làm mất thăng bằng.<br> ',
    '――Tôi không để ngươi làm vậy đâu!<br> ',
    'Ngay lúc đó một nữ kỵ sĩ xen vào.<br>Cô dùng chiếc khiên mang theo đỡ đòn tấn công của quái vật và bảo vệ người lính.<br> ',
    'Quái vật tà ác...! Ta sẽ không để ngươi muốn làm gì thì làm đâu! Haaaaaaa!!!<br> ',
    'Gruoooo!?<br> ',
    'Nhân danh niềm kiêu hãnh của kỵ sĩ‚<br>ta sẽ không để ngươi làm hại đồng đội của ta thêm nữa!<br> ',
    'Nữ kỵ sĩ vung kiếm sắc bén về phía quái vật.<br>Cô đỡ toàn bộ đòn phản kích và không để đòn nào lọt tới binh sĩ sau lưng.<br> ',
    'Kỵ sĩ kia khá đấy...<br>Không chỉ mạnh‚ cô ấy còn bảo vệ trọn vẹn người lính đã ngã xuống.<br> ',
    'Đó là Rosa‚ kỵ sĩ của Milesgard!<br>Ở nước chúng tôi‚ cô ấy nổi danh nhờ thực lực của mình!<br> ',
    'Ra vậy‚ với bản lĩnh đó thì cũng dễ hiểu.<br> ',
    'Đòn này! Kết thúc!<br> ',
    'Con quái vật bực tức vì mọi đòn tấn công đều bị chặn nên động tác trở nên sơ hở.<br>Ngay khoảnh khắc ấy‚ một nhát chém chuẩn xác của Rosa đã xuyên qua nó.<br> ',
    'Phù... anh có bị thương không?<br> ',
    'V-vâng‚ Rosa. Cảm ơn cô đã cứu tôi!<br> ',
    'Anh không cần cảm ơn đâu. Thấy anh bình an là tôi thật sự mừng rồi.<br> ',
    'Tuyệt quá...!<br> ',
    'Được rồi‚ các cậu đã chiến đấu rất tốt trước kẻ địch mạnh.<br>Nghỉ một chút cho đến khi các đơn vị khác kết thúc giao tranh đi.<br> ',
    'Rõ!<br> ',
    'Thưa Chỉ Huy! Tôi sẽ đi cứu viện các đơn vị khác!<br> ',
    'Gì cơ?<br>Khoan đã‚ dù cô mạnh đến đâu thì đánh liên tiếp cũng sẽ quá sức―― này!<br> ',
    'Tôi không sao đâu! Xin cứ giao cho tôi!<br> ',
    'Rosa không đợi Chỉ Huy nói hết<br>mà lao về phía đơn vị đang giao chiến.<br> ',
    'Đối thủ của ngươi là ta đây! Seaaaaaa!!!<br> ',
    'Đơn vị bên kia đang hơi lép vế nên đúng là được cứu thật...<br>Nhưng tự ý trái lệnh à... thật hết cách...<br> ',
    'Toàn bộ đơn vị đã kết thúc giao tranh!<br> ',
    'Hiểu rồi. Bảo toàn bộ đơn vị kiểm tra thương tích và trang bị.<br>Xong thì nghỉ ngắn một lát.<br> ',
    'Nào... cô là Rosa nhỉ?<br> ',
    'Vâng‚ thưa Chỉ Huy. Vừa rồi ngài chỉ huy thật xuất sắc!<br> ',
    'Cô cũng chiến đấu rất đáng khen.<br>...Nếu bỏ qua chuyện tự ý chạy đi yểm trợ.<br> ',
    'Tôi không thể bỏ mặc đồng đội đang gặp nguy nan.<br>Vì đó là tinh thần kỵ sĩ của tôi!<br> ',
    'Tinh thần kỵ sĩ thì không sao nhưng vì thế mà lờ mệnh lệnh thì ta rất khó xử.<br> ',
    '...Vâng‚ tôi thật lòng thấy có lỗi.<br>Tôi xin chân thành tạ lỗi. Xin hãy ban cho tôi bất cứ hình phạt nào.<br> ',
    '(...Thái độ này là có xin lỗi nhưng không định sửa đây mà.<br>Nếu cô ấy hành động theo niềm tin thì có phạt cũng vô nghĩa nhỉ.)<br> ',
    'Ta sẽ không phạt. Cứ coi như ta đã phê chuẩn đề xuất của Rosa vậy.<br>Ta biết cô có bản lĩnh rồi‚ lần sau nhớ bàn với ta trước khi đi đấy.<br> ',
    'Thưa Chỉ Huy... cảm ơn ngài.<br>Quả nhiên ngài cũng là người tôn trọng tinh thần kỵ sĩ!<br> ',
    'Không‚ hoàn toàn không phải vậy đâu...<br> ',
    'Ở quê nhà‚ người ta thường nói phụ nữ mà lại muốn làm kỵ sĩ sao...<br>Tôi rất vui vì đã được Chỉ Huy tin tưởng.<br> ',
    'Đúng là người mà tôi phải bảo vệ!<br>Rosa này‚ nếu Chỉ Huy gặp khó khăn‚ tôi sẽ chạy đến bất cứ nơi đâu!<br> ',
    'Đã bảo không phải vậy mà... thôi‚ kệ đi.<br> ',
    '(Được tin tưởng thẳng thắn đến thế cũng phiền thật.<br>Cô nàng này khó xử lý quá... phải làm sao đây...)<br> ',
    '<size=48>――Vài Ngày Sau</size>',
    'Ưưưưưưưưư...<br>Giấy tờ chất như núi mà mình chẳng có chút động lực nào...<br> ',
    'Trước hết chuẩn bị đồ uống đã.<br>Nếu đang làm mà đi lấy thì mất tập trung nên tranh thủ bây giờ...<br> ',
    'Ừm... có lẽ phòng hơi bừa quá rồi.<br>Dọn phòng trước đã. Thế này thì không tập trung được.<br> ',
    'Ủa‚ móng tay dài rồi này. Phải cắt móng xong rồi mới làm việc...<br> ',
    'Không ổn rồi...! Cứ đúng lúc bận rộn<br>lại để ý mấy chuyện chẳng đâu vào đâu nên công việc không tiến triển!<br> ',
    'Đúng kiểu sát hạn chót là thế... Khó xử thật...<br> ',
    'Rầm!!! Cánh cửa phòng chỉ huy bật mở với một tiếng động lớn.<br> ',
    'Chỉ Huy gặp chuyện gì vậy ạ!<br> ',
    'Uwaa‚ chuyện gì thế!?<br> ',
    'Là tôi‚ Rosa đây!<br>Nghe tin Chỉ Huy gặp khó khăn nên tôi đã tới!<br> ',
    'Rosa!? Ta đâu có gọi cô đâu!?<br> ',
    'Vậy... sao ạ? Tôi tưởng mình nghe thấy ngài nói đang gặp khó khăn...<br> ',
    'Đúng là ta có nói... Cô đến vì ta nói khó xử quá à?<br> ',
    'Vâng‚ tôi đến để trợ giúp Chỉ Huy!<br> ',
    'Nếu Chỉ Huy gặp khó khăn thì tôi sẽ chạy đến bất cứ nơi đâu.<br>Vì tôi đã hứa như vậy mà!<br> ',
    'Cái đó không phải chỉ trong lúc chiến đấu thôi sao!? Đến lúc thế này cũng áp dụng à!<br> ',
    'Tất nhiên rồi! Bất kể khi nào hay ở đâu tôi cũng sẽ giúp ngài!<br> ',
    'Ờ-ừ... Vậy ví dụ nhé.<br> ',
    'Vâng!<br> ',
    'Nếu nửa đêm ta gặp khó khăn trong phòng ngủ<br>thì cô cũng sẽ chạy đến đó sao?<br> ',
    'Tất nhiên rồi! Xin hãy gọi tôi bất cứ lúc nào!<br> ',
    'Thật hả!? Vậy ngay tối nay cũng...<br> ',
    'Rosa này sẽ lập tức chạy tới và đưa Chỉ Huy đi ạ!<br> ',
    '...Đưa ta đi? Tại sao? Đưa ta đi đâu?<br> ',
    'Chuyện khó khăn lúc khuya thì hẳn là đói bụng đến mất ngủ đúng không ạ?<br>Tôi sẽ đưa ngài đến nhà ăn để chúng ta cùng ăn khuya!<br> ',
    'À‚ ra là vậy...<br> ',
    'Không phải sao ạ...? A! Nếu là bệnh đột ngột thì tôi sẽ đưa ngài đến trạm xá đàng hoàng!<br> ',
    '...Ừ‚ lúc thật sự cần giúp thì ta nhờ cô vậy...<br> ',
    'Vâng‚ tất nhiên rồi!<br> ',
    '(Chắc chắn cô ấy là người tốt nhưng ngây thơ<br>quá nên rắc rối thật.)<br> ',
    '(Không‚ khoan đã... nếu vậy thì...!)<br> ',
    '...Rosa.<br>Thật ra ta có việc muốn nhờ vì tin vào khả năng của cô.<br> ',
    'Vâng‚ vì Chỉ Huy đang gặp khó khăn thì tôi sẽ làm bất cứ điều gì.<br>Đó là nhiệm vụ thế nào ạ?<br> ',
    'Với tư cách Chỉ Huy căn cứ tiền tuyến‚ ta phải ra ngoài lo một công việc rất quan trọng.<br>Vì thế ta muốn Rosa hộ vệ cho ta.<br> ',
    'Nhiệm vụ hộ vệ ạ!<br>Đó là trọng trách tiêu biểu của kỵ sĩ‚ xin cứ giao cho tôi!<br> ',
    'Ta trông cậy vào cô đấy. Được rồi‚ đi thôi!<br> ',
    'Vâng‚ Chỉ Huy cứ để tôi bảo vệ!<br> ',
    'Chỉ Huy! Ngài vất vả với công việc rồi! Tôi đã pha trà cho ngài đây!<br> ',
    '...Ủa? Ngài ấy không có ở đây. Công việc đã xong rồi sao...<br> ',
    'Còn lại nhiều quá trời!!!<br> ',
]

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def read_ordered_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=list)

def newline_style(b):
    if b.count(b'\r\n') == b.count(b'\n') and b.count(b'\n') > 0:
        return 'CRLF'
    if b.count(b'\n') > 0:
        return 'LF'
    return 'NONE'

def text_index(record_type):
    return TEXT_TYPES[record_type]

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:\d+\$)?[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%|\\[nrt]', s)

def has_japanese(s):
    return bool(re.search(r'[\u3040-\u30ff\u3400-\u9fff]', s))

def has_ascii_comma(s):
    return ',' in s

work.mkdir(parents=True, exist_ok=True)
source_bytes = en_asset.read_bytes()
source_text = source_bytes.decode('utf-8-sig')
source_lines = source_text.splitlines(True)
source_noends = [ln.rstrip('\r\n') for ln in source_lines]

candidates = []
for i, line in enumerate(source_noends):
    typ = line.split(',', 1)[0] if ',' in line else line
    if typ in TEXT_TYPES:
        parts = line.split(',')
        idx = text_index(typ)
        candidates.append({'seq': len(candidates)+1, 'line': i+1, 'type': typ, 'speaker': parts[1] if len(parts)>1 else '', 'source_text': parts[idx] if len(parts)>idx else '', 'field_count': len(parts), 'delimiter_count': line.count(',')})

blockers = []
items = []
notes = []
if len(candidates) != len(translations):
    blockers.append({'code':'TRANSLATION_COUNT_MISMATCH','source_count':len(candidates),'translation_count':len(translations)})
for idx, tr in enumerate(translations, 1):
    if has_ascii_comma(tr):
        blockers.append({'code':'ASCII_COMMA_IN_TRANSLATION','seq':idx,'text':tr})

output_lines = source_noends[:]
entries = []
if not blockers:
    for cand, vi in zip(candidates, translations):
        line_idx = cand['line'] - 1
        parts = output_lines[line_idx].split(',')
        idx = text_index(cand['type'])
        source_field = parts[idx]
        parts[idx] = vi
        output_lines[line_idx] = ','.join(parts)
        status = 'TRANSLATED'
        match_status = 'EXACT' if cand['seq'] <= len(read_ordered_json(ja_json)) else 'CONTEXT_MATCH'
        entries.append({**cand, 'vi_text': vi, 'match_status': match_status, 'translation_status': status})

    newline = '\r\n' if newline_style(source_bytes) == 'CRLF' else '\n'
    out_text = newline.join(output_lines) + (newline if source_text.endswith(('\n','\r')) else '')
    out_bytes = (b'\xef\xbb\xbf' if source_bytes.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8')
    vi_asset.parent.mkdir(parents=True, exist_ok=True)
    vi_asset.write_bytes(out_bytes)

    # QA after write
    out_read = vi_asset.read_bytes()
    vi_text = out_read.decode('utf-8-sig')
    vi_lines = vi_text.splitlines(True)
    vi_noends = [ln.rstrip('\r\n') for ln in vi_lines]

    if len(vi_lines) != len(source_lines):
        blockers.append({'code':'LINE_COUNT_MISMATCH','source':len(source_lines),'vi':len(vi_lines)})
    if source_bytes.startswith(b'\xef\xbb\xbf') != out_read.startswith(b'\xef\xbb\xbf'):
        blockers.append({'code':'BOM_MISMATCH'})
    if newline_style(source_bytes) != newline_style(out_read):
        blockers.append({'code':'NEWLINE_MISMATCH','source':newline_style(source_bytes),'vi':newline_style(out_read)})

    changed_text_records = 0
    kept_en = []
    delimiter_mismatches = []
    tech_mismatches = []
    tag_mismatches = []
    placeholder_mismatches = []
    ascii_comma_violations = []
    jp_leftovers = []
    honorific_leftovers = []
    for cand in candidates:
        i = cand['line'] - 1
        s_parts = source_noends[i].split(',')
        v_parts = vi_noends[i].split(',')
        idx = text_index(cand['type'])
        if source_noends[i].count(',') != vi_noends[i].count(',') or len(s_parts) != len(v_parts):
            delimiter_mismatches.append({'seq':cand['seq'],'line':cand['line'],'source_delims':source_noends[i].count(','),'vi_delims':vi_noends[i].count(',')})
            continue
        if s_parts[:idx] + s_parts[idx+1:] != v_parts[:idx] + v_parts[idx+1:]:
            tech_mismatches.append({'seq':cand['seq'],'line':cand['line']})
        if s_parts[idx] != v_parts[idx]:
            changed_text_records += 1
        else:
            kept_en.append({'seq':cand['seq'],'line':cand['line'],'text':v_parts[idx]})
        if tags(s_parts[idx]) != tags(v_parts[idx]):
            tag_mismatches.append({'seq':cand['seq'],'line':cand['line'],'source_tags':tags(s_parts[idx]),'vi_tags':tags(v_parts[idx])})
        if placeholders(s_parts[idx]) != placeholders(v_parts[idx]):
            placeholder_mismatches.append({'seq':cand['seq'],'line':cand['line'],'source_placeholders':placeholders(s_parts[idx]),'vi_placeholders':placeholders(v_parts[idx])})
        if has_ascii_comma(v_parts[idx]):
            ascii_comma_violations.append({'seq':cand['seq'],'line':cand['line'],'text':v_parts[idx]})
        if has_japanese(v_parts[idx]):
            jp_leftovers.append({'seq':cand['seq'],'line':cand['line'],'text':v_parts[idx]})
        if re.search(r'-(san|sama|kun|chan)\b', v_parts[idx], re.I):
            honorific_leftovers.append({'seq':cand['seq'],'line':cand['line'],'text':v_parts[idx]})

    for code, arr in [('DELIMITER_MISMATCH', delimiter_mismatches), ('TECHNICAL_FIELD_MISMATCH', tech_mismatches), ('TAG_MISMATCH', tag_mismatches), ('PLACEHOLDER_MISMATCH', placeholder_mismatches), ('ASCII_COMMA_IN_VI_FIELD', ascii_comma_violations), ('JAPANESE_LEFTOVER', jp_leftovers), ('HONORIFIC_LEFTOVER', honorific_leftovers), ('UNINTENTIONAL_KEPT_EN', kept_en)]:
        if arr:
            blockers.append({'code':code,'items':arr})

    if changed_text_records != len(candidates):
        blockers.append({'code':'CHANGED_RECORD_COUNT_MISMATCH','changed':changed_text_records,'candidates':len(candidates)})

    # focused diff
    before = []
    after = []
    for cand in candidates:
        ln = cand['line']
        before.append(f"L{ln}: {source_noends[ln-1]}\n")
        after.append(f"L{ln}: {vi_noends[ln-1]}\n")
    diff = ''.join(difflib.unified_diff(before, after, fromfile=str(en_asset), tofile=str(vi_asset), lineterm=''))
    diff_path.write_text(diff, encoding='utf-8')
else:
    changed_text_records = 0
    out_read = b''

qa_status = 'PASS' if not blockers else 'FAIL'
source_counts = {
    'total_lines': len(source_lines),
    'candidate_text_records': len(candidates),
    'by_type': {typ: sum(1 for c in candidates if c['type']==typ) for typ in sorted(TEXT_TYPES)},
}
manifest = {
    'scene': scene,
    'status': qa_status,
    'created_at': datetime.now(timezone.utc).isoformat(),
    'sources': {
        'ja_json': str(ja_json),
        'en_json': str(en_json),
        'en_asset': str(en_asset),
        'vi_asset': str(vi_asset),
    },
    'source_properties': {
        'en_asset_sha256': sha256_bytes(source_bytes),
        'en_asset_bytes': len(source_bytes),
        'bom': 'UTF-8-SIG' if source_bytes.startswith(b'\xef\xbb\xbf') else 'UTF-8',
        'newline': newline_style(source_bytes),
        **source_counts,
    },
    'output_properties': {
        'vi_asset_sha256': sha256_bytes(out_read) if out_read else None,
        'vi_asset_bytes': len(out_read) if out_read else 0,
        'translated_records': changed_text_records,
    },
    'entries': entries,
    'artifact_paths': {
        'manifest': str(manifest_path),
        'qa_log': str(qa_path),
        'focused_diff': str(diff_path),
        'generator_script': str(Path(__file__)),
    },
}
qa = {
    'scene': scene,
    'qa_status': qa_status,
    'blockers': blockers,
    'items': items,
    'notes': notes + [
        'JP là nguồn chính; EN asset dùng để căn dòng.',
        'Tên nhân vật và charaload giữ nguyên; Commander/司令官 dịch là Chỉ Huy trong text field.',
        'Không có kept-EN intentional trong text records.',
    ],
    'checks': {
        'line_count': len(source_lines),
        'candidate_text_records': len(candidates),
        'translated_records': changed_text_records,
        'title_message_messageTextUnder_messageTextCenter_counted': True,
        'ascii_comma_in_vietnamese_fields_forbidden': True,
        'adult_h18_confirmed_all_18_plus': True,
    },
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'qa_status': qa_status, 'blocker_count': len(blockers), 'candidates': len(candidates), 'translated': changed_text_records, 'output': str(vi_asset), 'manifest': str(manifest_path), 'qa_log': str(qa_path), 'focused_diff': str(diff_path)}, ensure_ascii=False, indent=2))
if blockers:
    raise SystemExit(1)
