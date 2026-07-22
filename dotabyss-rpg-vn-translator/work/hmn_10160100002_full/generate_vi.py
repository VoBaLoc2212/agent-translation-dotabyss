# -*- coding: utf-8 -*-
from __future__ import annotations
import hashlib, json, re, difflib
from pathlib import Path

SCENE = 'hmn_10160100002'
ROOT = Path('E:/AgentTranslation')
EN = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work'/f'{SCENE}_full'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
TEXT_PREFIXES = ('title,','message,','messageTextUnder,','messageTextCenter,')
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}')

translations = [
    'Tiêu Đề',
    '<size=48>――Quán Rượu Căn Cứ Tiền Tuyến</size>',
    'Ngày hôm sau khi gặp Wisteria trong rừng‚ %user% đi đến<br>quán rượu của Căn Cứ Tiền Tuyến.<br> ',
    '...Ludia‚ cô rảnh một chút không?<br> ',
    'Ôi‚ giờ này ban ngày mà có chuyện gì thế? Anh muốn uống rượu sao?<br> ',
    'Tôi đang tìm một người nên muốn hỏi thông tin.<br>Là Wisteria‚ cung thủ lão luyện.<br> ',
    'Wisteria...<br>Cô ấy là người được gọi là Chiến Thần nhỉ?<br> ',
    'Ừ‚ chính là cô ấy. Tôi có chút duyên gặp gỡ với cô ấy<br>nên định mời cô ấy đi ăn một bữa...<br> ',
    'Ôi chà♪<br>Quả không hổ là anh‚ luôn gặp được những mối duyên tốt nhỉ.<br> ',
    'Nhưng... khó rồi đây.<br>Tôi không có nhiều thông tin về Wisteria đâu.<br> ',
    'Ngay cả Ludia cũng vậy sao...?<br> ',
    'Vốn dĩ cô ấy là người thoắt ẩn thoắt hiện.<br>Đến mức tôi còn không biết cô ấy có dùng phòng trong doanh trại không.<br> ',
    'Vậy à... Được rồi‚ tôi sẽ tự đi tìm thêm một chút.<br> ',
    'Ừ‚ cố lên nhé♪<br> ',
    'Wisteria... ạ? Bọn em ở cùng đơn vị nhưng không thân thiết lắm...<br> ',
    'Cô có từng thấy cô ấy trong Căn Cứ Tiền Tuyến không?<br> ',
    'Dạ‚ em hầu như chưa từng thấy cô ấy nghỉ ngơi hay ăn uống.<br> ',
    'Ra vậy... cảm ơn.<br> ',
    'À‚ Wisteria hả? Khi nói chuyện thì cô ấy cũng chẳng phản ứng mấy<br>nên em chưa từng thật sự trò chuyện với cô ấy.<br> ',
    'Nhiều binh sĩ kính trọng cô ấy vì rất đáng tin trên chiến trường<br>nhưng chuyện riêng tư thì hoàn toàn...<br> ',
    'Quả nhiên là vậy... Thông tin đó giúp ích lắm‚ cảm ơn.<br> ',
    'Nếu là Chiến Thần thì thỉnh thoảng em thấy cô ấy đi mua đồ.<br> ',
    'Thật sao? Lúc đó trông cô ấy thế nào?<br> ',
    'Chủ yếu là mua lương thực ạ. Ngoài ra em cũng từng thấy cô ấy chuẩn bị dụng cụ cắm trại.<br> ',
    'Ra vậy... Xin lỗi vì đã làm mất thời gian của cô.<br> ',
    'Wisteria có vẻ không dùng phòng trong doanh trại.<br>Cô ấy cũng không ăn hay nghỉ ngơi trong căn cứ.<br> ',
    'Nhưng cô ấy vẫn đi mua sắm‚ tích trữ lương thực và chuẩn bị cho việc cắm trại.<br> ',
    'Và nếu xét đến nơi tôi đã gặp cô ấy trong rừng――.<br>Được‚ thử đến đó xem sao...!<br> ',
    'Xét theo nơi chúng tôi chạm mặt lần trước thì có lẽ là hướng này.<br>Ừm... nếu làm giống lần trước thì...<br> ',
    'A‚ tự nhiên thấy buồn đi quá! Chắc phải giải quyết một chút thôi!<br> ',
    'Nào‚ kéo quần xuống...<br> ',
    '――Đứng yên.<br> ',
    '...! Ừ‚ tôi sẽ không chống cự. Đừng mạnh tay nhé?<br> ',
    'Chỉ Huy quay lại khi quần vẫn đang tụt xuống. Đứng đó là Wisteria<br>với vẻ mặt hơi ngán ngẩm.<br> ',
    '...Quả nhiên là cậu. Tôi đã nghĩ bóng lưng này trông quen quen mà...<br> ',
    'Ha ha‚ tình cờ ghê nhỉ Wisteria.<br> ',
    'Sao cậu lại thong dong thế...<br>Đây đâu phải nơi có thể tình cờ gặp người khác.<br> ',
    'Vì sao cậu lại ở đây? Lại khảo sát địa hình à?<br> ',
    'Không‚ lần này tôi đến để gặp cô.<br> ',
    'Gặp tôi...? Chẳng lẽ cậu cứ đi lung tung để tìm tôi sao?<br> ',
    'Chỉ vì từng gặp tôi trong khu rừng này<br>đâu có nghĩa là sẽ có lần thứ hai...<br> ',
    'Không‚ tôi tin chắc cô sẽ tới.<br>Wisteria‚ căn cứ bí mật của cô ở quanh đây đúng không?<br> ',
    '…!?<br> ',
    'Sao cậu biết được!?<br> ',
    'Tôi suy luận từ thông tin thu thập ở căn cứ.<br>Tôi đoán cô đang cắm trại ở đâu đó.<br> ',
    '...Vì sao cậu lại đợi ở đây?<br>Nơi này đáng lẽ phải cách xa chỗ chúng ta gặp lần trước.<br> ',
    'Vì cô từng nói mình cẩn thận vòng ra sau lưng tôi.<br>Nghĩa là khi thấy tôi sắp đi giải quyết‚ cô đã cố ý vòng ra phía sau.<br> ',
    'Chỉ từ cuộc nói chuyện ngắn đó...!?<br> ',
    'Wisteria trông rất nghiêm túc mà.<br>Tôi nghĩ cô sẽ không cố ý nói dối đâu.<br> ',
    '...Cậu cũng đã thu thập thông tin về khu rừng này nhỉ.<br> ',
    'Từ thông tin về thảm thực vật và địa hình đã thu thập<br>cậu khoanh vùng những nơi thích hợp để cắm trại...<br> ',
    'Rồi cố ý để lộ sơ hở ở vị trí tôi sẽ nhận ra<br>và dụ tôi ra như thế này sao.<br> ',
    'Chính xác.<br> ',
    '...Tôi cứ tưởng mình giỏi lén bước<br>vậy mà lại bị dụ ra một cách hoàn hảo như thế.<br> ',
    'Có vẻ nhận định của tôi đã sai.<br>Cậu là một Chỉ Huy xuất sắc hơn tôi tưởng rất nhiều.<br> ',
    'Được cô khen vậy là vinh hạnh cho tôi rồi.<br> ',
    'Nhưng thật lạ là cậu lại thu thập được thông tin về tôi...<br> ',
    'Ở căn cứ đó đáng lẽ hầu như không có ai biết về tôi mới phải.<br> ',
    'Không đâu‚ mọi người đều để ý đến Wisteria đấy.<br>Đúng là Chiến Thần‚ cô nổi tiếng thật đấy.<br> ',
    'Tôi đâu có tự xưng như vậy. Làm gì có chuyện tôi nổi tiếng.<br> ',
    'Người cất công đến tìm tôi như thế này<br>chỉ có mình cậu thôi‚ Chỉ Huy.<br> ',
    'Tôi không nghĩ là vậy đâu...<br> ',
    'Đúng là tôi giỏi ẩn mật<br>nhưng ngay cả khi cư xử bình thường‚ rất nhiều người vẫn không nhận ra tôi.<br> ',
    'Nếu tôi xóa đi khí tức<br>thì có khi đứng ngay bên cạnh cũng không ai nhận ra.<br> ',
    'Không ai hứng thú với tôi cả. Dù là đồng đội cùng căn cứ cũng vậy.<br> ',
    'Ừm... có khi chỉ là vì Wisteria xóa khí tức quá giỏi thôi...<br> ',
    'Dù sao thì tôi cũng đã đến tận đây rồi. Cô có thể mời tôi đến căn cứ bí mật được không?<br> ',
    '...Tôi khó xử lắm. Tôi chưa từng mời ai đến đó cả.<br> ',
    'Tức là tôi sẽ là vị khách đầu tiên sao. Vinh hạnh thật đấy.<br> ',
    'Cậu đúng là người tích cực thật...<br>...Thôi được‚ giấu nơi cắm trại với cấp trên cũng là vấn đề nhỉ.<br> ',
    'Hơn nữa... nếu là cậu‚ người đã tìm thấy tôi...<br> ',
    'Được rồi‚ tôi sẽ dẫn đường.<br> ',
    'Thật sao? Cảm ơn cô‚ Wisteria.<br> ',
    '...Nhưng trước đó‚ Chỉ Huy. Ừm... chuyện... c-cái đó...<br> ',
    'Phía trước quần của cậu... đã kéo lại chưa...?<br> ',
    'Ừ‚ hôm nay không sao.<br>Tôi đã kéo lại đàng hoàng trước khi cô nói rồi.<br> ',
    'Wisteria‚ người vẫn luôn khẽ tránh ánh mắt‚ cuối cùng cũng nhìn<br>Chỉ Huy và thở phào nhẹ nhõm.<br> ',
    'Tôi thất lễ rồi.<br>Ấn tượng lần trước quá mạnh nên bất giác...<br> ',
    'Ồ‚ ra là vậy à. Vậy thì xin lỗi nhé.<br> ',
    'Thật sự là vậy... chẳng hiểu sao nó cứ mắc kẹt trong đầu tôi...<br> ',
    'Thỉnh thoảng tôi lại nhớ đến...<br>thậm chí còn xuất hiện trong mơ...<br> ',
    'Trong mơ...?<br> ',
    'K-không. Chuyện riêng của tôi thôi.<br>Quên đi.<br> ',
    'Nơi cắm trại của tôi ở hướng này.<br>Tôi không biết cậu có thấy thoải mái không... nhưng tôi chào đón cậu.<br> ',
]

