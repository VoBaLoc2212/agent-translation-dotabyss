# -*- coding: utf-8 -*-
"""Generate Vietnamese translation for hmn_10130100001 asset.
JP is primary; EN asset is structure authority.
"""
from __future__ import annotations

import json
import hashlib
import difflib
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10130100001'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JP_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10130100001_full'
MANIFEST = WORK/'manifest.json'
QA_LOG = WORK/'qa_log.json'
DIFF = WORK/'focused_diff.md'

COMMANDS = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

VI_TEXTS = [
    "Tiêu Đề",
    "――Cốc cốc.<br> ",
    "Mời vào.<br> ",
    "Xin phép nhé‚ Chỉ Huy.<br> ",
    "Thật ra tôi có chuyện muốn bàn với cậu...<br> ",
    "Có chuyện gì? Trông cô nghiêm trọng thế. Nếu là xin thêm<br>ngân sách tháng này thì dĩ nhiên tôi không duyệt đâu.<br> ",
    "Không phải chuyện tiền bạc! Với lại cái gì mà \"dĩ nhiên không duyệt\" chứ!?<br> ",
    "Tự nhớ lại hành động thường ngày của cô đi.<br> ",
    "Cô có biết thường ngày chúng tôi đã đổ bao nhiêu<br>tiền vào nghiên cứu của cô không... thật là.<br> ",
    "À... không... ừm... phải... chuyện đó thì...<br> ",
    "T-thử sai là chuyện luôn đi kèm với nghiên cứu mà!<br>Nên xin thêm ngân sách cũng đành chịu thôi!<br> ",
    "Mà một kẻ tầm thường như cậu chắc chắn không thể hiểu nổi đâu nhỉ♪<br> ",
    "Ra vậy‚ ra vậy. Tức là cô chen vào lịch bận rộn<br>chỉ để đến khích tôi thôi à.<br> ",
    "Được rồi‚ về đi. Tôi không bận bằng cô‚ nhưng cũng có việc của mình.<br> ",
    "Ưeeeeee!? X-x-xin lỗi mà!<br> ",
    "Tôi thật sự có chuyện muốn bàn mà! Làm ơn nghe tôi nói đi!<br> ",
    "Được rồi‚ được rồi... thế nội dung cần bàn là gì?<br> ",
    "Ư... ư-ừm... Có lẽ chuyện này nghe hơi khó tin‚ nhưng...<br> ",
    "Thật ra... mỗi khi làm thí nghiệm‚<br>tôi luôn tạo ra thứ dâm đãng nào đó.<br> ",
    "...Hửm? Cô vừa nói gì? Xin lỗi‚ nói lại lần nữa được không?<br> ",
    "Ưư... t-thì tôi đã nói là...!<br> ",
    "Dù làm gì... tôi cũng chỉ tạo ra toàn thứ dâm đãng thôi!<br> ",
    "V-vậy à. Không... thế là sao?<br> ",
    "Thứ dâm đãng... ví dụ cô đã tạo ra những gì?<br> ",
    "Hôm trước‚ tôi có cho Chỉ Huy xem thuốc tăng cường sinh lực đúng không?<br> ",
    "Thứ thuốc đó...<br>thật ra vốn là sản phẩm khi tôi định chế thuốc trường sinh bất tử...<br> ",
    "Lúc đó cô còn vênh mặt nói 'Nó có hiệu quả ghê gớm lắm!'‚<br>vậy ra nó là thành quả ngoài ý muốn à...<br> ",
    "Ự. T-thì... trước mắt cứ nghe tiếp đã.<br> ",
    "Một ngày khác... lẽ ra tôi đã tạo một ma pháp trận thổi bay mệt mỏi‚<br>nhưng chẳng hiểu sao nó chỉ thổi bay mỗi quần áo của tôi...<br> ",
    "Đúng lúc toàn bộ quần áo khác đều đang đem giặt...<br>nên tôi đành phải đi quanh trong bộ đồ ngủ...!<br> ",
    "À‚ ra đó là lý do có hôm cô được mọi người trong căn cứ<br>âu yếm quá mức. Cô bị vây kín nên tôi không thấy cô mặc gì.<br> ",
    "Â-âu yếm gì chứ... đừng nói như tôi là chó mèo vậy!<br> ",
    "...Hửm? Khoan đã... nghe vậy thì chuyện hôm qua cũng...<br> ",
    "Ự. Ưưưư...<br> ",
    "Báo cáo cũng tổng hợp xong rồi‚ đọc sách một chút vậy――<br> ",
    "Bùm!<br> ",
    "Ưnyaaaa!?<br> ",
    "Khói hồng từ phòng nghiên cứu...? Với lại giọng vừa rồi... là Frederica sao!?<br> ",
    "Chờ đó‚ tôi đến ngay!!<br> ",
    "Hộc‚ hộc... Frederica‚ cô ổn chứ!?<br> ",
    "Ha hi...♡ e-em ổn...♡<br> ",
    "Không‚ trông cô chẳng ổn chút nào.<br>Chờ đó‚ tôi đưa cô tới phòng y tế ngay...<br> ",
    "E-em thật sự ổn mà...♡<br> ",
    "Với lại... chuyện đó... bị bế kiểu công chúa thế này... ừm...<br>nhiều thứ... nguy hiểm lắm... a‚ á‚ aaaa...♡<br> ",
    "Ưnyaaaaaa～～～～...♡<br> ",
    "Rốt cuộc chúng ta không tới phòng y tế... ra vậy‚<br>chuyện đó cũng chỉ là do thuốc kích dục làm cô hưng phấn thôi à.<br> ",
    "Đ-đừng nói huỵch toẹt ra như thế!<br> ",
    "Nhưng... tôi xin lỗi vì đã gây phiền phức... ưư.<br> ",
    "Chuyện cỡ đó đừng bận tâm. Dù vậy... hiện tượng này lạ thật.<br> ",
    "Ưư～... sao mọi chuyện lại thành ra thế này chứ...<br>Tôi chỉ một lòng dốc sức nghiên cứu thôi mà...<br> ",
    "Cô không nhớ manh mối gì sao?<br> ",
    "Hoàn toàn không.<br>Trước khi đến đây tôi cũng đã tra đủ loại sách rồi‚ nhưng...<br> ",
    "Tôi còn chẳng tìm thấy thứ gì gần giống tình huống kỳ quặc này... haiz.<br> ",
    "Ừm. Nếu vậy...<br>hỏi sư phụ giả kim thuật của cô thì biết đâu sẽ hiểu ra gì đó?<br> ",
    "Ưể!? H-hỏi sư phụ á... không không! Tuyệt đối không được!<br> ",
    "Hửm? Sao cô lại ghét đến mức đó?<br> ",
    "...Trước khi đến đây‚ cậu biết tôi từng sống ở Eldorana đúng không?<br> ",
    "Đúng vậy. Giả kim thuật sư thường sống ở Perdion nên tôi vẫn thấy lạ.<br> ",
    "Lý do tôi sống ở Eldorana chỉ có một...<br> ",
    "Vì tôi muốn rời xa sư phụ... rời xa tên đó càng sớm càng tốt～!<br> ",
    "Hửm...? Đã là sư phụ thì hẳn cô đã cùng người đó<br>trải qua kha khá năm tháng rồi nhỉ? Sao lại thế?<br> ",
    "Chính vì đã cùng trải qua kha khá năm tháng nên mới vậy đó～!<br>Không được là không được! Tuyệt đối không được!!<br> ",
    "Ưư～... chỉ nhớ lại thôi đầu tôi đã～...!<br>Khưư... thôi đi‚ biến khỏi đầu ta đi...!<br> ",
    "Rốt cuộc cô đã trải qua những gì vậy...<br>Dù thế‚ hiện giờ đâu còn cách nào khác?<br> ",
    "Đ-đúng là... chuyện đó thì đúng... ưgưgư... nhưng mà...<br> ",
    "Tôi hiểu là cô ghét đến chết rồi... nhưng cứ thế này thì sớm muộn gì<br>phòng nghiên cứu của cô cũng ngập tràn toàn thứ dâm đãng đấy?<br> ",
    "Hừưưưーー! Chuyện đó... quá sức kinh khủngーーーー!!<br> ",
    "Nhưng đến chỗ sư phụ thì... cũng cực kỳ vô tận kinh khủng...!<br> ",
    "Ưgưgư... dù vậy... không thể tạo ra thành quả nghiên cứu...<br>mới là điều tôi ghét nhất...<br> ",
    "Yên tâm đi. Tôi cũng sẽ đi cùng cô.<br> ",
    "Thật không!? Chỉ Huy cũng đi cùng sao!! Vậy thì cực kỳーーー giúp tôi nhiều lắm!!<br> ",
    "Lúc khẩn cấp‚ càng nhiều người để đập tên đó càng tốt mà♪<br>Ôi đúng là cứu tinh!<br> ",
    "...Vừa rồi cô nói 'đập' à...?<br> ",
    "Hửm? Tôi nói mà?<br> ",
    "Tôi đã hy vọng mình nghe nhầm đấy...<br> ",
    "Nhà sư phụ tôi nằm ở một nơi hẻo lánh của Perdion.<br>Nói cách khác là ông ta sống như trong chỗ ẩn cư vậy.<br> ",
    "Thay lời chào hỏi... trước hết bắt đầu bằng việc dọa nhẹ bằng thuốc nổ nhé♪<br> ",
    "Khoan khoan khoan. Cô định phát động chiến tranh à?<br> ",
    "Tôi ghét đến mức đó‚ và làm đến mức đó cũng hoàn toàn<br>không thành vấn đề đâu... gặp rồi cậu sẽ hiểu...<br> ",
    "V-vậy à... Được rồi‚ trước tiên cứ tới đó xem sao.<br> ",
]


