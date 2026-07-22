#!/usr/bin/env python3
# Build VI output for hmn_10320100002 from EN asset (EN-asset-is-English mode,
# title field still JP). Per-field detection: messages translated JP->VI via
# ja.json/EN meaning; title translated from JP. Preserves BOM/CRLF/delimiters/
# tags/<br> counts/speaker+ID+voice fields byte-identical.
import io
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10320100002.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10320100002.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10320100002_full"

TITLE_VI = "Những Tin Đồn Xung Quanh Dahlia"

# line_no -> VI text field (includes trailing "<br> " suffix where the EN field has it)
MESSAGE_VI = {
    46: "Ồ‚ Chỉ Huy. Sao anh lại ở trong phòng em...?<br> ",
    48: "Anh tới đây có việc‚ nhưng giờ không phải lúc nói chuyện đó.<br> ",
    50: "Này‚ Dahlia. Rốt cuộc đống quặng khổng lồ này là sao thế?<br> ",
    61: "Á‚ ư‚ ừm...<br> ",
    90: "Khừ...<br> ",
    92: "Này nào‚ em thật sự không thể giả vờ ngủ lúc này được...<br> ",
    120: "D-dạ. Em xin lỗi...<br> ",
    122: "Để anh nghe em giải thích kỹ hơn nào. Rốt cuộc đống quặng nhiều thế này<br>em đào đâu ra?<br> ",
    133: "Giải thích... à? Ư‚ em nên nói sao đây...<br> ",
    144: "Ưm...<br> ",
    146: "Đừng có cứng đờ thế. Anh sẽ không tha cho em cho tới khi em giải thích rõ ràng.<br> ",
    148: "Nhìn kỹ hơn thì không chỉ có quặng đâu—có cả ma thạch và đá quý<br>lẫn vào nữa kìa.<br> ",
    150: "Em gom hết đống này từ đâu? Nói thật cho anh.<br> ",
    161: "Ư‚ ừm‚ là...<br> ",
    170: "Em... em thích đá quý.<br> ",
    172: "Chuyện đó anh nghe rồi. Rồi sao?<br> ",
    179: "Thế nên... sở thích của em là đi tìm đá quý. Khi tìm được viên to và đẹp‚ em<br>vui lắm.<br> ",
    181: "Có vẻ thế thật. Rồi sao?<br> ",
    192: "Thế nên... em cứ say mê đi tìm đá quý mất rồi. Lúc em nhận ra thì đã đào<br>lên một đống.<br> ",
    194: "Ừm...<br> ",
    205: "Lần thám hiểm trước em cũng... cuối cùng em nhét đầy vào túi áo khoác‚ thậm chí cả<br>vào trong quần lót nữa—<br> ",
    207: "Khoan đã! Dừng lại một chút. Em càng nói càng lạc đề rồi.<br> ",
    218: "Á... th-thật sao? Em xin lỗi...<br> ",
    220: "Để anh hỏi lại. Sao em có nhiều quặng thế?<br> ",
    231: "Ừm... Nhiều một chút thì không tốt sao...?<br> ",
    233: "Đó đâu tính là giải thích. Hãy nói cho anh em đã gom hết đống này bằng cách nào.<br> ",
    245: "Chuyện đó... em đã rất nỗ lực... vâng.<br> ",
    247: "Đó là điều anh đang hỏi mà! Ở đâu‚ bằng cách nào‚ tại sao? Anh cần biết em đã<br>gom chúng bằng cách nào.<br> ",
    266: "... *rên rỉ* ...<br> ",
    268: "...Á... xin lỗi. Anh hơi bốc đồng quá.<br> ",
    279: "Không... em mới là người phải xin lỗi. Em không trả lời được tử tế...<br> ",
    281: "*thở dài*... Nghe này‚ Dahlia.<br> ",
    283: "Anh tới đây là để xác minh xem những lời đồn về em là thật hay giả.<br> ",
    295: "Lời đồn... ư?<br> ",
    297: "Ừ. Có tin đồn rằng em vốn là một thành viên trong băng trộm.<br> ",
    308: "Hả!<br> ",
    310: "Các binh lính dường như sợ em. Tại vì lời đồn‚ ngay cả hành động<br>bình thường của em cũng trông đầy mờ ám.<br> ",
    321: "Ra là vậy... Thế sao...<br> ",
    323: "Lúc này nó chỉ là lời đồn thôi. Chính vì thế anh muốn xác minh. Thế nào?<br>Sự thật là gì?<br> ",
    334: "... *rên rỉ* ...<br> ",
    365: "Chỉ Huy... Thật đấy... Chuyện đó...<br> ",
    367: "Là gì thế?<br> ",
    376: "Chỉ Huy... em... em từng là kẻ trộm. Lời đồn đó cũng là sự thật... Xin lỗi vì đã giấu anh.<br> ",
    387: "Nhưng Chỉ Huy‚ giờ đã khác rồi. Em đã từ bỏ nghề trộm. Giờ em chỉ là một thợ mỏ.<br> ",
    398: "Chỉ Huy‚ tất cả những thứ này... không phải đồ ăn trộm. Sự thật là thế...<br> ",
    400: "Ừm... Ra là vậy.<br> ",
    402: "Dahlia‚ nếu lời đồn là thật... anh không thể cứ thế mà tin em được.<br> ",
    413: "...Em nghĩ anh nói đúng đấy‚ Chỉ Huy.<br> ",
    415: "Xin lỗi‚ Dahlia‚ nhưng anh cần nghe toàn bộ câu chuyện. Về núi quặng này‚ từ<br>đầu đến cuối—<br> ",
    419: "Rắc.<br> ",
    470: "Chị lớn ơi! Em tới chơi nè!<br> ",
    472: "Cái gì?!<br> ",
    483: "*thở hắt!*<br> ",
    494: "Hả? Ông già là ai thế?<br> ",
    496: "Ô-ông già? Này‚ em gọi ai thế—<br> ",
    543: "Đừng có vào!<br> ",
    545: "Hả!<br> ",
    556: "Nhanh lên‚ ra ngoài đi! Làm ơn...!<br> ",
    608: "Chị lớn...?<br> ",
    610: "Hừm. Xin lỗi‚ nhưng...<br> ",
    657: "Á!<br> ",
    659: "Anh không thể để em đi mà chưa nghe gì cả.<br> ",
    699: "……!<br> ",
}

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def replace_text_field(line: str, vi_text: str) -> str:
    if line.startswith("title,"):
        parts = line.split(",", 1)
        parts[1] = vi_text
        return ",".join(parts)
    parts = line.split(",", 5)
    parts[2] = vi_text
    return ",".join(parts)


