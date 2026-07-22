#!/usr/bin/env python3
# Build VI asset for hmn_10410100002 (EN-asset-is-English case).
# EN asset text fields = structural + alignment authority; JP consulted for meaning.
# Source uses fullwidth comma \uff0c inside text fields (not ASCII ','), so we mirror it.
# Every message, line's text field carries a trailing '<br> ' suffix (br + space).
# Matching is by EN text-field content (unique substring / exact) -> robust to line shifts.
import re

ROOT = "E:/AgentTranslation"
EN = f"{ROOT}/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10410100002.txt"
VI = f"{ROOT}/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10410100002.txt"

TEXT_CMDS_PREFIX = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# Exact-match map (for ambiguous / non-ASCII fields)
EXACT = {
    "殺すべきではありませんか？": "Chẳng phải chúng ta nên giết bọn họ sao?",
    "...<br> ": "…<br> ",
}

# Unique-substring -> VI text field (full VI including internal <br> and trailing '<br> ' for message,)
SEARCH = {
    "Shall we not kill": "Chẳng Phải Chúng Ta Nên Giết Bọn Họ Sao?",
    "no one you would like me to kill": "Chẳng lẽ không có ai mà ngài muốn tôi giết sao?<br> ",
    "Commander of this base": "...Tôi là Chỉ Huy của căn cứ này mà，ngài biết không? Tôi chẳng có ai để<br>mà ám sát đâu.<br> ",
    "With a position like yours": "Thế ạ? Với một vị trí như của ngài，tôi nghĩ những trở ngại sẽ<br>tự nhiên tăng lên thôi.<br> ",
    "can't completely deny": "Tôi cũng chẳng thể phủ nhận hoàn toàn chuyện đó……<br> ",
    "Would you not agree": "Phải không ạ? Nếu ngài giết những kẻ đó，cuộc sống thường ngày của ngài sẽ<br>trở nên phong phú hơn một chút，đúng không ạ?<br> ",
    "daily life enriched by assassination": "Tôi thà không có một cuộc sống thường ngày phong phú nhờ ám sát. Hơn nữa，tôi<br>cũng chẳng hề tuyển một sát thủ nào.<br> ",
    "applied as a secretary": "Cô ứng tuyển với tư cách là thư ký，nên tôi chỉ thuê cô đúng nghĩa là thư ký thôi.<br> ",
    "mean I passed": "Thuê sao...? Vậy là tôi đậu rồi ư?<br> ",
    "probation period first": "Như cô nói，trước tiên là thời gian thử việc. Để xem cô có thể làm việc như<br>một thư ký đàng hoàng không.<br> ",
    "throw someone I know is an assassin": "...Tôi cũng chẳng thể ném một kẻ mà tôi biết là sát thủ ra khỏi căn cứ được.<br> ",
    "work as hard as I can": "Cảm ơn ngài! Tôi sẽ làm việc hết sức mình!<br> ",
    "just a regular secretary": "Để tôi nhắc lại: công việc này chỉ là thư ký bình thường thôi.<br> ",
    "what would the work involve": "Thế thì，công việc cụ thể là gì ạ?<br> ",
    "cleaning the room": "Cô sẽ dọn phòng，sắp xếp giấy tờ，quản lý<br>vật tư，và làm mấy việc vặt.<br> ",
    "any confidence at all": "Ôi chao. Tôi chẳng tự tin chút nào……<br> ",
    "a few hours later": "<size=48>—Vài Giờ Sau</size>",
    "finished organizing the documents": "Chỉ Huy，tôi đã hoàn tất sắp xếp tài liệu rồi.<br> ",
    "seemed worried": "Hửm. Trông cô có vẻ lo lắng，nhưng làm cũng nhanh đấy. ...Hửm，hình như<br>chẳng có vấn đề gì.<br> ",
    "check this as well": "Và ngài cũng xem giúp cái này được không ạ?<br> ",
    "classified information mixed": "Phần lớn là những tài liệu tôi được phép xem，nhưng vì tôi thấy có vài<br>thông tin mật lẫn vào，nên tôi đã tách riêng ra.<br> ",
    "one's on me": "...Có chứa thông tin mật đấy，à. Lỗi tại tôi. Mắt nhìn tinh đấy.<br> ",
    "distinctive feel to them": "Giấy tờ quan trọng có một cảm giác đặc thù. Tôi quen với<br>việc nhận ra chúng rồi.<br> ",
    "no complaints about the": "Sao cô lại quen với chuyện đó nhỉ，tôi tự hỏi? Thôi，<br>việc sắp xếp giấy tờ thì tôi không có gì phàn nàn.<br> ",
    "previous experience is": "Tôi vinh dự được ngài khen. Tôi thấy nhẹ nhõm vì kinh nghiệm trước đây đang<br>phát huy tác dụng.<br> ",
    "won't pry": "Ah，tôi sẽ không hỏi sâu. Nhưng cô có vẻ đáng tin cậy đấy.<br> ",
    "Starting tomorrow": "Từ ngày mai，hãy phụ tá cho tôi. Nếu không có vấn đề gì，cô sẽ được chính thức nhận vào làm.<br> ",
    "Thank you very much": "Cảm ơn ngài nhiều lắm，Chỉ Huy!<br> ",
    "a few days later": "<size=48>—Vài Ngày Sau</size>",
    "clean copy of this document": "Ayame，có việc cho cô đây. Tôi cần một bản sao chép rõ của tài liệu này. Không<br>cần gấp，nhưng phải đảm bảo chính xác.<br> ",
    "Understood，Commander": "Tuân lệnh，Chỉ Huy.<br> ",
    "Yes，I'm finished": "Vâng，tôi xong rồi，Chỉ Huy.<br> ",
    "fast and beautiful handwriting": "Xong rồi sao! Thế này là...nhanh mà chữ lại đẹp nữa.<br> ",
    "forging documents was a daily": "Vâng，giả mạo giấy tờ từng là việc thường ngày，Chỉ Huy. Tôi cũng<br>từng học thư pháp nên rất tinh tường.<br> ",
    "make forgery a daily habit": "Đừng biến việc giả mạo thành thói quen hàng ngày. Dù sao，như vậy cũng giúp ích. Làm tốt lắm.<br> ",
    "Yes，thank you": "Vâng，cảm ơn ngài，Chỉ Huy.<br> ",
    "Wash my dress uniform": "Ayame，có việc đây. Đi giặt bộ lễ phục của tôi đi.<br> ",
    "Your dress uniform": "Lễ phục của ngài，đã rõ，Chỉ Huy.<br> ",
    "bigwig's coming": "Phiền phức thật，nhưng có ông lớn đến thị sát đấy. Tôi trông cậy<br>vào cô đấy.<br> ",
    "finished the laundry": "Chỉ Huy，tôi đã giặt xong rồi.<br> ",
    "No problems": "Làm tốt lắm. Không có vấn đề gì sao?<br> ",
    "shoulder measurements": "Vâng. Số đo vai hơi lệch một chút，nên tôi đã tự điều chỉnh lại.<br> ",
    "quite observant": "Tôi cũng nghĩ nó hơi rộng. Cô quan sát kỹ thật đấy，Ayame.<br> ",
    "because it is for you": "Fufu，vì là dành cho ngài mà，Chỉ Huy.<br> ",
    "you can sew too": "...Khoan đã，cô cũng biết may vá sao?<br> ",
    "adjust clothing for infiltrations": "Việc chuẩn bị và chỉnh sửa quần áo cho việc thâm nhập là chuyện thường ngày với tôi.<br> ",
    "confess to theft so casually": "Đừng tự nhiên thú tội ăn cắp một cách hờ hững vậy. Nếu sau này cô cần trang bị，<br>hãy nộp đơn xin.<br> ",
    "You will provide them": "Ngài sẽ chu cấp cho tôi sao? Thế thì giúp tôi nhiều lắm. Cảm ơn ngài.<br> ",
    "only natural as the Commander": "Đó là điều đương nhiên với tư cách Chỉ Huy. Đừng có mà mừng rỡ quá đáng vì<br>chuyện nhỏ nhặt đó.<br> ",
    "anything you command": "Còn công việc nào khác không ạ? Việc ngài sai khiến gì，tôi cũng sẽ làm hết，<br>Chỉ Huy.<br> ",
    "shoulder rub": "Hay là tôi nên nhờ cô đấm lưng giùm.<br> ",
    "Pat，pat，squeeze": "Vâng，lập tức thôi. Bụp，bụp，bóp，bóp.<br> ",
    "feels pretty good": "Hừm，cảm giác cũng khá hay đấy. Cô có kinh nghiệm với việc này sao?<br> ",
    "human body well": "Nghề nghiệp tôi nên tôi hiểu rõ cấu trúc cơ thể người.<br> ",
    "isn't that kind of profession": "Nhưng thư ký đâu phải là nghề có tính chất đó，cô biết không.<br> ",
    "haven't been a proper secretary": "...Thế mà，dù cô chưa từng làm một thư ký đúng nghĩa，<br>cô lại làm được gần như mọi thứ，Ayame.<br> ",
    "lived on my own": "Tôi đã sống một mình khá lâu，<br>nên hầu hết mọi thứ tôi đều có thể làm được.<br> ",
    "experience as an assassin": "Tôi đoán phần lớn là nhờ kinh nghiệm làm sát thủ của cô，<br>dù sao cũng……<br> ",
    "complaints about your work": "Dù sao，tôi cũng chẳng có gì phàn nàn về công việc thư ký của cô. Đã<br>tới lúc tôi chính thức nhận cô vào làm rồi.<br> ",
    "Um... is this all": "Ưm... chỉ có vậy thôi ạ? Ngài chắc chứ?<br> ",
    "handle most of the chores": "Tôi nghĩ mình đã nhờ cô làm hầu hết việc vặt，nhưng có gì<br>tôi đã bỏ sót không nhỉ?<br> ",
    "certain we do not need to kill": "Ngài có chắc là chúng ta không cần giết ai không ạ?<br> ",
    "secretary we're after": "Không cần đâu. Người thư ký chúng ta cần tìm thì chẳng giết ai cả.<br> ",
    "better to kill him": "Nhưng nếu có thể，thì giết luôn cho rồi không tốt hơn sao……<br> ",
    "kill anyone at this base": "Tại sao chúng ta lại cần giết ai ở căn cứ này chứ?<br> ",
    "what about the shop clerk": "Chẳng hạn，về tên nhân viên quầy hàng thì sao ạ? Chỉ Huy，ngài không muốn<br>giết hắn sao?<br> ",
    "kill the shop clerk": "Tại sao tôi lại phải giết tên nhân viên quầy hàng chứ?<br> ",
    "insisted it was": "Lúc trước，khi ngài ghé vào ngay trước giờ đóng cửa，hắn nhất quyết bảo là<br>đã đóng cửa rồi đuổi ngài đi mà，đúng không ạ?<br> ",
    "Now that you mention it": "...Đúng là ngài nói mới nhớ，chuyện đó có thật，nhưng sao cô lại biết<br>được chuyện đó cơ chứ，Ayame?<br> ",
    "walked around the base": "Vì tôi đã đi quanh căn cứ theo lệnh ngài，Chỉ Huy. Tôi<br>đã nghe đủ thứ chuyện.<br> ",
    "clicked his tongue": "Còn có cả người lính đã phớt lờ lời chào của ngài，và gã đàn ông ở<br>thị trấn gần đó đã thốt tiếng *tss* khi vai hắn va vào ngài.<br> ",
    "eliminate these unpleasant": "Chúng ta có thể loại bỏ những yếu tố khó chịu này，ngài biết không? Ngài có<br>thể giao phó việc này cho tôi như một nhiệm vụ không ạ?<br> ",
    "every little annoyance": "Nếu giết người chỉ vì mỗi chút bực bội，thì nơi này sẽ<br>vắng tanh bặt vậy!<br> ",
    "lighter heart": "Đừng nói thế. Hãy giết với một tâm thế nhẹ nhàng hơn，nhé?<br> ",
    "never anger you again": "Một khi chúng chết rồi，sẽ chẳng bao giờ làm ngài tức giận nữa，Chỉ Huy.<br> ",
    "see that face again": "Nếu ngài nghĩ mình sẽ không phải thấy gương mặt đó nữa，ngài có thể ngủ<br>ngon lành，đúng không，Chỉ Huy?<br> ",
    "good night's sleep": "Đừng giết người chỉ để ngủ ngon! Căn cứ này đâu có đến mức<br>đẫm máu thế đâu!<br> ",
    "okay if I do not kill": "Thế thì，tôi không giết ai cũng được sao……?<br> ",
    "look so disappointed": "Đừng có vẻ thất vọng thế. Từ nay về sau，cô chỉ cần làm việc như một<br>thư ký bình thường thôi.<br> ",
    "kill the warehouse soldier": "Nhưng... thế thì，thử giết tên lính kho này nhé?<br> ",
    "water leak in the warehouse": "Kho bị rò rỉ nước，nên họ đã chuyển vật tư<br>tới phòng tạm，đúng không ạ?<br> ",
    "embezzling them": "Lợi dụng chuyện đó，kẻ phụ trách đã nói dối là vật tư hư hỏng do rò rỉ nước，<br>và đang biển thủ chúng……đúng không ạ?<br> ",
    "dispose of": "Tôi đã hẹn gặp hắn tối nay rồi，nên có thể xử lý hắn<br>mà không ai thấy.<br> ",
    "relaxed look on his face": "Ufufu，hắn có vẻ mặt thư thái đến lạ，nên tôi chắc hắn sẽ đến<br>một mình mà chẳng nói với ai.<br> ",
    "seen firsthand": "...Ah，Ayame，tôi đã tận mắt thấy cô tài năng thế nào. Cả với tư cách<br>thư ký lẫn với tư cách sát thủ.<br> ",
    "real deal": "Được rồi，tôi giao cho cô một việc. Lần thật sự đấy.<br> ",
    "Get ready": "Chuẩn bị đi. Rõ chưa?<br> ",
    "Leave it to me": "Vâng! Cứ giao cho tôi，Chỉ Huy!<br> ",
}


