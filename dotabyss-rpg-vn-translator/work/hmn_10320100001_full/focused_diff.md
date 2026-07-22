# Focused Diff — hmn_10320100001 (Bí Mật Đáng Ngờ Của Thợ Mỏ)

Case: EN-asset-is-English (message fields English; title field JP). JP primary via ja.json (identity map) + en.json reverse map; EN asset = structural authority.

99 records translated (1 title + 97 message + 1 messageTextCenter). Sample:

| Line | JP | EN asset | VI |
|---|---|---|---|
| 22 | 採掘家の怪しい秘密 | (title JP) | Bí Mật Đáng Ngờ Của Thợ Mỏ |
| 30 | ふうっ……。今回の探索も順調だな。 | Whew... This expedition's going smoothly. | Phù... Chuyến thám hiểm lần này cũng suôn sẻ ghê. |
| 184 | おい、ダリア！ | Hey, Daria! | Này‚ Daria! |
| 196 | あ、親方……。 | Ah, Boss... | A‚ sếp... |
| 314 | よくやったぞダリア！ | Good work, Daria! | Làm tốt lắm‚ Daria! |
| 389 | 急に胸のあいだに手をつっこむな。 | Don't just shove your hand between your breasts. | Đừng có tự nhiên thọc tay vào giữa ngực như thế. |
| 690 | ――数日後 | —A few days later— | —Vài ngày sau— (messageTextCenter, size=48) |
| 768 | すみません、司令官。 | Sorry, Commander. | Xin lỗi Chỉ Huy. |
| 958 | 司令官自らですか | The Commander himself...! | Đích thân Chỉ Huy đi ạ...! |

## Key decisions
- 司令官/Commander → **Chỉ Huy**; 親方 (Boss) → **sếp** in dialogue.
- Daria (ダリア): self-ref `em`, addresses superiors as `sếp`; speaker label kept `ダリア`.
- Soldiers 兵士Ａ/兵士Ｂ speaker labels kept verbatim; they address Commander as `Chỉ Huy`, self `tôi`.
- SFX localized: Clink→Coong, Clatter→Loảng xoảng, knock→Cốc cốc, click→Cạch, Zzz→Khò, *huff*→Hì hục, *yawn*→Hoááp.
- ASCII commas inside VI text → U+201A ‚ (0 ASCII commas in text fields, verifier confirmed).
- All `<br>` counts matched EN asset exactly; `<size=48>`, voice IDs, chara_X, `<user>` preserved.
