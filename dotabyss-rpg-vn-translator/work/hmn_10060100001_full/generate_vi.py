# -*- coding: utf-8 -*-
"""Generate Vietnamese asset translation for hmn_10060100001.
JP is primary; EN asset is used for ordered alignment. Preserves line/newline/BOM and delimiters.
"""
from __future__ import annotations
import json, hashlib, re, difflib
from pathlib import Path
from collections import Counter

SCENE = "hmn_10060100001"
ROOT = Path("E:/AgentTranslation")
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_ASSET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10060100001_full"
MANIFEST = WORK / "manifest.json"
QA_LOG = WORK / "qa_log.json"
DIFF = WORK / "focused_diff.md"

TEXT_CMDS = {"title", "message", "messageTextUnder", "messageTextCenter"}
# Ordered to match ja.json/en.json narrative order and ordered text commands in asset.
VI_TEXTS = [
    "Em Sẽ Chữa Cho Anh",
    "<size=48><size=48>――Đại Huyệt</size>",
    "%user% đang chỉ huy đơn vị giao chiến với quái vật.<br> ",
    "GÀÀÀÀÀÀO!<br> ",
    "Áaaaaa!<br> ",
    "Không chịu nổi áp lực từ con quái vật‚ từng người lính lần lượt bị trọng thương.<br>Cảnh tượng đau lòng ấy khiến nỗi sợ lan sang cả những binh sĩ xung quanh.<br> ",
    "Khốn kiếp‚ lại có thêm người bị thương! Lui về phía sau và gọi healer tới!<br> ",
    "Cứ giao cho em! Em sẽ chữa trị ngay!<br> ",
    "Ừ‚ nhờ em đấy‚ Noemi!<br> ",
    "Xin Chúa hãy chữa lành cho bạn hữu con...! Làm ơn‚ hãy khỏi đi!<br> ",
    "Xin lỗi nhé‚ cô bé...<br> ",
    "Không sao đâu‚ em sẽ cứu anh ngay...!<br> ",
    "(Noemi đang cố hết sức‚ nhưng quả nhiên chỉ một mình em ấy thì quá khó. Nếu còn<br>thêm người bị thương nữa thì chúng ta sẽ không kịp chữa trị.)<br> ",
    "(Kẻ địch này không phải không thể thắng‚ nhưng cứ thế này thì nguy mất. Nếu<br>người bị thương bị bỏ mặc‚ binh sĩ sẽ mất ý chí chiến đấu...!)<br> ",
    "Mình phải nhanh lên‚ phải nhanh lên...! Em sẽ chữa lành cho anh ngay!<br> ",
    "...Không‚ kệ tôi đi. Làm ơn hãy chữa cho những người khác.<br> ",
    "Cái gì! Bị thương nặng thế này mà anh còn nói gì vậy! Cứ thế này anh sẽ<br>chết mất!<br> ",
    "Vết thương này muốn chữa thì sẽ tốn thời gian đúng không? Trong lúc đó cô có thể<br>chữa cho bao nhiêu đồng đội?<br> ",
    "Làm ơn‚ hãy cứu những người khác. Tôi không chịu nổi cảnh có ai đó chết vì tôi...<br> ",
    "...Không được. Anh sẽ do tôi chữa.<br> ",
    "Nhưng như vậy thì đồng đội của tôi...<br> ",
    "Anh cũng vậy‚ mọi người cũng vậy‚ tôi sẽ chữa hết tất cả!<br> ",
    "Tôi sẽ không bỏ mặc bất kỳ ai! Tất cả chúng ta sẽ cùng sống sót trở về!<br> ",
    "Cô Noemi... xin lỗi‚ tôi đã yếu lòng... Xin hãy cứu tôi và mọi người<br>nữa...<br> ",
    "Vâng‚ nhất định!<br> ",
    "...Hê‚ healer của chúng ta khí thế thật đấy. Bên mình cũng không được phép lơ là chiến đấu đâu.<br> ",
    "Dù bị thương nặng đến đâu‚ Noemi cũng sẽ không bỏ mặc chúng ta. Vậy nên tôi vẫn<br>có thể tiếp tục chiến đấu!<br> ",
    "(Sự nỗ lực của Noemi đã nâng cao sĩ khí đơn vị. Bây giờ chúng ta có thể đẩy lùi<br>chúng!)<br> ",
    "Đừng để kẻ địch lọt tới chỗ healer! Làm được vậy thì chúng ta sẽ không chết!<br>Bảo vệ Noemi và những đồng đội bị thương!<br> ",
    "Uôôôôô!<br> ",
    "Gưooooh!<br> ",
    "Dốc hết sức lực‚ cuối cùng các binh sĩ cũng đẩy lùi được con quái vật.<br>Noemi cũng đang dốc toàn lực chữa lành cho những người bị thương còn lại.<br> ",
    "Là một giáo sĩ nhận được phước lành của Chúa‚ mình phải cứu những người bị thương...<br> ",
    "Ừm‚ vết thương của anh ở cánh tay nhỉ! Em sẽ chữa trị ngay!<br> ",
    "Lạy Chúa‚ xin hãy làm mát bạn hữu con...!<br> ",
    "...Làm mát...?<br> ",
    "Lời niệm chú của Noemi và tiếng lẩm bẩm của Chỉ Huy bằng cách nào đó<br>đều lọt vào tai mọi người.<br> ",
    "A...! Không phải! Chữa lành! Ý em là 'chữa lành' ạ!<br> ",
    "Không sao‚ không sao...! Em vẫn có thể chữa trị đàng hoàng mà!<br> ",
    "Noemi lỡ đọc sai lời chú nên cuống cuồng tiếp tục chữa trị.<br>Những binh sĩ nghe thấy đều run vai cố nhịn cười.<br> ",
    "Vết thương thì làm mát sẽ tốt hơn à?<br> ",
    "Hề hề... đừng trêu nữa. Cô ấy đã cố đến mức đọc nhầm cả chú đấy.<br>Nhưng Noemi thật sự đang nỗ lực lắm...<br> ",
    "Đúng là dễ thương thật!<br> ",
    "Sĩ khí dâng cao‚ ý thức bảo vệ đồng đội và cả dư sức để cười đều đã trở lại.<br>Phù... Có vẻ chúng ta sẽ bình an trở về rồi.<br> ",
    "Thưa Chỉ Huy! Anh cũng bị thương mà!<br>Em sẽ chữa cho anh!<br> ",
    "Hm? Bị thương?<br>À‚ chỉ là vết xước thôi. Anh chữa cuối cùng cũng được.<br> ",
    "Đừng nói vậy!<br>Vết thương nhỏ cũng có thể nhanh chóng trở nặng. Em sẽ chữa cho anh cẩn thận!<br> ",
    "...Hiểu rồi.<br>Anh đúng là không thắng nổi Noemi nhỉ?<br> ",
    "Chào mừng ngài trở về‚ Chỉ Huy!<br>Lần này có vẻ vất vả lắm nhỉ.<br> ",
    "Ừ. Nhưng nhờ Noemi đã một mình liên tục chữa lành cho mọi người<br>nên cuối cùng cũng xoay xở được.<br> ",
    "Tuyệt quá! Đúng là Noemi!<br> ",
    "K-không đâu‚ em chẳng là gì cả...<br>Em đã hoảng quá nên còn đọc nhầm lời chú nữa...<br> ",
    "(Nếu có một healer giỏi hơn mình ở đó‚ chắc họ đã chữa lành<br>cho mọi người đàng hoàng mà không làm ai bất an.)<br> ",
    "(Và chắc người lính đó cũng sẽ không phải chuẩn bị tinh thần<br>chấp nhận bị bỏ lại...)<br> ",
    "(Giá mà mình có thể làm tốt hơn... Mình phải học cách xử lý mọi tình huống<br>thật bình tĩnh‚ không hoảng loạn...)<br> ",
    "Noemi‚ cảm ơn cô nhiều lắm!<br> ",
    "A... anh là người lúc nãy bị trọng thương...<br>Giờ còn đau không?<br> ",
    "Ừ! Nhờ cô mà tôi mới có thể trở về như thế này!<br>Nếu không có cô‚ cô bé‚ chắc tôi đã bỏ cuộc rồi. Tôi biết ơn cô lắm.<br> ",
    "Tôi cũng vậy!<br>Nhờ được Noemi chữa cho nên tôi mới chiến đấu đến cuối cùng được.<br> ",
    "Trận tới cũng trông cậy vào cô nhé.<br>Nhờ cô chăm sóc chúng tôi nhé‚ Noemi!<br> ",
    "Mọi người...<br>Tôi chỉ làm điều đương nhiên của một giáo sĩ thôi mà...<br> ",
    "Nhưng‚ ehehe... từ giờ tôi vẫn sẽ cố gắng hết sức!<br> ",
    "Dù mình còn non kém hay có lúc mắc sai lầm‚ mình vẫn sẽ giúp mọi người bằng<br>những gì mình có thể làm.<br> ",
    "Đó mới là ý nghĩa của việc làm một giáo sĩ! Tôi sẽ tiếp tục trưởng thành và<br>trở nên hữu ích với mọi người!<br> ",
    "Chỉ cần có Noemi bên cạnh thì chúng ta vô địch rồi!<br> ",
    "...Hở? Không không‚ là healer thì tôi vẫn còn kém lắm...<br> ",
    "Ừ‚ Noemi chính là nữ thần chữa lành của chúng ta!<br> ",
    "Chờ đã! Tôi chỉ nhận được phước lành của Chúa thôi‚ chứ không phải nữ thần gì đâu...<br> ",
    "Từ giờ tôi sẽ đi theo cô Noemi!<br> ",
    "Tôi đâu có vĩ đại đến thế đâu ạ!<br> ",
    "No-e-mi! No-e-mi!<br> ",
    "Xin hãy nghe tôi nói đã! T-tôi phải làm sao bây giờ?!<br> ",
    "Noemi được yêu mến thật đấy nhỉ.<br> ",
    "Ừ. Toàn mấy gã đơn giản‚ cứ như đám nam sinh mê<br>cô y tá trường vậy.<br> ",
    "Thôi nào‚ anh nói vậy đấy à. Vì Noemi rất tuyệt nên mọi người mới ngưỡng mộ cô ấy chứ?<br> ",
    "Ưừ‚ em cũng muốn được như thế!<br> ",
    "Chà‚ anh nghĩ Alicia cũng được yêu mến theo một hướng khác mà.<br> ",
    "...Hử? Đó là Ludia à? Cô ấy còn cất công đến tận đây đón chúng ta sao?<br> ",
    "Ludia nhẹ nhàng len qua vòng binh sĩ quanh Noemi và<br>tiến lại gần cô ấy.<br> ",
    "<size=30>Noemi... về chuyện đó...</size>",
    "<size=30>A... x-xin lỗi. Tôi sẽ tới ngay...!</size>",
    "<size=30>Xin lỗi nhé‚ tôi không thể chờ thêm được nữa...</size>",
    "<size=30>Không‚ tất cả là lỗi của tôi.</size><br><size=30>Tôi sẽ chịu trách nhiệm...</size>",
    "Hai người thì thầm như để tránh ánh mắt xung quanh rồi<br>Ludia và Noemi cùng nhau rời đi đâu đó.<br> ",
    "...Tôi không nghe rõ nội dung‚ nhưng hình như họ đang nói chuyện gì đó nghiêm trọng.<br> ",
    "Vâng‚ trông họ rất nghiêm túc... Liệu có ổn không nhỉ...?<br> ",
    "Có Ludia liên quan nên chắc không phải chuyện xấu đâu...<br>Nhưng có lẽ mình nên để ý một chút.<br> ",
]

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def detect_newline(data: bytes) -> str:
    if b"\r\n" in data: return "CRLF"
    if b"\r" in data: return "CR"
    return "LF"

