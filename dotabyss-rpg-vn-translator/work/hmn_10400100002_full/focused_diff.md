# Focused Diff — hmn_10400100002 (Luca vs Commander trust scene)

Mode: **EN-asset-is-English, title-still-JP**. ja.json = JP primary; EN asset = structural authority (BOM/CRLF/`<br>`/tags/field order); vi/ = output.

Records: **92** = 1 title (JP→VI) + 91 message (EN→VI). Verifier: **independent_verify PASS** (all checks clean).

Conventions applied (from sibling `hmn_10400100001`): Luca→`Luca`, Commander→`Chỉ Huy`, Alicia→`Alicia`, `Căn Cứ Tiền Tuyến`. EN asset typo `Commaander` (Luca's mangled "Commander") repaired to `Chỉ Huy`. ASCII commas in VI text → `‚` (U+201A). Title in Vietnamese Title Case.

## Translations

| # | JP (ja.json) | EN asset text | VI output |
|---|---|---|---|
| 1 | 次は負けないから！ | (title JP, empty en.json) | title,Lần Sau Sẽ Không Thua Đâu! |
| 2 | ふむ……この辺りなら大規模な防衛戦もできそうだな。… | Hmm... this area could work for a large-scale defense. I should prep a<br>strategy to lure monsters. | Hừm... chỗ này có vẻ ổn để bày một trận phòng ngự quy mô lớn. Phải chuẩn bị<br>một kế hoạch để nhử quái vật. |
| 3 | （ふふふ、しれーかんが考え込んでる。…） | (Fufufu，Commaander's deep in thought. He's definitely off guard now!) | (Hư hư hư‚ Chỉ Huy đang chìm trong suy nghĩ. Giờ anh ấy hoàn toàn mất cảnh giác rồi!) |
| 4 | （前線基地で最強のしれーかんに１度はやられちゃったけど、…） | (I lost to Commaander once at Frontline Base，but I'll be the World's Greatest Martial Artist，so I can't lose again!) | (Lần trước em có thua Chỉ Huy một lần ở Căn Cứ Tiền Tuyến‚ nhưng em sẽ trở thành võ sư số một thế giới‚ nên tuyệt đối không được thua lần nữa!) |
| 5 | 天気もいいし、少し眠くなってきたな……ふわぁ…… | The weather's nice，making me a bit drowsy... Fwaa... | Thời tiết đẹp thế này làm anh hơi buồn ngủ... Phùa... |
| … | (91 message records) | … | … |

Full JP/EN/VI triple aligned in `build_vi.py` (`VI` dict, 92 entries) and the verifier-confirmed output file.

## Structural QA (independent verifier)
- line_count match: 1446 EN == 1446 VI ✓
- BOM match ✓ · CRLF match ✓
- delimiter mismatches: 0 · technical-field mismatches: 0 · tag mismatches: 0 · placeholder mismatches: 0 · ASCII-comma-in-VI-text: 0
- unchanged text records: 0 (all 92 changed)

## Notes
- Title translated from JP key (en.json title value was empty) → Title Case `Lần Sau Sẽ Không Thua Đâu!`.
- `Commaander` → `Chỉ Huy` intentional repair (EN typo / Luca's mispronunciation) logged in manifest `notes`.
- `Frontline Base` → `Căn Cứ Tiền Tuyến` per project term bank.
- Speaker labels (field 1) kept byte-identical JP: `<user>`, `ルカ`, `アリシア`, ``. In-dialogue name mentions romanized (Luca/Alicia/Chỉ Huy).
- No H18 content in this scene; playful tickle/tease banter kept at source tone (Luca `em`/anh ↔ Commander `anh`/em; Alicia polite `tôi`/`ngài`).
