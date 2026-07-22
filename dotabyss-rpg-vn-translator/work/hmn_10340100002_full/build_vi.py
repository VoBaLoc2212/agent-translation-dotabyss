#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Field-index VI builder for hmn_10340100002 (EN-asset-is-English + title-still-JP).

Title is JP -> translate JP->VI Title Case.
All message fields are English (fullwidth ，commas) -> translate EN->VI.
Keep BOM/CRLF/structure exactly. Trailing "<br> " suffix mirrored automatically.
Convert fullwidth ， -> U+201A '‚'. Commander -> Chỉ Huy.
Carla (カーラ) = em; Commander (<user>) = anh.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10340100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# Ordered VI text fields, 1:1 with source text records in file order.
# INTERNAL <br> tags placed where source had them. Do NOT end with <br>.
TRANSLATIONS = [
    # --- title (JP -> VI Title Case) ---
    "Huấn Luyện Khắc Nghiệt Cận Kề Cái Chết",
    # --- messages (EN -> VI), in file order ---
    "Thế thì... cạn ly!",  # L36
    "Vâng‚ Chỉ Huy.<br>...cạn ly!",  # L45
    "Xin lỗi‚ chào mừng chỉ có hai chúng ta trong buổi tiệc này thôi.",  # L58
    "Không có gì đâu. Em thực sự rất vui vì được Chỉ Huy đón tiếp như thế này‚<br>Chỉ Huy ơi!",  # L69
    "Lúc em được phân công về Đội Cảnh Vệ‚ họ cũng đã bày một bữa nhậu<br>như thế này cho em.",  # L80
    "Hóa ra đó thật sự là một truyền thống.",  # L82
    "Vâng. Sau khi vượt qua khóa huấn luyện khắc nghiệt‚ đó là khoảnh khắc em<br>cuối cùng được công nhận là một người lính...",  # L93
    "Huấn luyện của Eldorana khắc nghiệt đến thế sao?",  # L95
    "Không hẳn là Eldorana‚ mà có lẽ Đội Cảnh Vệ Cộng Hòa mới là nơi<br>khắc nghiệt đặc biệt.",  # L106
    "Eldorana là một quốc gia của những người đi biển‚ và hầu hết biên giới của họ là biển. Và<br>nhiệm vụ của Đội Cảnh Vệ là bảo vệ biển và bờ biển.",  # L118
    "Tân binh phải chịu đựng huấn luyện khắc nghiệt để sinh tồn qua hải chiến‚ nơi cái chết<br>luôn cận kề‚ trước khi được phép nhập ngũ.",  # L127
    "Hừm‚ nhưng em đã trải qua kiểu huấn luyện cụ thể nào?",  # L129
    "...họ ép cậu vượt qua giới hạn tâm trí‚ và cảm giác như cả nhân cách của cậu<br>được tái tạo thành một người lính.",  # L140
    "Chỉ nghe thôi cũng thấy sợ. Anh chắc chắn không thể chịu nổi như thế.",  # L142
    "Nhưng Chỉ Huy ơi‚ sau huấn luyện kiểu Đội Cảnh Vệ‚ em nghĩ anh sẽ chẳng bao giờ<br>quấy rối tình dục ai nữa đâu.",  # L154
    "Đừng có tái tạo nhân cách của anh chỉ để ngăn quấy rối!",  # L156
    "Fufu‚ xin lỗi. Em chỉ muốn trả đũa anh một chút nãy giờ thôi.",  # L167
    "Thật tình... Nhưng Carla‚ em có vẻ đã bớt căng thẳng hơn chút đỉnh.",  # L169
    "Á... em xin lỗi nhiều! Tại Chỉ Huy rất dễ nói chuyện‚<br>nên em mới thế‚ Chỉ Huy ơi...",  # L181
    "Thế cũng tốt mà‚ phải không? Đấy là mục đích của một buổi tiệc chào đón<br>kiểu Eldorana‚ đúng không?",  # L183
    "...Vâng. Chúng em uống như thế này để thân thiết với đồng đội mới.",  # L194
    "Vậy là việc bày ra buổi này cũng có ý nghĩa. Từ nay về sau‚ cứ thoải mái<br>nói chuyện suồng sã như thế nhé.",  # L196
    "Chỉ Huy... em cảm ơn anh rất nhiều!",  # L208
    "...em không bao giờ tưởng tượng lúc mới đến rằng em có thể nói chuyện với<br>Chỉ Huy như thế này.",  # L215
    "Em có nghĩ anh chỉ là một Chỉ Huy hay quấy rối tình dục không?",  # L217
    "K-không‚ à‚ k-không có chuyện đó đâu! Em-em nghĩ anh là một<br>Chỉ Huy tuyệt vời.",  # L229
    "Này‚ chối gay gắt thế khiến trông như em đang nói dối đấy.",  # L231
    "Đây là bữa nhậu. Đừng bận tâm đến lễ nghi. Nào‚ hãy nói ra<br>suy nghĩ thật của em đi.",  # L233
    "...À‚ thành thật mà nói‚ em có hơi bất ngờ.",  # L245
    "Anh cũng nghĩ vậy. À‚ thế cũng tự nhiên thôi. Nói gì thì nói‚ em cũng đã chịu đựng khá tốt.",  # L247
    "Nếu em là một người lính nghiêm túc‚ anh nghĩ có khi nắm đấm đã bay vào mặt anh rồi.",  # L249
    "Không! Em sẽ không bao giờ đánh Chỉ Huy.",  # L261
    "Không tưởng tượng nổi‚ hử? Carla‚ em đúng là hình mẫu của đức hạnh. Thật sự là một người lính<br>chính trực.",  # L263
    "Là vậy sao...?",  # L275
    "Thế thì tại sao em lại bị điều đến Căn Cứ Tiền Tuyến này? Em có gặp<br>rắc rối ở Eldorana không?",  # L277
    "Em-em không có nghịch ngợm đâu!",  # L287
    "Đừng giấu nữa‚ đừng giấu nữa. Em có đấm một cấp trên hay quấy rối không? Hay là<br>đá vào hạ bộ một đồng nghiệp đang tán tỉnh em?",  # L289
    "Em xin nhắc lại: tấn công cấp trên hay đồng nghiệp là chuyện hoàn toàn không thể tưởng tượng nổi!",  # L301
    "...Thế thì tại sao em lại ở căn cứ này? Chắc phải có lý do nào đó‚ đúng không?",  # L305
    "Thực ra... à...",  # L319
    "Em đang làm nhiệm vụ cảnh vệ và đã đưa một công dân say rượu vào tạm giữ bảo hộ.<br>Em định đưa anh ta về nhà‚ nhưng...",  # L330
    "Công dân say rượu đó‚ với những lời dâm dục‚ đã đặt tay lên... lên<br>ngực em...",  # L341
    "Anh ta đã sờ mó em?",  # L343
    "S-sờ mó!",  # L354
    "...Vâng‚ đúng vậy.",  # L365
    "Nghe hơi kỳ đến từ anh‚ nhưng đó là quấy rối tình dục kinh khủng. Em có bắt được<br>hắn tại trận không?",  # L367
    "À‚ em bị bất ngờ vì sự việc quá đột ngột‚ và với tư cách người lính thì việc đó<br>không thể tha thứ được‚ nhưng...",  # L378
    "Em đã đấm anh ta hết sức lực.",  # L389
    "Ồ... nghe có vẻ em đã thực sự cho anh ta một trận.",  # L391
    "Người lính tấn công thường dân là hoàn toàn không thể tha thứ. Đó là hành vi<br>có thể dễ dàng khiến em bị giải ngũ...",  # L400
    "Em nói gì thế? Carla‚ em hoàn toàn không sai!",  # L402
    "Hả...?",  # L414
    "Anh ta sờ mó ngực em‚ mà em chỉ đấm một phát thôi‚ đúng không?",  # L416
    "Thế là quá nhẹ. Đáng lẽ em nên đánh anh ta nửa sống nửa chết.",  # L418
    "Chỉ Huy... em cảm ơn anh.",  # L430
    "Anh không tha thứ cho kẻ quấy rối tình dục. Người duy nhất được phép<br>quấy rối tình dục ở căn cứ này là anh.",  # L432
    "Ngay cả anh cũng không được‚ Chỉ Huy!",  # L443
    "Thật đáng tiếc.",  # L445
    "Anh hiểu rồi. Vậy là em bị điều đến Căn Cứ Tiền Tuyến vì họ đã<br>làm lớn chuyện việc em đánh một thường dân.",  # L450
    "Vâng... Đây là tiền tuyến bảo vệ mọi người.",  # L459
    "Em muốn chiến đấu ở đây‚ liều mạng sống của mình‚ và thực sự nhìn lại bản thân.",  # L468
    "Em đúng là một người rất nghiêm túc. À‚ đó là điều anh thích ở<br>em‚ Carla.",  # L470
    "Anh muốn giao cho em một nhiệm vụ tận dụng phẩm chất đó của em‚<br>nhưng...",  # L472
    "Phải. Anh có một đề xuất.",  # L489
    "Một nhiệm vụ tận dụng phẩm chất của em... ý anh là sao?",  # L500
    "Em có thể sẽ bất ngờ về chi tiết. Thế nào‚ nếu em tin<br>anh‚ có muốn thử không?",  # L502
    "...Vâng‚ em tin anh‚ Chỉ Huy! Làm ơn‚ hãy để em làm!",  # L536
]


