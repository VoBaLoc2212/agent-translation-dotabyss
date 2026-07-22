from pathlib import Path
import json, re, hashlib, difflib
from datetime import datetime, timezone

root = Path('E:/AgentTranslation')
en_asset = root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle/evs_10200010201.txt'
vi_asset = root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/evs_10200010201.txt'
ja_json = root/'dotabyss-translation-main/translations/novels/evs_10200010201/ja.json'
en_json = root/'dotabyss-translation-main/translations/novels/evs_10200010201/en.json'
work = root/'dotabyss-rpg-vn-translator/work/evs_10200010201_full'
work.mkdir(parents=True, exist_ok=True)

T = {
23: 'Tiêu Đề',
61: 'Ký túc xá――nơi lưu trú được cấp cho những người dấn thân khám phá Đại Huyệt. Trong<br>không gian nghỉ ngơi ở căn cứ tiền tuyến ấy‚ ba cô gái đang ngồi đối diện nhau.<br> ',
118: 'Vậy nên em muốn tổ chức một bữa tiệc bất ngờ<br>để chúc mừng Chỉ Huy nhậm chức!!<br> ',
187: 'Nghe thật tuyệt vời.<br>Phải không chị?<br> ',
198: 'Ừ nhỉ~♪<br>Cũng hơi muộn rồi đấy‚ nhưng thôi‚ cũng được mà~?<br> ',
200: 'Những người gật đầu trước lời Wendy là cặp chị em pháp sư của<br>Perdion――pháp sư băng Veera và chị cô ấy‚ pháp sư lửa Verisa.<br> ',
202: 'Từ sau khi làm người dẫn đường cho hai chị em đi tìm<br>quặng hiếm‚ họ đã trở thành số ít bạn bè mà Wendy có thể thật sự mở lòng.<br> ',
257: 'Hửm? Nghĩ lại thì bữa tiệc mừng em với chị gặp lại nhau<br>cũng chưa làm nhỉ? Hay là mình tổ chức cả bên đó nữa...<br> ',
316: 'Không cần đâu~~!<br>Đâu phải mình xa nhau lâu đến thế đâu~?<br> ',
318: 'Veera điều khiển ma pháp băng mạnh hơn chị mình nhiều bậc<br>nhưng cô vẫn yêu quý Verisa từ tận đáy lòng.<br> ',
320: 'Khi mới đến căn cứ tiền tuyến‚ Veera nhút nhát và điềm tĩnh quá mức<br>nhưng gần đây biểu cảm đã phong phú hơn. Trước cô em gái ấy‚ Verisa luôn cố tỏ ra ra dáng chị gái.<br> ',
322: 'Wendy rất thích những màn qua lại vụng về mà thân thiết<br>của cặp chị em này.<br> ',
333: 'Ừm‚ bữa tiệc tái ngộ với chị để sau hãy tính...<br>Em nghĩ ý tưởng làm tiệc mừng ngài Chỉ Huy thành bất ngờ rất tuyệt.<br> ',
344: 'Nếu chỉ mời ngài Chỉ Huy đến một bữa tiệc bình thường<br>chắc anh ấy sẽ viện lý do để từ chối mất... Hì hì.<br> ',
355: 'Không biết anh Chỉ Huy lúc nào cũng làm mặt tỉnh bơ kia sẽ vui vẻ thế nào đây...<br>Hì hì‚ đáng xem lắm đó~♪ Ý hay đấy Wendy.<br> ',
404: 'Không không. Thật ra chuyện bất ngờ này là ý tưởng của các anh lính.<br>Quả nhiên mọi người đều kính mến Chỉ Huy nhỉ...<br> ',
415: 'Em cũng không thể chịu thua được! Trước mắt‚ để gửi gắm lòng kính trọng và biết ơn<br>em định tổ chức tiệc suốt ba ngày ba đêm――không‚ suốt một tuần liền!<br> ',
460: 'Chức năng căn cứ sẽ tê liệt mất!!<br> ',
517: 'B-bình tĩnh nào Wendy-san.<br>Bọn em hiểu chị kính trọng ngài Chỉ Huy đến mức nào rồi mà‚ nhé?<br> ',
566: 'Vâng‚ em vô cùng kính trọng anh ấy! Những ngày hạnh phúc hiện giờ đều nhờ có<br>Chỉ Huy‚ nên nhân dịp này em phải báo đáp...!<br> ',
635: 'Hừm... chị hiểu tâm ý của Wendy rồi đó...<br>nhưng sao em lại kể chuyện bữa tiệc cho bọn chị~?<br> ',
646: 'À... nếu hai chị không phiền...<br>em muốn nhờ hai chị giúp... có được... không ạ...?<br> ',
657: 'Ngài Chỉ Huy cũng luôn quan tâm đến bọn em mà.<br>Tất nhiên là bọn em sẽ giúp. Phải không chị?<br> ',
668: 'Nói đúng hơn thì chị mới là người chăm sóc anh ấy ấy chứ~♪<br>Thôi được. Chị sẽ giúp em――<br> ',
723: '――chị muốn nói vậy lắm nhưng mà~ hì hì. Đã định làm anh ấy bất ngờ<br>thì chơi khăm chẳng phải thú vị hơn tiệc tùng sao~?<br> ',
780: 'Chơi khăm...!? Là gì vậy ạ!?<br>Nếu có thể làm Chỉ Huy vui thì em làm gì cũng được! Xin hãy chỉ em!<br> ',
791: 'Tinh thần tốt đấy♪<br>Vậy trước hết hãy đi mượn Adelheid cái gọi là máy ảnh đi♪<br> ',
803: 'Máy ảnh... hình như là cỗ máy ghi lại cảnh trước mắt đúng không ạ?<br>Vậy em nên chụp cảnh như thế nào đây ạ!?<br> ',
854: 'Hì hì hì... đó là~~ dáng vẻ thảm hại~~ của anh Chỉ Huy!<br>Nếu dùng nó để uy hiếp rồi biến anh ấy thành đầy tớ thì chắc chắn anh ấy sẽ sốc lắm♪<br> ',
897: 'K-khác hẳn điều em tưởng tượng luôn~~!<br>Em muốn Chỉ Huy phải “vui vẻ” cơ mà~~!<br> ',
958: 'Đúng đó chị...<br>Hơn nữa em chỉ thấy trước tương lai thất bại thôi‚ phải nói sao nhỉ...<br> ',
969: 'Ể~? Nhưng chị Verisa đây thích trò nghịch ngợm hơn mà~~.<br> ',
1018: 'Xin chị đó Verisa-san!!<br>Em nhất định phải truyền đạt lòng biết ơn của mình đến Chỉ Huy~!!!<br> ',
1075: 'Ư ưư!! Á-ánh mắt thuần khiết gì thế này...!?<br>Nó làm chị muốn gật đầu mất nên đừng nhìn chị nữa~!<br> ',
1124: 'Em xin hai chị~! Nếu được làm cùng hai chị<br>em tin chắc chúng ta sẽ tạo nên một bữa tiệc thật tuyệt~!!!<br> ',
1167: 'Ư-ưư... nhưng mà nhưng mà...<br>Chỉ làm người ta vui thôi thì... hình như hơi xấu hổ ấy...<br> ',
1224: 'Chị thật là. Chị cứ nói đồng ý là được mà.<br>Thật ra chị cũng muốn cùng mừng cho ngài Chỉ Huy đúng không?<br> ',
1233: 'L-làm gì có chuyện đó chứ!?<br>Chị chỉ hơi~~ biết ơn anh Chỉ Huy một tí xíu thôi!<br> ',
1282: 'À ha! Vậy tức là!<br>Theo cách của Verisa-san thì chị vẫn biết ơn anh ấy đúng không ạ!<br> ',
1339: 'Ư...!? K-không ngờ lại sắc bén thế...!<br> ',
1350: 'Em xin hai chị‚ xin hãy giúp em. Người bạn mà em có thể nhờ chuyện thế này<br>chỉ có Verisa-san và Veera-san thôi...<br> ',
1401: '...Chị ơi‚ bạn ấy đã nói đến mức này rồi<br>mà chị vẫn định từ chối sao?<br> ',
1456: 'Thôi nào... hết cách rồi nhỉ~.<br>Nếu Wendy đã nói đến vậy thì chị sẽ giúp.<br> ',
1467: 'Thật ạ!?<br>Chị sẽ cùng em tổ chức tiệc bất ngờ đúng không ạ!<br> ',
1478: 'Ừ thì chị cũng muốn thấy mặt anh ấy ngạc nhiên mà~?<br>Với lại lộ tuyến khiến anh Chỉ Huy mang ơn rồi biến thành đầy tớ cũng được đó chứ~?<br> ',
1529: 'Chị đúng là không thành thật chút nào.<br>Nhưng chính điểm đó lại tuyệt vời... hì hì... hì hì hì hì...<br> ',
1588: 'Này~~ quay về đi nào~~.<br>Veera cũng phải giúp đấy nhé~?<br> ',
1616: 'Khụ――em xin lỗi.<br>Tất nhiên rồi‚ ba chúng ta cùng cố gắng nhé.<br> ',
1665: 'Hoan hô! Cảm ơn hai chị nhiều lắm~!<br> ',
1735: 'Đã quyết vậy rồi thì trước hết ta đi mua sắm ở chợ nhé?<br>Nếu tổ chức tiệc bất ngờ thì đạo cụ là thứ không thể thiếu mà.<br> ',
1746: 'Một khi đã quyết làm thì chị không qua loa đâu~.<br>Vậy mỗi người mua thứ gì trông thú vị rồi tập hợp lại nhé!<br> ',
1799: 'Vâng! Bắt đầu chuẩn bị tiệc thôi!!<br> ',
1833: 'Khu phố mua sắm trong căn cứ tiền tuyến. Giữa những nhà thám hiểm tìm dụng cụ<br>cho nhiệm vụ và các thương nhân tất bật chào mời khách‚ ba cô gái xuất hiện ở đó.<br> ',
1896: 'Hai em mua sắm xong chưa~? Vậy để chị mở màn trước nhé...<br>Hừ hừ hừ... hãy chiêm ngưỡng thứ này――!<br> ',
1953: 'Ta-daa! Chị mua pháo giấy về rồi đây!<br>Nhắc đến tiệc thì phải có cái này chứ nhỉ~♪<br> ',
1996: 'Oa oa oa! N-nhiều quá...!<br>Có cả loại bắn liên tục và loại to như đại bác nữa kìa!<br> ',
2053: 'To thế này thì chắc chắn anh Chỉ Huy sẽ giật bắn mình~!<br>Khục khục... chị nóng lòng xem anh ấy sẽ lộ gương mặt thảm hại nào quá~♪<br> ',
2073: 'Hãy làm anh ấy cười chứ ạ~! À‚ nhưng không khí náo nhiệt thế này cũng vui thật...<br>Veera-san thấy sao?<br> ',
2124: 'Nếu là thứ chị tặng thì em vui với bất cứ thứ gì.<br>Em muốn trân trọng pháo giấy này‚ mang theo mỗi ngày‚ thậm chí mang cả vào bồn tắm.<br> ',
2183: 'Thuốc súng sẽ bị ẩm mất đấy.<br>Thôi‚ Veera đã mua gì nào?<br> ',
2194: 'Em thì nhé...<br>cái này!<br> ',
2243: 'Ừm‚ đây là... trượng ạ?<br>Còn đây là nhẫn gắn viên ngọc đỏ‚ rồi thuốc trong lọ...?<br> ',
2302: 'Trượng ma pháp‚ nhẫn khuếch đại ma lực‚ và cả thuốc hồi phục ma lực...?<br>Chất lượng món nào cũng tốt nhỉ~. Đến chị còn muốn có chúng... hửm?<br> ',
2313: 'Veera‚ em... chẳng lẽ em chọn toàn thứ chị muốn sao?<br> ',
2364: 'Khi đi mua sắm‚ em cứ vô thức cầm những thứ có ích cho chị...<br>Nhưng nếu là thứ khiến chị vui thì chắc ai nhận cũng vui đúng không?<br> ',
2409: 'Lý lẽ kiểu gì vậy hả!?<br> ',
2468: 'Thật là... thôi cũng được. Mấy thứ đó chị sẽ dùng.<br>Vậy Wendy đã mua gì nào~?<br> ',
2517: 'Chuyện là... em đã hỏi các anh lính xem Chỉ Huy có vẻ thích gì<br>rồi ghi chú lại‚ nhưng mãi vẫn chưa tìm ra...<br> ',
2574: 'Em đã điều tra trước cơ à. Hì hì‚ khá lắm~♪<br>Để xem nào. Anh Chỉ Huy thích thứ gì đây ta~~――<br> ',
2874: '<size=48>――Khu Rừng Gần Căn Cứ Tiền Tuyến</size>',
2919: 'Nhắc đến tiệc thì món ngon rất quan trọng nhỉ~.<br>Trong khu rừng này chắc sẽ kiếm được nguyên liệu tươi đấy.<br> ',
2930: 'Ưm... ồ‚ tìm thấy rồi!<br>Măng này cứ như mọc lên để được chị tìm thấy vậy~♪<br> ',
2941: 'Yếu xìu~ yếu xìu~~♪<br>Đang lớn dở mà bị tìm thấy và ăn mất dễ dàng‚ cây măng yếu xìu~~♪<br> ',
2986: 'Đúng là chị! Chị đã tìm được nhiều thế rồi!<br> ',
3029: 'Hừ hừ~ đúng chứ~?<br>Nếu là chị thì một hai cây măng chỉ là chuyện dễ như――<br> ',
3089: 'Wendy-san giỏi quá! Đã có nhiều thế này rồi!<br>Nấm chất thành cả núi luôn!<br> ',
3136: '...Hả?<br> ',
3181: 'Hướng hai giờ‚ cự ly 20... hướng mười một giờ‚ cự ly 32...<br>À‚ ở gốc cây cạnh Veera-san cũng có nữa!<br> ',
3238: 'Đúng thật... năng lực dò tìm của Wendy-san tuyệt quá.<br>Chỉ trong chớp mắt đã gom được nhiều thế này rồi.<br> ',
3249: 'Ehehe‚ được khen nhiều vậy em ngại quá~♪<br>Vì em là automata nên mấy việc thế này là sở trường của em!<br> ',
3298: '...H-hứ. Được thôi‚ chị không quan tâm... nói chứ chị theo phe măng<br>hơn nấm... mà phần lớn nhân loại cũng vậy thôi...<br> ',
3365: 'À‚ ừ-ừm――măng chị hái có màu sắc và độ bóng<br>đẹp lắm~. Hình dáng cũng rất tuyệt‚ kiểu như... rất nghệ thuật nhỉ.<br> ',
3416: 'Đừng cố gượng khen chị~~!<br>Lòng tốt kiểu đó mới đâm vào tim chị đau nhất đó~~!<br> ',
3477: 'K-không sao đâu Verisa-san!<br>N-nhìn này‚ vì phần của Verisa-san ít hơn nên nấu cũng đỡ mất công hơn mà!<br> ',
3530: 'Không phải an ủi chút nào hết~~!<br> ',
3565: '――Vài ngày sau<br>Công tác chuẩn bị cho bữa tiệc bất ngờ đang tiến triển thuận lợi.<br> ',
3606: 'Nguyên liệu đã hái thì bảo quản rồi‚ đạo cụ và quà cũng đã chuẩn bị xong...<br>Tốt‚ mọi thứ đang rất thuận lợi!<br> ',
3663: 'Hăng hái ghê nhỉ Wendy. Sau khi bọn chị ngủ‚ hình như em còn thức đến tận khuya<br>để làm đồ trang trí nữa. Em thật sự muốn anh Chỉ Huy vui lắm nhỉ~.<br> ',
3674: 'Ừ. Thấy Wendy-san cố gắng đến vậy<br>em cũng nghĩ nhất định phải làm bữa tiệc thành công vì bạn ấy.<br> ',
3685: 'Đúng rồi... vậy càng không thể để em ấy gục được<br>nên chị nên nhắc trước một câu nhỉ~.<br> ',
3745: 'Không biết Chỉ Huy có vui không nhỉ~.<br>Hì hì‚ mình phải cố hơn nữa để bữa tiệc thật tuyệt!<br> ',
3824: '...Cố gắng thì tốt thôi Wendy.<br>Nhưng em không thấy mình hơi quá sức rồi sao~?<br> ',
3835: 'Anh Chỉ Huy cũng từng nói rồi mà~? Dù em là automata<br>nếu dùng quá mức thì vẫn có thể phát sinh vấn đề đó.<br> ',
3888: 'Em ổn mà! Từ trước đến giờ em còn chưa từng bị cảm!<br>Hơn nữa‚ ở bữa tiệc em nhất định muốn Chỉ Huy vui vẻ!<br> ',
3947: 'Rồi rồi‚ hiểu rồi hiểu rồi~.<br>Thôi‚ còn lại chỉ là nấu nướng và trang trí trong ngày đó nên chắc ổn thôi.<br> ',
3958: 'Phải làm sao để ngài Chỉ Huy không phát hiện<br>nên lúc anh ấy vắng mặt chúng ta phải trang trí một lượt cho xong nhỉ.<br> ',
3969: 'Chắc chắn anh ấy sẽ bất ngờ lắm~. Vừa về đã thấy ký túc xá được<br>trang trí lộng lẫy mà. Hì hì‚ chị thấy háo hức rồi~♪<br> ',
4018: 'Đúng rồi! Chúng ta hãy cùng hô quyết tâm để nâng cao sĩ khí nhé!<br>Em hay làm với các anh lính lắm!<br> ',
4077: 'Hay đấy. Nào chị cũng làm đi.<br> ',
4088: 'Rồi rồi~. Hôm nay đặc biệt chị chiều theo vậy♪<br> ',
4137: 'Vậy thì... nhất định phải làm thành công nhé! Một‚ hai――!<br> ',
4156: 'Piiiiii-gagagagagagaga!!<br> ',
4223: 'Ểểểểểể!!??<br> ',
}

