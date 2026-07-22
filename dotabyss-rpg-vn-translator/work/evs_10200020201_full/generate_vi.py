# -*- coding: utf-8 -*-
"""Generate Vietnamese asset translation for evs_10200020201 with structural QA."""
from __future__ import annotations
import hashlib, json, re, difflib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'evs_10200020201'
JA = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/evs_10200020201_full'
MANIFEST = WORK/'manifest.json'
QA_LOG = WORK/'qa_log.json'
DIFF = WORK/'focused_diff.md'

TRANSLATIONS = [
"Tiêu Đề",
"（Bọn mình đã nhanh chóng hạ được lũ quái nên ngăn được thiệt hại‚<br>nhưng lại để tên trộm cướp viên tinh thể tẩu thoát mất rồi…）<br> ",
"…Đúng là một thất bại. Để một thứ nguy hiểm như thế bị đánh cắp…<br> ",
"Xin lỗi‚ Chỉ Huy… là do tôi đã mất cảnh giác. Lần thất bại thế này chắc cũng<br>mấy trăm năm rồi. Có lẽ tôi phải dành ít nhất 10 năm để tổng kết lại điểm cần rút kinh nghiệm…<br> ",
"Cô tự kiểm điểm quá đà rồi! Shiraes đã làm rất tốt mà!<br>Nhờ cô nên không có thương vong về người. Anh phải cảm ơn cô mới đúng.<br> ",
"Chỉ Huy… cậu đúng là đứa trẻ ngoan quá! Tôi sẽ chịu trách nhiệm tìm ra<br>tên trộm đó. Chắc không đến trăm năm đâu‚ cứ yên tâm!<br> ",
"Tuổi thọ của anh hết trước mất! Cô biết trong khoảng thời gian đó<br>viên tinh thể kia có thể gây ra bao nhiêu nguy hiểm không hả!<br> ",
"Có vẻ Adelheid có cách gì đó.<br>Trước hết cứ đợi cô ấy… à‚ vừa quay lại kìa.<br> ",
"Xin lỗi đã để mọi người đợi… Fufu. Lần nào Chỉ Huy cũng mang tới<br>những vụ thật kích thích nhỉ. Lần này tôi cũng phấn khích lắm. À‚ thuần túy là trí tuệ thôi‚ không phải tình dục――<br> ",
"Không ai nghĩ chuyện đó hết! Trời ạ‚ cô vẫn như mọi khi nhỉ.<br>Vậy‚ có cách giải quyết không?<br> ",
"Vâng. Có hơi vất vả một chút‚ nhưng tôi đã thành công bắt được<br>dạng sóng của viên tinh thể đang gây vấn đề.<br> ",
"Dạng sóng? Ý cô là thứ gì vậy?<br> ",
"Mỗi viên tinh thể đều phát ra một loại sóng năng lượng riêng biệt.<br>Bằng cách phân tích dữ liệu quan trắc đó‚ tôi đã xác định được vị trí đại khái hiện tại.<br> ",
"Tốt lắm‚ làm giỏi lắm‚ Adelheid! Quả nhiên em đúng là đáng tin cậy!<br> ",
"Cô làm được chuyện đó sao. Thật đáng kinh ngạc‚ xem ra vẫn còn nhiều điều tôi chưa biết.<br>Ngoan nào… trí tuệ ấy xứng đáng được khen ngợi.<br> ",
"…Ồồồ. Ra vậy‚ chuyện này thật tuyệt vời.<br>Chỉ số hạnh phúc của tôi đang tăng vọt. Đây chính là cái gọi là tình mẫu tính bao bọc nhỉ.<br> ",
"Dục vọng nguyên sơ được thỏa mãn khi phó thác bản thân cho một tồn tại tràn đầy mẫu tính….<br>Tôi có cảm giác muốn cứ thế buông mình theo khoái cảm và giải phóng tất cả.<br> ",
"Ừm ừm. Đừng khách sáo‚ cứ giao cả thân lẫn tâm cho tôi cũng được.<br>Con người chăm chỉ quá nên dễ tích tụ mệt mỏi. Cứ tha hồ làm nũng đi.<br> ",
"Aư… babư‚ mama…<br> ",
"Không được‚ Adelheid‚ tỉnh lại đi!<br>Bộ não quý giá của em đã tụt hẳn về cấp độ trẻ sơ sinh rồi đấy!<br> ",
"Hả…! N-nhưng hiệu ứng hạnh phúc này‚ khoa học hiện đại tuyệt đối không thể tái hiện.<br>Tôi muốn thu thập dữ liệu nên… thêm một chút nữa‚ làm ơn.<br> ",
"Tất nhiên rồi. Như thế này được chứ?<br> ",
"Babư… abư… aah‚ thật sự‚ rất tuyệt. Để có thêm tri thức‚<br>xin hãy xoa đầu‚ ôm chặt‚ và chà chà nhiều hơn nữa.<br> ",
"Chờ đã‚ chà chà là cô định bắt người ta làm gì hả!?<br> ",
"Cụ thể là chỗ――<br> ",
"Không‚ nghĩ lại thì đừng nói nữa!<br>H-hơn nữa‚ chuyện quan trọng là viên tinh thể đang ở đâu!?<br> ",
"À‚ chuyện đó… sau khi đối chiếu tọa độ với bản đồ‚<br>có vẻ viên tinh thể đang ở một địa điểm thuộc Hourai gọi là 『Oni Island』.<br> ",
"Hourai… là nước thành viên của Liên Hợp Thiên Quốc‚ nơi phồn thịnh với văn hóa kiểu Nhật.<br>Nhưng anh chưa từng nghe tới Oni Island đấy? Nó nổi ngoài biển à?<br> ",
"Không‚ Oni Island là nơi cư trú của tộc oni.<br>Tuy gọi là đảo‚ nhưng hình như vẫn nối liền với đất liền.<br> ",
"Tộc oni… thú vị thật. Họ khác với quái vật sao?<br> ",
"Tộc oni là chủng tộc có đặc trưng là sừng sắc nhọn và sức mạnh bẩm sinh.<br>Họ khác với loại quái vật được gọi là “oni”‚ nhưng đặc điểm ngoại hình thì khá giống.<br> ",
"Vì vậy tộc oni thường bị nhầm lẫn với quái vật “oni”<br>và bị khiếp sợ. Thực tế cũng có nhiều ghi chép rằng họ nóng tính.<br> ",
"Không rõ nguyên do‚ nhưng họ dần giữ khoảng cách với con người rồi chuyển tới<br>một nơi hẻo lánh hơn ở Hourai và lập nên làng của mình. Đó chính là hòn đảo cô lập trên đất liền――Oni Island.<br> ",
"Làng của tộc oni à… sao viên tinh thể lại ở một nơi như thế?<br>Nếu tộc oni mua lại từ tên trộm thì diễn biến nhanh quá…<br> ",
"Tên trộm đang lẩn trốn ở đó sao… không‚ nghĩ mãi cũng chẳng ích gì.<br>Tóm lại‚ ta cứ đến hiện trường thôi. Shiraes‚ cô đi cùng được không?<br> ",
"Tất nhiên rồi. Hãy để tôi chuộc lại thất bại.<br>Hơn nữa‚ tôi cũng có hứng thú cá nhân với Oni Island.<br> ",
"Hứng thú…? Cô có kỷ niệm gì với Oni Island à?<br> ",
"Ừ. Đó là 200 năm… hay 400 năm trước nhỉ? Không‚ 500… khoan đã‚<br>chắc là trước trận mưa sao băng 600 năm mới có một lần‚ nếu lấy đó làm mốc thì…<br> ",
"Quy mô cảm giác thời gian của cô vẫn khủng khiếp như mọi khi nhỉ….<br>Th-thôi‚ chuyện xảy ra lúc nào không quan trọng đâu‚ nhé?<br> ",
"Ừm‚ vậy sao? Thế thì là chuyện cách đây không lâu lắm.<br>Tôi từng muốn thân thiết với tộc oni nên đã định đi tới Oni Island.<br> ",
"Nhưng bạn bè quanh tôi phản đối vì nguy hiểm nên tôi đã từ bỏ.<br>Tuy có hiểu biết nhất định‚ nhưng làm người dẫn đường thì hơi khó đấy.<br> ",
"Dù vậy‚ chỉ cần Shiraes đi cùng là đã mạnh gấp trăm lần rồi.<br>Nhưng… chỉ đi thôi mà cũng bị phản đối‚ tộc oni đáng sợ đến thế sao.<br> ",
"Chỉ hai người đi thì hơi nguy hiểm đấy.<br>Giá mà có một cô bé am hiểu về tộc oni thì tốt‚ nhưng chuyện tiện lợi như vậy thì…<br> ",
"…………Không‚ có đấy.<br>Một người chắc chắn am hiểu tộc oni――<br> ",
"Chị Kureha ơi‚ nhìn này nhìn này~. Em làm vương miện bằng hoa đó~.<br> ",
"Ôi‚ đẹp quá còn gì. Rất hợp với em đấy.<br>Fufu. Trông cứ như cô dâu vậy.<br> ",
"Waai‚ cô dâu nè~!<br>Chị Kureha cũng sẽ làm cô dâu của ai đó hả?<br> ",
"Ừ‚ chị có một phu quân yêu chị và chị cũng yêu ngài ấy tha thiết.<br>Ở chỗ làm bọn chị lén âu yếm nhau‚ còn đút cơm a~ cho nhau ăn nữa…<br> ",
"Waa…! Hai người thân nhau ghê! Em muốn thấy chị Kureha lúc làm cô dâu quá~!<br> ",
"Fufu‚ cảm ơn em. Nhất định hãy đến dự lễ cưới nhé♪<br> ",
"C-cô ta… đến cả đứa trẻ như thế cũng bị nhồi chuyện sẽ kết hôn với anh sao!?<br>Dù đó chỉ là chuyện hồi nhỏ mà cô ta đang hoàn toàn bao vây anh từ mọi phía…!<br> ",
"Lén âu yếm? Đút a~…?<br>Ch-Chỉ Huy? Cậu có một phụ nữ thân thiết đến mức đó sao?<br> ",
"Hiểu lầm! Nhầm rồi! Vu oan đấy!<br>Kureha chỉ phóng đại lên thôi‚ chẳng có chuyện gì to tát cả!<br> ",
"V-vậy à. Ừ‚ tôi hiểu rồi.<br>Dù sao thì‚ chúc mừng kết hôn nhé‚ Chỉ Huy.<br> ",
"Anh còn chẳng nhớ mình đã đính hôn!<br>Chuyện kết hôn này nọ toàn là cô ấy tự nói thôi!<br> ",
"Ồ. Tôi biết rồi‚ hình như… gọi là vợ tự tìm đến nhà nhỉ.<br>Văn hóa loài người đúng là sâu sắc và thú vị thật.<br> ",
"Với anh thì đây đâu phải lúc để vui vẻ!<br>Kureha từng nói cô ấy đến căn cứ tiền tuyến để kết hôn với anh‚ lẽ nào nghiêm túc thật sao…?<br> ",
"Nhưng Kureha cũng đã hòa nhập với căn cứ tiền tuyến nhiều rồi nhỉ.<br>Lúc mới đến‚ mọi người từng sợ cô ấy vì là tộc oni mà.<br> ",
"Vậy sao? Nhìn cô ấy thì tôi cảm thấy lời đồn tộc oni nóng tính<br>có lẽ là hiểu lầm…<br> ",
"Chà‚ tạm gác chân tướng sang một bên‚ có cô ấy là tộc oni đi cùng thì chuyến tới Hourai sẽ yên tâm hơn.<br>Nếu nhờ cô ấy làm trung gian‚ chắc cũng dễ tạo cơ hội giao lưu với tộc oni hơn.<br> ",
"Đúng vậy. Ta đi nhờ cô ấy hợp tác ngay thôi.<br> ",
"Anh muốn em cùng đi tới Oni Island… ạ?<br>Ra vậy… đến Oni Island… cùng với phu quân…<br> ",
"（…………? Sao vậy‚ tưởng cô ấy ngạc nhiên‚ vậy mà đột nhiên run lên?<br>Hay là có lý do gì khiến cô ấy không muốn tới Oni Island…?）<br> ",
"Phu quân… chuyện đó là thật sao ạ…?<br> ",
"Ừ‚ đúng vậy… xin lỗi‚ anh chưa hỏi gì về hoàn cảnh của em cả.<br>Nếu em có lý do không muốn tới Oni Island thì anh sẽ không ép――<br> ",
"<size=48>――Cuối cùng ngài cũng hạ quyết tâm rồi nhỉ‚ phu quân!!</>",
"…C-cái gì!?<br> ",
"Oni Island là quê hương của em!<br>Nghĩa là ngài sẽ cùng em về quê để ra mắt xin cưới đúng không ạ! Đúng không!<br> ",
"B-bình tĩnh đã‚ Kureha! Anh không có ý đó!<br>Anh đã kể tình hình lúc nãy rồi mà!? Vì có viên tinh thể nguy hiểm nên ta đến thu hồi nó!<br> ",
"Anh nhờ em đi cùng vì nếu em làm trung gian với tộc oni thì sẽ rất yên tâm!<br>Em không nghe sao!?<br> ",
"Fufu‚ phu quân lại nữa rồi~♡<br>Kureha biết hết mà‚ ngài chỉ viện cớ khác vì đang xấu hổ thôi♪<br> ",
"Đúng vậy! Hiếm có dịp này‚ chúng ta hãy tổ chức một hôn lễ thật long trọng ở Oni Island đi!<br>Trong lời chúc phúc của mọi người‚ hai ta sẽ trao nhau nụ hôn thề nguyện… kya～～～～～♡<br> ",
"Nghe anh nói điiiii! Với lại‚ nếu đi ra mắt chuyện cưới xin‚<br>thì Shiraes ở đây là lạ lắm đúng không!<br> ",
"Cô Shiraes…? Là người đang làm cố vấn cho các binh sĩ đúng không ạ.<br>Tại sao vị này lại… hả!<br> ",
"Lẽ nào… cô định chen vào con đường lễ đường của em và phu quân…?<br>Và rồi cướp chú rể… nếu là vậy thì‚ dù có là cô Shiraes đi nữa…!<br> ",
"Ảo tưởng đang tiến triển với tốc độ khủng khiếp…!!<br> ",
"Ồồồ… trí tưởng tượng thật đáng nể. Từ con người đến tộc oni‚<br>tiềm lực của các cậu luôn khiến tôi kinh ngạc tận đáy lòng. Tôi càng hứng thú với tộc oni rồi đấy.<br> ",
"Đây là lúc để cảm thán hả!<br>Nếu không mau giải hiểu lầm thì câu chuyện chẳng tiến triển được đâu!<br> ",
"Quả thật là vậy. E hèm… Kureha‚ mong em đừng hiểu lầm.<br>Tôi… là bà mối của hai người.<br> ",
"Ừm ừm‚ đúng đúng. Shiraes là… gì của bọn anh cơ?<br> ",
"Tôi rất yêu quý con người mà. Được tham dự sân khấu trọng đại như thế<br>là vinh dự tột cùng. Xin hãy để tôi chứng kiến lễ cưới của Chỉ Huy và em.<br> ",
"Cô Shiraes… cô chúc phúc cho em và phu quân đến mức đó…!<br>Em cảm động lắm! Nhất định em sẽ hạnh phúc!<br> ",
"Khụ‚ câu chuyện càng lúc càng rắc rối hơn…!<br>Cô định làm gì vậy‚ Shiraes!?<br> ",
"Lúc này hóa giải cảnh giác của cô bé với tôi là quan trọng nhất đúng không?<br>Hơn nữa‚ tôi vẫn nghĩ gắn kết tình duyên cho người trẻ là bổn phận của bậc trưởng bối.<br> ",
"Đúng là vậy nhưng… dù thế thì cô cần gì phải nói dối kiểu đó?<br>Kureha‚ đừng tin nguyên xi lời Shiraes nói………… Kureha?<br> ",
"Ư～～m. Shiromuku cũng đẹp‚ nhưng mình cũng muốn thử váy cưới nữa~.<br>Ư～～～m‚ phân vân quá đi!<br> ",
"（Cô ấy hoàn toàn chìm vào thế giới riêng rồi…!<br>Chết tiệt‚ đã vậy thì! Chỉ còn cách nắm chỗ đó thôi!）<br> ",
"Funyuaaa～～～…! S-sừng‚ sừng thì không được đâuuu～～～…!<br> ",
"Quả nhiên sừng là điểm yếu… nghe này Kureha‚ chuyện này cấp bách lắm.<br>Ta không có thời gian chơi đâu‚ nên đừng có bạo phát quá nhé?<br> ",
"V-vânggg~…<br> ",
"Ồ? Có vẻ sừng của tộc oni rất nhạy cảm. Thật sự thú vị.<br>Lần sau tôi cũng được chạm thử chứ…?<br> ",
"Tùy cô… dù sao thì có Kureha hợp tác là đáng mừng rồi.<br>Nghe nói trong tộc oni cũng có nhiều người nóng tính. Anh muốn tránh va chạm không cần thiết.<br> ",
"Ôi‚ phu quân. Tộc oni là một dân tộc hiền hậu đấy ạ.<br>Tổ tiên tộc oni xây dựng Oni Island và chuyển đến đó cũng là vì nghĩ cho con người.<br> ",
"Thật ra họ muốn thân thiết với con người‚ nhưng giữa tộc oni và con người cũng có nhiều khác biệt….<br>Vì vậy họ giữ khoảng cách để không làm người khác sợ. Đó là lịch sử của tộc oni.<br> ",
"Vậy sao? Khác khá nhiều so với chuyện anh nghe từ Shiraes đấy.<br> ",
"Dù sao tôi cũng chỉ biết về tộc oni và Oni Island qua lời truyền miệng và sách vở thôi.<br>Nếu sự thật khác với lời đồn‚ tôi lại càng muốn gặp tộc oni hơn.<br> ",
"Vâng‚ xin hãy thử nói chuyện với đồng tộc của em.<br>Em chắc phu quân và cô Shiraes cũng sẽ thân thiết với họ thôi♪<br> ",
"Ra vậy‚ anh sẽ trông đợi.<br>Vậy thì khi chuẩn bị xong‚ chúng ta lên đường tới Oni Island thôi.<br> ",
"<size=48>――Vài Ngày Sau</size>",
"Đây là Oni Island à.<br>Lần trước đến Hourai‚ anh chưa từng tới tận vùng này.<br> ",
"Ồồồ… cuối cùng tôi cũng có thể đến đây. Thật xúc động vô cùng.<br>Hòn đảo nơi tộc oni hiền hậu sinh sống… ừm‚ tôi mong chờ lắm.<br> ",
"Khung cảnh quê hương‚ làn gió quê hương… thật hoài niệm.<br>Để em dẫn mọi người tới làng ngay――<br> ",
"…Chờ đã‚ Kureha‚ Chỉ Huy.<br>Chúng ta bị bao vây rồi.<br> ",
"Cái gì…!?<br> ",
"――Hảảảảảảảảảảảả? Lũ chúng mày là ai hảaaaaaaa!!?<br> ",
"Bọn bay tới đây làm cái quái gì thế hả!? Hảảảảảảảả!!?<br> ",
"Không hề‚ tộc oni chẳng hiền hậu chút nào！！！！<br> ",
]

TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r'%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrtt]')
JP_CHAR_RE = re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
ASCII_WORD_RE = re.compile(r'[A-Za-z]{3,}')
ALLOWED_ASCII = {'hourai','oni','island','shiraes','adelheid','kureha','shiromuku','funyuaaa','fufu','babư','mama','chara','size'}

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def detect_newline(text: str) -> str:
    return 'CRLF' if '\r\n' in text else 'LF'

def split_lines_preserve(text: str):
    return text.splitlines(keepends=True)

def line_body_ending(line: str):
    if line.endswith('\r\n'): return line[:-2], '\r\n'
    if line.endswith('\n'): return line[:-1], '\n'
    return line, ''

def parse_record(line_body: str):
    if line_body.startswith('title,'):
        return 'title', line_body.split(',', 1)
    if line_body.startswith('message,'):
        return 'message', line_body.split(',', 5)
    if line_body.startswith('messageTextUnder,'):
        return 'messageTextUnder', line_body.split(',', 5)
    if line_body.startswith('messageTextCenter,'):
        return 'messageTextCenter', line_body.split(',', 5)
    return None, None

def text_field_index(kind: str):
    return {'title':1,'message':2,'messageTextUnder':2,'messageTextCenter':2}[kind]

def command_count(lines):
    counts = {'title':0,'message':0,'messageTextUnder':0,'messageTextCenter':0}
    candidates=[]
    for idx,line in enumerate(lines,1):
        body,_=line_body_ending(line)
        kind,parts=parse_record(body)
        if kind in counts:
            counts[kind]+=1
            candidates.append((idx,kind,parts))
    return counts,candidates

