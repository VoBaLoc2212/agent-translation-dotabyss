#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deterministic VI generator for hmn_10200100003 (Laveria cute-goods-store scene).

Source of truth: EN asset (authoritative text). JP novel + EN novel for context.
All structural bytes (BOM, CRLF, delimiters, IDs, tags, placeholders, trailing
tech fields, blank lines) are preserved. Only the text field of each candidate
record (title,/message,) is replaced with a hand-authored Vietnamese translation.
Internal commas use U+201A (‚); Commander->Chỉ Huy; 兄さん->anh; Laveria kept;
shopkeeper addressed politely (tôi/khách).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10200100003.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10200100003.txt"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

TITLE = {21: "Quá Đỗi Dễ Thương!"}

MSG = {
    34: "Laveria chắc chắn đã vào tiệm này rồi... Rốt cuộc đây là tiệm gì thế...?<br> ",
    39: "Đừng động đậy.<br> ",
    42: "Hả!<br> ",
    55: "(Một lưỡi dao kề cổ anh...! Khi nào cô ấy lẻn ra sau lưng anh vậy!?)<br> ",
    68: "Á‚ thôi anh chịu thua‚ anh đầu hàng. Anh không chống cự đâu‚ chỉ xin tha mạng cho anh.<br> ",
    70: "Nhưng anh khuyên ngươi nên vứt vũ khí và mau rời khỏi đây đi‚ vì<br>hiện tại trong tiệm này có một nữ chiến binh mạnh đến kinh ngạc‚ đáng tin cậy.<br> ",
    80: "...Cô gái \"\"mạnh đến kinh ngạc\"\" mà anh vừa nhắc—chính là em‚ đúng không‚<br>anh?<br> ",
    84: "Cái gì! Chính là em sao‚ Laveria! Anh cứ tưởng em là một loại sát thủ nào đó!<br> ",
    97: "Lời đó phải là của em chứ. Em cứ tưởng có kẻ tình nghi đang bám đuôi‚<br>hóa ra lại là anh‚ Laveria.<br> ",
    101: "Cố tình lẩn trốn rồi bám theo em—em định làm gì thế?<br> ",
    103: "Chẳng có lý do lớn lao. Anh chỉ ghé xem thử vì em đã biểu hiện<br>sự đáng ngờ quá rành rành.<br> ",
    111: "...Em lại đáng ngờ đến thế sao?<br> ",
    113: "Đáng ngờ đến mức nếu anh là lính canh‚ anh đã giải em về<br>trạm gác rồi.<br> ",
    120: "R-Phải... Xin lỗi vì đã làm anh lo.<br> ",
    122: "Nhưng sao em lại làm vậy? Có chuyện gì ở tiệm này<br>hay không?<br> ",
    124: "Trông qua thì... có vẻ chỉ là một tiệm đồ dễ thương thôi.<br> ",
    132: "C-Đúng‚ đúng rồi‚ đây là tiệm bán đồ dễ thương—một tiệm xinh xắn... anh<br>không nghĩ có gì kỳ lạ đâu‚ đúng không?<br> ",
    134: "Kỳ lạ không phải là tiệm‚ mà là em‚ Laveria. Hay em có<br>việc gì ở đây?<br> ",
    141: "Ơ‚ cũng chẳng hẳn là việc‚ chỉ là... không phải em có lý do<br>gì đặc biệt đâu...<br> ",
    143: "Có chuyện gì em không thể nói với anh sao? Á! Anh hiểu rồi‚ giờ anh biết rồi!<br> ",
    145: "Hóa ra là vậy—tiệm này dính líu đến thế giới ngầm‚ và em đến để<br>điều tra‚ đúng không?<br> ",
    151: "Không đời nào! Làm sao một tiệm xinh đẹp thế này lại có quan hệ<br>mờ ám chứ!<br> ",
    154: "Em chỉ đến để mua đồ \"\"dễ thương\"\" thôi‚ thế thôi!<br> ",
    158: "…<br> ",
    171: "…<br> ",
    173: "...Vậy là em đến để mua đồ \"\"dễ thương\"\".<br> ",
    183: "Á... không‚ ý anh là...<br> ",
    185: "Ừ‚ đúng rồi‚ chỗ này dường như chỉ bán toàn đồ dễ thương. Thế nên<br>em đến mua đồ \"\"dễ thương\"\" là đúng thôi‚ phải không? Thế đấy.<br> ",
    191: "*ưm*... *chết tiệt*... Sao? Nếu anh muốn cười thì cứ cười đi. Đúng rồi‚<br>chính em—một nữ chiến binh—đã đến mua đồ dễ thương!<br> ",
    194: "Em thích đồ dễ thương! Em yêu cả cái khái niệm dễ thương! Phòng em đầy<br>những thú bông! Có vấn đề gì không hả?<br> ",
    196: "Không‚ anh không phiền. Thế nên anh tưởng em đến mua quà tặng‚<br>hóa ra là cho chính mình‚ đúng không?<br> ",
    203: "Á... ôi... ưgh‚ em lỡ lời rồi! Em nói quá nhiều!<br> ",
    205: "Cô ấy đã lỡ lời sạch sẽ và đỏ mặt rần rộ! Anh không ngờ<br>Laveria lại có nét đáng yêu đến thế.<br> ",
    225: "Ha! Anh nhìn thấu thật đấy‚ anh!<br> ",
    227: "Ơ—ôi chao!<br> ",
    232: "Đúng rồi! Ở đây có đống hàng dễ thương!<br> ",
    234: "Không‚ không‚ khi anh nói \"\"dễ thương\"\"‚ anh đâu có nhắc đến tiệm hay<br>món hàng...<br> ",
    237: "Đúng‚ tiệm này là một danh tiệm ẩn nổi tiếng. Họ mở chi nhánh tại đây để<br>xoa dịu lòng người ở căn cứ.<br> ",
    244: "Không chỉ dễ thương bề ngoài—triết lý của nó tràn ngập<br>sự đáng yêu. Tuyệt diệu làm sao...!<br> ",
    246: "Laveria chẳng thèm nghe anh nói chút nào...! Hay là anh cứ để em ấy yên<br>và đừng phá không khí này...?<br> ",
    253: "Em hiểu rồi‚ anh‚ em hiểu rồi! Bầu không khí này thật khó cưỡng! Đúng‚<br>tiệm này không chỉ có hàng—cả không khí cũng dễ thương!<br> ",
    261: "Chỉ cần ở trong không gian này‚ em như được bao bọc bởi sự dễ thương... Á‚ thật đáng yêu...<br> ",
    269: "...*há hốc!* E-xin lỗi‚ em đã nói quá đà và lỡ lời...<br> ",
    286: "...Em đã trở lại rồi? Ừ‚ nó thật sự dễ thương‚ ừm hứm. Anh cứ cảm giác như<br>đang nạp quá liều dễ thương.<br> ",
    293: "Á‚ anh đồng ý. Anh bị bao quanh bởi đồ dễ thương đến mức gần chịu không nổi...<br> ",
    298: "Không‚ quan trọng hơn... Vậy là giờ anh đã biết tất cả về em rồi‚<br>anh...<br> ",
    301: "Em van anh đấy‚ anh. Anh làm ơn quên chuyện này đi được không?<br> ",
    303: "Anh có thể giả vờ quên‚ nhưng như thế lại càng khó xử hơn‚ anh<br>nghĩ sao?<br> ",
    305: "Thôi‚ nếu điều đó làm em bận tâm‚ Laveria‚ anh sẽ giữ kín. Chứ anh đâu có<br>kể với ai đâu.<br> ",
    314: "...Nếu anh đã nói vậy‚ anh‚ em tin anh. Thế thì nhẹ nhõm rồi. Cảm ơn anh.<br> ",
    316: "Em cần phải giấu kỹ đến thế sao? Đâu phải sở thích xấu đâu.<br> ",
    320: "...Nhưng mà xấu hổ quá‚ đúng không? Một nữ chiến binh lại mê đồ dễ thương như vậy.<br> ",
    324: "Như anh nói‚ anh‚ em phải là một nữ chiến binh đáng tin cậy. Em có<br>hình tượng cần giữ gìn.<br> ",
    326: "Thế à? Cá nhân anh thấy đó là một sự bất ngờ thú vị đấy.<br> ",
    330: "Hơn nữa‚ đồ dễ thương là dành cho người dễ thương. Kẻ như em<br>thực không xứng sở hữu chúng.<br> ",
    340: "Đúng‚ em biết mà. Một nữ chiến binh thô ráp như em không hợp với tiệm<br>như thế này...<br> ",
    342: "Thật sao? Anh thấy chẳng có chuyện đó đâu.<br> ",
    346: "Em không cần nịnh hót. Em tự biết mình thế nào. Em sẽ về trước khi<br>trở nên vướng mắt ở tiệm.<br> ",
    349: "Á‚ khoan đã‚ Laveria. Em định bỏ mặc anh ở đây thật sao?<br> ",
    356: "...Ý anh là sao?<br> ",
    358: "Hôm nay anh bị kề dao sau lưng‚ nên anh bất an. Ở một mình thì<br>đáng sợ... Anh cần một vệ sĩ đáng tin cậy‚ em biết không?<br> ",
    365: "*rên rẩm*... thôi được. Nếu có ai tới‚ em sẽ nói em là vệ sĩ của anh‚ rõ chưa!<br> ",
    367: "Ừ‚ được đấy. Thế thì... hmm‚ anh nên lấy cái nào ta?<br> ",
    376: "Anh định mua gì sao?<br> ",
    378: "Một món quà nho nhỏ thôi.<br> ",
    383: "Á... Alicia từng để mắt đến chỗ này.<br> ",
    386: "Mọi thứ về cô ấy đều dễ thương. Khác với em‚ đồ ở tiệm này có lẽ<br>rất hợp với cô ấy.<br> ",
    388: "Thôi‚ quà tặng cho một cô gái dễ thương chắc chắn là lựa chọn đúng... Ồ‚ cái này<br>có nét giống em đấy‚ Laveria.<br> ",
    396: "Giống em sao?<br> ",
    398: "Nó là thú bông trông đáng tin cậy mà lại mềm mại‚ búng được.<br>Cá nhân anh thấy nó hợp với em hoàn hảo.<br> ",
    407: "Đó là mẫu mới của dòng thú bông đó... Nó đã có hàng rồi!<br> ",
    409: "Tốt‚ trông như em cũng chẳng ghét nó. Vậy anh lấy con này.<br> ",
    413: "Khoan‚ Chỉ Huy. Đó chỉ là sở thích cá nhân của em thôi‚ em không rõ nó<br>có hợp gu Alicia hay không.<br> ",
    416: "Điều quan trọng là người nhận cảm thấy thế nào. Anh nên hỏi cô ấy<br>trước đã...<br> ",
    418: "Thế thì không sao‚ ổn mà. Này‚ chủ tiệm‚ giúp anh<br>được không?<br> ",
    433: "Dạ‚ khách cần gì ạ?<br> ",
    435: "Làm ơn gói hộ anh cái này được không? Anh định tặng nó cho một cô gái<br>dễ thương.<br> ",
    443: "…<br> ",
    451: "Ôi chao‚ thế à? Tất nhiên‚ tôi sẽ gói thật xinh xắn cho khách.<br> ",
    453: "Cảm ơn‚ anh nhờ chị đấy.<br> ",
    467: "Dạ‚ của khách đây. Chắc chắn họ sẽ thích cho mà xem.<br> ",
    485: "Biết bao nơ‚ giấy gói đủ sắc màu‚ và một nhân vật linh vật<br>được đặt khéo léo...!<br> ",
    490: "Dễ thương quá‚ dễ thương quá! Thế ra đây là hàng thật...!<br> ",
    492: "Ngay cả anh cũng thấy nó khá dễ thương... Nào‚ Laveria.<br> ",
    497: "Á‚ về phòng chỉ huy‚ anh sẽ đưa cái này cho Alicia—<br> ",
    501: "Đây là quà tặng‚ Laveria. Hãy nhận lấy nó.<br> ",
    511: "Hả...? Cho... em sao...?<br> ",
    513: "Ừ. Em luôn giúp đỡ anh‚ dù trên chiến trường hay ở<br>phòng chỉ huy. Từ giờ anh vẫn trông cậy vào em.<br> ",
    519: "Cái gì...! Không‚ em không thể nhận.<br> ",
    521: "Tại sao không? Nãy em nói về nó đầy nhiệt huyết thế kia‚ rõ ràng em thích mà‚<br>đúng không?<br> ",
    527: "Tất nhiên em thích. Nhưng ngay cả anh cũng thấy kỳ lạ khi<br>kẻ như em lại thích đồ dễ thương...!<br> ",
    529: "Chẳng kỳ lạ chút nào. Đó là sở thích tốt mà. Em không cần kể<br>với ai‚ nhưng cũng chẳng cần xấu hổ.<br> ",
    532: "C-nhưng‚ đồ này là cho các cô gái dễ thương mà‚ đúng không...?<br> ",
    534: "Đó là lý do anh tặng em‚ Laveria. Nó là quà cho một cô gái dễ thương.<br> ",
    538: "Em sao...?<br> ",
    541: "E-không cần đâu. Em chẳng dễ thương tí nào.<br> ",
    543: "Không‚ hôm nay em dễ thương suốt cả ngày. Em đã cho anh thấy nét đáng yêu của mình‚<br>chứ không chỉ là một nữ chiến binh đáng tin cậy.<br> ",
    547: "Em... dễ thương sao...?<br> ",
    549: "Ừ‚ em dễ thương mà. Cách mắt em sáng lên khi nói về<br>những thứ em yêu thích‚ và cái cách em bối rối sau khi nói quá nhiều.<br> ",
    551: "Có gì sai đâu khi một cô gái dễ thương thích đồ dễ thương? Nó hợp với em<br>hoàn hảo mà‚ Laveria.<br> ",
    555: "Anh...<br> ",
    557: "Thôi‚ cứ coi đây là tiền thưởng. Lần sau anh lại nhờ em.<br> ",
    562: "...Ừ‚ cảm ơn anh.<br> ",
    564: "Được rồi. Ta về thôi. Vẫn còn chút việc phải làm mà.<br> ",
    575: "...Á‚ đúng là em là thú bông dễ thương thật. Dù nó chẳng hợp với<br>kẻ như em chút nào...<br> ",
    578: "Nhưng anh bảo em là một cô gái dễ thương. Anh nói đồ dễ thương hợp với em.<br> ",
    581: "...Anh cũng thấy em dễ thương sao‚ giống như em nhìn anh vậy...?<br> ",
    591: "Nếu vậy thì‚ em cũng hơi vui một chút. Nếu chỉ trước mặt<br>anh thôi‚ thì có lẽ làm cô gái dễ thương cũng chẳng tệ‚ nhỉ.<br> ",
}


