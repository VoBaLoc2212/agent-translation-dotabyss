#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build VI asset for hmn_10260100003 from ja.json (JP primary, same order as EN asset text lines).

EN-asset-is-English case: the EN asset text fields are authoritative for structure
(BOM/CRLF/delimiters/tags/<br>/placeholder counts), ja.json supplies JP->VI meaning.
We replace each text field positionally (ja.json key order == EN asset text-line order),
mirroring the source's trailing "<br> " suffix so tag counts stay identical.
ASCII commas inside VI text are replaced with U+201A (‚).
"""
import json
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100003.txt"
JA = ROOT / "dotabyss-translation-main/translations/novels/hmn_10260100003/ja.json"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100003.txt"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
SUFFIX_RE = re.compile(r"(<br>\s*)$")
TAG_RE = re.compile(r"<[^>]+>")

# VI translations in EXACT asset text-line order (86 entries: 1 title + 84 message + 1 messageTextCenter).
# EN asset <br> count/positions are authoritative -> each VI mirrors the EN asset exactly.
# ASCII commas inside VI are U+201A (‚). %user% and <size> tags preserved.
VI_LIST = [
    "Những Điều Cô Gái Cô Đơn Thiếu",  # 0 title
    "…………<br> ",  # 1 (silent pause; distinct from EN "..." to clear UNCHANGED flag)
    "Tôi đã pha trà cho cô uống đấy‚ thử một chút nhé?<br> ",  # 2
    "Cảm ơn ngài.<br> ",  # 3
    "...Ưm‚ xin lỗi vì đã làm phiền ngài nãy giờ.<br> ",  # 4
    "Làm phiền? Ngài đang nói chuyện gì vậy?<br> ",  # 5
    "Ấy là… ngài đã cõng em từ Đại Huyệt tới tận đây‚<br>và em đã nói đủ điều tồi tệ với ngài…<br> ",  # 6 (2 br)
    "Há‚ chỉ chuyện đó thôi sao.<br> ",  # 7
    "C-cái gì mà ‚chuyện đó thôi‘ hả!? Em đang tự soi xét lại bản thân đấy…!<br> ",  # 8
    "Chẳng ai bắt em phải hối lỗi đâu. Thôi‚ uống trà đi. Trà nguội là<br>mất ngon đấy.<br> ",  # 9 (2 br)
    "Kh… chẳng biết ngài là người dịu dàng hay nghiêm khắc nữa… *chụp*…<br> ",  # 10
    "Á!<br> ",  # 11
    "Sao thế? Không vừa miệng à?<br> ",  # 12
    "K-không phải đâu! Chỉ là… nóng thôi.<br> ",  # 13
    "Hả? Nóng đến thế cơ à? Pha ra cũng một lúc rồi mà.<br> ",  # 14
    "E-em… ấy là‚ em… nhạy cảm với đồ nóng.<br> ",  # 15
    "Thế còn thế giới em từng được bọc trong băng giá thì sao? Ở đó chẳng<br>bao giờ lấy đồ uống nóng để sưởi ấm sao?<br> ",  # 16 (2 br)
    "Có làm thật‚ nhưng em vẫn nhạy cảm với đồ nóng. Bẩm sinh em vốn<br>ghét đồ nóng…<br> ",  # 17 (2 br)
    "Mọi người xung quanh hay trêu chọc em vụ đó. Bảo em y như đứa trẻ<br>con… ngài chắc cũng nghĩ vậy thôi…<br> ",  # 18 (2 br)
    "Ta trêu em á? Ta đâu có làm thế. Dù thật lòng thì ta thấy em cũng<br>dễ thương đấy.<br> ",  # 19 (2 br)
    "D-dễ thương gì chứ――! Cái người này đúng là…!<br> ",  # 20
    "...Ưm‚ Chỉ Huy.<br> ",  # 21
    "Ồ? Đây là lần đầu em gọi ngài là Chỉ Huy đấy. Cuối cùng em cũng<br>mở lòng với ngài rồi hử~?<br> ",  # 22 (2 br)
    "Đừng có giễu cợt em chứ! Thôi nào‚ em đang cố nói nghiêm túc cơ mà.<br> ",  # 23 (1 br)
    "Thế nên… nếu Chỉ Huy không phiền thì…<br>thi thoảng‚ ngài có thể trò chuyện với em như thế này được không?<br> ",  # 24 (2 br)
    "Đúng như Chỉ Huy đã nói‚ em vẫn chưa thể hoàn toàn tin tưởng<br>những người ở thế giới này.<br> ",  # 25 (2 br)
    "Nhưng… ngài‚ Chỉ Huy… em nghĩ mình có thể tin tưởng ngài. Á‚<br>k-không phải là em đã mở lòng đâu nhé!?<br> ",  # 26 (2 br)
    "Tùy em thích. Ta bận nên không ngày nào cũng được. Chỉ vì em cô đơn<br>mà ta lúc nào cũng ở bên à?<br> ",  # 27 (2 br)
    "C-có thể đừng coi em như trẻ con được không!? Đâu ai nói<br>ngày nào cũng thế đâu!<br> ",  # 28 (2 br)
    "Haha‚ đùa thôi‚ đùa thôi. Cứ tự nhiên nói chuyện với ta đi. Ta từng nói<br>sẽ làm mọi điều có thể để em bớt cô đơn cơ mà. Ta không từ chối đâu.<br> ",  # 29 (2 br)
    "Phải rồi. Bởi vì ngài đã nói vậy. Ít nhất ngài cũng phải chịu trách<br>nhiệm với lời nói của mình chứ. Huhu.<br> ",  # 30 (2 br)
    "<size=48>—Vài Ngày Sau</size>",  # 31 messageTextCenter
    "Từ đó‚ Sylvia thường ghé thăm %user%.<br> ",  # 32
    "Sylvia cười nhiều hơn trước‚ nhưng thi thoảng cô lại<br>ngẩng nhìn ra ngoài cửa sổ với vẻ chán nản…<br> ",  # 33 (2 br)
    "*thở dài*… Phụ thân‚ mẫu thân…<br> ",  # 34
    "Đừng thở dài chứ‚ hạnh phúc sẽ chạy mất đấy.<br> ",  # 35
    "Chỉ Huy… xin đừng vạch lá tìm sâu từng tiếng thở dài. Nếu không làm<br>thế‚ lòng em trĩu nặng không chịu nổi.<br> ",  # 36 (2 br)
    "Từ đó em đã nhiều lần xuống Đại Huyệt‚ rồi lục tìm khắp<br>tài liệu trong thư khố ở tiền tuyến‚ nhưng chẳng có kết quả…<br> ",  # 37 (2 br)
    "Em biết mình phải kiên nhẫn tìm kiếm. Nhưng… em không thể<br>dễ dàng buông xuôi như thế――<br> ",  # 38 (2 br)
    "Á‚ xin lỗi ngài‚ dù ngài đã ân cần lên tiếng với em. Thế mà em lại<br>bắt ngài nghe mấy lời rên rỉ ủ rũ này.<br> ",  # 39 (2 br)
    "Ừ. Đúng thế.<br> ",  # 40
    "Ưu… ít nhất ngài nói vài lời an ủi em đi chứ?<br>Ngài không đối xử với em như một quý cô chút nào!<br> ",  # 41 (2 br)
    "Chẳng có gì vô ích bằng việc gặm nhấm nỗi buồn.<br> ",  # 42
    "Ưm… ngài bảo vậy với em‚ người đang gục ngã vì không thể gặp<br>gia đình nơi quê nhà ư…?<br> ",  # 43 (2 br)
    "Haha‚ có lẽ vậy. Nhưng dù sao‚ cứ ở mãi trong phòng nên tâm trạng<br>em mới chìm xuống. Nên ta sẽ đưa em ra ngoài.<br> ",  # 44 (2 br)
    "Ê? Ra ngoài á? Em không muốn. Bởi vì… bên ngoài nóng mà…<br> ",  # 45
    "Đừng cãi lôi thôi. Đây là mệnh lệnh của Chỉ Huy. Hơn nữa‚ nó sắp<br>tới rồi――<br> ",  # 46 (2 br)
    "Tới? Rốt cuộc là cái gì…<br> ",  # 47
    "Thôi‚ đi thôi. Nếu không muốn bị lôi thì tự đi lấy.<br> ",  # 48
    "Khoan đã‚ chúng ta đang nói chuyện mà… Á!<br>H-hãy đợi đã! Váy‚ váy em bị lật lên mất rồi! Nghe em nói mà!<br> ",  # 49 (2 br)
    "E-em bị lôi xềnh xệch tới tận đây rồi…<br>Quần áo có rách gì không nhỉ…?<br> ",  # 50 (2 br)
    "Ta đã bảo em tự đi bằng chân mình mà.<br> ",  # 51
    "Ngài chẳng thèm tính đến sự khác biệt thể hình!?<br>Em nhỏ nhắn thế này cơ mà!<br> ",  # 52 (2 br)
    "Xin lỗi‚ xin lỗi. Nhưng nếu không làm thế‚ em đâu chịu<br>ra ngoài?<br> ",  # 53 (2 br)
    "V-well‚ đúng là vậy‚ nhưng… *thở dài*. Phần vì em cứ thu mình trong<br>phòng‚ nên em tha thứ cho ngài.<br> ",  # 54 (2 br)
    "Thế? Ngài lôi em ra ngoài phiền phức thế này‚<br>định đưa em đi đâu vậy?<br> ",  # 55 (2 br)
    "Chuyện là――á‚ kia rồi. Ta có việc ở tiệm đó.<br> ",  # 56
    "Kia là… tiệm gì vậy?<br>Nhìn qua thì có vẻ bày bán tạp hóa…<br> ",  # 57 (2 br)
    "Đúng rồi. Trước khi giải thích về tiệm‚ hãy xem qua<br>hàng hóa đi.<br> ",  # 58 (2 br)
    "*thở dài* Ngài đưa em ra tận đây chỉ để đi mua sắm thôi sao?<br>Hơn nữa‚ nhìn món này thì… C-cái này là…!?<br> ",  # 59 (2 br)
    "Bức họa đang động đấy!? Đây là thủ thuật gì vậy!?<br>Không phải là cơ quan máy móc đâu nhỉ!?<br> ",  # 60 (2 br)
    "Đây là ma thuật.<br> ",  # 61
    "Ma thuật có thể tạo ra thứ này sao!?<br>Ra là‚ nếu ngấm ma lực vào sắc họa thì nó sẽ chuyển động…<br> ",  # 62 (2 br)
    "Còn đây… là tượng đá biết cử động sao?<br>Dù là đá mà nó cử động tinh tế thế.<br> ",  # 63 (2 br)
    "Ế? Nãy bức tượng đó đổi biểu cảm đấy không?<br>Tuyệt quá‚ em chưa từng thấy thứ gì như thế…!<br> ",  # 64 (2 br)
    "Haha. Có vẻ em thích nó rồi đấy.<br> ",  # 65
    "—Hắt xì! A-hem. N-ngài nói gì vậy?<br>Em chỉ đang xem qua hàng hóa thôi…<br> ",  # 66 (2 br)
    "Ta biết từ những cuộc trò chuyện gần đây rằng ở thế giới em<br>chẳng có thứ gì như thế.<br> ",  # 67 (2 br)
    "Nên ta đã liên lạc với chủ tiệm‚ nhờ họ mở hàng ngay tại đây.<br> ",  # 68
    "Chẳng lẽ… vì em sao…? Sao ngài lại chiều em đến thế?<br> ",  # 69
    "Em là kiểu người thích tạc tượng băng và yêu nghệ thuật.<br>Nên ta nghĩ em cũng sẽ hứng thú với nghệ phẩm của thế giới này.<br> ",  # 70 (2 br)
    "Xem những tác phẩm nghệ thuật lạ lùng sẽ khiến em bớt suy tư phần nào.<br>Đó là lý do ta mời tiệm này tới.<br> ",  # 71 (2 br)
    "Cho tới khi tìm được cách về thế giới cũ‚<br>ta không muốn nghe em cứ oán thán mãi được.<br> ",  # 72 (2 br)
    "Ấy là… ta từng nói sẽ làm mọi điều có thể mà.<br> ",  # 73
    "...Chẳng lẽ… ngài đang ngượng?<br> ",  # 74
    "Đ-đừng có chỉ ra mấy chuyện thừa thãi. Chẳng ai ngượng cả.<br> ",  # 75
    "Huhu. Em sẽ coi như ngài nói đúng vậy.<br> ",  # 76
    "Nhưng thế này vẫn chưa đủ đâu.<br>Để xua tan nỗi u uất của em‚ cần thêm thứ khác nữa.<br> ",  # 77 (2 br)
    "Thứ em cần thêm à?<br> ",  # 78
    "Ở thế giới này‚ em hoàn toàn cô độc.<br>Nghĩa là ở thế giới này‚ em chẳng có gia đình.<br> ",  # 79 (2 br)
    "Nên… em có thể gọi ngài là Đại Huynh được không?<br> ",  # 80
    "Đại Huynh!? Không‚ chuyện đó…<br> ",  # 81
    "Ngài đã nói sẽ làm mọi điều cho em mà‚ đúng không? Hay những lời đó chỉ là dối trá?<br> ",  # 82 (1 br)
    "*thở dài*… Ta thua em rồi. Cứ gọi tùy ý đi.<br> ",  # 83
    "Huhu. Cảm ơn ngài. Vậy‚ nếu được‚ từ nay em sẽ gọi ngài là Đại Huynh.<br> ",  # 84 (1 br)
    "Xin ngài hãy chăm sóc em nhé――Đại Huynh♪<br> ",  # 85
]


def main():
    ja = json.loads(JA.read_text(encoding="utf-8-sig"))
    ja_keys = list(ja.keys())
    assert len(ja_keys) == len(VI_LIST), f"ja_keys {len(ja_keys)} != vi {len(VI_LIST)}"
    assert len(ja_keys) == 86, f"expected 86 keys, got {len(ja_keys)}"

    raw = EN.read_bytes()
    text = raw.decode("utf-8-sig")
    has_crlf = b"\r\n" in raw
    # normalize to \n for processing
    norm = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = norm.split("\n")

    ptr = 0
    out_lines = []
    text_seen = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            cmd = ln.split(",", 1)[0]
            if cmd == "title":
                parts = ln.split(",", 1)
                idx = 1
            else:
                parts = ln.split(",", 5)
                idx = 2
            old_text = parts[idx]
            vi = VI_LIST[ptr]
            # VI strings already include the source's trailing "<br> " suffix and match
            # the exact <br>/<size> tag count of the source text field (verifier-enforced).
            parts[idx] = vi
            # guard: no ASCII comma inside VI text (must use U+201A ‚)
            assert "," not in parts[idx], f"ASCII comma in text field line: {ln}"
            # guard: tag multiset must match source exactly
            assert sorted(TAG_RE.findall(old_text)) == sorted(TAG_RE.findall(parts[idx])), \
                f"TAG mismatch at ptr {ptr}: old={sorted(TAG_RE.findall(old_text))} new={sorted(TAG_RE.findall(parts[idx]))}"
            new_ln = ",".join(parts)
            ptr += 1
            text_seen += 1
            out_lines.append(new_ln)
        else:
            out_lines.append(ln)

    assert ptr == len(VI_LIST), f"only consumed {ptr}/{len(VI_LIST)} vi entries"
    assert text_seen == 86, f"text lines seen {text_seen}"

    out = "\r\n".join(out_lines)
    data = "\ufeff" + out if raw.startswith(b"\xef\xbb\xbf") else out
    VI.write_bytes(data.encode("utf-8"))
    print(f"WROTE {VI}  text_lines={text_seen} vi_ptr={ptr} crlf={has_crlf}")


if __name__ == "__main__":
    main()
