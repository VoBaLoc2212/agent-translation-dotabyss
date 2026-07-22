# -*- coding: utf-8 -*-
"""Deterministic VI generator for hmn_10190100002.
Source EN asset actually carries JP text; en.json is blank, so we translate from JP.
Speaker labels (field 1) are kept as-is. Only the translatable text field is replaced.
VI prose uses U+201A (‚) instead of ASCII comma. BOM + CRLF preserved.
"""
import io, sys

SRC = r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10190100002.txt"
OUT = r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10190100002.txt"

raw = open(SRC, "rb").read()
assert raw[:3] == b"\xef\xbb\xbf", "source must be utf-8-sig"
lines = raw.decode("utf-8-sig").split("\r\n")

# Ordered VI text fields, aligned to candidate record order in the file:
# title (1) + messages (63) + messageTextCenter (2) = 66
vi = [
    # --- title ---
    "Đối Thủ Tuyệt Đối Không Thể Thua",
    # --- messages (file order) ---
    "Mọi người ơi! Lần này là một công việc lớn đấy!<br>Bọn tôi sẽ cho lũ ở vương quốc thấy sức mạnh thật của mình!",
    "Rõ!!",
    "Sao ấy nhỉ‚ thưa thủ lĩnh? Từ khi trở về từ Căn Cứ Tiền Tuyến‚ dạo này ngài vui hẳn ra.<br>Có chuyện vui gì à?",
    "Biết sao đây. Nhưng vì thủ lĩnh đang hăng hái thế này‚<br>bọn tôi cũng phải dốc sức thôi!",
    "Lương thực thì cứ lấy ở chỗ kia‚ còn vật tư thì tính sao đây?<br>Chỉ mấy tay thầu cũ quen biết thì e không đủ số lượng đâu…… ừm~.",
    "Ôi trời‚ Lucita.<br>Đang lầm bầm cái gì thế?",
    "Ui‚ Aura……!",
    "Bà đến làm gì vậy? Tôi đang bận.<br>Nếu định làm phiền thì đi chỗ khác đi!",
    "Chào hỏi đấy. Thế mà tôi còn ghé thăm xem tình hình cho.<br>……Ủa? Cái gì thế này? ……Phiếu đặt hàng à?",
    "Này‚ đừng có tự tiện xem chứ!<br>Đó là việc Chỉ Huy giao cho tôi đấy!",
    "Lucita cơ à?<br>Hừm…… Hóa ra là một đơn đặt hàng khá bự đấy nhỉ.",
    "Được thôi. Tôi sẽ chuẩn bị cho món hàng tuyệt nhất.",
    "Hả!? Sao lại thành ra thế chứ!<br>Tôi đã nói rồi‚ đây là việc tôi được giao mà!!",
    "Không liên quan gì tới Aura đâu! Đi chỗ khác đi!",
    "Chị hiểu lầm rồi nhé.<br>Chuyện không liên quan gì thì không có đâu.",
    "Đơn hàng lớn thế này mà nếu bà làm qua loa‚<br>thì uy tín của Eldorana cũng bị vướng vào đấy.",
    "Vậy nên‚ chỗ này để tôi lo món hàng tuyệt nhất cho.",
    "Nói gì bà cũng cãi lại……!",
    "Nhưng mà‚ công việc bà nhận cũng là thật.<br>Thế thì‚ chỗ này——.",
    "Đấu tay đôi đi!",
    "Đấu tay đôi ư?<br>Ý bà là sao?",
    "Tôi và Lucita‚ mỗi người sẽ chuẩn bị món hàng được đặt.<br>Khách hàng sẽ quyết định mua của ai trong hai chúng tôi.",
    "Quy tắc thế này có được không nhỉ?<br>Kinh doanh mà‚ xưa nay vốn là như vậy chứ?",
    "Hay là…… bà sợ thua nên mới thế?",
    "Cái gì cơ!?<br>Ai lại thua nổi Aura chứ!",
    "Thế mà trông bà chẳng có vẻ gì muốn lùi bước nhỉ?",
    "……!<br>Từ xưa tới giờ bà cứ thế mà coi thường tôi……!",
    "Được rồi! Trận đấu này tôi nhận!<br>Bà sủa om sòm rồi đấy!!",
    "Lời đó tôi xin hoàn trả nguyên vẹn cho bà.<br>Cứ cố gắng hết sức nhé!",
    # --- messageTextCenter #1 ---
    "<size=48>――Vài Ngày Sau</size>",
    # --- messages continue ---
    "Vụ lương thực thì ổn rồi. Còn vụ vật tư thì phải sang nhờ chỗ thầu đó<br>xem họ có chịu nới lỏng hơn chút không.",
    "Thưa thủ lĩnh. Về thiết bị được đặt hàng‚<br>địa chỉ đặt mua theo danh sách này được không ạ?",
    "Ồ‚ đưa tôi xem nào.",
    "……Ừm‚ không tệ‚ nhưng mà xài lâu dài thì lại khác.<br>Chỗ này lại là Căn Cứ Tiền Tuyến nữa…….",
    "Cũng phải tính cả độ bền và dễ sửa chữa nữa‚ nên đi qua xưởng bên này hỏi thử xem.",
    "Rõ ạ!",
    "Cố gắng hết mình thế nhỉ.",
    "Gì thế‚ Aura. Bà nhàn nhã nhỉ.<br>Việc thu mua ổn chưa?",
    "Đổ mồ hôi ngoài hiện trường không phải sở thích của tôi. Chẳng cần làm thế‚<br>cứ dùng quyền lực và mối quan hệ của tôi là tập hợp được món hàng tuyệt nhất.",
    "……Không phải đó gọi là lạm dụng chức quyền sao?<br>Thật sự‚ bà làm quá trớn thật đấy…….",
    "Đó cũng là một phần sức mạnh của tôi.<br>Tất nhiên là dùng hết mọi thứ có thể dùng chứ.",
    "……Đúng là‚ cách đó có lẽ hiệu quả hơn.<br>Nhưng tôi có cách làm và suy nghĩ của riêng tôi.",
    "Tôi…… muốn đáp lại người đã đặt kỳ vọng vào tôi.",
    "……Cố gắng kỳ lạ thật nhỉ. Có chuyện gì à?",
    "Tôi không thèm kể cho bà đâu.<br>Hơn nữa‚ nếu định làm phiền thì đi ra ngay đi. Tôi đang bận.",
    "Rồi rồi‚ tôi hiểu mà.",
    "……Chán thật nhỉ.<br>Này Lucita‚ người ta chẳng thèm ngoái lại nhìn tôi lấy một cái.",
    # --- messageTextCenter #2 ---
    "<size=48>――Rồi Lại Thêm Vài Ngày Nữa</size>",
    # --- messages continue ---
    "……Tốt! Thế là đủ hết mọi món có trong phiếu đặt hàng rồi!",
    "Thủ lĩnh‚ ngài đã nỗ lực lắm rồi ạ!",
    "Ồ! Thế này thì kịp đúng hạn giao hàng!<br>Nhờ mọi người cả đấy! Các cậu làm tốt lắm!",
    "Vì thủ lĩnh mà‚ chút này có là gì đâu ạ!",
    "Hê hê‚ lũ đệ tử đáng tin cậy ghê! Tình bằng hữu này‚<br>chắc chắn chẳng thua kém tổ tiên Vua Hải Tặc đâu ♪",
    "T‚ thủ lĩnh ạ! Có chuyện chẳng lành!",
    "Sao thế‚ sao thế? Dù sao thì bình tĩnh đã. Có chuyện gì xảy ra?",
    "C‚ chuyện là……!<br>Thương hội của Aura đã giao hàng vật tư cho Căn Cứ Tiền Tuyến rồi!",
    "Ê……!?",
    "C‚ sao lại thế!? Nhanh thế này cơ á……!?",
    "(Chết tiệt‚ bị gài rồi……!<br>　Mình cứ bám lấy chỗ đặt hàng‚ mất quá nhiều thời gian rồi……!)",
    "Thế thì‚ đống vật tư bọn này gom được sẽ thành công cốc sao……?",
    "……Không! Trận đấu do Aura khởi xướng‚<br>đâu có nghĩa là ai nhanh hơn người đó thắng!",
    "Chuẩn bị khởi hành ngay!<br>Tôi sẽ trực tiếp nói chuyện với Chỉ Huy và Aura!",
    "Đây là việc tôi nhận!<br>Đã vậy thì phải dốc hết sức tới cùng! Sai à!?",
    "Đúng quá ạ!!!",
    "Quan trọng hơn…… công sức của mọi người‚<br>tôi sẽ không để nó uổng phí đâu――!",
]

# sanity: no ASCII comma inside any VI field
for i, s in enumerate(vi):
    assert "," not in s, "ASCII comma in vi[%d]: %r" % (i, s)

out_lines = []
idx = 0
candidate_types = {"title", "message", "messageTextUnder", "messageTextCenter"}
for ln in lines:
    if ln == "":
        out_lines.append("")
        continue
    parts = ln.split(",")
    rtype = parts[0]
    if rtype in candidate_types:
        if rtype == "title":
            tindex = 1
        else:
            tindex = 2
        assert idx < len(vi), "ran out of VI entries at line: %s" % ln
        newtext = vi[idx]
        # preserve <br>/tag counts implicitly since we authored them to match
        parts[tindex] = newtext
        out_lines.append(",".join(parts))
        idx += 1
    else:
        out_lines.append(ln)

assert idx == len(vi), "VI count %d != applied %d" % (len(vi), idx)

data = "\r\n".join(out_lines).encode("utf-8")
open(OUT, "wb").write(b"\xef\xbb\xbf" + data)
print("WROTE", OUT)
print("candidates applied:", idx)
print("output lines:", len(out_lines))