def split_keep(text: str):
    """Split into (content, terminator) per physical line, preserving CRLF."""
    segs = re.split(r"(?<=\n)", text)
    out = []
    for s in segs:
        if s.endswith("\r\n"):
            out.append((s[:-2], "\r\n"))
        elif s.endswith("\n"):
            out.append((s[:-1], "\n"))
        else:
            out.append((s, ""))
    return out


def main() -> int:
    raw = EN.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    segs = split_keep(text)

    # sanity: candidate count
    cand = [i for i, (c, _) in enumerate(segs, 1) if c.startswith(TEXT_CMDS)]
    assert len(cand) == 109, f"expected 109 candidates, got {len(cand)}"

    missing, ascii_comma, br_mismatch = [], [], []
    new_segs = []
    for idx, (content, term) in enumerate(segs, 1):
        if not content.startswith(TEXT_CMDS):
            new_segs.append((content, term))
            continue
        parts = content.split(",")
        if content.startswith("title,"):
            vi = TITLE.get(idx)
            if vi is None:
                missing.append(idx); new_segs.append((content, term)); continue
            old_tf = parts[1]
            new_content = "title," + vi
        else:
            vi = MSG.get(idx)
            if vi is None:
                missing.append(idx); new_segs.append((content, term)); continue
            old_tf = parts[2]
            parts[2] = vi
            new_content = ",".join(parts)
        if "," in vi:
            ascii_comma.append(idx)
        if old_tf.count("<br>") != vi.count("<br>"):
            br_mismatch.append((idx, old_tf.count("<br>"), vi.count("<br>")))
        new_segs.append((new_content, term))

    assert not missing, f"missing translations for lines {missing}"
    assert not ascii_comma, f"ASCII comma in VI text at lines {ascii_comma}"
    assert not br_mismatch, f"<br> count mismatch: {br_mismatch}"

    out_text = "".join(c + t for c, t in new_segs)
    OUT.write_bytes(out_text.encode("utf-8-sig"))
    crlf = b"\r\n" in out_text.encode("utf-8-sig")
    print(f"WROTE {OUT}")
    print(f"segments={len(new_segs)} bom={has_bom} crlf={crlf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
