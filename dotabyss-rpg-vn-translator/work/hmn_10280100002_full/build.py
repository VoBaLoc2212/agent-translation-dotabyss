#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Field-index VI builder for hmn_10280100002 (EN-asset-is-English case).

JP primary source: novels/hmn_10280100002/ja.json
EN alignment:      novels/hmn_10280100002/en.json + en asset (structural authority)
VI output:         Translation/vi/.../hmn_10280100002.txt

Mirrors trailing tag suffix (every `message,` text field ends with literal
"<br> "; title does not). Supplies only body text with INTERNAL <br> tags placed
where the source had them. No ASCII commas (U+201A '‚' used inside VI text).
BOM + CRLF preserved byte-for-byte.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10280100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# Ordered VI text fields, 1:1 with source text records in file order.
# Record 1 = title; records 2..67 = message lines (lines 24..907 in source).
TRANSLATIONS = [
    # 1) title L17
    "Tìm Viên Quản Lý!",
    # 2) L24
    "—\"Nghe Tiếng Sóng Biển.\"<br>Ngày hôm sau khi nghe kể về cửa hàng Emily từng làm việc.",
    # 3) L63
    "Viên Quản Lý thực sự ở đâu đó trong khu chợ này sao‚ tôi tự hỏi...",
    # 4) L65
    "Cửa hàng Emily từng làm việc tại Eldorana.",
    # 5) L67
    "Ludia bảo cô ấy thấy một cửa hàng trùng tên với cửa hàng đó‚ vốn<br>đã đóng cửa từ khi viên quản lý xuống Đại Huyệt tìm kho báu.",
    # 6) L69
    "Có thể Ludia nhầm‚ hoặc cũng chỉ là trùng hợp trùng tên...<br>Nhưng anh vẫn muốn đi tìm nó đúng không?",
    # 7) L81
    "Vâng! Vì đã đi xa đến thế này rồi‚ em muốn tìm kiếm nhiều nhất có thể.",
    # 8) L93
    "Á‚ nhưng... anh thật sự không sao khi đi xa giúp em đến thế này sao‚<br>Chỉ Huy? Em vui lắm‚ nhưng...",
    # 9) L95
    "Đừng bận tâm. Công việc hôm nay anh đã xong rồi‚ với lại thỉnh<br>thoảng cũng cần vận động chút.",
    # 10) L106
    "Ôi! Một người đàn ông biết hoàn thành công việc!",
    # 11) L118
    "Được rồi! Thế thì‚ nếu anh khăng khăng... Cùng cố gắng tìm cửa<br>hàng của viên quản lý nhé!",
    # 12) L148
    "Hmm... khó tìm thật đấy‚ nhỉ?",
    # 13) L150
    "Biển hiệu cửa hàng thì vô số kể mà...",
    # 14) L152
    "Khu chợ đủ loại hàng‚ từ những cửa hàng lớn đến các sạp hàng chỉ<br>bày hàng ra đất‚ nên việc tìm kiếm cũng vất vả.",
    # 15) L163
    "Bình thường em chỉ lướt qua trên đường đi làm‚ nhưng khi thực sự<br>nhìn quanh thì có biết bao nhiêu cửa hàng khác nhau.",
    # 16) L213
    "Á‚ mấy đặc sản ở kia trông hợp làm quà lưu niệm<br>ghê.",
    # 17) L242
    "Á‚ đồ uống ở tiệm này trông ngon quá! Rượu trái cây‚ hả... Chắc<br>mang về bán ở chỗ em cũng được đấy.",
    # 18) L259
    "Này này‚ đừng đi lạc chủ đề quá... Ấy‚ đi đâu mất rồi?",
    # 19) L289
    "Chỉ Huy! Nhìn độ bóng của miếng thịt này này! Phần nước thịt chảy<br>xuống trông ngon tuyệt vời luôn!",
    # 20) L291
    "Thịt xiên nướng‚ hả... Thôi‚ trông cũng ngon thật‚ anh công nhận.",
    # 21) L302
    "Hôm nay chúng ta phải đi bộ nhiều‚ nên cần ăn uống tử tế để giữ<br>sức.",
    # 22) L336
    "Nói ahh đi!♪",
    # 23) L338
    "Không đời nào.",
    # 24) L379
    "Nhanh quá!",
    # 25) L388
    "Ư... em chỉ muốn đến gần anh hơn thôi‚ Chỉ Huy...<br>Đáng ghét quá...",
    # 26) L390
    "N-này... người ta sẽ hiểu lầm mất...! Thôi thôi‚ anh ăn là được mà.",
    # 27) L402
    "Thật ư!? Thế thì‚ một lần nữa—",
    # 28) L404
    "Nhưng anh sẽ tự ăn.",
    # 29) L415
    "Không công bằng!",
    # 30) L417
    "Mm... ồ‚ ngon đấy.",
    # 31) L428
    "Yay!♪ Ehehe‚ em vui vì anh thích nó!♪",
    # 32) L430
    "...Đáng lẽ đang buồn vì không được đút ăn mà‚ anh<br>chuyển sang nhanh thế.",
    # 33) L442
    "Thôi‚ dù sao được đút ăn thì cũng vui hơn... nhưng hơn thế nữa‚ em<br>chỉ thích thấy người khác vui vẻ thôi!♪",
    # 34) L444
    "Ra là vậy... anh đúng là nhất quán nhỉ?",
    # 35) L455
    "Thế thì‚ vừa ăn vừa đi tìm luôn nhé!<br>Được rồi‚ ăn nhiều vào♪",
    # 36) L457
    "Khoan khoan‚ chắc chắn là cần ăn... nhưng liệu có thời giờ vừa ăn<br>vừa đi bộ không?",
    # 37) L469
    "Hmm... nhưng nếu mua đồ ăn dọc đường‚ không phải cũng có thể hỏi<br>thăm mấy người bán hàng sao?",
    # 38) L471
    "Hmm... ừm‚ đúng là vậy thật.",
    # 39) L505
    "(Nghĩ kỹ thì‚ hỏi xin thông tin mà không mua gì là bất lịch sự‚<br>nên cách của Emily cũng khá hợp lý đấy.)",
    # 40) L539
    "Chỉ Huy‚ anh mở miệng ra một chút cho em được không?",
    # 41) L550
    "Nói ahh đi!♪",
    # 42) L552
    "À... ừm?",
    # 43) L590
    "Ehehe‚ kế hoạch của em thành công! Em bắt được anh lúc anh đang<br>ngày mơ giữa ban ngày‚ Chỉ Huy!♪",
    # 44) L601
    "Sao? Bánh bao ngon không?",
    # 45) L603
    "...Ừm‚ đúng là ngon... nhưng mà lợi dụng lúc anh mất tập trung<br>thế này thì...",
    # 46) L614
    "Hì hì!♪",
    # 47) L629
    "(Không chỉ dễ thương‚ cô ấy còn đáng tin cậy và tinh tế nữa. Một<br>người giỏi giang đấy‚ cô gái này.)",
    # 48) L656
    "Á‚ có con bọ! Bọ!",
    # 49) L658
    "Ừa‚ xung quanh toàn sạp hàng nên mấy con bọ thế này cũng hay có‚ tôi—",
    # 50) L671
    "Nhận lấy!",
    # 51) L691
    "*Rầm!*",
    # 52) L693
    "Trước khi anh kịp phản ứng‚ cô ấy đã nhặt tấm ván gỗ dưới đất rồi<br>đập bẹp con bọ.",
    # 53) L695
    "Cái gì...?",
    # 54) L707
    "Ehehe... xin lỗi vì làm anh giật mình.",
    # 55) L718
    "Em làm nhà hàng lâu quá rồi nên hễ thấy bọ là cơ thể tự động phản<br>ứng thôi. Phải xử lý trước khi khách thấy chứ!",
    # 56) L720
    "Dù vậy‚ tốc độ đó kinh hoàng thật.",
    # 57) L722
    "Emily cứng cáp hơn anh tưởng.",
    # 58) L770
    "Hmm... tìm mãi chẳng thấy.",
    # 59) L772
    "Trời đã tối. Thôi hôm nay đến đây thôi... Hử?",
    # 60) L797
    "Xin mời... giá hời...",
    # 61) L806
    "(Mở sạp hàng với bộ dạng rách rưới thế kia... có vẻ đang rất chật<br>vật đấy.)",
    # 62) L815
    "Nhìn một sạp hàng nổi bật giữa vô số cửa hàng trong chợ thì—<br>một tấm ván gỗ cũ kỹ đặt cạnh hàng hóa bỗng lọt vào mắt anh.",
    # 63) L854
    "...'Nghe Tiếng Sóng Biển—Chi Nhánh Căn Cứ Tiền Tuyến'...? Này‚<br>Emily. Có khi nào chỗ này là—",
    # 64) L892
    "Viên Quản Lý!",
    # 65) L894
    "Ôi!",
    # 66) L905
    "Chính là anh‚ Viên Quản Lý đúng không? Là em‚ Emily đây!",
    # 67) L907
    "Ưm...? ...Hử‚ Emily? Sao em lại ở đây...?",
]


def main() -> None:
    data = EN.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    vi_lines: list[str] = []
    idx = 0
    record_count = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            record_count += 1
            assert idx < len(TRANSLATIONS), f"Ran out of translations at record {record_count}"
            vi_text = TRANSLATIONS[idx]
            idx += 1
            assert "," not in vi_text, f"ASCII comma in VI text (record {record_count}); use U+201A '‚'"
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text
            else:
                parts = ln.split(",", 5)
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                parts[2] = vi_text + suffix
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    assert idx == len(TRANSLATIONS), f"translations not fully used: {idx}/{len(TRANSLATIONS)}"
    assert record_count == len(TRANSLATIONS), f"record count {record_count} != {len(TRANSLATIONS)}"

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()
