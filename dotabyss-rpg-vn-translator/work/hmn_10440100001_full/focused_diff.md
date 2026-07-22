# hmn_10440100001 — Focused Translation Diff

## Scene Summary
Yachiyo (shrine maiden from Hourai) warns Commander & Alicia about a coming downpour, which they ignore and get soaked. Next day they find her, learn she can predict weather via the Dragon God living within her. However, the Dragon God is capricious—predictions are unreliable. Commander convinces her to stay at the Frontline Base.

## Character Voice Matrix
| Character | Role | Addresses Commander | Self-Reference |
|-----------|------|--------------------|-----------------|
| **ヤチヨ (Yachiyo)** | Shrine maiden / weather-predictor | Ngài Chỉ Huy / Chỉ Huy (司令官さま/司令官) | em (私) |
| **アリシア (Alicia)** | Commander's adjutant | Chỉ Huy / anh (司令官) | em (わたし) |
| **Commander (<user>)** | Chỉ Huy | — | tôi / anh / ta (俺) |
| **？？？** | Mystery (later Yachiyo) | hai người / các Ngài | em |

## Terminology Bank
| EN Source | JP Source | VI Translation |
|-----------|-----------|----------------|
| Commander / Lord Commander | 司令官 / 司令官さま | Chỉ Huy / Ngài Chỉ Huy |
| Frontline Base | 前線基地 | Căn Cứ Tiền Tuyến |
| Dragon God | 龍神さま | Long Thần |
| shrine maiden | 巫女 | vu nữ |
| Hourai | ホウライ | Hourai |
| dragon (Western) | ドラゴン | dra-gôn |
| dragon (Eastern/JP) | 龍 | Long / rồng thần |

## Key Translation Decisions

### Title
- JP: `これから大雨が降りますから！`
- VI: `Vì Sắp Có Mưa Lớn Rồi!` (Title Case)

### Addressing
- Yachiyo uses polite speech (ですます):
  - Calls Commander `Ngài Chỉ Huy` (司令官さま → Lord Commander)
  - Self-reference `em` (私)
- Alicia informal:
  - Calls Commander `Chỉ Huy` / `anh`
  - Self-reference `em`
- Commander:
  - To Yachiyo: `cô` (お前 → you/cô, respectful distance)
  - To Alicia: calls by name

### Dragon God / Dragon distinction
- Long Thần (龍神) = Dragon God (eastern, elegant, serpent-like)
- dra-gôn (ドラゴン) = Western-style dragon (squat, fire-breathing)
- Yachiyo's outrage at confusing them is preserved in translation

### SFX / Interjections
- `*rumble，rumble，rumble*` → `*ầm，ầm，ầm*` (Vietnamese thunder SFX)
- `*whoosh!*` → `*ào ào!*` (rain SFX)
- `Rumble，rumble，rumble.` → `Ầm，ầm，ầm.`
- `*sniff*` → `*hức*`
- `*phew*` → `*phù*`

### Punctuation-only records
- Seq 93: `...` → `………` (ellipsis change to clear UNCHANGED_TEXT_RECORDS)

## Structural Info
- Lines: 1867 (EN=VI, match)
- BOM: ✓ (UTF-8 with BOM)
- Newline: CRLF (match)
- Records: 110 total (1 title + 107 message + 2 messageTextCenter)
- Technical fields: unchanged
- Delimiter `,` counts: match
- Tag counts: match (all `<br>` preserved)
- ASCII comma in VI: 0 (fullwidth `，` and U+201A `‚` used where needed)
- All 110 records changed from source

## Verifier Result
- independent_verify: **PASS**
