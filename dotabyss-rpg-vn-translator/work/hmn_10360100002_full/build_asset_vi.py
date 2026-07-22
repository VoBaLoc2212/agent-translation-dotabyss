# -*- coding: utf-8 -*-
"""
Field-index generator for hmn_10360100002 (EN-asset-is-English case, JP title only).
Source: E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100002.txt
Output: E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100002.txt
Strategy: field-index build. For message,* replace field index 2 (text field),
mirroring the source trailing suffix "<br> " (92 lines) / no suffix (title L33).
Preserves BOM, CRLF, delimiters, tags (<br>), %user%, speaker/voice/chara fields.
"""
import io, os

EN_PATH = r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100002.txt"
VI_PATH = r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100002.txt"

# line_no (1-based) -> VI text field (trailing "<br> " mirrored exactly; title none)
VI = {
    33:  "Phó Quan Lại Là Tại Tôi Cơ À!",
    46:  "…Một chiến dịch lấy chúng ta làm trọng tâm à?<br> ",
    48:  "Ừ. Lime‚ tôi nhờ cậu giải thích nhé.<br> ",
    104: "—Chiến dịch lần này không do Tiền Tuyến Căn Cứ đảm nhiệm‚<br>mà do một mình Đoàn Kỵ Sĩ Milesgard thực thi.<br> ",
    109: "Nội dung là thám sát một khu vực chưa khám phá mới được phát hiện<br>ở tầng trên của Đại Huyệt.<br> ",
    120: "…Một nhiệm vụ nguy hiểm. Sao chỉ mình chúng ta phải thực hiện?<br> ",
    131: "Chuyện đó có liên quan đến ý định của các nước…<br> ",
    139: "Dưới sự chỉ huy của Chỉ Huy‚ việc thám hiểm Đại Huyệt<br>đã đạt được tiến triển nhất định.<br> ",
    148: "Thế nhưng‚ người ta bắt đầu lo ngại rằng thành quả này<br>có thể là nhờ đặc tính riêng của Tiền Tuyến Căn Cứ.<br> ",
    160: "…Vậy nếu Đại Huyệt chỉ thám hiểm được bằng quân Tiền Tuyến Căn Cứ‚<br>thì các nước tài trợ sẽ nổi giận sao?<br> ",
    171: "Nhãn quan của ngài thật sắc bén‚ Tiểu thư Reyzeria!<br> ",
    183: "Để trấn an sự bất mãn của các nước khác‚ Đoàn Kỵ Sĩ<br>Milesgard phải tự mình đảm nhận chiến dịch này.<br> ",
    190: "Đại khái ta hiểu rồi. Thế… ngươi có nghĩ chiến dịch này sẽ thành công không?<br> ",
    231: "Tôi không phủ nhận đây là một thử thách nguy hiểm. Chính vì thế tôi<br>mới chỉ có thể trông cậy vào ngươi.<br> ",
    233: "Đoàn Kỵ Sĩ Milesgard do Reyzeria dẫn dắt. Nếu có ai đó hoàn thành được<br>nhiệm vụ này‚ thì chỉ có các ngươi.<br> ",
    244: "Hừm. Nghe cũng hay đấy.<br> ",
    255: "…Nhưng chọn chúng ta là quyết định đúng đắn.<br> ",
    257: "Ngươi sẽ nhận lời chứ?<br> ",
    268: "Bị nhờ vả đến mức đó mà từ chối thì tư cách kỵ sĩ củng cố gì nữa.<br>Tôi sẽ đáp lại kỳ vọng của ngươi.<br> ",
    279: "Chính vì nhiệm vụ gian nan nên mới bộc lộ được bản lĩnh thực sự của chúng ta.<br>Ngươi cứ nhìn kỹ sức mạnh của những kỵ sĩ mình đã chọn đi.<br> ",
    303: "Reyzeria vui vẻ bật cười rồi ung dung bước ra khỏi phòng chỉ huy.<br> ",
    335: "Phù‚ ít nhất cũng thuyết phục được cô ấy nhận nhiệm vụ. Giờ chỉ cần<br>cho nó thành công là xong.<br> ",
    346: "T–tên này…!<br> ",
    348: "Hm? Sao thế‚ Lime?<br> ",
    390: "Đồ ngốc gỗ‚ đồ nịnh hót‚ mặt dày vô sỉ…! Tôi không tha thứ cho ngươi<br>vì đã làm Tiểu thư Reyzeria mỉm cười như thế!<br> ",
    392: "*Thở dài*!? Nãy là đang bốc cháy vì nghĩa vụ sau khi<br>được giao nhiệm vụ nguy hiểm đấy chứ‚ có phải không!?<br> ",
    403: "Tiểu thư Reyzeria vui vẻ đến thế‚<br>chính là vì người giao nhiệm vụ cho cô ấy là ngươi!<br> ",
    414: "Huống chi‚ kế hoạch ta vạch ra đâu có nguy hiểm<br>đến mức này cơ chứ!?<br> ",
    423: "Sao nó lại biến thành chiến dịch nguy hiểm tính mạng thế này!?<br> ",
    425: "Đối thủ là Reyzeria đó? Cô ấy sẽ lập tức thấy rõ<br>một kế hoạch chỉ được dàn dựng để cho cô ấy tỏa sáng.<br> ",
    436: "T–tôi cũng nghĩ vậy. Nếu là Tiểu thư Reyzeria thì…<br> ",
    438: "Để cô ấy thực sự phát huy sức mạnh trong một chiến dịch nguy hiểm thực sự—<br>như thế mới ra kết quả tốt hơn chứ‚ đúng không?<br> ",
    449: "Chuyện đó… tôi không thể phủ nhận‚ nhưng…<br> ",
    451: "Tôi cũng sẽ đi thám hiểm cùng. Có tôi‚ Lime và Reyzeria‚<br>thì nhiệm vụ nào chẳng hoàn thành.<br> ",
    464: "…Anh đấy‚ đừng có kéo lùi chân bọn tôi nhé.<br> ",
    466: "Thêm chút kính trọng với Chỉ Huy đi‚ ngươi…<br> ",
    497: "Chiến dịch đặc biệt của Đoàn Kỵ Sĩ Milesgard: chiến dịch<br>thám hiểm Đại Huyệt.<br> ",
    499: "Tiến vào sâu Đại Huyệt‚ Đoàn Kỵ Sĩ Milesgard thể hiện bước tiến<br>vùi dập với Reyzeria ở vị trí trung tâm.<br> ",
    535: "*Thở dốc*! Lũ quái vật kia‚ ta không để các ngươi cản đường!<br> ",
    584: "Gùùùù!?<br> ",
    634: "Tiểu thư Reyzeria đỉnh thật…! Lũ quái vật chả là gì trước cô ấy!<br> ",
    645: "Một trận chiến tuyệt đẹp làm sao…! Chúng ta cũng tiếp tục thôi!<br> ",
    689: "Đừng có quá sức! Luôn đối đầu quái vật theo nhóm!<br> ",
    745: "Vâng‚ thưa ngài!<br> ",
    747: "Hưởng ứng trận chiến của Reyzeria‚ các binh sĩ Milesgard cũng<br>phát huy sức mạnh vượt giới hạn.<br> ",
    792: "Đúng là Tiểu thư Reyzeria! Cô ấy ở tiền phong đẩy lùi<br>quái vật đồng thời chỉ huy thuộc hạ trơn tru!<br> ",
    803: "Cô ấy thực sự phi thường! Tôi lấy làm tự hào khi được làm phó quan của Tiểu thư Reyzeria…!<br> ",
    805: "Ừ‚ cô ấy mạnh kinh hồn. Tôi tưởng đây là nhiệm vụ khó‚<br>nhưng có cô ấy thì có vẻ chẳng thành vấn đề.<br> ",
    863: "…Tôi chưa thể lơ là được.<br> ",
    867: "Reyzeria? Sao thế? Chẳng phải ngươi phải ở tiền tuyến sao?<br> ",
    879: "Bên đó thì đồng đội đang kiểm soát. Trong lúc đó ta muốn nghe ý kiến của ngươi.<br> ",
    890: "Địch đông nhưng toàn tiểu tốt.<br>Thế mà chẳng có vẻ bỏ chạy‚ cứ thế xông tới không ngừng.<br> ",
    902: "Dù là quái vật đi nữa‚ cảm giác này vẫn sai sai.<br>Ngươi thấy tình huống này thế nào?<br> ",
    904: "Hừm…<br> ",
    915: "Ư–ưm‚ Tiểu thư Reyzeria?<br> ",
    927: "À‚ Lime‚ cậu nghĩ cùng ta nhé.<br>Ta có dự đoán rồi‚ nhưng muốn độ chắc chắn cao hơn.<br> ",
    936: "V–vâng…<br> ",
    938: "Có lẽ lũ quái vật đang chiến đấu bây giờ bị một con lớn ở phía sau<br>đuổi tới‚ ép chạy về phía chúng ta.<br> ",
    940: "Bởi vậy dù là tiểu tốt vẫn không bỏ chạy‚ mà cứ thế<br>nhào tới tuyệt vọng.<br> ",
    951: "…Trùng với suy nghĩ của ta. Phần chính vẫn còn ở phía sau.<br> ",
    962: "T–tôi cũng cùng ý kiến!<br> ",
    974: "Tốt. Lime‚ dừng tiến quân. Lập trận hình đề phòng Quái Thú.<br> ",
    985: "V–vâng! Tôi sẽ lập tức truyền lệnh cho toàn quân!<br> ",
    996: "Nhờ cậu đấy. Tôi ra tiền tuyến giảm bớt số lượng!<br> ",
    1049: "Reyzeria lao khỏi chỗ đó‚<br>trong chớp mắt đã phóng về lại tiền tuyến.<br> ",
    1051: "Lại điềm tĩnh ngay giữa chiến trận‚ hử. Đúng là khí chất của kẻ đứng đầu.<br> ",
    1053: "Mắt nhìn của ngươi rất chuẩn đấy‚ Lime. …Lime?<br> ",
    1089: "…Tại sao? Sao lại thế này?<br> ",
    1091: "C–có chuyện gì thế?<br> ",
    1102: "Phó quan của Tiểu thư Reyzeria là tôi mà! Sao cô ấy lại đi hỏi ý ngươi thay vì tôi!?<br> ",
    1104: "Ư‚ ừm… Chắc là vì tôi rành Đại Huyệt hơn ngươi chứ gì?<br> ",
    1115: "Dù vậy‚ tôi muốn cô ấy hỏi ý kiến người phó quan là tôi trước‚<br>chứ đâu phải một kẻ Chỉ Huy–hóa–thành–khách–du–lịch–Đại–Huyệt như thế…!<br> ",
    1117: "Đúng là tôi chỉ đứng nhìn để Reyzeria tỏa sáng‚ nhưng đâu cần<br>nói cay nghiệt như thế…<br> ",
    1145: "—Và đúng như dự đoán‚ Quái Thú xuất hiện rồi bị Đoàn Kỵ Sĩ Milesgard<br>với tư thế chờ sẵn hoàn hảo đánh bại tuyệt đẹp.<br> ",
    1187: "Toàn quân‚ luân phiên nghỉ ngơi! Nghỉ ngơi cũng là một phần nhiệm vụ‚<br>đừng có bảo là vẫn còn mệt!<br> ",
    1245: "Tuân lệnh!<br> ",
    1272: "Suôn sẻ từ nãy đến giờ. Tiếp đà này thì nhiệm vụ thực sự có thể thành công.<br> ",
    1307: "Vâng‚ mọi công trạng đều nhờ sức của Tiểu thư Reyzeria!<br> ",
    1318: "*Thở dài*… Tiểu thư Reyzeria đúng là tuyệt vời. Đánh là thắng‚<br>bảo vệ dân chúng‚ tâm hồn không vương một gợn mây!<br> ",
    1329: "Thế mà lũ người ở bản quốc lại làm mấy chuyện cản đường<br>Tiểu thư Reyzeria…<br> ",
    1331: "Chắc vì cô ấy xuất chúng‚ đúng không? Chính vì ưu tú nên mới<br>đố kỵ‚ oán hận‚ coi là kẻ thù.<br> ",
    1333: "Vì nghĩ chỉ thắng được khi giữ khoảng cách xa‚ nên chúng<br>dốc sức kéo lùi chúng ta.<br> ",
    1344: "Ngu ngốc làm sao! Thà quy phục dưới trướng Tiểu thư Reyzeria<br>còn có tương lai sáng ngời hơn!<br> ",
    1355: "Người đó chỉ chiến đấu vì dân‚ vì chính nghĩa. Được đi theo<br>Tiểu thư Reyzeria đúng là hạnh phúc.<br> ",
    1357: "Cậu thực sự kính trọng cô ấy đấy… Giờ mới thấy cái gọi là charisma.<br> ",
    1359: "Nhưng mà‚ Reyzeria đúng là ghê gớm‚ không nghi ngờ gì‚ nhưng tôi nghĩ cậu cũng<br>ghê gớm chẳng kém‚ Lime.<br> ",
    1370: "Cái gì… Tôi ngang hàng với Tiểu thư Reyzeria ư?<br>Đừng nói bậy thế!<br> ",
    1372: "Tôi không nịnh đâu.<br>Đó là lời thật lòng với tư cách chỉ huy của cậu.<br> ",
    1383: "Càng tệ hơn nữa!<br>Khả năng nhìn thấu con người là tư chất quan trọng nhất của một chỉ huy!<br> ",
    1394: "Tôi không thể không nghi ngờ năng lực chỉ huy của cậu!<br> ",
    1410: "N–này‚ Lime!<br> ",
    1412: "Lime trừng mắt nghiêm nghị‚ giơ súng lên và chĩa nòng vào %user%.<br> ",
    1429: "Mắt ta đã mù…! Ngươi không xứng đứng bên cạnh Tiểu thư Reyzeria!<br> ",
}

