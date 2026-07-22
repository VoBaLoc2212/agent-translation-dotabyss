#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate focused_diff.md for hmn_10340100002: EN source text -> VI output, per record."""
from __future__ import annotations
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10340100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10340100002_full/focused_diff.md"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def text_field(line: str):
    if line.startswith("title,"):
        return line[len("title,"):].rstrip("\r\n")
    parts = line.split(",", 5)
    return ",".join(parts[2:]).rstrip("\r\n")


def main():
    en_lines = EN.read_text(encoding="utf-8-sig").splitlines()
    vi_lines = VI.read_text(encoding="utf-8-sig").splitlines()
    rows = []
    rec = 0
    for e, v in zip(en_lines, vi_lines):
        if e.startswith(TEXT_CMDS):
            rec += 1
            rows.append((rec, e.split(",", 1)[0].rstrip(","), text_field(e), text_field(v)))
    md = ["# focused_diff — hmn_10340100002", "",
          "EN-asset-is-English + title-still-JP case. Columns: # | command | EN source text field | VI output text field.", ""]
    md.append(f"Total text records: {len(rows)} (1 title + 67 message)")
    md.append("")
    for n, cmd, en_tf, vi_tf in rows:
        md.append(f"### {n}. `{cmd}`")
        md.append(f"- EN:  {en_tf}")
        md.append(f"- VI:  {vi_tf}")
        md.append("")
    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"WROTE {OUT} | rows={len(rows)}")


if __name__ == "__main__":
    main()
