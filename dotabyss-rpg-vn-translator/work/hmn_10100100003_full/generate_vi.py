# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

SCENE = 'hmn_10100100003'
ROOT = Path('E:/AgentTranslation')
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
TEXT_CMDS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}

VI = [
"Cuộc Thi Săn Tại Căn Cứ Tiền Tuyến",
"Phần săn bắn của cuộc thi săn đã kết thúc.<br>Các thợ săn ôm chiến lợi phẩm của mình và lần lượt quay về căn cứ tiền tuyến.",
"Trong số đó‚ người săn được con mồi oai vệ nhất là――",
"C‚ cái này là…… nguyên liệu cao cấp huyền thoại‚ Ushitoributa sao!?<br>Anh săn được thứ lợi hại thế này ư!?",
"Mình sẽ nấu nó thật ngon ngay đây‚<br>nên cứ mong chờ nhé♪",
"Tôi đã khổ sở lắm mới săn được đấy……!<br>Con này sẽ khiến cô há hốc mồm cho xem‚ Alicia……!",
"K‚ không thể nào……! Dù còn có điểm bất lợi là Chỉ Huy đi cùng‚<br>chẳng lẽ cô Diana vẫn quá xuất sắc sao!?",
"Này chờ đã! Tôi cũng có lập công mà!?",
"Chỉ Huy đã cố gắng nhiều lắm đấy♪<br>Nếu chỉ có mình thì chắc chắn không săn được con mồi này đâu!",
"Ơơơ?<br>Thật vậy sao……?",
"Diana‚ trông cậy vào món ngon nhất của em đấy!",
"Ừm! Cứ để mình lo♪",
"……Chỉ Huy không phụ nấu sao?",
"Ừ thì‚ riêng vụ này tôi đúng là chỉ vướng chân thôi……",
"Rồi‚ lửa đã chuẩn bị xong‚ rút máu cũng ổn cả.<br>Thịt thì chưa ủ được chút nào‚ nhưng đó cũng là một hương vị♪",
"Này nhìn kìa! Đó là Ushitoributa đúng không!?<br>Quả nhiên là Diana săn được à……",
"Đúng là lợi hại. Chúng ta bắn bao nhiêu mũi tên<br>mà còn chẳng sượt qua được nó.",
"Trước ánh mắt dõi theo của các thợ săn xung quanh‚<br>Diana bắt đầu nấu nướng.",
"Vậy em định nấu nó thế nào?<br>Trông nó là một con vật chẳng hiểu nổi……",
"Hư hư hư. Có vẻ cậu tò mò lắm nhỉ!<br>Yên tâm đi! Đây là lần đầu mình săn nó‚ nhưng mình từng xẻ thịt nó rồi~.",
"Con Ushitoributa này‚ nấu cũng vui lắm đấy!",
"Diana xoay con dao bếp lớn một vòng‚<br>rồi bắt đầu đưa lưỡi dao vào con Ushitoributa đang treo.",
"Ushitoributa là động vật chimera pha trộn từ ba loài……<br>Mình sẽ chia các phần thịt theo cấu trúc của nó rồi nghĩ xem nên nấu món gì.",
"Trước tiên là phần thân…… tức phần bò nhỉ♪<br>Thăn ngoại‚ thăn lưng‚ thăn nội đều là những phần khá quen thuộc nhưng……",
"Thật ra dù nhìn giống nhau‚<br>có những chỗ hòa lẫn hương vị của heo và gà nữa.",
"Những phần đó được gọi là thăn heo hay lưng gà và rất được ưa chuộng đấy~",
"……Tôi chưa từng nghe loại thịt nào như thế cả.",
"Ơ‚ cậu không biết sao? Cắt phần chuyển sắc này<br>thế nào mới chính là chỗ để đầu bếp thể hiện tay nghề đấy?",
"Lần này mình sẽ chuẩn bị cả phần hòa lẫn lẫn phần được tách thật gọn nhé!",
"Các phần khác cũng ngon‚ nhưng chỗ mình đặc biệt để ý là đây‚ phần cánh!<br>Dĩ nhiên sẽ có vị gà…… đúng rồi! Khoảng cánh giữa và cánh gốc ấy!",
"Cánh cỡ này thì gà bình thường không thể có được đâu nhỉ~.<br>Rất giàu gelatin nên núng nính lắm! Lấy nước dùng cũng tuyệt hảo!",
"Nhưng điều đáng ngạc nhiên là……<br>nghe nói khi cắn vào thì đôi lúc nó lại trơn tuột chạy mất.",
"Trước đây mình không hiểu lý do‚ nhưng sau khi săn thử thì thấy hợp lý ghê~.",
"Cái kiểu né tránh rợn người đó nấu lên rồi vẫn còn à!<br>Thế thì không nên ăn chút nào đâu!",
"Ngoài ra không thể quên Beast Vulture nữa.<br>Cho cả thăn gà lên cơm rồi làm thành tô cơm yakitori nhé!",
"Thịt cổ Flare Fox thì chắc đem nướng giấy bạc với nấm.<br>Nấu chín kỹ sẽ ngon hơn mà.",
"À! Xương vẫn còn cả đây nên cũng không thể quên sườn được.<br>Đặc biệt là ta có thể thưởng thức đủ sườn bò‚ gà và heo luôn đấy♪",
"Vừa trò chuyện‚ cô vừa lướt dao điêu luyện‚<br>còn nguyên liệu trên lửa trại cũng dần được làm chín.",
"……N‚ này! Không phải lúc đứng nhìn đâu!<br>Chúng ta cũng phải nấu mau lên‚ không là thua vì bỏ cuộc đấy!",
"Đúng vậy đại ca!",
"Những người tham gia khác đang ngẩn người nhìn cũng vội vàng bắt đầu nấu.<br>Mùi hương kích thích vị giác dần lan khắp hội trường.",
"Vậy thì‚ chúng ta bước vào phần chấm điểm nào!<br>Với tư cách giám khảo‚ tôi sẽ đánh giá thật nghiêm khắc và công bằng!",
"――Tôi đã muốn nói như vậy đấy.<br>Nhưng chỗ này…… hơi quá nhiều để một mình tôi ăn hết nhỉ……",
"Trước mặt Alicia‚ vị giám khảo‚ bày la liệt vô số món ăn‚<br>đến mức mỗi món chỉ nếm một miếng cũng đã là hết sức.",
"Vì vậy…… mọi người ơi!<br>Hãy cùng ăn và cùng chấm điểm nào!",
"Ồồồồồồ!",
"Các thợ săn và khán giả đã đói đến giới hạn<br>hào hứng cắn ngập vào những món ăn――",
"Đúng là Ash Boar‚ hương vị hoang dã mà vẫn tinh tế!<br>Hiện tại thì món này là nhất‚ nhỉ.",
"Hừ‚ làm gì có thợ săn nào thắng nổi tao chứ!",
"Quá đỉnh đại ca!",
"Nhưng…… cuối cùng vẫn còn món này nhỉ.<br>Ushitoributa của cô Diana……",
"Mình đã nấu chậm để có thể đem ra ở nửa sau mà‚ giờ là lúc ngon nhất đấy!",
"Ushitoributa mà mình và Chỉ Huy cùng săn!<br>Mình thật sự rất tự tin đó~‚ nào nào‚ mời mọi người thưởng thức~♪",
"Vậy thì…… xin phép dùng bữa!",
"――!? Ưưư～～～!?",
"C‚ cái này…… ngon…… ngon quá mức luôn!<br>Cứ như toàn bộ món ăn trước đây đều trở thành nền tôn món Ushitoributa vậy!",
"Cái…… Ash Boar của tao chỉ là nền tôn món khác á!?<br>Đừng đùa! Này‚ cho tao ăn thử!",
"……Không‚ thể nào…… so với thứ này thì thịt của tao còn chẳng phải thịt…….<br>Không thể nào…… làm sao lại có chênh lệch lớn đến thế được……",
"Đại ca…… món này ngon thật đấy……",
"Không chỉ hai ứng viên vô địch‚ các thợ săn<br>cứ mỗi lần nếm Ushitoributa lại gục xuống khuỵu gối.",
"Mọng nước và mềm‚ vậy mà vẫn giữ chắc cảm giác thớ thịt!<br>Sao lại ngon đến thế này chứ……!",
"Hãy phục vụ món này trong đám cưới của chúng ta nhé‚ em yêu!",
"Thứ này ngay cả ở chính quốc Miresgard tôi cũng chưa từng ăn……",
"Ừ…… chắc chắn giới quý tộc sẽ đổ xô mua cho xem……",
"Một con vật đột biến vì nhiễm chướng khí.<br>Ngon được đến mức này đúng là kỳ tích……",
"Không thắng nổi kỳ tích đâu nhỉ.<br>Hãy thành thật thừa nhận thất bại thôi.",
"……Có vẻ mọi người cũng không phản đối nhỉ.<br>Vậy thì‚ người chiến thắng cuộc thi săn tại căn cứ tiền tuyến là――",
"――Ơơ? Món của mọi người cũng ngon lắm mà?",
"Cô Diana…… ơi……?<br>Ơ‚ chuyện này……?",
"Nhìn này‚ món Ash Boar này được khử mùi rất kỹ bằng thảo mộc‚<br>bên ngoài giòn thơm còn bên trong mọng nước! Tuyệt nhất luôn~!",
"Diana‚ cô…….<br>Tôi đã cản trở cô nhiều đến vậy mà cô vẫn bảo món của tôi ngon sao……?",
"Tất nhiên rồi! Đây thật sự là một giải đấu vui mà‚<br>chẳng có chuyện khó chịu nào cả♪",
"À‚ con Grass Deer bên này được đem nướng à?<br>Lại còn hun khói để thêm hương nữa! Làm mình muốn uống rượu ghê~.",
"Còn bên này thì sao? Chân Crest Rabbit!?<br>Đặc sản hiếm đúng không!? Mình xin một miếng được không!?",
"……Ph‚ phải làm sao đây……?",
"Như cô thấy đấy.<br>Diana không quan tâm thắng thua đâu.",
"Giải đấu này đã vui hết mức rồi.<br>Ngoài chuyện đó ra‚ cô ấy chẳng cần gì khác.",
"……Như vậy có được không‚ Chỉ Huy?<br>Dù anh đã nói nhất định sẽ vô địch……",
"Không phải là vì Diana đâu……<br>Nhưng tôi cũng muốn giải đấu này kết thúc trong vui vẻ.",
"……Tôi hiểu rồi.<br>Vì mọi người đang vui vẻ và hạnh phúc đến thế này mà……",
"E hèm! Tôi xin công bố lại!<br>Cuộc thi săn lần này――tất cả mọi người đều vô địch!",
"Hãy cùng mọi người<br>ăn sạch nguyên liệu tuyệt vời nhất này nào!",
"Tiếng reo hò ồồồồồ vang lên từ tất cả mọi người‚<br>và cuộc thi săn càng lúc càng náo nhiệt hơn.",
"Chỉ Huy‚ cậu có ăn không đấy~?",
"Có chứ‚ tôi đang ăn đây.<br>Món nào cũng ngon nên tôi đang phân vân không biết nên lấy thêm món nào.",
"Ừm ừm‚ đúng là nỗi băn khoăn vui vẻ nhỉ!<br>Cậu thích món nào nhất?",
"Ushitoributa quả thật ngon kinh khủng.<br>Nhưng mà…… ừm‚ để xem nào.",
"Nếu buộc phải chọn thì――sau khi quyết định tha thứ cho bọn họ‚<br>tôi thấy thịt boar mà họ săn cũng khá ngon.",
"Nói ngắn gọn là thứ hạng chẳng còn quan trọng nữa‚<br>chỉ cần hôm nay thật vui là được‚ đúng không.",
"Hì hì…… ừm‚ ừm!<br>Tốt quá‚ vì với cậu đây cũng trở thành một kỷ niệm vui!",
"Mình cũng vui lắm.<br>Thật sự may quá vì có cậu ở bên……!",
"Hừm‚ nếu không có tôi thì em đã chẳng săn được Ushitoributa đâu.<br>Là tôi‚ một cộng sự đáng tin cậy chứ không phải kẻ vướng chân!",
"Không phải vì chuyến săn thuận lợi đâu.",
"Cả lúc vui lẫn lúc khổ‚ cậu đều không giấu mà bộc lộ ra ngoài‚<br>lắng nghe mình nói và cùng mình suy nghĩ……",
"Vì được ở cùng cậu‚ người đã tận hưởng cuộc săn đúng như lòng mình muốn‚<br>nên mình mới có khoảng thời gian tuyệt vời nhất♪",
"Diana……",
"Lần sau lại cùng đi săn nhé!<br>Lần tới chắc chắn cũng sẽ vui hết mức!",
"……Được ăn ngon đến thế này rồi thì khó mà từ chối lắm.<br>Được thôi‚ lúc nào tôi cũng đi cùng em.",
"Hay quá! Mình đã nghĩ sẵn con mồi muốn nhắm tới tiếp theo rồi~♪",
"Có vẻ ở cái ao gần Đại Huyệt có loài cá hễ đem khỏi nước là bốc cháy…….<br>Mình nghe nói ăn sống kiểu nhảy múa sẽ vui lắm!",
"……Thôi‚ tôi xin phép rút lại.<br>Lưỡi tôi sẽ bị bỏng mất……",
"Tại sao chứ~!?<br>Đi cùng mình đi mà! Chắc chắn sẽ vui lắm đó!!!",
]

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def split_lines_keep(text):
    return text.splitlines(keepends=True)

