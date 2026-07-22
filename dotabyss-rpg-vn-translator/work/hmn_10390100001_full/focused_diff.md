# Focused Diff — hmn_10390100001 (JP → VI)

**Source case:** EN-asset-is-English (title field still JP; all `message`/`messageTextCenter` fields English; `en.json` maps JP→EN). `ja.json` treated as JP primary; EN asset as structural authority.

**Text records:** 82 total = 1 title (JP→VI) + 79 message + 2 messageTextCenter.

## Title
- JP/EN: `神の教えで救済したいのです` → EN asset title field still JP
- VI: `Mong Cứu Rỗi Bằng Giáo Lý Của Chúa` (Vietnamese Title Case)

## messageTextCenter (2)
- EN: `<size=48>——A few minutes later——</size>`
- VI: `<size=48>——Vài Phút Sau——</size>` (Title Case, no comma)

## Representative message lines (EN → VI)
- L33 `<user>` "Geez... How infuriating!" → "Chà... Thật bực mình!"
- L44 アリシア "A-are you still so upset?" → "C-chẳng lẽ ngài vẫn còn bực tức sao ạ?"
- L182 `<user>` "What?" → "Cái gì?"
- L248 マーガレット "My name is Margaret. I am just a humble clergywoman..." → "Tôi tên là Margaret. Chỉ là một nữ tu khiêm tốn..."
- L516 マーガレット "Oh my. So you're the Lord Commander of this base." → "Ồ. Thế ra ngài là Chỉ Huy của căn cứ này sao."
- L826 `<user>` "..." → "…" (ellipsis char, clears unchanged-text)
- L1514 `<user>` "(...She really is a picture-perfect clergywoman...)" → "(...Cô ấy đúng là một nữ tu hoàn hảo...)"

## Conventions applied
- Commander / 司令官 → **Chỉ Huy**; 司令官様 (Lord Commander) → **Chỉ Huy** (Margaret uses polite `ngài Chỉ Huy` / `thưa Chỉ Huy`).
- Alicia / Margaret speaker labels kept verbatim (field 1).
- clergywoman → **nữ tu**; Frontline Base → **Căn Cứ Tiền Tuyến**; Milesgard / Perdion kept.
- ASCII comma inside VI text → U+201A (‚); `(`, `)`, `*`, `'` retained as source.
- All `<br>` counts, technical fields (voice id, chara keys), BOM, CRLF preserved.

## QA result
Independent verifier: **PASS** (0 issues; 82/82 records translated; line/delimiter/field/tag/placeholder/BOM/newline all match).
