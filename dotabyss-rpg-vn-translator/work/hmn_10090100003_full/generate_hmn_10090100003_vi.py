from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

scene = 'hmn_10090100003'
root = Path('E:/AgentTranslation')
work = root/'dotabyss-rpg-vn-translator'/'work'/f'{scene}_full'
en_asset = root/'Translation'/'en'/'RedirectedResources'/'assets'/'unnamed_assetbundle'/f'{scene}.txt'
vi_asset = root/'Translation'/'vi'/'RedirectedResources'/'assets'/'unnamed_assetbundle'/f'{scene}.txt'
ja_json = root/'dotabyss-translation-main'/'translations'/'novels'/scene/'ja.json'
en_json = root/'dotabyss-translation-main'/'translations'/'novels'/scene/'en.json'
work.mkdir(parents=True, exist_ok=True)
vi_asset.parent.mkdir(parents=True, exist_ok=True)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def file_meta(p):
    b=Path(p).read_bytes()
    return {
        'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
        'bom_utf8': b.startswith(b'\xef\xbb\xbf'),
        'newline': 'CRLF' if b'\r\n' in b and b.count(b'\r\n') == b.count(b'\n') else 'LF',
        'line_count': len(b.decode('utf-8-sig').splitlines(True)),
        'endswith_newline': b.endswith(b'\n'),
    }