REVIEW = {
2585: 'adult-uncertain reference: erotic novels and nude paintings; kept EN per instruction',
2636: 'adult-uncertain reaction adjacent to explicit-shopping joke; kept EN per instruction',
2695: 'adult-uncertain reference to Commander preferences; kept EN per instruction',
2744: 'adult-uncertain purchase intent for erotic novels; kept EN per instruction',
2802: 'adult-uncertain euphemism for male self-comfort; kept EN per instruction',
2813: 'adult-uncertain request for erotic novels; kept EN per instruction',
2847: 'adult-uncertain intervention line; kept EN per instruction',
}

raw = en_asset.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8-sig') if raw.startswith(b'\xef\xbb\xbf') else raw.decode('utf-8')
lines = text.splitlines()
out = lines[:]

# helpers
def fields(line): return line.split(',')
def set_field(line, idx, value):
    parts = line.split(',')
    parts[idx] = value
    return ','.join(parts)

for ln, val in T.items():
    line = out[ln-1]
    if line.startswith('title,'):
        out[ln-1] = set_field(line, 1, val)
    elif line.startswith('messageTextCenter,'):
        out[ln-1] = set_field(line, 2, val)
    elif line.startswith('message,'):
        out[ln-1] = set_field(line, 2, val)
    else:
        raise RuntimeError(f'Line {ln} is not translatable record: {line!r}')

