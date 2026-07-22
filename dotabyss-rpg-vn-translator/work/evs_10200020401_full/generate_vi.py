# -*- coding: utf-8 -*-
"""Generate Vietnamese asset for evs_10200020401 with structural QA artifacts."""
from pathlib import Path
import json, hashlib, re, difflib, datetime

ROOT = Path('E:/AgentTranslation')
SCENE = 'evs_10200020401'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/evs_10200020401_full'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
CMDS = ('title','message','messageTextUnder','messageTextCenter')

VI = [
    'Tiêu Đề',
    'Muốn quảng bá Đảo Quỷ…… nói cách khác là để mọi người nhân loại<br>biết được điểm hay của Đảo Quỷ thì phía giới thiệu phải hiểu Đảo Quỷ thật tường tận――<br> ',
    '――Vì lý do đó<br>trước hết em sẽ dẫn phu quân và mọi người đi tham quan nhé♪<br> ',
    'Ừ‚ nhờ em vậy.<br> ',
    'Trước tiên đây là cánh cổng có thể gọi là biểu tượng của Đảo Quỷ.<br>Thấy sao ạ? Được trang trí bằng đầu quỷ nên rất hoành tráng đúng không?<br> ',
    'Hoành tráng…… thì đúng là vậy.<br>Nhưng nói là rợn người thì hợp hơn.<br> ',
    'Ra là vậy…… thật thú vị. Nhìn là biết rõ bộ tộc nào sống ở đây<br>lại còn có thể uy hiếp ngoại địch. Hẳn là một dạng bùa trừ tà.<br> ',
    'Ơ? B-bùa trừ tà……? Ưm…… nó mang ý nghĩa chào mừng cơ mà……<br> ',
    '…………<br>Ra là vậy‚ thật thú vị.<br> ',
    'Cô không giấu nổi đâu. Mà ngay cả đèn lồng sau khi đi qua cổng<br>cũng có hình đầu quỷ nữa. Mới từ lối vào đã quá bất an rồi.<br> ',
    'Quả không hổ là phu quân‚ ngài tinh mắt lắm ạ! Thấy sao nào‚ ngầu đúng không?<br>Quỷ tộc là chủng tộc thấy những thứ rợn người thế này rất ngầu đấy ạ!<br> ',
    'Hơn nữa nhé‚ cánh cổng này còn có một cơ quan đặc biệt.<br>Nào nào‚ xin ngài đứng ngay trước mặt đầu quỷ này ạ.<br> ',
    'Chỗ này à?<br> ',
    "'Ôôôôôôô~~!! Có đứa trẻ hư nào ở đó khônggg~~!!'<br> ",
    'N-nó nói được……!? Với lại mắt con quỷ vừa sáng lên kìa!?<br> ',
    'Giọng nghe như vọng lên từ đáy địa ngục vậy.<br>Đám trộm cướp mà định tập kích ban đêm chắc cũng bỏ chạy bán sống bán chết.<br> ',
    'Ufufu‚ cơ quan này tuyệt lắm đúng không ạ?<br>Nó do những nghệ nhân quỷ tộc dốc hết tay nghề chế tác và được truyền lại qua nhiều đời đấy!<br> ',
    'Hề hề hề‚ hôm nay nó vẫn chạy ngon lắm nhỉ!<br>Dùng cái này đón tiếp thì đám trẻ con loài người chắc cũng thích mê cho xem!!<br> ',
    'Thích cái nỗi gì! Sợ quá rồi khóc thét lên thì có!!<br> ',
    'Ơ……? Thật vậy sao……? ……Ngầu thế này cơ mà?<br> ',
    'Khụ……! Hết cứu rồi‚ đám này……!<br>Cảm quan khác loài người quá xa……!<br> ',
    'Ơ‚ ưm…… p-phu quân‚ Đảo Quỷ còn nhiều điểm hấp dẫn khác nữa ạ!<br>Nhất là suối nước nóng! Rất hợp để xua tan mệt mỏi sau chuyến đi dài!<br> ',
    'Ồ? Vậy thì hay đấy. Quá hợp để tiếp đãi khách còn gì.<br>Dẫn bọn ta đi ngay được không?<br> ',
    'Vâng‚ chất nước ở đó tốt lắắắm luôn ạ~.<br>Phu quân cũng nhất định hãy xua tan mệt mỏi sau chuyến đi dài nhé♪<br> ',
    '……Này‚ Kureha. Đây…… là cái gì vậy?<br> ',
    'Cái gì là sao‚ suối nước nóng ạ?<br>Nơi phu quân đã mong chờ ấy.<br> ',
    '……Cái thứ đỏ rực như máu lại sôi ùng ục này là…… suối nước nóng……?<br> ',
    'Vâng. Thấy sao ạ‚ trông tuyệt đúng không?<br>Đây chính là danh thắng của Đảo Quỷ‚ Suối Nước Nóng Địa Ngục Cháy Bỏng♪<br> ',
    'Dễ chịu lắm nên nhân dịp này ngài vào ngâm thử thì sao ạ?<br>Em sẽ kỳ lưng cho ngài nữa~.<br> ',
    'Không không không‚ vào đó chắc chắn chết mất! Nước đó rốt cuộc bao nhiêu độ vậy!?<br> ',
    'Bây giờ thì…… 73 độ ạ.<br> ',
    'Gì chứ‚ nhiệt độ vừa đẹp còn gì.<br> ',
    'Chết là cái chắc!! Quỷ tộc các cô dai sức đến mức nào vậy!?<br>Với lại cái tên cũng đáng sợ quá rồi!!<br> ',
    'Cái tên hợp với ngoại hình đến thế anh còn bất mãn gì nữa chứ!<br> ',
    'Đưa khách đi thẳng sang thế giới bên kia thì được gì!<br>Quỷ tộc lệch sóng đến tận cùng luôn!<br> ',
    'Xin lỗi phu quân……<br>Quả nhiên việc quảng bá khó lắm sao ạ……<br> ',
    '……Đừng vội kết luận. Khó thì khó nhưng ta chưa nói là không thể.<br>Shiraes‚ cô nghĩ sao?<br> ',
    'Bản thân chất nước có vẻ tốt đấy.<br>Nếu dẫn nước sông hoặc nước ngầm vào để điều chỉnh nhiệt độ thì tôi nghĩ sẽ không vấn đề gì.<br> ',
    'Ồ? Đúng là mùi lưu huỳnh và bầu không khí cũng ra dáng khu suối nước nóng.<br>Nếu chỉnh sửa để cả phần trang trí này trông như một kiểu trình diễn…… liệu có ổn không?<br> ',
    '……Được. Kureha‚ cả mọi người quỷ tộc nữa‚ nghe ta nói.<br>Việc này sẽ lớn đấy nhưng hãy cố hết sức. Trước hết là――<br> ',
    'Để quảng bá cho quỷ tộc lệch sóng với loài người đến khó tin<br>%user% bắt đầu trình bày kế hoạch của mình――<br> ',
    '<size=48>――Ngày Hôm Sau</size>',
    '%user% đang đi đến lớp học ngoài trời của Shiraes<br>nơi dạy cách kết thân với loài người để kiểm tra tình hình thực hiện kế hoạch.<br> ',
    'Nào…… phía mình thì thuận lợi nhưng không biết Shiraes có làm ổn không.<br>Cô ấy hẳn phải hiểu cách kết thân với loài người hơn bất kỳ ai……<br> ',
    'Cô ấy nói sẽ mở lớp ngoài trời ở đây mà…… hửm?<br>Quỷ tộc đã tụ tập nhưng ai cũng ngẩn ra với vẻ mặt bối rối……?<br> ',
    'Gay thật…… giờ phải làm sao đây.<br> ',
    'Này‚ sao các cô không làm gì cả? Có vấn đề gì à?<br> ',
    'À‚ là phu quân đấy à. Chuyện là thế này‚ chị Shiraes ấy……<br> ',
    'Ừm…… làm thế nào để tiếp xúc với loài người rồi trở nên thân thiết sao……<br>Cách đó…… không‚ chưa đúng…… vậy thì cách kia…… hừưưm……<br> ',
    'Cô ấy cứ ngước lên trời rồi lẩm bẩm như thế<br>tính ra đã khoảng 5 tiếng rồi…… bọn tôi cũng không biết phải làm sao nữa.<br> ',
    'Lớp Shiraes lần thứ nhất dự kiến kết thúc trong 1 tiếng cơ mà!?<br>Cô ta định vượt giờ đến mức nào chỉ vì mải nghĩ vậy hả!<br> ',
    'Này! Shiraes! Quay về đi!<br>Không phải lúc ngồi nghĩ đâu! Mau tiếp tục bài học đi!<br> ',
    '――Ừ‚ quả nhiên chỉ có cách này thôi.<br>Cách để kết thân với loài người…… chính là cùng nhau trải qua thật nhiều thời gian!<br> ',
    'Fufufu‚ với tôi thì xem ra tôi đã tìm ra đáp án khá nhanh đấy.<br>Đây là thành quả của việc luôn học hỏi cách tiếp xúc với loài người.<br> ',
    'Đúng vậy‚ dù tính cách có khác nhau đến đâu thì chỉ cần sống cùng nhau khoảng 100 năm<br>và ăn chung một nồi cơm là chắc chắn sẽ thân thiết thôi.<br> ',
    'Thấy sao? Cậu không nghĩ đây là diệu kế à‚<br>Chỉ Huy?<br> ',
    'Xin lỗi vì đã để cô nghĩ lâu nhưng…… kế hoạch đó có một lỗ hổng chí mạng.<br>……Tuổi thọ của bọn ta không dài đến mức ấy.<br> ',
    'Aaaaa~~! Đ-đúng rồi nhỉ~~!<br>Tại sao tôi mãi vẫn không sửa được cảm giác thời gian của elf vậy chứ~~~!<br> ',
    'Không sao đâu ạ! Mama Shiraes đã cố gắng hết sức rồi!<br>Xin đừng tự xem thường mình như vậy!<br> ',
    'Đúng đó‚ chị đại! Bọn tôi cũng tin tưởng đại tỷ Shiraes mà!<br> ',
    'C-các cô…… sao mà tốt bụng đến thế chứ~~!<br>Thật sự‚ thật sự toàn là những đứa trẻ ngoan quá đi~~~! Tôi yêu các cô~~~!<br> ',
    'Mama Shiraes ơi!<br> ',
    'Đại tỷ~~~!<br> ',
    '(Đã thân nhau rồi sao‚ đám này…… không‚ khoan đã?<br>Lý do Shiraes được yêu mến đến thế―― chẳng phải gợi ý nằm ở đó sao?)<br> ',
    'Shiraes‚ ta muốn hỏi cô một chút.<br>Khi tiếp xúc với loài người‚ cô nghĩ gì vậy?<br> ',
    'Tôi à? Ừm…… cũng không đặc biệt ý thức điều gì cả.<br>Tôi chỉ tôn trọng các cậu và truyền đạt cảm xúc rằng tôi rất yêu loài người thôi.<br> ',
    'Truyền đạt cảm xúc sao…… ừ‚ đơn giản thật<br>nhưng có lẽ chính điều đó mới quan trọng.<br> ',
    'Điều đó…… ạ?<br> ',
    'Quỷ tộc cũng giống Shiraes‚ rất yêu loài người và có tấm lòng dịu dàng.<br>Vậy thì―― chỉ cần truyền đạt điều đó thôi. Không phải cứ bày mưu là được.<br> ',
    'Về chuyện đó‚ ta hãy nói thêm một chút cùng với Shiraes.<br>Biết đâu cách giải quyết lại đơn giản ngoài dự đoán đấy?<br> ',
    'Sau khi hiểu được tâm ý của quỷ tộc và cách truyền đạt nó<br>%user% sắp sửa khiến Đảo Quỷ thay đổi lớn lao――<br> ',
    '<size=48>――Vài Ngày Sau</size>',
    'Nhìn thấy đông đảo dân làng đang tiến về Đảo Quỷ<br>Kureha và mọi người mở to mắt kinh ngạc.<br> ',
    'T-tuyệt quá……! Nhiều người đến thế……!<br>Phu quân‚ rốt cuộc ngài đã làm thế nào vậy ạ!?<br> ',
    'Ta vốn giỏi khiến người khác hành động mà. Ta đã báo cho các làng gần đây.<br>Rằng họ được mời miễn phí đến điểm du lịch mới mở. Lại còn có quà lưu niệm―― như vậy đấy.<br> ',
    'Ban đầu họ cũng nghi ngờ nhưng cuối cùng thì như ngươi thấy đấy.<br>Kukukku―― loài người rất yếu trước hai chữ miễn phí mà! Đúng như ta nghĩ!<br> ',
    '……Cậu giấu chuyện đó là Đảo Quỷ sao? Nghe cứ như lừa gạt vậy……<br>Tôi không nhớ đã nuôi dạy cậu thành một tên tiểu nhân như thế đâu‚ Chỉ Huy.<br> ',
    'Dù vậy…… Kureha vẫn sẽ yêu phu quân mãi mãi<br>dù trong lòng ngài có tà ác đến đâu đi nữa……!<br> ',
    'M-mấy người thất lễ thật đấy…… thành công rồi thì được chứ sao.<br>Với lại nhìn kìa‚ quỷ tộc vui mừng đến mức nào!<br> ',
    'Ôôô……!<br>Loài người thật sự đến Đảo Quỷ của bọn ta chơi đông đến thế……!<br> ',
    'Được thấy cảnh tượng như thế này……! Cứ như mơ vậy còn gì nữa!<br> ',
    'Mọi người đều vui mừng nhỉ. Cứ xem như lời nói dối thiện ý đi.<br>Nhưng từ đây trở đi là tùy vào mọi người quỷ tộc đấy.<br> ',
    'Shiraes nói đúng ạ! Mọi người‚ vẫn chưa kết thúc đâu!<br>Điều quan trọng là từ giờ chúng ta sẽ tiếp đãi họ thế nào!<br> ',
    'Nhất định phải thành công và trở nên thân thiết với mọi người loài người nhé!!<br> ',
    'Vậy thì mọi người‚ đã sẵn sàng chưa? Mộộộột hai――!<br> ',
    'Chào mừng đến Đảo Quỷ~~~!!<br> ',
    '……Chính là nơi này sao? Nơi bảo vật của ta trôi dạt đến.<br>Quỷ tộc cái gì chứ. Muốn cướp bảo vật từ tay trộm cướp thì đừng hòng……!<br> ',
    'Viên pha lê…… là của ta!!<br> ',
]


