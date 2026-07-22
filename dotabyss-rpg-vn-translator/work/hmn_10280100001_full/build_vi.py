#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic VI builder for hmn_10280100001 (EN-asset-is-English case).

Each EN text field already holds faithful English (en.json non-empty English).
We translate EN -> VI, using ja.json/en.json for meaning, treating the EN asset
as structural authority: exact <br> counts, BOM, CRLF, fullwidth ， preserved
where present, and intra-text commas use U+201A '‚'.

Only lines present in TRANSLATIONS are rewritten; every other line (including the
charaload/charamove/command lines containing JP character names) is copied verbatim.
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10280100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# line_no -> VI text field (EXACTLY the part after title, or after the 2nd comma of
# message/messageTextUnder/messageTextCenter). Trailing "<br> " suffix is included.
TRANSLATIONS = {
    37: "Kỷ Niệm Sóng Biển",
    73: "Này Emily! Cho tôi một phần đồ nhắm nhé!<br> ",
    129: "Dạ dạ! Em lo ngay đây!♪<br> ",
    173: "Emily! Mang món này và món này ra bàn 5‚ và món này ra bàn 3!<br> ",
    204: "Rõ! Làm thôi!<br> ",
    272: "Ồ‚ tuyệt vời! Cô ấy đang bê bốn đĩa một lúc bằng cả<br>cẳng tay!<br> ",
    316: "Ehehehe! Dễ ợt!♪<br> ",
    362: "Emily‚ hôm nay em vẫn đáng yêu như mọi khi. Thế nào‚ cái mông của<br>em hôm nay ra sao rồi... ối.<br> ",
    433: "Này nào. Cấm quấy rối nhân viên đấy‚ rõ chưa?<br> ",
    479: "Emily‚ ca của em tan lúc mấy giờ? Xong rồi đi uống gì đó không?<br> ",
    490: "Không đời nào! Muốn uống thì uống tại đây đi!<br> ",
    501: "Chà‚ em chăm chỉ thật đấy.<br> ",
    552: "Emily‚ em lúc nào cũng làm việc chăm chỉ nhỉ.<br> ",
    563: "Fufu‚ đúng rồi. Dù bận đến mấy‚ cô ấy vẫn cứ cười tươi và làm việc<br>nhanh nhẹn đến thế... Đúng là một cô bé tuyệt vời!♪<br> ",
    565: "Emily đúng là gương mặt đại diện của quán—dường như nhiều khách<br>đến chỉ để được an lòng khi có em hiện diện.<br> ",
    590: "<size=48>Vài Ngày Sau.</size>",
    628: "Ư... Cửa hàng vắng khách quá...<br> ",
    630: "Hóa ra cũng có những ngày như thế này nhỉ.<br> ",
    647: "Chỉ thỉnh thoảng thôi‚ nhưng vẫn thế. Ư... em muốn làm việc nhiều hơn...<br> ",
    649: "Có thời gian rảnh cũng tốt mà? Lớn lên rồi em sẽ có<br>công việc ngập đầu đến mức không biết xoay sở sao‚ nên hãy tận hưởng tự do lúc còn có thể.<br> ",
    668: "Trời ơi! Chỉ Huy‚ ngài nói cái gì thế! Em đã là người lớn<br>chính hiệu rồi!<br> ",
    670: "Xin lỗi‚ xin lỗi. Em nói đúng mà.<br> ",
    727: "Ồ‚ hình như hôm nay quán vắng khách quá.<br> ",
    736: "Ừ‚ đúng rồi. Em biết những hôm ế là chuyện không tránh khỏi‚<br>nhưng... Ừm...<br> ",
    738: "Biểu cảm của em xụi lơ hẳn so với lúc quán đông khách.<br>Dường như tình cảnh hiện tại chẳng hợp với em chút nào.<br> ",
    750: "Nghĩ mới nhớ‚ bình thường tầm này em ăn cơm nhân viên rồi‚ phải<br>không? Hôm nay em chưa ăn à?<br> ",
    761: "Ừ... em ít hoạt động nên vẫn chưa đói lắm. Em cảm thấy ăn<br>bây giờ thì hơi phí...<br> ",
    763: "Ra thế. Vậy là em muốn ăn lúc bản thân ở trạng thái tốt nhất để<br>thưởng thức trọn vẹn... Cũng phải.<br> ",
    809: "Đúng thế!<br> ",
    820: "Được ăn cơm nhân viên sau khi làm việc vất vả và đói<br>meo đến cùng cực...<br> ",
    831: "Bữa đó ngon nhất quả đất... Nó làm em thấy mình hôm nay đã<br>thực sự làm việc thật chăm chỉ!♪<br> ",
    833: "Anh luôn hình dung em thưởng thức bữa ăn một cách ngon lành‚ Emily.<br> ",
    845: "Đúng rồi‚ em thích ăn lắm!♪<br> ",
    856: "Nhưng ăn bao nhiêu em cũng chẳng cao thêm tí nào... Thế<br>chất dinh dưỡng đó đi đâu hết rồi nhỉ? Hmm...<br> ",
    911: "Emily bé‚ lúc bận em bê bốn đĩa một lúc‚ phải<br>không?<br> ",
    913: "Sức mạnh của em đáng nể‚ nhưng khả năng giữ thăng bằng mới kinh khủng.<br> ",
    924: "Em muốn khách ăn lúc còn nóng nhất có thể nên mấy chuyện<br>như thế này chẳng là gì!♪<br> ",
    926: "Tự hào về công việc đến thế... Này‚ Emily‚ em thích điều gì ở<br>công việc này?<br> ",
    972: "Điều em thích ở công việc này là...?<br> ",
    983: "À‚ là được nhìn thấy thật nhiều gương mặt hạnh phúc‚ em nghĩ vậy!<br> ",
    994: "Được thấy mọi người thưởng thức đồ uống và món ngon‚ trò chuyện vui vẻ... em<br>thực sự hạnh phúc vì có thể mang đến không gian chữa lành ấy.<br> ",
    1005: "Và không chỉ thế... sau khi làm việc vất vả‚ chúng ta còn được ăn<br>cơm nhân viên ngon tuyệt!♪<br> ",
    1016: "Với em‚ công việc này... chính là thiên chức của em!<br> ",
    1018: "Nghĩ mới nhớ‚ Emily‚ sao em lại đến Tiền Tuyến Căn Cứ?<br> ",
    1030: "Ừm‚ trước khi đến đây em từng làm ở một nhà hàng tại Eldorana.<br> ",
    1041: "Đó là một nhà hàng sang trọng‚ nơi rất đông khách. Em cũng thích<br>làm việc ở đó‚ nhưng...<br> ",
    1051: "Ông chủ chỗ đó‚ này nhé... ông ấy cực kỳ‚ cực kỳ thích<br>đánh bạc...<br> ",
    1053: "Nghe có vẻ chẳng lành...<br> ",
    1062: "Ông ấy bảo 'Đại Huyệt! Ta ngửi thấy mùi kho báu!' rồi một ngày ông<br>ấy bỗng dưng bỏ đi...<br> ",
    1071: "Từ đó ông ấy chẳng trở về. *sigh*...<br> ",
    1073: "À‚ ra là thế... vậy ra là kiểu đó.<br> ",
    1075: "Khi Đại Huyệt xuất hiện‚ vô số người đã hấp tấp xông ra thám hiểm‚<br>nhắm tới một mẻ giàu to y như vậy.<br> ",
    1084: "Ư... Ông chủ... ông ấy ở đâu rồi...<br> ",
    1093: "Em đã tìm nhiều lần từ khi đến đây‚ nhưng... nơi này bao la quá‚ em<br>chẳng tìm thấy manh mối nào.<br> ",
    1095: "Tiền Tuyến Căn Cứ cũng rộng lớn phết... Tiện thể‚ chỗ đó tên là<br>gì nhỉ?<br> ",
    1107: "Tên là 'Hãy Lắng Nghe Tiếng Sóng'.<br> ",
    1118: "Đó là nhà hàng ngay bên biển‚ hải sản thì tuyệt cú mèo.<br>*sigh* Em bắt đầu nhớ món đó rồi.♪<br> ",
    1171: "'Hãy Lắng Nghe Tiếng Sóng'...?<br> ",
    1182: "Ludia cô? Có chuyện gì vậy?<br> ",
    1194: "Một nhà hàng cùng tên... hình như em từng thấy quanh<br>Tiền Tuyến Căn Cứ vài hôm trước...<br> ",
    1242: "Cái... Cái gì!<br> ",
}


