from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE = 'evs_10200020301'
ROOT = Path('E:/AgentTranslation')
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/evs_10200020301_full'
MANIFEST = WORK / 'manifest.json'
QA_LOG = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'

VI = [
    'Tiêu Đề',
    'Ê ê ê! Các người tới đây làm cái quái gì vậy hả~~? Hả!?<br> ',
    '(Chỗ nào là “chủng tộc hiền lành” chứ…! Nhìn hung dữ thấy sợ!<br>Mình muốn nhờ họ hợp tác‚ nhưng liệu có thương lượng nổi không đây…?)<br> ',
    'Các người có biết mình đang ở đâu không hả!? Đây là Đảo Quỷ đấy—<br>cách xa làng mạc con người lắm! Nghĩ sao mà lặn lội tới tận đây vậy!?<br> ',
    'Đúng là tự làm khổ mình mà! Với lại bây giờ trên Đảo Quỷ này<br>đang có quái vật nguy hiểm lảng vảng! Ra ngoài nguy hiểm lắm đấy!!<br> ',
    'Khoan đã‚ nghe anh nói! Bọn anh không tới đây để gây chiến… hửm?<br> ',
    'Các người lặn lội tới đây thì bọn này vui là cái chắc rồi!<br>Nhưng chuyện gì cũng phải tùy lúc tùy chỗ chứ!<br> ',
    'Lỡ bị quái vật tấn công rồi mất mạng thì sao!!?<br>Đừng có làm mẹ mình khóc nghe chưa hả!!<br> ',
    '…Ừm. Lời lẽ thô lỗ thật‚ nhưng có vẻ họ đang lo cho chúng ta.<br>Đúng như Kureha nói‚ họ là một tộc người hiền lành.<br> ',
    'Có vẻ là vậy… dù cách nói chuyện của họ thô quá mức.<br>Vấn đề còn lại là liệu họ có chịu tin chúng ta không…<br> ',
    'Mọi người‚ lâu rồi không gặp.<br> ',
    'Hửmmmm~~~? Ai đấy… khoan‚ K-Kureha tiểu thư…!? Là Kureha tiểu thư kìa!!<br> ',
    'Ôi trời đất‚ cô về rồi sao! Thấy cô vẫn khỏe mạnh là mừng quá rồi!!<br> ',
    'Cô ấy quen họ à… Mình có nghe trên đường rằng Kureha là con gái thủ lĩnh Đảo Quỷ‚<br>nhưng còn được gọi là “tiểu thư” nữa sao…?<br> ',
    'Có vẻ từ đây mọi chuyện sẽ thuận lợi hơn rồi.<br>Đưa Kureha đi cùng quả là quyết định đúng đắn.<br> ',
    'Kureha tiểu thư‚ việc ở căn cứ tiền tuyến xong rồi sao?<br>Hay lần này cô về thăm nhà ạ?<br> ',
    'Vâng. Em trở về để giới thiệu người rất quan trọng với em<br>cho mọi người trên Đảo Quỷ.<br> ',
    'Người quan trọng…? Ý cô là người đứng bên kia à?<br> ',
    'Vâng‚ để em giới thiệu nhé! Đây là phu quân của em—Chỉ Huy căn cứ tiền tuyến‚<br>%user%♪ Còn bên cạnh là bà mối của chúng em‚ Shiraes-sama♪<br> ',
    '…!?<br> ',
    'Phu quân!? Lại còn bà mối!? Vậy tức là hai người sắp làm lễ cưới sao!?<br>Ra vậy ra vậy! Mối tình đầu của Kureha tiểu thư cuối cùng cũng thành rồi!!<br> ',
    'Thế thì đáng mừng quá! Được rồi! Tối nay cả Đảo Quỷ mở tiệc lớn!!<br>Mọi người cùng chúc mừng hôn lễ của Kureha tiểu thư nào~~~!!<br> ',
    'UOOOOOOOOOO~~~!!<br> ',
    'Cảm ơn mọi người rất nhiều! Em nhất định sẽ hạnh phúc!!<br> ',
    'Mọi người vui như chuyện của chính mình vậy. Ta cũng thấy hào hứng rồi.<br>Được‚ ta cũng ăn mừng cùng mọi người nào. Hò dô ta nào!<br> ',
    'Khoan khoan khoan!! Đừng tự tiện đẩy câu chuyện đi tiếp!!!!<br> ',
    '<size=48>——Đảo Quỷ. Khu Định Cư Của Quỷ Tộc. Phòng Của Kureha.</size>',
    'Vậy ra không phải lời chào hỏi trước hôn lễ sao…<br>Bọn này cứ tưởng giấc mơ của Kureha tiểu thư cuối cùng đã thành sự thật…<br> ',
    'Em xin lỗi mọi người… Chỉ vì phu quân đến Đảo Quỷ<br>làm em vui quá nên lỡ cao hứng mất rồi.<br> ',
    'Ngoan nào… không cần ủ rũ đâu‚ Kureha.<br>Ta sẽ dõi theo em dù mấy chục năm nữa. Bà mối lúc nào ta cũng sẵn lòng làm.<br> ',
    'Ưưư… Mẹ Shiraes~~!<br> ',
    '…Hiểu lầm được giải tỏa thì tốt rồi‚ nhưng sao cứ như<br>anh mới là kẻ xấu vậy…?<br> ',
    'Này‚ mang tới rồi đây!! Xin lỗi đã để đợi lâu nghe chưa!!<br> ',
    '(Hết hồn… quỷ tộc lúc nào cũng phải hét lên mới chịu được sao…?<br>Thế này thì bị con người sợ cũng phải.)<br> ',
    'Ừm… đây đúng là viên pha lê đã bị lấy trộm của chúng ta.<br>Tìm lại được là tốt rồi.<br> ',
    'Quả nhiên là vậy. Thứ này trôi dạt vào bờ vài ngày trước.<br>Thấy nó quý quá nên bọn này định biến nó thành báu vật của Đảo Quỷ.<br> ',
    'Trôi dạt vào bờ à… vậy là tên trộm không trực tiếp mang nó tới đây.<br>Chắc giữa đường đã xảy ra chuyện gì đó.<br> ',
    'Kết luận như vậy là hợp lý. Có lẽ viên pha lê đã rơi xuống sông<br>vào lúc nào đó rồi bị dòng nước cuốn tới Đảo Quỷ này.<br> ',
    'Vậy thì cũng không rõ tên trộm còn sống hay không. Bắt được hắn<br>thì tốt nhất‚ nhưng trước mắt lấy lại được viên pha lê là ổn rồi.<br> ',
    'Mà nói thật… ai ngờ thứ này lại có sức dụ quái vật tới chứ.<br>Thảo nào dạo này quái vật nhiều bất thường.<br> ',
    'Khi thủ lĩnh đi công chuyện xa trở về‚<br>chắc ông ấy sẽ ngã ngửa vì kinh ngạc mất!<br> ',
    'Thủ lĩnh… tức là cha của Kureha.<br> ',
    'Vâng. Hiếm có dịp nên em vốn muốn giới thiệu phu quân với cha và mẹ<br>rồi tiến thẳng tới lễ đính ước luôn… tiếc thật.<br> ',
    'Chào hỏi gia đình thì còn được‚ nhưng đừng thản nhiên chen cả lễ đính ước<br>vào!<br> ',
    'Dù sao thì Đảo Quỷ cũng đã chịu nhiều phiền phức. Bọn anh sẽ thu hồi<br>viên pha lê này‚ nên chắc sẽ không còn vấn đề gì nữa. Cứ yên tâm.<br> ',
    'Ừm… à… phải‚ đúng vậy…<br> ',
    '(Sao vậy…? Họ có vẻ thất vọng lạ thường…<br>Cũng không giống chỉ là tiếc vì phải bỏ báu vật.)<br> ',
    'Có vẻ các người còn điều gì bận lòng nhỉ?<br> ',
    '…Không‚ thật ra là. Bọn này đã nói dạo gần đây vì ảnh hưởng của viên pha lê đó<br>mà quái vật tăng lên rồi đúng không?<br> ',
    'Bọn này đã hạ chúng trước khi chúng kịp tấn công làng của con người.<br>Cảm giác như cuối cùng cũng giúp ích được cho con người… nên vui lắm…<br> ',
    '…Nhắc mới nhớ‚ trên đường tới đây chúng ta đi qua vài ngôi làng<br>của con người‚ và không nơi nào bị quái vật tấn công cả.<br> ',
    'Con người được an toàn là nhờ các người. Nhưng tại sao<br>các người lại làm vậy?<br> ',
    'Con người còn chẳng biết các người đã chiến đấu vì họ.<br>Dù chiến đấu nhiều đến đâu‚ các người cũng sẽ không được cảm ơn đâu nhỉ?<br> ',
    'Ừ… đúng vậy. Nhưng mà… nghe bọn này nói đã‚ đừng cười nhé?<br>Bọn này… muốn hòa thuận với con người.<br> ',
    '…Hòa thuận? Tôi nghe nói quỷ tộc bị con người sợ hãi nên tự rút về Đảo Quỷ.<br>Các người không oán hận những con người đã không chấp nhận mình sao?<br> ',
    'Oán hận á!? Không đời nào! Bọn này chưa từng oán hận con người!<br>Nhìn bộ dạng bọn này đi. Họ sợ cũng đâu trách được chứ!<br> ',
    'Nhưng… bọn này cứ nghĩ nếu bảo vệ con người khỏi quái vật‚<br>biết đâu một ngày nào đó có thể làm bạn… thế là lại hy vọng…<br> ',
    '(…Bị sợ chắc là vì cách nói chuyện lúc nào cũng đáng sợ đấy…<br>Nhưng dù sao‚ tấm lòng họ hiền hậu là điều chắc chắn.)<br> ',
    'Chỉ Huy. Đúng như Kureha từng nói‚<br>họ thật sự là một tộc người có tấm lòng nhân hậu.<br> ',
    'Ừ. Bỏ qua cách ăn nói thô lỗ‚<br>cứ bị hiểu lầm mãi như vậy thật đáng thương.<br> ',
    'Đừng lo! Em biết mọi người có thể làm bạn với con người mà!<br>Ở căn cứ tiền tuyến em cũng đã kết bạn được với rất nhiều người đấy!<br> ',
    'Nói thì dễ lắm Kureha tiểu thư. Nhưng đó là vì cô dễ thương<br>và tốt bụng‚ lại được thủ lĩnh dạy lễ nghi đàng hoàng nữa.<br> ',
    'Bọn này đâu thể cư xử giống Kureha tiểu thư được…<br>Bọn này còn không biết phải làm gì để kết bạn với con người…<br> ',
    'Cách để kết bạn sao… Ừm~‚ trước hết cần hóa giải hiểu lầm‚<br>nhưng phải làm sao để thay đổi hình ảnh Đảo Quỷ đây… Ừm~‚ ừmmm~~...<br> ',
    '…Em nghĩ ra rồi! Hay là chúng ta quảng bá Đảo Quỷ thì sao?<br>Mời mọi người tới đây để họ biết văn hóa quỷ tộc và sự tốt bụng của mọi người!<br> ',
    'Để mọi người biết về bọn này…? Dù cô nói vậy‚ Kureha tiểu thư…<br>Dù bọn này làm gì thì con người vẫn sợ bọn này thôi…<br> ',
    '“Dù làm gì” … sao?<br> ',
    '——Chính vì cứ nhút nhát như thế nên quỷ tộc mới mãi bị hiểu lầm!!<br>Khí thế thường ngày của mọi người đâu rồi!!?<br> ',
    'K-Kureha tiểu thư…?<br> ',
    'Em cũng tức lắm! Khi mọi người tốt bụng như vậy mà vẫn bị hiểu lầm!<br>Vì thế… đừng bỏ cuộc kiểu “dù sao cũng chẳng thay đổi” nữa‚ cùng cố gắng nào!!<br> ',
    'Nếu không tự mình đưa tay ra trước‚ kết bạn chỉ mãi là giấc mơ trong mơ thôi!!<br> ',
    'Trước cơn giận bộc phát của Kureha‚ quỷ tộc tròn mắt sững sờ.<br>Và %user% cũng không khác gì.<br> ',
    '(Lần đầu mình thấy Kureha nổi giận đến mức lớn tiếng như vậy…<br>Chắc cô ấy thật sự trân trọng đồng tộc của mình.)<br> ',
    '…Phải. Đúng rồi. Bỏ cuộc không giống bọn này chút nào!<br>Làm thôi nào‚ mọi người!<br> ',
    'Đúng vậy! Không làm lúc này thì nhục danh quỷ tộc mất!<br>Cùng dốc hết sức mà làm nào!<br> ',
    'Tinh thần đó đấy‚ mọi người…!! Em cũng đã không bỏ cuộc<br>mà liên tục theo đuổi phu quân‚ nên cuối cùng mới đính hôn được đấy!!<br> ',
    'Xin lỗi phải cắt ngang lúc mọi người đang hào hứng‚ nhưng chúng ta chưa đính hôn đâu.<br> ',
    '——Hì hì. Ta rất hiểu tấm lòng muốn kết thân với con người của các ngươi.<br>Xin hãy để ta góp sức nữa.<br> ',
    'Đừng lo. Mọi người nhất định sẽ hiểu các ngươi thôi—ta chắc chắn.<br>Ta‚ người rất hiểu con người‚ xin bảo đảm điều đó.<br> ',
    'Quan trọng hơn… ta cũng thấy mình muốn làm bạn với các ngươi.<br> ',
    'Mẹ Shiraes…!<br> ',
    'Đại tỷ Shiraes~~!<br> ',
    'Kureha và quỷ tộc xúc động tụ lại bên Shiraes<br>với nụ cười đầy từ ái. Lúc này‚ trái tim họ đã hòa làm một.<br> ',
    'Đượccc rồi~~~! Mọi người cùng cố gắng để kết bạn với con người nào~~~!<br> ',
    'ÔÔÔÔÔÔÔÔÔÔ——!!<br> ',
    'Được rồi—quyết tâm đã vững‚ vậy cứ thế cùng nhau<br>chạy về phía hoàng hôn nào!<br> ',
    'Không cần‚ không cần! Thật là‚ cứ mặc kệ các người<br>là lại lao đi không biết điểm dừng.<br> ',
    'À… ừm‚ phu quân. Em đã tự tiện đẩy mọi chuyện đi xa như vậy…<br>Có… có được không ạ…?<br> ',
    'Dù anh nói không được thì em cũng sẽ làm thôi nhỉ?<br>Hơn nữa‚ quỷ tộc đã giúp bọn anh bù đắp sai lầm. Bọn anh nợ họ.<br> ',
    'Nếu họ không hạ những quái vật đó‚ làng của con người hẳn đã bị thiệt hại.<br>…Anh không thể không giúp được.<br> ',
    'Vâng! Đúng là phu quân yêu dấu của em!<br>Trông thì hơi gai góc mà trong lòng lại dịu dàng… em yêu anh lắm!<br> ',
    '“Hơi gai góc” là thừa đấy…<br> ',
    'Chỉ Huy‚ ta biết mình là người châm ngòi chuyện này‚<br>nhưng cứ để viên pha lê nằm đó có thật sự ổn không?<br> ',
    'Không vấn đề gì. Theo Adelheid‚ viên pha lê này phát huy sức mạnh<br>dụ quái vật tới bằng cách hấp thụ ma lực‚ nhưng…<br> ',
    'Cô ấy đã chuẩn bị một chiếc hộp đặc chế để phong ấn sức mạnh của viên pha lê.<br>Miễn là đặt nó trong đó‚ sức mạnh của viên pha lê sẽ không rò rỉ ra ngoài.<br> ',
    'Ra vậy. Nếu thế thì không còn gì phải lo nữa.<br>Chúng ta hãy tập trung vào việc quảng bá quỷ tộc thôi.<br> ',
    'Ừ. Vậy thì… bắt đầu thôi nào!<br>Quảng bá quỷ tộc… và cả chính Đảo Quỷ nữa——!<br> ',
    'Mọi người cùng làm Đảo Quỷ náo nhiệt hơn nhé! Một‚ hai‚ dô~~~~!!<br> ',
    'UOOOOOOOOOOOOOO!!!!!<br> ',
]

