# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib, json, re, difflib

scene = 'hmn_10030100003'
root = Path('E:/AgentTranslation')
en_asset = root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{scene}.txt'
vi_asset = root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{scene}.txt'
ja_json = root/'dotabyss-translation-main/translations/novels'/scene/'ja.json'
en_json = root/'dotabyss-translation-main/translations/novels'/scene/'en.json'
work = root/'dotabyss-rpg-vn-translator/work/hmn_10030100003_full'
work.mkdir(parents=True, exist_ok=True)

# Ordered Vietnamese strings aligned to asset candidate text records:
# title, messageTextCenter, then message/messageText* records in physical file order.
vi_texts = [
    'Cách Dùng Gold Đúng Đắn',
    '<size=48>――Hội Trường Đấu Giá――</size>',
    '『Quả Cầu Cổ Đại』 đang phong ấn một quái vật hùng mạnh!<br>Một triệu gold! Có ai ra giá cao hơn không?<br> ',
    'Khụ… mình tới giới hạn rồi…<br> ',
    'Ôi‚ bỏ cuộc rồi sao?<br>Vượt qua giới hạn rồi mới là lúc vui đấy nhé?<br> ',
    'Cô mang theo bao nhiêu đồng vàng vậy chứ…<br>Đúng là thương nhân đáng sợ…<br> ',
    'Em mạnh tay thật đấy‚ Marina?<br> ',
    'Hì hì‚ thật ra em đã thu xếp bán nó cho thương hội ở Eldorana<br>với giá 8 triệu gold rồi.<br> ',
    'Tám… tám triệu!?<br> ',
    'May là mọi người có vẻ đã dùng hết ngân sách.<br>Vì em thật sự muốn thắng món này mà.<br> ',
    'Chịu thật… buổi đấu giá này đúng là sân khấu riêng của Marina rồi.<br> ',
    'Hay là anh lại phải lòng em thêm lần nữa rồi ạ?<br> ',
    'Ừ‚ anh mê em thật rồi.<br>Marina đúng là một người phụ nữ tuyệt vời.<br> ',
    'Anh nói thẳng như vậy làm em ngượng đấy～.<br> ',
    'Không còn ai nữa nhỉ… Vậy chốt giá một triệu!<br>Xin chúc mừng!<br> ',
    'Người chủ trì gõ búa chan chát.<br>Như phản ứng với âm thanh đó‚ quả cầu rung lên rồi tuôn ra luồng hào quang đen ngòm.<br> ',
    'Gruooooon!!!<br> ',
    'Hả!? Đột nhiên có quái vật!?<br>Không lẽ…!<br> ',
    'Nó được giải phóng khỏi 『Quả Cầu Cổ Đại』 rồi!<br>Khốn thật‚ gã chủ trì đó quản lý chẳng ra gì!<br> ',
    'Kh‚ không thể nào～!!<br> ',
    'Gaaaaaaaah!<br> ',
    'Á áá! Q‚ quái vật kìa!<br> ',
    'Chạy đi!<br> ',
    'Khi quái vật cử động thân hình khổng lồ‚ hội trường đấu giá nhanh chóng sụp đổ.<br>Người tham gia và khách xem lập tức bỏ chạy tán loạn.<br> ',
    'Tch! Lại thêm chuyện phiền phức…<br>Phải tìm cách hạ nó ngay tại đây.<br> ',
    'Con quái một triệu gold kia trông mạnh thật nhỉ.<br> ',
    'Đừng gọi quái vật bằng giá trúng thầu.<br>Nhưng… đúng là rắc rối thật.<br> ',
    'Những người có thể trông cậy chỉ còn đám lính gác được thuê bảo vệ buổi đấu giá…<br>và em thôi‚ Marina.<br> ',
    'Em ạ?<br>Con quái trông mạnh đến thế thì dù là em cũng không thể đâu.<br> ',
    'Em có vũ khí và đạo cụ vừa đấu giá được còn gì!<br>Dùng chúng thì chắc chắn sẽ gây đủ sát thương!<br> ',
    'Hả!? Em không thể lãng phí như thế được!<br>Tiền trúng thầu có được hoàn lại không ạ!?<br> ',
    'Giờ là lúc nói chuyện đó sao!?<br> ',
    'Chạy mau!!!<br> ',
    'Này! Các ngươi chạy đi đâu hả!<br> ',
    'Chết tiệt! Gã chủ trì đó chẳng thuê nổi lính gác tử tế nào…<br> ',
    'Phu quân‚ xin hãy cho em một chút thời gian.<br>Marina này nhất định sẽ đáp lại kỳ vọng của phu quân♪<br> ',
    'Được! Anh sẽ gom đám lính gác bỏ chạy lại!<br> ',
    'Trước hết… dùng 『Đèn Đá Hộ Vệ』 vừa đấu giá được nào.<br>Đây!<br> ',
    'Một bức tường ánh sáng rực rỡ triển khai trước mặt những lính gác đang hoảng loạn bỏ chạy.<br> ',
    'Các ngươi bình tĩnh lại! Đây là tiền tuyến căn cứ‚<br>một con quái vật chẳng đáng sợ!<br> ',
    'Từ giờ Chỉ Huy tiền tuyến căn cứ là ta sẽ chỉ huy!<br>Giơ vũ khí lên‚ câu giờ cho dân thường sơ tán!<br> ',
    'R‚ rõ rồi…!<br> ',
    'C‚ chuyện này thành ra kinh khủng quá rồi…<br> ',
    '…Nào nào‚ thưa ngài chủ trì ở đằng kia.<br>Tình hình khó xử rồi nhỉ?<br> ',
    'À‚ à…?<br>Cô là thương nhân lúc nãy mua đủ thứ kia…<br> ',
    'Nhờ phu quân nhanh trí nên hiện giờ người bị thương chỉ có thuộc hạ của ông.<br>Nhưng nếu cứ bỏ mặc thế này‚ thành phố sẽ chịu thiệt hại rất lớn.<br> ',
    'Nếu có người chết thì tiền bồi thường sẽ lớn đến mức nào nhỉ?<br>Ông là người mang quả cầu tới‚ phá sản là điều khó tránh đấy…?<br> ',
    'Không thể nào… kết thúc vì chuyện thế này sao…!<br> ',
    'Vậy nên em muốn thương lượng. Nếu ông chấp nhận đề nghị của em‚<br>em sẽ xử lý con quái vật kia cho♪<br> ',
    'Hợp đồng ở đây ạ.<br>Nếu đồng ý với nội dung‚ xin hãy ký xác nhận♪<br> ',
    'Đó là một bản hợp đồng ngắn như viết vội‚ nhưng đầy đủ những điều khoản cần thiết.<br>Người chủ trì đấu giá tái mặt khi nhìn thấy nội dung.<br> ',
    'Hoàn trả số vàng đã nhận‚<br>lại còn giao cả hàng đấu giá… sao!?<br> ',
    'Cô bắt ta ký hợp đồng vô lý thế này sao!?<br>Trong khi còn chẳng có gì đảm bảo cô thật sự hạ được nó!<br> ',
    'Chỗ đó thì ông chỉ còn cách tin em thôi.<br>Dưới con mắt của một thương nhân như ông‚ em trông thế nào?<br> ',
    'Kh… ưưư…<br> ',
    'Trước Marina đang đứng đầy tự tin và không hề dao động giữa tình thế nguy cấp‚<br>người chủ trì cầm bút với vẻ mặt cay đắng.<br> ',
    'Được rồi‚ nhờ cô đấy…!<br> ',
    '…Em xin kính trọng quyết định của ông.<br>Thương nhân Marina này nhất định sẽ giữ đúng hợp đồng♪<br> ',
    'Gruooooon! Gaaaaaaaah!!!<br> ',
    'Bị cú đánh tức tối của quái vật giáng xuống‚ bức tường ánh sáng đang triển khai kêu răng rắc‚<br>chớp tắt rồi sụp đổ.<br> ',
    'U‚ uwaaaaaa!!<br> ',
    'Sắp tới giới hạn rồi sao…<br>Marina‚ vẫn chưa xong à…!<br> ',
    'Để phu quân đợi lâu rồi!<br>Thương lượng thành công♪<br> ',
    'Marina! Em chuẩn bị xong chưa!?<br> ',
    'Vâng‚ cứ giao cho em♪<br> ',
    'Một khi hợp đồng đã ký kết‚ chẳng còn lý do gì phải do dự nữa.<br>Từ đây là màn chi mạnh tay‚ đợt giảm giá đặc biệt bắt đầu♪<br> ',
    'Món đầu tiên là 『Chiến Phủ Bạo Viêm』 vừa trúng thầu.<br>Cùng với 『Đại Thương Băng Thụ』 mà em vất vả giành được‚ nào!<br> ',
    'Gruooooogh!?<br> ',
    'Những vũ cụ Marina ném ra khiến ma lực ẩn chứa bên trong bạo tẩu.<br>Vụ nổ sinh ra làm quái vật mất thăng bằng.<br> ',
    'Em dùng những món vừa đấu giá được sao…!?<br>Em thật sự đã ký được hợp đồng rồi!<br> ',
    'Nhưng để hạ nó‚<br>vẫn chưa đủ sức phá hủy…!<br> ',
    'Ôi‚ em đã nói là sẽ chi mạnh tay rồi mà?<br>Đợt sale của Marina vẫn còn lâu mới kết thúc!<br> ',
    'Hàng đặc giá hôm nay gồm 『Falchion Lôi Thiểm』 và 『Thủy Tinh Thường Ám』‚<br>『Lõi Ma Lực Phong Lang』‚ 『Kết Tinh Núi Lửa Ngục Viêm』‚ 『Mảnh Cầu Vồng』――<br> ',
    'Khoan đã! Em chuẩn bị bao nhiêu thứ vậy!?<br>Dù thế nào thì em cũng đâu trúng thầu nhiều đến thế!?<br> ',
    'Đó đều là những món em nhận được qua giao dịch công bằng‚ xin anh cứ yên tâm.<br>Nào‚ hãy nếm thật kỹ sức mạnh của thương nhân nhé♪<br> ',
    'Gaaaawooooogh!?<br> ',
    'Marina liên tục ném vũ khí và đạo cụ ma pháp không ngừng.<br>Ma lực của sấm sét‚ bóng tối‚ gió‚ lửa và ánh chớp nổ tung‚ khiến quái vật đau đớn khựng lại.<br> ',
    'Và đây là sản phẩm nổi bật.<br>Vì tiền tuyến căn cứ‚ nếu cần thì sẽ dùng――『Ma Đạo Bạo Thạch』 mà em đã hứa với phu quân!<br> ',
    'Xin hãy thưởng thức đến tận cuối cùng!<br> ',
    'Marina ném 『Ma Đạo Bạo Thạch』 vào con quái vật không thể cử động.<br>Sức nổ khổng lồ được giải phóng trong nháy mắt――<br> ',
    'Goaaaaaaagh!?<br> ',
    'Không chịu nổi sức phá hủy vượt quá giới hạn‚<br>con quái vật gầm lên tiếng cuối cùng rồi đổ gục.<br> ',
    'Em thật sự hạ được nó<br>chỉ bằng sức mạnh của những món hàng có ở đây sao…<br> ',
    'Đây là cách dùng tiền đúng đắn. Chính là biết vận dụng vốn liếng.<br>Phu quân thấy thế nào?<br> ',
    '…Anh thật sự khâm phục.<br>Một thương vụ tuyệt vời đấy‚ Marina.<br> ',
    'Hì hì hì‚ em rất vinh hạnh.<br>Phu quân cũng chỉ huy rất xuất sắc đấy♪<br> ',
    'Haizz… dùng hết sạch đạo cụ vừa lấy được‚<br>cuối cùng chẳng thu được gì cả…<br> ',
    'Thế cũng được mà～.<br>Theo hợp đồng thì tiền của những món đã dùng đều được hoàn lại rồi.<br> ',
    'Em cũng ký hợp đồng cung cấp vật tư cho căn cứ để đổi lấy việc không làm lớn chuyện.<br>Chắc Alicia cũng sẽ đồng ý thôi♪<br> ',
    '…Cuộc thương lượng đó cũng do Marina lo cả mà.<br>Nói là thi đấu‚ nhưng anh thua thảm rồi.<br> ',
    'Đúng vậy nhỉ‚ dù là đấu giá hay thương lượng‚<br>em vẫn chưa chịu thua phu quân đâu.<br> ',
    'Nhưng… khoảnh khắc bàn thương lượng biến thành chiến trường thật sự‚<br>em hoàn toàn không sánh được với lòng can đảm của phu quân.<br> ',
    'Quả không hổ là phu quân của em.<br>Anh tuyệt lắm đấy♪<br> ',
    'Con mắt đã tin vào anh của em không hề sai.<br>Em lại một lần nữa nghĩ như vậy♪<br> ',
    'Buổi đấu giá bị gián đoạn nên món đồ anh nhắm tới cũng không lấy được‚<br>lời đó là thành quả duy nhất rồi.<br> ',
    '…Món đồ anh nhắm tới sao?<br> ',
    'Phu quân có muốn em đoán xem anh muốn món nào không?<br> ',
    'Gì cơ…?<br>Dù là Marina thì anh nghĩ cũng không thể đâu…<br> ',
    'Trong catalog nó chỉ được ghi là 『Sách Cổ』‚ một món không rõ chi tiết.<br>Nhưng nhìn lai lịch 『tuyệt phẩm từng bị cấm lưu hành』 thì nội dung quá rõ rồi.<br> ',
    'Dù bị cấm vì quá táo bạo‚<br>nó vẫn được gọi là huyền thoại nhờ nội dung tuyệt vời và tranh minh họa của họa sĩ nổi tiếng…<br> ',
    'Marina nở một nụ cười sâu xa rồi lấy từ trong áo ra một cuốn sách.<br> ',
    'Cuốn 『Trò Đùa Của Nàng Elf Đã Có Chồng ～Bài Học Ma Pháp Dụ Hoặc Ban Đêm～』 này<br>chính là món phu quân nhắm tới phải không～?<br> ',
    'Đ‚ đó là…!!<br> ',
    'G‚ guuuuh! À‚ đúng vậy đấy!<br>Anh nhất định muốn thêm cuốn sách này vào bộ sưu tập của mình!<br> ',
    'Nhưng tại sao Marina lại có nó…!?<br>Đáng lẽ buổi đấu giá đã bị hủy trước khi cuốn sách đó được bán chứ!<br> ',
    'Em đã nhận nó như điều kiện để đánh lui quái vật.<br> ',
    'Nào phu quân‚ đến giờ thương lượng vui ơi là vui rồi.<br>Anh sẽ mua cuốn sách này với giá bao nhiêu ạ?<br> ',
    'Haizz… chịu thật.<br>Hễ nói tới buôn bán thì anh không thắng nổi Marina.<br> ',
    'Hì hì‚ Cửa hàng Marina có đủ mặt hàng đáp ứng nhu cầu của khách.<br>Xin hãy ghé dùng bất cứ lúc nào nhé‚ phu quân♪<br> ',
]

