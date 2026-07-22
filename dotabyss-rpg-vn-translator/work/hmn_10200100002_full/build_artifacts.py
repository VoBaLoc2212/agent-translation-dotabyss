#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build focused_diff.md and manifest.json for hmn_10200100002."""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10200100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
QA = WORK / "qa_log.json"
FOCUSED = WORK / "focused_diff.md"
MANIFEST = WORK / "manifest.json"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


en_lines = EN.read_bytes().decode("utf-8-sig").splitlines(True)
vi_lines = VI.read_bytes().decode("utf-8-sig").splitlines(True)

diff = ["# Focused diff: translatable text records", "",
        f"Scene: {SCENE}", f"EN source: {EN}", f"VI output: {VI}", ""]

entries = []
for i, (o, n) in enumerate(zip(en_lines, vi_lines), 1):
    oc = o.rstrip("\r\n")
    nc = n.rstrip("\r\n")
    if oc.startswith(TEXT_CMDS):
        cmd = oc.split(",", 1)[0]
        entries.append({"line": i, "cmd": cmd, "en": oc, "vi": nc})
        diff.append(f"## L{i} ({cmd})")
        diff.append(f"- EN: {oc}")
        diff.append(f"+ VI: {nc}")
        diff.append("")

FOCUSED.write_text("\n".join(diff) + "\n", encoding="utf-8")
print(f"focused_diff.md: {len(entries)} translatable records")

qa = json.loads(QA.read_text(encoding="utf-8-sig")) if QA.exists() else {}

manifest = {
    "scene": SCENE,
    "source_file": str(EN),
    "output_file": str(VI),
    "work_dir": str(WORK),
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source_sha256": sha(EN),
    "output_sha256": sha(VI),
    "source_line_count": len(en_lines),
    "output_line_count": len(vi_lines),
    "line_count_match": len(en_lines) == len(vi_lines),
    "translatable_records": len(entries),
    "candidate_counts": qa.get("candidate_counts", {}),
    "translated_records": qa.get("translated_records", len(entries)),
    "rules": {
        "jp_primary_en_alignment": True,
        "commander": "Chỉ Huy",
        "addressing_laveria": "em->anh (兄さん=anh)",
        "addressing_alicia_to_commander": "Chỉ Huy",
        "self_ref_laveria": "em (アタシ)",
        "self_ref_alicia": "em (わたし)",
        "title_case": "Vietnamese Title Case",
        "ascii_comma_in_text": False,
        "bom_preserved": True,
        "crlf_preserved": True,
        "tags_br_preserved": True,
    },
    "independent_verify": qa.get("independent_verify"),
    "status": qa.get("independent_verify"),
    "issues": qa.get("independent_issues", []),
    "entries": entries,
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"manifest.json written: status={manifest['status']}")