# Vietnamese translations in asset text-record order: title, messageTextCenter, then every message.
vi_texts = [
    'Hãy Cùng Tạo Nên Đêm Tuyệt Nhất!',
    '<size=48>Ngày Diễn Ra Cuộc Thi</size>',
    'Những vũ công cừ khôi từ khắp thế giới<br>đã tụ hội về thành phố.<br> ',
    'Phù… cuối cùng cũng đến lúc biểu diễn thật rồi…<br> ',
    'Em thấy trong người thế nào?<br>Đã ăn uống đầy đủ chưa?<br> ',
    'Ừ‚ nhiều lắm.<br>Có tăng cân một chút‚ nhưng thôi kệ!<br> ',
    '…Người chiến thắng sẽ là tôi.<br>Nhất định tôi sẽ đứng trên đỉnh…!<br> ',
    'Ta mới là số một.<br>Ta sẽ múa lộng lẫy hơn bất cứ ai và nghiền nát tất cả!<br> ',
    '…Không khí có vẻ căng thẳng nhỉ.<br> ',
    'Chắc anh cảm nhận được sự căng thẳng của mọi người rồi.<br>Em hiểu mà. Bản thân em cũng đang hồi hộp đây.<br> ',
    'Nhưng thế này thì không ổn.<br>Không khí như vậy thì khán giả cũng đâu thể vui được!<br> ',
    'Em sẽ dùng điệu nhảy của mình để thay đổi bầu không khí.<br>Em sẽ làm cho tất cả cùng vui.<br> ',
    'Nhớ nhìn cho kỹ nhé!<br> ',
    'Ừ‚ anh rất mong chờ đấy!<br> ',
    'Vũ công tiếp theo là cô Levienne!<br>Mọi người hãy dành một tràng pháo tay chào đón cô ấy——<br> ',
    'Chờ mãi rồi!<br>Levienne ơi!<br> ',
    'Này‚ đừng hò hét quá.<br>Đây đâu phải chỗ như vậy.<br> ',
    'Ối‚ phải rồi…<br> ',
    'Vì đây là một cuộc thi nên khán giả theo dõi trong bầu không khí đầy căng thẳng.<br>Dưới những ánh mắt ấy‚ Levienne nở một nụ cười đầy tự tin.<br> ',
    'Nào… bắt đầu thôi!<br>Mọi người cùng vui hết mình nhé!<br> ',
    'Levienne cất tiếng thật vang rồi bắt đầu bước nhảy.<br>Gót giày nện mạnh xuống sân khấu‚ khắc nhịp điệu vào lồng ngực khán giả.<br> ',
    'Hây‚ hự… này!<br>Hì hì‚ nhìn đây!<br> ',
    'Cô đan xen những động tác cuốn hút vào điệu nhảy‚<br>mỉm cười rạng rỡ và di chuyển khắp sân khấu như chẳng còn khoảng trống nào.<br> ',
    'Một điệu nhảy nhẹ nhàng đến mức khó tin là đang giữa cuộc thi.<br>Ở đó là một màn vũ đạo chân chính khiến người xem quên mất kỹ thuật tuyệt vời phía sau.<br> ',
    'Trông cô ấy… vui thật đấy.<br> ',
    'Nhìn thôi mà tôi cũng muốn nhảy theo rồi.<br>Cứ ngồi yên xem thế này bứt rứt quá!<br> ',
    '(Hì hì‚ có vẻ mọi người bắt đầu sôi động rồi.<br>Nếu vậy… mấy bước đã tập gì đó‚ mặc kệ hết!)<br> ',
    'Những khán giả vốn căng thẳng dần nóng lên.<br>Thấy vậy‚ Levienne chuyển sang điệu nhảy ngẫu hứng.<br> ',
    'Nào mọi người! Có đang cháy hết mình không nào!?<br> ',
    'Ô‚ ôôô!?<br> ',
    'Cô bật nhảy thật cao bằng những bước chân nhẹ tênh‚<br>rồi vươn tay về phía khán giả.<br> ',
    'Hô to hơn nữa! Cử động cơ thể đi!<br>Cho em thấy nhiệt huyết của mọi người nào!<br> ',
    'Uooooo!<br>Tuyệt nhất luôn‚ Levienne ơi!<br> ',
    'Dễ thương! Ngầu quá! Tuyệt vời!<br> ',
    'Hì hì‚ em cảm nhận được rồi! Tình cảm của mọi người đã truyền tới em!<br> ',
    'Không chỉ có em đâu‚ cả mọi người sau em nữa!<br>Tất cả sẽ cho các bạn thấy những điệu nhảy cực kỳ vui nhộn!<br> ',
    'Levienne lướt một vòng quanh sân khấu.<br>Cô chạm mắt với từng khán giả rồi cất giọng thật lớn.<br> ',
    'Vì vậy mọi người cũng hãy cùng nhau sôi động lên‚<br>và biến đêm nay thành đêm tuyệt nhất nhé!<br> ',
    'Uooooooo!!!<br> ',
    'Cảm ơn mọi người!<br>Tất cả tuyệt vời nhất luôn!!!<br> ',
    'Từ bầu không khí căng như dây đàn chuyển thành hội trường náo nhiệt‚<br>Levienne kết thúc điệu nhảy với vẻ vui sướng đến tận cùng.<br> ',
    'Vậy thì‚ chúng tôi xin công bố kết quả cuộc thi.<br>Trước hết là các giải thưởng…<br> ',
    'Phù… mình làm quá rồi.<br> ',
    '(Điệu nhảy thì toàn ngẫu hứng‚ lại còn gọi cả khán giả làm theo ý mình.<br>Chắc đến lọt giải cũng không nổi đâu.)<br> ',
    '(Nhưng… vui tuyệt vời. Mọi người cũng đã vui.<br>Mình chẳng hối tiếc chút nào.)<br> ',
    '(Vì không đạt được kết quả‚<br>mình phải xin lỗi anh ấy mới được.)<br> ',
    'Và người chiến thắng là… cô Levienne!<br> ',
    '…Hả?<br> ',
    'Nào‚ xin mời cô lên sân khấu!<br> ',
    'Ơ‚ ơ!? Em thắng á!?<br>Chắc nhầm gì rồi chứ!?<br> ',
    'Không phải còn người khác nhảy giỏi hơn sao!?<br> ',
    'Không nhầm đâu.<br>Ban giám khảo‚ khán giả‚ tất cả đều nhất trí rằng cô chiến thắng hoàn toàn xứng đáng.<br> ',
    'Không thể nào… vì em đã tự ý làm loạn như thế…<br> ',
    'Cô nói gì vậy chứ!<br>Đó là điệu nhảy tuyệt nhất đêm nay đấy!<br> ',
    'Chúc mừng Levienne!<br>Lần sau lại cho bọn tôi xem điệu nhảy vui như thế nhé!<br> ',
    'Một điệu nhảy… vui…!<br> ',
    '…Cảm ơn mọi người!<br>Tất cả các bạn cũng tuyệt lắm!<br> ',
    'Uooooooo!!!<br> ',
    'Em thắng… thật sao…?<br> ',
    'Chúc mừng‚ Levienne!<br>Điệu nhảy của cô tuyệt thật đấy!<br> ',
    '…Như vậy có ổn không?<br>Chắc vẫn có người nhảy giỏi hơn mà?<br> ',
    'Tất cả chúng tôi đều quá tập trung vào chiến thắng nên đã quên mất khán giả.<br>Không ai còn dư tâm trí để nghĩ làm sao cho người xem vui cả.<br> ',
    'Vậy mà cô lại dùng điệu nhảy tuyệt nhất để khuấy động cả khán giả…<br>Thế này thì chúng tôi chỉ còn biết thừa nhận thất bại thôi!<br> ',
    '…Cảm ơn cô.<br>Điệu nhảy của cô cũng tuyệt lắm!<br> ',
    'Thật ra xét riêng về kỹ thuật thì người chiến thắng cũng là cô Levienne.<br> ',
    'Hơn nữa cô còn nắm bắt trái tim những khán giả đang căng thẳng‚ khiến họ vui lên‚<br>và thay đổi bầu không khí để các thí sinh khác dễ nhảy hơn…<br> ',
    'Ngoài cô ra‚ không ai có thể là người chiến thắng cả‚ cô Levienne.<br> ',
    'Em chỉ nhảy thật vui thôi.<br>Nhưng nếu mọi người cũng có thể nhảy vui vẻ… thì em hạnh phúc lắm!<br> ',
    'Đây mới là một vũ công đích thực…<br>Hì hì‚ đúng là không đọ lại được.<br> ',
    'Đẹp‚ vui tươi‚ nhưng đâu đó lại có nét quyến rũ…<br>Levienne‚ bầu không khí quanh cô hơi khác rồi đấy.<br> ',
    'Ô kìa‚ chẳng lẽ là nhờ ảnh hưởng của ai đó sao?<br> ',
    'Cá… k-không phải đâu!<br>Em chỉ nghĩ là cứ vui hết mình một chút thôi!<br> ',
    'Hừm~?<br>Nhưng bạn của cô đang đi về phía này kìa.<br> ',
    'Ơ…<br> ',
    'Ở cuối ánh nhìn của Levienne‚<br>%user% đang tiến lại gần cô.<br> ',
    'Levienne‚ em làm tốt lắm!<br>Chúc mừng em đã chiến thắng!<br> ',
    'Này‚ đừng khen em nhiều quá…<br> ',
    'Nhưng… cảm ơn anh.<br>Tất cả là nhờ anh đấy.<br> ',
    'Anh có làm gì đâu.<br>Nhưng có lẽ anh đã nói được một điều hữu ích.<br> ',
    'Thấy chưa? Cuối cùng thì em vẫn phải ăn uống đầy đủ đúng không?<br> ',
    'Hì hì‚ đúng vậy.<br>Từ giờ em sẽ không ép mình ăn kiêng quá đà nữa.<br> ',
    'Nếu em vừa nhảy vừa thấy khổ sở‚<br>khán giả sẽ nhận ra ngay mà.<br> ',
    'Em sẽ nhảy vui hơn bất cứ ai.<br>Và làm cho mọi người cùng vui.<br> ',
    'Từ giờ em sẽ tiếp tục nhảy như thế!<br> ',
    'Phải thế chứ.<br>Anh cũng hào hứng đến đói bụng rồi‚ đi ăn gì thôi.<br> ',
    '…Hừm~?<br>Dám rủ nhà vô địch cuộc thi đi ăn‚ anh cũng gan đấy.<br> ',
    'Vậy câu trả lời là?<br> ',
    'Anh đã cùng em tập luyện‚<br>nên em sẽ đặc biệt cho phép!<br> ',
    'Chỉ có em và anh‚<br>cùng mở tiệc mừng chiến thắng riêng của hai chúng ta nhé.<br> ',
    '%user% và Levienne biến mất vào thành phố‚<br>trông vui vẻ hơn bất cứ ai.<br> ',
]

