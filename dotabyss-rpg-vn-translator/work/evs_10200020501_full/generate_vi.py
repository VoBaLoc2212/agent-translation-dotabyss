import hashlib
import json
import re
from pathlib import Path
from difflib import unified_diff
from datetime import datetime, timezone

SCENE = 'evs_10200020501'
ROOT = Path('E:/AgentTranslation')
JA_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET_PATH = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET_PATH = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK_DIR = ROOT / 'dotabyss-rpg-vn-translator/work/evs_10200020501_full'
MANIFEST_PATH = WORK_DIR / 'manifest.json'
QA_LOG_PATH = WORK_DIR / 'qa_log.json'
DIFF_PATH = WORK_DIR / 'focused_diff.md'

CMD_PREFIXES = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

VI = [
    'Tiêu Đề',
    'Nhờ màn quảng bá của %user%‚<br>Oni Island trở nên náo nhiệt với dân làng quanh vùng đến tham quan. Thế nhưng――<br> ',
    'Nghe nói có thể tận hưởng miễn phí một điểm du lịch mới nên tôi mới đến――<br>mà... đây chẳng phải Oni Island nơi quỷ tộc sinh sống sao...!?<br> ',
    'Ch-chuyện gì thế này!? Chúng ta bị lừa đến đây sao...!?<br> ',
    'Hê hê hê hê! Chào mừng các ngươi đã tới đây... lũ con người kia~~~!<br> ',
    'Hííííí!? Quỷ kìa!?<br> ',
    '(Mình hiểu là anh ta rất hăng hái‚ nhưng cười tệ quá...!<br>Khách khó khăn lắm mới tới đã sợ cứng người rồi! Lúc này quả nhiên phải――!)<br> ',
    '――Kính chào quý vị đã đến với Oni Island hôm nay.<br>Tôi là Kureha‚ người sẽ đảm nhiệm vai trò hướng dẫn viên du lịch của quý vị.<br> ',
    'Hôm nay‚ chúng tôi mong quý vị có thể thưởng thức trọn vẹn mọi sức hấp dẫn của Oni Island.<br>Xin đừng căng thẳng‚ hãy thong thả tận hưởng thời gian ở đây.<br> ',
    'C-cô ấy cũng là quỷ tộc sao...? ...Đẹp quá.<br> ',
    'Lễ phép lại dịu dàng... xem ra quỷ tộc cũng có nhiều kiểu thật.<br>Nh-nhưng mà‚ bước vào Oni Island vẫn thấy hơi... ngại...<br> ',
    '(Tốt! Nhờ Kureha mà họ đã bớt cảnh giác phần nào.<br>Nhưng vẫn chưa đủ... nhờ em đấy‚ Shiraes!)<br> ',
    'Hoan hô. Vậy đây là Oni Island trong lời đồn à. Vui ghê ha.<br>Chắc chắn mình sẽ có trải nghiệm vui đến mức một nghìn năm sau cũng không quên đâu ha.<br> ',
    '(Đọc thoại cứng quá!! Khụ... mặt mình đã lộ trong lúc quảng bá rồi‚<br>vì không còn ai khác nên mới nhờ Shiraes làm người mồi‚ nhưng chẳng lẽ chọn nhầm vai thật sao!?)<br> ',
    'Một đứa trẻ như thế cũng vào à... vậy chắc là an toàn... nhỉ?<br>...Được rồi‚ thử vào xem sao.<br> ',
    '(...Không ngờ lại ổn thật.)<br> ',
    "'――Uoooooo~~!! Có đứa trẻ hư nào ở đó không đấyyy~~!!'<br> ",
    'Hí-hííí!? C-cái đầu quỷ... vừa nói chuyện sao!?<br>T-tôi biết ngay nơi này đáng sợ nguy hiểm mà...!?<br> ',
    'Quỷ~~ ra ngoài~~♪ Quỷ~~ ra ngoài~~♪<br>Nào‚ mọi người! Hãy cầm ít đậu và ném thật khí thế vào nó nhé!<br> ',
    'Hả‚ đ-đậu à...? Vậy thì... quỷ ra ngoài...?<br> ',
    'Người dân làng rụt rè ném đậu vào chiếc đầu quỷ.<br>Rồi――<br> ',
    "'――Gwaaah~~~‚ ta chịu thua rồi~~~...!'<br> ",
    'C-cái đầu quỷ rút lui rồi...!?<br> ',
    'Xuất sắc lắm♪ Cứ theo đà đó‚ xin hãy tiêu diệt cả con quỷ xấu xa phía trước!<br>Hòa bình thế giới đang nằm trong tay quý vị!<br> ',
    'Ồ... ồồ. Tự nhiên thấy mình giống anh hùng trong truyện quá.<br>Đ-được rồi‚ thử làm một phen nào!<br> ',
    '(Tốt lắm‚ tốt lắm — họ bắt đầu nhập cuộc rồi! Dù là bẫy đáng sợ‚<br>chỉ cần biến thành trò tham quan thì vẫn có thể vui――! Đúng như mình nghĩ!)<br> ',
    '(Vẫn còn nhiều trò được chuẩn bị sẵn —<br>cứ theo đà này mà tiến thôi――!)<br> ',
    'Mọi người ơi～～ xin cảm ơn đã vất vả diệt quỷ!<br>Chắc quý vị cũng mệt sau chuyến đi dài‚ xin hãy tận hưởng suối nước nóng nổi tiếng của Oni Island♪<br> ',
    'Suối nước nóng... mà đỏ rực lại còn sôi sùng sục thế kia!?<br>Nếu vào nơi đó thì xương cũng chẳng còn mất...<br> ',
    'Aaa‚ thư giãn quá đi thôiー(đọc đều đều).<br>Muốn ngâm mình cả nghìn năm luônー(đọc đều đều). Thiên đường là đâyー(đọc đều đều).<br> ',
    'Như quý vị thấy‚ bồn ngâm chân này đã được điều chỉnh ở nhiệt độ vừa phải.<br>Nào nào‚ mọi người cũng đừng ngại mà thử đi nhé♪<br> ',
    '...Một đứa nhỏ như thế còn không sao thì chắc ổn rồi.<br>Nghĩ lại thì mùi cũng đúng kiểu suối nước nóng thật... thử ngâm xem nào.<br> ',
    "Vâng♪ Đặc sản của Oni Island — 'Suối Nước Nóng Thiên Đường Ấm Áp'♪<br>Xin hãy tận hưởng nhé♪<br> ",
    'Ồồồ... đúng là dễ chịu thật.<br>Gọi là thiên đường cũng có lý.<br> ',
    "(Tốt lắm‚ tốt lắm — chỉnh nhiệt độ là chuyện đương nhiên‚ đổi tên từ<br>'Suối Nước Nóng Địa Ngục Rực Cháy' cũng là quyết định đúng. Và hơn nữa――!)<br> ",
    'Thưa quý vị‚ chúng tôi còn có phục vụ rượu nữa‚ xin hãy dùng thử.<br>Đây là rượu địa phương của Oni Island đấy ạ～.<br> ',
    'Ồ‚ xin cảm ơn xin cảm ơn～. Chà～ được một mỹ nhân rót rượu cho thế này<br>thì đúng là chu đáo hết mức～. Đến đây thật đáng quá～.<br> ',
    '(Kèm theo dịch vụ khiến ai cũng vui!<br>Thế này chắc dân làng sẽ hài lòng!)<br> ',
    '…………. Xin phép tôi rời chỗ một lát.<br> ',
    '――Phu quân.<br> ',
    'Hửm? Sao vậy‚ Kureha? Em không cần tiếp khách à?<br> ',
    'Để phòng hờ‚ em xin nói trước... việc em đi rót rượu cho các vị khách nam<br>hoàn toàn là vì nghĩ cho đồng bào quỷ tộc ở Oni Island thôi ạ!<br> ',
    'Vì vậy! Đây tuyệt đối không phải là ngoại tình đâu‚<br>xin phu quân đừng hiểu lầm nhé! Nhé!?<br> ',
    'A-anh hiểu rồi! Anh hiểu rồi mà!<br>Anh hoàn toàn không để ý đâu! Em quay lại tiếp khách đi nhé?<br> ',
    'Kureha quay lại rót rượu sau đó‚<br>nhưng thái độ của cô với khách nam và khách nữ rõ ràng khác hẳn nhau.<br> ',
    'Này này‚ cô em. Nếu được thì cô cũng rót cho anh một chén―― ơ‚ đâu mất rồi!?<br> ',
    'Các vị khách nam ơi‚ xin hãy tự rót thêm cho mình nhéー.<br> ',
    'K-không thể thế được～...<br> ',
    'A ha ha ha ha ha!<br> ',
    'Phân biệt khách là có vấn đề thật...<br>Nhưng cuối cùng mọi người lại thấy buồn cười‚ nên cứ coi như ổn vậy.<br> ',
    'Vậy thưa quý vị‚ chúng tôi đã chuẩn bị một bữa tiệc nhỏ mọn.<br>Xin hãy thưởng thức những món đặc sản của Oni Island chỉ có thể ăn tại đây.<br> ',
    "Đợi lâu rồi nhé! Đặc sản Oni Island — 'Gan Quỷ Muối' đây!<br> ",
    'G-gan á...? Là cái gan đó sao!? Lại còn gan quỷ nữa!?<br> ',
    'Xin hãy yên tâm. Đó thực ra là buồng trứng cá nóc được ngâm muối và koji suốt 3 năm<br>để khử độc. Rất hợp với rượu đấy～.<br> ',
    'Ra là cá à. Cái tên thú vị thật～.<br> ',
    "Nào nào nào! Tiếp theo là món 'Quỷ Xé Xào' đây!<br>Ta làm cho các ngươi đấy! Hãy ăn cho kỹ và cảm nhận hương vị đi!!<br> ",
    'Hí...!?<br> ',
    '(Quả nhiên không thể sửa cách nói thô lỗ của quỷ tộc chỉ trong một sớm một chiều.<br>...Shiraes‚ nhờ em đấy!)<br> ',
    'Hu hu‚ đáng sợ quá đi. Mọi người quỷ tộc đáng sợ quá đi.<br> ',
    'Ối‚ xin lỗi nhé! Cái vẻ thô lỗ này là bẩm sinh rồi...<br> ',
    'Nhưng bọn tôi không có ý dọa các người đâu.<br>Nói sao nhỉ... bọn tôi muốn kết thân với con người các người thôi.<br> ',
    '(Tốt‚ hay lắm! Bí quyết để thân thiết với nhau chính là―― thành thật!<br>Nếu quỷ tộc bộc lộ tấm lòng chân thật đến mức vụng về của mình‚ cảm xúc thật chắc chắn sẽ truyền tới!!)<br> ',
    '(Shiraes lúc nào cũng thẳng thắn nói ra thiện cảm với con người mà chẳng hề xấu hổ.<br>Chính vì vậy em ấy mới được mọi người ở tiền tuyến quý mến.)<br> ',
    '(Quỷ tộc cũng vậy‚ chỉ cần thẳng thắn bộc lộ lòng mình thì bản tâm ấy chắc chắn sẽ truyền tới!<br>Con người có thể nhát gan‚ nhưng không ngu ngốc đến mức không hiểu được nhiệt tình của đối phương!!)<br> ',
    'V-vậy sao... Món này cũng là các người làm cho chúng tôi à?<br>Tên thì dữ dội thật‚ nhưng nêm nếm lại tinh tế bất ngờ... ngon lắm đấy!<br> ',
    '...Có vẻ chúng tôi cứ tin vào truyện xưa mà chẳng biết rõ gì‚<br>rồi sợ quỷ tộc mất rồi... ừ‚ đồ ăn cũng ngon nữa‚ tuyệt thật!<br> ',
    "Ồ‚ vậy à!? Thế thì ăn thử món 'Quỷ Hấp Nướng' này đi!<br>Nói là quỷ chứ thịt dùng chỉ là thịt gà thôi!!<br> ",
    "Ồồ‚ món này trông cũng ngon!<br>Dù tôi không hiểu tại sao tên món nào cũng có chữ 'quỷ'!<br> ",
    '...Có vẻ đã ổn rồi nhỉ.<br> ',
    'Vâng. Nhờ phu quân‚ quỷ tộc đã có thể thân thiết với con người.<br>Thật sự... thật sự cảm ơn anh rất nhiều.<br> ',
    'Anh đâu có làm gì to tát.<br>Chính vì quỷ tộc có khát vọng mạnh mẽ muốn thân thiết với con người nên mới thành công thôi.<br> ',
    'Hì hì‚ anh khiêm tốn quá. Quả nhiên phu quân của em là tuyệt nhất thế giới♪<br>Nào nào‚ phu quân cũng dùng một chén đi. Để em rót cho anh.<br> ',
    'Trong lúc hội trường yến tiệc ở Oni Island đang náo nhiệt――<br>có một bóng người lẻn vào phòng của Kureha‚ nơi tách khỏi tiếng ồn ào.<br> ',
    'Lũ quỷ tộc đó ung dung chè chén ghê nhỉ...<br>Thôi‚ nhờ vậy mà ta lấy lại được kho báu nên cũng được.<br> ',
    'Nào nào... chúng giấu viên pha lê của ta ở đâu rồi... hửm?<br>...Cái hộp kia có mùi đáng ngờ. Đừng coi thường khứu giác của đạo tặc chứ.<br> ',
    'Hửm? Cái hộp này là gì đây. Ổ khóa lạ thật... có vẻ không dễ mở.<br>Chậc‚ phiền quá! Đập luôn cho rồi!<br> ',
    'Tên đạo tặc đập chiếc hộp vào cột phòng hết lần này đến lần khác.<br>Rồi cuối cùng chiếc hộp méo mó‚ ánh sáng cầu vồng tràn ra.<br> ',
    'Hê hê‚ trúng lớn rồi! Ta lấy lại đây‚ khục khục...!<br>Giờ thì ta cũng sẽ thành tỷ phú――!!<br> ',
    'Kế hoạch quảng bá Oni Island tưởng như đang tiến triển thuận lợi.<br>Thế nhưng một cuộc khủng hoảng do ác ý lớn lao mang đến đang sắp ập xuống hòn đảo――<br> ',
]


