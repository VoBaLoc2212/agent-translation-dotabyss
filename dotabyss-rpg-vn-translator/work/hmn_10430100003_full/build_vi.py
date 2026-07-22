# -*- coding: utf-8 -*-
# Build VI output for hmn_10430100003 (EN-asset-is-English + title-still-JP).
# Sequential record keying (seq = file-order index over text commands).
# CRLF-safe: read bytes -> utf-8-sig -> splitlines(keepends=True) -> rebuild text
# fields, rejoin with '' (no separator). EN <br> count is authoritative.
import sys

EN_PATH = r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100003.txt"
VI_PATH = r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100003.txt"

# VI keyed by sequential record number (1 = title, 2..118 = message in file order).
# message cores must contain (en_br_total - 1) internal <br> so the mirrored suffix
# makes the line's total <br> count equal the EN source (EN-asset-authoritative).
# Internal fullwidth commas (，) -> U+201A (‚).
VI = {
1: "Tổn Thương‚ Phai Màu‚ Rực Sáng",
2: "Tôi đã cõng Gemma trên lưng đi dạo qua những con phố yên tĩnh trong đêm tĩnh lặng.<br>Tiếng reo hò từ phố ăn chơi xa xa đã lấn át bước chân của tôi.",
3: "Hừm… Ồ…? Cái gì thế này‚ cậu nhóc…?",
4: "Thức rồi à‚ Gemma? Chắc chắn là người lùn tửu lượng cao thật‚ nhưng dạo này cậu<br>uống hơi quá đấy.",
5: "Hô hô hô‚ bọn ta xử lý rượu nhanh mà‚ cậu biết chứ. Chút rượu này thì<br>chẳng là cái thá gì.",
6: "Nào‚ lập tức hạ ta xuống đi.",
7: "Rồi rồi‚ biết rồi.",
8: "Gemma rời khỏi lưng tôi và bắt đầu bước đi với dáng hơi loạng choạng.",
9: "Vẫn còn hơi xỉn nhỉ. Này cậu nhóc‚ ở lại với ta một lát đi. Đó là việc của<br>một người trẻ tuổi mà…",
10: "Đi theo hầu một bà lão sao? Tôi hiểu mà.",
11: "Ừm‚ ngoan đấy. Đến ghế đá kia ngồi mát một lát nhé.",
12: "...Cậu còn nhớ chiếc nhẫn chúng ta thấy ở thị trấn này không?",
13: "Cái mà cậu tặng bạn làm quà cưới đúng không? Tôi đương nhiên là<br>nhớ chứ.",
14: "Nói thật thì‚ tôi đã nghi chiếc nhẫn đó rồi sẽ có ngày được bán đi.",
15: "Sao lại thế? Nó là món quà tặng bạn cơ mà?",
16: "Bọn họ thì hiền quá mức đi‚ tôi chẳng nghĩ họ lại là kiểu người<br>biết tích trữ của cải.",
17: "Dù bản thân họ có giữ lại đi nữa‚ tôi cũng nghĩ rồi sẽ có người<br>đổi nó thành tiền.",
18: "À‚ chuyện đó đành chịu thôi. Kẻ kiếm được tiền lớn chỉ toàn là<br>lũ ác đảng như tôi mà.",
19: "Hahaha! Nói hay lắm‚ thằng tốt bụng này.",
20: "Này‚ Gemma. Nếu cậu muốn nghe thì nghe cũng được‚ nhưng…",
21: "Tôi đã liên lịch với một tiệm cầm đồ ở Perdion về những người cậu đã tặng chiếc nhẫn đó‚ và nắm được<br>câu chuyện đầy đủ.",
22: "Hả… cái gì cơ……? Ý cậu là một tiệm cầm đồ chuyên nghiệp lại đi lạy làng kể lể<br>thông tin khách hàng của họ à?",
23: "Đúng vậy‚ khi tôi hỏi thì họ chẳng thèm trả lời. Nhưng tôi đây có quyền lực mà‚<br>cậu biết chứ.",
24: "Cậu cứ cảm ơn một người bạn hay giúp đỡ mà cũng hay lên mặt của tôi đi.",
25: "Felicione‚ cô gái đó… Tôi cứ bảo cô ta nghĩ đến địa vị của mình đi‚ thế mà.",
26: "Cô ấy đâu có làm gì sai. Lần này coi như được mà‚ đúng không? Thế‚ cậu có<br>muốn nghe không?",
27: "Ừm‚ tôi thực sự có hơi tò mò thật. Để tôi nghe từ chính cậu nhóc kể ra.",
28: "Hình như đó là một tiệm cầm đồ có tiếng. Họ lưu trữ rất cẩn thận thông tin<br>những món đã mua.",
29: "...Theo như lai lịch ghi lại‚ đó là kỷ vật của người cha mẹ đã mất vì<br>bệnh tật.",
30: "Hóa ra là thế sao…",
31: "Và hình như họ cũng là do hoàn cảnh éo le mới đành bán nó. Trong ghi chú có ghi là<br>vẫn có khả năng sẽ mua lại.",
32: "Ra thế‚ ra thế. Ừm ừm‚ hợp lý đấy. Cảm ơn cậu nhóc.",
33: "...Đừng quá buồn. Nó được giữ gìn đến mức có thể đem bán lại‚ chắc chắn là bằng chứng<br>họ chưa từng quên tình bạn với cậu.",
34: "Không không‚ đừng hiểu lầm. Tôi chẳng hề bận tâm việc nó bị bán cho<br>tiệm cầm đồ đâu.",
35: "Nếu nó trở thành của nuôi cho con cháu họ thì tôi cũng<br>chẳng sao cả.",
36: "Đó là bản chất của trang sức. Cứ truyền lại kèm lời dặn rằng lúc túng quẫn thì<br>đem bán đi.",
37: "...Người bạn của ta đã trân trọng chiếc nhẫn ấy cả đời‚ và trao lại nó với niềm tin rằng nó sẽ giúp ích<br>cho con cái mình.",
38: "Với tư cách người tặng‚ điều đó khiến tôi vui. Cảm giác như con cái của bạn tôi đã đến nhờ cậy<br>tôi vậy.",
39: "Chiếc nhẫn ấy đã hoàn thành vai trò của nó thật tốt. Tôi muốn tán dương nó quá.",
40: "...Thế thì để nó kể cho cậu nghe những câu chuyện kỷ niệm đi. Này.",
41: "—Chàng đưa chiếc nhẫn đã chuộc lại vào tay Gemma.",
42: "Cậu nhóc… cậu đã chuộc nó lại từ tiệm đó à.",
43: "Đương nhiên. Tôi làm sao để mặc kệ nó thành hàng bày được.",
44: "Chiếc nhẫn lặn lội đến tận chốn này chính là để cậu tìm thấy nó. Tôi<br>chắc chắn là vậy.",
45: "...Hô hô‚ có lẽ thế thật. Tôi sẽ nâng niu giữ hộ nó vậy.",
46: "Gemma nhìn chằm chằm vào chiếc nhẫn trên lòng bàn tay như thể đó là thứ quý giá. Dưới ánh sáng của những vì sao‚<br>chiếc nhẫn tỏa ra ánh sáng dịu dàng.",
47: "Ngoài ra‚ tôi nghĩ tặng phụ kiện cho bạn bè là một phong tục hay. Và tôi cũng có một món quà cho cậu đấy‚ Gemma‚<br>vì cậu đã giúp đỡ tôi nhiều.",
48: "Quà từ cậu nhóc à? Tặng tôi sao?",
49: "Ừ‚ là nó đây. Cầm lấy đi.",
50: "Tôi đặt một chiếc khuyên tai cũ kỹ‚ bạc màu lên lòng bàn tay Gemma‚ bên cạnh chiếc nhẫn đang<br>rực rỡ sáng ngời.",
51: "Cái này… không phải món đồ tồi‚ nhưng nó đã rất cũ. Màu sắc cũng bạc đi‚ lại có vết trầy và<br>sứt mẻ…",
52: "Nếu cậu tặng tôi thì tôi xin vui vẻ nhận. Nhưng sao cậu lại<br>chọn cái này…?",
53: "Thì‚ tôi nghĩ nó hợp với cậu mà. Này‚ để tôi đeo cho.",
54: "Ừ‚ trông cậu đeo vào đẹp thật đấy.",
55: "Hợp với tôi cơ à? Cái đồ cũ rích mang tiếng tích này sao……?",
56: "Cậu nghĩ thứ như thế là đủ tốt cho kẻ như tôi sao‚ cậu nhóc…?",
57: "...Ừ thì‚ một viên đá quý được cất giữ cẩn thận thì đẹp hơn món đồ đã mòn và mang đầy vết sẹo vì dùng lâu như thế này‚<br>đúng không.",
58: "Nhưng tôi là Chỉ Huy. Tôi chẳng tin nổi một binh sĩ chưa từng chiến đấu<br>lần nào.",
59: "Cứ tiếp tục chiến đấu ở tiền tuyến‚ rồi cậu sẽ bị bào mòn‚ mang thương tích‚<br>bạc màu…… Nhưng chính lịch sử đó mang lại sức mạnh‚ và vẻ đẹp tỏa sáng vì thế.",
60: "Đó là thứ tôi yêu.",
61: "Tôi cứ nghĩ cậu cũng chẳng ghét mấy thứ kiểu này đâu‚ Gemma. Tôi nhầm sao?",
62: "…",
63: "Gemma khẽ chạm vào khuyên tai và né ánh mắt khỏi<br>Chỉ Huy.",
64: "Cậu đang nói tôi cũng giống như thứ này sao?",
65: "Thế nhé. Cậu muốn nghĩ sao thì nghĩ.",
66: "...Thật tình‚ cậu nhóc này láo xược quá. Nhưng mà—",
67: "À‚ tôi không ghét đâu. Tôi yêu cậu đấy.",
68: "Chúng ta hợp gu đấy nhỉ. Vậy thì‚ cậu cứ dùng nó bất cứ khi nào thích.",
69: "Có bảo tôi cũng chẳng khác.",
70: "Haa‚ chà chà! Cậu nhóc này chỉ giỏi mỗi mấy lời đường mật thôi!",
71: "Sao thế‚ cậu tưởng tôi đang tán tỉnh cậu à?",
72: "Ự! Đừng có trêu người lớn tuổi! Nói mấy lời ngọt ngào rồi bỏ chạy‚ đó là chuyện<br>nhục nhã nhất đấy!",
73: "T-tôi đâu có định bỏ chạy đâu!",
74: "Hô hô? Thế để tôi nhắc lại từ đầu những lời cậu vừa nói nhé?",
75: "Thôi thôi! Này‚ cậu đã tỉnh rượu rồi‚ câu chuyện kết thúc ở đây. Mau<br>quay về thôi!",
76: "...Này‚ cậu nhóc.",
77: "Gì thế.",
78: "...Đừng có chết.",
79: "Hả…… Gemma……?",
80: "Không‚ tôi chẳng dám mong thế. Cậu cũng chẳng sống thọ hơn tôi được đâu‚ cậu nhóc.",
81: "Nhưng ít nhất hãy chết trước mặt tôi. Tôi không chịu nổi cảnh cậu mất ở nơi xa xôi mà tôi không hề<br>hay biết.",
82: "Tôi muốn nhìn cậu ra đi và khóc‚ cậu nhóc. Hãy để tôi tiễn biệt cậu.",
83: "Đây là lời request của một bà lão. Xin cậu‚ hãy hứa với tôi đi‚ cậu nhóc.",
84: "Đôi mắt Gemma như bám lấy anh. Trước mặt cô‚ anh từ từ<br>lắc đầu.",
85: "...Xin lỗi‚ nhưng chuyện đó tôi không thể hứa được.",
86: "Tại sao chứ‚ cậu nhóc……!",
87: "Ở Tiền Tuyến Căn Cứ đang chống lại Tai Ương này‚ mà đòi chọn cách mình chết thì<br>quá ngạo mạn.",
88: "Một trận giao chiến bất ngờ‚ một cuộc xâm lăng từ Đại Huyệt‚ hay không kìm được Tai Ương――. Tôi chết ở đâu<br>chẳng có gì lạ.",
89: "Có lẽ thế…… Nhưng mà‚ tôi…",
90: "Chỉ là——tôi sẽ chiến đấu đến cùng. Cho đến ngày tôi và đồng đội có thể chọn được<br>cách mình chết.",
91: "Cậu nhóc…",
92: "Vậy nên Gemma‚ cậu cũng giúp tôi đi. Hãy dùng hết kỹ năng‚ trí tuệ‚ tấm lòng và toàn bộ sức mạnh cậu có để<br>hỗ trợ tôi.",
93: "Thế thì khi tôi an nhiên qua đời trên chiếc giường lớn trong dinh thự xa hoa‚ được gia đình vây quanh‚<br>tôi sẽ gọi cả cậu nữa.",
94: "…",
95: "Fufu‚ hô hô hô‚ fwa fwa fwa!",
96: "Vừa bảo chọn cái chết là ngạo mạn‚ thế mà cậu lại vẽ ra một giấc mơ xa hoa thế đấy à‚<br>thằng nhóc này!",
97: "Được thôi được thôi! Tôi nhất định sẽ có mặt bên giường bệnh cậu và hỏi xem đó có phải là<br>lý tưởng của cậu không!",
98: "Và tôi sẽ nắm chặt khuyên tai này mà khóc nức nở! Cậu hãy hối hận vì đã chết bỏ lại tôi<br>mà!",
99: "Cậu đúng là kẻ ích kỷ… Thôi‚ mức đó thì cũng được.",
100: "Thế thì là lời hứa nhé. Hãy sống để chứng kiến cái chết của tôi đi‚ Gemma.",
101: "Ừ‚ tôi sẽ sống tiếp. Vì một cậu nhóc ngạo mạn như cậu.",
102: "Nói về Gemma… có vẻ cô ấy đã ổn hơn rồi.",
103: "Ra thế. Nếu cô ấy đã vui lên thì tốt quá.",
104: "Làm được thế này so với cậu thì cũng giỏi đấy. Giỏi lắm‚ ta khen ngợi cậu.",
105: "Nói năng gì mà bề trên thế. Cậu tưởng mình là ai chứ……",
106: "...? Ta đây là hoàng nữ mà.",
107: "Ra là thế nhỉ! Mà ngược lại‚ được nhận lời khen trực tiếp như vậy khiến tôi thấy hơi vinh dự đấy!",
108: "Đúng thế. Một người Perdion mà nghe được thì khóc vì vui mừng ấy chứ.",
109: "Dù vậy thì nghe cũng đáng ngờ thật…",
110: "Nhưng có một chuyện tôi tò mò. Gemma thỉnh thoảng lại lấy thứ gì đó ra‚<br>ngắm nghía nó thật trân trọng.",
111: "Cái đó…… là gì vậy?",
112: "À‚ chẳng phải món gì ghê gớm. Chỉ là một món đồ hư hại có chút lịch sử.",
113: "Chỉ là—",
114: "Ồ‚ cô Gemma. Chiếc khuyên tai này stylish đấy nhỉ. Dù không phải mốt hiện nay‚ nhưng chính vì thế mà<br>nó có nét riêng.",
115: "Đúng không? Gu ăn mặc của tôi cũng chẳng tệ đâu nhỉ.",
116: "Nhưng mà…… có vẻ nó hơi bị sứt một chút. Cô có muốn nhờ người chế tác lại<br>không?",
117: "Hô hô hô‚ tôi cứ giữ nguyên thế này là được rồi.",
118: "Tôi cứ không thể không thích những thứ kiểu này—cả cậu nhóc và tôi đều vậy‚<br>cậu biết mà.",
}

