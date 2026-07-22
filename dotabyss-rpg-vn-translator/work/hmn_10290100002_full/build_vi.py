#!/usr/bin/env python3
# Build VI output for hmn_10290100002 from the EN asset (EN-asset-is-English condition).
# ja.json = JP primary meaning; en.json = English meaning; EN asset = structural authority.
# Field-index approach: only text field (parts[2], or parts[1] for title) is replaced.
# All delimiter / speaker / ID / voice fields are preserved byte-identical.
# Vietnamese uses '‚' (U+201A) for commas; <br> counts mirrored exactly from EN asset.
import sys
from pathlib import Path

ROOT = Path(r"E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100002.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100002.txt"

data = EN.read_bytes()
has_crlf = b"\r\n" in data
text = data.decode("utf-8-sig")
lines = text.split("\n")  # each element may still carry trailing '\r'

TITLE = "Với Tư Cách Là Thợ Làm Bánh Của Vương Quốc Bánh Ngọt"
CENTER = "<size=48>—Vài Ngày Sau.</size>"

MSG = {
    47: "Đã muộn thế này rồi... hôm nay ta đã làm việc hơi quá sức một chút.<br> ",
    58: "...Hừm? Mùi thơm ngọt ngào‚ thoảng thoảng này là gì thế?<br> ",
    60: "...Ta đi xem thử một chút vậy.<br> ",
    94: "Ứ... mình phải làm sao đây...?<br> ",
    109: "(Myrtille à? Nàng nướng bánh tới tận đêm muộn thế này...)<br> ",
    139: "Bánh tart này thì quá đơn giản‚ nhưng cái kia thì rời rạc... Ừ‚ hay là mình gộp<br>cả hai thành một cái luôn!<br> ",
    172: "Này‚ Myrtille?<br> ",
    189: "Oa!<br> ",
    198: "Chỉ Huy! Ngài đến đây vào giờ muộn thế này làm gì?<br> ",
    200: "Đáng ra ta mới là người phải hỏi em điều đó. Em đang làm đồ bán cho<br>ngày mai à?<br> ",
    208: "Không đâu! Bây giờ mình đang làm bánh tart cho Cuộc Thi Bánh Ngọt.<br> ",
    210: "Cuộc Thi Bánh Ngọt à? ...À‚ cuộc thi nướng bánh mà họ tổ chức ở<br>căn cứ đúng không?<br> ",
    221: "Đây là cuộc thi cực kỳ quan trọng để chọn ra thợ làm bánh số một của<br>căn cứ!<br> ",
    232: "Với tư cách là thợ làm bánh từ Vương Quốc Bánh Ngọt‚ Mil nhất định phải thắng.<br> ",
    234: "Ta không biết Vương Quốc Bánh Ngọt là nơi ra sao‚ nhưng ta hiểu em không<br>thể thua được.<br> ",
    238: "Nhưng không có gì phải lo đâu. Bánh tart được Mil làm bằng cả tấm lòng thì<br>khó mà thua dễ dàng thế đâu.<br> ",
    249: "Nhưng‚ nhưng! Dù mình có làm bao nhiêu đi nữa‚ mình cũng chẳng thể thấy \"\"Đây chính là<br>nó!\"\"<br> ",
    258: "Mình chẳng chọn nổi nên đưa loại tart nào đi thi nữa!<br> ",
    269: "Loại tart nào cũng có điểm hay riêng của nó‚ em biết không? Mình không thể chọn<br>ra cái nào là nhất được!<br> ",
    271: "Vậy ra rắc rối của em là tại em yêu bánh tart quá nhiều đó hử... Thôi‚ sao<br>em không nhờ ai đó nếm thử xem?<br> ",
    282: "Ra thế! Mil cần một ý kiến công bằng! Vậy thì‚ Chỉ Huy‚ hãy chọn giúp Mil một<br>cái được không?<br> ",
    284: "Ta á? Ta có thể nếm thử‚ nhưng ta chẳng phải chuyên gia bánh ngọt gì cho lắm...<br> ",
    313: "Gâu‚ gâu‚ gâu?<br> ",
    315: "Ừ‚ tốt hơn là nhờ một người quen thuộc với bánh ngọt của em hơn‚ một<br>người yêu bánh tart đích thực‚ chọn thì hơn...<br> ",
    327: "Khoan đã‚ em... là gấu à!<br> ",
    333: "Gâu.<br> ",
    335: "Chú gấu con‚ kẻ đã lẻn vào bếp mà không ai hay biết‚ đã giơ một<br>cái chân lên như thể nói 'Chào buổi tối!'<br> ",
    366: "Ồ‚ anh Gấu! Hôm nay anh cũng tới nữa à!<br> ",
    368: "Gâu!<br> ",
    370: "Hắn hay tới đây lắm à?<br> ",
    378: "Ừ! Lúc không có ai‚ anh ấy lẻn tới ăn trộm bánh tart của Mil.<br> ",
    380: "Gâu‚ gâu‚ gâu‚ Gâuu!<br> ",
    382: "Trông hắn to hơn lần trước rồi đấy. Hắn được cưng chiều khá nhiều đây.<br> ",
    390: "Thôi‚ cẩn thận đừng để bị bắt. Ở đây có không ít kẻ có thể biến em thành<br>súp chỉ với một đòn đấy.<br> ",
    394: "Gâu...<br> ",
    396: "Chú gấu con cau mày như thể nói 'Đáng sợ thật...' Đó là một cử chỉ<br>kỳ lạ giống hệt con người.<br> ",
    406: "Nhưng có lẽ hắn tới đúng lúc cũng tốt. Hắn đã ăn bánh tart của em nhiều<br>lần rồi‚ nên hắn biết mùi vị chứ‚ phải không?<br> ",
    408: "Gâu?<br> ",
    410: "Để hắn nếm thử luôn đi.<br> ",
    452: "Ra là thế! Anh Gấu‚ làm ơn hãy chọn giúp xem loại tart nào ngon nhất được không?<br> ",
    454: "Gâu!<br> ",
    456: "Chú gấu con vỗ ngực như thể nói‚ 'Cứ giao cho tôi!'<br> ",
    499: "Đây là những chiếc bánh tart mà Mil đang phân vân—nên đưa loại nào đi thi<br>trong cuộc thi.<br> ",
    501: "Gâu‚ gâu gâu!<br> ",
    512: "Anh chắc chứ? Thế thì bắt đầu thử đi!<br> ",
    551: "Gâu!<br> ",
    555: "Chú gấu con thạo tay cầm dao nĩa cắt một chiếc bánh tart với sự điêu luyện<br>thuần thục.<br> ",
    557: "Khoan đã‚ khoan đã‚ khoan đã! Sao một con gấu lại dùng dao nĩa ăn bánh tart<br>điệu đàng thế!<br> ",
    597: "Mil nghĩ chân anh ấy sẽ dính bẩn nên mới đưa cho anh ấy‚ và anh ấy đã dùng<br>ngay lập tức.<br> ",
    599: "Gấu tài năng thật đấy...<br> ",
    635: "Chú gấu con thanh lịch đưa bánh tart lên miệng‚ gật đầu đầy suy tư‚ rồi bắt<br>đầu gừ gừ.<br> ",
    637: "Gâu‚ gâu gâu‚ gâu gâu.<br> ",
    639: "...Hắn dường như đang nói gì đó‚ nhưng ta chẳng hiểu chút nào hắn đang<br>nói gì.<br> ",
    650: "Hừm... nhưng hình như không được đánh giá cao lắm... Có lẽ sự cân bằng<br>nguyên liệu hơi bị lệch.<br> ",
    652: "Gâu... gâu‚ gâu gâu?<br> ",
    654: "Chú gấu con cầm chiếc bánh tart tiếp theo‚ áp mũi gần vết cháy mờ trên cạnh‚<br>rồi lắc đầu như thể nói 'chẹp chẹp'.<br> ",
    665: "Ồ! Nó bị cháy rồi! Chắc tại Mil nướng thử nhiều lần quá nên đã hơi lơ<br>đễnh với nhiệt độ...<br> ",
    667: "Gâu gâu. Gâu gâu.<br> ",
    678: "Ừm‚ Mil sẽ cẩn thận.<br> ",
    680: "Hắn là cái gì thế? Một tay sành ăn nào đó à?<br> ",
    684: "Gâu.<br> ",
    686: "Đừng có gật đầu. Không phải đâu‚ đúng không? Trời ạ‚ anh ta có gu<br>ẩm thực cực kỳ tinh tế đấy.<br> ",
    728: "Fufufu. Nhưng anh ta cũng đáng tin cậy đấy hử?<br> ",
    766: "Chú gấu con ăn hết mấy chiếc bánh tart và cuối cùng để lại một cái trên<br>bàn. Đó là một chiếc bánh tart đơn giản được trang trí bằng trái cây.<br> ",
    810: "Ể... c-cái này á? Bánh Tart Trái Cây Theo Mùa à?<br> ",
    812: "Gâu‚ gâu‚ gâu.<br> ",
    814: "Bánh tart trái cây cũng ngon mà‚ có gì đâu? Có vấn đề gì sao?<br> ",
    825: "Nó là món kinh điển ai cũng thích‚ nhưng chẳng có gì độc đáo! Trong cuộc<br>thi‚ nó dễ bị lẫn vào đám đông lắm!<br> ",
    862: "Gâu‚ gâu‚ gâu‚ gâu? Gâuu‚ gâu‚ gâu‚ gâu‚ gâu!<br> ",
    864: "Ta chẳng hiểu hắn đang hăng lên vì cái gì‚ nhưng... ta nghĩ hắn đang bảo em<br>hãy tự tin lên.<br> ",
    868: "Gâu!<br> ",
    870: "Bánh tart đơn giản giúp tài nghệ của Myrtille tỏa sáng‚ đúng không? Ta nghĩ<br>đó cũng là một lựa chọn tốt.<br> ",
    879: "Thắng bằng một chiếc bánh tart thông thường... khó quá‚ sẽ vất vả lắm!<br> ",
    890: "Nhưng... Mil là thợ làm bánh từ Vương Quốc Bánh Ngọt! Mil phải có thể thắng<br>bằng cái này cơ chứ!<br> ",
    892: "Gâu‚ gâu! Gâuu‚ gâu‚ gâu!<br> ",
    934: "Ừ! Mil sẽ không ngừng nâng cao chất lượng chiếc bánh tart này‚ và rồi Mil sẽ<br>thắng cuộc thi!<br> ",
    945: "Chỉ Huy! Anh Gấu! Mil nhất định sẽ thắng đấy‚ nghe chưa!<br> ",
    947: "Ừ‚ ta rất trông chờ đấy.<br> ",
    951: "Gâuu!<br> ",
}

# ---- preflight: compare <br> counts (source vs VI) and forbid ASCII commas ----
mismatches = []
ascii_comma = []
for i, raw in enumerate(lines, 1):
    cr = raw.endswith("\r")
    s = raw[:-1] if cr else raw
    if s.startswith("title,"):
        old_tf = s.split(",", 1)[1]
        new_tf = TITLE
    elif s.startswith("messageTextCenter,"):
        old_tf = s.split(",", 5)[2]
        new_tf = CENTER
    elif s.startswith("message,"):
        old_tf = s.split(",", 5)[2]
        new_tf = MSG.get(i)
        if new_tf is None:
            continue
    else:
        continue
    if old_tf.count("<br>") != new_tf.count("<br>"):
        mismatches.append((i, old_tf.count("<br>"), new_tf.count("<br>")))
    if "," in new_tf:
        ascii_comma.append(i)

if mismatches:
    print("PREFAILED <br> mismatches:")
    for m in mismatches:
        print("  line", m[0], "en=", m[1], "vi=", m[2])
if ascii_comma:
    print("PREFAILED ASCII comma in VI text at lines:", ascii_comma)
if mismatches or ascii_comma:
    sys.exit(1)
print("Preflight OK: <br> counts match, no ASCII commas in VI text fields.")

# ---- build ----
out = []
for i, raw in enumerate(lines, 1):
    cr = raw.endswith("\r")
    s = raw[:-1] if cr else raw
    if s.startswith("title,"):
        new = "title," + TITLE
    elif s.startswith("messageTextCenter,"):
        parts = s.split(",", 5)
        parts[2] = CENTER
        new = ",".join(parts)
    elif s.startswith("message,"):
        parts = s.split(",", 5)
        if i in MSG:
            parts[2] = MSG[i]
        new = ",".join(parts)
    else:
        new = s
    out.append(new + ("\r" if cr else ""))

result = "\n".join(out)
VI.write_bytes(b"\xef\xbb\xbf" + result.encode("utf-8"))
print("Wrote", VI, "lines=", len(out), "crlf=", has_crlf)
