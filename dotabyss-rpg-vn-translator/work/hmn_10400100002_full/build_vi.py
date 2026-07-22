#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI for hmn_10400100002 from EN asset (EN-asset-is-English, title-still-JP).

Field-index replacement: keep all technical fields (parts[3:]) and tags byte-identical,
auto-mirror the trailing tag suffix of each source text field, fix the EN typo
"Commaander" -> "Chỉ Huy", and write BOM + CRLF exactly like the source.
"""
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10400100002.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10400100002.txt"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAG_RE = re.compile(r"<[^>]+>")
SUFFIX_RE = re.compile(r"(?:<[^>]+>\s*)+$")  # trailing tags incl. trailing space

# VI prose (WITHOUT trailing tag suffix). size30 lines exclude <size=30> wrapper.
VI = {
    1: "Lần Sau Sẽ Không Thua Đâu!",  # title (JP: 次は負けないから！)
    2: "Hừm... chỗ này có vẻ ổn để bày một trận phòng ngự quy mô lớn. Phải chuẩn bị<br>một kế hoạch để nhử quái vật.",
    3: "(Hư hư hư‚ Chỉ Huy đang chìm trong suy nghĩ. Giờ anh ấy hoàn toàn mất cảnh giác rồi!)",  # size30
    4: "(Lần trước em có thua Chỉ Huy một lần ở Căn Cứ Tiền Tuyến‚ nhưng em sẽ trở thành võ sư số một thế giới‚ nên tuyệt đối không được thua lần nữa!)",  # size30
    5: "Thời tiết đẹp thế này làm anh hơi buồn ngủ... Phùa...",
    6: "(Tuyệt! Chỉ Huy hoàn toàn mất cảnh giác rồi! Lúc này!)",  # size30
    7: "(Nhanh hơn‚ mạnh hơn... Một đòn quyết định!)",  # size30
    8: "Ủa! Bị tập kích à!",
    9: "Ăn miếng trả miếng! Xin lỗi vì đòn tập kích bất ngờ nhé! Têi!",
    10: "Luca lao về phía Chỉ Huy đang ngồi bệt xuống‚ định tung một<br>đòn tập kích bất ngờ.",
    11: "Hả!",
    12: "Nửa dưới cơ thể em ấy chìm gọn gàng xuống đất.",
    13: "C-cái gì thế này!?",
    14: "Ủa‚ ngạc nhiên thật — một nữ võ sĩ muốn trở thành số một thế giới lại đi<br>tập kích anh. May mà tình cờ có sẵn một cái hố bẫy.",
    15: "Hố bẫy đâu tự dưng mà xuất hiện! Này‚ khoan đã! Nó vừa vặn<br>với em thế này‚ em chẳng thể cựa quậy chút nào!",
    16: "Suýt soát như thể người hiểu em tường tận đã giăng sẵn rồi. Hahaha!",
    17: "Đòn đó gian lận đó‚ Chỉ Huy!",
    18: "Gian lận thì anh chấp luôn! Nào‚ lần này cũng nhận thua đi!",
    19: "Không đời nào! Nếu thua hai lần liên tiếp‚ mục tiêu Võ Sư Số Một Thế Giới<br>của em lại càng xa vời!",
    20: "Em sẽ không bao giờ đầu hàng — đừng có lạch lạch em! ưm! Ha... hahahaha!",
    21: "Nào‚ cái tinh thần chiến đấu lúc nãy đâu rồi?",
    22: "Em chịu hết nổi rồi! Em đầu hàng‚ em đầu hàng!",
    23: "Thú thật‚ đầu tiên em cứ nói vậy từ nãy tới giờ là được rồi.",
    24: "Ư... lần sau em sẽ không thua đâu! Và em nhất quyết không dính phải cái hố bẫy<br>như thế nữa!",
    25: "...Em vẫn chưa từ bỏ sao?",
    26: "Tất nhiên! Nói gì thì nói‚ chính vì anh là một đối thủ mạnh đến thế<br>nên em càng phấn chấn‚ Chỉ Huy!",
    27: "Ra thế... đúng là tinh thần đáng quý.",
    28: "Hứ! Em sẽ chẳng bao giờ phản bội giấc mơ của mình! Em sẽ vượt qua Chỉ Huy‚<br>trở thành người mạnh nhất ở Căn Cứ Tiền Tuyến‚ rồi sau đó là số một thế giới!",
    29: "Này‚ Chỉ Huy... em không thể tự bước ra được‚ anh kéo em lên được không?",
    30: "Chỗ này cây cỏ rậm rạp thật. Chúng ta có nên lắp một hệ thống giám sát<br>để phát hiện quái vật xuất hiện không?",
    31: "(Chỉ Huy đang tính toán chiến thuật... Anh ấy đứng yên bất động‚ nghiêm túc thế...)",  # size30
    32: "(Nếu tiếp cận từ bóng cây và đánh tập hậu‚ mình sẽ không dẫm phải hố bẫy...! Lần này em thắng chắc rồi‚ Chỉ Huy!)",  # size30
    33: "Được rồi‚ em bắt đầu đây!",
    34: "Hửm! Lại có kẻ xâm nhập à?",
    35: "Đòn tập kích thứ hai phá luật rồi! Chỉ Huy‚ hãy<br>sẵn sàng đi!",
    36: "Ta-a-a-a!",
    37: "Trong tích tắc‚ Luca áp sát sau lưng mục tiêu và vung một<br>nắm đấm bao bọc sấm sét. Cú đánh toàn lực nghiền nát thân thể đối phương.",
    38: "Em làm được rồi‚ em thắng... Hả‚ cái gì! Chỉ Huy bị đập nát bét rồi!",
    39: "Này này‚ đáng sợ thật đấy‚ Luca. Em định đập nát anh thành từng mảnh à?",
    40: "...! Phía sau em! Phùa!",
    41: "Một bàn tay túm lấy em ấy từ phía sau‚ và Luca vùng vẫy giãy giụa.",
    42: "Chỉ Huy! Sao lại thế? Anh không bị thổi bay thành mảnh sao?",
    43: "Anh mà bị sao! Anh không hề xước một tí nào‚ xem này!",
    44: "Hể... vậy em vừa hạ cái gì thế?",
    45: "Thứ em đập nát là một con bù nhìn mặc đồ của anh. Nó do Lux Nova<br>cung cấp‚ gắn máy ghi âm phát ra giọng nói y hệt anh.",
    46: "Không đời nào! Nó trông và nghe y hệt anh‚ thì em lấy gì mà<br>phân biệt được?",
    47: "Ư‚ em cứ tưởng mình thắng nhờ đập Chỉ Huy nát bét...",
    48: "Đập nát Chỉ Huy làm gì chứ! Em đâu cần dùng nhiều sức đến thế chỉ để hạ anh! Biết tiết chế<br>chút đi!",
    49: "Á‚ chà‚ cái máy ghi âm cũng vỡ nát luôn rồi. Mà nó đắt tiền thế cơ.",
    50: "Lại còn xài mấy món đồ hiếm nữa‚ gian lận quá! Thật sự<br>tiểu xảo đấy‚ Chỉ Huy!",
    51: "Anh tự hào vì mình xài tiểu xảo đấy! Nào‚ hôm nay nhận thua lần nữa đi‚<br>Luca!",
    52: "Hi ân! Đừng có chọc lưng em! Ahahahahaha!",
    53: "Nhưng em không chịu thua trước cái trò bẩn thỉu đó đâu!",
    54: "Anh thích cái tinh thần đó! Nhưng em có thắng nổi thủ pháp của anh không?",
    55: "Cái gì mà di chuyển ngón tay kỳ cục thế? Đừng có chơi đùa với người em! Phùa...<br>Ừm‚ Ahahahahaha!",
    56: "Nào‚ nào‚ nào.",
    57: "Hi a‚ ha an! Ahahaha! Em đầu hàng‚ em thua! Em bại rồi!",
    58: "Hahaha‚ coi như anh thắng ba trận liên tiếp rồi.",
    59: "Ư‚ em mới là người tập kích anh‚ sao anh lại giăng sẵn bù nhìn? Chuyện<br>đó kỳ quái quá đi!",
    60: "Đó chỉ là một phần sức mạnh của anh thôi. Em bực thì cứ thử mà thắng đi.",
    61: "Kư... tất nhiên rồi. Võ Sư Số Một Thế Giới không bao giờ thua<br>vì chuyện nhỏ nhặt thế này.",
    62: "Vậy‚ Chỉ Huy‚ anh bám chặt lấy em suốt từ nãy đến giờ... anh thả em ra<br>được chưa?",
    63: "Hừm... có lẽ anh sẽ tận hưởng thêm chút nữa.",
    64: "Đồ hèn! Đồ gian lận! Đồ biến thái! Chỉ Huy biến thái!",
    65: "Cái miệng này là miệng vừa chửi người thắng sao? Hả?",
    66: "Ừm‚ ừm‚ ừm! Thả em ra!",
    67: "*thở hắt*! *thở dốc*! *hi ách*!",
    68: "Đêm khuya trên sân tập. Một mình trong căn phòng tối‚<br>Luca ướt đẫm mồ hôi.",
    69: "*thở dốc*!",
    70: "Luca tung một cú móc nhảy toàn lực bao bọc sấm sét‚ mọi<br>thớ cơ bắp căng tràn. Sau cú chốt hạ‚ em ấy giữ nguyên thế đứng một lát.",
    71: "...Ừm‚ thế đứng của em cũng khá ổn đấy‚ chắc vậy. Nhưng... em chẳng thể hình dung<br>nó trúng được Chỉ Huy.",
    72: "Động tác của em chẳng quan trọng. Dù em có tung bao nhiêu cú đấm‚<br>em cũng chẳng với tới được anh ấy.",
    73: "Đúng là em chỉ tự tập một mình thôi‚ nhưng... em cá là Chỉ Huy đã<br>quan sát em cực kỳ sát sao.",
    74: "Lúc đầu — à‚ cú chốt hạ của em cần một chút thời gian vung tay‚ nên anh đã làm<br>vũng slime trơn tuột.",  # no trailing <br>
    75: "Cái hố bẫy vừa vặn nên em chẳng trèo lên nổi‚ và vì anh<br>không thể bắt người trên không trung‚ Chỉ Huy đã túm lấy em sau khi em đập vỡ bù nhìn.",  # no trailing <br>
    76: "Em thua không phải ngẫu nhiên‚ và anh ấy cũng chẳng hề gian lận. Chỉ Huy<br>thật sự đã nghĩ cho em và dốc toàn lực để đánh bại em.",
    77: "...anh ấy lúc nào cũng chỉ trêu chọc em‚ nên đời nào nói được những lời như thế.<br>Nhưng mà mặt đó của anh cũng bất công quá đi‚ Chỉ Huy.",
    78: "Cứ tiếp tục thế này‚ em sẽ chẳng bao giờ thắng nổi Chỉ Huy. Chỉ dùng sức mạnh<br>áp đảo anh ấy là không đủ.",
    79: "Em phải suy tính đường đường mạch lạc như Chỉ Huy...!",
    80: "C-Chỉ Huy! Có một bức thư khiêu chiến từ Luca gửi tới! Ý nghĩa<br>là sao đây?!",
    81: "Ồ? Con nhỏ đó biết dùng cái đầu rồi đấy‚ Luca ấy. Thế là em ấy tự chỉ định<br>thời gian và địa điểm à?",
    82: "...Ngài chẳng hề bất ngờ trước bức thư khiêu chiến‚ đúng không?",
    83: "Anh dây dưa với Luca một thời gian rồi. Em ấy muốn đánh bại anh để<br>trở thành Võ Sư Số Một Thế Giới.",
    84: "Cũng khá vui. Anh đã cho tổ lính ở căn cứ thu thập tin tình báo và thậm chí điều phối<br>thời điểm em ấy tập kích.",
    85: "...Ngạc nhiên thật. Em tưởng ngài sẽ thấy phiền phức<br>và chán nản cơ.",
    86: "Luca thẳng thắn về chuyện mạnh lên. Dù có thua<br>vì chiến thuật‚ em ấy cũng chẳng bướng bỉnh — em ấy quay lại với một biện pháp đối phó.",
    87: "Thấy em ấy tích cực và nghiêm túc thế này khiến anh cũng có động lực. Thôi‚<br>hôm nay anh đi chơi đùa với em ấy một chút vậy.",
    88: "Đừng có làm quá sức đấy‚ được không? Và cũng đừng để bị thương.",
    89: "Ừ‚ cứ giao cho anh. Hư hư hư‚ lần tới anh sẽ lừa em ấy thế nào đây?",
    90: "...Hả? K-khoan đã‚ Chỉ Huy! Chúng ta đang giữa giờ làm việc mà!",
    91: "Anh sẽ làm sau khi chơi đùa với Luca xong!",
    92: "Thật tình! Xin ngài hãy đổ nhiệt huyết đó vào công việc nữa!",
}

assert len(VI) == 92, len(VI)


def build_text_field(cmd: str, old_tf: str, rec: int) -> str:
    prose = VI[rec]
    if "<size=30>" in old_tf:
        return "<size=30>" + prose + "</size>"
    m = SUFFIX_RE.search(old_tf)
    suffix = m.group() if m else ""
    return prose + suffix


def main():
    raw = EN.read_bytes()
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = [l.rstrip("\r") for l in text.split("\n")]
    out_lines = []
    rec = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            rec += 1
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = VI[rec]
                out_lines.append(",".join(parts))
            else:
                parts = ln.split(",", 5)
                parts[2] = build_text_field("message", parts[2], rec)
                out_lines.append(",".join(parts))
        else:
            out_lines.append(ln)
    body = "\n".join(out_lines)
    if has_crlf:
        body = body.replace("\r\n", "\n").replace("\n", "\r\n")
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_PATH.write_bytes(b"\xef\xbb\xbf" + body.encode("utf-8"))
    print("WROTE", VI_PATH, "records applied:", rec)


if __name__ == "__main__":
    main()