TEXT_TYPES = {'title':1, 'message':2, 'messageTextUnder':2, 'messageTextCenter':2}

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def read_pairs(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=list)

def newline_style(data):
    if b'\r\n' in data and data.count(b'\r\n') == data.count(b'\n'):
        return 'CRLF'
    return 'LF'

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%(?:\d+\$)?[sd]|\{\w+\}|\$\{\w+\}|\\[nrt]|%%', s)

def text_records(lines):
    out=[]
    counts={k:0 for k in TEXT_TYPES}
    for idx,line in enumerate(lines,1):
        body=line.rstrip('\r\n')
        parts=body.split(',')
        typ=parts[0] if parts else ''
        if typ in TEXT_TYPES:
            text_idx=TEXT_TYPES[typ]
            counts[typ]+=1
            out.append({'line':idx,'type':typ,'parts':parts,'text_idx':text_idx,'text':parts[text_idx],
                        'tech_sig':parts[:text_idx]+parts[text_idx+1:], 'comma_count':body.count(',')})
    return out, counts

def main():
    src_bytes = en_asset.read_bytes()
    bom = src_bytes.startswith(b'\xef\xbb\xbf')
    enc = 'utf-8-sig' if bom else 'utf-8'
    nl = '\r\n' if newline_style(src_bytes) == 'CRLF' else '\n'
    src_text = src_bytes.decode(enc)
    # split preserving exact line endings
    src_lines = src_text.splitlines(keepends=True)
    recs, counts = text_records(src_lines)
    blockers=[]; notes=[]
    if len(vi_texts) != len(recs):
        blockers.append({'code':'VI_COUNT_MISMATCH','expected':len(recs),'actual':len(vi_texts)})
    ja_pairs = read_pairs(ja_json)
    en_pairs = read_pairs(en_json)
    if len(ja_pairs) != len(recs) or len(en_pairs) != len(recs):
        notes.append({'code':'NOVEL_COUNT_DIFF','asset_records':len(recs),'ja_pairs':len(ja_pairs),'en_pairs':len(en_pairs)})
    # Build output
    out_lines = list(src_lines)
    entries=[]
    for n,(rec,vi) in enumerate(zip(recs,vi_texts),1):
        # Preserve the exact count of UI line-break tags in the authoritative EN asset.
        while vi.count('<br>') > rec['text'].count('<br>'):
            vi = vi.replace('<br>', ' ', 1)
        if ',' in vi:
            blockers.append({'code':'ASCII_COMMA_IN_VI_DRAFT','ordinal':n,'line':rec['line'],'text':vi})
        parts = list(rec['parts'])
        parts[rec['text_idx']] = vi
        out_lines[rec['line']-1] = ','.join(parts) + ('\r\n' if src_lines[rec['line']-1].endswith('\r\n') else '\n')
        jp = ja_pairs[n-1][0] if n-1 < len(ja_pairs) else None
        en_ref = en_pairs[n-1][1] if n-1 < len(en_pairs) else None
        entries.append({'ordinal':n,'line':rec['line'],'type':rec['type'],'speaker':rec['parts'][1] if len(rec['parts'])>1 else '',
                        'jp':jp,'en_asset':rec['text'],'en_novel':en_ref,'vi':vi,
                        'match_status':'EXACT' if en_ref and en_ref.replace(',', '，') == rec['text'] else 'CONTEXT_MATCH',
                        'translation_status':'TRANSLATED'})
    vi_asset.parent.mkdir(parents=True, exist_ok=True)
    if blockers:
        print('Draft blockers before write:', blockers)
        raise SystemExit(1)
    vi_text = ''.join(out_lines)
    vi_asset.write_bytes((('\ufeff' if bom else '') + vi_text).encode('utf-8'))
    out_bytes = vi_asset.read_bytes()
    out_text = out_bytes.decode(enc)
    out_lines2 = out_text.splitlines(keepends=True)
    out_recs, out_counts = text_records(out_lines2)
    # Independent QA
    delimiter_mismatch=[]; technical_mismatch=[]; tag_mismatch=[]; placeholder_mismatch=[]; ascii_comma=[]; unchanged=[]; jp_left=[]; targeted=[]
    japanese_re=re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
    english_patterns=re.compile(r'\b(?:Honey|Commander|Auction Hall|Run away|Marina\'s Emporium|Old Book|Play of a Married Elf|Night Temptation Magic Lesson|What\?|Ugh|Ah|Fufu|Fufufu|Ehh|Kyaaa|Mister|Mr\.)\b', re.I)
    allowed_unchanged=[]
    for src, dst in zip(recs, out_recs):
        if src['comma_count'] != dst['comma_count']:
            delimiter_mismatch.append({'line':src['line'],'src':src['comma_count'],'vi':dst['comma_count']})
        if src['tech_sig'] != dst['tech_sig']:
            technical_mismatch.append({'line':src['line'],'src':src['tech_sig'],'vi':dst['tech_sig']})
        if tags(src['text']) != tags(dst['text']):
            tag_mismatch.append({'line':src['line'],'src':tags(src['text']),'vi':tags(dst['text'])})
        if placeholders(src['text']) != placeholders(dst['text']):
            placeholder_mismatch.append({'line':src['line'],'src':placeholders(src['text']),'vi':placeholders(dst['text'])})
        if ',' in dst['text']:
            ascii_comma.append({'line':src['line'],'text':dst['text']})
        if src['text'] == dst['text']:
            unchanged.append({'line':src['line'],'text':dst['text']})
        # speaker names are allowed JP; text field should not contain JP besides intentional item title Kanji? We localized item titles.
        if japanese_re.search(dst['text']):
            jp_left.append({'line':src['line'],'text':dst['text']})
        m=english_patterns.search(dst['text'])
        if m:
            targeted.append({'line':src['line'],'match':m.group(0),'text':dst['text']})
    blockers2=[]
    for code, arr in [('DELIMITER_MISMATCH',delimiter_mismatch),('TECHNICAL_FIELD_MISMATCH',technical_mismatch),('TAG_MISMATCH',tag_mismatch),('PLACEHOLDER_MISMATCH',placeholder_mismatch),('ASCII_COMMA_IN_VI_TEXT',ascii_comma),('UNCHANGED_TEXT',unchanged),('JAPANESE_LEFTOVER',jp_left),('TARGETED_ENGLISH_LEFTOVER',targeted)]:
        if arr:
            blockers2.append({'code':code,'count':len(arr),'items':arr[:20]})
    # focused diff only text records
    before=[]; after=[]
    for src,dst in zip(recs,out_recs):
        before.append(f"L{src['line']} {src['type']} {src['text']}\n")
        after.append(f"L{dst['line']} {dst['type']} {dst['text']}\n")
    diff=''.join(difflib.unified_diff(before, after, fromfile='EN text fields', tofile='VI text fields', lineterm='\n'))
    (work/'focused_diff.md').write_text('```diff\n'+diff+'\n```\n', encoding='utf-8')
    manifest={
        'scene':scene,
        'status':'PASS' if not blockers2 else 'FAIL',
        'source':{'en_asset':str(en_asset),'ja_json':str(ja_json),'en_json':str(en_json),'sha256':sha256(src_bytes),'bytes':len(src_bytes),'bom':bom,'newline':newline_style(src_bytes),'line_count':len(src_lines)},
        'output':{'vi_asset':str(vi_asset),'sha256':sha256(out_bytes),'bytes':len(out_bytes),'bom':out_bytes.startswith(b'\xef\xbb\xbf'),'newline':newline_style(out_bytes),'line_count':len(out_lines2)},
        'candidate_counts':counts,
        'translated_records':len(out_recs),
        'entries':entries,
        'artifacts':{'manifest':str(work/'manifest.json'),'qa_log':str(work/'qa_log.json'),'focused_diff':str(work/'focused_diff.md'),'script':str(work/'generate_vi.py')}
    }
    qa={
        'scene':scene,
        'qa_status':'PASS' if not blockers2 else 'FAIL',
        'blockers':blockers2,
        'items':[],
        'notes':[{'code':'ADULT_RULE','message':'All characters confirmed 18+ by project context; adult-adjacent book title translated normally.'},
                 {'code':'ADDRESSING','message':'Marina uses phu quân/em toward Commander per 旦那さま and playful merchant-spouse tone; Commander uses anh/em.'}],
        'independent_verify':{
            'line_count':{'en':len(src_lines),'vi':len(out_lines2),'match':len(src_lines)==len(out_lines2)},
            'bom_match':bom==out_bytes.startswith(b'\xef\xbb\xbf'),
            'newline_match':newline_style(src_bytes)==newline_style(out_bytes),
            'candidate_counts':out_counts,
            'changed_text_records':sum(1 for a,b in zip(recs,out_recs) if a['text']!=b['text']),
            'delimiter_mismatch_count':len(delimiter_mismatch),
            'technical_field_mismatch_count':len(technical_mismatch),
            'tag_mismatch_count':len(tag_mismatch),
            'placeholder_mismatch_count':len(placeholder_mismatch),
            'ascii_comma_in_vi_text_count':len(ascii_comma),
            'unchanged_unlogged_text_records':len(unchanged),
            'japanese_leftover_count':len(jp_left),
            'targeted_english_leftover_count':len(targeted),
            'status':'PASS' if not blockers2 else 'FAIL'
        }
    }
    (work/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (work/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status':manifest['status'],'output':str(vi_asset),'qa':qa['independent_verify']}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