def newline_style(b):
    return 'CRLF' if b.count(b'\r\n') == b.count(b'\n') and b.count(b'\n') else 'LF'

def text_idx(parts):
    return TEXT_CMDS.get(parts[0])

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:[A-Za-z_][A-Za-z0-9_]*|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}', s)

def field_no_eol(line):
    return line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith('\n') else line

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    src_b = EN_ASSET.read_bytes()
    bom = src_b.startswith(b'\xef\xbb\xbf')
    text = src_b.decode('utf-8-sig')
    lines = split_lines_keep(text)
    recs = []
    for idx, line in enumerate(lines, 1):
        body = field_no_eol(line)
        parts = body.split(',') if body else ['']
        if parts and parts[0] in TEXT_CMDS:
            recs.append((idx, parts[0], text_idx(parts[0] if False else parts), parts))
    if len(recs) != len(VI):
        raise SystemExit(f'Translation count mismatch: {len(VI)} vs records {len(recs)}')
    new_lines = list(lines)
    entries = []
    blockers = []
    for n, (line_no, cmd, tidx, parts) in enumerate(recs):
        vi = VI[n]
        if ',' in vi:
            blockers.append({'line': line_no, 'type': 'ASCII_COMMA_IN_VI', 'text': vi})
        if tidx is None or tidx >= len(parts):
            blockers.append({'line': line_no, 'type': 'FIELD_INDEX_ERROR'})
            continue
        src_text = parts[tidx]
        if tags(src_text) != tags(vi):
            blockers.append({'line': line_no, 'type': 'TAG_MISMATCH', 'src': tags(src_text), 'vi': tags(vi)})
        if placeholders(src_text) != placeholders(vi):
            blockers.append({'line': line_no, 'type': 'PLACEHOLDER_MISMATCH', 'src': placeholders(src_text), 'vi': placeholders(vi)})
        new_parts = parts[:]
        new_parts[tidx] = vi
        eol = '\r\n' if lines[line_no-1].endswith('\r\n') else '\n' if lines[line_no-1].endswith('\n') else ''
        new_line = ','.join(new_parts) + eol
        if new_line.count(',') != lines[line_no-1].count(','):
            blockers.append({'line': line_no, 'type': 'DELIMITER_COUNT_MISMATCH', 'src_commas': lines[line_no-1].count(','), 'vi_commas': new_line.count(',')})
        new_lines[line_no-1] = new_line
        entries.append({'ordinal': n+1, 'line': line_no, 'command': cmd, 'source_text': src_text, 'vi_text': vi, 'match_status': 'EXACT', 'translation_status': 'TRANSLATED'})
    out_text = ''.join(new_lines)
    out_b = (b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
    VI_ASSET.write_bytes(out_b)
    delimiter_mismatches=[]; tech_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; unchanged=[]
    out_lines = split_lines_keep(out_b.decode('utf-8-sig'))
    for i,(a,bline) in enumerate(zip(lines,out_lines),1):
        if a.count(',') != bline.count(','):
            delimiter_mismatches.append(i)
        ab = field_no_eol(a); bb = field_no_eol(bline)
        ap = ab.split(',') if ab else ['']; bp = bb.split(',') if bb else ['']
        if ap and ap[0] in TEXT_CMDS:
            ti = TEXT_CMDS[ap[0]]
            if ap[:ti]+ap[ti+1:] != bp[:ti]+bp[ti+1:]: tech_mismatches.append(i)
            if tags(ap[ti]) != tags(bp[ti]): tag_mismatches.append(i)
            if placeholders(ap[ti]) != placeholders(bp[ti]): placeholder_mismatches.append(i)
            if ap[ti] == bp[ti]: unchanged.append(i)
        elif ab != bb:
            tech_mismatches.append(i)
    qa_status = 'PASS' if not blockers and not delimiter_mismatches and not tech_mismatches and not tag_mismatches and not placeholder_mismatches and not unchanged and len(lines)==len(out_lines) else 'FAIL'
    diff_src=[]; diff_dst=[]
    for e in entries:
        diff_src.append(f"L{e['line']} {e['command']}: {e['source_text']}\n")
        diff_dst.append(f"L{e['line']} {e['command']}: {e['vi_text']}\n")
    diff = ''.join(difflib.unified_diff(diff_src, diff_dst, fromfile='source_text_fields', tofile='vi_text_fields', lineterm='\n'))
    (WORK/'focused_diff.md').write_text(diff, encoding='utf-8')
    counts = {c: sum(1 for _,cmd,_,_ in recs if cmd==c) for c in TEXT_CMDS}
    manifest = {
        'scene': SCENE,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_asset': str(EN_ASSET),
        'output_asset': str(VI_ASSET),
        'ja_json': str(JA_JSON),
        'en_json': str(EN_JSON),
        'source': {'sha256': sha256(src_b), 'bytes': len(src_b), 'bom': bom, 'newline': newline_style(src_b), 'line_count': len(lines)},
        'output': {'sha256': sha256(out_b), 'bytes': len(out_b), 'bom': out_b.startswith(b'\xef\xbb\xbf'), 'newline': newline_style(out_b), 'line_count': len(out_lines)},
        'candidate_counts': counts,
        'candidate_total': len(recs),
        'translated_total': len(entries),
        'qa_status': qa_status,
        'entries': entries,
        'artifacts': {'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'script': str(WORK/'generate_vi.py')},
        'notes': ['JP asset text matched novel order; EN novel values are blank for this scene‚ so JP was primary and EN asset/asset text order was used for alignment.', 'Diana voice: playful boku/kimi localized mostly as mình/cậu; explicit 司令官くん translated as Chỉ Huy.', 'No H18/adult lines found in this scene.']
    }
    qa = {
        'scene': SCENE,
        'qa_status': qa_status,
        'blockers': blockers,
        'structural_checks': {
            'line_count_match': len(lines)==len(out_lines),
            'delimiter_mismatches': delimiter_mismatches,
            'technical_field_mismatches': tech_mismatches,
            'tag_mismatches': tag_mismatches,
            'placeholder_mismatches': placeholder_mismatches,
            'unchanged_text_records': unchanged,
            'candidate_counts': counts,
            'translated_total': len(entries),
        },
        'linguistic_notes': manifest['notes'],
        'manual_review_items': []
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'qa_status': qa_status, 'output': str(VI_ASSET), 'manifest': str(WORK/'manifest.json'), 'qa_log': str(WORK/'qa_log.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'counts': counts, 'blockers': blockers}, ensure_ascii=False, indent=2))
    if qa_status != 'PASS':
        raise SystemExit(1)
if __name__ == '__main__':
    main()
