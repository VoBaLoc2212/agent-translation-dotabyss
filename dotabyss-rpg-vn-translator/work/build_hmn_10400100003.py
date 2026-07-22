# -*- coding: utf-8 -*-
"""Build VI output for hmn_10400100003.

EN-asset-is-English case (en.json holds English; ja.json == identity map).
All text fields already hold English -> translate EN->VI.
EN asset "Commaander" typo repaired to "Chỉ Huy" (intentional correction).
Structural authority = EN asset (delimiters, BOM, CRLF, <br> count, <size> cards).
Per field:
  - title,            : VI at field index 1 (no <br> suffix mirror)
  - message,          : VI at field index 2, then mirror the source trailing "<br> " suffix
  - messageTextCenter,: VI at field index 2, preserve parts[3:] (e.g. ,,,on)
Field 1 (speaker label) preserved byte-identical (JP keys / <user>).
ALL trailing parts[3:] are preserved so delimiter/field/tag counts match EN.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10400100003.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10400100003.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
SUF_RE = re.compile(r"(?:<br>\s*)+$")

# line_no -> VI text field (inner text; EN <br> counts already match source)
VI: dict[int, str] = {
    29: "Bọn Tuyệt Đỉnh Hai Người Đấy Thôi!",
    39: "<size=48>—Khu Rừng Gần Căn Cứ Tiền Tuyến</size>",
    48: "Tiếng đất bị đào bới mạnh mẽ vang vọng từ sâu trong<br>rừng thẳm.",
    84: "Rồi‚ mình đào xong mấy cái hố bẫy rồi! Còn đặt thêm bẫy<br>th slime trơn và mấy con bù nhìn trông y như mình nữa!",
    95: "Mình cá là Chỉ Huy nghĩ mình chỉ là một cô bé ngốc lao<br>thẳng vào thôi! Anh ấy chẳng ngờ mình giăng bẫy thế này đâu!",
    107: "Chỉ Huy chắc cũng có kế hoạch‚ nhưng chỉ cần mình làm anh ấy<br>đứng yên là mình thắng chắc!",
    147: "Giờ chỉ còn chờ Chỉ Huy sa vào bẫy thôi... mà sao anh ấy<br>chưa tới nhỉ?",
    158: "Ừm‚ chỗ này khó tìm quá à? Mình đi tìm chỗ trống trải thì lạc<br>tận sâu trong rừng mất rồi...",
    226: "Luca đi quẩn quanh tìm Chỉ Huy. Mặt đất<br>dưới chân cô bỗng sụt xuống rào xạo xạc.",
    257: "Á‚ á á! Mình lại rớt xuống hố bẫy mình tốn biết bao công đào!",
    268: "Khoan khoan! Phải chui ra mau! Giờ Chỉ Huy tới thì<br>chết dở!",
    270: "Còn anh thì sao?",
    281: "Chỉ Huy mà tới‚ anh ấy lại nhễu mình rồi bắt mình nhận thua...",
    292: "Hả? Chỉ Huy?",
    327: "Ý em là anh lo chuyện này à? Ừm? Thế này hả?",
    338: "Phì ha ha ha ha! Thôi đi‚ thôi đi!",
    340: "Thật đấy‚ anh đang nghĩ ra đủ chiêu mới để thắng em‚ thế mà em tự<br>rớt xuống bẫy của chính mình rồi.",
    351: "Đáng lẽ anh mới là người rớt vào... *sụt sịt* thế này thì mình có<br>làm nổi Võ Sư Vĩ Đại Nhất Thế Giới không ta...?",
    353: "Xử lý bẫy và mồi nhử là nhờ kinh nghiệm. Anh nghĩ trải nghiệm<br>này sẽ giúp em trưởng thành đấy‚ em biết không?",
    364: "Th-thế à...? Tự dưng mình hết tự tin rồi...",
    375: "Đâu phải mình tự nghĩ ra kế hoạch hay ho rồi...",
    377: "Đâu có gì suôn sẻ ngay từ đầu. Nào‚ anh đưa tay kéo em<br>lên khỏi hố đi.",
    394: "Ừm. Cảm ơn‚ Chỉ Huy.",
    431: "*thở dài*... mình yếu thế này sao...",
    433: "Anh nói gì thế? Em mạnh mà‚ Luca. Mạnh hơn anh<br>nhiều.",
    444: "Mình mạnh hơn Chỉ Huy...? Thế mà mình thua anh ấy bao nhiêu lần!",
    446: "Chính vì anh yếu hơn em nên anh mới dùng bẫy và mưu mẹo.<br>Nếu đánh đường hoàng‚ anh chẳng có cửa thắng.",
    457: "Nhưng anh là người mạnh nhất Căn Cứ Tiền Tuyến‚ đúng<br>không‚ Chỉ Huy?",
    459: "Ý họ là nếu anh dùng mọi thủ đoạn. Và nghe này‚ nếu anh<br>nghiêm túc thì anh thắng trước khi trận đánh bắt đầu.",
    470: "Hả!? Sao cơ?",
    472: "Đầu tiên‚ đánh kẻ đã sẵn sàng là không hiệu quả. Anh sẽ chuẩn bị<br>lực lượng áp đảo rồi tung đòn bất ngờ.",
    474: "Chỗ đó anh cũng giăng bẫy‚ thậm chí có khi bắt cả con tin. Có khi anh<br>cho chúng uống rượu để mất cảnh giác‚ hoặc dùng độc.",
    476: "Anh sẽ dùng mọi cách để tiêu diệt kẻ địch. Chính vì anh là<br>người mạnh nhất căn cứ trong điều kiện đó nên anh mới là Chỉ Huy.",
    487: "Ê hè? Thắng kiểu vậy mà cũng nói được là thắng à?",
    489: "Anh không phải võ sư. Anh phải thắng bằng mọi thủ đoạn. Đó là<br>ý nghĩa của việc làm Chỉ Huy.",
    491: "Đến lúc chiến đấu với Tai Họa‚ em chẳng thể nói 'dù thua cũng không<br>gian lận' được‚ đúng không?",
    502: "...Ra là vậy. Chỉ Huy mà thua thì mọi người cùng thua‚ phải không?",
    504: "Đúng thế. Vì em mạnh nên anh muốn cho em thấy kẻ như anh—<br>kẻ yếu đuối khao khát chiến thắng—phản kháng ra sao.",
    506: "Điều em cần không phải mưu mẹo bỉ ổi như anh. Mà là sức mạnh<br>hiểu rõ mưu mẹo là gì rồi vượt qua cả chúng.",
    517: "Biết về chiêu trò bỉ ổi mà đủ mạnh để không thua trước<br>chúng... không biết mình có thành được như vậy không.",
    580: "Gùuu...",
    584: "Hả! Quái vật!",
    586: "Nghe tiếng gầm thấp‚ bọn họ nhìn quanh thấy quái vật từ<br>trong rừng ùa ra vây quanh.",
    634: "Kẻ địch...! Có phải tại mình gọi Chỉ Huy sâu vào rừng nên...?",
    636: "Đừng lo. Chỉ là vài kẻ địch lọt qua vành đai phòng thủ<br>thôi. Em xử dễ dàng mà‚ đúng không?",
    647: "Ừ-ừm‚ được...",
    673: "Luca bước tới‚ nhưng khựng lại. Đôi tay cô giơ thế thủ<br>run lên bần bật.",
    675: "Sao thế‚ Luca?",
    717: "Em ổn‚ chắc vậy. Nhưng nếu lũ quái vật đó giăng bẫy‚ hay thực<br>chất chỉ là bù nhìn thì sao?",
    719: "Theo anh biết‚ chúng không phải loại dùng mưu mẹo. Đừng<br>lo. Em đánh đường hoàng thì gần như chẳng ai thắng nổi em.",
    730: "Thật hả?",
    732: "Ừ! Em mạnh hơn anh‚ mà anh được gọi là mạnh nhất Căn Cứ<br>Tiền Tuyến. Vậy tức là em mạnh nhất căn cứ!",
    743: "Mình mạnh nhất...? Mình là mạnh nhất?",
    745: "Đúng vậy‚ Luca‚ em là mạnh nhất. Nếu em nghĩ anh mạnh thì<br>em phải nghĩ mình còn mạnh hơn!",
    757: "Em không rõ... không hiểu nổi‚ nhưng... nếu Chỉ Huy nói vậy thì<br>em tin được.",
    768: "Được rồi‚ mình thử! Mình sẽ tung hết sức‚ Chỉ Huy!",
    770: "Ừ‚ thổi bay chúng đi!",
    795: "*haaaa!*",
    872: "Gùuoooo!",
    929: "Luca lao tới con quái vật không do dự. Nắm đấm cô bao bọc<br>sấm sét thổi bay kẻ địch chỉ trong một đòn.",
    965: "Mình đánh trúng—mình thắng được! Mình mạnh!",
    1092: "GUUUUUÔN!",
    1207: "Luca nhảy múa tàn sát lũ quái vật. Mỗi cú đấm tay sấm<br>sét giáng xuống‚ hàng ngũ địch thưa dần.",
    1250: "ÔÔÔÔÔÔ!",
    1300: "Ôi! Con quái vật cuối trốn thoát rồi! Chạy đi‚ Chỉ Huy!",
    1334: "Không sao! Được rồi‚ lối này‚ con quái vật kia!",
    1361: "ƯN!",
    1369: "Con quái vật lao vào Chỉ Huy trượt trên lớp slime trơn‚ ngã<br>và giẫm chân vào hố bẫy.",
    1409: "Nó vấp ngã...! Á‚ đúng rồi! Đó là bẫy mình giăng!",
    1420: "Dù không tự giăng nhưng anh dùng quá chuẩn... Chỉ Huy‚<br>ghê thật!",
    1422: "Đang khen anh mà cắt ngang‚ nhưng anh nghĩ nhễu không<br>tác dụng với con này đâu. Kết liễu nó đi‚ Luca!",
    1463: "Ừ! Đây là chiêu bài song tấu tối thượng—mình và Chỉ Huy!",
    1482: "Và biến đi!",
    1527: "Gùaaaaaah!",
    1556: "Cú móc xoay của Luca bùng cháy sấm sét dữ dội‚ biến con<br>quái vật bất động thành tàn tích cháy đen.",
    1592: "Chúng ta thắng rồi!",
    1624: "Hêm‚ hêm‚ nhờ có em‚ Luca‚ anh mới sống sót được.",
    1635: "Không‚ anh mới là người cứu em‚ Chỉ Huy.",
    1646: "Vậy ra có kẻ địch mình không thắng nổi chỉ bằng sức mạnh... có<br>khi mình vẫn chưa đủ mạnh trước những đối thủ đó.",
    1658: "Nhưng mình như đã tìm ra con đường cần đi để trở thành<br>võ sư vĩ đại nhất thế giới!",
    1669: "Nếu chiến đấu bên anh và học từng bước một‚ mình chắc chắn<br>sẽ thành võ sư vĩ đại nhất thế giới!",
    1671: "Ừ‚ cho đến khi em thành Võ Sư Vĩ Đại Nhất Thế Giới‚ anh sẽ bù<br>đắp những gì em thiếu. Hãy tin anh mà chiến đấu hết sức.",
    1683: "Ừ! Có Chỉ Huy thông minh và võ thuật của mình‚ bọn mình<br>không gì cản nổi! Chắc chắn là song tấu mạnh nhất căn cứ!",
    1706: "Thôi nào‚ ăn mừng cho song tấu mạnh nhất đi. Luca‚ đi<br>kiếm chút đồ ăn không?",
    1717: "Yay! Anh mời em chứ‚ đúng không‚ Chỉ Huy?",
    1719: "Trời ạ‚ em lẹ thế chuyện trục lợi...",
    1765: "Tìm thấy anh rồi‚ Chỉ Huy!",
    1769: "Gớ!",
    1823: "Ô‚ Alicia à? Có chuyện gì? Chị cần Chỉ Huy việc gì à?",
    1834: "Vâng! Chỉ Huy bỏ việc để đi gặp em đấy! Giờ tôi phải bắt anh<br>làm nốt phần còn lại!",
    1836: "Khoan đã! Tôi vừa sống sót suýt chết xong! Cho tôi nghỉ hôm nay!",
    1888: "Tôi không thể! Sắp hết hạn rồi! Nào‚ quay lại phòng chỉ<br>huy thôi!",
    1890: "T-tôi từ chối! Tôi không quay lại đâu!",
    1923: "Chỉ Huy! Tôi không để anh trốn thoát đâu!",
    1989: "Ông Chỉ Huy đó bất lực trước Alicia-san đúng là... ghê thật!",
    2000: "Tức là Alicia-san là người mạnh nhất căn cứ này!",
    2017: "Alicia-san ơiii!",
    2083: "Có chuyện gì‚ Luca? Tôi sắp tóm được Chỉ Huy rồi—",
    2094: "Em thách đấu chị‚ Alicia-san‚ người mạnh nhất căn cứ! Đấu với em đi!",
    2105: "Êêêhh!",
    2116: "Em sẽ đánh bại Alicia-san và trở thành người mạnh nhất căn cứ!",
    2127: "Tôi đâu có mạnh nhất chút nào!",
    2129: "Song tấu mạnh nhất thì sao? Em đổi ý nhanh thật... mà‚ đó<br>chính là điểm tốt nhất của Luca.",
    2175: "Mình sẽ thành Võ Sư Vĩ Đại Nhất Thế Giới! Cứ thử xem!",
}

assert len(VI) == 104, f"expected 104 VI entries, got {len(VI)}"

lines = EN.read_text(encoding="utf-8-sig").splitlines()
raw = EN.read_bytes()
has_crlf = b"\r\n" in raw

# ---- preflight: compare inner <br> counts for ALL message lines before writing ----
mismatches = []
for i, line in enumerate(lines, 1):
    if line.startswith("message,"):
        parts = line.split(",", 5)
        tf = parts[2]
        m = SUF_RE.search(tf)
        inner_en = tf[: m.start()] if m else tf
        new_text = VI[i]
        if "," in new_text:
            mismatches.append(f"L{i}: ASCII comma in VI: {new_text!r}")
        if inner_en.count("<br>") != new_text.count("<br>"):
            mismatches.append(
                f"L{i}: <br> mismatch en_inner={inner_en.count('<br>')} vi={new_text.count('<br>')}\n"
                f"     EN : {inner_en!r}\n     VI : {new_text!r}"
            )
if mismatches:
    print("PREFLIGHT FAILED - fix these before writing:")
    print("\n".join(mismatches))
    raise SystemExit(1)

out = []
for i, line in enumerate(lines, 1):
    if line.startswith(TEXT_CMDS):
        if line.startswith("title,"):
            parts = line.split(",", 1)
            cmd = parts[0]
            new_text = VI[i]
            assert "," not in new_text, f"ASCII comma in VI title line {i}: {new_text!r}"
            out.append(f"{cmd},{new_text}")
        elif line.startswith("message,"):
            parts = line.split(",", 5)
            cmd = parts[0]
            tf = parts[2]
            m = SUF_RE.search(tf)
            suf = m.group(0) if m else ""
            inner_en = tf[: m.start()] if m else tf
            new_text = VI[i]
            assert "," not in new_text, f"ASCII comma in VI message line {i}: {new_text!r}"
            assert inner_en.count("<br>") == new_text.count("<br>"), (
                f"<br> mismatch line {i}: en_inner={inner_en.count('<br>')} vi={new_text.count('<br>')}"
            )
            parts[2] = new_text + suf
            out.append(",".join(parts))
        else:  # messageTextUnder / messageTextCenter
            parts = line.split(",", 5)
            cmd = parts[0]
            new_text = VI[i]
            assert "," not in new_text, f"ASCII comma in VI {cmd} line {i}: {new_text!r}"
            parts[2] = new_text
            out.append(",".join(parts))
    else:
        out.append(line)

text = "\n".join(out)
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
VI_PATH.write_text("\ufeff" + text + "\n", encoding="utf-8")
print(f"WROTE {VI_PATH} :: {len(out)} lines, crlf_mirror={has_crlf}")
print("VI entries:", len(VI))