text_commands = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}
# Read EN bytes preserving BOM/newline
raw = en_asset.read_bytes()
enc = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
text = raw.decode(enc)
newline = '\r\n' if '\r\n' in text else '\n'
lines = text.splitlines(True)
records = []
for i,line in enumerate(lines, start=1):
    stripped = line[:-len(newline)] if line.endswith(newline) else line
    parts = stripped.split(',')
    cmd = parts[0] if parts else ''
    if cmd in text_commands:
        idx = text_commands[cmd]
        records.append((i, cmd, idx, parts[idx] if len(parts)>idx else None))

assert len(records) == len(vi_texts), (len(records), len(vi_texts))

out_lines = []
changes = []
for line_no, line in enumerate(lines, start=1):
    has_nl = line.endswith(newline)
    stripped = line[:-len(newline)] if has_nl else line
    parts = stripped.split(',')
    cmd = parts[0] if parts else ''
    if cmd in text_commands:
        idx = text_commands[cmd]
        vi = vi_texts[len(changes)]
        old = parts[idx]
        if ',' in vi:
            raise ValueError(f'ASCII comma in VI field #{len(changes)+1}: {vi!r}')
        parts[idx] = vi
        new_stripped = ','.join(parts)
        changes.append({'record_index': len(changes)+1, 'line': line_no, 'command': cmd, 'old_text': old, 'vi_text': vi})
    else:
        new_stripped = stripped
    out_lines.append(new_stripped + (newline if has_nl else ''))