def clean(s):
    return s.rstrip("\r\n")


def main():
    data = open(EN, "rb").read()
    text = data.decode("utf-8-sig")
    lines = text.splitlines(True)
    out = []
    matched = set()
    for raw in lines:
        body = clean(raw)
        ending = raw[len(body):]
        if not body.startswith(TEXT_CMDS_PREFIX):
            out.append(raw)
            continue
        if body.startswith("title,"):
            parts = body.split(",")
            en_field = parts[1]
        else:
            parts = body.split(",")
            en_field = parts[2]
        # resolve VI
        vi = None
        if en_field in EXACT:
            vi = EXACT[en_field]
            matched.add("EXACT:" + en_field)
        else:
            hits = [k for k in SEARCH if k in en_field]
            if len(hits) != 1:
                raise SystemExit(f"AMBIGUOUS/MISS ({len(hits)} hits) for field: {en_field[:50]!r}")
            vi = SEARCH[hits[0]]
            matched.add(hits[0])
        # guard: no ASCII comma inside VI text field
        assert "," not in vi, f"VI contains ASCII comma: {vi!r}"
        if body.startswith("title,"):
            parts[1] = vi
        else:
            parts[2] = vi
        out.append(",".join(parts) + ending)

    assert len(out) == len(lines), f"LINE COUNT {len(lines)}->{len(out)}"
    # ensure all SEARCH keys were used (no dead entries) and all text lines covered
    used_search = {k for k in matched if not k.startswith("EXACT:")}
    unused = set(SEARCH) - used_search
    assert not unused, f"UNUSED SEARCH keys: {unused}"
    joined = "".join(out)
    open(VI, "wb").write(b"\xef\xbb\xbf" + joined.encode("utf-8"))

    n_text = sum(1 for ln in out if clean(ln).startswith(TEXT_CMDS_PREFIX))
    en_clean = [clean(l) for l in lines]
    vi_clean = [clean(l) for l in out]
    changed = sum(1 for ec, vc in zip(en_clean, vi_clean) if ec.startswith(TEXT_CMDS_PREFIX) and ec != vc)
    print(f"WROTE {VI}")
    print(f"lines={len(out)} text_records={n_text} changed_text_lines={changed} search_keys={len(SEARCH)} exact={len(EXACT)}")


if __name__ == "__main__":
    main()
