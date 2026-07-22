from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10100100002'
EN_PATH = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_PATH = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
JP_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON_PATH = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST_PATH = WORK / 'manifest.json'
QA_PATH = WORK / 'qa_log.json'
DIFF_PATH = WORK / 'focused_diff.md'

TEXT_TYPES = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}')

VI_TRANSLATIONS = [
    "Cuộc Thi Săn Bắn",
    "Cuộc thi săn bắn được tổ chức tại căn cứ tiền tuyến.<br>Đây là cuộc thi săn mồi‚ chế biến món ăn rồi chấm điểm bằng hương vị.",
    "Và rồi cuộc thi săn bắn sắp bước vào cao trào lớn――<br>sự xuất hiện của nguyên liệu cao cấp Ushitoributa.",
    "Người ta nói Ushitoributa là loài vật bị đột biến bởi chướng khí của Đại Huyệt.<br>Nó là sinh vật lai có thân bò‚ chân và mũi heo‚ cùng cánh và mỏ chim.",
    "……Nếu thứ đó được phát hiện ở một nước xa Đại Huyệt<br>thì chẳng phải sẽ bị xem là quái vật sao?",
    "Điều tra đã xác nhận nó là động vật rồi nên không sao đâu!<br>Nó ngon lắm đó～♪",
    "Đó là con mồi không thể bỏ qua nếu muốn thắng……!<br>Khoan‚ tiếng kêu đang đến gần rồi.",
    "――Mò-kéc-cô-bụhiii!!!",
    "Ushitoributa cất tiếng kêu lớn rồi lao xuyên qua khu rừng.<br>Phía sau nó là rất nhiều thợ săn đang truy đuổi.",
    "Nhất định phải hạ nó!<br>Để nó chạy thoát thì coi như tuột luôn chức vô địch đấy!",
    "Khự…… nó nhanh quá! Không thể ngắm chuẩn được!",
    "Nó cứ bay bay nhảy nhảy kiểu gì ấy……!<br>Cái thân to đùng đó mà còn bay lên được bằng đôi cánh tệ hại kia‚ không thấy kỳ sao!?",
    "Thứ đó thật sự không phải quái vật à!? Này!?<br>Ma pháp của tôi chẳng trúng nổi phát nào!",
    "Wa‚ náo nhiệt ghê.<br>Không nhập cuộc ngay thì mất vui đó!",
    "Ừ‚ trông cậy vào em đấy Diana!",
    "Cứ để em! Nào……!",
    "Diana bắn một mũi tên về hướng Ushitoributa đang lao tới.<br>Phát bắn như thể nhìn thấu tương lai ấy bay thẳng về đầu con mồi――",
    "――Mò-kéc-cô-bụhihiii!!!",
    "Trượt… rồi……!?",
    "Ushitoributa lách mình trơn tuột như trượt đi và né được mũi tên.",
    "Vừa rồi là sao……?<br>Diana đã ngắm hoàn hảo mà……!",
    "Một… lần nữa……!",
    "Mũi tên được bắn ra lần nữa vẫn bị nó né bằng chuyển động kỳ lạ.<br>Kéo theo đám thợ săn truy đuổi‚ Ushitoributa biến mất vào trong rừng.",
    "Để nó chạy mất rồi……<br>Chuyện gì vậy‚ anh không thấy em bắn trượt mà……",
    "Em nghĩ chắc là cùng nguyên lý với loài chim.<br>Nó nương theo luồng gió rồi nhẹ nhàng né mũi tên.",
    "……Cái thân khổng lồ đó với đôi cánh bé tí‚ lại còn đang lao trên mặt đất nữa.<br>Sao nó lại né theo nguyên lý của chim được chứ……",
    "Có lẽ dù em bắn bao nhiêu mũi tên cũng không trúng được.<br>Nhưng mà vẫn còn cách khác đó.",
    "Ồ? Cách gì vậy?",
    "Một vũ khí đáng tin cậy khác của thợ săn!<br>――Bẫy đó!",
    "Được rồi.<br>Vậy là đã đặt xong hết rồi nhỉ.",
    "Dấu móng còn lại trên mặt đất…… đây là dấu chân của Ushitoributa à.<br>Phân tích kỹ cả tuyến di chuyển như vậy‚ đúng là thợ săn hạng nhất.",
    "Săn đâu chỉ là đuổi theo rồi bắn tên thôi mà♪",
    "Bình thường thì phải đợi cả đêm‚ nhưng có vẻ Ushitoributa đang chạy khắp nơi.<br>Theo dự đoán của em‚ chắc sắp đến lúc nó đi ngang qua chiếc bẫy đặt đầu tiên rồi.",
    "Được rồi‚ đi xem tình hình nào.<br>Nếu không nhanh lên thì có thể bị thợ săn khác hạ mất!",
    "Hy vọng người săn được nó là một thợ săn biết nấu món thật ngon～.",
    "Chúng ta! Mới là người săn nó!!!",
    "Em đã đặt ở đây‚ nhưng mà…… đây là……",
    "Cái bẫy đã bị tháo ra và nằm lăn trên đất…… bên này cũng vậy……",
    "Bẫy kẹp của Diana đã bị gỡ và ném xuống đất.<br>Rõ ràng đây không phải do Ushitoributa mà là do con người làm.",
    "……Có thể chỉ là trùng hợp thôi.<br>Thử đến cái bẫy tiếp theo nào!",
    "À‚ ừ……",
    "Trái với kỳ vọng của hai người‚ cả hố bẫy lẫn bẫy vướng chân<br>đều đã bị lấp‚ bị tháo và phá hỏng.",
    "……Cái tiếp theo là cuối cùng rồi.",
    "Mong là nó mắc bẫy……",
    "Khi đến gần vị trí chiếc bẫy cuối cùng‚ họ nghe thấy tiếng nói chuyện hốt hoảng.<br>Ở đó có hai thợ săn đang loay hoay đụng vào cái bẫy.",
    "Này‚ tháo nhanh lên!<br>Mày còn lề mề cái gì hả!",
    "Nhưng mà đại ca ơi‚ cái này được đặt chắc cực kỳ luôn ấy.<br>Chắc chắn là do thợ săn cao tay làm đấy ạ!",
    "Đồ ngu!<br>Chính vì thế mới phải phá chứ!",
    "Là do bọn bay làm hảảảảảảả!",
    "Ghêêê‚ Chỉ Huy!?<br>Cả Diana nữa…… bẫy của bọn mày à!",
    "Đúng rồi đó～.<br>Nè‚ sao các anh lại phá bẫy vậy?",
    "Hả? Còn phải hỏi sao!<br>Để bọn tao giành chức vô địch chứ sao!",
    "Cản trở đâu có phạm luật! Đừng trách bọn tao!<br>Nào‚ đi thôi!",
    "Vâng‚ đại ca!",
    "Bọn chúng……!<br>Thủ đoạn hèn hạ gì thế này!",
    "……Chỉ để… thắng thôi sao……?",
    "Muốn làm món ngon rồi ăn cùng mọi người.<br>Lẽ ra mục đích của chúng ta phải giống nhau‚ vậy sao họ lại đi cản trở chứ.",
    "Có thể chỉ một người lấy được con mồi.<br>Nhưng trong bãi săn nguy hiểm‚ chỉ những thợ săn mới có thể giúp đỡ lẫn nhau.",
    "Làm khó người khác như vậy<br>thì đến lúc bản thân gặp khó cũng sẽ không còn ai giúp nữa.",
    "Mọi người cùng vui với nhau đi mà.<br>Cùng trải qua thời gian vui vẻ rồi ăn chung một món đi.",
    "Nếu vậy thì chắc sẽ không ai nghĩ đến chuyện cản trở người khác nữa……<br>Đúng không‚ Chỉ Huy?",
    "À‚ ừ…… đúng… vậy.<br>Anh cũng nghĩ thế‚ ừm……",
    "Không hề có bầu không khí đồng ý chút nào!<br>Sao vậy!? Anh không muốn cùng ăn vui vẻ với mấy người đó sao!?",
    "Ngược lại anh còn muốn gọi chúng ra sau khi cuộc thi kết thúc<br>rồi chất vấn xem dám có thái độ đó với cấp trên à……",
    "Không được dùng vị trí Chỉ Huy như thế chứ!?<br>Với lại đừng để kết quả cuộc thi ám ảnh sau này nữa!",
    "Đúng vậy.<br>Hết cách rồi…… anh sẽ th… tha… tha thứ cho bọn chúng!",
    "Anh do dự dữ quá……<br>Anh giận thật rồi nhỉ‚ Chỉ Huy……",
    "Đương nhiên rồi!<br>Chúng phá hỏng những cái bẫy Diana đặt bằng trí tuệ và kỹ thuật mà……!",
    "Nhưng dù vậy anh vẫn sẽ tha!<br>Vì đó mới là cuộc thi vui vẻ đối với Diana đúng không?",
    "……Ừ!<br>Thật sự may quá vì anh là cộng sự của em……",
    "Nhưng em không nghĩ ra cách nào nữa rồi～.<br>Lần này có lẽ hết cách thật……",
    "Anh ở đây là vì lúc này mà‚ để anh thử nghĩ xem.<br>Một cách khác…… quả nhiên mũi tên sét kia là chìa khóa……",
    "Anh không cần cố quá đâu?<br>Beast Vulture và Flare Fox cũng ngon mà.",
    "Sau đó mình hái ít nấm rồi về căn cứ đi.<br>Em sẽ chuẩn bị món cực kỳ ngon cho anh♪",
    "Cũng không tệ…… hửm‚ nấm……?",
    "Ừ‚ dù sao em cũng là thợ săn mà.<br>Nhân lúc đặt bẫy‚ em cũng đã xem qua chỗ nấm ngon mọc thành cụm rồi.",
    "Nấm…… nấm! Ra vậy‚ chính là nó!<br>Làm được đấy Diana! Cuộc săn của chúng ta vẫn chưa kết thúc!",
    "S… sao cơ……?",
    "――Một lúc sau<br>Diana ở một mình bên mép nước‚ nâng cao sự tập trung.",
    "Chỉ Huy đã bảo cứ để anh ấy lo.<br>Nhưng anh ấy là tay mơ trong chuyện săn bắn‚ liệu có suôn sẻ không nhỉ……",
    "Nhưng mình có thể tin.<br>Không‚ mình muốn tin anh ấy.",
    "Chỉ Huy thật kỳ lạ.<br>Cả những điều khổ sở lẫn buồn bã‚ khi ở cùng anh thì tất cả đều trở thành chuyện vui.",
    "Ngay lúc này cũng vậy. Chờ đợi thì bất an và lo lắng……<br>nhưng mình lại háo hức vì chắc chắn sẽ có chuyện vui nào đó xảy ra!",
    "Ngay sau khi cô nói vậy.<br>Một tiếng kêu lớn vang lên từ trong rừng.",
    "――Mò-kéc-cô-bụhiii!!!",
    "……Tới rồi!",
    "Dianaaaaa!<br>Chuẩn bị bắắắắn!",
    "<user> lao ra từ sâu trong rừng<br>ôm đầy nấm trước ngực và kéo theo Ushitoributa――",
    "Dùng nấm để dẫn dụ……?<br>Ushitoributa sao?",
    "Ừ. Nó pha trộn đủ thứ nhưng mũi là của heo đúng không?<br>Heo là loài có khứu giác nhạy‚ rất giỏi tìm thức ăn.",
    "Ở một nước nào đó còn có chuyện để heo đi tìm nấm nữa……<br>Mà dù không vậy‚ nấm cũng là món heo thích.",
    "……Bò‚ chim‚ heo đều cần ăn thường xuyên.<br>Ushitoributa bị thợ săn đuổi chắc hẳn đang đói……",
    "Nếu ôm nhiều nấm như vậy‚ nó hẳn sẽ tự tiến lại gần.<br>Còn lại thì…… tin vào Diana.",
    "Dẫn dụ Ushitoributa bằng cách như thế này……!<br>Anh đúng là người thú vị thật đó‚ Chỉ Huy!",
    "Theo tao nào‚ cứ thế‚ cứ thế……!<br>Được rồi!",
    "<user> ném nấm xuống nước.<br>Ushitoributa đuổi theo nấm và bước chân xuống nước.",
    "――Ngay lúc này!",
    "Ừ! Em sẽ dùng mũi tên của mình đáp lại kỳ vọng của anh!<br>Xin hãy trúng…… Mũi Tên Tê Liệt!!!",
    "Mũi tên mang sấm sét lao xuyên không trung về phía thân Ushitoributa.<br>Thế nhưng――",
    "――Mò-kéc-cô-bụh!?",
    "Dù chân đang ngập nước‚ chuyển động của nó vẫn không hề kém đi.<br>Ushitoributa lách mình và né được mũi tên.",
    "Có né cũng vô ích thôi!<br>Nào‚ nổ tung đi!",
    "Mũi tên sét cắm xuống mặt nước và bùng nổ ánh chớp.<br>Sấm sét lan qua nước rồi phóng vào đôi chân trước ướt đẫm của Ushitoributa.",
    "――Mò-kéc-cô-bụhiiii!!!",
    "Con mồi bị tê liệt và dừng hẳn lại.<br>Dáng vẻ nó phơi ra trước mặt thợ săn quá mức không phòng bị.",
    "Kết thúc ở đây thôi……!",
    "Đôi cánh tê liệt không thể bắt lấy gió.<br>Lần này‚ mũi tên của Diana cuối cùng cũng cắm vào Ushitoributa.",
    "Kéc-cô-bụh-mòoooo――",
    "Ushitoributa đổ sụp xuống không còn sức.<br>Thân hình khổng lồ ấy không hề nhúc nhích thêm một chút nào nữa.",
    "Làm… được rồi……?",
    "Ừ! Chúng ta đã săn được nó rồi đó‚ Chỉ Huy!",
    "Ô‚ ôôôôô!<br>Làm được rồi‚ Diana!",
    "Alicia còn dám nói anh là gánh nặng!<br>Cuộc thi này thuộc về chúng ta rồi!",
    "Ừ! Hãy đãi mọi người<br>món ăn ngon tuyệt nhất nào!",
    "……À‚ ừ‚ phải……<br>Đúng vậy! Chính là thế!",
    "Hai người mang nguyên liệu cao cấp Ushitoributa quay về căn cứ.<br>Trọng lượng của nó nặng đến mức cả hai cùng khiêng cũng rất vất vả――",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def newline_style(raw: bytes) -> str:
    if b'\r\n' in raw:
        return 'CRLF'
    if b'\n' in raw:
        return 'LF'
    return 'NONE'


def tags(text: str):
    return sorted(TAG_RE.findall(text))


def placeholders(text: str):
    return sorted(PH_RE.findall(text))


def text_idx(record_type: str) -> int:
    return 1 if record_type == 'title' else 2


def parse_pairs(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=list)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    raw = EN_PATH.read_bytes()
    src_text = raw.decode('utf-8-sig')
    had_bom = raw.startswith(b'\xef\xbb\xbf')
    nl = '\r\n' if b'\r\n' in raw else '\n'
    lines = src_text.splitlines()
    endings = src_text.splitlines(True)

    candidates = []
    out_lines = list(lines)
    for line_no, line in enumerate(lines, 1):
        rec_type = line.split(',', 1)[0] if ',' in line else line
        if rec_type in TEXT_TYPES:
            parts = line.split(',')
            idx = text_idx(rec_type)
            if len(parts) <= idx:
                raise SystemExit(f'Bad text record at line {line_no}')
            candidates.append((line_no, rec_type, idx, parts[idx]))

    if len(candidates) != len(VI_TRANSLATIONS):
        raise SystemExit(f'translation count mismatch: {len(VI_TRANSLATIONS)} vs candidates {len(candidates)}')

    for (line_no, rec_type, idx, old_field), vi in zip(candidates, VI_TRANSLATIONS):
        if ',' in vi:
            raise SystemExit(f'ASCII comma in VI translation for candidate line {line_no}: {vi}')
        if tags(old_field) != tags(vi):
            raise SystemExit(f'Tag mismatch in translation at line {line_no}: {tags(old_field)} vs {tags(vi)}')
        if placeholders(old_field) != placeholders(vi):
            raise SystemExit(f'Placeholder mismatch in translation at line {line_no}: {placeholders(old_field)} vs {placeholders(vi)}')
        parts = out_lines[line_no - 1].split(',')
        parts[idx] = vi
        out_lines[line_no - 1] = ','.join(parts)

    out_text = nl.join(out_lines)
    if src_text.endswith(('\r\n', '\n')):
        out_text += nl
    out_raw = out_text.encode('utf-8')
    if had_bom:
        out_raw = b'\xef\xbb\xbf' + out_raw
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_PATH.write_bytes(out_raw)

    vi_text = out_raw.decode('utf-8-sig')
    vi_lines = vi_text.splitlines()
    blockers = []
    warnings = []
    delimiter_mismatches = []
    tech_mismatches = []
    tag_mismatches = []
    placeholder_mismatches = []
    ascii_comma_lines = []
    unchanged_text_lines = []

    if len(lines) != len(vi_lines):
        blockers.append({'type': 'LINE_COUNT_MISMATCH', 'en': len(lines), 'vi': len(vi_lines)})
    if had_bom != out_raw.startswith(b'\xef\xbb\xbf'):
        blockers.append({'type': 'BOM_CHANGED'})
    if newline_style(raw) != newline_style(out_raw):
        blockers.append({'type': 'NEWLINE_CHANGED', 'en': newline_style(raw), 'vi': newline_style(out_raw)})

    candidate_counts = {k: 0 for k in TEXT_TYPES}
    for line_no, old, new in zip(range(1, len(lines) + 1), lines, vi_lines):
        if old.count(',') != new.count(','):
            delimiter_mismatches.append(line_no)
        old_type = old.split(',', 1)[0] if ',' in old else old
        if old_type in TEXT_TYPES:
            candidate_counts[old_type] += 1
            if old == new:
                unchanged_text_lines.append(line_no)
            idx = text_idx(old_type)
            old_parts = old.split(',')
            new_parts = new.split(',')
            if old_parts[:idx] + old_parts[idx+1:] != new_parts[:idx] + new_parts[idx+1:]:
                tech_mismatches.append(line_no)
            old_field = old_parts[idx]
            new_field = new_parts[idx]
            if tags(old_field) != tags(new_field):
                tag_mismatches.append(line_no)
            if placeholders(old_field) != placeholders(new_field):
                placeholder_mismatches.append(line_no)
            if ',' in new_field:
                ascii_comma_lines.append(line_no)

    if delimiter_mismatches:
        blockers.append({'type': 'DELIMITER_MISMATCH', 'lines': delimiter_mismatches})
    if tech_mismatches:
        blockers.append({'type': 'TECH_FIELD_MISMATCH', 'lines': tech_mismatches})
    if tag_mismatches:
        blockers.append({'type': 'TAG_MISMATCH', 'lines': tag_mismatches})
    if placeholder_mismatches:
        blockers.append({'type': 'PLACEHOLDER_MISMATCH', 'lines': placeholder_mismatches})
    if ascii_comma_lines:
        blockers.append({'type': 'ASCII_COMMA_IN_TEXT_FIELD', 'lines': ascii_comma_lines})
    if unchanged_text_lines:
        blockers.append({'type': 'UNCHANGED_TEXT_RECORDS', 'lines': unchanged_text_lines})

    # Focused diff for translatable lines only.
    old_focus = []
    new_focus = []
    for line_no, rec_type, idx, _ in candidates:
        old_focus.append(f'{line_no}: {lines[line_no - 1]}')
        new_focus.append(f'{line_no}: {vi_lines[line_no - 1]}')
    diff = difflib.unified_diff(old_focus, new_focus, fromfile=str(EN_PATH), tofile=str(VI_PATH), lineterm='')
    DIFF_PATH.write_text('# Focused Diff: hmn_10100100002\n\n```diff\n' + '\n'.join(diff) + '\n```\n', encoding='utf-8')

    jp_pairs = parse_pairs(JP_PATH)
    en_pairs = parse_pairs(EN_JSON_PATH)
    entries = []
    for i, ((line_no, rec_type, idx, src), vi) in enumerate(zip(candidates, VI_TRANSLATIONS)):
        jp_ref = None
        if i == 0:
            jp_ref = 'タイトル'
        else:
            # Asset order is authoritative; JSON source lacks one repeated animal-cry record in the second half.
            matches = [k for k, _v in jp_pairs if k == src]
            jp_ref = matches[0] if matches else src
        entries.append({
            'candidate_index': i,
            'line': line_no,
            'record_type': rec_type,
            'source_text': src,
            'jp_primary': jp_ref,
            'vi': vi,
            'match_status': 'EXACT' if any(k == src for k, _v in jp_pairs) or i == 0 else 'ASSET_DIRECT_JP',
            'translation_status': 'TRANSLATED',
        })

    qa_status = 'PASS' if not blockers else 'FAIL'
    qa = {
        'scene': SCENE,
        'qa_status': qa_status,
        'blockers': blockers,
        'warnings': warnings,
        'candidate_counts': candidate_counts,
        'translatable_records': len(candidates),
        'translated_records': len(candidates) - len(unchanged_text_lines),
        'line_count': {'source': len(lines), 'output': len(vi_lines), 'match': len(lines) == len(vi_lines)},
        'bom': {'source': had_bom, 'output': out_raw.startswith(b'\xef\xbb\xbf'), 'match': had_bom == out_raw.startswith(b'\xef\xbb\xbf')},
        'newline': {'source': newline_style(raw), 'output': newline_style(out_raw), 'match': newline_style(raw) == newline_style(out_raw)},
        'delimiter_mismatches': delimiter_mismatches,
        'technical_field_mismatches': tech_mismatches,
        'tag_mismatches': tag_mismatches,
        'placeholder_mismatches': placeholder_mismatches,
        'ascii_comma_in_vi_text_lines': ascii_comma_lines,
        'unchanged_text_lines': unchanged_text_lines,
        'adult_content': {'present': False, 'all_characters_confirmed_18_plus_by_user_context': True},
        'notes': [
            'JP/asset text is primary; en.json values are identical/blank in this source snapshot and used only as alignment artifact.',
            'Asset contains one repeated Ushitoributa cry record not represented as a distinct novel JSON key; translated directly from asset JP and logged as ASSET_DIRECT_JP if unmatched.',
            'Diana voice: playful bokukko; localized to em–anh with Chỉ Huy for 司令官くん where natural.',
        ],
    }
    QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

    manifest = {
        'scene': SCENE,
        'status': qa_status,
        'source_paths': {
            'jp_json': str(JP_PATH),
            'en_json': str(EN_JSON_PATH),
            'en_asset': str(EN_PATH),
        },
        'output_paths': {
            'vi_asset': str(VI_PATH),
            'manifest': str(MANIFEST_PATH),
            'qa_log': str(QA_PATH),
            'focused_diff': str(DIFF_PATH),
            'script': str(Path(__file__)),
        },
        'hashes': {
            'jp_json_sha256': hashlib.sha256(JP_PATH.read_bytes()).hexdigest(),
            'en_json_sha256': hashlib.sha256(EN_JSON_PATH.read_bytes()).hexdigest(),
            'en_asset_sha256': sha256_bytes(raw),
            'vi_asset_sha256': sha256_bytes(out_raw),
        },
        'source_properties': {
            'bytes': len(raw),
            'bom': had_bom,
            'newline': newline_style(raw),
            'line_count': len(lines),
        },
        'output_properties': {
            'bytes': len(out_raw),
            'bom': out_raw.startswith(b'\xef\xbb\xbf'),
            'newline': newline_style(out_raw),
            'line_count': len(vi_lines),
        },
        'candidate_counts': candidate_counts,
        'translatable_records': len(candidates),
        'translated_records': len(candidates) - len(unchanged_text_lines),
        'entries': entries,
        'qa': qa,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'scene': SCENE, 'qa_status': qa_status, 'output': str(VI_PATH), 'manifest': str(MANIFEST_PATH), 'qa_log': str(QA_PATH), 'focused_diff': str(DIFF_PATH)}, ensure_ascii=False, indent=2))
    return 0 if qa_status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
