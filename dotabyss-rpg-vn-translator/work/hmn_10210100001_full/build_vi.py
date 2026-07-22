#!/usr/bin/env python3
# Build VI asset for hmn_10210100001 from EN asset (structural authority),
# translating JP->VI only in text fields. JP primary, EN alignment.
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10210100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10210100001.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10210100001_full"
WORK.mkdir(parents=True, exist_ok=True)

# VI translations in exact order of text-command appearance (1 title + 68 messages)
VI_TEXT = [
    # [1] title
    "Sức Mạnh Tinh Linh Nước!",
    # [2] <user>
    "...Hôm nay bỗng dưng có nhiều gã trai vạm vỡ thế nhỉ. Chưa có báo cáo nào về<br>quái vật‚ nhưng...<br> ",
    # [3] <user>
    "Bọn họ hình như không có ác ý‚ nên chắc không có gì đáng lo đâu...<br>Ơ?<br> ",
    # [4] ？？？
    "Nào‚ đến giờ ăn rồi! Ăn thật nhiều vào nhé?♪<br> ",
    # [5] <user>
    "Đó là người mới đến Căn Cứ Tiền Tuyến gần đây... Chính là<br>Humena‚ đúng không? Đã đến đây rồi‚ chắc mình sẽ bắt chuyện với cô ấy.<br> ",
    # [6] <user>
    "Này‚ Humena!<br> ",
    # [7] ヒュメナ
    "Hửm? À‚ Chỉ Huy. Chào anh.<br> ",
    # [8] <user>
    "Ừ. Đây là lần đầu chúng ta thực sự nói chuyện đấy. Đã quen với cuộc sống<br>ở đây chưa? Có chuyện gì phiền lòng cứ nói ta biết nhé.<br> ",
    # [9] ヒュメナ
    "Fufu‚ cảm ơn anh. Nhưng nhờ có anh mà em ổn cả rồi.<br> ",
    # [10] ヒュメナ
    "Mọi người ở căn cứ đều tốt bụng‚ và chúng ta là đồng đội cùng chiến đấu bên nhau!♪<br> ",
    # [11] <user>
    "Ra thế‚ tốt quá. Thế đang làm gì đấy? Đang cho cô ấy ăn à?<br> ",
    # [12] ヒュメナ
    "Ừm! Em đang cho Upa-chan ăn mà!♪<br> ",
    # [13] ヒュメナ
    "Nào‚ Upa-chan‚ chào Chỉ Huy đi nào!<br> ",
    # [14] ウパ
    "Upa!<br> ",
    # [15] <user>
    "Ủa! Con đó là cá cơ à‚ mà lại kêu được?<br> ",
    # [16] ヒュメナ
    'Ừ! Vì nó kêu ""Upa! Upa!""‚ nên em gọi nó là Upa-chan! Nhìn có<br>dễ thương không?♪<br> ',
    # [17] <user>
    "Á‚ ừ... Nó đẹp một cách kỳ lạ thật. Loài sinh vật gì vậy?<br> ",
    # [18] ヒュメナ
    "...Ngài đã hỏi đúng câu hỏi rồi đó!<br> ",
    # [19] <user>
    "O-ơ!<br> ",
    # [20] ヒュメナ
    "Upa-chan không chỉ là một con cá bình thường đâu! Nó là tinh linh nước phục<br>vụ em‚ một nữ tu sĩ của Thủy Thần!<br> ",
    # [21] ヒュメナ
    "Vậy nên để đền đáp‚ em dùng bí thuật của giáo hội để làm một cái bể<br>thật thoải mái cho Upa-chan! Á‚ đây chính là cái bể đó!<br> ",
    # [22] ヒュメナ
    "Cái bể này trông bên ngoài tuy nhỏ‚ nhưng bên trong thực ra lại<br>rộng thật sự—Á‚ không‚ không‚ không phải thế! Giờ em phải giới thiệu Upa-chan đã!<br> ",
    # [23] ヒュメナ
    "Ưm‚ ưm‚ dù sao thì‚ Upa-chan với em thân thiết lắm‚ lúc nào<br>cũng ở bên nhau‚ và nó thì đáng yêu quá‚ quá đi!<br> ",
    # [24] ヒュメナ
    "Trước hết‚ má phúng phính với đôi mắt tròn xoe này! Nhìn đáng yêu đến mức em<br>chịu không nổi‚ đúng không?<br> ",
    # [25] <user>
    "(Cô ấy nói nhanh quá trời! Em chẳng kịp chen lời nào!)<br> ",
    # [26] <user>
    "(Thôi thì‚ chắc cô ấy là kiểu người nói nhiều khi được hỏi về thứ<br>mình thích... Thôi cứ nghe cho đến khi cô ấy thỏa mãn vậy.)<br> ",
    # [27] ヒュメナ
    "Đương nhiên không chỉ đáng yêu thôi! Vảy sáng lấp lánh với làn da mịn màng thật<br>đẹp‚ rồi vây với mang nom cũng khỏe khoắn và ngầu nữa—!<br> ",
    # [28] ヒュメナ
    "Rồi... à... ư‚ ưm...<br> ",
    # [29] <user>
    "...Sao thế? Nói tiếp đi.<br> ",
    # [30] ヒュメナ
    "Ơ‚ ưm... Em nói một mình quá nhiều rồi phải không...<br>Ahaha!<br> ",
    # [31] <user>
    "Không‚ ta chẳng phiền chút nào. Ta đến bắt chuyện vì muốn nghe về<br>chuyện kiểu này mà.<br> ",
    # [32] <user>
    "Muốn hiểu về em‚ thì hỏi những thứ em thích là cách<br>tốt nhất‚ đúng không?<br> ",
    # [33] ヒュメナ
    "Chỉ Huy... Ừ‚ anh là một người tốt bụng đấy!<br> ",
    # [34] <user>
    "Cái gì thế? Nãy còn nói chuyện như trẻ con‚ giờ lại<br>coi ta như trẻ con à?<br> ",
    # [35] ヒュメナ
    "Trời ơi‚ em bảo đừng nói vậy mà!<br> ",
    # [36] ？？？
    "Ồ kìa‚ kỷ lục mới đây: 37 viên ngói!<br> ",
    # [37] 歓声
    "Hoooooooo!<br> ",
    # [38] ヒュメナ
    "...? Hình như bên đó đang náo nhiệt lên. Đó là bãi huấn luyện<br>phải không? Không biết đang làm gì thế nhỉ?<br> ",
    # [39] ヒュメナ
    "Này‚ này. Đi xem thử xem sao‚ Chỉ Huy!<br> ",
    # [40] <user>
    "Ừ‚ em nói đúng.<br> ",
    # [41] 前線基地の兵士A
    "Nào‚ ai khác muốn thử sức không!<br> ",
    # [42] <user>
    "Này‚ ở đây đang làm gì vậy?<br> ",
    # [43] 前線基地の兵士A
    "Thưa Chỉ Huy! Thực ra chúng tôi đang tổ chức một giải đấu xem<br>ai đập vỡ được nhiều viên ngói nhất!<br> ",
    # [44] 前線基地の兵士A
    "Đây là cuộc thử sức truyền thống của Hầu Lai—đập ngói. Rất nhiều<br>binh sĩ và kẻ lực lưỡng đã tụ tập về cả!<br> ",
    # [45] <user>
    "Ra thế... Thì ra lũ đàn ông vạm vỡ tụ tập quanh đây là vì chuyện này.<br> ",
    # [46] ヒュメナ
    "Hơ‚ nghe có vẻ vui đấy. Sao anh không thử luôn một phen‚ Chỉ Huy?<br> ",
    # [47] <user>
    "Ta thiên về trí tuệ hơn. Có đập cũng chẳng vỡ nổi một viên<br>mà chỉ chuốc lấy thương tích thôi.<br> ",
    # [48] ヒュメナ
    "Hmm... Thế thì‚ để em tham gia thay anh nhé?<br> ",
    # [49] <user>
    "Humena? Em là nữ tu sĩ mà‚ đúng không? Em chắc chắn đó là ý hay<br>đấy chứ?<br> ",
    # [50] ヒュメナ
    "Tất nhiên! Có vài tinh linh nước sức mạnh khủng khiếp‚ và em luôn<br>nhờ bọn họ cùng luyện tập!<br> ",
    # [51] <user>
    "Ta chưa từng hình dung tinh linh nước lại mạnh đến thế...<br> ",
    # [52] ヒュメナ
    "Ô‚ anh không tin em à? Được rồi‚ để em cho anh thấy sức mạnh của<br>tinh linh nước!<br> ",
    # [53] ヒュメナ
    "Rõ! Em sẽ nhận thử thách!<br> ",
    # [54] 前線基地の兵士B
    "Này‚ này‚ cô chắc chắn đấy à‚ cô nương? Đống ngói này không dễ đập vỡ đâu với<br>người mới bắt đầu đâu.<br> ",
    # [55] 格闘家
    "Cô nghĩ có đập vỡ được kỷ lục 37 viên của tôi không? Thôi‚ tôi nghi ngờ lắm!<br>Hahaha!<br> ",
    # [56] 前線基地の兵士B
    "Thôi‚ chỉ cần đừng để bị thương là được‚ nhé?<br> ",
    # [57] ヒュメナ
    "Cứ giao cho em! Em sẽ cho anh thấy một cái gì đó tuyệt vời!<br> ",
    # [58] ヒュメナ
    "Được rồi‚ em bắt đầu nhé!<br> ",
    # [59] (narration, empty name)
    "Humena đứng trước chồng ngói xếp chồng và từ từ giơ tay lên. Rồi<br>...<br> ",
    # [60] ヒュメナ
    "HAAAA—!<br> ",
    # [61] (narration, empty name)
    "Một tiếng nổ âm thanh‚ chẳng giống đập ngói chút nào‚ vang vọng khắp<br>khu vực! Khi chấn động lắng xuống‚ thứ nằm ở đó là...<br> ",
    # [62] 前線基地の兵士A
    "Tất cả... đều vỡ tan...<br> ",
    # [63] 前線基地の兵士B
    "Không đùa chứ! Có tận một trăm viên xếp chồng mà!<br> ",
    # [64] 格闘家
    "S-sức mạnh kinh hoàng thế...!<br> ",
    # [65] <user>
    "(Sức mạnh của cô ấy quả đáng nể‚ nhưng không chỉ có thế. Kỹ thuật‚ tốc độ‚<br>và sự quyết tâm. Tâm‚ kỹ‚ thân—đó mới là cái tạo nên kết quả.)<br> ",
    # [66] ヒュメナ
    "Chỉ Huy‚ anh thấy rồi đúng không?<br> ",
    # [67] <user>
    "Ừ‚ thú thật ta không ngờ em lại làm tới mức đó.<br> ",
    # [68] ヒュメナ
    "Fufufu! Đó là sức mạnh của tinh linh nước!<br> ",
    # [69] <user>
    "(Thế này thì đúng là một đồng minh đáng tin cậy...)<br> ",
]

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAG_RE = __import__("re").compile(r"<[^>]+>")

