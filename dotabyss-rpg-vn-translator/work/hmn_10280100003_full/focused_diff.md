# Focused Diff — hmn_10280100003 (Lời Thề Hội Ngộ Giữa Tiếng Sóng)

**Case:** EN-asset-is-English — `en.json` holds English values; the EN asset text fields are English.
JP (`ja.json`) is the meaning primary; the EN asset is the **structural authority** (BOM/CRLF/delimiter/`<br>` count).
All 89 text records were translated JP/EN → Vietnamese via field-index replacement, preserving every byte
of structure.

**Independent verification:** `PASS` (verifier `work/verify_asset_translation.py`).
- `translatable_records` = 89, `translated_records` = 89, `kept_text_lines` = [].
- `line_count` EN 939 = VI 939; `bom_match` = true; `newline_match` = true.
- `delimiter_mismatch_count` = 0, `technical_field_mismatch_count` = 0, `tag_mismatch_count` = 0,
  `placeholder_mismatch_count` = 0, `ascii_comma_in_vi_text_count` = 0.

**Rules applied**
- 司令官 / Commander → **Chỉ Huy** (all occurrences).
- Title → Vietnamese Title Case: `A Promise by the Sound of Waves` → `Lời Thề Hội Ngộ Giữa Tiếng Sóng`.
- ASCII commas inside VI text fields → `‚` (U+201A).
- Speaker labels kept verbatim: `ルディア`, `エミリー`, `女店長`, `<user>`; chara/move/voice keys untouched.
- BOM + CRLF + trailing `<br> ` suffix + exact `<br>` counts copied from EN asset.

**Selected before/after (text field only)**

| Ln | EN (source) | VI (output) |
|----|-------------|-------------|
| 20 (title) | A Promise by the Sound of Waves | Lời Thề Hội Ngộ Giữa Tiếng Sóng |
| 28 | The battered stall we spotted at the Market belonged to the owner of\<br>the shop where Emily used to work.\<br> | Sạp hàng rách nát chúng ta bắt gặp ở Chợ chính là của chủ cửa hàng\<br>nơi Emily từng làm việc.\<br> |
| 70 | Now then‚ former shop owner... I've heard from Emily that you left\<br>your shop in Eldorana one day in pursuit of treasure.\<br> | Giờ thì‚ cựu chủ tiệm… tôi nghe Emily kể rằng vì đuổi theo kho báu mà một ngày nọ anh đã rời bỏ\<br>cửa hàng ở Eldorana đi mất…\<br> |
| 117 | Boss... I was so worried‚ geez! Why didn't you say anything before\<br>you left?\<br> | Sếp ơi… em lo lắng lắm đấy‚ trời ạ!\<br>Sao lúc ra đi anh chẳng nói năng gì với em vậy!\<br> |
| 415 | About the future‚ I have a proposal.\<br> | Về chuyện tương lai‚ tôi có một đề xuất.\<br> |
| 426 | Huh? Commander?\<br> | Hả? Chỉ Huy?\<br> |
| 505 | Don't get me wrong. This isn't for you. It's for Emily. Go back to\<br>Eldorana and use this to rebuild your shop.\<br> | Đừng có hiểu lầm. Không phải cho cô đâu. Là cho Emily đấy. Hãy về\<br>Eldorana và dùng thứ này để tái thiết tiệm.\<br> |
| 857 | Huh? T-That's amazing‚ Commander! How did you know that?!\<br> | Hả… t‚ tuyệt quá‚ Chỉ Huy! Sao ngài lại biết được vậy!?\<br> |
| 904 | But for me... the one I want to make the happiest of all... is you‚\<br>Commaander!♪\<br> | Nhưng với em… người em muốn làm vui nhất… chính là ngài‚\<br>Chỉ Huy!♪\<br> |
| 930 | From now on‚ I'll do my very best to make you smile a lot‚\<br>Commaander!♪\<br> | Từ nay về sau‚ em sẽ nỗ lực hết mình để làm ngài thật nhiều nụ cười‚\<br>Chỉ Huy!♪\<br> |

**Points / notes**
- No H18 content in this scene. All characters confirmed 18+ per project rule; no adult-content line needed handling.
- `女店長` (former female shop owner) is kept as a JP speaker label (field 1); inside dialogue she is addressed
  by Emily as "sếp/anh" and refers to herself as "em" / to Commander as "ngài".
- `Ludia` romanized in dialogue (matches shipped VI convention); `Emily`, `Eldorana` kept as proper names.
- No intentionally-kept-English text records; all 89 changed.
