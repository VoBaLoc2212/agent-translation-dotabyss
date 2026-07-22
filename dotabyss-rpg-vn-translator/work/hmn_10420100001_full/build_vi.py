#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate VI asset for hmn_10420100001 (mixed JP-title / EN-message case).

EN asset text fields are English (en.json populated). Title field is still JP.
Translate EN->VI for message* fields, JP->VI Title Case for title.
Mirror each message,* trailing <br>  suffix exactly; keep messageTextCenter
<size=48>...</size> verbatim (with its ,,,on suffix). Preserve BOM/CRLF/line count.

Record order (text-command sequence, file order):
  1 title
  2..70 messages (69)
  71 messageTextCenter  (—A few minutes later.)
  72..91 messages (20)
  92 messageTextCenter  (—The next day.)
  93..101 messages (9)
Total = 1 + 98 + 2 = 101 text records.
"""
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100001.txt"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TRAIL_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# seq-keyed VI text fields (file order, text-command lines only)
# message,* entries EXCLUDE the trailing <br>  suffix (mirrored at build time)
VI_DICT = {
    # 1 title (JP -> VI Title Case)
    1: "Hãy Ngủ Đi Được Nuốt Chửng Bởi Bóng Tối Của Ta!",
    # 2..70 messages (EN -> VI)
    2: "Grào!",
    3: "Chỉ Huy! Thêm kẻ địch nữa!",
    4: "...Chuyện này tệ thật. Nhiều kẻ địch hơn mức ta dự liệu.<br>Không muốn bị kẹt lại ở đây đâu—",
    5: "Ta cần một lối thoát—Ừm?",
    6: "Đúng lúc ấy‚ một cô gái vươn mình nhảy vọt lên trên đầu con quái thú.",
    7: "Hyah!",
    8: "Cô gái đâm thanh đại kiếm vào quái thú‚ hạ gục con mồi khổng lồ.<br>Lính tráng rên lên vì choáng ngợp.",
    9: "Fufu... Ta thấy rồi! Con Đường Máu — con đường tắm máu dẫn lũ kẻ thù<br>đến Valhalla!",
    10: "Lũ Thú (Marionette) bị kẻ Thao Túng sai khiến làm sao mà cản nổi<br>con đường vinh quang của ta được!",
    11: "Ngủ đi‚ được nuốt chửng bởi bóng tối của ta!... Kukuku‚ Kuhahaha!<br>Này các chiến binh! Đi theo ta! Đừng tụt lại phía sau!",
    12: "...C-cô ta là ai vậy? Có hơi đáng sợ...",
    13: "N-nhưng mà cô ta mạnh thật‚ nên tạm thời đi theo thôi...?",
    14: "Hyah!",
    15: "Dù lính tráng giữ khoảng cách‚ cô gái lại vượt lên trên đầu con quái<br>thú. Thế trận xoay chuyển có lợi‚ và Chỉ Huy thở phào nhẹ nhõm.",
    16: "(Bọn họ có vẻ bất an‚ nhưng ta nên cảm ơn cô gái đó.<br>Đợi chút nữa chiến trận lắng xuống‚ ta sẽ bắt chuyện với cô ấy.)",
    17: "Haa...",
    18: "Xin lỗi‚ tôi biết anh đang mệt‚ nhưng cho tôi một chút thời gian được không?",
    19: "Có chuyện gì thế‚ thưa Chủ Nhân của ta?",
    20: "Ừm? Chủ nhân? Tôi là Chỉ Huy mà.",
    21: "Ngài là bậc bề trên của ta‚ nên ngài là Chủ Nhân của ta. Đến bao giờ ngài sẽ<br>đi cùng ta trên con đường này ở chiều không gian này thì không ai hay — chỉ có thần mới biết.",
    22: "...Tôi chẳng hiểu lắm‚ nhưng tôi muốn nói chuyện với người lính đã lập công<br>lớn như vậy. Được chứ?",
    23: "Nói ngắn gọn thôi. Sau trận chiến‚ sức Bóng Tối dễ rò rỉ ra.<br>Ta chỉ mong kìm nén nổi thôi.",
    24: "...Á! Cái mắt trái bị phong ấn của ta vừa bắt đầu nhói lên— Thưa Chủ Nhân‚<br>nếu ngài có điều muốn nói thì hãy nhanh lên trong khi ta vẫn còn tỉnh táo!",
    25: "Vậy là sức mạnh của ngươi có bí mật‚ và dùng nó thì có rủi ro!<br>Nếu ngươi không khỏe thì tôi sẽ gọi y tá—",
    26: "K-khoan đã! Khoan đã‚ thưa Chủ Nhân của ta!",
    27: "Hả? Không‚ nhưng—",
    28: "...Ta không muốn làm chuyện to chuyện nhỏ vô ích. Hiểu cho ta.<br>Ta sẽ nghe yêu cầu của ngài.",
    29: "...Được rồi. Đầu tiên‚ hãy cho ta biết tên ngươi.",
    30: "Ngài muốn biết Chân Danh của ta sao?",
    31: "...Chân Danh là cái gì?",
    32: "Ừm?",
    33: "Này‚ 'Thiên Thần'‚ ngươi nghĩ sao? Ngươi giả vờ ngu dốt<br>nhưng xem ra có thể là tay chân của kẻ Thao Túng.",
    34: "A‚ ah... phải. Dù chỉ là vai tạm thời‚ ta cũng chỉ là một quân cờ.<br>Ta sẽ không chống lại. Ở đây‚ ta chỉ khai ra bí danh thôi.",
    35: "Rốt cuộc ngài đang nói chuyện với ai vậy?",
    36: "Nếu ngài biết được điều đó‚ ta không còn cách nào khác ngoài việc xóa sổ ngài...",
    37: "Đột nhiên nguy hiểm thế kia luôn!",
    38: "...Nếu có kẻ tiếp cận tương lai khoa học thì sẽ gây nghịch lý thời gian‚<br>ngăn tận thế. ...Và ngài cứ gọi ta là Hield de Zieger cũng được.",
    39: "Này‚ Hayley.<br>Cô quên lương thực khẩn cấp rồi. Tôi để đây nhé.",
    40: "...Ể!? Sao tôi đã bảo bao nhiêu lần là Chân Danh của ta đặc biệt<br>nên đừng gọi bừa bãi thế kia rồi mà!!!",
    41: "Vậy là cô tên Hayley à. Một cái tên không tệ.",
    42: "Hô... Ngài có hứng thú với âm hưởng của Chân Danh sao. Xem ra ngài cũng<br>có tư cách đuổi theo chân tướng Vạn Vật mà tổ chức đã che giấu bằng lời Nói Dối.",
    43: "Ư... khoan đã. Đừng tung thêm thông tin gì nữa.<br>Để ta tổng hợp lại lời ngài nói đã.",
    44: "Tóm lại thì‚ ngươi đang chiến đấu vì chân tướng với cái Bóng Tối đó‚<br>nhưng có kẻ địch nào đó mà ngươi đang đề phòng.",
    45: "…!",
    46: "Ngươi đến Đại Huyệt chiến đấu‚ vậy kẻ địch đó dính líu đến<br>chuyến thám hiểm hay quái thú à? ...Và ngươi muốn hạ gục bọn chúng?",
    47: "...K-không thể nào! Mới gặp nhau chưa bao lâu mà ngươi đã thấu được<br>ý định thật sự của ta rồi ư? Không thể tin nổi! Ngươi‚ thuộc về đâu? Ngươi mang cờ của ai!",
    48: "Trước khi đến Căn Cứ Tiền Tuyến tôi ở nơi khác‚ nhưng giờ tôi không thuộc<br>về tổ chức nào khác ngoài đây.",
    49: "...Có vẻ ký ức của ngài vẫn chưa trở lại.",
    50: "Ể? Tôi đã gặp ngài ở đâu đó trước đó sao?",
    51: "Vừa đúng lại vừa không...",
    52: "Ư‚ à... tức là ngài không biết. Nhưng ngài đang hy vọng là chúng ta đã từng gặp nhau phải không?",
    53: "...Ôôôôô!",
    54: "(Tuyệt vời‚ trúng phóc! Cảm giác thỏa mãn bí ẩn gì thế này!!!)",
    55: "Thú vị! Thật thú vị! Ta đang vô cùng hưng phấn! Thưa Chủ Nhân!<br>Chắc chắn ngài cũng thấu hiểu được sự rung động này trong ngực ta chứ‚ đúng không!",
    56: "Ý anh là anh rất vui vì chúng ta có thể giao tiếp được đúng không?",
    57: "Fufufu! Đúng như ta nghĩ——<br>Xem ra ta cuối cùng đã kết duyên nhân quả với kiếp trước——",
    58: "Ở kiếp trước‚ chúng ta hoặc là bạn hữu không ai thay thế được‚ hoặc là<br>kỳ địch chiến đấu suốt đời. Anh hùng hay kẻ ác——rốt cuộc là bên nào?",
    59: "Sau khi ký ức của ngài trở lại‚ chúng ta có thể trở thành kẻ địch‚ nhưng<br>giờ hãy mừng ngày tái ngộ và vui vì ta có thể chiến đấu ngang hàng.",
    60: "Ừ‚ ừm‚ đúng vậy. Tôi mừng là ta hợp nhau. Dù sao ngươi cũng tài giỏi.<br>Tôi trông cậy ngươi cho phần còn lại của chuyến thám hiểm đấy.",
    61: "Fufu‚ hiểu rồi. Thưa Chủ Nhân. Không‚ theo luật của ngài thì giờ tôi sẽ gọi<br>ngài là Chỉ Huy. Đêm nay‚ tôi sẽ thành thanh gươm của ngài... cho đến khi tái ngộ.",
    62: "...Suýt soát là xong xuôi‚ nhưng... đúng là một cô nương bất trị.",
    63: "Hayley lúc nào cũng thế mà‚ anh biết không...",
    64: "Chúng tôi không tài nào bắt chuyện được với cô ấy kiểu đó. Lần đầu tôi<br>thấy một cuộc đối thoại thực sự... Đúng là Chỉ Huy có khác.",
    65: "Nghe thế thì mấy người cũng vất vả không kém... Không lẽ<br>chẳng có ai thân thiết với cô ấy sao?",
    66: "Tôi chưa thấy ai cả. Vốn dĩ chẳng ai dám lại gần cô ấy.",
    67: "Không biết vì sao cô ấy thành ra thế nhỉ... Nhìn trang bị thì<br>có vẻ không phải xuất thân từ gia cảnh nghèo khó.",
    68: "Chẳng ai biết về nguồn gốc của Hayley sao?",
    69: "Chắc không đâu. Tôi nghe nói có người từng hỏi‚ nhưng cô ấy chỉ bảo<br>'một anh hùng phải biết chờ thời' rồi chẳng chịu trả lời.",
    70: "Hmm…",
    71: "<size=48>—Vài Phút Sau.</size>",
    72: "Hãy bị bóng tối của ta nuốt chửng! Hyah!",
    73: "GRÀOO!",
    74: "*Bịch*",
    75: "Xin ân huệ giáng xuống những linh hồn khốn khổ này... Amen.",
    76: "(Tôi chẳng hiểu lắm‚ nhưng cô ấy tài thật.)",
    77: "...Tôi không muốn đến quá gần‚ nhưng chỗ của Hayley chính là lối thoát!<br>Đi theo tôi!",
    78: "Haa... suýt soát an toàn rồi. Chuyến thám hiểm này thành công lớn.<br>Nhờ có cô đấy‚ Hayley. Cảm ơn cô.",
    79: "Đừng khách sáo‚ thưa Chỉ Huy của tôi. Tiêu diệt quái thú là gánh nặng thề<br>nguyền của dòng tộc tôi. Tôi đã đáp lại tiếng gọi của định mệnh nhân quả ấy.",
    80: "Ừm? Vậy gia đình ngươi làm nghề săn quái vật—",
    81: "Ô-ô kìa! Tiểu thư! Cuối cùng tôi cũng tìm được ngài! Hôm nay ngài<br>rực rỡ hơn bao giờ hết!",
    82: "Á!",
    83: "Sao thế ạ? Là tôi đây‚ người hầu cũ của ngài. Tôi đến Căn Cứ Tiền Tuyến<br>để thăm ngài đấy.",
    84: "T-tôi biết‚ tôi biết rồi! Vậy nên xin ngài‚ giờ cứ để tôi yên!",
    85: "Đột nhiên sao thế? Sao ngươi bối rối thế?",
    86: "Không gì khiến ta sợ hãi ngoài Kẻ Thao Túng — kẻ cai trị các Thế Giới<br>Song Song. Bóng Tối chẳng hề dao động dù dưới sắc thái nào!",
    87: "...Tiểu thư. Đừng bảo là... lại là chuyện đó nữa rồi?",
    88: "Ực...",
    89: "...Tôi xin lỗi mọi người. Tôi có chuyện cần bàn với tiểu thư.<br>Tiểu thư‚ phiền ngài đi cùng tôi một chút được không?",
    90: "V-vâng... Chỉ Huy‚ tôi xin phép cáo từ...",
    91: "...Ừm? Vừa rồi là sao thế?",
    92: "<size=48>—Ngày Hôm Sau.</size>",
    93: "(Được rồi. Hôm nay ta tiếp tục chuyến thám hiểm của hôm qua. ...Ồ? Là<br>Hayley.)",
    94: "...A‚ Chỉ Huy. Tôi mong được tiếp tục hợp tác với ngài hôm nay!",
    95: "...Hả? Cô sao thế? Cách nói của cô khác hẳn<br>so với hôm qua mà!",
    96: "X-xin ngài đừng bận tâm. Dù cách nói có khác‚ tôi vẫn sẽ hoàn thành<br>nhiệm vụ... Tôi phải chuẩn bị khởi hành‚ nên xin phép.",
    97: "Á‚ khoan—",
    98: "Hmph‚ cô ấy đã đi mất rồi.",
    99: "...Này. Anh đã nói chuyện với Hayley chưa?",
    100: "Ừm... Tôi chưa từng thấy Hayley như thế. Không biết cô ấy đã<br>trải qua chuyện gì.",
    101: "(Sự bất an cũng đang lan sang đám lính. Hy vọng nó không gây<br>tác dụng tiêu cực...)",
}

def preflight(en_lines):
    seq = 0
    errs = []
    for ln in en_lines:
        body = ln[:-2] if ln.endswith("\r\n") else ln
        for cmd in TEXT_CMDS:
            if body.startswith(cmd):
                seq += 1
                parts = body.split(",", 5)
                en_tf = parts[2] if cmd != "title," else parts[1]
                vi = VI_DICT.get(seq, None)
                if vi is None:
                    errs.append(f"MISSING seq {seq} for line {body[:30]!r}")
                    continue
                if "," in vi:
                    errs.append(f"ASCII_COMMA seq {seq}: {vi!r}")
                if cmd != "title," and cmd != "messageTextCenter,":
                    en_br = en_tf.count("<br>")
                    core_en = re.sub(TRAIL_RE, "", en_tf)
                    if vi.count("<br>") != core_en.count("<br>"):
                        errs.append(f"BR_MISMATCH seq {seq}: en_core_br={core_en.count('<br>')} vi_br={vi.count('<br>')} ({vi!r})")
                    tags_vi = set(re.findall(r"<[^>]+>", vi))
                    tags_en = set(re.findall(r"<[^>]+>", core_en))
                    if tags_vi != tags_en:
                        errs.append(f"TAG_MISMATCH seq {seq}: en={tags_en} vi={tags_vi}")
    if seq != len(VI_DICT):
        errs.append(f"RECORD_COUNT seq={seq} dict={len(VI_DICT)}")
    return errs

def build():
    data = EN.read_bytes()
    en_text = data.decode("utf-8-sig")
    en_lines = en_text.splitlines(keepends=True)
    errs = preflight(en_lines)
    if errs:
        print("PREFLIGHT FAILED:")
        for e in errs:
            print("  ", e)
        raise SystemExit(1)
    print("preflight OK: all <br>/ASCII-comma/tag/count guards passed")

    out = []
    seq = 0
    for raw_line in en_lines:
        body = raw_line[:-2] if raw_line.endswith("\r\n") else raw_line
        ending = raw_line[len(body):]
        is_title = body.startswith("title,")
        is_center = body.startswith("messageTextCenter,")
        is_msg = body.startswith("message,") or body.startswith("messageTextUnder,")
        if is_title or is_center or is_msg:
            seq += 1
            parts = body.split(",", 5)
            vi = VI_DICT[seq]
            if is_title:
                parts[1] = vi
            elif is_center:
                parts[2] = vi
            else:
                suf = re.findall(TRAIL_RE, parts[2])
                suffix = suf[-1] if suf else ""
                parts[2] = vi + suffix
            out.append(",".join(parts) + ending)
        else:
            out.append(raw_line)
    result = "".join(out)
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(b"\xef\xbb\xbf" + result.encode("utf-8"))
    print(f"wrote {VI} ({len(en_lines)} lines, {len(result.encode('utf-8'))} bytes)")

if __name__ == "__main__":
    build()