# Review lines remain original EN intentionally
vi_asset.parent.mkdir(parents=True, exist_ok=True)
out_text = newline.join(out) + (newline if text.endswith(('\n','\r')) else '')
vi_asset.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8'))

ja = json.loads(ja_json.read_text(encoding='utf-8'))
en = json.loads(en_json.read_text(encoding='utf-8'))
keys = list(ja.keys())

# identify translatable records in asset order
record_lines=[]
for i,l in enumerate(lines,1):
    if l.startswith('title,') or l.startswith('message,') or l.startswith('messageTextCenter,'):
        record_lines.append(i)

# Build QA
issues=[]
orig_counts=[len(x.split(',')) for x in lines]
out_counts=[len(x.split(',')) for x in out]
for i,(a,b) in enumerate(zip(orig_counts,out_counts),1):
    if a!=b: issues.append({'severity':'BLOCKER','line':i,'type':'field_count','source_count':a,'output_count':b})
if len(lines)!=len(out): issues.append({'severity':'BLOCKER','type':'line_count','source':len(lines),'output':len(out)})

tag_re=re.compile(r'<[^>]+>')
ph_re=re.compile(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]')
technical_fields_checked = 0
nontext_lines_checked = 0
for i,(a,b) in enumerate(zip(lines,out),1):
    if tag_re.findall(a)!=tag_re.findall(b):
        issues.append({'severity':'BLOCKER','line':i,'type':'tag_mismatch','source':tag_re.findall(a),'output':tag_re.findall(b)})
    if ph_re.findall(a)!=ph_re.findall(b):
        issues.append({'severity':'BLOCKER','line':i,'type':'placeholder_mismatch','source':ph_re.findall(a),'output':ph_re.findall(b)})
    if a.count(',')!=b.count(','):
        issues.append({'severity':'BLOCKER','line':i,'type':'delimiter_count','source':a.count(','),'output':b.count(',')})
    ap, bp = a.split(','), b.split(',')
    if len(ap) == len(bp):
        if a.startswith('title,'):
            technical_fields_checked += 1
            if ap[0] != bp[0]:
                issues.append({'severity':'BLOCKER','line':i,'type':'technical_field_changed','source':ap[0],'output':bp[0]})
        elif a.startswith('messageTextCenter,'):
            technical_fields_checked += 1
            if ap[:2] + ap[3:] != bp[:2] + bp[3:]:
                issues.append({'severity':'BLOCKER','line':i,'type':'technical_field_changed','source':ap[:2]+ap[3:],'output':bp[:2]+bp[3:]})
        elif a.startswith('message,'):
            technical_fields_checked += 1
            if ap[:2] + ap[3:] != bp[:2] + bp[3:]:
                issues.append({'severity':'BLOCKER','line':i,'type':'technical_field_changed','source':ap[:2]+ap[3:],'output':bp[:2]+bp[3:]})
        else:
            nontext_lines_checked += 1
            if a != b:
                issues.append({'severity':'BLOCKER','line':i,'type':'nontext_line_changed','source':a,'output':b})