def main():
    assert TRANSLATIONS, "fill TRANSLATIONS"
    for ln, vi in TRANSLATIONS.items():
        assert "," not in vi, f"ASCII comma in VI L{ln}: use U+201A ,"

    raw = EN.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf", "EN source must have BOM"
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(True)

    # ---- preflight: compare <br> counts EN vs VI for each translated line ----
    mismatches = []
    for ln, vi in TRANSLATIONS.items():
        en_line = lines[ln - 1].rstrip("\r\n")
        if en_line.startswith("title,"):
            en_field = en_line.split(",", 1)[1]
        else:
            en_field = en_line.split(",", 5)[2]
        en_br = en_field.count("<br>")
        vi_br = vi.count("<br>")
        if en_br != vi_br:
            mismatches.append((ln, en_br, vi_br, en_field, vi))
    if mismatches:
        print("PREFLIGHT <br> MISMATCHES:")
        for ln, eb, vb, ef, vf in mismatches:
            print(f"  L{ln}: EN={eb} VI={vb}")
            print(f"     EN field: {ef!r}")
            print(f"     VI field: {vf!r}")
        raise SystemExit(1)

    out = []
    translated = 0
    for idx, line in enumerate(lines, 1):
        if idx in TRANSLATIONS:
            vi = TRANSLATIONS[idx]
            cleaned = line.rstrip("\r\n")
            if cleaned.startswith("title,"):
                new = "title," + vi
            elif cleaned.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
                parts = cleaned.split(",", 5)
                parts[2] = vi
                new = ",".join(parts)
            else:
                raise AssertionError(f"unexpected text cmd L{idx}: {line!r}")
            trailer = line[len(line.rstrip("\r\n")):]
            assert trailer in ("\r\n", "\n", ""), f"bad trailer L{idx}: {trailer!r}"
            out.append(new + trailer)
            translated += 1
        else:
            out.append(line)
    out_bytes = b"\xef\xbb\xbf" + "".join(out).encode("utf-8")
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out_bytes)
    print(f"translated {translated}/{len(lines)} lines -> {VI}")


if __name__ == "__main__":
    main()