TEXT_CMDS = ("message,", "title,", "messageTextUnder,", "messageTextCenter,")

def main():
    raw = open(EN_PATH, "rb").read()
    text = raw.decode("utf-8-sig")
    en_lines = text.splitlines(keepends=True)
    out = []
    seq = 0
    errors = []
    for ln in en_lines:
        stripped = ln.rstrip("\r\n")
        is_text = any(stripped.startswith(c) for c in TEXT_CMDS)
        if not is_text:
            out.append(ln)
            continue
        seq += 1
        if seq not in VI:
            errors.append(f"seq {seq} missing in VI dict")
            out.append(ln)
            continue
        vi = VI[seq]
        if stripped.startswith("title,"):
            en_br = 0
            new_line = "title," + vi
        else:
            parts = stripped.split(",")
            old_tf = parts[2]
            suffix = "<br> " if old_tf.endswith("<br> ") else ""
            en_br = old_tf.count("<br>")
            parts[2] = vi + suffix
            new_line = ",".join(parts)
        if "," in vi:
            errors.append(f"seq {seq}: ASCII comma in VI -> {vi!r}")
        if stripped.startswith("message,"):
            new_br = new_line.count("<br>")
            if new_br != en_br:
                errors.append(f"seq {seq}: <br> mismatch vi={new_br} en={en_br} :: {vi!r}")
        out.append(new_line + ln[len(ln.rstrip("\r\n")):])
    if len(out) != len(en_lines):
        errors.append(f"line count changed: {len(out)} vs {len(en_lines)}")
    if seq != 118:
        errors.append(f"seq total {seq} != 118")
    if len(VI) != 118:
        errors.append(f"VI dict size {len(VI)} != 118")
    if errors:
        sys.stderr.write("PREFLIGHT FAILED:\n" + "\n".join(errors) + "\n")
        sys.exit(1)
    data = "".join(out)
    open(VI_PATH, "wb").write(b"\xef\xbb\xbf" + data.encode("utf-8"))
    sys.stderr.write(f"WROTE {VI_PATH}: {seq} text records, {len(out)} lines\n")

if __name__ == "__main__":
    main()
