# Focused Diff — hmn_10290100001 (JP/EN → VI)

Case: **EN-asset-is-English** (en.json has English values; title field still JP `美味しそうに食べてくれてるよ`; `message,` text fields are English). Translated from JP (`ja.json`) via aligned EN text fields, then substituted the English text field. Title translated to Vietnamese Title Case.

## Title
- EN: `美味しそうに食べてくれてるよ`
- VI: `title,Trông Cậu Ăn Ngon Lắm`

## Sample text-field substitutions (field 1 = speaker label, kept verbatim)
| Line | Speaker | VI text field |
|------|---------|---------------|
| 27 | `<user>` | `Ưm‚ kế tiếp làm sao đây... Dù có nghĩ mãi<br>mà não vẫn không chịu vận hành!<br> ` |
| 66 | `アリシア` | `Chỉ Huy! Em đã chuẩn bị trà và bánh ngọt rồi. Nghỉ giải lao một chút<br>nhé?<br> ` |
| 108 | `アリシア` | `Của em đây! Đây là bánh tart trái cây đặc biệt do Myrtille mang tới làm quà đấy!<br> ` |
| 242 | `ミルティーユ` | `Làm phiền! Chào Alicia‚ Chỉ Huy!<br> ` |
| 519 | `<user>` | `Ừ‚ với tư cách Chỉ Huy anh không thể làm ngơ.<br>Lên hiện trường thôi!<br> ` |
| 765 | `ミルティーユ` | `Anh Gấu ơi‚ là gì nhỉ?<br> ` |
| 836 | `ミルティーユ` | `Ể! Vậy thủ phạm là Anh Gấu à?<br> ` |
| 1107 | `<user>` | `(Myrtille đưa đồ ăn đó như thể cảm nhận được anh đang rối.<br>Cô ấy đang cố cứu người bằng đồ ngọt của mình‚ phải không?)<br> ` |
| 1228 | `ミルティーユ` | `Cảm ơn cậu~ Chỉ Huy!<br>Giờ em có thể bảo mọi người ở ký túc đừng lo!<br> ` |

## Structural notes
- 100 text records (1 title + 99 message), all translated.
- Every `message,` trailing suffix `<br> ` preserved; 43 lines had an internal `<br>` (2 total per source) and were mirrored exactly.
- ASCII commas inside VI text → `‚` (U+201A) — 0 ASCII commas in output.
- `%user%` placeholder preserved on lines 139, 660.
- Speaker labels (field 1) kept byte-identical JP: `アリシア`, `ミルティーユ`, `子熊`, `<user>`.
- Bear-cub SFX localized: `*grr*`→`*gừ*`, `Ruff`→`Gâu`, `Grr`→`Gừ`; `Mr. Bear`→`Anh Gấu`; `Myrtille` romanized in dialogue (matches shipped VI), self-name `Mil` kept; `Sweets Kingdom`→`Vương Quốc Đồ Ngọt`, `Lux Nova` kept.
- No H18 content in this scene; all characters 18+ confirmed per project rule.
- BOM + CRLF + delimiter + line count (1328) preserved (verifier `independent_verify: PASS`).
