# hmn_10470100001 — Merem Fortune-Teller Scene
## Focused Translation Diff (JP → VI via EN asset)

**Detection:** EN-asset-is-English with `title,` still JP  
**Records:** 1 title + 79 message = **80 total** (all translated)  
**Verifier:** `independent_verify: PASS`

### Title
| JP (ja.json) | VI |
|---|---|
| ようこそ、メレムの占い館へ | **Chào Mừng Đến Tiệm Bói Toán Của Merem** |

### Key Terminology
| EN Asset | JP (ja.json) | VI |
|---|---|---|
| Commander / 司令官 | 司令官 | **Chỉ Huy** |
| Abyss | 大穴 | **Đại Huyệt** |
| scrying basin | 水盆 | **bát thủy chiếu / bát nước thủy chiếu** |
| Dark Star | 昏き星 | **Ngôi Sao Tối** |
| House of Divination | 占い館 | **Tiệm Bói Toán** |
| grimoire | 魔導書 | **ma đạo thư** |
| compatibility | 相性 | **chỉ số hòa hợp** |
| fortune / divination | 占い | **bói toán** |
| calamity / disaster | 災い / 災厄 | **tai ương** |

### Character Voice & Addressing

**Merem (メレム)** — fortune teller
- Self-reference: tôi
- Addresses Commander: anh / Chỉ Huy / Ngôi Sao Tối
- Voice: polite professional, mystical when performing readings

**Alicia (アリシア)** — secretary/companion
- Self-reference: em
- Addresses Commander: Chỉ Huy / anh
- Voice: energetic, supportive, playful

**Commander / Chỉ Huy**
- Self-reference: anh / tôi (俺)
- Addresses Alicia: em
- Addresses Merem: chị (respectful toward professional)

### Selected Translation Examples

| Seq | EN Asset | JP Source | VI |
|---|---|---|---|
| 2 | Commander, here are the new documents on the Abyss! I'll just leave them here for you! | 司令官、大穴の新しい資料です。こちらに置いておきますね～。 | **Chỉ Huy，đây là tài liệu mới về Đại Huyệt! Em để ở đây cho anh nhé～.** |
| 9 | Hoh, an accurate fortune teller, huh? That's got me curious. Should I get my love or war fortune?... No, I want my money fortune! | ほう、よく当たる占い師、か。そりゃ気になるな。恋愛運か、それとも武運……いや、金運を占ってもらいたいな！ | **Hô，thầy bói linh à? Nghe tò mò đấy. Nên xem vận tình yêu hay vận chiến trận nhỉ?... Không，anh muốn xem vận tài lộc!** |
| 22 | Understood. Then, shall we use the cards this time?
O cards, teach the past, show the present, and paint the future— | かしこまりました。では、今回はカードを使いましょうか。
カードよ、過去を教え、現在を示し、未来を描け―― | **Đã hiểu. Vậy，lần này dùng bài tarot nhé?
Hỡi những lá bài，hãy dạy về quá khứ，chỉ ra hiện tại，vẽ nên tương lai——** |
| 42 | This is... a star? Not a brilliant star that illuminates the world. It's a Dark Star that devours even light itself... | これは、星……？眩く世界を照らす輝かしい星ではない。光をも呑み込むような、昏き星…… | **Đây là... một ngôi sao? Không phải ngôi sao sáng rực chiếu rọi thế giới. Là một Ngôi Sao Tối nuốt chửng cả ánh sáng...** |
| 72 | Yes, near you... a place close to danger. This must be the Abyss. | ええ、あなたの近く……危険とも近い場所。これは大穴でしょうね。 | **Vâng，gần anh... một nơi gần với nguy hiểm. Chắc hẳn là Đại Huyệt.** |
| 77 | Wh-What! You can't go alone, Commander! | え、えええっ！？ダメですよ、司令官お１人でなんてっ！ | **C-Cái gì! Anh không thể đi một mình được，Chỉ Huy!** |

### Structural QA
| Check | Result |
|---|---|
| Line count match (EN=VI) | ✅ 1334 = 1334 |
| BOM match | ✅ Both have BOM (EF BB BF) |
| Newline style | ✅ LF (both) |
| Text records translated | ✅ 80/80 (100%) |
| Tag mismatches | ✅ 0 |
| Delimiter mismatches | ✅ 0 |
| Placeholder mismatches | ✅ 0 |
| ASCII comma in VI text | ✅ 0 |
| Kept English text lines | ✅ 0 (empty) |

### Notes
- Built via field-index generator (split by `,` max 5 parts) preserving trailing voice key and chara fields
- Fullwidth comma `，` (U+FF0C) used in VI text fields, matching EN asset convention
- `<br>` tag counts preserved exactly per EN asset authority
- Title translated with Vietnamese Title Case capitalization
- All 80 records verified as changed (0 kept English lines)
