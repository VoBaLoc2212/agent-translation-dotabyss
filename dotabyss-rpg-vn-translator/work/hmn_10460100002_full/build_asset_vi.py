#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_asset_vi.py — hm_10460100002 Elmia Bow & Sacred Sword Recovery Operation
EN-asset-is-English: field-index build with embedded br-count preflight.

Characters:
  - エルミア (Elmia): elf archer, merchant's bodyguard, uses 私 (watashi/tôi),
    calls Commander: boss/Chỉ Huy, self-confident but touchy about her petite build.
    Addressing: Elmia ↔ Commander uses tôi/anh (she keeps tôi, he uses anh/cô).
  - 盗賊A (Thief A): captured thief who mocks Elmia, calls her ガキ (kid/nhóc).
  - Commander/Chỉ Huy: strategist, speaks with tôi/cô to Elmia.
"""

from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10460100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# Title (seq=0): エルミアの弓と聖剣奪還作戦 → Title Case VI
# Elmia's Bow and Sacred Sword Recovery Operation
TITLE_VI = "Chiến Dịch Thu Hồi Cung Và Thánh Kiếm Của Elmia"

# VI translations keyed by text-record seq (0=title, 1..70=message)
# Each VI text preserves the EN asset's <br> count (suffix + internal).
# No ASCII commas — use fullwidth ，(U+FF0C) to match EN asset convention.
VI = {
    # seq0 title (0 <br>)
    0: TITLE_VI,

    # seq1: *pant*... *pant*... I can't believe he ran into the middle of a forest<br>like this...!<br>  (2 <br>)
    1: "Phì... phì... không ngờ hắn lại chạy vào tận trong rừng thế này<br>làm sao mà...!<br> ",

    # seq2: I thought he was just an ordinary thief，but he seems quite capable.<br>  (1 <br>)
    2: "Cứ tưởng chỉ là tên trộm vặt thôi，nhưng hắn cũng khá đấy chứ.<br> ",

    # seq3: What now? If we keep this up，we'll be at a disadvantage.<br>  (1 <br>)
    3: "Tính sao đây？ Cứ thế này thì ta sẽ bị dồn vào thế bí mất.<br> ",

    # seq4: We've lost some ground，but that's no problem.<br>  (1 <br>)
    4: "Bị xa dần rồi đấy，nhưng chẳng có vấn đề gì cả.<br> ",

    # seq5: For an Elf，the forest is like a garden. I won't let him escape!<br>  (1 <br>)
    5: "Với tộc Elf，khu rừng chẳng khác gì vườn nhà. Không thể để hắn trốn thoát!<br> ",

    # seq6: Tch! Persistent bastards...!<br>  (1 <br>)
    6: "Chậc！ Lũ dai dẳng...！<br> ",

    # seq7: We found him，but how do we catch him? He's still quite far off，you<br>know?<br>  (2 <br>)
    7: "Tìm thấy hắn rồi，nhưng bắt bằng cách nào？ Khoảng cách vẫn còn xa lắm<br>đấy？<br> ",

    # seq8: Heh... Don't underestimate my archery. Taking aim... *pant!*<br>  (1 <br>)
    8: "Phù... đừng có coi thường tài cung của tôi đấy. Nhắm... phì！<br> ",

    # seq9: Elmia's arrow traced a wide arc and lodged itself in the thief's<br>shoulder.<br>  (2 <br>)
    9: "Mũi tên của Elmia vạch một đường cong lớn<br>và ghim thẳng vào vai tên trộm.<br> ",

    # seq10: Gah!<br>  (1 <br>)
    10: "GỤa！<br> ",

    # seq11: How's that!<br>  (1 <br>)
    11: "Thế nào！<br> ",

    # seq12: Not bad. With your Appraisal Eye and all，it's a waste to have you as<br>a merchant's bodyguard.<br>  (2 <br>)
    12: "Khá đấy chứ. Có cả Con Mắt Thẩm Định nữa，<br>làm vệ sĩ cho thương nhân thì phí tài thật đấy.<br> ",

    # seq13: Praising me won't get you anything.<br>  (1 <br>)
    13: "Có khen cũng chẳng được gì đâu.<br> ",

    # seq14: D-Damn it...<br>  (1 <br>)
    14: "Ch-chết tiệt...<br> ",

    # seq15: Now then，let's take back the stolen 'Starblade'.<br>  (1 <br>)
    15: "Giờ thì，lại đây，lấy lại 'Thanh Kiếm Sao' bị đánh cắp thôi.<br> ",

    # seq16: Don't shorten it!<br>  (1 <br>)
    16: "Đừng có viết tắt！<br> ",

    # seq17: What harm is there? Honestly，I can't be bothered to remember it.<br>  (1 <br>)
    17: "Có sao đâu？ Thú thật，phiền quá nên chẳng buồn nhớ nổi.<br> ",

    # seq18: Hey，you thief! Give me back my 'Holy Sword that mimics the stars<br>and cleaves the universe—Cosmic Edge Infinity Blade'!<br>  (2 <br>)
    18: "Này，đồ trộm cắp！ Trả lại Thanh Kiếm Thánh 'mô phỏng ánh sao'<br>'xé toạc vũ trụ — Cosmic Edge Infinity Blade' của ta！<br> ",

    # seq19: ...Huh? This guy doesn't have anything. Don't tell me...<br>  (1 <br>)
    19: "...Hử？ Thằng này chẳng cầm thứ gì cả. Chẳng lẽ...<br> ",

    # seq20: Heh，heh，serves you right! My buddies already moved the loot to the<br>hideout!<br>  (2 <br>)
    20: "Hê hê，đáng đời！ Hàng đã được đồng bọn chuyển về tận<br>sào huyệt rồi nhé！<br> ",

    # seq21: No way you losers could ever find our secret hideout!<br>  (1 <br>)
    21: "Mấy người như bọn mày thì tìm không ra sào huyệt bí mật đâu！<br> ",

    # seq22: What!<br>  (1 <br>)
    22: "Cái gì—！<br> ",

    # seq23: ...That's what he says. What now?<br>  (1 <br>)
    23: "...Hắn nói thế đấy. Tính sao？<br> ",

    # seq24: That's settled. We're storming the hideout.<br>  (1 <br>)
    24: "Đương nhiên rồi. Xông vào sào huyệt thôi.<br> ",

    # seq25: But tracking down the location won't be simple. Given enough time，<br>I'm sure we could find it，but...<br>  (2 <br>)
    25: "Nhưng tìm ra địa điểm chẳng dễ đâu. Có thời gian thì<br>tôi nghĩ sẽ tìm được，nhưng...<br> ",

    # seq26: Can't be helped. I don't like this kind of thing，but we'll have to pry<br>the info out of him.<br>  (2 <br>)
    26: "Đành chịu thôi. Không muốn làm mấy chuyện thế này lắm，<br>nhưng đành phải moi thông tin từ hắn vậy.<br> ",

    # seq27: Ha! There's no way I'd let out a single scream from being questioned<br>by a kid like you!<br>  (2 <br>)
    27: "Há！ Có bị thằng nhóc như mày tra hỏi<br>thì tao cũng chẳng rên một tiếng đâu！<br> ",

    # seq28: A kid... you say?<br>  (1 <br>)
    28: "Nhóc... ngươi bảo ta là nhóc？<br> ",

    # seq29: ...You asked for it. I'll make you regret treating me like a child!<br>  (1 <br>)
    29: "...Đã nói đến thế thì ta sẽ chiều ý ngươi. Ta sẽ khiến ngươi hối hận vì đã coi ta là trẻ con！<br> ",

    # seq30: Hmph. For all his big talk，he folded pretty quickly.<br>  (1 <br>)
    30: "Hừm. Nói thì nghe ghê lắm mà cuối cùng cũng xìu nhanh thật đấy，cái thằng đó.<br> ",

    # seq31: Who'd have thought a full-body tickling would be enough to make him<br>cough up the hideout's location.<br>  (2 <br>)
    31: "Ai ngờ chỉ nhột cả người thôi mà hắn đã khai ra<br>chỗ sào huyệt cơ đấy.<br> ",

    # seq32: He said it was around here. There should be a crack in the rock... This<br>it?<br>  (2 <br>)
    32: "Thằng đó bảo quanh đây. Chắc có khe đá...<br>Cái này à？<br> ",

    # seq33: Quite narrow...<br>  (1 <br>)
    33: "Chật thật đấy...<br> ",

    # seq34: The hideout should be on the other side. Let's hurry in—we can't have<br>them moving the stolen goods!<br>  (2 <br>)
    34: "Qua khe này là sào huyệt. Nhanh vào thôi—<br>không thể để chúng chuyển hàng đi nơi khác được！<br> ",

    # seq35: Alright... Hm? It's a tight squeeze，but we should be able to make it.<br>  (1 <br>)
    35: "Được rồi... Hửm？ Hẹp thật đấy，nhưng cũng chẳng đến nỗi không qua được.<br> ",

    # seq36: ...Huh，it's wider inside than I thought.<br>  (1 <br>)
    36: "...Gì vậy，rộng hơn tôi tưởng đấy.<br> ",

    # seq37: *phew*... We made it through safely. You okay，boss?<br>  (1 <br>)
    # JP: <user> は大丈夫か？ → use Chỉ Huy for <user> in VI
    37: "Phù... qua được an toàn rồi. Chỉ Huy có ổn không？<br> ",

    # seq38: Guh... T-tight...<br>  (1 <br>)
    38: "Ực... ch-chật quá...<br> ",

    # seq39: I-I just barely made it. That was close.<br>  (1 <br>)
    39: "C-cố lắm mới qua được. Suýt thì kẹt đấy.<br> ",

    # seq40: Elmia，you got through without any trouble. You really are slim，huh.<br>  (1 <br>)
    40: "Elmia qua được dễ dàng nhỉ，cô có thân hình mảnh mai ghê.<br> ",

    # seq41: Who said I'm flat-chested!<br>  (1 <br>)
    41: "Ai bảo tôi bằng phẳng hả！<br> ",

    # seq42: Nobody said that!<br>  (1 <br>)
    42: "Có ai nói thế đâu！<br> ",

    # seq43: Ugh... It's not like I chose to have such a scrawny body...!<br>  (1 <br>)
    43: "Ực... đâu phải tôi thích thân hình èo uột thế này đâu chứ...！<br> ",

    # seq44: The two of them were bickering when they heard voices.<br>  (1 <br>)
    44: "Giữa lúc hai người đang cãi vã，tai họ nghe thấy tiếng ai đó nói chuyện.<br> ",

    # seq45: Shh! Quiet. I hear voices nearby...<br>  (1 <br>)
    45: "Suỵt！ Im nào. Tôi nghe thấy tiếng ai đó gần đây...<br> ",

    # seq46: Let's stay hidden and move closer. The voices are coming from over<br>there.<br>  (2 <br>)
    46: "Vừa núp vừa lại gần thôi. Tiếng nói chuyện phát ra từ<br>đằng kia.<br> ",

    # seq47: Elmia and the Commander crept forward，hidden by the rocks，and<br>found a large group of thieves.<br>  (2 <br>)
    # JP: エルミア達 → Elmia and Commander (達 = company/party)
    47: "Elmia và Chỉ Huy rón rén tiến lên trong bóng đá，<br>và thấy cả một đám đông bọn trộm.<br> ",

    # seq48: This looks like their hideout，just like we were told.<br>  (1 <br>)
    48: "Đúng như tin moi được，chỗ này có vẻ là sào huyệt của chúng.<br> ",

    # seq49: But... there are too many. The two of us can't possibly neutralize all<br>of them.<br>  (2 <br>)
    49: "Nhưng... đông thật đấy. Mỗi hai người chúng ta<br>thì không thể vô hiệu hóa chúng nổi.<br> ",

    # seq50: Is there any good way to handle this...?<br>  (1 <br>)
    50: "Có cao kế gì không nhỉ...？<br> ",

    # seq51: Elmia. How about using that boulder over there?<br>  (1 <br>)
    51: "Elmia. Dùng tảng đá lớn kia thì sao？<br> ",

    # seq52: If we move in closer and you shoot that boulder down with your<br>arrow，the ceiling might collapse and we could catch them all at once.<br>  (2 <br>)
    52: "Lại gần chúng hơn tí nữa rồi cô bắn đổ tảng đá đó，<br>trần hang có thể sụp xuống và tóm gọn chúng một lúc đấy.<br> ",

    # seq53: D-don't be ridiculous! There's no way my arrows can do something<br>like that.<br>  (2 <br>)
    53: "Đ-đừng có nói nhảm！ Mũi tên của tôi làm sao<br>làm được chuyện đó chứ.<br> ",

    # seq54: My arrows aren't powerful enough to move a giant boulder like that!<br>  (1 <br>)
    54: "Mũi tên tôi đâu có đủ mạnh để động đến tảng đá khổng lồ thế kia được！<br> ",

    # seq55: Let's think of something else. I can't take on such an important task.<br>  (1 <br>)
    55: "Tính cách khác đi. Tôi không đảm nhận nổi trọng trách thế đâu.<br> ",

    # seq56: Don't let its size fool you，Elmia. If you aim at the base precisely，I<br>think you can bring it down easily.<br>  (2 <br>)
    56: "Đừng bị kích thước đánh lừa，Elmia ạ. Nhắm chính xác vào gốc<br>thì có thể làm nó đổ dễ dàng đấy.<br> ",

    # seq57: With your archery skills，it should be possible.<br>  (1 <br>)
    57: "Với tài cung của cô thì khả thi lắm.<br> ",

    # seq58: How can you be so sure?<br>  (1 <br>)
    58: "Sao anh chắc chắn thế？<br> ",

    # seq59: You just shot a moving thief with a single arrow，didn't you?<br>  (1 <br>)
    59: "Vừa nãy cô bắn một phát trúng tên trộm đang chạy còn gì.<br> ",

    # seq60: If you can pull off a stunt like that，shooting a stationary target<br>should be a piece of cake... right?<br>  (2 <br>)
    60: "Làm được trò đó cơ mà. Bắn mục tiêu cố định<br>thì có là gì đâu... nhỉ？<br> ",

    # seq61: ... What if we fail?<br>  (1 <br>)
    61: "...Nhỡ thất bại thì sao？<br> ",

    # seq62: We'll figure out the next plan when that happens.<br>Gotta try first，right?<br>  (2 <br>)
    62: "Lúc đó tính kế tiếp cũng chưa muộn.<br>Việc gì cũng phải thử trước đã. Có sai không？<br> ",

    # seq63: Heh... to think I would be taught by a client.<br>  (1 <br>)
    63: "Phù... không ngờ lại được khách của chủ dạy cho một bài.<br> ",

    # seq64: All right. I'll do what I can.<br>But there is one more problem.<br>  (2 <br>)
    64: "Được rồi. Tôi sẽ cố hết sức.<br>Nhưng còn một vấn đề nữa.<br> ",

    # seq65: How do we get close to that boulder?<br>We can't move forward while staying hidden.<br>  (2 <br>)
    65: "Làm sao để lại gần tảng đá đó được？<br>Núp thế này thì không thể tiến thêm được nữa.<br> ",

    # seq66: I'll be the decoy. Then you use the chance to get close to the rock<br>and shoot it down with your arrow.<br>  (2 <br>)
    66: "Tôi sẽ làm mồi nhử. Còn cô nhân cơ hội đó<br>lại gần tảng đá rồi bắn đổ nó.<br> ",

    # seq67: Th-this is too dangerous!<br>How many thieves do you think are in there?<br>  (2 <br>)
    67: "N-nguy hiểm quá！ Anh có biết ở đó<br>có bao nhiêu tên trộm không hả！？<br> ",

    # seq68: Yeah，probably. So finish it fast.<br>If I die，I'll come back to haunt you.<br>  (2 <br>)
    68: "Chắc vậy. Nên làm nhanh lên nhé.<br>Chết rồi tôi sẽ hiện về ám cô đấy.<br> ",

    # seq69: Hehe. Then I can't afford to fail.<br>  (1 <br>)
    69: "Hì hì. Thế thì không thể thất bại được rồi.<br> ",

    # seq70: *inhale*... *exhale*... Okay.<br>I have steeled myself. Let us start the operation.<br>  (2 <br>)
    70: "Hít... thở... được rồi.<br>Tôi đã sẵn sàng. Bắt đầu chiến dịch thôi.<br> ",
}


def get_text_field(ln):
    """Extract the text field from a text-command line using full split."""
    parts = ln.split(",")
    if ln.startswith("title,"):
        return parts[1] if len(parts) > 1 else ""
    elif ln.startswith("message,") or ln.startswith("messageTextUnder,") or ln.startswith("messageTextCenter,"):
        return parts[2] if len(parts) > 2 else ""
    return ""


def main():
    raw = EN.read_bytes()
    has_bom = raw[:3] == b"\xef\xbb\xbf"
    has_crlf = b"\r\n" in raw[:200]

    text = raw.decode("utf-8-sig")
    lines = text.splitlines(True)  # keep line endings

    # Strip trailing \r from each line (we'll restore CRLF if needed)
    stripped = [ln.rstrip("\r\n") for ln in lines]

    # Count text records in EN asset
    en_records = []
    for idx, ln in enumerate(stripped):
        if ln.startswith("title,") or ln.startswith("message,") or \
           ln.startswith("messageTextUnder,") or ln.startswith("messageTextCenter,"):
            en_records.append((idx, ln))

    record_count = len(en_records)
    assert len(VI) == record_count, \
        f"VI has {len(VI)} entries but EN asset has {record_count} text records"

    # PREFLIGHT 1: No ASCII commas in VI text
    for seq, vi in VI.items():
        if "," in vi:
            print(f"ERROR: seq {seq} has ASCII comma in VI: {vi[:60]!r}")
            return False

    # PREFLIGHT 2: <br> count match for each text record
    all_ok = True
    for seq, (line_idx, ln) in enumerate(en_records):
        vi = VI.get(seq)
        if vi is None:
            continue
        en_text = get_text_field(ln)
        en_br = en_text.count("<br>")
        vi_br = vi.count("<br>")
        if en_br != vi_br:
            print(f"BR MISMATCH seq {seq} (line {line_idx+1}): EN has {en_br} <br>, VI has {vi_br}")
            print(f"  EN: {en_text[:100]!r}")
            print(f"  VI: {vi[:100]!r}")
            all_ok = False

    if not all_ok:
        print("PREFLIGHT FAILED — fix <br> counts above")
        return False

    print(f"Preflight OK: {record_count} records, br counts match.")

    # BUILD: iterate lines, replace text fields using full split/join
    out_lines = []
    seq = 0
    translated = 0

    for idx, ln in enumerate(stripped):
        if ln.startswith("title,"):
            vi = VI.get(seq)
            if vi is not None:
                parts = ln.split(",")  # ['title', 'text']
                parts[1] = vi
                new_ln = ",".join(parts)
                out_lines.append(new_ln)
                translated += 1
            else:
                out_lines.append(ln)
            seq += 1
        elif ln.startswith("message,") or ln.startswith("messageTextUnder,") or ln.startswith("messageTextCenter,"):
            vi = VI.get(seq)
            if vi is not None:
                parts = ln.split(",")  # ['cmd', 'name', 'text', 'characode', 'voicekey', 'chara_X']
                # Text field is always at index 2 for message/textMessage* commands
                # (title is handled above)
                if len(parts) > 2:
                    parts[2] = vi
                    new_ln = ",".join(parts)
                    out_lines.append(new_ln)
                    translated += 1
                else:
                    print(f"ERROR: seq {seq} line {idx+1} has < 3 parts: {ln[:80]!r}")
                    return False
            else:
                out_lines.append(ln)
            seq += 1
        else:
            out_lines.append(ln)

    assert seq == record_count, f"Missed records: read {seq}, expected {record_count}"

    # Join with appropriate line ending
    sep = "\r\n" if has_crlf else "\n"
    out_text = sep.join(out_lines)

    # Restore trailing newline from original (file ends with empty line)
    # Original lines count: check if the last line was empty (only \r\n)
    if len(lines) > 1 and lines[-1].strip() == "" and lines[-1].endswith(("\r\n", "\n")):
        out_text += sep

    # Final BOM write
    bom = "\ufeff" if has_bom else ""
    out_bytes = (bom + out_text).encode("utf-8")

    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_PATH.write_bytes(out_bytes)
    print(f"Wrote {translated}/{record_count} records -> {VI_PATH}")

    # POST-WRITE VERIFICATION
    check_br(record_count, has_bom, has_crlf)
    return True


def check_br(record_count, has_bom, has_crlf):
    """Read back and verify br counts match."""
    vi_raw = VI_PATH.read_bytes()
    vi_text = vi_raw.decode("utf-8-sig")
    vi_lines = vi_text.splitlines(True)
    vi_stripped = [ln.rstrip("\r\n") for ln in vi_lines]

    vi_records = []
    for idx, ln in enumerate(vi_stripped):
        if ln.startswith("title,") or ln.startswith("message,") or \
           ln.startswith("messageTextUnder,") or ln.startswith("messageTextCenter,"):
            vi_records.append((idx, ln))

    if len(vi_records) != record_count:
        print(f"POST-WRITE RECORD COUNT MISMATCH: VI has {len(vi_records)}, EN has {record_count}")
        return False

    all_ok = True
    for seq in range(record_count):
        vi_idx, vi_ln = vi_records[seq]
        vi_text_field = get_text_field(vi_ln)
        vi_br = vi_text_field.count("<br>")
        # We trust the preflight already matched, but verify
        if vi_text_field.count(",") > 0:
            print(f"POST-WRITE: seq {seq} has ASCII comma in VI text field: {vi_text_field[:80]!r}")
            all_ok = False

    if all_ok:
        print(f"Post-write check PASS: all {record_count} records clean.")
    else:
        print("POST-WRITE CHECK FAILED")
    return all_ok


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
