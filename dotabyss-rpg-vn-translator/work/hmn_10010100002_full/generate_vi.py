# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE = 'hmn_10010100002'
ROOT = Path('E:/AgentTranslation')
JP = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10010100002_full'
WORK.mkdir(parents=True, exist_ok=True)

TEXT_RECORDS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}

def sha256(data: bytes):
    return hashlib.sha256(data).hexdigest()

def props(path):
    b = path.read_bytes()
    bom = b.startswith(b'\xef\xbb\xbf')
    newline = 'CRLF' if b'\r\n' in b else 'LF'
    return {'path': str(path), 'bytes': len(b), 'sha256': sha256(b), 'bom': bom, 'newline': newline, 'line_count': len(b.decode('utf-8-sig').splitlines())}

def split_keepends(text):
    return text.splitlines(True)

def text_field(parts):
    rec = parts[0]
    if rec in TEXT_RECORDS and len(parts) > TEXT_RECORDS[rec]:
        return TEXT_RECORDS[rec]
    return None

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:user|s|d)|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%', s)

translations = [
    'Em Phải Làm Sao Đây',
    'Nào‚ Rosa‚ kỵ sĩ được giao hộ vệ ta. Đây là điểm đến hôm nay.<br> ',
    'Thưa Chỉ Huy…… nơi này…… chẳng phải là quán rượu sao……?<br> ',
    'Đúng vậy. Hôm nay ta có công việc quan trọng ở đây. Nhưng như em biết đấy‚<br>quán rượu không thể gọi là nơi tuyệt đối an toàn.<br> ',
    'Vâng‚ em nghe nói quán rượu có rất nhiều khách lui tới<br>và là nơi dễ xảy ra đánh nhau hay cãi vã.<br> ',
    'Ừm. Vì thế ta cần sức của em đấy‚ Rosa. Ta muốn em đứng<br>hộ vệ thật chắc ở trước cửa quán.<br> ',
    'Ra là vậy! Em đã rõ! Xin cứ giao nơi này cho em!<br> ',
    'À‚ tất nhiên khách bình thường thì cứ cho vào nhé! Chỉ cần chặn<br>những kẻ có vẻ sẽ gây rắc rối cho ta thôi.<br> ',
    'Nhất là mấy cô gái định bắt ta làm việc vặt khác trong lúc<br>ta đang thi hành nhiệm vụ quan trọng‚ tuyệt đối đừng cho qua!<br> ',
    'Chỉ thị của ngài cụ thể quá nhỉ…… Em hiểu rồi‚<br>nhất định em sẽ bảo vệ đến cùng.<br> ',
    'Nhờ em đấy‚ Rosa!<br> ',
    'Được rồi! Mọi người‚ đang uống chứ?<br> ',
    'Ôi‚ Chỉ Huy đấy à? Chào mừng anh. Em vui vì anh đã đến lắm.<br> ',
    'Không biết đây là nhiệm vụ gì nhỉ……? Không‚ dù nội dung là gì‚<br>em chỉ cần hoàn thành nhiệm vụ hộ vệ của mình thôi!<br> ',
    'Nào‚ hôm nay uống cho đã nào! Mọi người nâng ly lên‚ cạn ly!!!<br> ',
    'Kyaa‚ Chỉ Huy tuyệt quá! Cạn ly!<br> ',
    '(……Đây thật sự là công việc‚ phải không ạ? Thưa Chỉ Huy……?)<br> ',
    'Không thấy có kẻ khả nghi nào xuất hiện. Từ giờ em cũng không được lơ là‚<br>phải tiếp tục làm tròn nhiệm vụ hộ vệ……<br> ',
    'Ư ư‚ Chỉ Huy…… anh đi đâu rồi vậy……?<br> ',
    'Kia là Alicia……? Trông chị ấy bối rối như vậy‚ rốt cuộc có chuyện gì nhỉ?<br> ',
    'Em còn nhiệm vụ hộ vệ‚ nhưng…… bỏ mặc người đang gặp khó khăn<br>là trái với tinh thần kỵ sĩ.<br> ',
    'Alicia‚ chị đang gặp chuyện gì sao?<br> ',
    'A‚ Rosa! Thật ra Chỉ Huy bỏ mặc công việc<br>rồi đi đâu mất rồi……<br> ',
    'C-Chỉ Huy ấy ạ!? Ngài ấy bỏ bê công việc sao!?<br> ',
    'Đúng vậy. Dù còn rất nhiều báo cáo sắp đến hạn……<br>Rosa‚ cô có thấy Chỉ Huy không?<br> ',
    'Em có…… thấy ngài ấy‚ nhưng mà……<br> ',
    'Thật sao!? Chỉ Huy đã đi đâu rồi!?<br> ',
    'Chuyện đó‚ ừm……<br> ',
    '(Alicia đang rất khổ sở‚ nhưng nếu cứ để chị ấy vào trong‚<br>chắc chắn Chỉ Huy cũng sẽ gặp rắc rối.)<br> ',
    '(Như vậy em sẽ không thể hoàn thành công việc được giao với tư cách hộ vệ.<br>Nhưng em cũng không thể bỏ mặc Alicia được……)<br> ',
    '(E-em phải làm sao đây!?)<br> ',
    'Rosa bối rối đến cùng cực. Alicia nhìn tòa nhà phía sau cô<br>rồi gật đầu như thể đã hiểu ra tất cả.<br> ',
    '……À‚ ra là vậy. Chỉ Huy đang ở trong quán rượu đúng không!<br> ',
    'A‚ Alicia!? Không được‚ chị không được vào!<br> ',
    'Miễn tranh luận!<br> ',
    'Ha ha ha! Chà‚ rượu hôm nay ngon thật!<br>Rượu uống khi trốn việc đúng là ngon hơn tất cả!<br> ',
    'Chỉ Huy! Anh đang làm gì vậy hả!?<br> ',
    'A-Alicia sao!? Sao cô lại ở đây!? Hộ vệ Rosa đâu rồi!?<br> ',
    'E-em vô cùng xin lỗi! Em đã không thể ngăn chị ấy!<br> ',
    'Rosa hốt hoảng đứng chắn trước Alicia<br>như để bảo vệ Chỉ Huy.<br> ',
    'Alicia‚ xin chị dừng lại!<br>Em sẽ không để chị động tay vào Chỉ Huy đâu!<br> ',
    'Ồ‚ đúng là hộ vệ của ta! Làm ơn bảo vệ ta khỏi Alicia với!<br> ',
    'Vâng‚ dù phải đánh đổi cả thân này!<br> ',
    'Cảm ơn em‚ Rosa! Ta chỉ còn biết trông cậy vào em thôi……<br> ',
    'Thưa Chỉ Huy……!<br> ',
    'Sao thành ra em mới là người xấu vậy chứ! Là lỗi của Chỉ Huy mà!<br> ',
    'Alicia‚ xin chị rộng lượng tha thứ!<br> ',
    'Khi Alicia định áp sát Chỉ Huy‚<br>Rosa lấy thân mình ra ngăn lại.<br> ',
    'Trời ơi! Rốt cuộc chuyện này là sao vậy!?<br>Tại sao Chỉ Huy đi uống rượu mà lại cần hộ vệ chứ!?<br> ',
    'Chuyện là‚ vì Chỉ Huy trông có vẻ đang gặp khó khăn nên……<br> ',
    'Anh ấy trông chẳng khó khăn chút nào cả! Xin cô giải thích cho rõ đi!<br> ',
    'Thật ra Chỉ Huy đang trong lúc làm nhiệm vụ quan trọng.<br>Em đang đảm nhiệm việc hộ vệ cho ngài ấy.<br> ',
    'Nhiệm vụ quan trọng……?<br> ',
    'Vâng‚ em được nghe như vậy.<br> ',
    'Đúng đấy Alicia‚ ta đang làm việc‚ đừng làm phiền ta.<br> ',
    'Nhìn thế nào cũng là nói dối mà! Làm gì có công việc nào như thế chứ!<br> ',
    'Có…… thật vậy không ạ‚ thưa Chỉ Huy?<br> ',
    'Ta đâu có nói dối? Ta có một bản báo cáo về tình hình kinh tế trong thành‚<br>nên đang điều tra thực địa đây.<br> ',
    'Ra là vậy! Hóa ra là như thế!<br> ',
    'Vậy nên Alicia‚ chị có thể cho chúng em thêm chút thời gian được không?<br> ',
    'Đừng để bị lừa‚ đó chỉ là cái cớ thôi!<br>Anh ấy chỉ đang uống rượu chơi bời thôi mà!<br> ',
    'Không không‚ khách ít hơn lần trước đấy chứ?<br>Ta vẫn đang quan sát rất kỹ mà‚ biết không?<br> ',
    'Chỉ là vì Rosa đứng canh ở lối vào<br>nên mấy người thô lỗ không vào được thôi mà!<br> ',
    'Vâng‚ loại bỏ nguy hiểm cho Chỉ Huy từ trước khi nó xảy ra<br>là công việc đương nhiên của một hộ vệ.<br> ',
    'Ừm‚ em làm tốt lắm‚ Rosa. Cứ tiếp tục như vậy nhé.<br> ',
    'Vâng‚ xin cứ giao cho em!<br> ',
    'Trời ơi!!!<br> ',
    'Ôi Chỉ Huy‚ anh còn gọi thêm cô gái khác nữa à?<br> ',
    'Ha ha ha‚ hôm nay đối tượng của anh chỉ có em thôi.<br> ',
    '“Đối tượng hôm nay” cơ đấy. Chỉ Huy vẫn y như mọi khi nhỉ.<br> ',
    'Nhìn đi Rosa! Làm gì có nhiệm vụ nào là tán tỉnh phụ nữ chứ!<br> ',
    'C-chuyện đó…… có lẽ là vậy‚ nhưng……<br> ',
    'Không không‚ bằng việc uống rượu và giao lưu với phụ nữ‚ ta giải phóng<br>trái tim mệt mỏi rồi biến nó thành sức mạnh để bảo vệ hòa bình.<br> ',
    'Đây cũng là nhiệm vụ của Chỉ Huy đấy.<br> ',
    'Ra là vậy…… Em chưa từng tưởng tượng đến! Em hiểu rồi‚<br>em cũng sẽ giúp Chỉ Huy bảo vệ hòa bình!<br> ',
    'Ơ-ồ!?<br> ',
    'Rosa ngồi xuống cạnh %user%‚ rồi rụt rè và vụng về tựa sát vào anh.<br> ',
    'Nếu uống rượu cùng nhau có thể giúp ích cho Chỉ Huy‚<br>xin hãy cho em được hỗ trợ nữa……!<br> ',
    'À‚ ừ…… cảm ơn em……<br> ',
    '<size=30>CHỈ HUY KHÔNG THẤY CẮN RỨT SAO?</size>',
    '……Thành thật mà nói‚ có một chút.<br> ',
    '……? Em đã làm sai gì sao?<br> ',
    'À…… đúng rồi nhỉ. Một kỵ sĩ như em<br>đâu thể nào xoa dịu được Chỉ Huy.<br> ',
    'Em sẽ quay lại nhiệm vụ hộ vệ. Xin Chỉ Huy hãy nghỉ ngơi cho tâm hồn được thư thái.<br> ',
    'Không‚ không sao đâu‚ Rosa. Nhờ có em mà ta đã được xoa dịu đủ rồi.<br> ',
    'Thật sao ạ?<br> ',
    'Ừ. Việc thị sát cũng xong rồi‚ ta cũng nên quay lại làm việc thôi.<br>Đúng không‚ Alicia?<br> ',
    'Ngay từ đầu anh cứ ngoan ngoãn làm thế đi!<br> ',
    'Nếu khó khăn của cả hai người đều được giải quyết‚ thì thật sự tốt quá rồi!<br> ',
    'Ừ‚ cảm ơn em đã cùng ta giải khuây.<br>……Có vẻ ta cũng không còn thời gian để trốn tránh thực tại nữa rồi.<br> ',
    'Đúng vậy! Anh cứ trì hoãn việc giấy tờ‚<br>người gặp rắc rối từ giờ sẽ là Chỉ Huy đấy!<br> ',
    'Chỉ Huy sẽ…… gặp khó khăn sao……!?<br> ',
]