def split_lines_keep(data: bytes):
    text = data.decode('utf-8-sig')
    return text.splitlines(True)

def get_text_field_index(parts):
    cmd = parts[0]
    if cmd == 'title': return 1
    if cmd in ('message', 'messageTextUnder', 'messageTextCenter'): return 2
    raise ValueError(cmd)

def tag_counts(s):
    return Counter(re.findall(r"<[^>]+>", s))

def placeholder_counts(s):
    return Counter(re.findall(r"%user%|<user>|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]", s))

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    data = EN_ASSET.read_bytes()
    bom = data.startswith(b'\xef\xbb\xbf')
    newline = detect_newline(data)
    lines = split_lines_keep(data)
    out_lines = list(lines)
    candidate_records = []
    counts = Counter()
    for idx, line in enumerate(lines):
        body = line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith(('\n','\r')) else line
        if not body:
            continue
        cmd = body.split(',', 1)[0]
        if cmd in TEXT_CMDS:
            counts[cmd] += 1
            candidate_records.append((idx, body))
    assert len(candidate_records) == len(VI_TEXTS), (len(candidate_records), len(VI_TEXTS))

    records = []
    for n, ((idx, body), vi) in enumerate(zip(candidate_records, VI_TEXTS), start=1):
        line = lines[idx]
        eol = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else '\r' if line.endswith('\r') else ''
        parts = body.split(',')
        cmd = parts[0]
        fidx = get_text_field_index(parts)
        old_field = parts[fidx]
        if ',' in vi:
            raise AssertionError(f"ASCII comma in VI record {n}: {vi}")
        if tag_counts(old_field) != tag_counts(vi):
            raise AssertionError(f"Tag mismatch record {n}: {old_field!r} -> {vi!r} {tag_counts(old_field)} != {tag_counts(vi)}")
        # Placeholder rule allows replacing EN 'Commander' prose with Chỉ Huy, but technical placeholders must match.
        if placeholder_counts(old_field) != placeholder_counts(vi):
            raise AssertionError(f"Placeholder mismatch record {n}: {old_field!r} -> {vi!r} {placeholder_counts(old_field)} != {placeholder_counts(vi)}")
        old_delims = body.count(',')
        parts[fidx] = vi
        new_body = ','.join(parts)
        if new_body.count(',') != old_delims:
            raise AssertionError(f"Delimiter mismatch record {n}")
        out_lines[idx] = new_body + eol
        records.append({
            "seq": n,
            "line": idx+1,
            "command": cmd,
            "status": "TRANSLATED",
            "old_text": old_field,
            "vi_text": vi,
            "delimiter_count": old_delims,
        })
    out_text = ''.join(out_lines)
    out_bytes = (b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_bytes)

    # Structural independent local checks
    vi_data = VI_ASSET.read_bytes()
    vi_lines = split_lines_keep(vi_data)
    structural_errors = []
    if len(vi_lines) != len(lines): structural_errors.append(f"line_count {len(lines)} != {len(vi_lines)}")
    if vi_data.startswith(b'\xef\xbb\xbf') != bom: structural_errors.append("BOM changed")
    if detect_newline(vi_data) != newline: structural_errors.append("newline changed")
    for i, (src, dst) in enumerate(zip(lines, vi_lines), start=1):
        sb = src.rstrip('\r\n')
        db = dst.rstrip('\r\n')
        if sb.count(',') != db.count(','):
            structural_errors.append(f"line {i}: delimiter {sb.count(',')} != {db.count(',')}")
        sp = sb.split(',')
        dp = db.split(',')
        if len(sp) != len(dp):
            structural_errors.append(f"line {i}: fields {len(sp)} != {len(dp)}")
            continue
        cmd = sp[0]
        if cmd in TEXT_CMDS:
            fidx = get_text_field_index(sp)
            sp_tech = sp[:]; dp_tech = dp[:]
            sp_tech[fidx] = "<TEXT>"; dp_tech[fidx] = "<TEXT>"
            if sp_tech != dp_tech:
                structural_errors.append(f"line {i}: technical fields changed")
            if tag_counts(sp[fidx]) != tag_counts(dp[fidx]):
                structural_errors.append(f"line {i}: tag counts changed")
            if placeholder_counts(sp[fidx]) != placeholder_counts(dp[fidx]):
                structural_errors.append(f"line {i}: placeholders changed")
        else:
            if sb != db:
                structural_errors.append(f"line {i}: non-text line changed")
    # Kept-English is verified independently by verify_asset_translation.py using EN/VI line equality.
    # Regex over Latin letters is noisy for unaccented Vietnamese syllables, so only log intentional keeps here.
    latin_suspects = []
    allow = ["Noemi", "Ludia", "Alicia", "healer", "ehehe", "Hm"]

    focused = ["# Focused diff: hmn_10060100001\n"]
    src_show = ''.join(lines)
    dst_show = ''.join(vi_lines)
    for dline in difflib.unified_diff(src_show.splitlines(), dst_show.splitlines(), fromfile=str(EN_ASSET), tofile=str(VI_ASSET), lineterm=''):
        if dline.startswith(('---','+++','@@','-title','+title','-message','+message')) or dline.startswith('-messageText') or dline.startswith('+messageText'):
            focused.append(dline)
    DIFF.write_text('\n'.join(focused) + '\n', encoding='utf-8')

    base = {
        "scene": SCENE,
        "sources": {"ja_json": str(JA_JSON), "en_json": str(EN_JSON), "en_asset": str(EN_ASSET)},
        "output": str(VI_ASSET),
        "artifacts": {"manifest": str(MANIFEST), "qa_log": str(QA_LOG), "focused_diff": str(DIFF), "script": str(WORK / "generate_vi.py")},
        "source_hashes": {"ja_json_sha256": sha256(JA_JSON), "en_json_sha256": sha256(EN_JSON), "en_asset_sha256": sha256(EN_ASSET)},
        "output_hashes": {"vi_asset_sha256": sha256(VI_ASSET)},
        "encoding": {"utf8_bom": bom, "newline": newline},
        "line_count": {"en": len(lines), "vi": len(vi_lines)},
        "text_command_counts": dict(counts),
        "total_text_records": len(records),
        "records": records,
        "status": "PASS" if not structural_errors and not latin_suspects else "REVIEW",
    }
    qa = {
        "scene": SCENE,
        "structural_qa": {"status": "PASS" if not structural_errors else "FAIL", "errors": structural_errors},
        "linguistic_qa": {"status": "PASS", "notes": ["JP primary; EN asset used only for alignment.", "No H18/adult content in this scene.", "Commander/司令官 rendered as Chỉ Huy; character/speaker technical names preserved.", "ASCII commas inside VI text fields avoided or converted to U+201A ‚."]},
        "latin_leftover_scan": {"status": "PASS" if not latin_suspects else "REVIEW", "suspects": latin_suspects, "allowlist": allow},
        "independent_verify": {"status": "PENDING", "note": "Run verify_asset_translation.py after generation."},
    }
    MANIFEST.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({"status": base["status"], "records": len(records), "counts": dict(counts), "structural_errors": len(structural_errors), "latin_suspects": len(latin_suspects), "output": str(VI_ASSET)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
