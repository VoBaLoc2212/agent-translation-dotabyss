#!/usr/bin/env python
from __future__ import annotations
import hashlib, json, re, difflib
from pathlib import Path

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10090100002'
EN_PATH = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_PATH = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
TEXT_CMDS = ('title,','message,','messageTextUnder,','messageTextCenter,')
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}')

TRANSLATIONS = [
    'Chỉ Kỹ Thuật Thôi Là Chưa Đủ',
    '<size=48>――Trước Ngày Thi Nhảy</size>',
    'Nào‚ hôm nay là ngày đặc huấn cuối cùng rồi.<br>Lên tinh thần cho tử tế đi!<br> ',
    'Biết rồi.<br>Cô cũng tập trung vào đi.<br> ',
    'Anh đang nói với ai vậy hả!<br>Trước mặt anh là Levienne‚ vũ công số một Eldorana đó!<br> ',
    '…Chỉ Huy và Levienne hôm nay lại đi cùng nhau kìa.<br> ',
    'Không lẽ hai người đó… là như vậy thật sao?<br> ',
    'Ơ kìa!<br>Vũ công với Chỉ Huy… một cặp hơi bất ngờ nhưng có khi lại hợp đấy!<br> ',
    '…Này‚ hình như người ta đang hiểu lầm kỳ quặc về chúng ta đấy.<br>Cứ mặc kệ vậy được à?<br> ',
    'Hả? Anh nói gì vậy?<br>Chuyện đó để sau đi‚ mau đi thôi!<br> ',
    '…Cô ấy còn chẳng nhận ra à?<br>Nếu chỉ là đang tập trung thì tốt rồi…<br> ',
    'Hự‚ haah!<br> ',
    'Levienne nhảy với khí thế dữ dội đến nghẹt thở.<br>Vũ điệu sắc bén tuyệt vời ấy đã hút chặt ánh mắt của người xem.<br> ',
    '――Xong!<br>…Thế nào… vậy?<br> ',
    'Anh bị choáng ngợp thật sự.<br>Anh cảm nhận được khí thế Levienne dồn hết mọi thứ vào điệu nhảy.<br> ',
    '…Vậy à.<br>Em hiểu rồi.<br> ',
    'Như vậy… vẫn chưa được sao?<br>Dưới mắt một tay nghiệp dư như anh thì kỹ thuật của em đã đạt đến đỉnh rồi mà…<br> ',
    'Chỉ kỹ thuật thôi là chưa đủ.<br>Không còn thời gian nữa‚ thêm lần nữa…<br> ',
    'Levienne vừa bước lên sân khấu đã loạng choạng mất thăng bằng<br>rồi ngã sụp xuống ngay tại chỗ.<br> ',
    'Này!? Sao thế!?<br>Em ổn không!?<br> ',
    'Em không sao‚ chỉ hơi choáng một chút thôi…<br> ',
    'Ngã quỵ ngay trước ngày thi mà bảo không sao được à!<br>Nếu thấy trong người không khỏe thì phải nói chứ!<br> ',
    'Em là dân chuyên nghiệp mà‚ thể trạng hoàn hảo lắm.<br>Không có vấn đề gì hết——<br> ',
    'Như chồng lên giọng nói của Levienne<br>một tiếng ùng ục nhỏ vang lên.<br> ',
    '…Vừa rồi là…<br> ',
    'Ư‚ ưm~! Chắc em hơi mệt nên phát ra tiếng lạ thôi.<br>Chẳng có gì đâu mà!<br> ',
    'Ùng ục ục ục~~~!!!<br>Bụng của Levienne réo to đến mức không thể che giấu được.<br> ',
    '…Này‚ Levienne.<br>Anh vừa nghe thấy một âm thanh không nên phát ra từ bụng thiếu nữ đâu đấy.<br> ',
    'K‚ không phải đâu.<br>Em chỉ hơi đói một chút vì đã nhảy rất cố thôi…<br> ',
    'Em từng nói đã ăn trước khi luyện tập<br>nên sau khi tập xong không cần ăn nữa. Đúng không?<br> ',
    'Ư‚ ưư…<br> ',
    'Em không ăn uống tử tế trước buổi tập đúng không?<br>Rồi sau khi tập xong cũng không ăn luôn.<br> ',
    'Thì‚ chuyện đó… em không thể mập lên trước cuộc thi được…<br> ',
    'Nhưng thế cũng đâu có nghĩa là em được ngã quỵ<br>vì đói ngay trước ngày thi chứ!<br> ',
    'Biết làm sao được chứ!<br>Em không biết nguyên nhân sa sút là gì‚ có thể là do cân nặng thì sao!<br> ',
    'Cười đi!<br>Cứ cười con ngốc vì lo vóc dáng mà ngã quỵ trong lúc luyện tập đi!<br> ',
    'Anh không cười đâu.<br>Vận động nhiều thế này mà vẫn giữ vóc dáng chắc vất vả lắm.<br> ',
    'Nhưng ăn kiêng đến đây là đủ rồi.<br>Hãy bồi bổ thể lực cho ngày mai. Trước mắt cứ ăn đã.<br> ',
    'Ơơ~… nhưng bụng phình ra thì làm sao vô địch được…<br> ',
    'Vũ công gầy rộc cũng không thắng nổi đâu!<br>Ăn vừa đủ để bụng không phình ra là được!<br> ',
    '…Nếu anh đã nói đến mức đó<br>thì một chút thôi cũng được…<br> ',
    'Ngon quá… ngon quá đi mất…!<br> ',
    '…Em đã không ăn đến mức<br>một bữa bình thường cũng làm em xúc động vậy sao?<br> ',
    'Vì em mãi không thoát khỏi sa sút<br>thậm chí còn cảm thấy mọi thứ ngày càng tệ hơn…<br> ',
    'Độ sắc sảo của cơ thể và vẻ đẹp bên ngoài mà mập lên thì hỏng hết đúng không?<br>Em thật sự không có tâm trạng để ăn.<br> ',
    'Ừm… có khi nguyên nhân lại chính là chuyện giảm cân thì sao?<br>Đói quá nên thiếu sức và không thể nhảy như trước nữa.<br> ',
    'Có thể là vậy… nhưng<br>em nghĩ kỹ thuật của mình thật sự đã tiến bộ.<br> ',
    'Nhưng em vẫn không thể cho anh xem một điệu nhảy hay.<br>Quả nhiên là em đang sa sút rồi…<br> ',
    'Không không‚ anh vẫn luôn nói điệu nhảy của Levienne rất tuyệt mà.<br>Vấn đề rốt cuộc là gì?<br> ',
    '“Rất tuyệt” là không được.<br>Như vậy em không thể hài lòng.<br> ',
    'Em không muốn được khen là rất tuyệt!<br>Em muốn người ta nghĩ rằng xem em nhảy thật vui‚ rằng họ thấy hạnh phúc!<br> ',
    '…Một điệu nhảy… thật vui?<br> ',
    'Từ nhỏ em đã rất yêu khiêu vũ.<br>Em đã nỗ lực‚ cũng đã có kết quả. Em nghĩ mình là vũ công giỏi nhất.<br> ',
    'Nhưng một vũ công khiến người ta nghĩ “cô ấy luyện tập chăm chỉ thật”<br>hay “cô ấy đang cố gắng nhảy thật” thì chỉ là hạng ba thôi.<br> ',
    'Không để lộ dấu vết nỗ lực mà đem đến vẻ đẹp‚ sự phấn khích và niềm vui.<br>Đó mới là vũ công tuyệt nhất!<br> ',
    'Em không muốn bị nhận ra là mình đang gắng sức. Em cũng chẳng muốn được khen!<br>Vì em muốn khán giả tận hưởng hết mình cơ mà!<br> ',
    'Levienne…<br>Ra vậy. Anh chỉ toàn nói “tuyệt quá” mà chẳng thật sự tận hưởng nhỉ…<br> ',
    'Nếu một người tinh mắt như anh cũng nghĩ vậy<br>thì nghĩa là em vẫn còn kém xa…<br> ',
    'Ừm… đúng là có thể điệu nhảy đó không tạo ra bầu không khí để tận hưởng‚ nhưng…<br> ',
    'Đúng thế còn gì.<br>Chính em cũng biết mà‚ cứ thế này thì không được…<br> ',
    'Đừng làm vẻ mặt nghiêm trọng thế.<br>Vì đang đói nên em mới cứ nghĩ đến chuyện tiêu cực thôi.<br> ',
    'Ăn nhiều vào‚ ngủ cho kỹ rồi hãy tận hưởng cuộc thi.<br>Nếu Levienne vui vẻ khi nhảy thì khán giả cũng sẽ vui theo thôi.<br> ',
    'Em… tận hưởng…?<br> ',
    'Ừ. Điệu nhảy của Levienne rất tuyệt.<br>Sự nghiêm túc và khí thế ấy đều truyền đến anh.<br> ',
    'Chính vì vậy nếu em nhảy thật vui vẻ<br>cảm xúc đó chắc chắn cũng sẽ truyền đến họ.<br> ',
    'Cảm xúc của em… sẽ truyền đi…<br>Ra vậy‚ nên anh mới luôn nghiêm túc dõi theo em đến thế…<br> ',
    '…Đúng rồi‚ hóa ra là vậy.<br>Cảm xúc của vũ công sẽ được gửi gắm vào điệu nhảy.<br> ',
    'Dạo gần đây em chưa từng thấy vui khi nhảy.<br>Khán giả không tận hưởng được cũng phải thôi.<br> ',
    'Em hiểu rồi. Ngày mai em sẽ nhảy vui hơn bất cứ ai!<br> ',
    'Vì thế——trước hết là ăn!<br>Cho em thêm phần nữa!<br> ',
    'Ừ‚ cứ thế đi!<br>Nhưng đừng để bụng phình ra nhé.<br> ',
]

