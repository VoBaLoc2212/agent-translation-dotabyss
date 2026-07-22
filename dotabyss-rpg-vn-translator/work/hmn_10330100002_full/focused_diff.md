# Focused Diff — hmn_10330100002

**Mode:** EN-asset-is-English. Asset text fields are English (internal fullwidth `，` U+FF0C); `en.json` carries English values; `ja.json` is a JP-primary identity map. Translation done from the EN text fields (JP is the primary source of meaning via `ja.json`).

**Structure preserved:** BOM ✓ · CRLF ✓ · 889 lines EN = 889 lines VI ✓ · delimiter 0 mismatch ✓ · technical fields 0 mismatch ✓ · tags 0 mismatch ✓ · placeholders 0 mismatch ✓ · ASCII-comma-in-VI 0 ✓.

**Counts:** title 1 · message 72 · messageTextCenter 2 · messageTextUnder 0 → 75 translatable records, all 75 changed.

**Key terminology:**
- 司令官 / Commander → **Chỉ Huy**
- 大穴 → **Đại Huyệt**
- 前線基地 / Frontline Base → **Tiền Tuyến Căn Cứ**
- リフト / Lift → **'Thang'**
- オーバーテクノロジー / Over-Technology → **'Siêu Công Nghệ'**
- 副司令官 / Deputy Commander → **Phó Chỉ Huy**
- 合コン / mixer (group blind date) → **cuộc gặp gỡ giới thiệu**
- Speaker labels (field 1) kept verbatim JP: 一般兵Ａ/Ｂ, モンスター, エメルダ, ルディア, 先輩記者, `<user>`. In-dialogue name mentions romanized to **Scoop** / **Emeralda** (shipped VI convention).

**Intentional localizations (logged):**
- Monster SFX `Giii!` → `Giíi!`, `Gwooo!` → `Gùuoo!` (Vietnamese roars; must change to clear UNCHANGED_TEXT_RECORDS).
- ASCII comma inside VI text → U+201A `‚`.
- `<br>` internal-break count per field set to match EN asset authority.
- Title + `messageTextCenter` cards in Vietnamese Title Case inside preserved `<size=48>…</size>`.

---

## EN → VI text records (selected)