def tech_signature(kind, parts):
    if kind == 'title': return [parts[0]]
    return [parts[0], parts[1]] + parts[3:]

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    vi_dir = VI_ASSET.parent
    vi_dir.mkdir(parents=True, exist_ok=True)
    src_bytes = EN_ASSET.read_bytes()
    bom = src_bytes.startswith(b'\xef\xbb\xbf')
    enc = 'utf-8-sig' if bom else 'utf-8'
    src_text = src_bytes.decode(enc)
    newline = '\r\n' if detect_newline(src_text) == 'CRLF' else '\n'
    src_lines = split_lines_preserve(src_text)
    counts, candidates = command_count(src_lines)
    blockers=[]; items=[]; notes=[]; entries=[]
    if len(TRANSLATIONS) != len(candidates):
        blockers.append({'code':'TRANSLATION_COUNT_MISMATCH','expected':len(candidates),'actual':len(TRANSLATIONS)})
    for i,t in enumerate(TRANSLATIONS):
        if ',' in t:
            blockers.append({'code':'ASCII_COMMA_IN_VI','record_index':i+1,'text':t})
    out_lines = list(src_lines)
    for i,(line_no,kind,parts) in enumerate(candidates):
        if i >= len(TRANSLATIONS): break
        field_idx = text_field_index(kind)
        old_parts = list(parts)
        new_parts = list(parts)
        new_parts[field_idx] = TRANSLATIONS[i]
        new_body = ','.join(new_parts)
        body,end = line_body_ending(src_lines[line_no-1])
        out_lines[line_no-1] = new_body + end
        old_text = old_parts[field_idx]
        vi_text = TRANSLATIONS[i]
        status = 'TRANSLATED'
        if old_text == vi_text:
            status = 'UNCHANGED'
            items.append({'line':line_no,'code':'UNCHANGED_TEXT_FIELD','severity':'major','source':old_text,'translation':vi_text,'status':'review'})
        if TAG_RE.findall(old_text) != TAG_RE.findall(vi_text):
            blockers.append({'line':line_no,'code':'TAG_MISMATCH','source_tags':TAG_RE.findall(old_text),'vi_tags':TAG_RE.findall(vi_text)})
        if PLACEHOLDER_RE.findall(old_text) != PLACEHOLDER_RE.findall(vi_text):
            blockers.append({'line':line_no,'code':'PLACEHOLDER_MISMATCH','source_placeholders':PLACEHOLDER_RE.findall(old_text),'vi_placeholders':PLACEHOLDER_RE.findall(vi_text)})
        # kept English scan: only flag source EN alphabetic tokens that remain in VI,
        # excluding approved proper names/onomatopoeia. This avoids false positives for
        # Vietnamese words without diacritics such as "anh", "nhanh", "trong".
        src_tokens = {tok.lower() for tok in ASCII_WORD_RE.findall(old_text)}
        vi_tokens = {tok.lower() for tok in ASCII_WORD_RE.findall(vi_text)}
        kept = sorted((src_tokens & vi_tokens) - ALLOWED_ASCII)
        if kept:
            items.append({'line':line_no,'code':'POSSIBLE_KEPT_EN_TOKEN','severity':'major','tokens':kept,'source':old_text,'translation':vi_text,'status':'review'})
        banned_suffixes = [tok for tok in ('-kun', '-sama', '-san') if tok in vi_text.lower()]
        if banned_suffixes:
            blockers.append({'line':line_no,'code':'JAPANESE_SUFFIX_LEFT_IN_VI','tokens':banned_suffixes,'translation':vi_text})
        if JP_CHAR_RE.search(vi_text):
            # allow Japanese technical-style title marks? log all for review.
            items.append({'line':line_no,'code':'JP_CHAR_IN_VI','severity':'minor','text':vi_text,'status':'logged'})
        entries.append({'record_index':i+1,'line':line_no,'kind':kind,'speaker':parts[1] if len(parts)>1 else None,'source_text':old_text,'vi_text':vi_text,'match_status':'EXACT_ORDERED','translation_status':status})
    out_text = ''.join(out_lines)
    out_bytes = out_text.encode(enc)
    # structural QA
    out_counts, out_candidates = command_count(out_lines)
    if len(out_lines) != len(src_lines): blockers.append({'code':'LINE_COUNT_MISMATCH','source':len(src_lines),'output':len(out_lines)})
    if counts != out_counts: blockers.append({'code':'COMMAND_COUNT_MISMATCH','source':counts,'output':out_counts})
    delimiter_mismatches=[]; tech_mismatches=[]
    for idx,(sline,oline) in enumerate(zip(src_lines,out_lines),1):
        sb,_=line_body_ending(sline); ob,_=line_body_ending(oline)
        if sb.count(',') != ob.count(','):
            delimiter_mismatches.append({'line':idx,'source_commas':sb.count(','),'output_commas':ob.count(',')})
        sk,sp=parse_record(sb); ok,op=parse_record(ob)
        if sk in ('title','message','messageTextUnder','messageTextCenter'):
            if sk != ok or tech_signature(sk,sp) != tech_signature(ok,op):
                tech_mismatches.append({'line':idx,'source_signature':tech_signature(sk,sp),'output_signature':tech_signature(ok,op) if ok else None})
    if delimiter_mismatches: blockers.append({'code':'DELIMITER_MISMATCH','items':delimiter_mismatches[:20],'count':len(delimiter_mismatches)})
    if tech_mismatches: blockers.append({'code':'TECH_FIELD_MISMATCH','items':tech_mismatches[:20],'count':len(tech_mismatches)})
    # newline preservation
    if detect_newline(out_text) != detect_newline(src_text): blockers.append({'code':'NEWLINE_STYLE_MISMATCH','source':detect_newline(src_text),'output':detect_newline(out_text)})
    # parse JSON ordered counts
    ja_pairs = json.loads(JA.read_text(encoding='utf-8'), object_pairs_hook=list)
    en_pairs = json.loads(EN_JSON.read_text(encoding='utf-8'), object_pairs_hook=list)
    if len(ja_pairs) != len(en_pairs):
        items.append({'code':'NOVEL_PAIR_COUNT_MISMATCH','severity':'major','ja_count':len(ja_pairs),'en_count':len(en_pairs),'status':'logged'})
    VI_ASSET.write_bytes(out_bytes)
    focused=[]
    focused.append(f'# Focused Diff: {SCENE}\n')
    for entry in entries:
        line=entry['line']; src=src_lines[line-1].rstrip('\r\n'); out=out_lines[line-1].rstrip('\r\n')
        if src != out:
            focused.append(f'## Line {line} / {entry["kind"]}\n')
            focused.extend(difflib.unified_diff([src+'\n'], [out+'\n'], fromfile='en', tofile='vi', lineterm=''))
            focused.append('\n')
    DIFF.write_text('\n'.join(focused), encoding='utf-8')
    manifest={
        'scene':SCENE,
        'generated_at':datetime.now(timezone.utc).isoformat(),
        'paths':{'ja_json':str(JA),'en_json':str(EN_JSON),'en_asset':str(EN_ASSET),'vi_asset':str(VI_ASSET),'work_dir':str(WORK),'focused_diff':str(DIFF),'qa_log':str(QA_LOG)},
        'source':{'sha256':sha256_bytes(src_bytes),'bytes':len(src_bytes),'bom':bom,'encoding':enc,'newline':detect_newline(src_text),'line_count':len(src_lines),'command_counts':counts,'candidate_count':len(candidates)},
        'novel':{'ja_pair_count':len(ja_pairs),'en_pair_count':len(en_pairs)},
        'output':{'sha256':sha256_bytes(out_bytes),'bytes':len(out_bytes),'line_count':len(out_lines),'command_counts':out_counts,'candidate_count':len(out_candidates)},
        'entries':entries,
        'qa_status':'PASS' if not blockers else 'FAIL',
        'blocker_count':len(blockers),
        'item_count':len(items),
        'notes':notes + ['JP primary translated with EN asset ordered alignment; all characters treated as confirmed 18+ per task context.', 'ASCII comma forbidden inside VI text fields; Vietnamese pauses use U+201A where needed.']
    }
    qa={'scene':SCENE,'qa_status':manifest['qa_status'],'blockers':blockers,'items':items,'summary':{'source_lines':len(src_lines),'output_lines':len(out_lines),'translated_records':sum(1 for e in entries if e['translation_status']=='TRANSLATED'),'unchanged_records':sum(1 for e in entries if e['translation_status']=='UNCHANGED'),'delimiter_mismatches':len(delimiter_mismatches),'tech_mismatches':len(tech_mismatches),'command_counts':out_counts}}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'qa_status':manifest['qa_status'],'blockers':len(blockers),'items':len(items),'source_sha256':manifest['source']['sha256'],'output_sha256':manifest['output']['sha256'],'translated_records':qa['summary']['translated_records'],'candidate_count':len(candidates),'paths':manifest['paths']}, ensure_ascii=False, indent=2))
    if blockers:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