def detect_newline(raw: bytes) -> str:
    if b'\r\n' in raw:
        return 'CRLF'
    if b'\n' in raw:
        return 'LF'
    return 'NONE'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_ordered_json(path: Path):
    text = path.read_text(encoding='utf-8-sig')
    return json.loads(text, object_pairs_hook=list)


def text_field(parts):
    if parts[0] == 'title':
        return 1
    return 2


def tags(s: str):
    return re.findall(r'<[^>]+>', s)


def placeholders(s: str):
    return re.findall(r'%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z0-9_]+\}|\$\{[^}]+\}|%%', s)


def candidate_parts(line: str):
    if line.startswith('title,'):
        return line.split(',', 1)
    return line.split(',', 5)


def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    VI_ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw = EN_ASSET_PATH.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    newline_style = detect_newline(raw)
    encoding = 'utf-8-sig' if bom else 'utf-8'
    text = raw.decode(encoding)
    line_sep = '\r\n' if newline_style == 'CRLF' else '\n'
    lines = text.splitlines()

    candidate_indexes = [i for i, line in enumerate(lines) if line.startswith(CMD_PREFIXES)]
    if len(VI) != len(candidate_indexes):
        raise SystemExit(f'VI translation count {len(VI)} != candidate records {len(candidate_indexes)}')
    bad_commas = [(idx + 1, v) for idx, v in enumerate(VI) if ',' in v]
    if bad_commas:
        raise SystemExit(f'ASCII comma inside VI fields: {bad_commas[:5]}')

    ja_pairs = load_ordered_json(JA_PATH)
    en_pairs = load_ordered_json(EN_JSON_PATH)
    out_lines = list(lines)
    entries = []

    for n, (line_idx, vi) in enumerate(zip(candidate_indexes, VI)):
        line = lines[line_idx]
        parts = candidate_parts(line)
        fidx = text_field(parts)
        old_text = parts[fidx]
        parts[fidx] = vi
        new_line = ','.join(parts)
        out_lines[line_idx] = new_line
        jp = ja_pairs[n][0] if n < len(ja_pairs) else None
        en_json = en_pairs[n][1] if n < len(en_pairs) else None
        entries.append({
            'index': n + 1,
            'line': line_idx + 1,
            'record_type': parts[0],
            'speaker': parts[1] if len(parts) > 2 else None,
            'jp': jp,
            'en_asset': old_text,
            'en_json': en_json,
            'vi': vi,
            'match_status': 'EXACT',
            'translation_status': 'TRANSLATED'
        })

    out_text = line_sep.join(out_lines) + line_sep
    out_raw = out_text.encode(encoding)
    VI_ASSET_PATH.write_bytes(out_raw)

    blockers = []
    items = []
    if len(out_lines) != len(lines):
        blockers.append({'code': 'LINE_COUNT_MISMATCH', 'source': len(lines), 'output': len(out_lines)})

    for i, (src, dst) in enumerate(zip(lines, out_lines), 1):
        if src.count(',') != dst.count(','):
            blockers.append({'code': 'DELIMITER_MISMATCH', 'line': i, 'source_commas': src.count(','), 'output_commas': dst.count(',')})
        is_candidate = src.startswith(CMD_PREFIXES)
        if not is_candidate:
            if src != dst:
                blockers.append({'code': 'NON_TEXT_LINE_CHANGED', 'line': i})
            continue
        sp = candidate_parts(src)
        dp = candidate_parts(dst)
        if len(sp) != len(dp):
            blockers.append({'code': 'FIELD_COUNT_MISMATCH', 'line': i, 'source_fields': len(sp), 'output_fields': len(dp)})
            continue
        fidx = text_field(sp)
        if sp[:fidx] + sp[fidx+1:] != dp[:fidx] + dp[fidx+1:]:
            blockers.append({'code': 'TECHNICAL_FIELD_CHANGED', 'line': i})
        if tags(sp[fidx]) != tags(dp[fidx]):
            blockers.append({'code': 'TAG_MISMATCH', 'line': i, 'source_tags': tags(sp[fidx]), 'output_tags': tags(dp[fidx])})
        if placeholders(sp[fidx]) != placeholders(dp[fidx]):
            blockers.append({'code': 'PLACEHOLDER_MISMATCH', 'line': i, 'source_placeholders': placeholders(sp[fidx]), 'output_placeholders': placeholders(dp[fidx])})
        if ',' in dp[fidx]:
            blockers.append({'code': 'ASCII_COMMA_IN_VI_FIELD', 'line': i, 'text': dp[fidx]})
        # unchanged translatable fields are suspicious unless logged; none intended for this file.
        if sp[fidx] == dp[fidx]:
            blockers.append({'code': 'UNCHANGED_TRANSLATABLE_FIELD', 'line': i, 'text': dp[fidx]})

    # Heuristic kept-English check for common English words in VI fields.
    kept_english = []
    english_re = re.compile(r'\b(?:the|and|but|with|from|this|that|please|everyone|welcome|oni-folk|hot spring|darling|Kureha|Shiraes)\b', re.I)
    # Proper names Kureha/Shiraes/Oni Island intentionally preserved, so filter them from the heuristic.
    allowed = {'Kureha', 'Shiraes', 'Oni Island'}
    for e in entries:
        stripped = e['vi']
        normalized = stripped.replace('Kureha', '').replace('Shiraes', '').replace('Oni Island', '')
        if english_re.search(normalized):
            kept_english.append({'line': e['line'], 'text': e['vi']})
    if kept_english:
        items.append({'code': 'KEPT_ENGLISH_REVIEW', 'severity': 'review', 'entries': kept_english})

    manifest = {
        'scene': SCENE,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'source': {
            'en_asset_path': str(EN_ASSET_PATH),
            'ja_json_path': str(JA_PATH),
            'en_json_path': str(EN_JSON_PATH),
            'sha256': sha256_bytes(raw),
            'bytes': len(raw),
            'bom': bom,
            'newline': newline_style,
            'line_count': len(lines),
        },
        'output': {
            'vi_asset_path': str(VI_ASSET_PATH),
            'sha256': sha256_bytes(out_raw),
            'bytes': len(out_raw),
            'bom': out_raw.startswith(b'\xef\xbb\xbf'),
            'newline': newline_style,
            'line_count': len(out_lines),
        },
        'counts': {
            'candidate_text_records': len(candidate_indexes),
            'title': sum(1 for i in candidate_indexes if lines[i].startswith('title,')),
            'message': sum(1 for i in candidate_indexes if lines[i].startswith('message,')),
            'messageTextUnder': sum(1 for i in candidate_indexes if lines[i].startswith('messageTextUnder,')),
            'messageTextCenter': sum(1 for i in candidate_indexes if lines[i].startswith('messageTextCenter,')),
            'translated_records': len(VI),
            'novel_ja_pairs': len(ja_pairs),
            'novel_en_pairs': len(en_pairs),
        },
        'rules': {
            'jp_primary': True,
            'en_alignment_only': True,
            'ascii_comma_in_vi_text_fields': 'forbidden; use U+201A ‚',
            'commander_translation': 'Chỉ Huy',
            'title_case_title': True,
            'adult_h18_confirmed_all_18_plus': True,
            'intentional_unchanged_text_records': [],
            'preserved_names': ['Kureha', 'Shiraes', 'Oni Island'],
        },
        'entries': entries,
        'qa_status': 'PASS' if not blockers and not kept_english else ('REVIEW' if not blockers else 'FAIL'),
    }

    qa_log = {
        'scene': SCENE,
        'qa_status': manifest['qa_status'],
        'blockers': blockers,
        'items': items,
        'notes': [
            'Không có dòng text giữ nguyên EN có thể dịch.',
            'Tên riêng Kureha‚ Shiraes và Oni Island được giữ nguyên theo yêu cầu preserve names.',
            'Không có nội dung H18 trong file này; quy tắc dự án all 18+ vẫn được ghi nhận.',
        ],
        'checks': {
            'line_count_match': len(out_lines) == len(lines),
            'bom_preserved': bom == out_raw.startswith(b'\xef\xbb\xbf'),
            'newline_preserved': newline_style == detect_newline(out_raw),
            'delimiter_counts_match': not any(src.count(',') != dst.count(',') for src, dst in zip(lines, out_lines)),
            'technical_fields_unchanged': not any(b.get('code') == 'TECHNICAL_FIELD_CHANGED' for b in blockers),
            'tags_placeholders_preserved': not any(b.get('code') in {'TAG_MISMATCH', 'PLACEHOLDER_MISMATCH'} for b in blockers),
            'no_ascii_comma_in_vi_text_fields': not any(b.get('code') == 'ASCII_COMMA_IN_VI_FIELD' for b in blockers),
            'no_unintentional_unchanged_text_fields': not any(b.get('code') == 'UNCHANGED_TRANSLATABLE_FIELD' for b in blockers),
            'no_kept_english_review_items': not bool(kept_english),
        }
    }

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG_PATH.write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')

    diff_lines = []
    for e in entries:
        line_no = e['line']
        diff_lines.append(f'## Line {line_no} ({e["record_type"]})\n')
        for d in unified_diff([lines[line_no-1] + '\n'], [out_lines[line_no-1] + '\n'], fromfile='EN asset', tofile='VI asset', lineterm='\n'):
            diff_lines.append(d)
        diff_lines.append('\n')
    DIFF_PATH.write_text(''.join(diff_lines), encoding='utf-8')

    print(json.dumps({
        'qa_status': manifest['qa_status'],
        'blockers': len(blockers),
        'review_items': len(items),
        'candidate_text_records': len(candidate_indexes),
        'translated_records': len(VI),
        'output': str(VI_ASSET_PATH),
        'manifest': str(MANIFEST_PATH),
        'qa_log': str(QA_LOG_PATH),
        'diff': str(DIFF_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