out_text = ''.join(out_lines)
# Preserve BOM if present
vi_asset.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8'))

# QA checks
def tag_counts(s):
    return sorted(re.findall(r'<[^>]+>', s))
def placeholders(s):
    return sorted(re.findall(r'%user%|%s|%d|\{\d+\}|\$\{[^}]+\}', s))
qa_errors=[]
out_raw = vi_asset.read_bytes()
out_text_dec = out_raw.decode(enc)
out_lines_dec = out_text_dec.splitlines(True)
if len(lines) != len(out_lines_dec): qa_errors.append(f'line_count {len(lines)} != {len(out_lines_dec)}')
for n,(src,dst) in enumerate(zip(lines,out_lines_dec), start=1):
    src_s = src[:-len(newline)] if src.endswith(newline) else src
    dst_s = dst[:-len(newline)] if dst.endswith(newline) else dst
    if src_s.count(',') != dst_s.count(','):
        qa_errors.append(f'line {n}: delimiter count changed {src_s.count(",")} -> {dst_s.count(",")}')
    sp=src_s.split(','); dp=dst_s.split(',')
    if sp and sp[0] in text_commands:
        idx=text_commands[sp[0]]
        if len(sp)!=len(dp): qa_errors.append(f'line {n}: field count changed {len(sp)} -> {len(dp)}')
        # nontext fields byte/string unchanged
        for j,(a,b) in enumerate(zip(sp,dp)):
            if j != idx and a != b:
                qa_errors.append(f'line {n}: nontext field {j} changed')
        if tag_counts(sp[idx]) != tag_counts(dp[idx]):
            qa_errors.append(f'line {n}: tag mismatch {tag_counts(sp[idx])} -> {tag_counts(dp[idx])}')
        if placeholders(sp[idx]) != placeholders(dp[idx]):
            qa_errors.append(f'line {n}: placeholder mismatch {placeholders(sp[idx])} -> {placeholders(dp[idx])}')
        if ',' in dp[idx]:
            qa_errors.append(f'line {n}: ASCII comma inside VI text field')