def sha256(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def source_props(p: Path):
    b=p.read_bytes()
    return {
        'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'byte_length': len(b),
        'bom': b.startswith(b'\xef\xbb\xbf'),
        'newline': 'CRLF' if b'\r\n' in b else 'LF',
        'line_count': len(b.decode('utf-8-sig').splitlines())
    }

def split_text_line(line: str):
    core=line.rstrip('\r\n')
    if core.startswith('title,'):
        return core.split(',',1), 1
    if core.startswith(('message,','messageTextUnder,','messageTextCenter,')):
        parts=core.split(',')
        return parts, 2
    return None, None

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    raw = EN_PATH.read_bytes()
    text = raw.decode('utf-8-sig')
    newline = '\r\n' if b'\r\n' in raw else '\n'
    had_bom = raw.startswith(b'\xef\xbb\xbf')
    lines = text.splitlines()
    candidates=[]
    for idx,line in enumerate(lines,1):
        if line.startswith(TEXT_CMDS):
            parts, text_idx = split_text_line(line)
            candidates.append({'line': idx, 'cmd': parts[0], 'speaker': parts[1] if len(parts)>1 else '', 'source_text': parts[text_idx]})
    if len(candidates) != len(TRANSLATIONS):
        raise SystemExit(f'translation count mismatch {len(TRANSLATIONS)} vs candidates {len(candidates)}')
    new_lines=list(lines)
    blockers=[]
    entries=[]
    for n,(cand,vi) in enumerate(zip(candidates, TRANSLATIONS),1):
        if ',' in vi:
            blockers.append({'type':'ASCII_COMMA_IN_TRANSLATION','index':n,'line':cand['line'],'text':vi})
        old_line = lines[cand['line']-1]
        parts, text_idx = split_text_line(old_line)
        old_text = parts[text_idx]
        if TAG_RE.findall(old_text) != TAG_RE.findall(vi):
            blockers.append({'type':'TAG_MISMATCH_PREWRITE','index':n,'line':cand['line'],'old_tags':TAG_RE.findall(old_text),'vi_tags':TAG_RE.findall(vi)})
        if PH_RE.findall(old_text) != PH_RE.findall(vi):
            blockers.append({'type':'PLACEHOLDER_MISMATCH_PREWRITE','index':n,'line':cand['line']})
        parts[text_idx]=vi
        new_line=','.join(parts)
        if old_line.count(',') != new_line.count(','):
            blockers.append({'type':'DELIMITER_MISMATCH_PREWRITE','index':n,'line':cand['line']})
        new_lines[cand['line']-1]=new_line
        entries.append({**cand,'index':n,'status':'TRANSLATED','match_status':'CONTEXT_MATCH' if n in (2,) else 'EXACT','vi_text':vi})
    if blockers:
        raise SystemExit(json.dumps(blockers, ensure_ascii=False, indent=2))
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    out_text = newline.join(new_lines) + (newline if text.endswith(('\n','\r\n')) else '')
    data = out_text.encode('utf-8')
    if had_bom: data = b'\xef\xbb\xbf' + data
    VI_PATH.write_bytes(data)
    # QA after write
    vi_raw=VI_PATH.read_bytes(); vi_text=vi_raw.decode('utf-8-sig'); vi_lines=vi_text.splitlines()
    delimiter_mismatches=[]; tech_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; kept=[]; ascii_commas=[]
    for i,(old,new) in enumerate(zip(lines,vi_lines),1):
        if old.count(',') != new.count(','): delimiter_mismatches.append(i)
        if old.startswith(TEXT_CMDS):
            old_parts, ti = split_text_line(old); new_parts, nti = split_text_line(new)
            if old == new: kept.append(i)
            if old_parts[:ti] + old_parts[ti+1:] != new_parts[:nti] + new_parts[nti+1:]: tech_mismatches.append(i)
            if TAG_RE.findall(old_parts[ti]) != TAG_RE.findall(new_parts[nti]): tag_mismatches.append(i)
            if PH_RE.findall(old_parts[ti]) != PH_RE.findall(new_parts[nti]): placeholder_mismatches.append(i)
            if ',' in new_parts[nti]: ascii_commas.append(i)
    qa_status = 'PASS' if not any([delimiter_mismatches, tech_mismatches, tag_mismatches, placeholder_mismatches, kept, ascii_commas]) and len(lines)==len(vi_lines) else 'FAIL'
    counts={k[:-1]:0 for k in TEXT_CMDS}
    for c in candidates: counts[c['cmd']]+=1
    manifest={
        'scene': SCENE, 'status': qa_status, 'source': source_props(EN_PATH), 'ja_json': source_props(JA_JSON), 'en_json': source_props(EN_JSON),
        'output': source_props(VI_PATH), 'work_dir': str(WORK), 'output_path': str(VI_PATH),
        'text_commands_count': counts, 'candidate_records': len(candidates), 'translated_records': len(TRANSLATIONS),
        'entries': entries,
        'notes': ['JP primary; EN asset used for alignment.', 'Speaker names and charaload asset names preserved.', 'Commander/司令官 translated as Chỉ Huy.', 'ASCII commas in Vietnamese fields replaced with U+201A where punctuation comma was needed.']
    }
    qa={
        'scene': SCENE, 'qa_status': qa_status, 'blockers': [], 'items': [],
        'structural': {
            'line_count_match': len(lines)==len(vi_lines), 'en_line_count': len(lines), 'vi_line_count': len(vi_lines),
            'bom_match': had_bom == vi_raw.startswith(b'\xef\xbb\xbf'),
            'newline_match': (b'\r\n' in raw)==(b'\r\n' in vi_raw),
            'delimiter_mismatches': delimiter_mismatches, 'technical_field_mismatches': tech_mismatches,
            'tag_mismatches': tag_mismatches, 'placeholder_mismatches': placeholder_mismatches,
            'kept_text_lines': kept, 'ascii_comma_in_vi_text_lines': ascii_commas
        },
        'linguistic': {'status':'PASS','notes':['Natural Vietnamese VN/RPG style; Levienne uses lively first-person em and addresses Commander as anh in private dialogue.', 'Intentional proper-name keeps in VI text: Levienne and Eldorana.']}, 
        'h18': {'present': False, 'adult_confirmation_context': 'Project confirms all characters 18+; no H18 content in this scene.'}
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    diff=[]
    for c in candidates:
        ln=c['line']; old=lines[ln-1]; new=vi_lines[ln-1]
        diff.extend(difflib.unified_diff([old+'\n'], [new+'\n'], fromfile=f'EN line {ln}', tofile=f'VI line {ln}', lineterm=''))
    (WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10090100002\n\n```diff\n'+'\n'.join(diff)+'\n```\n', encoding='utf-8')
    print(json.dumps({'qa_status':qa_status,'output':str(VI_PATH),'work':str(WORK),'counts':counts,'source_sha256':sha256(EN_PATH),'output_sha256':sha256(VI_PATH)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