def raw_info(path: Path):
    data = path.read_bytes()
    bom = data.startswith(b'\xef\xbb\xbf')
    newline = 'CRLF' if b'\r\n' in data else 'LF'
    return {
        'path': str(path),
        'sha256': hashlib.sha256(data).hexdigest(),
        'bytes': len(data),
        'bom_utf8': bom,
        'newline': newline,
        'line_count_splitlines': len(data.decode('utf-8-sig').splitlines()),
        'trailing_newline': data.endswith(b'\n'),
    }


def split_lines_preserve(text: str):
    return text.splitlines(keepends=True)


def line_body_newline(line: str):
    if line.endswith('\r\n'):
        return line[:-2], '\r\n'
    if line.endswith('\n'):
        return line[:-1], '\n'
    return line, ''


def text_index_for_fields(fields):
    cmd = fields[0]
    if cmd == 'title':
        return 1
    if cmd in {'message', 'messageTextUnder', 'messageTextCenter'}:
        return 2
    raise ValueError(cmd)


def tag_counts(s: str):
    return re.findall(r'<[^>]+>', s)


def placeholder_counts(s: str):
    return re.findall(r'%(?:user|s|d)|\{\d+\}|\$\{[^}]+\}|\\[nrt]', s)


def has_ascii_comma_in_text(s: str) -> bool:
    return ',' in s


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    src_raw = EN_ASSET.read_bytes()
    src_text = src_raw.decode('utf-8-sig')
    lines = split_lines_preserve(src_text)
    candidate_positions = []
    src_texts = []
    counts_by_cmd = {c: 0 for c in COMMANDS}
    for i, line in enumerate(lines):
        body, nl = line_body_newline(line)
        if not body:
            continue
        fields = body.split(',')
        cmd = fields[0]
        if cmd in COMMANDS:
            ti = text_index_for_fields(fields)
            candidate_positions.append((i, fields, ti, nl))
            src_texts.append(fields[ti])
            counts_by_cmd[cmd] += 1
    assert len(candidate_positions) == len(VI_TEXTS), (len(candidate_positions), len(VI_TEXTS))

    out_lines = list(lines)
    qa_errors = []
    records = []
    for n, ((i, fields, ti, nl), vi) in enumerate(zip(candidate_positions, VI_TEXTS), start=1):
        old_fields = list(fields)
        old_text = old_fields[ti]
        if has_ascii_comma_in_text(vi):
            qa_errors.append({'record': n, 'line': i+1, 'error': 'ascii_comma_in_vi_text', 'text': vi})
        if tag_counts(old_text) != tag_counts(vi):
            qa_errors.append({'record': n, 'line': i+1, 'error': 'tag_mismatch', 'old': tag_counts(old_text), 'new': tag_counts(vi)})
        if placeholder_counts(old_text) != placeholder_counts(vi):
            qa_errors.append({'record': n, 'line': i+1, 'error': 'placeholder_mismatch', 'old': placeholder_counts(old_text), 'new': placeholder_counts(vi)})
        new_fields = list(fields)
        new_fields[ti] = vi
        old_delims = ','.join(old_fields).count(',')
        new_body = ','.join(new_fields)
        if new_body.count(',') != old_delims:
            qa_errors.append({'record': n, 'line': i+1, 'error': 'delimiter_count_changed', 'old': old_delims, 'new': new_body.count(',')})
        out_lines[i] = new_body + nl
        records.append({
            'record_index': n,
            'line': i+1,
            'command': fields[0],
            'speaker': fields[1] if fields[0] != 'title' and len(fields) > 1 else None,
            'status': 'TRANSLATED',
            'source_en': old_text,
            'vi': vi,
        })

    out_text = ''.join(out_lines)
    # Preserve BOM exactly.
    out_bytes = (b'\xef\xbb\xbf' if src_raw.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8')
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_bytes)

    vi_raw = VI_ASSET.read_bytes()
    structural = {
        'source': raw_info(EN_ASSET),
        'output': raw_info(VI_ASSET),
        'jp_json': raw_info(JP_JSON),
        'en_json': raw_info(EN_JSON),
        'candidate_counts': counts_by_cmd,
        'candidate_total': len(candidate_positions),
        'vi_text_count': len(VI_TEXTS),
        'line_count_match': len(src_text.splitlines()) == len(vi_raw.decode('utf-8-sig').splitlines()),
        'delimiter_line_counts_match': all(
            line_body_newline(a)[0].count(',') == line_body_newline(b)[0].count(',')
            for a, b in zip(lines, split_lines_preserve(vi_raw.decode('utf-8-sig')))
        ),
        'qa_errors': qa_errors,
    }
    structural['status'] = 'PASS' if not qa_errors and structural['line_count_match'] and structural['delimiter_line_counts_match'] else 'FAIL'

    qa = {
        'scene': SCENE,
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'adult_content_rule': 'All characters confirmed 18+ by project context; H18/adult-adjacent lines translated normally while preserving source tone/consent.',
        'translation_basis': 'JP ja.json primary; en.json and EN asset used for ordered alignment; EN asset is authoritative for command order and tag counts.',
        'structural_qa': structural,
        'linguistic_qa': {
            'status': 'PASS',
            'notes': [
                'Frederica/フレデリカ kept as speaker and charaload name because no explicit VI name mapping was provided.',
                'Commander/司令官 translated as Chỉ Huy in dialogue text.',
                'Frederica uses casual tôi/cậu toward Commander in this early comedic scientist scene; Commander generally uses tôi/cô.',
                'ASCII comma inside Vietnamese text fields avoided; U+201A used where a comma-like pause is needed.',
            ],
            'unresolved_items': [],
        },
        'records': records,
    }
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

    diff = difflib.unified_diff(
        src_text.splitlines(),
        vi_raw.decode('utf-8-sig').splitlines(),
        fromfile=str(EN_ASSET),
        tofile=str(VI_ASSET),
        lineterm='',
    )
    DIFF.write_text('# Focused Diff: hmn_10130100001\n\n```diff\n' + '\n'.join(diff) + '\n```\n', encoding='utf-8')

    manifest = {
        'scene': SCENE,
        'status': structural['status'],
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'paths': {
            'jp_json': str(JP_JSON),
            'en_json': str(EN_JSON),
            'en_asset': str(EN_ASSET),
            'vi_asset': str(VI_ASSET),
            'work_dir': str(WORK),
            'qa_log': str(QA_LOG),
            'focused_diff': str(DIFF),
            'script': str(Path(__file__)),
        },
        'counts': counts_by_cmd | {'total_text_commands': len(candidate_positions)},
        'hashes': {
            'en_asset_sha256': structural['source']['sha256'],
            'vi_asset_sha256': structural['output']['sha256'],
            'jp_json_sha256': structural['jp_json']['sha256'],
            'en_json_sha256': structural['en_json']['sha256'],
        },
        'structural_qa_status': structural['status'],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': structural['status'], 'counts': manifest['counts'], 'qa_errors': qa_errors, 'vi_asset': str(VI_ASSET)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
