#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build VI asset for hmn_10430100001 (EN-asset-is-English, mixed JP-title case).
Keyed by sequential text-record index (1-based, file order).

Scene: Gemma (ジェンマ) the old dwarf + Commander (<user>) + 店主 (shopkeeper, JP label kept).
- <user> / Commander -> Chỉ Huy (addressed by Gemma as "boy" -> "chú bé"; Commander self-refers anh/em).
- Gemma: old dwarf woman, gruff-but-fond, "ワシ" (washi) -> "ta"; calls Commander "小僧/boy" -> "chú bé".
- 店主: shopkeeper (male merchant). Commander addresses him "mister" -> "ông", "shopkeeper" -> "chủ tiệm".
  The JP speaker label 店主 is KEPT verbatim (technical field).
- Title JP -> Vietnamese Title Case. Center card retranslated (EN paraphrased "Frontline Base Town";
  use project term Căn Cứ Tiền Tuyến).
- ASCII commas inside VI text -> U+201A (‚).
- Tag/placeholder/BOM/CRLF preserved via parts[1]/parts[2] rejoin.
"""
from pathlib import Path
import sys

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100001.txt"

VI_DICT = {
1: "Món Quà Từ Ngày Xa Xưa",
2: "<size=48>—Căn Cứ Tiền Tuyến</size>",
3: "Hô hô hô‚ hôm nay phố phường lại đông đúc nhỉ. Bước ra những nơi<br>náo nhiệt thế này khiến lão người lùn này thấy mình trẻ lại.<br> ",
4: "Nhưng trông ngài vẫn nhanh nhẹn thế kia mà… nếu trẻ lại nữa thì<br>sẽ làm gì đây?<br> ",
5: "Ta đã bảo ta là người lùn rồi chứ gì! Lão Gemma này chỉ là một bà lão yếu đuối thôi.<br> ",
6: "Phụ tá cho người già là việc của kẻ trẻ. Nên ta bắt chú bé phải<br>bám sát lấy ta đấy.<br> ",
7: "Phụ tá cái gì chứ‚ chỉ là con vật khuân vác thôi. Nhìn xem ngài bắt<br>ta xách hết cả đống này! Khỉ thật…<br> ",
8: "Coi như tiền học phí rẻ bèo vì được tận mắt thấy con mắt tinh đời<br>của lão già này là được.<br> ",
9: "Ừm‚ đúng vậy. Dù có lúc ta mua bừa bãi‚ ngài vẫn luôn soi xét<br>kỹ càng từng món.<br> ",
10: "Phải rồi phải rồi! Không bỏ lỡ cơ hội học hỏi là điểm tốt của<br>chú bé đấy.<br> ",
11: "Chú bé vẫn nhớ những lời khôn ngoan của người lùn ta giảng dọc đường chứ?<br> ",
12: "Vật liệu xây dựng‚ lát đường… ta học được nhiều thứ. Biết đâu còn<br>giúp ích cho việc chỉ huy của ta nữa‚ nhưng…<br> ",
13: "Ngài cứ vòng vo và dài dòng quá đi! Không thể nói ngắn gọn hơn chút nào à?<br> ",
14: "Gaah‚ chú bé chẳng hiểu gì cả. Ta làm thế là vì lo cho chú bé‚ muốn<br>truyền hết sự hiểu biết của ta cơ mà!<br> ",
15: "Chính vì thích chú bé‚ ta mới chậm rãi kể cho chú bé nghe. Chú bé<br>không có chút khí chất nào để chiều theo ta một chút sao?<br> ",
16: "Đấy‚ nên ta mới đang chịu đựng ngài chứ gì? Thôi… cũng chẳng phải là<br>ta ghét mấy câu chuyện dài dòng của ngài.<br> ",
17: "Ô hô! Sao thế chú bé‚ cũng biết nói thật lòng đấy chứ! Ừm ừm‚ ngoan<br>lắm! Để ta khen ngợi chú bé!<br> ",
18: "Thôi ngay‚ đừng có kiễng lên xoa đầu ta! Người ta nhìn chúng ta ánh<br>mắt kỳ lạ rồi kìa!<br> ",
19: "Hô hô hô‚ với ta thì chú bé chỉ là một cậu bé dễ thương thôi. Chẳng có gì lạ cả.<br> ",
20: "…Ừm?<br> ",
21: "Có chuyện gì vậy‚ Gemma?<br> ",
22: "Cái nhẫn ở kia kia… chẳng lẽ là…?<br> ",
23: "Tiệm phụ kiện à? Gemma‚ ngài cũng quan tâm đến mấy thứ đó<br>sao?<br> ",
24: "…!<br> ",
25: "…Tại sao?! Sao món này lại được bày bán ở đây chứ?!<br> ",
26: "H-hey? Ngài tìm thấy gì thế‚ Gemma?<br> ",
27: "Gemma nhặt chiếc nhẫn từ trước cửa hàng và nâng nó lên bằng<br>những ngón tay run rẩy.<br> ",
28: "Này‚ anh đang làm cái quái gì đấy?! Món đó là hàng bán mà!<br> ",
29: "Ông là chủ tiệm à? Xin lỗi‚ bọn ta đã tự ý chạm vào nó.<br> ",
30: "Này‚ anh lấy món này ở đâu?! Đây là món đồ độc nhất vô nhị ta<br>tặng cho một người bạn!<br> ",
31: "Ồ‚ ồ? Vậy ra anh là người từng sở hữu nó?<br> ",
32: "Đúng thế! Ta đã nhờ chế tác đặc biệt chiếc nhẫn từ quặng ta đào<br>bằng chính đôi tay này làm quà cưới tặng một người bạn!<br> ",
33: "Ông ấy đã hứa sẽ trân trọng nó mãi mãi…!<br> ",
34: "Gemma…<br> ",
35: "Chủ tiệm‚ ông có thể cho tôi biết chiếc nhẫn đó từ đâu ra không?<br> ",
36: "Tôi lấy từ chính Perdion. Nó bị cầm đồ nên tôi đã mua lại.<br> ",
37: "Bị cầm đồ… ở Perdion… ông nói vậy sao…?<br> ",
38: "Đồ đẹp đấy‚ nhưng hơi đắt một chút nên chẳng bán được‚ tôi nghĩ vậy.<br> ",
39: "Nó bị đưa vào hiệu cầm đồ hơn mười năm trước… hay là tôi nghe thế.<br> ",
40: "Mười năm… xa xưa đến thế sao…?<br> ",
41: "Ngài có ổn không‚ Gemma?<br> ",
42: "…Hô‚ chú bé à. Ngài chưa cần lo cho ta đâu.<br> ",
43: "Ta đã trải qua vô số lần gặp gỡ và chia ly. Ta chỉ hơi<br>ngạc nhiên thôi‚ thế thôi.<br> ",
44: "…Ta hiểu rồi.<br> ",
45: "Cảm ơn ông chủ tiệm nữa. Xin lỗi vì đã làm ồn ào.<br> ",
46: "Không sao đâu‚ nhưng…<br> ",
47: "…Thế thì‚ ta xin phép cáo từ đây.<br> ",
48: "H-hey‚ Gemma?<br> ",
49: "Xin lỗi chú bé. Ta về trước đây. Đồ ta mua để lại cho chú bé–thích<br>làm gì thì làm.<br> ",
50: "Ta nghĩ mình sẽ uống một chén và suy ngẫm về cuộc gặp gỡ hiếm hoi này. Hô hô<br>hô…<br> ",
51: "Gemma… bà ấy cười đấy‚ nhưng lại đang khóc…<br> ",
52: "Ta đã nhận ra hôm nay bà ấy chỉ mua những thứ ta cần. Hóa ra từ<br>đầu bà ấy đã chọn cho ta… bà lão đó…<br> ",
53: "Cô bé đó‚ thuộc chủng tộc trường thọ phải không? Tôi đã nói<br>những điều không nên…<br> ",
54: "Không‚ ông không làm gì sai. Cảm ơn vì đã kể cho tôi nghe.<br> ",
55: "Thế ông không đuổi theo bà ấy sao‚ ông chủ? Tôi nghĩ đàn ông đích<br>thực phải an ủi người phụ nữ đang khóc chứ.<br> ",
56: "Đương nhiên ta sẽ an ủi bà ấy. Nhưng trước đó‚ có thứ ta cần–đúng không?<br> ",
57: "…Hề‚ nếu thế thì tôi giảm giá cho.<br> ",
58: "Ông nhạy bén đấy. Thế‚ chiếc nhẫn Gemma tặng ta này… và cái này nữa‚<br>tôi có thể lấy được không?<br> ",
59: "Ừm‚ đó là món ông muốn à? Tôi có thể giảm giá cho món đắt tiền<br>hơn đấy‚ ông biết không?<br> ",
60: "Không‚ thế này là được. Còn nữa‚ tôi muốn ông cho biết ông đã mua<br>chiếc nhẫn của Gemma ở tiệm nào.<br> ",
61: "(Người bạn ta‚ dù thiếu tiền đến mấy‚ cũng chẳng bao giờ mang quà tặng đi cầm đồ.)<br> ",
62: "(Dù bị ai đó ăn cắp và bán đi‚ nếu nó xuất hiện ở hiệu cầm đồ<br>Perdion thì họ hẳn đã tìm mua lại rồi.)<br> ",
63: "(Thế nghĩa là họ đã giữ lời hứa‚ trân trọng nó suốt đời… trước khi<br>được bán cho chủ sở hữu kế tiếp.)<br> ",
64: "(…Họ đã mất rồi. Hẳn là đã qua đời hơn mười năm trước…)<br> ",
65: "Ta lại mất thêm một người bạn…<br> ",
}

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def preflight():
    raw = EN.read_bytes()
    txt = raw.decode("utf-8-sig")
    lines = txt.splitlines(keepends=True)
    seq = 0
    problems = []
    total_br = 0
    for ln in lines:
        s = ln.rstrip("\r\n")
        if not s.startswith(TEXT_CMDS):
            continue
        seq += 1
        parts = s.split(",", 5)
        cmd = parts[0]
        tf = parts[1] if cmd == "title" else parts[2]
        en_br = tf.count("<br>")
        total_br += en_br
        if seq not in VI_DICT:
            problems.append(f"seq {seq} MISSING from VI_DICT")
            continue
        vi = VI_DICT[seq]
        vi_br = vi.count("<br>")
        if vi_br != en_br:
            problems.append(f"seq {seq} BR MISMATCH en={en_br} vi={vi_br} :: {vi[:60]!r}")
        if "," in vi:
            problems.append(f"seq {seq} ASCII COMMA in VI :: {vi[:60]!r}")
    if seq != len(VI_DICT):
        problems.append(f"SEQ COUNT MISMATCH file_text_records={seq} vi_dict={len(VI_DICT)}")
    print(f"EN text records: {seq}  | total <br> in EN: {total_br}")
    print(f"VI dict entries: {len(VI_DICT)}")
    if problems:
        print("PREFLIGHT PROBLEMS:")
        for p in problems:
            print("  -", p)
        return False
    print("PREFLIGHT OK")
    return True

def build():
    raw = EN.read_bytes()
    txt = raw.decode("utf-8-sig")
    has_crlf = b"\r\n" in raw
    lines = txt.splitlines(keepends=True)
    out = []
    seq = 0
    for ln in lines:
        ending = ln[len(ln.rstrip("\r\n")):]
        s = ln.rstrip("\r\n")
        if not s.startswith(TEXT_CMDS):
            out.append(ln)
            continue
        seq += 1
        parts = s.split(",", 5)
        cmd = parts[0]
        if cmd == "title":
            parts[1] = VI_DICT[seq]
        else:
            parts[2] = VI_DICT[seq]
        new = ",".join(parts) + ending
        out.append(new)
    data = "".join(out)
    if has_crlf:
        data = data.replace("\r\n", "\n").replace("\n", "\r\n")
    blob = b"\xef\xbb\xbf" + data.encode("utf-8")
    VI.write_bytes(blob)
    print(f"WROTE {VI}  (lines kept, text records rewritten={seq})")

if __name__ == "__main__":
    ok = preflight()
    if not ok:
        sys.exit(1)
    build()