counts = {k:0 for k in text_commands}
for _,cmd,_,_ in records: counts[cmd]+=1
manifest = {
    'scene': scene,
    'status': 'PASS' if not qa_errors else 'FAIL',
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'sources': {'ja_json': file_meta(ja_json), 'en_json': file_meta(en_json), 'en_asset': file_meta(en_asset)},
    'output': file_meta(vi_asset),
    'work_dir': str(work),
    'text_command_counts': counts,
    'total_text_records': len(records),
    'translated_records': len(changes),
    'delimiter': ',',
    'internal_comma_rule': 'ASCII comma in Vietnamese text fields replaced/avoided; U+201A used where needed.',
    'mapping_status': {'TRANSLATED': len(changes), 'UNMATCHED': 0, 'AMBIGUOUS': 0, 'REVIEW': 0},
    'characters': {'レヴィエーヌ': 'kept charaload/speaker name; translated prose as Levienne', 'ルディア': 'kept charaload/speaker name; translated prose references contextually', '<user>/%user%': 'placeholder preserved'},
    'qa_errors': qa_errors,
    'independent_verify': {'status': 'PENDING', 'note': 'Run project verifier after generation.'}
}
qa_log = {
    'scene': scene,
    'status': manifest['status'],
    'adult_content': {'present': False, 'all_characters_confirmed_18_plus_by_user_context': True},
    'structural_qa': {
        'line_count_preserved': len(lines)==len(out_lines_dec),
        'bom_preserved': raw.startswith(b'\xef\xbb\xbf') == out_raw.startswith(b'\xef\xbb\xbf'),
        'newline_preserved': file_meta(en_asset)['newline'] == file_meta(vi_asset)['newline'],
        'delimiter_counts_preserved': not any('delimiter count' in e for e in qa_errors),
        'field_counts_preserved': not any('field count' in e for e in qa_errors),
        'tags_preserved': not any('tag mismatch' in e for e in qa_errors),
        'placeholders_preserved': not any('placeholder mismatch' in e for e in qa_errors),
        'text_command_counts': counts,
        'translated_records': len(changes),
    },
    'translation_qa': {
        'source_priority': 'JP primary; EN asset/novel used for alignment',
        'title_case': True,
        'commander_rule': 'Commander/司令官 -> Chỉ Huy; no Commander term appeared in this scene text fields',
        'speaker_names_preserved': True,
        'ascii_commas_in_vi_text': False,
        'unmatched': [], 'ambiguous': [], 'unresolved': []
    },
    'issues': [{'severity':'blocker','message':e} for e in qa_errors],
    'independent_verify': {'status': 'PENDING'}
}
(work/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(work/'qa_log.json').write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')
# Focused diff on text records only
old_focus=[]; new_focus=[]
for c in changes:
    old_focus.append(f"L{c['line']} {c['command']}: {c['old_text']}")
    new_focus.append(f"L{c['line']} {c['command']}: {c['vi_text']}")
diff='\n'.join(difflib.unified_diff(old_focus, new_focus, fromfile='EN text fields', tofile='VI text fields', lineterm=''))+'\n'
(work/'focused_diff.md').write_text('# Focused Text Diff: hmn_10090100003\n\n```diff\n'+diff+'```\n', encoding='utf-8')
print(json.dumps({'status': manifest['status'], 'records': len(records), 'counts': counts, 'qa_errors': qa_errors, 'output': str(vi_asset), 'work': str(work)}, ensure_ascii=False, indent=2))