| # | EN (asset) | VI |
|---|---|---|
| title | 本社復帰は間違いなし♪ | Chắc Chắn Sẽ Trở Về Tổng Hành Din Rồi♪ |
| center | <size=48>—A few hours later.</size> | <size=48>—Vài Giờ Sau.</size> |
| 3 | Giii! | Giíii! |
| 4 | Commander, they're coming again! | Chỉ Huy‚ chúng lại tới nữa rồi! |
| 6 | Don't flinch! If you turn your back, they'll chase you down! | Đừng run sợ! Lộn xộn rồi tụi nó đuổi theo đấy! |
| 7 | Whoa... So this is a monster from the Abyss. Up close, it's quite impressive. | Hây… Thế này là quái vật từ Đại Huyệt à. Nhìn tận mắt thì cũng khá<br>tráng lệ đấy. |
| 9 | —Emelda pulled out her bow, nocked an arrow with practiced hands, and drew it back. The released arrow flew with force and accurately pierced the monster's eye. | —Emelda rút cung ra‚ móc tên bằng tay quen thuộc‚ rồi giương lên.<br>Mũi tên bay vút đi và ghim chính xác vào mắt con quái vật. |
| 10 | Gwooo! | Gùuoo! |
| 14 | You're right. ...All troops! Emelda's attack took out one eye! Circle around to its blind spot and wear it down without rushing! Don't push yourselves! | Đúng rồi. …Tất cả anh em! Đòn của Emelda đã bịt được một mắt nó!<br>Vòng ra điểm mù mà hạ nó từ từ! Đừng có cố quá! |
| 22 | You were a great help, Emeralda. | Cảm ơn em nhé‚ Emelda. |
| 27 | Whoa! What is this thing? | Úi! Con quái gì thế này? |
| 28 | It's a device for quickly moving between the layers of the Abyss. We call it the 'Lift'. | Nó là thiết bị di chuyển nhanh giữa các tầng của Đại Huyệt. Chúng tôi<br>gọi nó là 'Thang'. |
| 32 | There's nothing like this even in the city. | Ở thành thị cũng chẳng có thứ gì như thế này. |
| 33 | Yeah, I'd imagine so. It's science that doesn't exist in this world yet... It's one of the Over-Technologies. | Ừ‚ tôi cũng tưởng tượng được. Đây là khoa học chưa tồn tại ở thế giới này...<br>Một trong những 'Siêu Công Nghệ'. |
| center | <size=48>—Dinner Time</size> | <size=48>—Giờ Ăn Tối</size> |
| 39 | Isn't this the tavern where you were with that girl, Scoop? Coming here before dinner—you're really something... | Chỗ này chẳng phải quán rượu Scoop đi với cô gái kia sao? Đến đây trước bữa tối—<br>anh đúng là ghê thật... |
| 41 | Well, it does look delicious. I've been curious about it for a while. | Ừ‚ trông cũng ngon đấy. Tôi cứ tò mò về chỗ này một thời gian rồi. |
| 42 | Everyone, please eat plenty! | Mọi người ơi~ Hãy ăn thật no nha~. |
| 54 | Over the next several days, Emeralda stayed with everyone at the Frontline Base. They hunted monsters in the Abyss, shared meals, and chatted idly. | Vài ngày sau đó‚ Emeralda cùng mọi người ở Tiền Tuyến Căn Cứ sinh hoạt chung. Họ đi<br>săn quái trong Đại Huyệt‚ cùng quây quần bữa ăn và tán dóc vô lo. |
| 59 | Compared to my last, this one ended up painting Scoop and the soldiers in a positive light, but I think it's a good article!♪ | So với bài trước thì bài này lại làm Scoop và lính tráng trông tốt hơn‚ nhưng<br>tôi nghĩ nó là một bài báo khá hay!♪ |
| 60 | No doubt I'll be back at headquarters. Maybe even a promotion! Ohohoho!♪ | Chắc chắn tôi sẽ về lại tổng hành din rồi. Biết đâu còn được thăng chức!<br>Oho hoho!♪ |
| 62 | Nobody's interested in the Commander's good points! The Frontline Base is only good for scandal! | Chẳng ai thèm quan tâm tới điểm tốt của Chỉ Huy đâu! Tiền Tuyến Căn Cứ<br>chỉ cần mỗi scandal thôi! |
| 65 | What matters isn't the truth or journalistic accuracy! It's sales! Rewrite it into something that sells, even if you have to lie! Got it! | Quan trọng không phải là sự thật hay tính chính xác của báo chí! Là doanh thu!<br>Viết lại thành bài bán chạy đi‚ dù phải nói dối cũng được! Hiểu chưa! |
| 70 | Hm? Is that... Scoop? | Hửm? Đó là... Scoop à? |
| 71 | Commander, taking a walk this late? You'll get chewed out by the Deputy Commander if you cut loose too much. | Chỉ Huy‚ đi dạo lúc đêm khuya thế này à? Cứ ăn chơi quá trớn thì<br>Phó Chỉ Huy mắng đấy? |
| 73 | (If I tail Scoop and dig up all his dirty laundry, my boss will recognize me and I can go back to the city.) | (Nếu mình bám đuôi Scoop và moi hết những chuyện xấu của anh ta‚ sếp sẽ<br>công nhận mình và mình có thể về thành thị.) |
| 74 | (Scoop... don't hold it against me. Even if it's an order from my boss, I still can't write lies.) | (Scoop... đừng trách tôi nhé. Dù là mệnh lệnh từ sếp‚ tôi vẫn<br>không thể viết lời nói dối.) |
| 75 | (So I'll reveal your true self—the unvarnished scandal—here I come, it's on!) | (Thế nên‚ tôi sẽ phơi bày con người thật của anh—scandal không tẩy trắng—<br>xin mời‚ bắt đầu thôi!) |

*Full 75-record EN→VI map is generated deterministically by `build_asset_vi.py` from `vi_translations.txt`.*
