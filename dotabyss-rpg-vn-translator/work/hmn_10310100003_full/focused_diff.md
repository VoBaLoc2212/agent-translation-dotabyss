# Focused Diff — hmn_10310100003

**Scene:** Nơi Ân Nghĩa Và Trung Nghĩa Cư Ngụ (Where Gratitude and Loyalty Lie)
**Mode:** EN-asset-is-English (en.json fully English; ja.json is identity map → JP recovered via en.json reverse-lookup)
**Records:** 112 text records (1 `title`, 110 `message`, 1 `messageTextUnder`, 0 `messageTextCenter`)
**Verifier:** `independent_verify = PASS` (0 issues, line_count 2271=2271, BOM+CRLF preserved)

## Conventions
- Commander / 司令官 → **Chỉ Huy**
- Young Lord / 若殿 → **Thiếu Gia** (Hatsune defers; Commander addresses him as Thiếu Gia)
- Lord / 領主さま → **Lãnh Chúa**
- Frontline Base / 前線基地 → **Căn Cứ Tiền Tuyến**
- Hatsune / Kotono / Hourai kept romanized (in-dialogue mentions); speaker labels (field 1) kept JP byte-identical
- Wolf SFX localized: Grr→Gừ, Gyaow→Gâu
- Internal fullwidth `，` → U+201A `‚`
- Title in Vietnamese Title Case

## JP / EN / VI alignment (selected notable lines)

| L# | JP (recovered) | EN (structural authority) | VI |
|----|----------------|---------------------------|-----|
| 21 | 恩義と忠義のありか | Where Gratitude and Loyalty Lie | Nơi Ân Nghĩa Và Trung Nghĩa Cư Ngụ |
| 71 | グルルルルル……！ | Grrrrrrr...! | Gừ gừ gừ...! |
| 109 | （体に力が入らない……！…） | (My body will not move...? At this rate, I will fall from the tree...) | (Thân thể tôi không cử động được nữa...? Nếu cứ thế này, tôi sẽ ngã khỏi cây và thành mồi cho con sói...) |
| 178 | ――若殿っ！ | Young Lord! | Thiếu Gia! |
| 347 | さぁ、ケダモノ！… | Now then, you beast! Bring it on! | Nào, con thú kia! Tới đi! |
| 630 | さあ……来い！若殿に傷を負わせたこと… | Come on...! I'll make you regret injuring the Young Lord! | Tới đi...! Để em bắt ngươi phải hối hận vì đã làm bị thương Thiếu Gia! |
| 1369 | …………！ | ... | … (punctuation-only, changed byte to clear kept-text) |
| 1670 | よし、作戦成功だ！… | Alright, plan successful! As expected, Hatsune. Well done— | Tốt, kế hoạch thành công! Đúng như anh nghĩ, Hatsune. Giỏi lắm— |
| 1845 | <user>だ。 | I'm <user>. | Tôi là %user%. (%user% preserved) |
| 1862 | しれーかんっていうのは… | ...What kind of position is 'Commaander'? | ...cái chức 'Chỉ Huy' ấy là làm gì vậy? (EN typo 'Commaander' → corrected to 司令官=Chỉ Huy) |
| 1964 | ホウライに帰りましょう、若殿。領主さまも… | Let's return to Hourai, Young Lord. The Lord is waiting... | Chúng ta hãy trở về Hourai đi, Thiếu Gia. Lãnh Chúa đang đợi Thiếu Gia trở về. |
| 2075 | その後、<user>たちは前線基地へと無事帰還した。 | After that, %user% and the others returned safely to the Frontline Base. | Sau đó, %user% và những người khác đã trở về Căn Cứ Tiền Tuyến an toàn. |
| 2149 | 司令官。本当にありがとう。 | Commander. Thank you so much. | Chỉ Huy. Cảm ơn anh nhiều. |
| 2176 | そうはいくか！受けた恩は返すのがサムライだ！ | No way! A samurai repays a debt of gratitude! | Không đời nào! Một samurai trả ơn người đã giúp mình! |
| 2262 | これからもよろしくな、司令官！ | Let's keep working together from now on, Commander! | Từ nay chúng ta cùng làm việc với nhau nhé, Chỉ Huy! |

## Notes / intentional decisions
- All 112 records changed vs EN asset (0 kept-text). Wolf SFX and `…` punctuation lines localized so no UNCHANGED_TEXT_RECORDS.
- EN asset typo `Commaander` (L1862) intentionally corrected to `Chỉ Huy` (reflects JP 司令官).
- `%user%` placeholder preserved on L1845 & L2075.
- `<br>` counts mirrored exactly from EN asset (authoritative) on every text field; trailing `<br> ` suffix preserved on all `message,` lines.