TRANSLATABLE_PREFIXES = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def read_source(path):
    b = path.read_bytes()
    bom = b.startswith(b'\xef\xbb\xbf')
    text = b.decode('utf-8-sig')
    newline = 'CRLF' if b'\r\n' in b else 'LF'
    sep = '\r\n' if newline == 'CRLF' else '\n'
    has_final_newline = text.endswith('\n')
    lines = text.splitlines()
    return b, text, lines, bom, newline, sep, has_final_newline

def text_field_info(line):
    if line.startswith('title,'):
        parts = line.split(',', 2)
        return parts, 1
    if line.startswith('messageTextCenter,') or line.startswith('messageTextUnder,'):
        parts = line.split(',', 5)
        return parts, 2
    if line.startswith('message,'):
        parts = line.split(',', 5)
        return parts, 2
    return None, None

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z0-9_]+\}|\$\{[A-Za-z0-9_]+\}|%%', s)

def technical_signature(line):
    parts, idx = text_field_info(line)
    if parts is None:
        return line
    return parts[:idx] + parts[idx+1:]

def replace_field(line, value):
    parts, idx = text_field_info(line)
    parts[idx] = value
    return ','.join(parts)

def ascii_comma_in_text(s):
    return ',' in s

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)

    src_bytes, src_text, src_lines, bom, newline, sep, final_nl = read_source(EN_ASSET)
    ja_bytes = JA_JSON.read_bytes()
    en_json_bytes = EN_JSON.read_bytes()
    candidates = [(i, line) for i, line in enumerate(src_lines) if line.startswith(TRANSLATABLE_PREFIXES)]

    qa = {
        'scene': SCENE,
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'qa_status': 'PASS',
        'blockers': [],
        'items': [],
        'notes': [
            'JP is primary source; EN asset used only for alignment.',
            'All characters confirmed 18+ by task context; no H18 content in this asset.',
            'No existing VI file was found before generation; output created from EN asset structure.',
            'Proper names/placeholders preserved: Kureha, Shiraes, Adelheid, %user%.'
        ],
        'counts': {}
    }

    if len(VI) != len(candidates):
        qa['blockers'].append({'type': 'COUNT_MISMATCH', 'expected': len(candidates), 'actual': len(VI)})

    for n, v in enumerate(VI, 1):
        if ascii_comma_in_text(v):
            qa['blockers'].append({'type': 'ASCII_COMMA_IN_VI_FIELD', 'candidate_index': n, 'text': v})

    out_lines = list(src_lines)
    entries = []
    for idx, ((line_no0, src_line), vi) in enumerate(zip(candidates, VI), 1):
        out_lines[line_no0] = replace_field(src_line, vi)
        src_parts, src_idx = text_field_info(src_line)
        out_parts, out_idx = text_field_info(out_lines[line_no0])
        status = 'TRANSLATED'
        entries.append({
            'index': idx,
            'line': line_no0 + 1,
            'record_type': src_parts[0],
            'speaker_or_slot': src_parts[1] if len(src_parts) > 1 else '',
            'match_status': 'EXACT',
            'translation_status': status,
            'source_en': src_parts[src_idx],
            'translation_vi': vi,
        })
        if len(src_parts) != len(out_parts):
            qa['blockers'].append({'type': 'FIELD_COUNT_MISMATCH', 'line': line_no0 + 1, 'src_fields': len(src_parts), 'out_fields': len(out_parts)})
        if src_line.count(',') != out_lines[line_no0].count(','):
            qa['blockers'].append({'type': 'DELIMITER_COUNT_MISMATCH', 'line': line_no0 + 1})
        if technical_signature(src_line) != technical_signature(out_lines[line_no0]):
            qa['blockers'].append({'type': 'TECHNICAL_FIELD_CHANGED', 'line': line_no0 + 1})
        if tags(src_parts[src_idx]) != tags(out_parts[out_idx]):
            qa['blockers'].append({'type': 'TAG_MISMATCH', 'line': line_no0 + 1, 'src': tags(src_parts[src_idx]), 'out': tags(out_parts[out_idx])})
        if placeholders(src_parts[src_idx]) != placeholders(out_parts[out_idx]):
            qa['blockers'].append({'type': 'PLACEHOLDER_MISMATCH', 'line': line_no0 + 1, 'src': placeholders(src_parts[src_idx]), 'out': placeholders(out_parts[out_idx])})

    out_text = sep.join(out_lines) + (sep if final_nl else '')
    out_bytes_no_bom = out_text.encode('utf-8')
    out_bytes = (b'\xef\xbb\xbf' if bom else b'') + out_bytes_no_bom
    VI_ASSET.write_bytes(out_bytes)

    # Post-write full structural QA.
    new_bytes, new_text, new_lines, out_bom, out_newline, _, out_final = read_source(VI_ASSET)
    if len(src_lines) != len(new_lines):
        qa['blockers'].append({'type': 'LINE_COUNT_MISMATCH', 'src': len(src_lines), 'out': len(new_lines)})
    if bom != out_bom:
        qa['blockers'].append({'type': 'BOM_MISMATCH', 'src': bom, 'out': out_bom})
    if newline != out_newline:
        qa['blockers'].append({'type': 'NEWLINE_MISMATCH', 'src': newline, 'out': out_newline})

    unchanged_text_records = []
    for e in entries:
        vi = e['translation_vi']
        if vi == e['source_en']:
            unchanged_text_records.append({'line': e['line'], 'text': vi, 'reason': 'unchanged_translatable_field'})
    if unchanged_text_records:
        qa['blockers'].append({'type': 'UNCHANGED_EN_TEXT_FIELD', 'items': unchanged_text_records})
    else:
        qa['notes'].append('No translatable field was left identical to its EN asset source; proper names/technical placeholders only remain where required.')

    qa['counts'] = {
        'source_lines': len(src_lines),
        'output_lines': len(new_lines),
        'candidate_records': len(candidates),
        'translated_records': len(entries),
        'title_records': sum(1 for _, l in candidates if l.startswith('title,')),
        'message_records': sum(1 for _, l in candidates if l.startswith('message,')),
        'messageTextUnder_records': sum(1 for _, l in candidates if l.startswith('messageTextUnder,')),
        'messageTextCenter_records': sum(1 for _, l in candidates if l.startswith('messageTextCenter,')),
        'blocker_count': len(qa['blockers']),
    }
    qa['qa_status'] = 'PASS' if not qa['blockers'] else 'FAIL'

    focused = ['# Focused Diff: evs_10200020301', '']
    for e in entries:
        src = e['source_en']
        vi = e['translation_vi']
        focused.append(f"## Line {e['line']} ({e['record_type']})")
        focused.append('```diff')
        for dl in difflib.unified_diff([src], [vi], fromfile='EN asset field', tofile='VI field', lineterm=''):
            focused.append(dl)
        focused.append('```')
        focused.append('')
    DIFF.write_text('\n'.join(focused), encoding='utf-8')

    manifest = {
        'scene': SCENE,
        'timestamp_utc': qa['timestamp_utc'],
        'source_files': {
            'en_asset': {'path': str(EN_ASSET), 'bytes': len(src_bytes), 'sha256': sha256_bytes(src_bytes), 'bom_utf8': bom, 'newline': newline, 'line_count': len(src_lines)},
            'ja_json': {'path': str(JA_JSON), 'bytes': len(ja_bytes), 'sha256': sha256_bytes(ja_bytes)},
            'en_json': {'path': str(EN_JSON), 'bytes': len(en_json_bytes), 'sha256': sha256_bytes(en_json_bytes)},
        },
        'output': {'path': str(VI_ASSET), 'bytes': len(new_bytes), 'sha256': sha256_bytes(new_bytes), 'bom_utf8': out_bom, 'newline': out_newline, 'line_count': len(new_lines)},
        'work_artifacts': {'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'script': str(Path(__file__))},
        'counts': qa['counts'],
        'entries': entries,
        'qa_status': qa['qa_status'],
    }

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps({'qa_status': qa['qa_status'], 'counts': qa['counts'], 'output_sha256': manifest['output']['sha256'], 'artifacts': manifest['work_artifacts']}, ensure_ascii=False, indent=2))
    if qa['blockers']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
