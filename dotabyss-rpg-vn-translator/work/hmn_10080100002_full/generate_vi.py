# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib
SCENE='hmn_10080100002'
ROOT=Path('E:/AgentTranslation')
EN=ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI=ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK=ROOT/'dotabyss-rpg-vn-translator/work/hmn_10080100002_full'
JA=ROOT/'dotabyss-translation-main/translations/novels/hmn_10080100002/ja.json'
ENJSON=ROOT/'dotabyss-translation-main/translations/novels/hmn_10080100002/en.json'
TEXT_CMDS={'title':1,'message':2,'messageTextUnder':2,'messageTextCenter':2}
translations = [
"Chị Em Trong Đại Huyệt",
"<size=48>――Trong Đại Huyệt: Nhiệm Vụ Hộ Tống Đội Vận Chuyển Đến Căn Cứ Tạm</size>",
"Vậy đây là bên trong Đại Huyệt… Không gian này kỳ lạ hơn em<br>từng nghe nhiều.<br> ",
"Veera lần đầu vào Đại Huyệt nhỉ. Lần này suy cho cùng chỉ là<br>nhiệm vụ hộ tống. Đừng căng thẳng quá‚ cứ bình tĩnh làm việc.<br> ",
"Vâng. Em sẽ cho anh thấy em gái của chị là một pháp sư đến mức nào.<br> ",
"Em sẽ làm việc sao cho không khiến chị mất mặt. Xin hãy kỳ vọng<br>ở em‚ Chỉ Huy.<br> ",
"Như thế gọi là căng thẳng quá đấy… Thôi‚ đừng cố sức quá.<br> ",
"Cứ giao cho em.<br> ",
"Verisa nhìn Veera đang hừng hực khí thế rồi lặng lẽ<br>tiến lại gần %user%.<br> ",
"Hư hư hư‚ xem ra Veera đang rất hăng hái nhỉ.<br> ",
"Nhưng tiếc quá nha! Hôm nay người tỏa sáng hơn Veera sẽ là em!<br> ",
"Em đang nghĩ chuyện đó đấy à?<br> ",
"Ơ kìa? Có gì sai sao? Muốn cho em gái thấy đẳng cấp khác biệt<br>là ham muốn rất tự nhiên của một người chị mà‚ đúng không?<br> ",
"Hay là anh không thích chuyện người ngoài anh bị dạy cho biết thân biết phận?<br>Chẳng lẽ anh đang ghen đó hả～♡<br> ",
"…Nhân tiện‚ Veera thì có vẻ không muốn làm Verisa mất mặt đâu. Xem ra<br>về mặt nhân cách thì em đã thua rồi nhỉ?<br> ",
"Ưư… con bé cứ như vậy đó‚ thật là! Người sẽ mất mặt vì thua tan nát<br>trước ma pháp của em gái là em cơ mà…!<br> ",
"…Trông hai chị em đâu có ghét nhau. Chỉ là em không thích<br>thua kém về ma pháp thôi à?<br> ",
"Làm gì có chuyện đó! Em đời nào nói rằng mình ghét em gái<br>vì con bé giỏi chứ!<br> ",
"Chỉ là… ở Perdion‚ con bé được kỳ vọng hơn em‚<br>cũng thật sự có tài và có thành quả nên…<br> ",
"Em chỉ muốn cho con bé thấy uy nghiêm của một người chị ở đây thôi.<br> ",
"Dù không có uy nghiêm gì thì<br>con bé vẫn rất tôn trọng Verisa mà.<br> ",
"Chính thế cũng không được! Em muốn cho con bé thấy rõ<br>mình xứng đáng được tôn trọng chứ!<br> ",
"Đúng là nếu em thể hiện tốt trong Đại Huyệt<br>thì mọi người sẽ nói quả nhiên là Verisa nhỉ.<br> ",
"Nhưng Veera là một pháp sư lão luyện đúng không?<br>Nói thật thì em thắng nổi không?<br> ",
"Hư hưーn! Nếu là chiến đấu trong Đại Huyệt thì em dày dạn kinh nghiệm!<br>Dù đối thủ là Veera thì em cũng không định thua đâu!<br> ",
"Tiếc vì không được thấy em thua hả～?<br>Nè nè‚ cay không? Anh ơi?<br> ",
"…Ừ thì‚ người anh quen lâu hơn là Verisa.<br>Anh sẽ cổ vũ em một chút vậy.<br> ",
"Hiếm khi anh chịu thật lòng đấy. Tinh thần tốt lắm!<br>Nhìn cho kỹ dáng vẻ người chị vô địch của em đây!<br> ",
"Verisa phấn chấn bước đến chỗ Veera<br>và tự tin cất tiếng gọi.<br> ",
"Veera.<br>Lần đầu vào Đại Huyệt thế nào? Có căng thẳng không đó?<br> ",
"A‚ chị ơi.<br>Ừm‚ đúng là nơi nguy hiểm thật.<br> ",
"Đúng vậy‚ trong Đại Huyệt này chỉ một chút lơ là cũng có thể mất mạng.<br>Ví dụ như‚ nguy hiểm là… ừm‚ thì…<br> ",
"Cấu trúc bên trong Đại Huyệt đôi khi sẽ thay đổi.<br>Chỉ cần mất cảnh giác một chút là có thể lạc đường hoặc bị phục kích nhỉ?<br> ",
"Ơ… Veera‚ em biết thông tin về Đại Huyệt sao?<br> ",
"Vì đó là những gì chị và mọi người đã điều tra mà.<br>Trước khi đến em đã học kỹ rồi.<br> ",
"Ư… đúng là em gái của chị…!<br>Nhưng nguy hiểm của Đại Huyệt đâu chỉ có thế!<br> ",
"Đặc biệt phải cẩn thận với quái vật…<br> ",
"Ừm‚ quái vật trong Đại Huyệt dù bề ngoài giống nhau<br>vẫn có thể khác thuộc tính hoặc có năng lực đặc biệt nên không được chủ quan nhỉ.<br> ",
"Ư‚ ưưưư!<br> ",
"Sao ngay cả những lúc thế này<br>em cũng không để chị ra dáng chị gái chứ…!<br> ",
"…?<br>Sao vậy chị?<br> ",
"Không có gì… Chị vẫn chưa thua đâu…!<br> ",
"…Đúng là có vẻ không ổn rồi.<br>Cố lên Verisa. Hãy cho con bé thấy uy nghiêm của người chị đi…<br> ",
"Sắp đến thang nâng rồi nhỉ.<br>Như vậy là nhiệm vụ kết thúc rồi sao?<br> ",
"Đúng vậy. Dù là nhiệm vụ ít nguy hiểm<br>nhưng chúng ta thật sự đã trở về bình an.<br> ",
"Em chẳng có đất diễn…<br>Em đã muốn cho chị thấy điểm tốt của mình mà…<br> ",
"Không có nguy hiểm vẫn tốt hơn chứ.<br>Hai chị em các em hơi giống nhau đấy…<br> ",
"Gàoồồồồồ!<br> ",
"Hả!? Chuyện gì vậy!?<br> ",
"Đội vận chuyển đang chuẩn bị quay về thang nâng<br>bất ngờ bị một bầy golem trồi lên từ mặt đất bao vây.<br> ",
"Sao golem lại xuất hiện ở nơi này!?<br> ",
"Là bẫy hay ngẫu nhiên cũng vậy. Dù sao chúng ta chỉ còn cách chiến đấu.<br>Toàn đội‚ chuẩn bị chiến đấu!<br> ",
"N‚ nhưng chúng tôi chỉ là đội vận chuyển thôi mà…!<br> ",
"Bọn tôi không thể đánh nhau với golem đâu!<br> ",
"Mọi người bình tĩnh! Không saaao đâu!<br>Có bọn tôi thì chúng không phải đối thủ đâu!<br> ",
"Chị ơi!<br> ",
"Cứ để chị lo‚ Veera lùi lại đi. Với người mới thì có vẻ hơi khó<br>nên chỗ này là việc của cựu binh‚ hiểu chứ?<br> ",
"Nhưng…! Em cũng chiến đấu được mà!<br> ",
"Yên tâm‚ chị không nghi ngờ ma lực của Veera đâu. Vậy nên nếu chị gặp nguy<br>thì em phải cứu chị cho đàng hoàng đó nhé?<br> ",
"Ừm…<br>Cố lên nhé chị!<br> ",
"Phù… mọi người nghe cho kỹ. Chúng là golem cấp thấp nhất‚<br>chỉ cần tấn công lõi là hạ được dễ dàng!<br> ",
"Nói thì nói vậy‚ nhưng làm sao đánh trúng lõi đây!?<br>Đến gần còn không được nữa là!?<br> ",
"Chuyện đó cứ để ma pháp của tôi lo♪<br>Nào‚ bắt đầu thôi～～～!<br> ",
"Verisa giơ trượng lên và triển khai ma pháp trận.<br>Cô nhắm vào golem rồi tạo ra một quả cầu lửa.<br> ",
"Nhắm bắn lõi…!<br>Thiêu rụi đi!<br> ",
"Gừừừừ…!<br> ",
"Quả cầu lửa được bắn ra trúng thẳng golem.<br>Lõi bị sức nóng dữ dội và vụ nổ mạnh phá hủy‚ golem đổ sụp ngay tại chỗ.<br> ",
"Ồồ…! Hay lắm‚ cô bé Verisa!<br> ",
"Phải cho em gái thấy điểm tốt của chị chứ!<br>Nào‚ tiếp tục tới luôn nào!<br> ",
"Verisa triển khai nhiều ma pháp trận và liên tiếp phóng cầu lửa.<br>Thế nhưng――<br> ",
"Con tiếp theo… tiếp theo!<br> ",
"V‚ Verisa!?<br>Golem đang càng lúc càng tới gần đấy!<br> ",
"Gàoồồồ!<br> ",
"Biết rồi～～～!!!<br>Nhưng không bắn trúng lõi thì không thể hạ chúng được!<br> ",
"C‚ cứ thế này thì chúng ta chết mất…!<br>Phải làm sao đây!?<br> ",
"…Cảm ơn chị.<br>Em hiểu đại khái rồi.<br> ",
"Veera…!?<br> ",
"Veera tạo ra một sàn băng dưới chân rồi lướt đến trước mặt Verisa.<br>Ma lực khổng lồ hội tụ vào cây trượng cô giơ trong tay.<br> ",
"Ta sẽ không để các ngươi cản trở nhiệm vụ của ta và chị nữa.<br>Đóng băng vĩnh viễn đi‚ lũ cản đường…!<br> ",
"――Keng‚ một âm thanh cao vút vang lên. Ngay khoảnh khắc ánh sáng bắn ra từ trượng<br>toàn bộ golem xung quanh đã bị băng bao phủ.<br> ",
"…Vậy là xong.<br> ",
"Khi Veera búng tay‚ những lõi bị bọc trong băng vỡ tan răng rắc.<br>Không còn sót lại một con nào‚ tất cả golem sụp đổ rồi biến mất.<br> ",
"Nếu lõi nằm ở đâu đó<br>thì chỉ cần đóng băng tất cả là có thể phá hủy cả lõi cùng lúc.<br> ",
"So với chị<br>đây là một ma pháp khá vụng về nhỉ.<br> ",
"…Xuất sắc lắm.<br>Em làm tốt lắm‚ Veera.<br> ",
"Không đâu‚ em chỉ xử lý để không gây phiền cho chị thôi.<br>Đúng không chị?<br> ",
"…Em giỏi quá‚ Veera. Em thật sự đã cứu chị rồi.<br>Quả nhiên‚ người như chị…<br> ",
"Chị… ơi…?<br> ",
"Bằng ma pháp Veera tung ra‚ bọn golem đã bị tiêu diệt sạch.<br>Trước chiến quả tuyệt vời ấy‚ Verisa không thể che giấu vẻ mặt cay đắng.<br> ",
"Đội vận chuyển do Verisa và Veera hộ tống<br>đã nhờ ma pháp của Veera đẩy lùi cuộc phục kích của golem và an toàn trở về căn cứ tiền tuyến.<br> ",
"Chà‚ cô bé này dùng ma pháp ghê gớm thật đấy!<br>Làm tôi giật cả mình!<br> ",
"Ừ‚ nhờ cô ấy mà chúng ta được cứu!<br> ",
"Người chỉ ra điểm yếu là chị mà.<br>Em chỉ phá hủy chúng bằng ma pháp thôi‚ chuyện đó ai cũng…<br> ",
"Không‚ chị không làm được.<br>Đó là sức mạnh của em đấy‚ Veera.<br> ",
"Chị ơi‚ sao chị lại nói vậy…?<br> ",
"Đúng như cô bé Verisa nói!<br>Cô là một pháp sư kinh khủng đấy!<br> ",
"Này Veera‚ để tôi đãi cô một ly nhé!<br>Coi như cảm ơn vì đã cứu bọn tôi!<br> ",
"Ơ…!?<br> ",
"Chỉ Huy‚ em nên làm sao đây…?<br> ",
"Cũng được mà nhỉ?<br>Một ly chúc mừng hoàn thành nhiệm vụ đầu tiên cũng hay đấy.<br> ",
"Được rồi‚ tôi sẽ trả tiền.<br>Mọi người‚ giờ đến quán rượu nào!<br> ",
"Quả đúng là Chỉ Huy! Hiểu chuyện ghê!<br> ",
"Đi thôi‚ Veera!<br> ",
"Em hiểu rồi.<br>Chị ơi‚ đi cùng em nhé?<br> ",
"Ừm… chị thôi.<br>Chị no rồi và cũng không có tâm trạng đó.<br> ",
"Chị không đi sao?<br>Vậy em cũng không đi nữa.<br> ",
"Không‚ Veera cứ đi đi nhé?<br>Giao lưu với đồng đội ở căn cứ này cũng là chuyện quan trọng mà.<br> ",
"N‚ nhưng…<br> ",
"Cứ đi đi. Nhé?<br> ",
"…Ừm.<br>Nhưng lúc nào chị cũng có thể đến nhé?<br> ",
"Verisa… em ổn chứ?<br> ",
"Gì vậy anh?<br>Anh đến cười em là người chị vô dụng thua em gái à?<br> ",
"Ai lại làm chuyện đó.<br>Em đã chiến đấu rất ra dáng mà.<br> ",
"…Cảm ơn anh.<br>Nhưng hôm nay có lẽ em hơi mệt rồi.<br> ",
"Đừng bận tâm đến em.<br>Anh hãy đi chúc mừng chiến quả của Veera đi.<br> ",
"Anh hiểu rồi.<br>Nhưng lát nữa nhất định phải ghé mặt đấy.<br> ",
"Veera chắc chắn muốn được em<br>chúc mừng hơn bất kỳ ai.<br> ",
"…Ừm. Em biết.<br> ",
]

