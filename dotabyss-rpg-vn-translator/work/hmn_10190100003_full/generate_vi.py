#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deterministic VI generator for hmn_10190100003.

Reads the EN asset (which holds the JP source text for this project),
replaces only the translatable text field of title/message records in
file order, converts any ASCII comma inside a text field to U+201A,
and writes the VI output preserving BOM + CRLF and all technical fields.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10190100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10190100003.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10190100003_full"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
SUB_COMMA = "\u201a"  # ‚ U+201A


def c2sub(s: str) -> str:
    """Replace ASCII commas inside a text field with U+201A."""
    return s.replace(",", SUB_COMMA)


TITLE_VI = "Quyết Đấu! Kết Cục Trận Đấu Là……!?"

# 96 message text fields in file order (aligned to EN asset message lines)
MSG_VI = [
    "Thế nào?<br>Hàng tôi thu thập đấy.",
    "Tôi đã xem bản kê khai, hàng hóa đúng là tốt thật đấy.",
    "Nhưng, Aura.<br>Vốn dĩ anh mới là người giao việc cho Lucita cơ. Sao cậu lại đến giao hàng?",
    "Hứ, nói năng ngây thơ thật đấy. Thương trường luôn là mạnh được yếu thua!<br>Kẻ chuẩn bị hàng tốt hơn, nhanh hơn mới là người chiến thắng!",
    "Đúng không?",
    "Phi vụ đó! Khoan đã------!",
    "Ồn ôn, đến muộn quá nhỉ, Lucita.",
    "Aura! Từ xưa đến nay cậu lúc nào cũng<br>làm phiền việc của tôi……!",
    "Thật bất ngờ. Cậu cũng là thương nhân mà, sao không nghĩ đến việc quảng bá bản thân<br>trước khi đi chỉ trích người khác?",
    "Thích nhảy vào giữa rồi lên mặt dạy đời à!",
    "Ra thế.<br>Tức là Aura định qua mặt Lucita đúng không.",
    "Hứ, nhạy bén đấy. Nhưng Chỉ Huy cũng bậy bạ thật.<br>Đáng ra từ đầu cứ giao cho tôi thì xong chuyện sớm hơn.",
    "Đứng ở vị trí trông coi tiền tuyến‚ hẳn là phải chọn kỹ<br>đối tác giao dịch chứ?",
    "Ồ?<br>Vậy tức là cậu cho mình là đối tác giao dịch tốt hơn đúng không.",
    "Tất nhiên.<br>Đương nhiên rồi.",
    "Tôi cũng đã dồn hết sức thu thập mà!<br>Chỉ là bị cậu đi trước một chút thôi!",
    "Ô hô hô hô!<br>Tiếng hú của kẻ bại trận vang xa thật đấy!",
    "Chưa quyết là thua đâu!<br>Chỉ Huy, xem cả bản kê khai giao hàng của tôi nữa đi!",
    "À, tôi sẽ xem qua chuyện đó…….<br>Hai đứa bây, tại sao quan hệ lại tệ thế? Là quen biết lâu năm mà nhỉ?",
    "Tôi không biết đâu.<br>Ả này lúc nào cũng coi thường người khác.",
    "Còn cậu thì, dù thua tôi bao nhiêu lần vẫn cứ thách đấu mãi.",
    "Tôi không thích kiểu cứ ăn đòn mãi.<br>Vả lại, tôi chưa bao giờ nghĩ mình thua đâu!",
    "Thật đấy, cậu đúng ghét thua cuộc ghê~.",
    "――Đúng vậy, chỉ có mình cậu thôi.<br>Là người tiếp tục đấu với tôi.",
    "Hả?",
    "Dù bao kẻ khác đã thôi đấu với tôi,<br>chỉ riêng cậu là mãi mãi cứ bám lấy, không chịu thua tôi.",
    "Vì thế tôi cũng đã có thể nỗ lực hơn,<br>để không thua một cậu như cậu.",
    "N, n, sao tự dưng vậy.",
    "Ra thế. Tức là cùng hội cùng thuyền nhỉ.",
    "Cùng hội cùng thuyền……?",
    "Đúng không? Cả hai đều ghét thua cuộc như nhau.<br>Aura cũng chẳng muốn thua cậu nên mới đấu suốt đúng không.",
    "Aura mà, lại nói với tôi……?",
    "……Tôi cứ nghĩ cậu chẳng bao giờ để tôi trong mắt.",
    "Đừng có nói bậy.<br>Cậu ồn ào như vậy, làm sao mà bỏ mặc được chứ.",
    "N, nói cái gì chứ!<br>Cậu mới là người ồn ào hơn mà!",
    "Aura. Cậu không còn điều gì muốn nói sao?",
    "Chuyện đó thì…….",
    "Này, có gì muốn nói thì nói đi.<br>Aura mà dây dưa thế này chẳng hợp chút nào.",
    "……Ưn~~~~tôi, thôi đi!<br>Cậu đúng là khó đối phó quá chừng!",
    "Ơ kìa, đúng thế! Đối thủ của tôi chỉ có Lucita!<br>Không có cậu thì chẳng còn ai đấu với tôi nữa!",
    "Hể!? Đối thủ……?",
    "Đúng vậy! Vì thế tôi mới bực mình khi cậu được Chỉ Huy giao việc rồi hăng hái thế!<br>Như thể chẳng thèm để tôi vào mắt vậy!",
    "Hể!?<br>H, hóa ra là lý do đó sao!?",
    "~~~~tôi, thật tình, nói cái gì chứ.<br>Làm tôi mất nhịp quá…….",
    "Hiểu rồi……. Đã thế thì thôi.<br>Dù cay đắng nhưng đúng là Aura làm tốt hơn tôi.",
    "Lần này, tôi thua.",
    "Ồ, dễ dàng nhận thua thế, chẳng giống cậu chút nào.",
    "Hàng Aura chuẩn bị chắc chẳng kém chất lượng đâu.<br>Thế thì xét về giao hàng nhanh, Aura mới là người giỏi.",
    "Lần này tôi cũng học được nhiều.<br>Nhưng lần sau tôi sẽ không thua đâu!",
    "Lucita, cậu…….",
    "Hứ……. Cậu như thể đã lột xác rồi đấy.<br>Từ giờ có vẻ sẽ là đối thủ khó nhằn hơn.",
    "Â, chuẩn bị đi nhé!",
    "Nói tóm lại, Chỉ Huy.<br>Hàng tôi chuẩn bị thì tôi sẽ mang về.",
    "Không, tôi sẽ nhận hàng Lucita chuẩn bị.",
    "……Hả!?",
    "Sao lại ngạc nhiên thế.<br>Vốn dĩ tôi đâu có đặt luật giao hàng trước thì thắng.",
    "Tôi vừa xem xong bản kê khai giao hàng của Lucita.<br>Vì thấy hàng của Lucita tốt nên tôi mới chọn cậu.",
    "T, thật sao!?<br>Nhưng tại sao lại là tôi?",
    "Tôi nghe lý do được không?",
    "Hàng Aura chuẩn bị đúng là toàn đồ cao cấp, chất lượng đảm bảo.<br>Xét ở điểm đó thì không chê vào đâu được.",
    "Nhưng――đó là nếu ở Eldorana.",
    "Nếu là Eldorana……?<br>Ý là sao cơ?",
    "Lucita. Cậu cố tình không lấy hàng cao cấp mà<br>nhập nhiều hàng đại trà. Tại sao vậy?",
    "À, ra là vậy. Tiền tuyến không có môi trường tốt như Eldorana,<br>chắc máy móc cũng dễ hỏng đúng không?",
    "Nhất là máy móc thiết kế phức tạp, hỏng thì cần thợ sửa chuyên môn.<br>Nhưng chẳng mấy khi có thợ chịu đến tận tiền tuyến nguy hiểm để sửa đâu.",
    "Nên lần này, chất lượng đúng là quan trọng,<br>nhưng tôi nghĩ độ bền và dễ bảo trì cũng thiết yếu.",
    "…………!",
    "Này, tôi vốn trước đây làm nghề cướp biển mà?<br>Trên biển mà hỏng gì thì cũng chẳng sửa ngay được.",
    "Ở môi trường đó thì đồ chắc chắn hay đơn giản mới dễ dùng.<br>Nên tôi nghĩ ở tiền tuyến hàng đại trà vẫn tốt hơn.",
    "Cậu tính toán xa đến thế cơ…….",
    "Đúng thế. Lúc đặt hàng, anh cố tình không nói rõ yêu cầu.<br>Vì tin Lucita sẽ tự chọn được món phù hợp mà không cần nhắc.",
    "Kết quả là Lucita đã chuẩn bị hàng như anh kỳ vọng.<br>Aura. Cần giải thích thêm không?",
    "……Không. Tôi hiểu rồi.<br>Đúng là tôi dường như đã không thỏa mãn nhu cầu khách hàng.",
    "Nghĩ lại thì từ đầu tôi chỉ nghĩ đến chuyện thắng Lucita,<br>còn Lucita chỉ nghiêm túc nghĩ cho khách hàng thôi…… thua là đúng rồi.",
    "Aura…….",
    "(Đến cả Aura cũng sốc vì thua sao……)",
    "――Thôi, đã thế thì hàng tôi chuẩn bị<br>tôi sẽ đem bán tống ở tiệm cao cấp ngoài chợ.",
    "Hả……?",
    "Ở tiền tuyến khó mà mua được hàng cao cấp thế.<br>Chắc chắn bán được giá cao thôi~♪",
    "Á, còn nữa Lucita. Hôm nay thì tôi thua,<br>nhưng lần sau nhất định tôi thắng nên cứ rửa sạch cổ mà đợi nhé!",
    "Vậy hai người, chào nhé~.",
    "…………",
    "Sao nhỉ…… bả đúng là không biết nản.",
    "……Ha ha! Đúng là thế!<br>Tôi chưa từng thấy Aura buồn bã thế này!",
    "Ra thế. Dù sao thì giao hàng xong rồi. Cậu làm tốt lắm.",
    "Nào, cảm thấy thế nào? Sau khi làm xong một việc lớn.",
    "Có vất vả nhưng là một trải nghiệm tốt!",
    "Chỉ Huy, cảm ơn anh đã giao việc cho tôi!",
    "À, còn nữa…….",
    "Ưm? Có chuyện gì?",
    "Thỉnh thoảng anh cũng để ý đến Aura giùm tôi được không?",
    "Này, ả ấy hay gây rắc rối đủ thứ nên tôi hơi lo.<br>Sợ ả dính vào chuyện với bọn nước khác.",
    "Hứ, được thôi. Coi như phần thưởng vì cậu đã làm tốt.",
    "Ô, cảm ơn anh!",
    "Nhờ Chỉ Huy mà tôi cũng tự tin hơn trước!<br>Từ giờ tôi sẽ tiếp tục buôn bán rôm rả…….",
    "Vẫn mong được anh giúp đỡ tiếp nhé!",
]


