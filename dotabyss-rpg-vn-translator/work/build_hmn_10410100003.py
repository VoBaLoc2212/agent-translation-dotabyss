# -*- coding: utf-8 -*-
"""Build VI output for hmn_10410100003.

EN-asset-is-English case (en.json holds English; ja.json == identity map).
All text fields already hold English -> translate EN->VI.
`title,` field is still JP (本当の笑顔で) -> translate JP->VI Title Case.
Structural authority = EN asset (delimiters, BOM, CRLF, <br> count, <size> cards).
Per field:
  - title,            : VI at field index 1 (no <br> suffix mirror)
  - message,          : VI at field index 2, then mirror the source trailing "<br> " suffix
  - messageTextCenter,: VI at field index 2, preserve parts[3:] (e.g. ,,,on)
Field 1 (speaker label) preserved byte-identical (JP keys / <user>).
ALL trailing parts[3:] are preserved so delimiter/field/tag counts match EN.

Addressing matrix (Ayame trust event):
  - Ayame (アヤメ, female subordinate secretary/assassin): self "em"; addresses Commander
    as "Chỉ Huy" (title) and respectful "Ngài" where EN says "you ... Lord Commander".
  - Commander (<user>, male, 俺): self "anh"; addresses Ayame as "em".
  - Guard soldier (倉庫警備の兵士, male subordinate): self "tôi"; addresses Commander "Chỉ Huy".
  - Monster SFX localized: groooaaar/GROOOAAARRR -> Gừư!/Gừưư!; gyaaaaaa -> Giáaaa...;
    bang! -> Bùm!/Bùm! Bùm! Bùm!/*bùm!*; Wha -> Á; *phew* -> *thở phào*; Ahem -> Khụ khụ.
  - "Calamity" -> "Tai Họa" (project convention, hmn_10400100003).
  - All commas inside VI text use U+201A '‚' (ASCII comma forbidden in text fields).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10410100003.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10410100003.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10410100003_full"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
SUF_RE = re.compile(r"(?:<br>\s*)+$")

# line_no -> VI text field (inner text; EN <br> counts already match source)
VI: dict[int, str] = {
    29: "Nụ Cười Chân Thật",
    64: "Gừư!",
    100: "Á‚ aaaaaaah!",
    160: "Xin lỗi ạ.",
    180: "Bùm!",
    233: "Giáaaa...",
    303: "Ufufu. Cảm ơn Chỉ Huy đã vất vả với việc mồi nhử và đánh lạc hướng.",
    358: "Gừư!",
    408: "Không‚ tôi không muốn chết‚ tôi không muốn chết!",
    509: "Bùm! Bùm! Bùm!",
    542: "Giáaaa...",
    595: "<size=48>—Vài Giờ Sau Đó.</size>",
    638: "Á‚ á... tôi sống rồi‚ tôi sống rồi...",
    640: "Hứ‚ anh sống sót được rồi à. Gã may mắn. Thôi‚ được‚ lần này anh tha cho<br>ngươi.",
    651: "C-cảm ơn Chỉ Huy! Tôi sẽ không bao giờ biển thủ vật tư nữa!",
    653: "Đương nhiên. Đừng nghĩ sẽ có lần hai. ...Bọn anh có việc‚<br>anh đi trước đi.",
    662: "T-tôi xin phép cáo lui!",
    718: "Chỉ Huy thật là tốt bụng.",
    720: "Hắn sẽ chẳng phản bội anh nữa đâu. Anh đã gieo đủ nỗi sợ và ơn nghĩa<br>để hắn mang ơn.",
    722: "Không cần giết hắn làm gì. Hắn vẫn còn dùng được.",
    733: "...Vâng‚ đúng vậy. Từ nay hắn sẽ không làm phiền Chỉ Huy nữa.",
    735: "Thế là xong chuyện. Vậy‚ còn việc giết chóc thì sao?",
    746: "Vâng‚ em đã dọn sạch mọi chướng ngại chắn đường. Không có vấn đề gì<br>cả‚ Chỉ Huy.",
    748: "Làm tốt lắm. Giờ‚ theo khảo sát trước‚ phía trước...",
    785: "Tuyệt‚ đúng là kho báu chúng ta đã đoán! Thu hoạch khá đấy!",
    824: "Cảm ơn Chỉ Huy. Em rất vui vì đã có ích cho Chỉ Huy.",
    826: "Anh thấy ổn‚ nhưng em có bị thương hay gì không?",
    838: "Không‚ tất nhiên là không.",
    849: "Thế nhưng‚ giết thứ không phải con người lại là một trải nghiệm<br>khá mới mẻ.",
    851: "...Vậy là em chán truy đuổi con người rồi?",
    863: "Đây là công việc của em‚ nên em chẳng bao giờ chán. Nhưng em cũng chẳng<br>mấy hứng thú với việc giết người.",
    865: "Ra là vậy... Em là một loại sát thủ hiếm có đấy‚ Ayame.",
    876: "Nghề chính của em là thư ký‚ nên bị gọi là sát thủ khiến em hơi<br>bối rối.",
    878: "Không phải ý anh thế. Những sát thủ anh nghĩ tới là loại người<br>biến thái hơn.",
    889: "Biến thái‚ Chỉ Huy nói vậy sao?",
    891: "Ừ‚ hoặc như cỗ máy vô cảm‚ hoặc ngược lại‚ bị cảm xúc<br>chi phối.",
    893: "Một sát thủ như em‚ điềm tĩnh‚ lúc nào cũng mỉm cười và dễ gần<br>dù có hơi lơ đãng‚ thật hiếm có.",
    904: "Em hân hạnh được khen... Em vui về chuyện này thì được chứ‚<br>đúng không?",
    906: "Anh không phiền. Nhưng chỉ khi nụ cười đó là thật‚ nhớ đó.",
    918: "Nụ cười lúc nào cũng có trên môi của em làm Chỉ Huy không vui sao?",
    920: "Không phải vậy. Anh chỉ nghĩ đó không phải nụ cười thật của em.",
    922: "Nơi này tôn vinh kỹ năng giết người‚ nhưng nhiều kẻ lại vất vả<br>mới làm được kiểu người đó.",
    924: "Nếu em núp sau nụ cười‚ kìm nén sự ghê tởm khi đoạt mạng<br>người...",
    926: "Em có thể bỏ nghề sát thủ mà làm thư ký<br>bình thường. Chẳng ai trách em vì lựa chọn đó đâu.",
    940: "Á... em phải làm sao đây?",
    953: "Chỉ Huy‚ Ngài luôn xem trọng cảm xúc của em và nghĩ cho em nhiều thế...",
    964: "Em vui lắm‚ Chỉ Huy. Vâng‚ rất...",
    966: "Anh không chiều chuộng em đâu. Dùng thuộc cấp cho đúng cách là bổn<br>phận của một Chỉ Huy.",
    977: "Ufufu‚ em hiểu rồi. Sự quan tâm chu đáo của Chỉ Huy.",
    988: "Nhưng‚ em xin lỗi‚ em cũng chẳng ghét giết người đến thế...",
    990: "Là... vậy sao?",
    1002: "Lúc đầu‚ chỉ là để kiếm sống. Em thấy hơi<br>lạ‚ nhưng chẳng có nghề nào trả cao khác em có thể làm...",
    1009: "Nhưng nếu cố gắng‚ em rồi cũng tìm thấy sự thỏa mãn.",
    1011: "Nhưng chắc hẳn đã có lúc em giết kẻ mình không<br>muốn giết‚ đúng không?",
    1023: "Dĩ nhiên‚ có những trải nghiệm khó chịu. Nhưng đó chỉ là một phần<br>của bất kỳ công việc nào thôi‚ phải không?",
    1034: "Dù chuyện chẳng vui xảy ra‚ em cũng nhẫn nhịn vì đó là<br>công việc. Cô hầu bàn và lính tráng cũng vậy‚ phải không?",
    1046: "Và khi nỗi đau quá sức chịu đựng‚ em có thể giúp họ gột bỏ<br>nó.",
    1057: "Khi kẻ họ thù ghét bấy lâu cuối cùng cũng chết‚ họ mỉm cười như<br>thể được giải thoát.",
    1059: "Anh... hiểu rồi. Hóa ra em vẫn tìm được ý nghĩa trong việc ám sát...",
    1071: "Có những kẻ tốt hơn là nên chết. Đó là điều em luôn được<br>dạy ở nghề trước.",
    1073: "...Em không thể dễ dàng quyết định kẻ sống người chết như vậy.",
    1084: "Fufufu‚ dĩ nhiên. Nhưng quả thật có kẻ cướp nụ cười<br>của người khác.",
    1111: "Mẹ em đã khuất vẫn thường nói: nếu em cứ mỉm cười‚ rồi<br>sẽ thực sự hạnh phúc.",
    1122: "Em cũng tin rằng nếu ép mình mỉm cười ngay cả lúc đau khổ<br>và gian nan‚ mai sau em sẽ thực sự hạnh phúc.",
    1124: "Hóa ra vì thế em lúc nào cũng mỉm cười. Không phải để giấu nỗi đau‚<br>mà vì một tương lai em có thể thực sự mỉm cười.",
    1135: "Vâng‚ em luôn cố giữ nụ cười trên môi‚ và em cũng<br>đã nỗ lực mang nụ cười đến mọi người.",
    1146: "Nhưng cũng có kẻ không muốn người khác mỉm cười.<br>Kẻ sống bằng cách cướp nụ cười quanh mình.",
    1155: "Khi em giết những kẻ như thế‚ nhiều người khác lại mỉm cười...",
    1167: "Nên em chẳng hề thấy áy náy khi giết những kẻ đó.",
    1178: "Nhưng nhìn lại bây giờ‚ nụ cười sinh ra từ việc đoạt mạng<br>người sao mà méo mó.",
    1187: "Em nghĩ mình chỉ đang giấu sự hối hận bằng những lời như 'Chúng đáng<br>chết' hay 'Đó chỉ là trừng phạt.'",
    1198: "Có lẽ vì em chỉ tạo nổi những nụ cười giả dối đó‚ em chẳng thể<br>mỉm cười chân thành.",
    1200: "Anh không phủ nhận một số mạng sống đáng giá hơn kẻ khác. Nếu anh<br>không tin thế‚ anh chẳng thể làm Chỉ Huy.",
    1202: "Nhưng kẻ tầm thường chẳng thể gạt bỏ cảm xúc đi được. Dù<br>bị căm hận nuốt chửng đến đâu.",
    1213: "Vâng. Giết chóc chẳng bao giờ mang lại nụ cười chân thành.",
    1224: "Nhưng kể từ khi em tới đây‚ được làm việc dưới trướng Chỉ Huy‚ em<br>đã có thể mỉm cười bằng cả tấm lòng.",
    1235: "Hôm nay cũng thật vui. Cùng Chỉ Huy tiêu diệt kẻ địch‚<br>nhặt được kho báu...",
    1247: "Em được chứng kiến kẻ đáng chết lại trở thành<br>kẻ nên để sống.",
    1258: "Nhờ Abyss và Chỉ Huy‚ em đã tìm được một công việc<br>tuyệt vời.",
    1260: "Hứ‚ ra nơi này là chỗ làm tốt à? Gu của em tệ<br>thật đấy.",
    1271: "Chỉ Huy nghĩ vậy sao? Em muốn tin mình có con mắt nhìn người tốt.",
    1273: "Em từng bảo bọn sát thủ đó tử tế mà‚ đúng không? Anh chẳng tin nổi<br>cái con mắt của em chút nào.",
    1284: "Ôi‚ thật đáng thất vọng.<br>Nhưng em nói thật lòng mà.",
    1295: "Căn cứ này thật là một nơi tuyệt vời.<br>Là nơi làm việc lý tưởng với em.",
    1303: "Và‚ Chỉ Huy‚ bảo vệ nơi này không phải chuyện dễ‚<br>đúng không?",
    1305: "Bởi nó không dễ‚<br>nên mọi người ở đây đều dốc sức.",
    1307: "Kẻ vì tiền‚ kẻ vì danh dự‚ kẻ vì tình ái.<br>Mỗi người có lý do riêng.",
    1318: "...Vậy em sẽ chiến đấu vì Chỉ Huy.<br>Vừa là thư ký vừa là sát thủ.",
    1320: "...Vậy có ổn không?<br>Từ nay em vẫn sẽ tiếp tục giết người.",
    1331: "Em muốn bảo vệ những nụ cười chân thành<br>xuất hiện quanh Chỉ Huy.",
    1343: "Vậy‚ nếu cần‚<br>xin Chỉ Huy hãy sai em làm bất cứ điều gì.",
    1350: "Dù là một con người hay một Tai Họa—",
    1394: "Gừưư!",
    1434: "Ồ?",
    1436: "...?! Quái vật phục kích?<br>Ayame—",
    1456: "*bùm!*",
    1552: "*thở phào*...<br>Xin lỗi vì làm gián đoạn.",
    1554: "...Một đòn tập kích từ điểm mù‚<br>và em đã phản đòn trong tích tắc...",
    1566: "Khụ khụ.<br>Dù là một con người hay một Tai Họa—",
    1577: "Em sẽ giết nó không sai một li.<br>Nếu Chỉ Huy muốn thế.",
    1579: "...Ra là vậy.<br>Anh sẽ sai em làm việc hết công suất.",
    1581: "Đổi lại‚ anh sẽ bảo đảm em kiếm được bộn. Như hôm nay.",
    1592: "Vâng‚ em rất mong được thế.",
    1604: "Từ nay‚ nếu có kẻ Chỉ Huy muốn chết‚ xin hãy gọi em<br>bất cứ lúc nào‚ Chỉ Huy của em.",
}

assert len(VI) == 104, f"expected 104 VI entries, got {len(VI)}"

lines = EN.read_text(encoding="utf-8-sig").splitlines()
raw = EN.read_bytes()
has_crlf = b"\r\n" in raw

# ---- preflight: compare inner <br> counts + ASCII comma for ALL text lines before writing ----
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
    elif line.startswith(("title,", "messageTextCenter,")):
        parts = line.split(",", 5)
        tf = parts[2] if len(parts) > 2 else ""
        new_text = VI[i]
        if "," in new_text:
            mismatches.append(f"L{i}: ASCII comma in VI: {new_text!r}")
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

# ---- focused diff (EN source text field -> VI text field) ----
WORK.mkdir(parents=True, exist_ok=True)
diff_lines = []
for i, line in enumerate(lines, 1):
    if line.startswith(TEXT_CMDS):
        if line.startswith("title,"):
            parts = line.split(",", 1)
            en_tf = parts[1] if len(parts) > 1 else ""
        else:
            parts = line.split(",", 5)
            en_tf = parts[2] if len(parts) > 2 else ""
        vi_tf = VI.get(i, "")
        cmd = line.split(",", 1)[0]
        diff_lines.append(f"L{i} [{cmd}]")
        diff_lines.append(f"  EN : {en_tf}")
        diff_lines.append(f"  VI : {vi_tf}")
        diff_lines.append("")
diff_path = WORK / "focused_diff.md"
diff_path.write_text("\n".join(diff_lines), encoding="utf-8")
print("WROTE", diff_path)