def main() -> None:
    raw = EN.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)

    # Preflight: compare <br> counts and ASCII comma for covered text lines
    errors = []
    for i, rl in enumerate(lines):
        ln = i + 1
        line = rl.rstrip("\r\n")
        if line.startswith("title,"):
            vi = TITLE_VI
        elif ln in MESSAGE_VI:
            vi = MESSAGE_VI[ln]
        else:
            continue
        old_tf = line.split(",", 1)[1] if line.startswith("title,") else line.split(",", 5)[2]
        if old_tf.count("<br>") != vi.count("<br>"):
            errors.append(f"LINE {ln}: <br> count {old_tf.count('<br>')} -> {vi.count('<br>')}")
        if "," in vi:
            errors.append(f"LINE {ln}: ASCII comma in VI text field")
        if "，" in vi:
            errors.append(f"LINE {ln}: fullwidth comma left in VI")
    if errors:
        raise SystemExit("PREFLIGHT FAILED:\n" + "\n".join(errors))

    out_lines = []
    for i, rl in enumerate(lines):
        ln = i + 1
        line = rl.rstrip("\r\n")
        if line.startswith("title,"):
            new_line = replace_text_field(line, TITLE_VI)
        elif ln in MESSAGE_VI:
            new_line = replace_text_field(line, MESSAGE_VI[ln])
        else:
            new_line = line
        out_lines.append(new_line + rl[len(line):])

    out = "".join(out_lines)
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"Wrote {VI} ({len(out_lines)} lines)")


if __name__ == "__main__":
    main()