def main() -> None:
    raw = EN.read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    # Normalize: split on newline, strip any trailing CR (source is CRLF).
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    has_crlf = b"\r\n" in raw
    out_lines: list[str] = []
    msg_idx = 0
    title_done = False
    entries: list[dict] = []

    counts = {c[:-1]: 0 for c in TEXT_CMDS}

    for line in lines:
        if line.startswith("title,"):
            parts = line.split(",", 1)
            vi = c2sub(TITLE_VI)
            entries.append({"cmd": "title", "speaker": "", "jp": parts[1], "vi": vi})
            counts["title"] += 1
            out_lines.append("title," + vi)
            title_done = True
        elif line.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
            parts = line.split(",")
            cmd = parts[0]
            speaker = parts[1]
            jp = parts[2] if len(parts) > 2 else ""
            if cmd == "message":
                if msg_idx >= len(MSG_VI):
                    raise SystemExit(f"MSG_VI exhausted at line: {line[:40]}")
                vi = c2sub(MSG_VI[msg_idx])
                msg_idx += 1
            else:
                vi = c2sub(jp)  # no translation available; keep (should not happen)
            counts[cmd.rstrip(",")] += 1
            new_parts = list(parts)
            new_parts[2] = vi
            out_lines.append(",".join(new_parts))
            entries.append({"cmd": cmd[:-1], "speaker": speaker, "jp": jp, "vi": vi})
        else:
            out_lines.append(line)

    if not title_done:
        raise SystemExit("title record not found")
    if msg_idx != len(MSG_VI):
        raise SystemExit(f"message count mismatch: generated {msg_idx}, expected {len(MSG_VI)}")

    # Guard: no ASCII comma inside any VI text field
    for e in entries:
        if "," in e["vi"]:
            raise SystemExit(f"ASCII comma leaked into VI text: {e['vi']!r}")

    out_text = "\n".join(out_lines)
    VI.parent.mkdir(parents=True, exist_ok=True)
    # Write with BOM if source had it; restore CRLF if source had CRLF.
    if has_crlf:
        out_text = out_text.replace("\n", "\r\n")
    VI.write_bytes(("\ufeff" + out_text).encode("utf-8") if had_bom else out_text.encode("utf-8"))

    src_sha = hashlib.sha256(raw).hexdigest()
    out_sha = hashlib.sha256(VI.read_bytes()).hexdigest()

    manifest = {
        "scene": "hmn_10190100003",
        "source_file": str(EN),
        "output_file": str(VI),
        "source_sha256": src_sha,
        "output_sha256": out_sha,
        "bom_preserved": had_bom,
        "newline": "CRLF" if has_crlf else "LF",
        "candidate_counts": counts,
        "translatable_records": sum(counts.values()),
        "translated_records": sum(counts.values()),
        "title_translated": True,
        "entries": entries,
        "notes": [
            "Speaker names ルシータ/アウラ/<user>/ルシータ・アウラ kept unchanged (no explicit mapping).",
            "Commander 司令官 -> Chỉ Huy; 俺 (male Commander) -> anh; women アタシ -> tôi; mutual アンタ/おまえ -> cậu.",
            "ASCII commas inside VI text fields converted to U+201A (‚).",
            "Source EN asset holds JP text for this project; ja.json/en.json are JP/blank references.",
        ],
    }
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # focused diff (translatable lines only)
    diff_lines = []
    for e in entries:
        diff_lines.append(f"- {e['cmd']},{e['speaker']},{e['jp']}")
        diff_lines.append(f"+ {e['cmd']},{e['speaker']},{e['vi']}")
        diff_lines.append("")
    (WORK / "focused_diff.md").write_text("\n".join(diff_lines), encoding="utf-8")

    print(f"OK title={counts['title']} message={counts['message']} msg_idx={msg_idx}")
    print(f"src_sha={src_sha}")
    print(f"out_sha={out_sha}")


if __name__ == "__main__":
    main()
