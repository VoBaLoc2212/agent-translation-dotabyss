from __future__ import annotations

import csv
import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10160100001'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST = WORK / 'manifest.json'
QA_LOG = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'
TEXT_CMDS = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

# Ordered translations for: title + every message/messageText* record in the EN asset.
TRANSLATIONS = [
    'Chiến Thần Wisteria',
    'Ngay sau khi Chỉ Huy được điều đến Căn Cứ Tiền Tuyến và căn cứ<br>bắt đầu vận hành toàn diện.<br> ',
    'ÔÔÔÔÔHHH!<br> ',
    'B-Bị bao vây rồi! Trước sau gì cũng toàn quái vật!<br> ',
    'Không thể nào...! Chẳng còn chỗ nào để chạy cả!<br> ',
    '(Aaaa‚ chết tiệt! Mình thiếu tất cả—chiến lực‚ thuộc hạ đáng tin<br>cậy...!)<br> ',
    '(Nhưng thứ thiếu nhất vẫn là thông tin...! Đơn vị nào còn đủ gan lì<br>để trụ lại trong tình thế này đây!?)<br> ',
    'Khốn thật! Mình cần một ai đó có thể phá vỡ tình thế thật hoành<br>tráng! Có ai ở đâu không! Cứ xử chúng đi!<br> ',
    '...Đã rõ.<br> ',
    'Hả!?<br> ',
    'Lời buột miệng đầy bất lực của tôi bất ngờ được đáp lại.<br> ',
    'Cô là...!?<br> ',
    'Phía sau lẽ ra không có ai lại có một xạ thủ cầm cây cung rực cháy<br>đang đứng chờ. Bằng động tác uyển chuyển‚ cô giương cung lên trời—<br> ',
    'Hự!<br> ',
    'Cùng một hơi thở khẽ‚ mũi tên chất chứa sức mạnh khổng lồ được<br>bắn ra. Ngay khi mũi tên vút lên biến mất giữa bầu trời‚ một cơn mưa tên rực lửa đổ xuống.<br> ',
    'Mưa... lửa!? Lũ quái vật đang bị thiêu rụi!<br> ',
    'Làm được rồi... chúng ta sẽ sống sót trở về...!<br> ',
    'Ôôôôôh...<br> ',
    'Lũ quái vật lần lượt gục xuống dưới cơn mưa tên‚ còn những người<br>lính nhặt lại được mạng sống thì reo hò vang dội.<br> ',
    'Không thể tin nổi... Cô ấy thật sự phá vỡ thế trận cái rầm như thế.<br> ',
    '...Tình hình chiến sự thế nào‚ Chỉ Huy? Tôi nghĩ mình đã hoàn thành<br>mệnh lệnh.<br> ',
    'Vượt cả mong đợi. Cô cứu tôi rồi. Tôi là %user%‚ còn cô?<br> ',
    '...Tôi là Wisteria. Vậy anh là Chỉ Huy mới.<br> ',
    'Ừ. Lần đầu gặp đã được cứu khỏi nguy hiểm‚ tôi để cô thấy cảnh mất mặt rồi.<br> ',
    'Tôi vốn muốn thể hiện mặt tốt trước một người đáng tin cậy như<br>cô‚ vậy mà...<br> ',
    '...Cũng không tệ.<br> ',
    'Giữa loạn chiến‚ anh vẫn không bỏ cuộc mà tìm cách xoay chuyển<br>tình thế. Bám lấy sự sống không phải chuyện xấu.<br> ',
    'Dù không có tôi‚ anh hẳn vẫn sẽ sống sót trở về.<br> ',
    'Khó nói lắm. Tôi thì thấy mình nhặt được mạng nhờ Wisteria đấy.<br> ',
    'Dù sao thì một chiến lực đáng tin rất quý giá. Từ giờ tôi trông cậy<br>vào cô.<br> ',
    '...Đã rõ. Tôi sẽ quay lại cảnh giới.<br> ',
    'Nói vậy rồi rời đi‚ Wisteria trông như chỉ đang thong thả bước<br>dạo. Nhưng chỉ trong khoảnh khắc tôi rời mắt‚ cô đã biến mất khỏi tầm nhìn.<br> ',
    'Biến mất rồi... không‚ là mình để mất dấu cô ấy sao? Đúng là một người thú vị.<br> ',
    'Chỉ Huy‚ vừa rồi... là Chiến Thần đúng không ạ?<br> ',
    'Chiến Thần? Ý cô là Wisteria à?<br> ',
    'Vâng. Chỉ với một cây cung‚ cô ấy có thể xoay chuyển cục diện<br>chiến trường. Đúng như một vị thần chiến đấu nên được gọi là Chiến Thần.<br> ',
    'Cô ấy ở đó trước khi ta hay biết‚ và biến mất trước khi ta kịp nhận<br>ra. Ngay cả điểm ấy cũng giống thần linh vậy...<br> ',
    'Ra vậy. Một biệt danh xứng với cô ấy. Chiến Thần Wisteria‚ nhỉ...<br> ',
    'Một thời gian sau trận chiến ở vùng núi‚ %user% lên đường khảo sát<br>địa hình quanh căn cứ.<br> ',
    'Chậc‚ đến địa hình quanh căn cứ mà mình còn chưa nắm rõ hoàn<br>toàn. Thế thì chỉ huy kiểu gì đây?<br> ',
    'Ừm... hơi buồn đi tiểu rồi. Giải quyết quanh đây vậy.<br> ',
    'Ngay khi tôi vừa kéo quần xuống trong bụi cây để đi tiểu—<br> ',
    '—Đứng yên.<br> ',
    'Một giọng nói lạnh lẽo vang lên từ phía sau‚ khiến tôi bất giác đứng khựng lại.<br> ',
    'Úwaa!? A-Ai đó!?<br> ',
    'Tôi đã bảo đứng yên. Đừng cử động thêm nữa.<br> ',
    'C-Cô bảo đừng cử động thì... ít nhất cũng cho tôi cất vào hoặc lấy<br>ra chứ...!<br> ',
    'Nói nhảm gì vậy... Anh định lấy gì ra?<br> ',
    'Gì thì... cái đó... thứ ấy ấy...<br> ',
    '...Đủ rồi. Giơ cả hai tay lên và quay mặt về phía tôi.<br> ',
    '*thở dài*... Được rồi...<br> ',
    'Quần vẫn tuột‚ tôi giơ tay lên rồi quay người lại.<br>Wisteria đứng đó‚ không hề lơ là khi chĩa cung về phía tôi.<br> ',
    'Hả...? Chỉ Huy!?<br> ',
    'Ồ‚ là Wisteria à. Giống lần trước‚ cô giỏi thật đấy‚ lại tiếp cận mà<br>không để tôi cảm nhận được khí tức.<br> ',
    'Tôi thấy một bóng người lạ lảng vảng nên mới thận trọng tiếp cận<br>từ phía sau‚ nhưng...<br> ',
    'Tôi không ngờ lại là anh‚ Chỉ Huy. Xin thứ lỗi vì đã thất lễ.<br> ',
    'Nhưng... tại sao anh lại ở nơi như thế này?<br> ',
    'Tôi muốn tự mắt xem địa hình quanh căn cứ. Sở chỉ huy vẫn còn<br>thiếu quá nhiều thông tin.<br> ',
    'Đích thân Chỉ Huy phải tự mắt xem ư?<br> ',
    'Những gợn địa hình nhỏ không có trên bản đồ‚ lối mòn thú có thể<br>dùng được‚ thay đổi tầm nhìn do độ dày thảm thực vật.<br> ',
    'Chỉ một thông tin nhỏ cũng liên quan trực tiếp đến sống chết của<br>binh sĩ. Với tư cách Chỉ Huy‚ tôi nên biết chứ?<br> ',
    '...Anh tận tâm với công việc thật. Có vẻ nhận định của tôi rằng anh<br>không tệ đã không sai.<br> ',
    'Được cô khen thế thì tôi vui rồi.<br> ',
    'Nhưng để lộ sơ hở vẫn là vấn đề. Nếu đối thủ không phải tôi‚ có<br>lẽ anh đã chết.<br> ',
    'Biết sao được‚ tôi đang đi vệ sinh dở mà.<br> ',
    'Chính lúc không thể cử động mới càng cần cảnh giác. Nhất là khi<br>đã kéo quần áo xuống...<br> ',
    'Q-Qu‚ quần áo...<br> ',
    'Sao vậy‚ Wisteria? Tự nhiên lại ấp úng.<br> ',
    'Ch‚ chuyện đó là...<br> ',
    'Cô sao thế? Trông cô thật sự lạ lắm đấy.<br> ',
    'Đ-Đừng lại gần!!!<br> ',
    'Cô không cần phản ứng như thể có kẻ nguy hiểm đang đến gần vậy<br>đâu. Tự nhiên bị né tránh cũng tổn thương lắm chứ.<br> ',
    'A-Anh không nhận ra sao...? Sao anh có thể bình thản nói chuyện trong tình trạng này được...!?<br> ',
    'Cô bắt đầu tránh mặt rõ ràng luôn rồi đấy... Quay mặt đi khỏi Chỉ<br>Huy đang đứng ngay trước mắt thì thế nào đây?<br> ',
    'Làm sao tôi nhìn thẳng được chứ! Anh nói thật đấy à‚ Chỉ Huy...!<br> ',
    'Thật hay không thì tôi cũng chẳng hiểu. Cô đang xấu hổ vì chuyện<br>gì vậy‚ Wisteria?<br> ',
    'Vì thế đó...! Làm ơn đi‚ mau cất phía trước lại giùm!<br> ',
    '...Phía trước? À‚ tôi vẫn để quần tuột xuống. Quên béng mất.<br> ',
    'Chuyện đó mà cũng quên được sao...!? Anh không thật sự là biến<br>thái đấy chứ?<br> ',
    'Thất lễ thật đấy. Cô bảo “đừng cử động‚ giơ tay lên!” nên tôi chỉ<br>làm theo thôi.<br> ',
    'Dù sao thì xin lỗi vì đã để cô thấy thứ kỳ quặc. Tôi sai rồi.<br> ',
    '...Việc tôi thất lễ cũng là sự thật. Vậy coi như chúng ta không ai nợ ai nữa.<br> ',
    '...Tôi nghĩ người xuất hiện lúc tôi đang tụt quần là Wisteria mà.<br> ',
    'Chỉ Huy? Anh có điều gì muốn nói sao?<br> ',
    'Không‚ chẳng có gì. Tiện đây Wisteria‚ tôi về căn cứ đây. Hộ tống<br>tôi nhé.<br> ',
    'À khoan‚ sau khi tôi giải quyết xong đã.<br> ',
    '*thở dài*... Tôi sẽ đợi‚ nên làm cho nhanh đi.<br> ',
    'Wisteria nhún vai như thể cạn lời rồi biến mất giữa những hàng cây.<br> ',
    'Ừ‚ quả nhiên cô ấy là người thú vị.<br> ',
    '—Tôi nghe thấy đấy. Đừng nói linh tinh nữa. Nhanh lên.<br> ',
    'Ồ‚ xin lỗi nhé. Tai cô thính là chuyện tuyệt vời‚ nhưng đừng nghe âm thanh đó đấy.<br> ',
    'Ai mà thèm nghe chứ...!<br> ',
    'Thật tình‚ đúng là một người hay đùa. Anh ta không có cái gọi là xấu hổ sao?<br> ',
    'Nhưng... đã lâu rồi mình mới nói chuyện với người khác nhiều đến<br>vậy. Mình không định buông lỏng cảnh giác‚ nhưng lạ thay‚ cũng không thấy khó chịu.<br> ',
    'Đây là Chỉ Huy của căn cứ này sao...<br> ',
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_with_meta(path: Path):
    b = path.read_bytes()
    bom = b.startswith(b'\xef\xbb\xbf')
    newline = 'CRLF' if b'\r\n' in b else 'LF'
    text = b.decode('utf-8-sig')
    return b, text, bom, newline


def split_fields(line: str):
    return line.split(',')


def text_field_index(parts):
    cmd = parts[0]
    if cmd == 'title':
        return 1
    if cmd in ('message', 'messageTextUnder', 'messageTextCenter'):
        return 2
    raise ValueError(cmd)


def tags(s: str):
    return re.findall(r'<[^>]+>', s)


def placeholders(s: str):
    return re.findall(r'%user%|<user>|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%', s)


def internal_ascii_comma_violations(line: str):
    # Splitting preserves only delimiter commas; any extra internal comma would alter field count.
    # Project convention: no ASCII comma inside translated fields. Since parser is raw delimiter,
    # field count equality is the guard.
    return []


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    src_b, src_text, src_bom, src_newline = decode_with_meta(EN_ASSET)
    src_lines = src_text.splitlines(keepends=True)
    line_end = '\r\n' if src_newline == 'CRLF' else '\n'
    text_positions = []
    counts = Counter()
    delimiter_counts = []
    for idx, raw in enumerate(src_lines):
        line = raw[:-2] if raw.endswith('\r\n') else raw[:-1] if raw.endswith('\n') else raw
        parts = split_fields(line)
        if parts and parts[0] in TEXT_CMDS:
            counts[parts[0]] += 1
            text_positions.append(idx)
            delimiter_counts.append(line.count(','))
    if len(text_positions) != len(TRANSLATIONS):
        raise SystemExit(f'translation count mismatch: asset {len(text_positions)} vs list {len(TRANSLATIONS)}')

    out_lines = src_lines[:]
    mappings = []
    for n, idx in enumerate(text_positions):
        raw = src_lines[idx]
        eol = '\r\n' if raw.endswith('\r\n') else '\n' if raw.endswith('\n') else ''
        line = raw[:-len(eol)] if eol else raw
        parts = split_fields(line)
        tfi = text_field_index(parts)
        old_text = parts[tfi]
        new_text = TRANSLATIONS[n].replace(',', '‚')
        # Preserve asset placeholders exactly where required; TRANSLATIONS already uses %user% for asset records.
        if tags(old_text) != tags(new_text):
            raise SystemExit(f'tag mismatch at asset line {idx+1}: {tags(old_text)} vs {tags(new_text)}')
        if placeholders(old_text) != placeholders(new_text):
            raise SystemExit(f'placeholder mismatch at asset line {idx+1}: {placeholders(old_text)} vs {placeholders(new_text)}')
        parts[tfi] = new_text
        newline = ','.join(parts) + eol
        if newline.count(',') != raw.count(','):
            raise SystemExit(f'delimiter count mismatch at asset line {idx+1}')
        out_lines[idx] = newline
        mappings.append({
            'asset_line': idx + 1,
            'command': parts[0],
            'speaker': parts[1] if parts[0] != 'title' and len(parts) > 1 else None,
            'old_text': old_text,
            'vi_text': new_text,
            'status': 'TRANSLATED',
            'match_status': 'CONTEXT_MATCH' if n == 0 else 'EXACT_OR_ORDERED',
        })

    out_text = ''.join(out_lines)
    out_bytes = (b'\xef\xbb\xbf' if src_bom else b'') + out_text.encode('utf-8')
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_bytes)

    # Structural QA
    vi_b, vi_text, vi_bom, vi_newline = decode_with_meta(VI_ASSET)
    vi_lines = vi_text.splitlines(keepends=True)
    errors = []
    if len(vi_lines) != len(src_lines):
        errors.append({'type': 'line_count', 'source': len(src_lines), 'vi': len(vi_lines)})
    if src_bom != vi_bom:
        errors.append({'type': 'bom', 'source': src_bom, 'vi': vi_bom})
    if src_newline != vi_newline:
        errors.append({'type': 'newline', 'source': src_newline, 'vi': vi_newline})
    translated_records = 0
    for i, (sraw, vraw) in enumerate(zip(src_lines, vi_lines), 1):
        seol = '\r\n' if sraw.endswith('\r\n') else '\n' if sraw.endswith('\n') else ''
        veol = '\r\n' if vraw.endswith('\r\n') else '\n' if vraw.endswith('\n') else ''
        sline = sraw[:-len(seol)] if seol else sraw
        vline = vraw[:-len(veol)] if veol else vraw
        if sline.count(',') != vline.count(','):
            errors.append({'line': i, 'type': 'delimiter_count', 'source': sline.count(','), 'vi': vline.count(',')})
        sp = split_fields(sline)
        vp = split_fields(vline)
        if len(sp) != len(vp):
            errors.append({'line': i, 'type': 'field_count', 'source': len(sp), 'vi': len(vp)})
            continue
        if sp and sp[0] in TEXT_CMDS:
            tfi = text_field_index(sp)
            translated_records += 1
            if sp[:tfi] != vp[:tfi] or sp[tfi+1:] != vp[tfi+1:]:
                errors.append({'line': i, 'type': 'technical_field_changed'})
            if tags(sp[tfi]) != tags(vp[tfi]):
                errors.append({'line': i, 'type': 'tag_list', 'source': tags(sp[tfi]), 'vi': tags(vp[tfi])})
            if placeholders(sp[tfi]) != placeholders(vp[tfi]):
                errors.append({'line': i, 'type': 'placeholder_list', 'source': placeholders(sp[tfi]), 'vi': placeholders(vp[tfi])})

    # Focused diff for text records only
    diff_src = []
    diff_vi = []
    for m in mappings:
        diff_src.append(f"{m['asset_line']}: {m['command']},{m.get('speaker') or ''},{m['old_text']}\n")
        diff_vi.append(f"{m['asset_line']}: {m['command']},{m.get('speaker') or ''},{m['vi_text']}\n")
    diff = ''.join(difflib.unified_diff(diff_src, diff_vi, fromfile='EN text records', tofile='VI text records', lineterm=''))
    DIFF.write_text('# Focused Diff - hmn_10160100001\n\n```diff\n' + diff + '\n```\n', encoding='utf-8')

    manifest = {
        'scene': SCENE,
        'status': 'GENERATED_PENDING_INDEPENDENT_VERIFY' if errors else 'QA_PASS_PENDING_INDEPENDENT_VERIFY',
        'paths': {
            'ja_json': str(JA_JSON),
            'en_json': str(EN_JSON),
            'en_asset': str(EN_ASSET),
            'vi_asset': str(VI_ASSET),
            'manifest': str(MANIFEST),
            'qa_log': str(QA_LOG),
            'focused_diff': str(DIFF),
            'script': str(Path(__file__)),
        },
        'source': {
            'en_asset_sha256': sha256(EN_ASSET),
            'encoding': 'utf-8-sig' if src_bom else 'utf-8',
            'bom': src_bom,
            'newline': src_newline,
            'line_count': len(src_lines),
            'text_command_counts': dict(counts),
            'text_record_total': len(text_positions),
        },
        'output': {
            'vi_asset_sha256': sha256(VI_ASSET),
            'line_count': len(vi_lines),
            'bom': vi_bom,
            'newline': vi_newline,
            'translated_records': translated_records,
        },
        'character_notes': {
            'Wisteria': 'Nữ xạ thủ trầm tĩnh, cảnh giác, nói với Chỉ Huy bằng tôi-anh/Chỉ Huy; Commander đáp tôi-cô trong cảnh mới gặp.',
            'Commander': 'Nam chính; Commander/司令官 dịch là Chỉ Huy.',
        },
        'title_vi': TRANSLATIONS[0],
        'structural_errors': errors,
        'mapping_summary': {'TRANSLATED': len(mappings), 'UNMATCHED': 0, 'AMBIGUOUS': 0},
        'mappings': mappings,
    }
    qa = {
        'scene': SCENE,
        'status': 'PASS' if not errors else 'FAIL',
        'checks': {
            'line_count': len(vi_lines) == len(src_lines),
            'bom_preserved': src_bom == vi_bom,
            'newline_preserved': src_newline == vi_newline,
            'delimiter_counts_preserved': not any(e.get('type') in ('delimiter_count', 'field_count') for e in errors),
            'technical_fields_preserved': not any(e.get('type') == 'technical_field_changed' for e in errors),
            'tags_preserved': not any(e.get('type') == 'tag_list' for e in errors),
            'placeholders_preserved': not any(e.get('type') == 'placeholder_list' for e in errors),
            'text_command_counts': dict(counts),
            'translated_records': translated_records,
        },
        'errors': errors,
        'notes': [
            'JP ja.json used as primary; EN novel and EN asset used for ordered alignment.',
            'All text command types counted: title/message/messageTextUnder/messageTextCenter.',
            'ASCII commas inside VI text replaced with U+201A where needed.',
            'Speaker fields, charaload names, IDs, voice IDs, placeholders, and tags preserved.',
            'Scene contains non-explicit adult-adjacent exposure comedy; translated normally under project adult-content confirmation without changing consent/tone.',
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'status': qa['status'],
        'text_records': translated_records,
        'counts': dict(counts),
        'errors': errors,
        'vi_asset': str(VI_ASSET),
        'manifest': str(MANIFEST),
        'qa_log': str(QA_LOG),
        'diff': str(DIFF),
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