def main():
    src_b = EN_ASSET.read_bytes()
    src_text = src_b.decode('utf-8-sig')
    lines = split_keepends(src_text)
    candidates = []
    for i, line in enumerate(lines):
        bare = line.rstrip('\r\n')
        parts = bare.split(',')
        idx = text_field(parts)
        if idx is not None:
            candidates.append((i, parts[0], idx, parts[idx]))
    if len(candidates) != len(translations):
        raise SystemExit(f'translation count mismatch: candidates={len(candidates)} translations={len(translations)}')
    new_lines = list(lines)
    entries = []
    blockers = []
    for n, ((line_idx, rec, idx, old_text), vi) in enumerate(zip(candidates, translations), 1):
        if ',' in vi:
            blockers.append({'line': line_idx+1, 'type': 'ASCII_COMMA_IN_VI', 'text': vi})
        old_bare = lines[line_idx].rstrip('\r\n')
        ending = lines[line_idx][len(old_bare):]
        parts = old_bare.split(',')
        before_sig = parts[:idx] + parts[idx+1:]
        parts[idx] = vi
        new_bare = ','.join(parts)
        new_lines[line_idx] = new_bare + ending
        new_sig = new_bare.split(',')[:idx] + new_bare.split(',')[idx+1:]
        status = 'TRANSLATED'
        if old_text == vi:
            status = 'INTENTIONAL_IDENTICAL'
        if before_sig != new_sig:
            blockers.append({'line': line_idx+1, 'type': 'TECH_FIELD_CHANGED', 'record': rec})
        if old_bare.count(',') != new_bare.count(','):
            blockers.append({'line': line_idx+1, 'type': 'DELIMITER_COUNT_MISMATCH', 'old': old_bare.count(','), 'new': new_bare.count(',')})
        if tags(old_text) != tags(vi):
            blockers.append({'line': line_idx+1, 'type': 'TAG_MISMATCH', 'old': tags(old_text), 'new': tags(vi)})
        if placeholders(old_text) != placeholders(vi):
            blockers.append({'line': line_idx+1, 'type': 'PLACEHOLDER_MISMATCH', 'old': placeholders(old_text), 'new': placeholders(vi)})
        entries.append({'index': n, 'asset_line': line_idx+1, 'record': rec, 'status': 'EXACT_TO_ORDERED_NOVEL', 'translation_status': status, 'en_text': old_text, 'vi_text': vi})
    out_text = ''.join(new_lines)
    if EN_ASSET.read_bytes().startswith(b'\xef\xbb\xbf'):
        out_b = ('\ufeff' + out_text).encode('utf-8')
    else:
        out_b = out_text.encode('utf-8')
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_b)

    # independent structural QA
    vi_b = VI_ASSET.read_bytes()
    vi_text = vi_b.decode('utf-8-sig')
    vi_lines = split_keepends(vi_text)
    qa = {
        'file': SCENE + '.txt',
        'qa_status': 'PASS',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'blockers': [],
        'items': [],
        'notes': ['JP used as primary source; EN asset used only for ordered alignment.', 'All characters confirmed 18+ by project context; this file contains no explicit H18 content.'],
        'counts': {'candidate_records': len(candidates), 'translated_records': len(translations), 'title': 0, 'message': 0, 'messageTextUnder': 0, 'messageTextCenter': 0, 'kept_en_records': 0}
    }
    for _, rec, _, _ in candidates:
        qa['counts'][rec] += 1
    qa['blockers'].extend(blockers)
    if len(lines) != len(vi_lines):
        qa['blockers'].append({'type': 'LINE_COUNT_MISMATCH', 'en': len(lines), 'vi': len(vi_lines)})
    if props(EN_ASSET)['bom'] != props(VI_ASSET)['bom'] or props(EN_ASSET)['newline'] != props(VI_ASSET)['newline']:
        qa['blockers'].append({'type': 'ENCODING_OR_NEWLINE_MISMATCH', 'en': props(EN_ASSET), 'vi': props(VI_ASSET)})
    for i, (a, b) in enumerate(zip(lines, vi_lines), 1):
        ab = a.rstrip('\r\n'); bb = b.rstrip('\r\n')
        if ab.count(',') != bb.count(','):
            qa['blockers'].append({'line': i, 'type': 'DELIMITER_COUNT_MISMATCH_POST', 'en': ab.count(','), 'vi': bb.count(',')})
        ap = ab.split(','); bp = bb.split(',')
        if ap[0] in TEXT_RECORDS and len(ap) > TEXT_RECORDS[ap[0]]:
            idx = TEXT_RECORDS[ap[0]]
            if ap[:idx] + ap[idx+1:] != bp[:idx] + bp[idx+1:]:
                qa['blockers'].append({'line': i, 'type': 'TECH_FIELD_CHANGED_POST'})
            if ap[idx] == bp[idx]:
                qa['items'].append({'line': i, 'type': 'KEPT_EN_TEXT', 'severity': 'major', 'status': 'review'})
                qa['counts']['kept_en_records'] += 1
            if re.search(r'\b(Commander|Lord Commander|guard duty|important business|Alicia|Rosa was|Really\?|No arguments|Cheers|Geez|work|tavern|drinking|paperwork)\b', bp[idx]):
                # Alicia/Rosa proper-name alone is OK; this targets common EN leftovers in strings.
                if not re.fullmatch(r'.*(Alicia|Rosa|%user%|<user>).*', bp[idx]) or re.search(r'Commander|Lord Commander|guard duty|important business|Really\?|No arguments|Cheers|Geez|work|tavern|drinking|paperwork', bp[idx]):
                    qa['blockers'].append({'line': i, 'type': 'POSSIBLE_EN_LEFTOVER', 'text': bp[idx]})
            if re.search(r'[ぁ-んァ-ン一-龯]', bp[idx]):
                qa['blockers'].append({'line': i, 'type': 'JP_LEFTOVER_IN_TEXT', 'text': bp[idx]})
    if qa['blockers']:
        qa['qa_status'] = 'FAIL'

    manifest = {
        'scene': SCENE,
        'status': qa['qa_status'],
        'sources': {'ja_json': str(JP), 'en_json': str(EN_JSON), 'en_asset': props(EN_ASSET), 'vi_asset': props(VI_ASSET)},
        'text_command_counts': qa['counts'],
        'translation_source_policy': 'JP primary; EN for alignment only',
        'entries': entries,
        'qa_log': str(WORK/'qa_log.json'),
        'focused_diff': str(WORK/'focused_diff.md'),
        'script': str(WORK/'generate_vi.py')
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

    diff_lines = ['# Focused diff for hmn_10010100002.txt\n\n']
    for e in entries:
        diff_lines.append(f"## Record {e['index']} - asset line {e['asset_line']} - {e['record']}\n\n")
        diff_lines.append('```diff\n')
        diff_lines.extend(difflib.unified_diff([e['en_text']+'\n'], [e['vi_text']+'\n'], fromfile='EN text', tofile='VI text', lineterm=''))
        diff_lines.append('\n```\n\n')
    (WORK/'focused_diff.md').write_text(''.join(diff_lines), encoding='utf-8')
    print(json.dumps({'qa_status': qa['qa_status'], 'blockers': len(qa['blockers']), 'counts': qa['counts'], 'vi': str(VI_ASSET), 'work': str(WORK)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
