#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Preflight: compare EN source text-field <br> counts and ASCII-comma usage
against the VI translations, WITHOUT writing the output file."""
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10330100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
DATA = Path(__file__).resolve().parent / "vi_translations.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

raw = EN.read_bytes()
text = raw.decode("utf-8-sig")
lines = text.split("\r\n")
translations = [ln for ln in DATA.read_text(encoding="utf-8").split("\n") if ln != ""]

idx = 0
record = 0
errors = 0
for ln in lines:
    if ln.startswith(TEXT_CMDS):
        record += 1
        if idx >= len(translations):
            print(f"[REC {record}] NO translation available (have {len(translations)})")
            errors += 1
            idx += 1
            continue
        vi = translations[idx]
        idx += 1
        vi_body = re.sub(r"<br>\s*$", "", vi)
        if ln.startswith("title,"):
            en_body = ln.split(",", 1)[1]
        else:
            en_body = re.sub(r"(?:<br>\s*)+$", "", ln.split(",", 5)[2])
        en_br = en_body.count("<br>")
        vi_br = vi_body.count("<br>")
        if en_br != vi_br:
            print(f"[REC {record}] <br> count MISMATCH en={en_br} vi={vi_br}")
            print(f"    EN: {ln[:110]}")
            print(f"    VI: {vi[:110]}")
            errors += 1
        if "," in vi_body:
            print(f"[REC {record}] ASCII comma in VI body (use U+201A '‚'): {vi[:110]}")
            errors += 1

print(f"records={record} translations={len(translations)} errors={errors}")