def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def field_text(line):
    s=line.rstrip('\r\n').lstrip('\ufeff')
    if s.startswith('title,'):
        return s.split(',',1)[1]
    if s.startswith(('message,','messageTextUnder,','messageTextCenter,')):
        return s.split(',',5)[2]
    return None

def replace_text(line, new_text):
    eol='\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else '')
    core=line[:-len(eol)] if eol else line
    bom='\ufeff' if core.startswith('\ufeff') else ''
    bare=core.lstrip('\ufeff')
    if bare.startswith('title,'):
        pref, old = bare.split(',',1)
        return bom + pref + ',' + new_text + eol
    parts=bare.split(',',5)
    return bom + ','.join([parts[0], parts[1], new_text, *parts[3:]]) + eol

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    raw=EN.read_bytes()
    text=raw.decode('utf-8-sig')
    lines=text.splitlines(True)
    bom=raw.startswith(b'\xef\xbb\xbf')
    newline='CRLF' if b'\r\n' in raw else 'LF'
    text_idx=[]
    counts={k[:-1]:0 for k in TEXT_PREFIXES}
    for i,line in enumerate(lines,1):
        bare=line.lstrip('\ufeff')
        if bare.startswith(TEXT_PREFIXES):
            text_idx.append(i)
            counts[bare.split(',',1)[0]]+=1
    assert len(text_idx)==len(translations), (len(text_idx),len(translations))
    new_lines=lines[:]
    records=[]
    issues=[]
    for n,(line_no,vi_text) in enumerate(zip(text_idx, translations),1):
        old_line=lines[line_no-1]
        old_text=field_text(old_line)
        if ',' in vi_text:
            issues.append({'line':line_no,'issue':'ASCII_COMMA_IN_TRANSLATION_DRAFT'})
        if TAG_RE.findall(old_text or '') != TAG_RE.findall(vi_text):
            issues.append({'line':line_no,'issue':'TAG_MISMATCH_DRAFT','old_tags':TAG_RE.findall(old_text or ''),'new_tags':TAG_RE.findall(vi_text)})
        if sorted(PH_RE.findall(old_text or '')) != sorted(PH_RE.findall(vi_text)):
            issues.append({'line':line_no,'issue':'PLACEHOLDER_MISMATCH_DRAFT','old_ph':PH_RE.findall(old_text or ''),'new_ph':PH_RE.findall(vi_text)})
        new_line=replace_text(old_line, vi_text)
        if old_line.count(',') != new_line.count(','):
            issues.append({'line':line_no,'issue':'DELIMITER_COUNT_MISMATCH_DRAFT','old_commas':old_line.count(','),'new_commas':new_line.count(',')})
        new_lines[line_no-1]=new_line
        records.append({'record_index':n,'line':line_no,'command':old_line.lstrip('\ufeff').split(',',1)[0],'status':'TRANSLATED','source_asset_text':old_text,'vi_text':vi_text})
    if issues:
        raise SystemExit(json.dumps({'draft_issues':issues},ensure_ascii=False,indent=2))
    out=(''.join(new_lines)).encode('utf-8-sig' if bom else 'utf-8')
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out)
    diff=''.join(difflib.unified_diff(
        [l.rstrip('\r\n')+'\n' for l in lines],
        [l.rstrip('\r\n')+'\n' for l in new_lines],
        fromfile=str(EN), tofile=str(VI), lineterm='\n'))
    (WORK/'focused_diff.md').write_text('# Focused Diff: hmn_10160100002\n\n```diff\n'+diff+'\n```\n',encoding='utf-8')
    manifest={
        'scene':SCENE,
        'status':'GENERATED_PENDING_INDEPENDENT_VERIFY',
        'source_paths':{'ja_json':str(JA_JSON),'en_json':str(EN_JSON),'en_asset':str(EN)},
        'output_path':str(VI),
        'work_dir':str(WORK),
        'format':{'encoding':'utf-8-sig' if bom else 'utf-8','bom':bom,'newline':newline,'line_count':len(lines),'delimiter':'ASCII comma','translatable_commands':list(TEXT_PREFIXES)},
        'source_sha256':sha(EN),
        'output_sha256_preverify':hashlib.sha256(out).hexdigest(),
        'candidate_counts':counts,
        'translatable_records':len(text_idx),
        'translated_records':len(text_idx),
        'records':records,
        'notes':['JP ja.json used as primary source; en.json and EN asset used for ordered alignment.','Speaker/charaload names and technical fields preserved.','ASCII commas avoided in Vietnamese text fields; Vietnamese internal pauses use U+201A where needed.','All characters confirmed 18+ by project context; mild adult-adjacent gag translated normally.']
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    qa={
        'scene':SCENE,
        'qa_status':'GENERATED_PENDING_INDEPENDENT_VERIFY',
        'structural_precheck':{'line_count_match':len(lines)==len(new_lines),'bom_preserved':bom==(out.startswith(b'\xef\xbb\xbf')),'newline_preserved':newline,'candidate_counts':counts,'translatable_records':len(text_idx),'translated_records':len(text_idx),'draft_issues':issues},
        'linguistic_qa':{'jp_primary':True,'commander_term':'司令官/Commander -> Chỉ Huy','title_case':'Tiêu Đề','character_names_preserved':True,'adult_content_rule':'confirmed 18+; translated normally while preserving tone/consent'},
        'unresolved_items':[],
        'output_path':str(VI),
        'diff_path':str(WORK/'focused_diff.md')
    }
    (WORK/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'generated':str(VI),'records':len(text_idx),'work':str(WORK),'sha256':hashlib.sha256(out).hexdigest()},ensure_ascii=False,indent=2))
if __name__=='__main__':
    main()
