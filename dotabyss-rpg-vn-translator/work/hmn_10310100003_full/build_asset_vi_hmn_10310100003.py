#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI text fields for hmn_10310100003 from the EN asset (EN-asset-is-English case).

Field-index generation: replace the text field (index 1 for title, 2 for message*) of each
text command line, keeping every technical field, delimiter, tag, placeholder, BOM, CRLF
and <br> count identical to the EN source.

Conventions applied:
- Commander / 司令官 -> Chiet Huy (Chỉ Huy)
- Young Lord (若殿) -> Thiếu Gia ; Lord (領主さま) -> Lãnh Chúa
- Frontline Base -> Căn Cứ Tiền Tuyến ; Hatsune/Kotono/Hourai kept romanized
- internal fullwidth ， -> U+201A ‚
- wolf SFX localized (Grr->Gừ, Gyaow->Gâu)
- punctuation-only lines changed byte (... -> …)
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10310100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10310100003.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10310100003_full"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# line_no -> VI text field (including trailing "<br> " suffix where the source had it)
VI_TEXT = {
    21: "Nơi Ân Nghĩa Và Trung Nghĩa Cư Ngụ",  # title, no suffix

    # ---- wolf SFX (localized) ----
    71: "Gừ gừ gừ...!<br> ",
    296: "Gừ gừ gừ...!<br> ",
    403: "Gừm!<br> ",
    521: "Gừm!?<br> ",
    586: "Gừ gừ gừ...!<br> ",
    670: "Gừm!<br> ",
    921: "Gừ gừ gừ...!<br> ",
    1023: "Gừ... Gừm!<br> ",
    1171: "Gừm!<br> ",
    1532: "Gâu! Gừ! Gừ‚ gừ...!<br> ",
    1621: "Gâu...!<br> ",

    # ---- Hourai youth (Young Lord) : speaker ホウライの青年, self "tôi" ----
    109: "(Thân thể tôi không cử động được nữa... Chẳng lẽ tôi đã mất quá nhiều máu rồi sao...? Nếu cứ thế này‚ tôi<br>sẽ ngã khỏi cây và thành mồi cho con sói...)<br> ",
    111: "(Chẳng lẽ tôi lại chết ở một nơi như thế này sao...? Thật là oán hận...)<br> ",
    126: "Xin lỗi... Cha‚ mẹ...<br> ",
    209: "Cái gì...!?<br> ",
    211: "Chẳng lẽ... là Hatsune‚ sao...? Sao em lại ở đây...!?<br> ",
    349: "Hatsune...! Cẩn thận‚ con thú đó rất nguy hiểm!<br> ",
    1175: "H-Hatsune! Coi chừng!<br> ",
    1843: "À‚ tôi đã cầm máu xong rồi. Tôi mang ơn em đấy‚ Hatsune. Còn<br>người kia...<br> ",
    1847: "Chỉ Huy...?<br> ",
    1849: "…Chẳng lẽ ngài chính là Chỉ Huy của Căn Cứ Tiền Tuyến?<br> ",
    1864: "Hatsune‚ em không biết sao...? Ngài ấy là người nắm toàn quyền<br>với Căn Cứ Tiền Tuyến.<br> ",
    1898: "Nhờ có anh‚ mạng sống của tôi đã được cứu. Tôi biết lấy gì để đáp đền...<br> ",
    1902: "Ngài thật bao dung... So với anh‚ tôi vẫn còn phải<br>học hỏi nhiều.<br> ",
    1953: "Con đoản đao cha đã tặng tôi...<br> ",
    1966: "Hatsune... Liệu kẻ như tôi có xứng đáng cầm con đoản đao này<br>không?<br> ",
    1979: "Tại Căn Cứ Tiền Tuyến tôi gặp Kotono và được cô ấy chỉ dạy‚ tưởng mình<br>đã mạnh lên. Thế mà tình cảnh thảm hại này... tôi không dám mặt đối mặt với cha.<br> ",
    1992: "Tôi xin lỗi‚ Hatsune. Tôi vẫn chưa thể trở về Hourai.<br>Tôi muốn<br>ở lại Căn Cứ Tiền Tuyến thêm một thời gian để tiếp tục tu luyện.<br> ",
    2028: "Ra vậy... Tôi xin lỗi‚ Hatsune.<br>Có em ở đây‚ tôi thấy an tâm.<br> ",

    # ---- Hatsune (ハツネ) : self "em", addresses Commander "anh", Young Lord "Thiếu Gia" ----
    178: "Thiếu Gia!<br> ",
    255: "Để sau em sẽ giải thích! Làm ơn chờ một chút!<br> ",
    347: "Nào‚ con thú kia! Tới đi! Để em làm đối thủ của ngươi!<br> ",
    354: "Đã rõ!<br> ",
    448: "(Nhanh quá...! Nhưng—)<br> ",
    577: "Đừng tưởng bắt được em dễ dàng như vậy!<br> ",
    630: "Tới đi...! Để em bắt ngươi phải hối hận vì đã làm bị thương Thiếu Gia!<br> ",
    728: "Ồ!<br> ",
    834: "Hatsune tiếp tục né tránh răng nanh và móng vuốt của con sói trong gang tấc.<br>khoảng cách hiểm nghèo.<br> ",
    880: "Hả! Chỉ có thế thôi sao!<br> ",
    978: "(Em cứ né tránh đòn tấn công của nó‚ nên nó bắt đầu bực bội hơn rồi...<br>Đến lúc rồi.)<br> ",
    1067: "Ồ! Ngươi đang nhìn gì vậy! Em ở đây này...<br> ",
    1099: "Hatsune định lách né cú xông tới của con sói‚ nhưng đột nhiên bị mất<br>thăng bằng.<br> ",
    1110: "Chết! Khốn kiếp‚ em vấp phải rễ cây!<br> ",
    1173: "Con sói lao vào Hatsune đang mất thăng bằng!<br> ",
    1239: "...Chỉ là đùa thôi!<br> ",
    1279: "Bẫy sao...?<br> ",
    1294: "Anh thật sự làm được sao...?<br> ",
    1311: "Em sao...?<br> ",
    1340: "Chuyện đó... Ừ‚ em nghĩ mình làm được.<br> ",
    1353: "Đó là lúc chúng ta giật bẫy!<br> ",
    1369: "…<br> ",
    1380: "Ừ... tất nhiên rồi! Em sẽ làm!<br> ",
    1423: "(Nó đã nổi điên lên và tự sa vào bẫy luôn!)<br> ",
    1449: "Giờ!<br> ",
    1497: "Con sói lao về phía Hatsune bị dây leo quấn lấy chân và bị<br>treo lơ lửng lên không trung—!<br> ",
    1543: "—Dù ngươi có gào thét bao nhiêu‚ thì đã quá muộn rồi.<br> ",
    1581: "Hãy chuẩn bị đi!<br> ",
    1619: "Xẹt—!<br> ",
    1716: "Tuyệt quá!<br> ",
    1750: "Ồ! Này‚ sao tự nhiên ôm anh thế...?<br> ",
    1763: "Tuyệt quá‚ anh! Anh hạ gục được kẻ mà ngay cả Kotono cũng thất bại<br>khi đối đầu!<br> ",
    1765: "Anh hiểu rồi‚ anh hiểu rồi. Bình tĩnh lại đã‚ được không?<br> ",
    1776: "Ahaha! Em cảm thấy như có anh thì em đánh thắng được mọi kẻ thù!<br> ",
    1795: "…*thở dốc*! Phải rồi‚ Thiếu Gia!<br> ",
    1830: "Hatsune…<br> ",
    1841: "Thiếu Gia! Ngài có sao không? Chúng ta cần sơ cứu vết thương nhanh lên...<br> ",
    1862: "Nghĩ lại thì‚ thiên hạ đúng là gọi anh thế. Cái chức 'Chỉ Huy' ấy là<br>làm gì vậy?<br> ",
    1883: "Hả?! T-thật sao! Em nghĩ mình đã vô lễ mà không hề hay biết...<br> ",
    1896: "O-ồ‚ thật sao? Hehe‚ dù anh là một nhân vật lớn thế kia‚ anh<br>vẫn giúp bọn em. Anh Chỉ Huy đúng là một người tốt!<br> ",
    1913: "Thiếu Gia…<br> ",
    1925: "…Trên đường em nhặt được thứ này. Của anh‚ em trả lại cho anh đây.<br> ",
    1964: "Chúng ta hãy trở về Hourai đi‚ Thiếu Gia.<br>Lãnh Chúa đang đợi Thiếu Gia trở về.<br> ",
    1977: "Tất nhiên.<br>Ngài chính là người sẽ trở thành tộc trưởng kế tiếp...<br> ",
    1990: "Thiếu Gia... ngài đang nói gì vậy...<br> ",
    2003: "Thiếu Gia…<br> ",
    2026: "Em hiểu rồi.<br>Vậy thì‚ em Hatsune‚ sẽ tháp tùng ngài đến Căn Cứ Tiền Tuyến luôn!<br> ",
    2039: "Em sẽ bảo vệ ngài khỏi mọi nguy hiểm!<br>Đầu tiên‚ chúng ta hãy trở về Căn Cứ Tiền Tuyến để chữa vết thương cho ngài.<br> ",
    2115: "Thế thì nhẹ nhõm rồi...<br> ",
    2149: "Chỉ Huy. Cảm ơn anh nhiều.<br> ",
    2161: "Một mình em đã không thể cứu được Thiếu Gia...<br>Em mang ơn anh một món nợ lớn‚ Chỉ Huy.<br> ",
    2176: "Không đời nào!<br>Một samurai trả ơn người đã giúp mình!<br> ",
    2185: "Dù anh bảo không cần thì em cũng nhất định sẽ đền đáp<br>anh!<br> ",
    2198: "À thì ra‚ Chỉ Huy ơi‚ em tính ở lại Căn Cứ Tiền Tuyến cùng với<br>Thiếu Gia luôn‚ nhưng...<br> ",
    2209: "Ưm... nếu không phiền‚ em có thể giúp anh công việc lần nữa được không?<br> ",
    2216: "Em muốn đền đáp món nợ‚ nhưng mà‚ chỉ cần ở đây thôi em cũng cảm thấy<br>mình sẽ mạnh lên gấp bội!<br> ",
    2225: "Em nhất định sẽ trở nên có ích cho anh‚ Chỉ Huy! Anh nghĩ sao?<br> ",
    2240: "T-thật sao!? Ehehe‚ nếu anh đã nói vậy‚ em chịu thua thôi.<br> ",
    2251: "Lúc anh gặp khó khăn‚ em sẽ tới giúp anh! Vậy nên...<br> ",
    2262: "Từ nay chúng ta cùng làm việc với nhau nhé‚ Chỉ Huy!<br> ",

    # ---- Commander (<user>) : self "anh"/"tôi", addresses Hatsune "em" ----
    1268: "Nghe này‚ trước tiên hãy thu hút sự chú ý của con sói đó. Trong lúc đó‚ anh sẽ giăng<br>bẫy.<br> ",
    1281: "Ừ. Mấy cái cây quanh đây có cành mềm và dẻo.<br>Thêm nữa‚ có rất nhiều dây leo.<br> ",
    1283: "Dùng cành cây‚ dây leo‚ và bất cứ dụng cụ nào tiện tay‚ chúng ta sẽ<br>có thể giăng một cái bẫy đơn giản để bắt con sói đó.<br> ",
    1296: "Nhưng con sói đó khá thông minh. Kotono bị bất ngờ là vì<br>nó tấn công từ hướng xuôi gió.<br> ",
    1298: "Có lẽ‚ nếu chúng ta dẫn nó thẳng vào bẫy‚ nó sẽ nghi ngờ<br>và không hiệu quả đâu.<br> ",
    1300: "Đó là lúc em phát huy đấy.<br> ",
    1313: "Ừ. Với những động tác của em ở trường huấn luyện‚ em sẽ có thể<br>tiếp tục né tránh đòn của con sói. Em nghĩ sao?<br> ",
    1342: "Tốt. Hãy chọc tức và dồn ép nó thật triệt để. Rồi‚ khi nó đã<br>nóng máu...<br> ",
    1355: "Đúng vậy. Thành bại của chiến thuật này là ở em đấy.<br> ",
    1357: "—Chính em là người sẽ cứu Thiếu Gia.<br> ",
    1670: "Tốt‚ kế hoạch thành công! Đúng như anh nghĩ‚ Hatsune. Giỏi lắm—<br> ",
    1750: "Ồ! Này‚ sao tự nhiên ôm anh thế...?<br> ",
    1765: "Anh hiểu rồi‚ anh hiểu rồi. Bình tĩnh lại đã‚ được không?<br> ",
    1845: "Tôi là %user%.<br> ",
    1851: "Đại loại vậy.<br> ",
    1885: "Anh không bận tâm. Giờ đổi thái độ thì kỳ quặc lắm.<br> ",
    1900: "Đừng bận tâm. Chúng ta đã tiêu diệt một quái vật nguy hiểm và giữ<br>thương vong ở mức tối thiểu. Kết thúc có hậu mà.<br> ",
    2107: "Mừng quá. Chàng trai trẻ kia mất nhiều máu‚ nhưng nghe nói mạng sống<br>của cậu ấy không nguy hiểm.<br>Có vẻ cậu ấy sẽ cử động được sau khoảng một tuần.<br> ",
    2163: "Đừng bận tâm.<br>Nếu em không có ở đó‚ anh đã mất đi một người tài năng quý giá.<br> ",
    2165: "Nên đừng coi đó là món nợ.<br> ",
    2187: "Được rồi‚ được rồi. Em đúng là một kẻ ngoan cố‚ nhỉ?<br> ",
    2227: "Hả‚ em nghiêm túc hẳn lên rồi mà chỉ có thế thôi sao?<br> ",
    2229: "Tất nhiên‚ không có lý do gì để từ chối. Có em ở đây khiến Căn Cứ Tiền Tuyến<br>thêm vững chắc.<br> ",

    # ---- messageTextUnder (no suffix, no <br>) ----
    2075: "Sau đó‚ %user% và những người khác đã trở về Căn Cứ Tiền Tuyến an toàn.",
}


