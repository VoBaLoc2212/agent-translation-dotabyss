#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Field-index VI builder for hmn_10250100002 (EN-asset-is-English case).

Mirrors the trailing tag suffix (every `message,` ends with literal "<br> ";
messageTextUnder/title do not). Supplies only body text with INTERNAL <br>
tags placed where the source had them. No ASCII commas (U+201A '‚' used).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10250100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# Ordered VI text fields, 1:1 with source text records in file order.
TRANSLATIONS = [
    # 1) title
    "Wendy Và Các Pháp Sư",
    # 2) message L61  (source has 1 internal <br> + suffix = 2 total)
    "Hãy cẩn thận bước chân nhé! Nếu ngã thì bạn sẽ lộn nhào<br>xuống tận đáy luôn đấy!",
    # 3) L110
    "Ư… Này‚ Wendy? Chỗ mỏ quặng chúng ta vẫn chưa tới à?",
    # 4) L119
    "Em bắt đầu đi bộ mỏi rã rời rồi đấy.",
    # 5) L130
    "Nhưng chúng ta mới đi bộ chưa tới một tiếng thôi mà... Thế mà bạn đã mệt rồi à?<br>",
    # 6) L141
    "Ư… Em không hề mệt chút nào!♪",
    # 7) L152
    "Hả? Nhưng nãy bạn vừa nói mà...",
    # 8) L163
    "Ha! Ahaha‚ đúng rồi! Em lơ đễnh quá‚ xin lỗi nha?♡",
    # 9) L207
    "Xin lỗi Wendy nhé. Chị gái em đúng là rất hay đua tranh.",
    # 10) L285
    "Này‚ Veera! Đừng có nói với cô ấy thế chứ!",
    # 11) L293
    "Ưm‚ à… Nhưng bạn là pháp sư mà‚ nên thể lực kém hơn cũng là chuyện bình thường thôi‚ em nghĩ vậy!<br>",
    # 12) L306
    "Em là ô-tô-mát nên đúng nghĩa là chẳng bao giờ biết mệt!",
    # 13) L358
    "Em biết mà! Em cứ thắc mắc mãi về chuyện đó!",
    # 14) L416
    "Tiện thể‚ bạn có những chức năng gì thế?<br>Em cũng tò mò về nguồn năng lượng của bạn. Rồi cả chất liệu da nữa...",
    # 15) L427
    "K… Khoan đã! Mắt bạn‚ mắt bạn trông đáng sợ quá!",
    # 16) L455
    "Á‚ xin lỗi bạn. Tính tò mò ham hiểu biết của em trỗi dậy quá đà mất rồi.",
    # 17) L466
    "Loại ô-tô-mát có hiệu năng cao thế này đâu phải lúc nào cũng gặp được đâu‚ phải nói vậy.<br>",
    # 18) L477
    "Fufuu!♪ Bởi vì Cha là một pháp sư tuyệt vời còn gì!",
    # 19) L488
    "Cha à? ...Á‚ ra là bạn gọi người phát triển là \"\"Cha.\"\"",
    # 20) L536
    "Bắt một ô-tô-mát gọi ổng là \"\"Cha\"\"... Nghe cũng hơi biến thái phết nhỉ?<br>đùa thôi!♡",
    # 21) L580
    "Em được tạo hình dựa trên người con gái đã mất của Cha đấy‚ bạn biết mà!",
    # 22) L589
    "Chúng em không chung dòng máu‚ chỉ giống nhau bề ngoài thôi‚ nhưng cha của em vẫn là cha em!<br>",
    # 23) L646
    "…",
    # 24) L663
    "Chị ơi‚ nếu nghĩ mình có lỗi thì chị nên xin lỗi mới đúng.",
    # 25) L672
    "E… em biết mà!",
    # 26) L737
    "Ưm‚ à… xin lỗi vì đã gọi bố bạn là kẻ biến thái...",
    # 27) L748
    "Biến thái? Ý đó là sao?",
    # 28) L759
    "Hả? À… ý là một người như ông anh ấy.",
    # 29) L770
    "Ra là thế... vậy ý là một người cực kỳ tuyệt vời! Tại sao bạn lại xin lỗi khi đang khen ngợi ổng thế?<br>",
    # 30) L781
    "C… không phải ý đó đâu... Ahaha‚ thôi bỏ qua chuyện này đi!♡",
    # 31) L790
    "Dù sao thì‚ chúng ta vẫn chưa tới chỗ có quặng sao...?",
    # 32) L799
    "Sắp tới nơi rồi. Tiện thể‚ bạn định dùng mỏ quặng đó làm gì đấy?<br>",
    # 33) L810
    "Bạn có nói là dùng cho ma pháp thí nghiệm mà...",
    # 34) L858
    "Đúng rồi! Em định dùng nó cho một việc cực kỳ tuyệt vời!♪",
    # 35) L870
    "Em cần mỏ quặng đó để tăng sức mạnh cho ma pháp của mình.",
    # 36) L881
    "Em sẽ làm ma pháp của mình mạnh hơn nữa và làm ông anh bất ngờ!",
    # 37) L892
    "Thế thì ổng sẽ chẳng còn cãi lại em được nữa!♪",
    # 38) L945
    "Cãi lại à...?",
    # 39) L956
    "Chị ấy thật sự rất thích Chỉ Huy‚ nên cứ hay trêu chọc ổng‚ và ổng thường hay la mắng chị ấy.<br>",
    # 40) L967
    "Chị ấy cứ thẳng thắn nói là mình thích ổng đi. Nhưng tính cách đó của chị ấy cũng đáng yêu mà‚ bạn không nghĩ vậy sao?<br>",
    # 41) L978
    "Ư… ừm… em không chắc.",
    # 42) L1026
    "Á‚ ừm… chúng ta tới nơi rồi!<br>Đây là khu mỏ khai thác quặng.",
    # 43) L1100
    "Ồa‚ đầy đá thế này...<br>Thế nó nằm ở đâu trong đống này?",
    # 44) L1150
    "Nó ở đâu đó quanh đây thôi!",
    # 45) L1204
    "Hả?",
    # 46) L1215
    "C… ý bạn là sao?<br>Em có hỏi là nó ở đâu mà‚ bạn biết mà...?",
    # 47) L1227
    "Vì đây là quặng hiếm nên em chỉ có thể nói là nó có thể ở đâu đó quanh<br>đây thôi!",
    # 48) L1238
    "Dù đào lên có khi cũng chẳng thấy đâu. Nhưng mọi người cùng nhau cố gắng đào nhé!<br>",
    # 49) L1247
    "Không đời nào... phiền phức quá đi!",
    # 50) L1258
    "Hả? C… sao tự dưng thế?",
    # 51) L1267
    "*thở dài*... hay là em về nhà vậy.",
    # 52) L1315
    "Chị lớn ơi‚ nếu chị tự tay đào được quặng ra ở đây‚ chị không nghĩ Chỉ Huy sẽ vô cùng bất ngờ sao?<br>",
    # 53) L1371
    "…",
    # 54) L1384
    "Nếu chị làm vậy‚ em nghĩ Chỉ Huy cũng sẽ nể phục chị luôn đấy...",
    # 55) L1395
    "...Em biết mà.<br>Từ đầu em đã định tự mình tìm ra nó rồi!",
    # 56) L1406
    "Với một người như em thì tìm một hai mỏ quặng cũng dễ ợt!",
    # 57) L1474
    "Ahaha… ra là thế.<br>Ra đây mới là Verisa thật sự.",
    # 58) L1524
    "Vậy mọi người cùng nhau nỗ lực đào nhé.<br>Hướng tới mỏ quặng hiếm thôi!",
    # 59) L1570
    "Tìm thấy rồi!<br>Chính là nó.<br>Đây chính là thứ em muốn!",
    # 60) L1634
    "Chúc mừng!♪<br>Chị lớn!",
    # 61) L1645
    "Kẻ lót đường!♡ Kẻ lót đường!♡<br>'Quặng hiếm' thế mà dễ tìm ra thế—đồ quặng lót đường!",
    # 62) L1656
    "Tìm thấy rồi em mừng quá! Một mảnh thôi có đủ không?",
    # 63) L1667
    "Tất nhiên rồi! Vì em là thiên tài mà. Em có thể thành công ngay lần thử đầu tiên với thí nghiệm mà!<br>",
    # 64) L1674
    "Chúng em sẽ đến xưởng chế tác bây giờ để chuẩn bị cho thí nghiệm.",
    # 65) L1685
    "Wendy‚ cảm ơn bạn nhiều vì đã giúp đỡ hôm nay.",
    # 66) L1694
    "Em cũng vui lắm khi được trò chuyện với hai bạn!",
    # 67) L1742
    "Này! Bạn bỏ kiểu nói trang trọng đi được rồi. Giờ chúng ta là bạn rồi mà‚<br>đúng không!♪",
    # 68) L1753
    "Hay là sao? Bạn muốn làm tiểu đệ của em à? Để em gọi bạn là 'kẻ lót đường' nhé?♪",
    # 69) L1815
    "Bạn bè... em vui quá! Em muốn có bạn!",
    # 70) L1826
    "Trời ơi‚ trông bạn vui hết cả lên kìa.",
    # 71) L1890
    "Fufu!♪ Em nghĩ chị lớn cũng trông vui nữa kìa.",
    # 72) L1899
    "C… không phải đâu!",
    # 73) L1919
    "Dù sao thì‚ chúng em đi đây! Tạm biệt nhé‚ Wendy!",
    # 74) L1930
    "Lần sau gặp lại‚ cho em khám cơ thể bạn kỹ càng nhé.",
    # 75) L1939
    "Ừ! Hẹn gặp lại hai bạn sau nhé!",
    # 76) L2000
    "Ehehe. Hôm nay em có hai người bạn mới luôn.",
    # 77) L2012
    "Em phải báo cáo việc này với Cha!♪ Giấy viết thư hình như ở quanh<br>đây...",
    # 78) L2031
    "Tìm thấy rồi! Ưm‚ trước tiên...",
    # 79) L2055 messageTextUnder
    "Wendy đặt tờ giấy viết thư lên bàn và bắt đầu viết ra những sự kiện trong ngày.",
    # 80) L2077 messageTextUnder
    "Kính gửi Cha‚ hôm nay con đã có bạn mới. Một bạn là cô bé dễ thương và vui vẻ‚ bạn kia là một cô gái sành điệu và tuyệt vời.",
    # 81) L2088 messageTextUnder
    "Dù con là ô-tô-mát‚ họ vẫn đối xử với con như bạn bè mà chẳng chút do dự.",
    # 82) L2100 messageTextUnder
    "Lần sau con cũng sẽ giới thiệu Cha với họ nữa...",
    # 83) L2132
    "Rồi‚ con viết xong thư rồi! Mai con sẽ gửi đi. Ehehe.",
    # 84) L2144
    "*ngáp*... con nên đi ngủ sớm thôi. Ngày mai con cũng có việc mà!",
    # 85) L2157
    "Chúc ngủ ngon...",
    # 86) L2159
    "Đang Chuyển Sang Chế Độ Ngủ.",
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