# Check ASCII comma inside translated fields by verifying delimiter count suffices. Also spot accidental ASCII comma in field values for T.
for ln,val in T.items():
    if ',' in val:
        issues.append({'severity':'BLOCKER','line':ln,'type':'ascii_comma_in_vi_text','text':val})

manifest=[]
for idx, ln in enumerate(record_lines):
    line=lines[ln-1]
    out_line=out[ln-1]
    if line.startswith('title,'):
        src_en=line.split(',')[1]; vi=out_line.split(',')[1]
        rec_type='title'; speaker=''
    elif line.startswith('messageTextCenter,'):
        src_en=line.split(',')[2]; vi=out_line.split(',')[2]
        rec_type='messageTextCenter'; speaker=''
    else:
        parts=line.split(','); oparts=out_line.split(',')
        src_en=parts[2]; vi=oparts[2]; rec_type='message'; speaker=parts[1]
    status = 'REVIEW' if ln in REVIEW else ('TRANSLATED' if vi!=src_en else 'EXACT')
    # Match by order to novels; asset lacks one JP entry? record_lines length should equal keys length
    jp_src = keys[idx] if idx < len(keys) else None
    en_ref = en.get(jp_src) if jp_src else None
    manifest.append({
        'asset_line': ln,
        'record_type': rec_type,
        'speaker': speaker,
        'jp_source': jp_src,
        'en_reference': en_ref,
        'asset_en': src_en,
        'vi_output': vi,
        'status': status,
        'match_status': 'EXACT' if (en_ref and src_en.strip()==en_ref.strip()) else ('CONTEXT_MATCH' if en_ref else 'UNMATCHED'),
        'note': REVIEW.get(ln, '')
    })