def sha256(b): return hashlib.sha256(b).hexdigest()
def enc_props(b):
    return {'bom': b.startswith(b'\xef\xbb\xbf'), 'newline': 'CRLF' if b'\r\n' in b else 'LF', 'endswith_newline': b.endswith((b'\n', b'\r\n')), 'byte_length': len(b), 'sha256': sha256(b)}
def text_field_index(cmd): return 1 if cmd == 'title' else 2

def split_line(line): return line.split(',',5)
def is_candidate(line): return any(line.startswith(c+',') for c in CMDS)
def tagset(s): return re.findall(r'<[^>]+>', s)
def placeholders(s): return re.findall(r'%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z0-9_]+\}|\$\{[^}]+\}|\\[nrt]|%%', s)
def en_like(s): return bool(re.search(r'[A-Za-z]{3,}', re.sub(r'<[^>]+>|%[A-Za-z0-9_]+%', '', s)))

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    raw = EN_ASSET.read_bytes()
    props = enc_props(raw)
    text = raw.decode('utf-8-sig')
    newline = '\r\n' if props['newline']=='CRLF' else '\n'
    lines = text.splitlines()
    candidates = [(i,l) for i,l in enumerate(lines) if is_candidate(l)]
    assert len(VI) == len(candidates), (len(VI), len(candidates))
    out_lines = lines[:]
    entries=[]; blockers=[]; warnings=[]; kept=[]
    for n, ((idx,line), vi) in enumerate(zip(candidates, VI), 1):
        cmd=line.split(',',1)[0]
        parts=split_line(line)
        fi=text_field_index(cmd)
        old_text=parts[fi]
        if ',' in vi:
            blockers.append({'line':idx+1,'type':'ASCII_COMMA_IN_VI','text':vi})
        parts[fi]=vi
        out_lines[idx]=','.join(parts)
        entries.append({'ordinal':n,'line':idx+1,'command':cmd,'speaker':parts[1] if len(parts)>1 else '', 'source_text':old_text, 'vi_text':vi, 'match_status':'EXACT', 'translation_status':'TRANSLATED'})
    out_text = newline.join(out_lines) + (newline if props['endswith_newline'] else '')
    out_bytes = (b'\xef\xbb\xbf' if props['bom'] else b'') + out_text.encode('utf-8')
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_bytes)

    out_raw = VI_ASSET.read_bytes(); out_props = enc_props(out_raw)
    out_lines2 = out_raw.decode('utf-8-sig').splitlines()
    if len(lines)!=len(out_lines2): blockers.append({'type':'LINE_COUNT_MISMATCH','en':len(lines),'vi':len(out_lines2)})
    if props['bom'] != out_props['bom']: blockers.append({'type':'BOM_MISMATCH','en':props['bom'],'vi':out_props['bom']})
    if props['newline'] != out_props['newline']: blockers.append({'type':'NEWLINE_MISMATCH','en':props['newline'],'vi':out_props['newline']})

    for i,(a,b) in enumerate(zip(lines,out_lines2),1):
        if a.count(',') != b.count(','):
            blockers.append({'line':i,'type':'DELIMITER_COUNT_MISMATCH','en':a.count(','),'vi':b.count(',')})
        ac=a.split(',',5); bc=b.split(',',5)
        if ac and ac[0] in CMDS:
            fi=text_field_index(ac[0])
            sig_a=ac[:fi]+ac[fi+1:]
            sig_b=bc[:fi]+bc[fi+1:]
            if sig_a!=sig_b:
                blockers.append({'line':i,'type':'TECH_FIELD_CHANGED','en_sig':sig_a,'vi_sig':sig_b})
            if tagset(ac[fi]) != tagset(bc[fi]):
                blockers.append({'line':i,'type':'TAG_MISMATCH','en':tagset(ac[fi]),'vi':tagset(bc[fi])})
            if placeholders(ac[fi]) != placeholders(bc[fi]):
                blockers.append({'line':i,'type':'PLACEHOLDER_MISMATCH','en':placeholders(ac[fi]),'vi':placeholders(bc[fi])})
            if ',' in bc[fi]:
                blockers.append({'line':i,'type':'ASCII_COMMA_IN_TEXT_FIELD','text':bc[fi]})
            if ac[fi] == bc[fi]:
                kept.append({'line':i,'text':bc[fi]})
            # Kept-English QA is based on unchanged text records above. Proper names
            # and accepted onomatopoeia/nicknames may contain Latin letters but are
            # not kept EN sentences, so do not flag Vietnamese lines solely for ASCII.

    focused=[]
    for (idx, old), new in zip(candidates, [out_lines2[i] for i,_ in candidates]):
        if old != new:
            focused.extend(difflib.unified_diff([old+'\n'], [new+'\n'], fromfile=f'EN line {idx+1}', tofile=f'VI line {idx+1}', lineterm='\n'))
    (WORK/'focused_diff.md').write_text(''.join(focused), encoding='utf-8')

    qa={
      'file': str(VI_ASSET), 'qa_status': 'PASS' if not blockers and not kept else 'FAIL',
      'blockers': blockers, 'kept_english_or_unchanged_text_records': kept,
      'warnings': warnings, 'checks': {
        'source_line_count': len(lines), 'output_line_count': len(out_lines2),
        'candidate_text_records': len(candidates), 'translated_records': len(entries),
        'commands_count': {c: sum(1 for _,l in candidates if l.startswith(c+',')) for c in CMDS},
        'delimiter_mismatches': sum(1 for i,(a,b) in enumerate(zip(lines,out_lines2),1) if a.count(',')!=b.count(',')),
        'technical_field_changes': sum(1 for b in blockers if b.get('type')=='TECH_FIELD_CHANGED'),
        'tag_mismatches': sum(1 for b in blockers if b.get('type')=='TAG_MISMATCH'),
        'placeholder_mismatches': sum(1 for b in blockers if b.get('type')=='PLACEHOLDER_MISMATCH'),
      },
      'notes': ['JP primary via ja.json; EN asset/en.json used for ordered alignment.', 'Commander/司令官 translated as Chỉ Huy. 旦那様 in Kureha speech rendered phu quân per scene tone.', 'No intentionally unchanged translatable records.']
    }
    if not blockers and not kept: qa['qa_status']='PASS'
    (WORK/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    manifest={
      'scene':SCENE, 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'sources': {'ja_json':str(JA_JSON), 'en_json':str(EN_JSON), 'en_asset':str(EN_ASSET)},
      'output': str(VI_ASSET), 'work_dir': str(WORK),
      'source_props': props, 'output_props': out_props,
      'counts': qa['checks'], 'entries': entries,
      'qa_status': qa['qa_status'], 'output_sha256': out_props['sha256']
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'qa_status':qa['qa_status'],'blockers':len(blockers),'kept':len(kept),'warnings':len(warnings),'output':str(VI_ASSET),'manifest':str(WORK/'manifest.json'),'qa_log':str(WORK/'qa_log.json'),'diff':str(WORK/'focused_diff.md'),'counts':qa['checks'],'sha256':out_props['sha256']},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
