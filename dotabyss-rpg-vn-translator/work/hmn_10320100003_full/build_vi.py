#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic VI builder for hmn_10320100003 (EN-asset-is-English case).

Reads the EN asset, swaps ONLY the text field with the ordered VI translations,
mirrors the source trailing "<br> " suffix automatically, preserves BOM/CRLF/
delimiter/field/tag/placeholder structure. Asserts <br> counts match the EN
asset (authoritative) before writing, and forbids ASCII commas in VI text.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10320100003"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# Ordered VI text fields, 1:1 with source text records in file order.
# (title first, then each message in order). Internal <br> placed where the
# EN asset had them; do NOT include the trailing "<br> " suffix.
TRANSLATIONS = [
    "B\u00cd M\u1eadt C\u1ee7a C\u1ef1u Tr\u00f4m",  # title
    "D\u1eebng l\u1ea1i \u0111i! Th\u1ea3 em ra!",
    "Daria\u201a l\u1ea7n n\u00e0y h\u00e3y gi\u1ea3i th\u00edch t\u1eed t\u1ebf cho. Con nh\u00f3c n\u00e0y r\u1ed1t cu\u1ed9c l\u00e0 ai v\u1eady?",
    "C-con b\u00e9 \u1ea5y l\u00e0\u2026\u2026",
    "Ch\u00e1u \u1ea5y l\u00e0 m\u1ed9t \u0111\u1ee9a tr\u1ebb\u2026\u2026",
    "Nh\u00ecn c\u0169ng th\u1ea5y r\u00f5. T\u00f4i \u0111ang h\u1ecfi n\u00f3 v\u00e0 em c\u00f3 m\u1ed1i quan h\u1ec7 g\u00ec.",
    "T\u1eeb c\u00e1ch em h\u00e0nh \u0111\u1ed9ng n\u00e3y gi\u1edd\u201a r\u00f5 r\u00e0ng hai \u0111\u1ee9a quen bi\u1ebft nhau m\u00e0. G\u1eb7p nhau \u1edf \u0111\u00e2u<br>m\u00e0 quen? M\u1ed1i quan h\u1ec7 l\u00e0 g\u00ec?",
    "Em h\u00e9t to\u00e1ng l\u00ean r\u1ed3i c\u00f2n \u0111\u1ecbnh th\u1ea3 n\u00f3 ch\u1ea1y n\u1eefa. Ch\u1eafc n\u00f3 l\u00e0<br>ng\u01b0\u1eddi c\u1ef1c k\u1ef3 quan tr\u1ecdng v\u1edbi em \u0111\u00fang kh\u00f4ng?",
    "\u01afm\u2026\u2026c-chuy\u1ec7n \u0111\u00f3 l\u00e0\u2026\u2026",
    "*th\u1edf d\u00e0i*... C\u00f3 im l\u1eb7ng th\u00ec c\u0169ng ch\u1eb3ng gi\u1ea3i quy\u1ebft \u0111\u01b0\u1ee3c g\u00ec \u0111\u00e2u.",
    "N\u1ebfu em c\u00f2n gi\u1ea5u gi\u1ebfm Ch\u1ec9 Huy\u201a th\u00ec em s\u1ebd ph\u1ea3i nh\u1eadn<br>h\u00ecnh ph\u1ea1t th\u00edch \u0111\u00e1ng \u0111\u1ea5y.",
    "H\u1ea3!?",
    "Em kh\u00f4ng mu\u1ed1n th\u1ebf \u0111\u00e2u\u201a ph\u1ea3i kh\u00f4ng? \u0110\u00e3 hi\u1ec3u th\u00ec mau tr\u1ea3 l\u1eddi<br>c\u00e2u h\u1ecfi c\u1ee7a t\u00f4i \u0111i\u2014",
    "Hyaa!",
    "\u1ef0!",
    "H\u1ea3...!?",
    "\u00d4ng gi\u00e0 x\u1ea5u xa! \u0110\u1eebng b\u1eaft n\u1ea1t ch\u1ecb g\u00e1i em m\u00e0!!",
    "N\u00e0y\u201a th\u00f4i \u0111i! \u0110\u1eebng \u0111\u00e1nh!",
    "D-d\u1eebng l\u1ea1i! V\u00f9ng v\u1eaby nguy hi\u1ec3m l\u1eafm...!",
    "Ch\u1ecb g\u00e1i l\u00e0 ng\u01b0\u1eddi t\u1ed1t m\u00e0! Ch\u1ecb \u1ea5y ch\u1eb3ng l\u00e0m \u0111i\u1ec1u x\u1ea5u n\u00e0o \u0111\u00e2u!",
    "Ch\u1ecb \u1ea5y l\u00fac n\u00e0o c\u0169ng c\u1ed1 g\u1eafng v\u00ec em m\u00e0!",
    "\u00abV\u00ec em\u00bb...? \u00d3 em l\u00e0 sao?",
    "C-chuy\u1ec7n \u0111\u00f3 l\u00e0\u2026\u2026",
    "*n\u1ee9c n\u1edf*...<br>\u00d2a kh\u00f3c!",
    "\u00d4i! Kh\u00f4ng kh\u00f4ng kh\u00f4ng...!",
    "N\u00e0y\u201a \u0111\u1eebng kh\u00f3c!<br>\u00c1... ch\u00e0\u201a c\u00e1i qu\u00e1i g\u00ec \u0111\u00e2y...",
    "S\u1ee5t s\u1ecbt... s\u1ee5t\u201a s\u1ee5t...",
    "...\u0110\u00e3 b\u00ecnh t\u0129nh ch\u01b0a?",
    "S\u1ee5t s\u1ecbt... \u1eebng.<br>C\u1ea3m \u01a1n\u201a ch\u1ecb g\u00e1i.",
    "*th\u1edf d\u00e0i*. Th\u1eadt l\u00e0 m\u1ed9t phen v\u1ea5t v\u1ea3.",
    "\u0110\u01b0\u1ee3c r\u1ed3i\u201a t\u00f4i \u0111\u00e3 nghe to\u00e0n b\u1ed9 c\u00e2u chuy\u1ec7n. \u0110\u1ec3 t\u00f4i s\u1eafp x\u1ebfp l\u1ea1i suy ngh\u0129 m\u1ed9t ch\u00fat\u201a nh\u00e9?",
    "V\u00e2ng\u2026\u2026",
    "Th\u1ebf th\u00ec... tr\u01b0\u1edbc h\u1ebft\u201a c\u00f3 tin \u0111\u1ed3n em t\u1eebng l\u00e0 c\u1ef1u tr\u00f4m. Chuy\u1ec7n \u0111\u00f3<br>\u0111\u00fang s\u1ef1 th\u1eadt ch\u01b0?",
    "...V\u00e2ng. Tr\u01b0\u1edbc khi th\u00e0nh th\u1ee3 khai th\u00e1c\u201a em t\u1eebng gia nh\u1eadp b\u0103ng tr\u00f4m.",
    "\u1eecm. V\u00e0 c\u0169ng v\u00e0o th\u1eddi \u0111i\u1ec3m \u0111\u00f3\u201a em \u0111\u00e3 g\u1eb7p con b\u00e9.",
    "...\u0110\u00fang v\u1eady. C\u00f3 tin t\u1ee9c n\u00f3i r\u1eb1ng gia \u0111\u00ecnh con b\u00e9 r\u1ea5t gi\u00e0u c\u00f3\u2026\u2026",
    "\u0110\u1ec3 t\u1ea1o c\u01a1 h\u1ed9i cho \u0111\u1ed3ng b\u1ed9n x\u00e2m nh\u1eadp\u201a em \u0111\u00e3 l\u00e0m quen v\u1edbi con b\u00e9 v\u00e0 tr\u1edf n\u00ean th\u00e2n thi\u1ebft.",
    "Em gi\u1ea3 v\u1eddi l\u00e0m ng\u01b0\u1eddi t\u1eed t\u1ebf\u2026\u2026. Th\u1eadt s\u1ef1\u201a em \u0111\u00e3 l\u00e0m m\u1ed9t chuy\u1ec7n t\u1ed3i t\u1ec7\u2026\u2026",
    "Kh\u00f4ng \u0111\u00fang \u0111\u00e2u! Ch\u1ecb g\u00e1i ch\u1ec9 \u0111\u01b0\u1ee3c b\u1ea3o l\u00e0m th\u1ebf th\u00f4i\u201a ph\u1ea3i kh\u00f4ng?",
    "Ch\u1ecb g\u00e1i \u0111\u00e3 t\u1eed t\u1ebf v\u1edbi em m\u00e0! Ch\u1ecb \u1ea5y ch\u1eb3ng l\u00e0m \u0111i\u1ec1u x\u1ea5u n\u00e0o \u0111\u00e2u!",
    "\u1eea. Nghe c\u00e2u chuy\u1ec7n th\u00ec t\u00f4i c\u0169ng \u0111\u1ed3ng \u00fd v\u1edbi em.",
    "H\u1ed3i \u0111\u00f3 v\u1ecb th\u1ebf c\u1ee7a Daria r\u1ea5t y\u1ebfu \u0111u\u1ed1i\u201a ph\u1ea3i kh\u00f4ng? N\u00ean b\u1ecdn tr\u00f4m \u0111\u00e3 b\u1eaft em<br>l\u00e0m vi\u1ec7c c\u1ef1c nh\u1ecdc theo m\u1ec7nh l\u1ec7nh c\u1ee7a ch\u00fang.",
    "Nh\u01b0ng m\u00e0\u2026\u2026gi\u1eefa l\u00fac \u0111\u00f3\u201a m\u1ed9t s\u1ef1 c\u1ed1 b\u1ea5t ng\u1edd \u0111\u00e3 x\u1ea3y ra.",
    "A... ph\u1ea3i\u2026\u2026",
    "B\u1ecdn \u0111\u1ed3ng b\u1ed9n \u0111\u00e3 l\u1ee3i d\u1ee5ng s\u01a1 h\u1edf do em t\u1ea1o ra m\u00e0 l\u1ebfn v\u00e0o nh\u00e0.",
    "Nh\u01b0ng m\u00e0\u2026\u2026k\u1ebf ho\u1ea1ch kh\u00f4ng su\u00f4n s\u1ebb\u201a b\u1ecdn ch\u00fang \u0111\u00e3 \u0111\u1ee5ng \u0111\u1ed9 tr\u1ef1c ti\u1ebfp v\u1edbi<br>ch\u1ee7 nh\u00e0...",
    "R\u1ed3i th\u00ec\u2026\u2026. T\u1ea1i \u0111\u00f3\u2026\u2026. Cha m\u1eb9 c\u1ee7a con b\u00e9 th\u00ec l\u00e0\u2026\u2026",
    "Hmph\u2026\u2026. C\u00e2u chuy\u1ec7n th\u1eadt s\u1ef1 kh\u00f3 ch\u1ecbu.",
    "L\u00fac \u0111\u00f3\u2026\u2026em \u0111\u00e3 ch\u00e1n gh\u00e9t t\u1ea5t c\u1ea3. Gh\u00e9t b\u0103ng tr\u00f4m. V\u00e0 h\u01a1n h\u1ebft\u201a em gh\u00e9t ch\u00ednh<br>m\u00ecnh v\u00ec \u0111\u00e3 l\u00e0 m\u1ed9t trong b\u1ecdn ch\u00fang.",
    "Nh\u01b0ng m\u00e0\u2026\u2026khi em xin l\u1ed7i\u201a con b\u00e9 \u0111\u00e3 n\u00f3i v\u1edbi em r\u1eb1ng:<br>\u00abKh\u00f4ng ph\u1ea3i l\u1ed7i c\u1ee7a ch\u1ecb g\u00e1i \u0111\u00e2u.\u00bb",
    "H\u1ea3!?",
    "D\u00f9 v\u00ec em m\u00e0 con b\u00e9 ph\u1ea3i ch\u1ecbu c\u1ea3nh kinh kh\u1ee7ng nh\u01b0 v\u1eady. Th\u1ebf m\u00e0 con b\u00e9 v\u1eabn<br>th\u1ee9a cho em...",
    "\u1eea! V\u00ec \u0111\u00f3 l\u00e0 s\u1ef1 th\u1eadt m\u00e0!",
    "L\u0169 tr\u00f4m \u0111\u1ec1u l\u00e0 k\u1ebb x\u1ea5u\u201a nh\u01b0ng ch\u1ec9 c\u00f3 ch\u1ecb g\u00e1i l\u00e0 ng\u01b0\u1eddi t\u1eed t\u1ebf th\u00f4i!",
    "V\u00ec ch\u1ecb \u0111\u00e3 c\u1ee9u em m\u00e0!",
    "...C\u1ea3m \u01a1n em\u2026\u2026",
    "T\u00f4i \u0111\u00e3 hi\u1ec3u r\u00f5 t\u00ecnh h\u00ecnh. Chuy\u1ec7n em \u0111i thu th\u1eadp qu\u1eb7ng c\u0169ng c\u00f3 th\u1ec3 gi\u1ea3i th\u00edch \u0111\u01b0\u1ee3c.",
    "V\u1eady to\u00e0n b\u1ed9 qu\u1eb7ng \u1edf \u0111\u00e2y \u0111\u1ec1u l\u00e0 \u0111\u1ec3 \u0111\u01b0a cho con b\u00e9\u201a \u0111\u1ec3 gi\u00fap con b\u00e9 sinh s\u1ed1ng.",
    "V\u00e2ng\u2026\u2026\u0111\u00fang v\u1eady\u201a s\u1ebfp.",
    "Sau khi ho\u00e0n th\u00e0nh xong c\u00f4ng vi\u1ec7c ch\u00ednh\u201a em \u0111\u00e3 t\u1eeb t\u1eeb thu th\u1eadp trong<br>th\u1eddi gian r\u00e3nh r\u1ed5i.",
    "N\u00ean em \u0111\u00e2u c\u00f3 \u0103n tr\u00f4m g\u00ec. Em \u0111\u00e3 xin ph\u00e9p \u0111\u00e0ng ho\u00e0ng t\u1eeb \u0111\u1ed9i th\u00e1m hi\u1ec3m<br>m\u00e0\u2026\u2026",
    "\u0110\u1ec3 cho ch\u1eafc th\u00ec h\u1ecfi r\u00f5\u201a c\u1ee5 th\u1ec3 l\u00e0 th\u1ebf n\u00e0o?",
    "\u01afm\u2026\u2026. Sau khi xong ch\u1ec9 ti\u00eau\u201a em h\u1ecfi \u00abC\u00f3 \u0111\u01b0\u1ee3c \u0111\u00e0o m\u1ed9t m\u00ecnh kh\u00f4ng\u00bb hay<br>g\u00ec \u0111\u00f3\u2026\u2026",
    "...Qu\u1ea3 nhi\u00ean em n\u00f3i ch\u01b0a \u0111\u1ee7 r\u00f5.",
    "A ha ha!\u266a Ch\u1ecb g\u00e1i h\u00e0i h\u01b0\u1edbc th\u1eadt!\u266a",
    "Th\u1ebf \u00e0\u2026\u2026?",
    "*th\u1edf d\u00e0i*... Gi\u00e1 nh\u01b0 em k\u1ec3 s\u1edbm h\u01a1n cho t\u00f4i. H\u1ebfn \u0111\u00e3 c\u00f3 c\u00e1ch gi\u1ea3i quy\u1ebft<br>kh\u00e1c t\u1ed1t h\u01a1n.",
    "Xin l\u1ed7i\u201a s\u1ebfp\u2026\u2026. Nh\u01b0ng em ngh\u0129 n\u1ebfu l\u00e0m v\u1eady\u201a c\u00f3 l\u1ebd em s\u1ebd kh\u00f4ng th\u1ec3 c\u1ee9u<br>\u0111\u01b0\u1ee3c con b\u00e9...",
    "S\u1ef1 th\u1eadt l\u00e0\u201a vi\u1ec7c \u0111\u01b0a con b\u00e9 v\u00e0o doanh tr\u1ea1i c\u0169ng ch\u1eb3ng ph\u1ea3i chuy\u1ec7n hay\u2026\u2026",
    "V\u1ec1 m\u1eb7t quy t\u1eafc th\u00ec \u0111\u00fang v\u1eady. Quy \u0111\u1ecbnh l\u00e0 ch\u1ec9 nh\u1eefng ng\u01b0\u1eddi l\u00e0m vi\u1ec7c t\u1ea1i<br>C\u0103n C\u1ee9 Ti\u1ec1n Tuy\u1ebfn m\u1edbi \u0111\u01b0\u1ee3c ra v\u00e0o.",
    "H\u1ea3? V\u1eady l\u00e0 em kh\u00f4ng \u0111\u01b0\u1ee3c \u0111\u1ebfn n\u1eefa sao? \u01a0i ch\u00e0\u2026\u2026!",
    "Th\u00f4i\u201a \u0111\u1eebng ho\u1ea3ng. T\u00f4i v\u1eeba n\u1ea9y ra m\u1ed9t \u00fd hay.",
    "N\u00e0y\u201a em n\u00e0y. Em c\u00f3 mu\u1ed1n c\u00f9ng l\u00e0m vi\u1ec7c \u1edf \u0111\u00e2y v\u1edbi Daria kh\u00f4ng?",
    "\u00c1!",
    "Em \u0111ang t\u00fang thi\u1ebfu ph\u1ea3i kh\u00f4ng? N\u1ebfu em l\u00e0m vi\u1ec7c \u1edf \u0111\u00e2y\u201a t\u00f4i s\u1ebd tr\u1ea3 ti\u1ec1n cho<br>em v\u00e0 cho em ch\u1ed7 \u1edf.",
    "Th\u1eadt \u00e1!?",
    "\u1eea. Nh\u01b0ng t\u00f4i kh\u00f4ng d\u1ec5 d\u00e3i nh\u01b0 Daria \u0111\u00e2u. N\u1ebfu em kh\u00f4ng ch\u1ecbu kh\u00f3 l\u00e0m vi\u1ec7c\u201a t\u00f4i<br>s\u1ebd \u0111u\u1ed5i em \u0111i ngay l\u1eadp t\u1ee9c\u2014",
    "C\u1ea3m \u01a1n \u00f4ng nha!\u266a",
    "N\u00e0y n\u00e0y\u201a \u0111\u1eebng \u00f4m ta! V\u1edbi l\u1ea1i\u201a th\u00f4i g\u1ecdi ta l\u00e0 \u00ab\u00f4ng\u00bb \u0111i!",
    "\u1ed0i\u201a s\u1ebfp. Th\u1eadt s\u1ef1 \u1ed5n sao\u2026\u2026?",
    "\u1eea. C\u00f4ng vi\u1ec7c c\u1ee7a \u0111\u1ed9i th\u00e1m hi\u1ec3m c\u0169ng s\u1ebd c\u00f2n b\u1eadn r\u1ed9n h\u01a1n nhi\u1ec1u\u201a n\u00ean... V\u1edbi<br>l\u1ea1i\u2026\u2026",
    "N\u00e0y\u201a m\u1ecdi ng\u01b0\u1eddi c\u0169ng \u0111\u1ed3ng \u00fd v\u1edbi t\u00f4i ch\u1ee9?",
    "\u2026?",
    "V-v\u00e2ng!",
    "T\u00f4i ngh\u0129 \u0111\u00f3 l\u00e0 \u00fd hay\u2026\u2026!",
    "H\u1ea3! M\u1ecdi ng\u01b0\u1eddi!? Sao c\u00e1c v\u1ecb l\u1ea1i \u1edf \u0111\u00e2y\u2026\u2026",
    "B\u1ecdn h\u1ecd t\u00f2 m\u00f2 v\u1ec1 s\u1ef1 th\u1eadt sau nh\u1eefng l\u1eddi \u0111\u1ed3n\u201a n\u00ean \u0111\u00e3 l\u00e9n nghe tr\u1ed9m. Th\u1ebf n\u00e0o\u201a<br>\u0111\u00e3 s\u00e1ng t\u1ecf ch\u01b0a?",
    "V\u00e2ng\u2026\u2026t\u00f4i \u0111\u00e3 hi\u1ec3u r\u1ed3i.",
    "N\u1ebfu c\u00f3 vi\u1ec7c g\u00ec ch\u00fang t\u00f4i gi\u00fap \u0111\u01b0\u1ee3c\u201a c\u1ee9 n\u00f3i nh\u00e9!",
    "...A\u201a v\u00e2ng\u2026\u2026",
    "Th\u1ebf l\u00e0 m\u1ecdi chuy\u1ec7n \u0111\u00e3 \u00eam \u0111\u1eb9p c\u1ea3 r\u1ed3i.",
    "V\u1eady l\u00e0 quy\u1ebft \u0111\u1ecbnh nh\u00e9! Hai \u0111\u1ee9a\u201a h\u00e3y d\u1eabn con b\u00e9 \u0111i tham quan.",
    "V\u00e2ng! Th\u1ebf th\u00ec ch\u00fang ta \u0111i th\u00f4i?",
    "\u1ee6m! \u00d4ng\u201a t\u1ea1m bi\u1ec7t nh\u00e9!",
    "*th\u1edf d\u00e0i*... \u00c1\u201a \u0111\u1ee7 th\u1ee9 chuy\u1ec7n khi\u1ebfn ng\u01b0\u1eddi ta m\u1ec7t m\u1ecfi.",
    "...\u01afm\u201a s\u1ebfp\u2026\u2026. Em xin l\u1ed7i v\u00ec \u0111\u00e3 l\u00e0m phi\u1ec1n s\u1ebfp nhi\u1ec1u\u2026\u2026",
    "Hmph. \u0110\u00fang th\u1ebf. Ph\u1ea7n phi\u1ec1n to\u00e1i em g\u00e2y cho t\u00f4i\u201a em s\u1ebd \u0111\u1ec1n b\u00f9 b\u1eb1ng c\u00f4ng<br>vi\u1ec7c.",
    "...D\u00f9 sao th\u00ec Daria. C\u00f4ng vi\u1ec7c khai th\u00e1c c\u1ee7a em \u0111\u1ebfn gi\u1edd h\u1eb3n v\u1ea5t v\u1ea3 l\u1eafm.",
    "D\u00f9 em ch\u1ec9 t\u00edch l\u0169y t\u1eebng ch\u00fat m\u1ed9t\u201a em v\u1eabn thu th\u1eadp \u0111\u01b0\u1ee3c nhi\u1ec1u qu\u1eb7ng \u0111\u1ebfn th\u1ebf<br>n\u00e0y. \u0110\u00fang nh\u01b0 t\u00f4i ngh\u0129\u201a em l\u00e0 m\u1ed9t th\u1ee3 khai th\u00e1c tuy\u1ec7t v\u1eddi.",
    "T\u1eeb nay tr\u1edf \u0111i\u201a c\u1ee9 ch\u0103m ch\u1ec9 ho\u00e0n th\u00e0nh ch\u1ec9 ti\u00eau l\u00e0 \u0111\u01b0\u1ee3c. ...Nh\u01b0ng \u0111\u1eebng c\u00f3<br>l\u00e0m qu\u00e1 s\u1ee9c.",
    "...V\u00e2ng. C\u1ea3m \u01a1n s\u1ebfp nhi\u1ec1u.\u266a",
    "...Nh\u01b0ng\u201a \u01afm\u2026\u2026. N\u1ebfu anh kh\u00f4ng phi\u1ec1n th\u00ec\u2026\u2026",
    "\u1eeam? C\u00f3 chuy\u1ec7n g\u00ec?",
    "Em c\u00f3 th\u1ec3 \u0111\u00e0o... nhi\u1ec1u h\u01a1n n\u1eefa kh\u00f4ng\u2026\u2026?",
    "...H\u1ea3?",
    "\u0110i\u1ec1u em n\u00f3i v\u1ec1 vi\u1ec7c y\u00eau \u0111\u00e1 qu\u00fd... l\u00e0 th\u1eadt. H\u00ecnh nh\u01b0 em h\u01a1i tham lam \u0111\u1ee7<br>th\u1ee9......",
    "M\u1ed7i khi \u0111\u00e0o \u0111\u01b0\u1ee3c th\u1eadt nhi\u1ec1u \u0111\u00e1 qu\u00fd\u201a em vui l\u1eafm. Chuy\u1ec7n \u0111\u00f3 c\u0169ng l\u00e0 v\u00ec con<br>b\u00e9\u201a nh\u01b0ng kh\u00f4ng ch\u1ec9 c\u00f3 th\u1ebf\u2026\u2026",
    "H-h\u00f3a ra l\u00e0 v\u1eady. Th\u1ebf \u00e0.",
    "V\u00e2ng\u2026\u2026. Th\u1ef1c ra \u0111\u1ebfn gi\u1edd em v\u1eabn \u0111ang k\u00ecm n\u00e9n \u0111\u1ea5y. N\u1ebfu c\u00f3 th\u1ec3\u201a em mu\u1ed1n \u0111\u00e0o<br>nhi\u1ec1u h\u01a1n n\u1eefa......",
    "...N\u00e0y\u201a khoan \u0111\u00e3. Sao em l\u1ea1i ti\u1ebfn l\u1ea1i g\u1ea7n?",
    "Xin s\u1ebfp \u0111\u1ea5y\u201a s\u1ebfp\u2026\u2026. Em ngh\u0129 vi\u1ec7c n\u00e0y c\u0169ng l\u00e0 c\u00e1ch \u0111\u1ec3 \u0111\u1ec1n \u01a1n<br>s\u1ebfp......",
    "C\u00f4ng vi\u1ec7c n\u00e0y \u0111\u00e3 thay \u0111\u1ed5i cu\u1ed9c \u0111\u1eddi em\u2026\u2026. Ch\u1eafc ch\u1eafn n\u00f3 l\u00e0 thi\u00ean ch\u01a9c c\u1ee7a<br>em......",
    "V\u00ec \u0111\u00e1 qu\u00fd\u201a em s\u1ebd l\u00e0m b\u1ea5t c\u1ee9 \u0111i\u1ec1u g\u00ec\u2026\u2026",
    "V\u00ec \u0111\u1ed9i\u201a v\u00ec s\u1ebfp\u2026\u2026<br>xin h\u00e3y \u0111\u1ec3 em l\u00e0m......",
    "...\u1ed4-\u1ed5n r\u1ed3i! \u1ed4n r\u1ed3i!!<br>\u0110\u01b0\u1ee3c. T\u1eeb nay\u201a c\u1ee9 l\u00e0m theo \u00fd em th\u00edch.",
    "C\u1ea3m \u01a1n s\u1ebfp nhi\u1ec1u l\u1eafm!\u2661\u266a",
    "\u1ed0i\u201a n\u00e0y\u201a th\u00f4i \u0111i!<br>Sao c\u1ea3 em c\u0169ng \u00f4m l\u1ea5y ta n\u1eefa!",
]


def main() -> None:
    assert len(TRANSLATIONS) == 117, f"expected 117 translations, got {len(TRANSLATIONS)}"
    for vi in TRANSLATIONS:
        assert "," not in vi, f"ASCII comma in VI text; use U+201A \u201a: {vi!r}"

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
                vi_lines.append(",".join(parts))
                continue
            else:
                parts = ln.split(",", 5)
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                parts[2] = vi_text + suffix
            # structural <br> guard: source total == built total
            src_br = ln.count("<br>")
            built_br = parts[2].count("<br>")
            assert built_br == src_br, (
                f"LINE <br> mismatch record {record_count}: src={src_br} built={built_br} :: {ln!r}"
            )
            assert "," not in parts[2], f"ASCII comma slipped into text field record {record_count}"
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    assert idx == len(TRANSLATIONS), f"translations not fully used: {idx}/{len(TRANSLATIONS)}"
    assert record_count == len(TRANSLATIONS), f"record count {record_count} != {len(TRANSLATIONS)}"

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()