qa = {
    'file': 'evs_10200010201.txt',
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'source': str(en_asset),
    'output': str(vi_asset),
    'line_count_source': len(lines),
    'line_count_output': len(out),
    'translatable_records': len(record_lines),
    'translated_records': sum(1 for m in manifest if m['status']=='TRANSLATED'),
    'review_records_kept_en': sum(1 for m in manifest if m['status']=='REVIEW'),
    'blockers': [x for x in issues if x['severity']=='BLOCKER'],
    'issues': issues + [{'severity':'REVIEW','line':ln,'type':'adult_uncertain_kept_en','note':note} for ln,note in REVIEW.items()],
    'technical_fields_checked': technical_fields_checked,
    'nontext_lines_checked': nontext_lines_checked,
    'technical_fields_unchanged': not any(x.get('type') in {'technical_field_changed','nontext_line_changed'} for x in issues),
    'delimiter_counts_unchanged': not any(x.get('type') == 'delimiter_count' for x in issues),
    'tags_unchanged': not any(x.get('type') == 'tag_mismatch' for x in issues),
    'placeholders_unchanged': not any(x.get('type') == 'placeholder_mismatch' for x in issues),
    'hashes': {
        'en_sha256': hashlib.sha256(raw).hexdigest(),
        'vi_sha256': hashlib.sha256(vi_asset.read_bytes()).hexdigest(),
    },
    'newline': 'CRLF' if newline=='\r\n' else 'LF',
    'encoding': 'UTF-8-BOM' if raw.startswith(b'\xef\xbb\xbf') else 'UTF-8',
}

