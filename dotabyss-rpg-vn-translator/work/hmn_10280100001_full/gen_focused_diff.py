#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate focused_diff.md (EN -> VI text-field changes) for hmn_10280100001."""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10280100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = Path(__file__).parent / "focused_diff.md"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def field_of(line):
    line = line.rstrip("\r\n")
    if line.startswith("title,"):
        return line.split(",", 1)[1]
    if line.startswith(TEXT_CMDS[1:] + ("message,",)):
        return line.split(",", 5)[2]
    return None


def main():
    en_lines = EN.read_text(encoding="utf-8-sig").splitlines()
    vi_lines = VI.read_text(encoding="utf-8-sig").splitlines()
    parts = ["# Focused Diff — hmn_10280100001", "",
             "Format: `EN field` -> `VI field` (only changed text records shown).", ""]
    n = 0
    for i, (el, vl) in enumerate(zip(en_lines, vi_lines), 1):
        if not el.startswith(TEXT_CMDS):
            continue
        ef, vf = field_of(el), field_of(vl)
        if ef != vf:
            n += 1
            label = el.split(",", 1)[0]
            parts.append(f"### L{i} ({label})")
            parts.append(f"- EN: `{ef}`")
            parts.append(f"- VI: `{vf}`")
            parts.append("")
    parts.append(f"_{n} text records changed._")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({n} changed records)")


if __name__ == "__main__":
    main()