def main():
    with io.open(EN_PATH, "r", encoding="utf-8-sig", newline="") as f:
        content = f.read()
    has_crlf = "\r\n" in content
    lines = content.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    out_lines = []
    text_cmds = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
    replaced = 0
    for idx, ln in enumerate(lines):
        s = ln.rstrip("\r")
        file_lineno = idx + 1
        if s.startswith(text_cmds) and file_lineno in VI:
            replaced += 1
            vi_text = VI[file_lineno]
            if s.startswith("title,"):
                parts = s.split(",", 1)
                new = parts[0] + "," + vi_text
            else:
                parts = s.split(",", 5)
                new = ",".join(parts[:2] + [vi_text] + parts[3:])
            out_lines.append(new)
        else:
            out_lines.append(s)
    if has_crlf:
        joined = "\r\n".join(out_lines) + "\r\n"
    else:
        joined = "\n".join(out_lines) + "\n"
    os.makedirs(os.path.dirname(VI_PATH), exist_ok=True)
    with io.open(VI_PATH, "wb") as f:
        f.write(b"\xef\xbb\xbf" + joined.encode("utf-8"))
    print("Replaced text lines:", replaced, "/", len(VI))
    print("Output written:", VI_PATH, "CRLF:", has_crlf)

if __name__ == "__main__":
    main()