def field_index(cmd): return TEXT_CMDS[cmd]
def tags(s): return re.findall(r'<[^>]+>', s)
def placeholders(s): return re.findall(r'%[A-Za-z0-9_]+%|%user%|\\[nrt]|\{[^}]+\}|\$\{[^}]+\}', s)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def newline_info(b):
    return 'CRLF' if b'\r\n' in b else 'LF'

def text_records(lines):
    out=[]
    for i,line in enumerate(lines,1):
        raw=line.rstrip('\r\n')
        cmd=raw.split(',',1)[0] if raw else ''
        if cmd in TEXT_CMDS:
            parts=raw.split(',')
            out.append((i,cmd,parts,field_index(cmd)))
    return out

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    src_b=EN.read_bytes(); bom=src_b.startswith(b'\xef\xbb\xbf'); nl=newline_info(src_b)
    text=src_b.decode('utf-8-sig')
    lines=text.splitlines(True)
    recs=text_records(lines)
    if len(recs)!=len(translations): raise SystemExit(f'translation count {len(translations)} != records {len(recs)}')
    out_lines=list(lines)
    entries=[]; blockers=[]
    for n,(rec,vi) in enumerate(zip(recs, translations),1):
        line_no,cmd,parts,ti=rec
        src_text=parts[ti]
        vi = vi.replace('\n', '')
        # Asset EN text-field tag counts are authoritative. If a draft used an
        # extra UI break from JP/for readability, merge it back into prose.
        while vi.count('<br>') > src_text.count('<br>'):
            vi = vi.replace('<br>', ' ', 1)
        if vi.count('<br>') < src_text.count('<br>'):
            vi = vi.rstrip() + '<br> ' * (src_text.count('<br>') - vi.count('<br>'))
        if ',' in vi: blockers.append({'line':line_no,'type':'ASCII_COMMA_IN_TRANSLATION','text':vi})
        if len(tags(src_text))!=len(tags(vi)) or tags(src_text)!=tags(vi): blockers.append({'line':line_no,'type':'TAG_MISMATCH','source':tags(src_text),'vi':tags(vi)})
        if placeholders(src_text)!=placeholders(vi): blockers.append({'line':line_no,'type':'PLACEHOLDER_MISMATCH','source':placeholders(src_text),'vi':placeholders(vi)})
        newparts=list(parts); newparts[ti]=vi
        newline='\r\n' if out_lines[line_no-1].endswith('\r\n') else '\n' if out_lines[line_no-1].endswith('\n') else ''
        out_lines[line_no-1]=','.join(newparts)+newline
        entries.append({'index':n,'line':line_no,'cmd':cmd,'source_text':src_text,'vi_text':vi,'status':'TRANSLATED','match':'CONTEXT_MATCH' if n>2 else 'EXACT'})
    out_text=''.join(out_lines)
    out_b=(b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
    VI.parent.mkdir(parents=True, exist_ok=True); VI.write_bytes(out_b)
    # focused diff only changed text records
    before=[]; after=[]
    for line_no,cmd,parts,ti in recs:
        before.append(f'{line_no}: '+lines[line_no-1].rstrip('\r\n'))
        after.append(f'{line_no}: '+out_lines[line_no-1].rstrip('\r\n'))
    diff='\n'.join(difflib.unified_diff(before, after, fromfile='EN text records', tofile='VI text records', lineterm='\n'))
    (WORK/'focused_diff.md').write_text('# Focused Diff\n\n```diff\n'+diff+'\n```\n', encoding='utf-8')
    # QA independent local
    vi_b=VI.read_bytes(); vi_lines=vi_b.decode('utf-8-sig').splitlines(True); vi_recs=text_records(vi_lines)
    delims=[]; tech=[]; tagm=[]; phm=[]; ascii_commas=[]; unchanged=[]
    for (line_no,cmd,src_parts,ti),(vline_no,vcmd,vparts,vti) in zip(recs, vi_recs):
        if lines[line_no-1].count(',') != vi_lines[vline_no-1].count(','): delims.append(line_no)
        if src_parts[:ti]+src_parts[ti+1:] != vparts[:vti]+vparts[vti+1:]: tech.append(line_no)
        if tags(src_parts[ti]) != tags(vparts[vti]): tagm.append(line_no)
        if placeholders(src_parts[ti]) != placeholders(vparts[vti]): phm.append(line_no)
        if ',' in vparts[vti]: ascii_commas.append(line_no)
        if src_parts[ti] == vparts[vti]: unchanged.append(line_no)
    targeted=[]
    pats=['Lord Commander','Commander','Mister','Big Sis','big sister','little sister','Abyss','Fufufu','Yeah','Okay','Verisa... You alright','Sis!','What is it']
    for line_no,cmd,parts,ti in vi_recs:
        for pat in pats:
            if pat in parts[ti]: targeted.append({'line':line_no,'term':pat})
    status='PASS' if not (blockers or delims or tech or tagm or phm or ascii_commas or unchanged or targeted) and len(lines)==len(vi_lines) else 'FAIL'
    qa={'scene':SCENE,'qa_status':status,'blockers':blockers,'items':[], 'notes':['JP primary; EN asset used for alignment. Character names in technical fields preserved. Verisa/Veera romanization used in Vietnamese text. No H18 content in this file.'],
        'independent_verify':{'status':status,'line_count':{'en':len(lines),'vi':len(vi_lines),'match':len(lines)==len(vi_lines)},'bom_match':bom==vi_b.startswith(b'\xef\xbb\xbf'),'newline_match':nl==newline_info(vi_b),'candidate_counts':{k:sum(1 for _,c,_,_ in recs if c==k) for k in TEXT_CMDS},'changed_text_records':sum(1 for a,b in zip(recs,vi_recs) if a[2][a[3]]!=b[2][b[3]]),'delimiter_mismatch_count':len(delims),'technical_field_mismatch_count':len(tech),'tag_mismatch_count':len(tagm),'placeholder_mismatch_count':len(phm),'ascii_comma_in_vi_text_count':len(ascii_commas),'unchanged_unlogged_text_records':len(unchanged),'targeted_english_leftover_count':len(targeted),'targeted_english_leftovers':targeted}}
    manifest={'scene':SCENE,'source':str(EN),'output':str(VI),'work_dir':str(WORK),'source_sha256':hashlib.sha256(src_b).hexdigest(),'output_sha256':sha(VI),'bom':bom,'newline':nl,'source_line_count':len(lines),'output_line_count':len(vi_lines),'text_record_count':len(recs),'candidate_counts':qa['independent_verify']['candidate_counts'],'entries':entries,'qa_status':status,'independent_verify':qa['independent_verify']}
    (WORK/'qa_log.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    (WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':status,'output':str(VI),'work':str(WORK),'records':len(recs),'blockers':len(blockers),'sha256':sha(VI)},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
