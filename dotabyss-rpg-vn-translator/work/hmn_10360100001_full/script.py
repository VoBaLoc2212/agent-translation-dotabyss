#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI output for hmn_10360100001 from EN asset (EN-asset-is-English case).

- title, field is JP -> translate JP->VI Title Case.
- message, fields are English -> translate EN->VI.
- Keeps speaker labels (field 1) byte-identical, %user% placeholder, BOM/CRLF,
  and EXACTLY mirrors each message field's trailing <br>  suffix.
- Uses U+201A (‚) for in-text commas; never ASCII ','.
"""
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100001.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100001.txt"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
SUFFIX_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# line_no -> VI text field content (WITHOUT the trailing <br>  suffix for message lines)
VI = {
    30: "Phó Quan Lime Của Lady Reyzeria",  # title (full replacement, no suffix)
    38: "Tại thao trường của Căn Cứ Tiền Tuyến‚ một cuộc huấn luyện<br>phối hợp giữa quân Milesgard và Eldorana đang được tổ chức.",
    115: "*hừ!* *hà!*",
    176: "Ngươi không thể hạ gục em bằng những đòn tấn công như thế!",
    180: "Dưới sự dõi theo của nhiều binh sĩ‚ Lime đang tham gia một<br>trận đấu tập với Người Lính Eldorana.",
    245: "Chết... Nhưng cô chỉ đang cố phòng thủ thôi! Tôi sẽ kết thúc trận này tại đây!",
    380: "Khi Lime tiếp tục đỡ các đòn tấn công‚ sự chú ý của người lính<br>dần chuyển sang tấn công.",
    423: "Em biết rằng nếu cứ đỡ đòn‚ ngươi sẽ lơ là và tung ra một đòn điên cuồng... Đúng như em dự đoán!<br>",
    507: "Hả!",
    535: "Đã hoàn toàn đoán trước đòn tấn công đó‚ Lime phản đòn bằng những động tác uyển chuyển<br>và hạ gục người lính xuống đất.",
    552: "—Chiếu tướng. Vậy‚ cô còn muốn tiếp tục không?",
    583: "...Không‚ tôi thua rồi. Cô thắng.",
    629: "Ồ! Phó Quan Lime thắng rồi! Đứng trước cả đối thủ nam mà chẳng lùi bước nào<br>thật kinh ngạc!",
    638: "Cô ấy đã đọc trọn dòng chảy trận đấu để giành chiến thắng!<br>Đúng là phó quan của chúng ta!",
    691: "Là một hiệp sĩ kiêu hãnh của Milesgard‚ điều đó là lẽ đương nhiên. Các anh cũng đừng lơ là<br>huấn luyện.",
    749: "Dạ!",
    797: "...Một trận chiến tuyệt vời đấy‚ Lime.",
    851: "Lady Reyzeria! Xin ngài‚ lời khen đó quá hảo tâm với em...!",
    862: "Em sẽ tiếp tục phụng sự<br>không làm ô nhục cương vị phó quan của ngài!",
    874: "Phải‚ ta luôn cậy nhờ em.",
    885: "Lady Reyzeria...! Vâng! Xin ngài hãy giao việc phụ tá cho em!",
    947: "Lady Reyzeria đã khen ngợi em‚ và còn nói ngài cậy nhờ em...! Em mà<br>được hạnh phúc thế này sao?",
    1003: "Phó Quan Lime‚ cô có chút thời gian không?",
    1014: "Ôi‚ có chuyện gì thế? Các anh có báo cáo gì cho phó quan được Lady Reyzeria tín nhiệm<br>không?",
    1025: "Thực ra‚ chúng tôi nhận được một thông điệp bí mật từ những thành viên<br>ở lại bản đảo Milesgard...",
    1036: "...Không phải lúc đùa. Được rồi‚ đưa đây cho em xem.",
    1089: "Lime từ từ xem xét bức thư nhận được. Càng đọc nội dung<br>sắc mặt cô càng méo mó.",
    1100: "...'Lady Reyzeria‚ hiệp sĩ nhục nhã phục vụ một lão đánh thuê hết thời<br>' à?",
    1111: "Bọn họ thậm chí còn nghi ngờ tư cách kế vị ngai vàng của ngài! Cái gì thế này!",
    1163: "Có vẻ những ý kiến như vậy đang lan rộng tại bản đảo Milesgard<br>...",
    1174: "Bọn ở bản đảo đang nghĩ cái gì vậy? Nghi ngờ phẩm chất của Lady Reyzeria<br>... Em không tha thứ cho chuyện này đâu!",
    1185: "Em phải khôi phục danh tiếng cho Lady Reyzeria bằng mọi giá!",
    1233: "Dù có phải lợi dụng gã Chỉ Huy lười biếng đó...!",
    1266: "Phù‚ chắc thế là ổn rồi. Anh để phần còn lại cho ngày mai<br>hôm nay anh nghỉ ngơi thoải mái một chút.",
    1278: "...Chỉ Huy có đây rồi. Em vào nhé.",
    1307: "Không đợi câu trả lời‚ Lime mở cửa phòng chỉ huy và<br>cau mày nhìn %user% đang thư giãn trên ghế.",
    1318: "Thuộc cấp của anh đang làm việc‚ mà anh lại trốn việc nữa à?<br>Thật tình‚ đồ bỏ đi này...",
    1320: "Cô nói với cấp trên thế khi anh đang nghỉ‚ Lime.<br>Đó có phải cách của Milesgard không? Hửm?",
    1332: "Ôi‚ em xin lỗi‚ Chỉ Huy. Em không ngờ công việc đơn giản đến thế<br>lại cần nghỉ ngơi.",
    1334: "Cô lúc nào cũng nhanh miệng thế nhỉ... Thế<br>cô muốn gì?",
    1368: "Em‚ với tư cách là phó quan của Lady Reyzeria‚ đã tự ý soạn thảo<br>một kế hoạch tác chiến mới cho anh.",
    1380: "Nào‚ mau ký đi. Rốt cuộc đó cũng là tất cả công việc của anh<br>mà.",
    1382: "Ý cô là 'Xin hãy ký sau khi xác nhận và phê duyệt' phải không?",
    1384: "Trời ạ... nào‚ đưa anh xem thử.",
    1411: "%user% cầm lấy tài liệu từ tay Lime và lật qua vài trang.",
    1413: "Hừm... anh hiểu rồi.",
    1449: "Kế hoạch này sẽ có lợi cho tương lai‚ anh không nghĩ vậy sao? Nào‚<br>mau phê duyệt đi.",
    1451: "Hừm... nói chung‚ anh cho chừng 50 điểm.",
    1462: "Cái gì! Đừng có giỡn với em! Mắt anh thối rữa rồi hay sao‚ đồ ngốc này!",
    1473: "Phần nào trong kế hoạch của em chưa ổn! Nào‚ nói đi!",
    1475: "Bề ngoài thì đây là một kế hoạch được lập tốt. Không trừ điểm chỗ đó.",
    1477: "Nhưng ý đồ thầm kín không giấu nổi. Nên điểm chỉ bằng một nửa thôi.",
    1488: "…!",
    1490: "Xét theo nội dung‚ mục tiêu thực sự là nâng cao vị thế của<br>Reyzeria. Anh nói sai sao?",
    1492: "Xem cô căng thẳng hơn bình thường‚ anh đoán cô nhận được<br>báo cáo từ bản đảo Milesgard mà cô không vừa ý phải không?",
    1503: "...Ừm‚ thôi được! Anh lúc nào cũng để ý mấy chuyện không nên để ý!",
    1505: "Vậy là anh đã đúng.",
    1516: "Đúng rồi! Anh nói chuẩn xác hoàn toàn!",
    1525: "Bọn hèn nhát ở nhà nói bất cứ điều gì chúng muốn từ vị trí an toàn<br>của chúng!",
    1536: "Nói rằng Lady Reyzeria là nỗi nhục của hiệp sĩ vì phục vụ<br>một lão đánh thuê hết thời!",
    1547: "Nghi ngờ tư cách hoàng tộc của ngài dựa trên thành tích gần đây<br>—bọn họ nói gì cũng được!",
    1556: "Đây toàn là lỗi tại anh!<br>Hãy nhận trách nhiệm và hợp tác!",
    1558: "Anh cũng không vui khi Reyzeria bị đối xử lạnh nhạt. Thực lực<br>của cô ấy là có thật.",
    1560: "Nhưng ở đâu cũng vậy: danh tiếng giảm khi càng xa quê hương.<br>Reyzeria đã biết căn cứ này là một canh bạc thua‚ phải không?",
    1571: "Vâng. Lady Reyzeria đã biết rằng đến căn cứ này sẽ khiến ngài<br>gặp bất lợi.",
    1582: "Thế nhưng‚ ngài ấy tin rằng điều đó là cần thiết để bảo vệ thế giới này và<br>người dân Milesgard‚ nên đã đến.",
    1593: "Phán xét một người cao quý như vậy một cách bất công... tuyệt đối<br>không thể chấp nhận được!",
    1604: "Đó là lý do em muốn giải quyết việc này trước khi Lady Reyzeria phát hiện!",
    1606: "Anh hiểu rồi... anh thấu cảm xúc của em‚ Lime. Và cả tình cảnh của em nữa.",
    1608: "Được rồi‚ anh sẽ phê duyệt kế hoạch sau khi chỉnh sửa đôi chút.",
    1619: "Thật sao!? Anh hiểu chuyện đấy‚ đúng là Chỉ Huy có khác!",
    1630: "Em sẽ đi chuẩn bị tác chiến ngay bây giờ!",
    1648: "Lime hớn hở chạy vụt khỏi phòng chỉ huy. Trông cô chẳng giống<br>chút nào với hình ảnh phó quan đắc lực thường ngày.",
    1660: "Á‚ này... trời ạ‚ cô ta đúng là một trường hợp.",
    1662: "Thôi‚ anh hiểu cô ấy cảm thấy thế nào. Để anh phụ một tay vậy.",
    1664: "...Nhưng Reyzeria thật sự không nhận ra chuyện gì đang xảy ra sao?",
}


def main():
    raw = EN.read_bytes()
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    out = []
    errors = []

    # preflight: a simple structural check before writing
    for i, ln in enumerate(lines, 1):
        s = ln.rstrip("\r\n")
        if not s.startswith(TEXT_CMDS):
            continue
        if i not in VI:
            errors.append(f"L{i}: missing VI translation")
            continue
        if s.startswith("title,"):
            tf = s.split(",", 1)[1]
            new = VI[i]
            if "," in new:
                errors.append(f"L{i} title: ASCII comma in text")
            continue
        parts = s.split(",", 5)
        tf = parts[2] if len(parts) > 2 else ""
        m = SUFFIX_RE.search(tf)
        suffix = m.group(0) if m else ""
        en_br = tf.count("<br>")
        # VI content must contain exactly (en_br - 1) internal <br> for message lines
        vi_br = VI[i].count("<br>")
        if vi_br != en_br - 1:
            errors.append(f"L{i}: <br> count mismatch (EN field={en_br}, VI content={vi_br}, need {en_br-1})")
        if "," in VI[i]:
            errors.append(f"L{i}: ASCII comma in VI text field")

    if errors:
        print("PREFLIGHT FAILED:")
        for e in errors:
            print("  " + e)
        raise SystemExit(1)
    print("PREFLIGHT OK: all <br> counts and comma checks passed.")

    for i, ln in enumerate(lines, 1):
        s = ln.rstrip("\r\n")
        if s.startswith("title,") and i in VI:
            new_text = VI[i]
            new = "title," + new_text
        elif s.startswith(("message,", "messageTextUnder,", "messageTextCenter,")) and i in VI:
            parts = s.split(",", 5)
            tf = parts[2] if len(parts) > 2 else ""
            m = SUFFIX_RE.search(tf)
            suffix = m.group(0) if m else ""
            parts[2] = VI[i] + suffix
            new = ",".join(parts)
        else:
            out.append(ln)
            continue
        ending = "\r\n" if has_crlf else "\n"
        out.append(new + ending)

    VI_PATH.write_bytes(b"\xef\xbb\xbf" + "".join(out).encode("utf-8"))
    print(f"WROTE {VI_PATH} ({len([k for k in VI if k!=30])} message + 1 title records)")


if __name__ == "__main__":
    main()
