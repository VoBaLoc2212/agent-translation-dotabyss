#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Field-index VI builder for hmn_10250100001 (EN-asset-is-English case).
Mirrors trailing tag suffix automatically (every message field ends with "<br> ").
Translations derived from ja.json (JP primary) + en.json/en-asset alignment.
All persona: Wendy/Verisa/Veera = em (female); Worker (male citizen) = anh.
Commander -> Chit Huy (Chỉ Huy). Names romanized: Wendy, Veera, Verisa, Perdion.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10250100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# Ordered VI text fields, 1:1 with source text records (title first, then messages).
TRANSLATIONS = [
    # 0 title
    "N\u01a1i L\u00e0m Vi\u1ec7c M\u1edbi C\u1ee7a Wendy",
    # 1 Wendy
    "M\u1ecdi ng\u01b0\u1eddi \u01a1i! Em n\u00ean \u0111\u1eb7t kh\u1ed1i qu\u1eb7ng n\u00e0y \u1edf \u0111\u00e2u \u0111\u00e2y?",
    # 2 Worker
    "\u00c0\u201a \u0111\u1ec3 n\u00f3 v\u00e0o c\u00e1i r\u1ed5 b\u00ean \u0111\u00f3 \u0111i.",
    # 3 Wendy
    "R\u00f5 r\u1ed3i! D\u00f4 ta\u201a d\u00f4 ta\u2026\u2026",
    # 4 Worker
    "Xin l\u1ed7i ph\u1ea3i b\u1eaft em l\u00e0m v\u1eady. N\u1eb7ng kh\u00f4ng \u0111\u1ea5y?",
    # 5 Wendy
    "Ho\u00e0n to\u00e0n kh\u00f4ng sao! V\u00ec em l\u00e0 m\u1ed9t \u00f4-t\u00f4-m\u00e1t m\u00e0!",
    # 6 Worker
    "\u0110\u00fang v\u1eady. V\u00ec em tr\u00f4ng nh\u01b0 m\u1ed9t c\u00f4 g\u00e1i b\u00ecnh th\u01b0\u1eddng n\u00ean anh c\u1ee9 qu\u00ean m\u1ea5t.",
    # 7 Worker (2 br)
    "T\u1eeb khi Wendy \u01a1i \u0111\u1ebfn C\u0103n C\u1ee9 Ti\u1ec1n Tuy\u1ebfn n\u00e0y<br>m\u1ecdi vi\u1ec7c \u0111\u00e3 nh\u1eb9 nh\u00f5m h\u01a1n nhi\u1ec1u.",
    # 8 Wendy
    "E h\u00e8 h\u00e8\u2026\u2026",
    # 9 Wendy (2 br)
    "Nh\u01b0ng em ch\u1eb3ng l\u00e0m \u0111\u01b0\u1ee3c g\u00ec gh\u00ea g\u1edbm \u0111\u00e2u.<br>Em ch\u1ec9 \u0111ang ho\u00e0n th\u00e0nh nh\u1eefng c\u00f4ng vi\u1ec7c \u0111\u01b0\u1ee3c giao ph\u00f3 th\u00f4i!",
    # 10 Wendy
    "T\u1ea5t c\u1ea3 c\u0169ng l\u00e0 nh\u1edd Ch\u1ec9 Huy \u0111\u00e3 gi\u1edbi thi\u1ec7u c\u00f4ng vi\u1ec7c n\u00e0y cho em.",
    # 11 Wendy (2 br)
    "V\u1edbi l\u1ea1i\u2026\u2026 m\u1ecdi ng\u01b0\u1eddi c\u0169ng \u0111\u1ed1i x\u1eed t\u1ed1t v\u1edbi em\u2026\u2026<br>em th\u1ef1c s\u1ef1 tr\u00e0n \u0111\u1ea7y l\u00f2ng bi\u1ebft \u01a1n!",
    # 12 Wendy (2 br)
    "\u1ede nh\u1eefng n\u01a1i kh\u00e1c<br>v\u00ec l\u00e0 \u00f4-t\u00f4-m\u00e1t n\u00ean em lu\u00f4n th\u1ea5y l\u1ea1c l\u00f5ng \u1edf ch\u1ed7 l\u00e0m.",
    # 13 Worker
    "Tr\u01b0\u1edbc khi \u0111\u1ebfn \u0111\u00e2y em \u0111\u00e3 l\u00e0m g\u00ec th\u1ebf?",
    # 14 Wendy (2 br)
    "Cha b\u1ea3o em \u0111i ng\u1eafm nh\u00ecn th\u1ebf gi\u1edbi\u201a n\u00ean em \u0111\u00e3 \u0111i du l\u1ecbch<br>kh\u1eafp c\u00e1c n\u01a1i!",
    # 15 Wendy (2 br)
    "Nh\u01b0ng d\u1ecdc \u0111\u01b0\u1eddng em h\u1ebft s\u1ea1ch ti\u1ec1n\u2026\u2026<br>l\u1ea1i c\u00f2n su\u00fdt b\u1ecb b\u1eaft l\u00e0m n\u00f4 l\u1ec7\u2026\u2026",
    # 16 Worker
    "\u00d4i\u201a tr\u1eddi \u01a1i\u2026\u2026",
    # 17 Wendy
    "Ch\u00ednh l\u00fac \u0111\u00f3 Ch\u1ec9 Huy \u0111\u00e3 c\u1ee9u em!",
    # 18 Worker
    "Wendy \u01a1i\u201a em \u0111\u00e3 tr\u1ea3i qua nhi\u1ec1u gian kh\u1ed5 r\u1ed3i \u0111\u00fang kh\u00f4ng\u2026\u2026",
    # 19 Wendy
    "Nh\u01b0ng \u1edf C\u0103n C\u1ee9 Ti\u1ec1n Tuy\u1ebfn n\u00e0y th\u00ec ch\u1eb3ng c\u00f3 chuy\u1ec7n \u0111\u00f3!",
    # 20 Wendy (2 br)
    "C\u00f3 ng\u01b0\u1eddi t\u1eeb \u0111\u1ee7 m\u1ecdi xu\u1ea5t th\u00e2n n\u00ean ngay c\u1ea3 \u00f4-t\u00f4-m\u00e1t nh\u01b0 em<br>c\u0169ng c\u00f3 th\u1ec3 h\u00f2a nh\u1eadp \u0111\u01b0\u1ee3c!",
    # 21 Wendy (2 br)
    "Em c\u0169ng mu\u1ed1n ti\u1ebfp t\u1ee5c chuy\u1ebfn du l\u1ecbch\u201a nh\u01b0ng m\u00e0 l\u00e0m vi\u1ec7c \u1edf \u0111\u00e2y m\u00e3i<br>c\u0169ng ch\u1eb3ng t\u1ec7 \u0111\u00e2u!",
    # 22 Worker
    "Wendy \u01a1i\u2026\u2026!",
    # 23 Worker
    "\u0110\u01b0\u1ee3c r\u1ed3i! V\u00ec n\u1ee5 c\u01b0\u1eddi c\u1ee7a Wendy\u201a anh s\u1ebd n\u1ed7 l\u1ef1c l\u00e0m vi\u1ec7c h\u1ebft s\u1ee9c!",
    # 24 Wendy
    "V\u00e2ng! Em c\u0169ng s\u1ebd c\u1ed1 g\u1eafng h\u1ebft s\u1ee9c!",
    # 25 Verisa (2 br)
    "Haa\u2026\u2026 cu\u1ed1i c\u00f9ng c\u0169ng t\u1edbi n\u01a1i r\u1ed3i. N\u00e0y\u201a Veera.\u1ed5n ch\u1ee9?",
    # 26 Veera (2 br)
    "Theo l\u1eddi Ch\u1ec9 Huy k\u1ec3 th\u00ec \u1edf c\u00e1c \u0111\u01b0\u1eddng h\u1ea7m quanh \u0111\u00e2y<br>c\u00f3 m\u1ed9t ng\u01b0\u1eddi d\u1eabn \u0111\u01b0\u1eddng \u0111\u1ea5y.",
    # 27 Verisa
    "\u1edc. Kh\u00f4ng bi\u1ebft c\u00f4 \u1ea5y l\u00e0 ng\u01b0\u1eddi nh\u01b0 th\u1ebf n\u00e0o nh\u1ec9?",
    # 28 Wendy
    "H\u1eed? C\u00e1c v\u1ecb l\u00e0 kh\u00e1ch sao?",
    # 29 Wendy
    "Xin ch\u00e0o\u2014\u2661",
    # 30 Wendy
    "Xin l\u1ed7i v\u00ec \u0111\u00e3 \u0111\u1ed9t ng\u1ed9t gh\u00e9 th\u0103m.",
    # 31 Verisa
    "C\u00f4 b\u00e9 kia\u201a ch\u1eebng tu\u1ed5i em \u0111\u00fang kh\u00f4ng?",
    # 32 Verisa (2 br)
    "\u01afm\u2026\u2026 x\u00e9t v\u1ec1 b\u1ec1 ngo\u00e0i th\u00ec c\u00f3 l\u1ebd v\u1eady\u2026\u2026?<br>Nh\u01b0ng tr\u00f4ng c\u00f4 \u1ea5y kh\u00f4ng gi\u1ed1ng m\u1ed9t c\u00f4 g\u00e1i b\u00ecnh th\u01b0\u1eddng\u2026\u2026",
    # 33 Wendy
    "Xin l\u1ed7i\u201a c\u00f4 c\u00f3 ph\u1ea3i l\u00e0 Wendy kh\u00f4ng?",
    # 34 Wendy
    "V\u00e2ng! C\u00f2n hai v\u1ecb l\u00e0 ai th\u1ebf?",
    # 35 Veera
    "Em l\u00e0 Veera. Nh\u01b0 c\u00f4 th\u1ea5y \u0111\u1ea5y\u201a em l\u00e0 m\u1ed9t ph\u00e1p s\u01b0 t\u1eeb Perdion.",
    # 36 Veera
    "V\u00e0 \u0111\u00e2y l\u00e0 ch\u1ecb g\u00e1i c\u1ee7a em\u201a Verisa.",
    # 37 Verisa
    "Cứ g\u1ecdi em l\u00e0 Verisa nh\u00e9!\u2661",
    # 38 Wendy (2 br)
    "R\u1ea5t h\u00e2n h\u1ea1nh \u0111\u01b0\u1ee3c l\u00e0m quen\u201a Verisa\u201a Veera. \u01afm\u201a v\u1eady hai v\u1ecb t\u1edbi \u0111\u00e2y<br>t\u1eeb Perdion \u0111\u1ec3 l\u00e0m g\u00ec v\u1eady?",
    # 39 Veera
    "Th\u1ef1c ra ch\u00fang em \u0111ang t\u00ecm m\u1ed9t lo\u1ea1i qu\u1eb7ng n\u00e0o \u0111\u00f3.",
    # 40 Wendy
    "Qu\u1eb7ng \u00e1?",
    # 41 Verisa (2 br)
    "L\u00e0 lo\u1ea1i qu\u1eb7ng em c\u1ea7n cho th\u00ed nghi\u1ec7m ma ph\u00e1p c\u1ee7a m\u00ecnh. M\u1ed9t th\u1ee9 hi\u1ebfm<br>h\u1ee3p r\u1ea5t t\u1ed1t v\u1edbi l\u1eeda \u0111\u1ea5y.",
    # 42 Veera
    "Nh\u01b0 ch\u1ecb n\u00f3i\u201a lo\u1ea1i qu\u1eb7ng \u0111\u00f3 r\u1ea5t hi\u1ebfm v\u00e0 kh\u00f4ng b\u00e1n \u1edf ch\u1ee3.",
    # 43 Verisa (2 br)
    "Th\u1ebf l\u00e0 b\u1ecdn em c\u00f3 h\u1ecfi \u00fd Ch\u1ec9 Huy\u201a v\u00e0 ng\u00e0i b\u00e1o c\u00f3 th\u1ec3 t\u00ecm \u0111\u01b0\u1ee3c<br>\u1edf \u0110\u1ea1i Huy\u1ec7t\u2026\u2026",
    # 44 Veera (2 br)
    "Ch\u1ec9 Huy \u0111\u00e3 truy\u1ec1n l\u1ec7nh cho b\u1ecdn em nh\u1edd m\u1ed9t ng\u01b0\u1eddi t\u00ean Wendy<br>d\u1eabn \u0111\u01b0\u1eddng t\u1edbi m\u1ecf qu\u1eb7ng.",
    # 45 Wendy
    "Ch\u1ec9 Huy \u0111\u00e3 giao c\u00f4ng vi\u1ec7c n\u00e0y cho em sao!?",
    # 46 Wendy
    "H\u01b0 h\u01b0\u2026\u2026 e h\u00e8 h\u00e8\u2026\u2026 \u00e1\u201a \u00e1 kh\u1ee5m!",
    # 47 Wendy
    "\u0110\u00e3 th\u1ebf th\u00ec \u0111\u1ec3 em d\u1eabn \u0111\u01b0\u1eddng cho hai v\u1ecb!",
    # 48 Veera
    "C\u1ea3m \u01a1n em.",
    # 49 Verisa
    "Wendy \u01a1i\u201a em tr\u00f4ng \u0111\u00e1ng tin c\u1eady \u0111\u1ea5y!\u2661 H\u00f4m nay nh\u1eddi em nh\u00e9!\u2661",
    # 50 Verisa
    "Em kh\u00f4ng m\u1ea1nh \u0111\u1ebfn th\u1ebf \u0111\u00e2u\u201a n\u00ean n\u1ebfu \u0111\u01b0\u1ee3c Wendy che ch\u1edf th\u00ec em s\u1ebd vui l\u1eafm nh\u00e9\u2014?",
    # 51 Wendy
    "Ra l\u00e0 v\u1eady! C\u1ee9 y\u00ean t\u00e2m!",
    # 52 Wendy (2 br)
    "\u0110\u00e2y l\u00e0 c\u00f4ng vi\u1ec7c quan tr\u1ecdng t\u1eeb Ch\u1ec9 Huy. Em s\u1ebd ho\u00e0n th\u00e0nh tr\u1ecdn v\u1eb9n<br>cho m\u00e0 xem!",
    # 53 Verisa
    "Tuy\u1ec7t qu\u00e1! C\u1ea3m \u01a1n em! Em y\u00eau Wendy \u01a1i!\u2661",
    # 54 Wendy
    "E h\u00e8 h\u00e8 h\u00e8\u2026\u2026\u266a",
    # 55 Veera
    "Haa\u2026\u2026 ch\u1ecb \u01a1i\u201a ch\u1ecb l\u1ea1i gi\u1ea3 ngu \u0111\u1ec3 l\u01b0\u1eddi bi\u1ebfc r\u1ed3i\u2026\u2026",
    # 56 Verisa (2 br)
    "\u00ca\u201a n\u00f3i c\u00e1i g\u00ec th\u1ebf\u2014?<br>\u0110\u1eebng c\u00f3 n\u00f3i m\u1ea5y \u0111i\u1ec1u k\u1ef3 qu\u1eb7c nh\u01b0 v\u1eady ch\u1ee9?",
    # 57 Veera (2 br)
    "\u2026\u2026 Em th\u00ec kh\u00f4ng sao\u201a nh\u01b0ng n\u1ebfu Ch\u1ec9 Huy l\u1ea1i m\u1eafng em l\u1ea7n n\u1eefa<br>th\u00ec em \u0111\u1eebng c\u00f3 kh\u00f3c nh\u00e9!",
    # 58 Wendy
    "H\u1eed\u201a Verisa\u201a ch\u1ecb l\u00fac n\u00e0o c\u0169ng b\u1ecb m\u1eafng sao?",
    # 59 Verisa
    "V\u00e2ng. Kh\u00f4ng ch\u1ec9 b\u1ecb m\u1eafng\u2014Ch\u1ec9 Huy c\u00f2n tr\u00eau ch\u1ecdc em n\u1eefa c\u01a1.",
    # 60 Veera
    "M\u1ed7i l\u1ea7n nh\u01b0 v\u1eady em l\u1ea1i kh\u00f3c\u2026\u2026 nh\u01b0ng m\u00e0 ch\u1ed7 \u0111\u00f3 c\u0169ng d\u1ec5 th\u01b0\u01a1ng \u0111\u1ea5y ch\u1ee9.",
    # 61 Verisa
    "Vi\u201a Veera! \u0110\u1eebng c\u00f3 t\u1ef1 ti\u1ec7n b\u00e9p x\u00e9p b\u00ed m\u1eadt c\u1ee7a em!",
    # 62 Veera
    "E h\u00e8 h\u00e8! Xin l\u1ed7i em. T\u1ea1i l\u1edf mi\u1ec7ng th\u00f4i\u2026\u2026",
    # 63 Wendy
    "\u01afm\u2026\u2026?",
    # 64 Verisa (2 br)
    "H\u1ea3!? Kh\u201a kh\u00f4ng c\u00f3 g\u00ec \u0111\u00e2u\u2014\u2661 \u0110\u00f9a th\u00f4i\u2661 \u0110\u00f9a th\u00f4i\u2661 N\u00e0o\u201a mau \u0111i t\u00ecm<br>kh\u1ed1i qu\u1eb7ng th\u00f4i!",
    # 65 Wendy
    "\u00c1\u201a \u0111\u00fang r\u1ed3i nh\u1ec9! Em hi\u1ec3u r\u1ed3i. M\u1eddi hai v\u1ecb \u0111i theo em!",
]


def main() -> None:
    data = EN.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    vi_lines: list[str] = []
    idx = 0
    record_count = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            record_count += 1
            assert idx < len(TRANSLATIONS), f"Ran out of translations at record {record_count}"
            vi_text = TRANSLATIONS[idx]
            idx += 1
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text
            else:
                parts = ln.split(",", 5)
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                assert "," not in vi_text, f"ASCII comma in VI text (record {record_count}); use U+201A '‚'"
                parts[2] = vi_text + suffix
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    assert idx == len(TRANSLATIONS), f"translations not fully used: {idx}/{len(TRANSLATIONS)}"
    assert record_count == len(TRANSLATIONS), f"record count {record_count} != {len(TRANSLATIONS)}"

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()