def main() -> None:
    raw = EN.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(True)

    # Pre-compute expected <br> counts from source text fields
    expected_br = {}
    for i, ln in enumerate(lines, 1):
        s = ln.strip().lstrip("\ufeff")
        if not s.startswith(TEXT_CMDS):
            continue
        cmd = s.split(",", 1)[0]
        if cmd == "title":
            tf = s.split(",", 1)[1].rstrip("\r\n")
        else:
            parts = ln.rstrip("\r\n").split(",")
            tf = parts[2]
        expected_br[i] = tf.count("<br>")

    # Assertions before writing
    assert set(VI_TEXT) == set(expected_br), \
        f"line set mismatch: {set(VI_TEXT) ^ set(expected_br)}"
    for ln_no, vi in VI_TEXT.items():
        assert "," not in vi, f"ASCII comma in VI line {ln_no}: {vi!r}"
        assert vi.count("<br>") == expected_br[ln_no], \
            f"<br> count mismatch line {ln_no}: got {vi.count('<br>')} want {expected_br[ln_no]}"
        # no stray ASCII < that would look like a tag other than <br>
        assert "<" not in vi.replace("<br>", ""), f"unexpected '<' in line {ln_no}: {vi!r}"

    out_lines = []
    changed = 0
    for i, ln in enumerate(lines, 1):
        s = ln.strip().lstrip("\ufeff")
        if s.startswith(TEXT_CMDS) and i in VI_TEXT:
            body = ln.rstrip("\r\n")
            parts = body.split(",")
            cmd = parts[0]
            idx = 1 if cmd == "title" else 2
            parts[idx] = VI_TEXT[i]
            new_body = ",".join(parts)
            out_lines.append(new_body + "\r\n")
            changed += 1
        else:
            out_lines.append(ln)

    out_text = "".join(out_lines)
    out_bytes = b"\xef\xbb\xbf" + out_text.encode("utf-8")
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out_bytes)

    # write preflight report
    report = {
        "changed_text_lines": changed,
        "total_text_lines": len(expected_br),
        "has_bom_in": has_bom,
        "has_crlf_in": has_crlf,
        "out_has_bom": out_bytes.startswith(b"\xef\xbb\xbf"),
        "out_has_crlf": b"\r\n" in out_bytes,
        "in_lines": len(lines),
        "out_lines": out_text.count("\r\n") + (0 if out_text.endswith("\r\n") else 1),
    }
    (WORK / "_preflight.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("WROTE", VI)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
