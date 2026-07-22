from __future__ import annotations

import json, hashlib, re, difflib, shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10080100003'
EN_PATH = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_PATH = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
WORK.mkdir(parents=True, exist_ok=True)

TEXT_PREFIXES = ('title,','message,','messageTextUnder,','messageTextCenter,')

VI = [
'Lửa Và Băng',
'Bị quái vật tập kích rồi sống sót trở về.<br>Những binh sĩ trong đoàn vận tải vừa vượt qua cơn nguy hiểm đang ăn mừng vô cùng náo nhiệt.<br> ',
'Ở trung tâm bầu không khí ấy là Veera‚<br>người đã lập công lớn đem lại chiến thắng.<br> ',
'Cảm ơn nhiều lắm‚ Veera! Không có em thì bọn chị chắc chắn đã<br>bị quét sạch rồi!<br> ',
'Nữ thần của bọn tôi! Phép thuật đó đỉnh thật đấy!<br> ',
'Cảm ơn mọi người.<br>Nhưng thật sự cũng không có gì ghê gớm đâu ạ.<br> ',
'Không có chuyện đó đâu!<br>Em cứ tự hào hơn nữa cũng được mà!<br> ',
'Chà‚ vừa dễ thương vừa khiêm tốn‚ phép thuật lại còn ghê gớm.<br>Đúng là hoàn hảo không chỗ chê!<br> ',
'Được khen nhiều như vậy làm em ngại quá……<br> ',
'Mấy tên say xỉn này……<br>Gặp loại này em cứ đáp lại qua loa là được‚ Veera.<br> ',
'Không đâu ạ. Được mọi người đón nhận như thế này khiến em rất vui.<br>Em cảm thấy mình đã trở thành đồng đội của chị và mọi người……<br> ',
'Nhưng được khen nhiều quá thì em hơi khó xử.<br> ',
'Phép thuật em dùng chỉ có phạm vi rộng thôi.<br>Nó không mạnh đến mức ấy đâu ạ.<br> ',
'Nếu dùng hơi lạnh tấn công toàn bộ không gian thì chắc chắn sẽ trúng lõi……<br>Đó là kiểu phép như vậy nhỉ.<br> ',
'Vâng. Chính vì chị đã cho em thấy cần bao nhiêu ma lực để phá hủy lõi<br>nên em mới làm được như vậy.<br> ',
'Chị mới là người có phép thuật hoàn thiện hơn nhiều<br>vì chị xuyên thủng lõi bằng lượng sức mạnh tối thiểu.<br> ',
'Hoàn thiện hơn…… thì anh không nghĩ vậy đâu…… ừm……<br> ',
'Vốn dĩ dù không có em<br>thì Chỉ Huy và chị cũng xoay xở được mà……<br> ',
'Em muốn anh thấy phép thuật của em<br>nên lỡ bước ra phía trước.<br> ',
'Ừ‚ đúng là vậy. Verisa vừa tiêu diệt đám golem xung quanh<br>vừa dùng phép với ý thức bảo đảm đường rút lui.<br> ',
'Chúng ta hẳn đã có thể rút trước khi bị dồn đến đường cùng.<br>Em ấy thật sự rất đáng nể.<br> ',
'Đúng vậy ạ……!<br>Quả nhiên Chỉ Huy hiểu rất rõ.<br> ',
'Ồ? Đang nói về cô bé Verisa à?<br>So với Veera thì cũng chẳng có gì ghê gớm đâu nhỉ!<br> ',
'Sau khi thấy phép thuật của Veera<br>thì cô ấy đúng là một pháp sư hơi thảm hại nhỉ～♪<br> ',
'Ngược lại‚ ngược lại cơ.<br>Tôi đang nói Verisa là một pháp sư rất giỏi.<br> ',
'Này Veera.<br>……Hả? Veera?<br> ',
'――Vừa rồi các người nói gì cơ?<br> ',
'Một luồng khí lạnh buốt đến cắt da<br>thổi xuyên qua quán rượu đang hừng hực náo nhiệt.<br> ',
'Chị không có gì ghê gớm……?<br>Một pháp sư thảm hại……!?<br> ',
'Ngu ngốc làm sao……!<br>Chẳng hiểu gì cả mà lại thốt ra những lời xúc phạm tàn nhẫn như vậy……!<br> ',
'Cùng với lời nói ấy‚ Veera phóng ra xung quanh một luồng ma lực khủng khiếp.<br>Hơi lạnh như thể đóng băng mọi thứ dần lấp đầy quán rượu.<br> ',
'Ơ‚ ơơ!? Sao em lại nổi giận vậy‚ Veera!?<br> ',
'C‚ cái lạnh này là sao!? Phép thuật à!?<br> ',
'K‚ khoan đã‚ chuyện gì vậy!?<br>L‚ lạnh quá!? Kyaa!<br> ',
'Dám coi thường chị……!<br>Em không thể tha thứ được nữa……!<br> ',
'Ma lực bạo tẩu……!?<br>Veera‚ em không khống chế được phép thuật sao!?<br> ',
'Ư…… lạnh‚ quá…… cơ thể không cử động được……<br> ',
'T‚ tôi sắp đóng băng mất……!<br> ',
'Khốn……!<br>Cứ thế này sẽ có người bị thương mất!<br> ',
'Bình tĩnh lại‚ Veera!<br> ',
'Chỉ Huy ôm chặt lấy Veera<br>khi cô đang tỏa ra hơi lạnh dữ dội.<br> ',
'!?<br>Chỉ Huy…… sao……?<br> ',
'Đừng làm hơn nữa.<br>Đồng đội của anh sắp đóng băng mất rồi.<br> ',
'Nếu là trừng phạt thì thế này đủ rồi chứ?<br>Hãy tha cho họ đi……!<br> ',
'Ưư…… nhưng những người này<br>đã nói xấu chị của em……!<br> ',
'Vậy nên‚ vậy nên……!<br> ',
'Chính em cũng không kìm được cảm xúc và phép thuật của mình sao……!?<br>Chết tiệt‚ phải làm sao đây……!<br> ',
'<size=48>――Một Lát Trước Khi Veera Bắt Đầu Bạo Tẩu</size>',
'Thua em gái rồi lại hờn dỗi……<br>Mình đang làm gì thế này……<br> ',
'……Sau khi làm nguội cái đầu thì tâm trạng cũng khá hơn một chút.<br>Hay là đi xem Veera thế nào……<br> ',
'……? Vừa rồi là……<br> ',
'Ngay khi Verisa hướng mắt về phía quán rượu<br>cô cảm nhận được một đợt ma lực mạnh mẽ.<br> ',
'Đây là ma lực của Veera……!?<br>Trời ơi! Con bé đang làm gì vậy chứ～～～!!!<br> ',
'Bên trong quán rượu đầy hơi lạnh như đóng băng<br>nhiều binh sĩ không kịp thoát ra đã ngã gục.<br> ',
'Ư…… ý thức của tôi cũng……<br>Ai đó làm gì đi……!<br> ',
'Em đang làm gì vậy Veera!<br>Ngọn lửa ơi‚ làm ơn! Hãy xoa dịu luồng khí lạnh đang nổi giận này……!<br> ',
'Chị……!<br> ',
'Cùng với giọng nói ấy‚ ma lực ấm áp được giải phóng.<br>Quán rượu lạnh buốt dần được bao bọc trong hơi ấm như mùa xuân.<br> ',
'Chị ơi‚ sao chị lại ở đây……?<br> ',
'Trời ạ‚ chị đến là đương nhiên rồi chứ?<br>Ma lực của Veera thì chị nhận ra ngay mà!<br> ',
'Ồ‚ ồ…… Verisa……<br>Em đốt anh nhẹ một chút được không……?<br> ',
'Hya!? Anh ơi‚ anh sắp đóng băng rồi kìa!?<br>Trời ơi! Đúng là yếu xìu hết chỗ nói!<br> ',
'Verisa nắm lấy tay %user%<br>và bao bọc anh trong ma lực dịu dàng làm ấm toàn thân.<br> ',
'A…… ấm quá……<br> ',
'Chỉ trong chớp mắt Verisa đã trung hòa ma lực của Veera<br>và hỗn loạn trong quán rượu dần lắng xuống.<br> ',
'Tôi ngạc nhiên đấy……<br>Vậy là ổn rồi nhỉ?<br> ',
'Xin lỗi mọi người thật nhiều vì đã gây náo loạn nhé?<br>Nào‚ Veera cũng xin lỗi cho đàng hoàng đi.<br> ',
'Em xin lỗi!<br>Vì mọi người nói xấu chị nên em hơi làm quá tay!<br> ',
'Hả…… vừa rồi còn giận dữ đến thế mà giờ lại nhẹ nhàng vậy sao……?<br> ',
'Đó là mức hơi quá tay à……?<br> ',
'Biết nổi giận vì người khác là điểm tốt của em<br>nhưng mất kiểm soát ma lực thì không được đâu nhé!<br> ',
'Vâng.<br>Em sẽ cẩn thận.<br> ',
'Verisa‚ chuyện thế này đã có từ trước rồi à?<br> ',
'Ừm～ thỉnh thoảng thôi nhỉ?<br>Ma lực càng mạnh thì càng khó khống chế mà.<br> ',
'Vậy nên mỗi khi con bé bạo tẩu như thế này<br>em lại dùng phép thuật của mình để trung hòa đó～.<br> ',
'Ra là vậy.<br>Gì chứ‚ em đúng là một người chị đáng tin cậy đấy.<br> ',
'Anh bị sao vậy anh ơi‚ tự dưng khen em nhiều thế.<br>Là gia đình thì chuyện đó là đương nhiên mà?<br> ',
'Không đâu‚ chị thật sự rất tuyệt vời.<br> ',
'Khi em lần đầu làm phép thuật bạo tẩu cũng như vậy nhỉ……<br> ',
'(Khi còn nhỏ em kém khống chế ma lực hơn bây giờ rất nhiều<br>và rồi một lần kia em đã để phép thuật bạo tẩu.)<br> ',
'Phải…… làm sao đây……<br>Phép thuật‚ hơi lạnh‚ không dừng lại……<br> ',
'(Phép thuật không thể kìm lại quay nanh vuốt về phía chính em<br>và em suýt bị đóng băng bởi phép thuật của mình.)<br> ',
'Thế giới trở nên lạnh quá…… em cũng sắp đóng băng……<br>Em sẽ chết như thế này sao……?<br> ',
'Em đang làm gì vậy‚ Veera!<br> ',
'Chị…… ơi……?<br> ',
'(Rồi chị đã đến bên em.<br>Chị ôm chặt lấy em khi em run rẩy vì lạnh.)<br> ',
'Không được‚ tránh ra đi……<br>Cả chị cũng sẽ bị cuốn vào mất……<br> ',
'Nếu chị buông ra thì em sẽ đóng băng mất còn gì!<br>Không sao đâu‚ cứ để phép lửa của chị lo!<br> ',
'Không được đâu…… phép thuật của chị thì……<br> ',
'Veera‚ em đang xem thường phép thuật của chị đúng không～?<br>Hừ hừ‚ cứu một đứa em gái thì dễ như chơi…… ư‚ chị cứu được mà……!<br> ',
'Làm thế này…… ư‚ ưư……<br> ',
'(Với phép thuật của chị lúc ấy còn yếu hơn bây giờ rất nhiều<br>chị đã không thể kìm được phép thuật của em.)<br> ',
'(Nhưng chị không bỏ cuộc và mãi không buông em ra.<br>Dù khi đó cả hai có nguy cơ cùng chết cóng……)<br> ',
'N‚ này…… làm như vậy là ấm lên‚ đúng không……?<br> ',
'Ừm‚ ấm lắm.<br>Chị tuyệt thật đấy……<br> ',
'(Cuối cùng chị đã tạo ra một phép thuật kìm lại hơi lạnh<br>và cứu em khỏi thế giới băng giá ấy……!)<br> ',
'Khả năng khống chế ma lực tuyệt vời‚ tài năng tạo ra phép thuật mới<br>và tinh thần cao đẹp luôn muốn cứu giúp người khác.<br> ',
'Là một pháp sư<br>em thật lòng kính trọng chị từ tận đáy lòng.<br> ',
'Cô bé Verisa đã làm những chuyện như vậy sao……<br> ',
'……Cô ấy thật sự là một pháp sư tuyệt vời nhỉ.<br> ',
'Đúng vậy‚ chị tuyệt vời lắm.<br>Mỗi lần em làm ma lực bạo tẩu‚ chị luôn dùng phép lửa để cứu em.<br> ',
'Vậy mà chị lại làm như đó là chuyện đương nhiên……!<br>Chưa một lần bắt em phải mang ơn cả!<br> ',
'Chúng ta là gia đình mà‚ ân nghĩa hay nợ nần gì đâu có liên quan đúng không?<br>Em không cần để tâm đâu.<br> ',
'Chính những chỗ như vậy mới khiến chị tuyệt vời.<br>Mọi người hiểu rồi chứ?<br> ',
'Ừ…… tôi sẽ không nói xấu chị của cô nữa.<br>Tôi hối hận rồi.<br> ',
'Đó là lời nói thiếu suy nghĩ……<br>Xin lỗi nhé‚ Verisa.<br> ',
'Không sao không sao.<br>Chuyện em vẫn còn kém xa so với Veera cũng là thật mà.<br> ',
'Đừng vì chuyện này mà xa lánh Veera nhé.<br>Con bé không phải người xấu đâu‚ được chứ.<br> ',
'Ừ‚ tất nhiên rồi!<br>Cạn ly vì hai chị em pháp sư thiên tài!<br> ',
'Đúng! Cạn ly vì hai chị em pháp sư mỹ thiếu nữ!<br> ',
'Mấy người khéo nói quá rồi đấy……<br> ',
'Veera‚ người em lạnh hết rồi nhỉ.<br>Hay chúng ta cùng vào tắm để làm ấm hẳn lên nhé♪<br> ',
'Ừm!<br> ',
'Tôi sẽ dẫn đường.<br>Phòng tắm ở lối này.<br> ',
'Chà chà‚ hai chị em thân thiết là tốt rồi.<br>Cứ thong thả nhé.<br> ',
'À…… Chỉ Huy cũng muốn vào cùng không ạ?<br> ',
'Ồồ!?<br> ',
'Fuah!?<br>Sao anh ơi cũng vào cùng chứ!?<br> ',
'Vì Chỉ Huy đã ôm em suốt lúc em bạo tẩu mà.<br>Giống hệt như chị vậy.<br> ',
'Vậy à…… hừm?<br>Ông anh Chỉ Huy yếu xìu cũng có lúc làm được việc ra trò nhỉ.<br> ',
'Vậy thì anh ơi đã cố gắng cũng phải được thưởng chứ nhỉ?<br>Đặc biệt đó nha‚ anh có thể đi cùng cũng được?<br> ',
'A‚ anh cũng được vào tắm cùng sao?<br> ',
'Tiếc ghê. Anh ơi ở ngoài phòng tắm nhé♪<br>Nếu chỉ nghe giọng và âm thanh thì cũng được đó?<br> ',
'……Anh biết ngay sẽ là thế mà.<br> ',
'Lần khác mới được vào trong nhé?<br>Nào‚ đi thôi Veera.<br> ',
'Vâng‚ chị.<br> ',
'Vậy thì Chỉ Huy.<br>Chuyện tắm chung để lần khác nhé.<br> ',
'……Thật sao?<br>Lần khác thì được à?<br> ',
'Hì hì…… em đùa thôi.<br>Vì em muốn chỉ có hai chị em với nhau mà.<br> ',
'Đúng vậy đó.<br>Không được chen vào giữa hai chị em đâu‚ dù là anh ơi cũng không nhé?<br> ',
'Em yêu chị lắm.<br> ',
'Ừm‚ chị cũng yêu em lắm.<br>……Chào mừng em đến tiền tuyến‚ Veera.<br> ',
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def newline_style(data: bytes):
    if b'\r\n' in data:
        return 'CRLF'
    if b'\n' in data:
        return 'LF'
    return 'NONE'

def text_field_index(prefix):
    return 1 if prefix == 'title' else 2

def set_text(line: str, new_text: str) -> str:
    prefix = line.split(',',1)[0]
    if prefix == 'title':
        parts = line.split(',',1)
        return parts[0] + ',' + new_text
    parts = line.split(',',5)
    parts[2] = new_text
    return ','.join(parts)

def text_field(line: str):
    prefix = line.split(',',1)[0]
    if prefix == 'title':
        return line.split(',',1)[1]
    return line.split(',',5)[2]

def tags(s): return sorted(re.findall(r'<[^>]+>', s))
def placeholders(s): return sorted(re.findall(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}', s))

def main():
    src = EN_PATH.read_bytes()
    bom = src.startswith(b'\xef\xbb\xbf')
    text = src.decode('utf-8-sig')
    lines = text.splitlines()
    endings = re.findall(r'\r\n|\n|\r', text)
    assert len(endings) == len(lines)
    rec_idxs = [i for i,l in enumerate(lines) if l.startswith(TEXT_PREFIXES)]
    if len(rec_idxs) != len(VI):
        raise SystemExit(f'translation count mismatch {len(VI)} vs records {len(rec_idxs)}')
    out_lines = lines[:]
    manifest_records = []
    issues = []
    for n, idx in enumerate(rec_idxs):
        old = lines[idx]
        old_tf_for_br = text_field(old)
        vi_text = VI[n]
        # The EN asset is authoritative for <br> counts; trim extra VN line breaks
        # introduced from the JP novel while preserving the final UI break.
        while vi_text.count('<br>') > old_tf_for_br.count('<br>'):
            vi_text = vi_text.replace('<br>', ' ', 1)
            vi_text = re.sub(r' {2,}', ' ', vi_text)
        while vi_text.count('<br>') < old_tf_for_br.count('<br>'):
            vi_text = vi_text.rstrip() + '<br> '
        new = set_text(old, vi_text)
        old_tf = text_field(old); new_tf = text_field(new)
        if old.count(',') != new.count(','):
            issues.append({'line': idx+1, 'issue': 'delimiter_count'})
        if ',' in new_tf:
            issues.append({'line': idx+1, 'issue': 'ascii_comma_in_text', 'text': new_tf})
        if tags(old_tf) != tags(new_tf):
            issues.append({'line': idx+1, 'issue': 'tag_mismatch', 'old': tags(old_tf), 'new': tags(new_tf)})
        if placeholders(old_tf) != placeholders(new_tf):
            issues.append({'line': idx+1, 'issue': 'placeholder_mismatch', 'old': placeholders(old_tf), 'new': placeholders(new_tf)})
        out_lines[idx] = new
        manifest_records.append({'record_index': n+1, 'line': idx+1, 'command': old.split(',',1)[0], 'status': 'TRANSLATED'})
    if issues:
        raise SystemExit(json.dumps({'issues': issues[:20], 'count': len(issues)}, ensure_ascii=False, indent=2))
    out_text = ''.join(line+end for line,end in zip(out_lines,endings))
    out_bytes = (b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    if VI_PATH.exists():
        backup = WORK/(VI_PATH.name+'.bak')
        if not backup.exists():
            shutil.copy2(VI_PATH, backup)
    VI_PATH.write_bytes(out_bytes)
    diff = ''.join(difflib.unified_diff(lines, out_lines, fromfile=str(EN_PATH), tofile=str(VI_PATH), lineterm=''))
    (WORK/'focused_diff.md').write_text('```diff\n'+diff+'\n```\n', encoding='utf-8')
    ja = json.loads(JA_JSON.read_text(encoding='utf-8'))
    en = json.loads(EN_JSON.read_text(encoding='utf-8'))
    counts = {k.rstrip(','): sum(1 for l in lines if l.startswith(k)) for k in TEXT_PREFIXES}
    manifest = {
        'scene': SCENE,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'source': {'en_asset': str(EN_PATH), 'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'sha256': sha(EN_PATH), 'bytes': len(src), 'bom': bom, 'newline': newline_style(src), 'line_count': len(lines)},
        'output': {'vi_asset': str(VI_PATH), 'sha256': sha(VI_PATH), 'bytes': len(out_bytes), 'bom': out_bytes.startswith(b'\xef\xbb\xbf'), 'newline': newline_style(out_bytes), 'line_count': len(out_lines)},
        'candidate_counts': counts,
        'total_text_records': len(rec_idxs),
        'translated_records': len(rec_idxs),
        'records': manifest_records,
        'rules': {'jp_primary': True, 'commander': 'Chỉ Huy', 'ascii_comma_in_vi_fields': 'replaced with U+201A when needed', 'speaker_names_preserved': True, 'h18_confirmed_adult_project_rule': True},
        'status': 'GENERATED_PENDING_INDEPENDENT_VERIFY'
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    qa = {
        'scene': SCENE,
        'qa_status': 'PENDING_INDEPENDENT_VERIFY',
        'structural': {'line_count_match': len(lines)==len(out_lines), 'bom_match': bom==out_bytes.startswith(b'\xef\xbb\xbf'), 'newline_match': newline_style(src)==newline_style(out_bytes), 'delimiter_issues': 0, 'tag_issues': 0, 'placeholder_issues': 0, 'ascii_comma_in_vi_text': 0},
        'linguistic_notes': ['JP used as primary source; EN asset used for alignment.', 'Veera xưng em với Chỉ Huy; gọi Commander là Chỉ Huy.', 'Verisa giữ giọng trêu chọc; おにーさん được Việt hóa là anh/anh ơi/ông anh tùy sắc thái.', 'Tên speaker và charaload giữ nguyên.'],
        'unresolved': [],
        'changed_text_records': len(rec_idxs),
        'candidate_counts': counts,
    }
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'written': str(VI_PATH), 'work': str(WORK), 'records': len(rec_idxs), 'counts': counts}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
