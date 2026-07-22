#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Field-index VI builder for hmn_10330100002 (EN-asset-is-English case).

Reads the EN asset, swaps ONLY the text field (parts[2] for
message*/messageTextUnder/messageTextCenter, parts[1] for title) with the
ordered Vietnamese translations from vi_translations.txt (one VI text per line,
in source text-record order), and preserves BOM/CRLF/delimiter/field/tag/
placeholder structure. Trailing tag suffix ("<br> " for message fields,
"</size>" for center cards) is MIRRORED automatically from the source.

Then: python ../verify_asset_translation.py --root E:/AgentTranslation hmn_10330100002
"""
from __future__ import annotations
import re
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10330100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
DATA = WORK / "vi_translations.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")


def main() -> None:
    raw = EN.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    translations = [ln.rstrip("\n") for ln in DATA.read_text(encoding="utf-8").split("\n")]
    # drop trailing blank lines
    while translations and translations[-1] == "":
        translations.pop()

    out_lines: list[str] = []
    idx = 0
    record_count = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            record_count += 1
            assert idx < len(translations), f"Ran out of translations at record {record_count}"
            vi_text = translations[idx]
            idx += 1
            assert "," not in vi_text, f"ASCII comma in VI text (record {record_count}); use U+201A '‚'"
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text
            elif ln.startswith("messageTextCenter,") or ln.startswith("messageTextUnder,"):
                # these fields already carry their own enclosing tags (e.g. <size=48>...</size>)
                parts = ln.split(",", 5)
                parts[2] = vi_text
            else:  # message,
                parts = ln.split(",", 5)
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                # VI body may be authored with its own trailing <br> (for readability);
                # strip it so the mirrored source suffix isn't duplicated.
                vi_text = re.sub(r"<br>\s*$", "", vi_text)
                parts[2] = vi_text + suffix
            out_lines.append(",".join(parts))
        else:
            out_lines.append(ln)

    assert idx == len(translations), f"translations not fully used: {idx}/{len(translations)}"
    assert record_count == len(translations), f"record count {record_count} != {len(translations)}"

    out = ("\r\n" if has_crlf else "\n").join(out_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(out_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()