def main() -> None:
    data = EN.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    # ---- structural <br> self-check (batch, all mismatches at once) ----
    idx = 0
    bad = 0
    for li, ln in enumerate(lines, start=1):
        if not ln.startswith(TEXT_CMDS):
            continue
        idx += 1
        assert idx <= len(TRANSLATIONS), f"Ran out of translations at record {idx} (line {li})"
        vi_text = TRANSLATIONS[idx - 1]
        if ln.startswith("title,"):
            src_field = ln[len("title,"):]
            src_internal = src_field.count("<br>")
        else:
            parts = ln.split(",", 5)
            src_field = parts[2]
            src_internal = src_field.count("<br>") - 1  # trailing <br>  suffix
        vi_internal = vi_text.count("<br>")
        if src_internal != vi_internal:
            bad += 1
            print(f"BR_MISMATCH record {idx} (line {li}): EN_internal={src_internal} VI_internal={vi_internal}")
            print("  EN:", repr(src_field[:160]))
            print("  VI:", repr(vi_text[:160]))
    assert idx == len(TRANSLATIONS), f"used {idx} but have {len(TRANSLATIONS)} translations"
    assert bad == 0, f"{bad} <br> mismatches — fix before writing"
    print("BR self-check OK: all internal <br> counts match.")

    # ---- build output ----
    vi_lines: list[str] = []
    idx = 0
    record_count = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            record_count += 1
            vi_text = TRANSLATIONS[idx]
            idx += 1
            assert "," not in vi_text, f"ASCII comma in VI text (record {record_count}); use U+201A '‚'"
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text
            else:
                parts = ln.split(",", 5)
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                parts[2] = vi_text + suffix
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()
