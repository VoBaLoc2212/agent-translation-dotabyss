# Focused Diff: hmn_10480100002 — Tất Cả Là Tại Chỉ Huy!!

## Scene Overview
Celeste (a lazy guard) and the Commander investigate a market robbery. Celeste complains about low pay, the Commander offers a bounty to motivate her, and they use info brokers to track the robber.

## Text Commands
- `title`: 1
- `message`: 89
- `messageTextUnder`: 2
- **Total**: 92

## Terminology Bank

| JP (ja.json) | EN (asset) | VI |
|---|---|---|
| 司令官 | Commander | Chỉ Huy |
| 前線基地 | Frontline Base | Căn Cứ Tiền Tuyến |
| ミレスガルド | Milesgard | Milesgard |
| 警備隊 | patrol squad | đội tuần tra |
| 衛兵隊 | Guard Corps | Đội Vệ Binh |
| 隊長 | Captain | Đội trưởng |
| ルディア | Ludia | Ludia |
| 情報屋 | info brokers | bán tin |
| 懸賞金 | bounty | tiền thưởng |

## Character Voice Notes

**Celeste (セレスト)**: Lazy, money-motivated guard. Uses casual tone:
- Self-reference: `あたし` → `tôi`
- To Commander: `あんた` → `anh` (casual, not deferential)
- Tone: sarcastic, whiny when complaining, gleeful about money

**Commander**: Male, uses `ore`/`omae`:
- To Celeste: `cô` with casual/dominant tone
- Self: `tôi`
- Offers bounty, pragmatic

## Key Translation Decisions

1. **Title**: 「ぜーんぶ、司令官のせいよ！！」→ `Tất Cả Là Tại Chỉ Huy!!` (Title Case)
2. **"It's all that stingy Commander's fault!"** → `Tất cả là tại cái tên Chỉ Huy keo kiệt đó!` (Celeste's casual blame)
3. **"Frontline Base really is easygoing"** → `Căn Cứ Tiền Tuyến đúng là thoải mái thật`
4. **"yaaawn..."** → `*ngáp*...` (localized SFX)
5. **"*sigh*..."** → `*thở dài*...` (localized SFX)
6. **"Info brokers. The underground kind."** → `Bán tin đấy. Hàng chợ đen ấy.` (natural VI underworld terminology)
7. **"Those clergy assholes"** → `mấy thằng cha đạo đức chết tiệt` (preserving Celeste's irreverent tone)
8. **messageTextUnder** fields translated directly with %user% preserved

## BR Count Preservation
EN asset `<br>` counts treated as authoritative. Adjustments made to match:
- Seq 19: Added internal `<br>` (EN: 3, VI initially 2)
- Seq 23: Collapsed to 1 `<br>` (EN: 1, VI initially 2)
- Seq 55: Added internal `<br>` (EN: 2, VI initially 1)
- Seq 59: Added internal `<br>` (EN: 2, VI initially 1)
- Seq 86: Added internal `<br>` (EN: 2, VI initially 1)

## Alignment Notes
- `en.json` has English values (EN-asset-is-English case)
- `ja.json` is the JP source (identity map for this scene)
- Title field in EN asset is still JP → translated directly from JP