# sanity: no ASCII comma in any VI text field
for i, t in enumerate(VI_TEXT, 1):
    assert "," not in t, f"ASCII comma in VI#{i}: {t!r}"

data = EN.read_bytes()
text = data.decode("utf-8-sig")
assert data.startswith(b"\xef\xbb\xbf"), "EN missing BOM"
has_crlf = b"\r\n" in data
lines = [ln.rstrip("\r") for ln in text.split("\n")]

# load JP source for diff
ja = json.loads((ROOT / "dotabyss-translation-main/translations/novels/hmn_10210100001/ja.json").read_text(encoding="utf-8-sig"))
# build ordered JP text list aligned to en message order via ja.json values (same order as file lines)
import re as _re
# Extract JP text fields from EN asset lines by mapping to ja.json keys is unreliable; instead
# we capture JP per text line from the ja.json in file order (keys appear in order).
ja_ordered = list(ja.values())  # ja.json keys == values here; preserve insertion order

idx = 0
out_lines = []
diff_rows = []
for ln in lines:
    if ln.startswith(TEXT_CMDS):
        idx += 1
        vi = VI_TEXT[idx - 1]
        if ln.startswith("title,"):
            new = "title," + vi
            # title has no trailing space convention issue
            out_lines.append(new)
            diff_rows.append((idx, "title", ja_ordered[0] if ja_ordered else "", vi))
            continue
        parts = ln.split(",", 2)
        cmd, name = parts[0], parts[1]
        rest = parts[2] if len(parts) > 2 else ""
        if rest.count(",") == 0:
            textfield, suffix = rest, ""
        else:
            rp = rest.split(",")
            textfield, suffix = rp[0], "," + ",".join(rp[1:])
        # verify tag parity before replacing
        assert TAG_RE.findall(textfield) == TAG_RE.findall(vi), f"TAG mismatch line {idx}:\n EN={textfield}\n VI={vi}"
        new = cmd + "," + name + "," + vi + suffix
        out_lines.append(new)
        jp = ja_ordered[idx - 1] if idx - 1 < len(ja_ordered) else ""
        diff_rows.append((idx, name, jp, vi))
    else:
        out_lines.append(ln)

assert idx == len(VI_TEXT), f"text line count {idx} != vi {len(VI_TEXT)}"

out = "\r\n".join(out_lines)
if out.endswith("\r\n"):
    pass
VI.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
print("WROTE", VI, "lines:", len(out_lines), "text_records:", idx, "crlf:", has_crlf)

# write focused diff
md = ["# Focused Diff — hmn_10210100001", "",
      "JP primary, EN alignment. Structural fields (cmd, speaker name, IDs, tags, delimiters, BOM/CRLF) preserved; internal commas → U+201A ‚.", "",
      "| # | Speaker | JP (source) | VI (output) |", "|---|---|---|---|"]
for n, name, jp, vi in diff_rows:
    md.append(f"| {n} | {name} | {jp} | {vi} |")
(WORK / "focused_diff.md").write_text("\n".join(md), encoding="utf-8")
print("WROTE focused_diff.md rows:", len(diff_rows))