(work/'manifest.json').write_text(json.dumps({'records': manifest, 'summary': {k: qa[k] for k in ['file','timestamp_utc','translatable_records','translated_records','review_records_kept_en']}}, ensure_ascii=False, indent=2), encoding='utf-8')
(work/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

diff_lines = list(difflib.unified_diff(lines, out, fromfile=str(en_asset), tofile=str(vi_asset), lineterm=''))
# Focused diff: only hunks around changed/review records, still full unified diff from changed lines
md = ['# Focused Diff — evs_10200010201.txt', '', f'- Output: `{vi_asset}`', f'- Translated records: {qa["translated_records"]}', f'- REVIEW kept EN: {qa["review_records_kept_en"]}', '', '```diff']
md.extend(diff_lines)
md.append('```')
(work/'focused_diff.md').write_text('\n'.join(md), encoding='utf-8')

print(json.dumps({
    'output': str(vi_asset),
    'manifest': str(work/'manifest.json'),
    'qa_log': str(work/'qa_log.json'),
    'diff': str(work/'focused_diff.md'),
    'line_count': [len(lines), len(out)],
    'records': len(record_lines),
    'translated': qa['translated_records'],
    'review': qa['review_records_kept_en'],
    'blockers': len(qa['blockers'])
}, ensure_ascii=False, indent=2))
if qa['blockers']:
    raise SystemExit(2)
