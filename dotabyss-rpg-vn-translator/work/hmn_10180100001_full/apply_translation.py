from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SCENE = "hmn_10180100001"
ROOT = Path("E:/AgentTranslation")
WORK = ROOT / "dotabyss-rpg-vn-translator" / "work" / f"{SCENE}_full"
EN_ASSET = ROOT / "Translation" / "en" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{SCENE}.txt"
VI_ASSET = ROOT / "Translation" / "vi" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{SCENE}.txt"
JA_JSON = ROOT / "dotabyss-translation-main" / "translations" / "novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main" / "translations" / "novels" / SCENE / "en.json"
TRANSLATIONS = WORK / "translations_vi.json"
MANIFEST = WORK / "manifest.json"
QA_LOG = WORK / "qa_log.json"
DIFF = WORK / "focused_diff.md"
TEXT_COMMANDS = ("title", "message", "messageTextUnder", "messageTextCenter")
TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"(%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%)")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_bytes(path: Path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "CRLF" if b"\r\n" in raw else "LF"
    text = raw.decode("utf-8-sig")
    return raw, text, bom, newline


def split_keep_newlines(text: str):
    return text.splitlines(keepends=True)


def line_body(line: str) -> str:
    return line[:-2] if line.endswith("\r\n") else line[:-1] if line.endswith("\n") else line


def line_eol(line: str) -> str:
    return "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""


def command(line: str) -> str:
    body = line_body(line)
    return body.split(",", 1)[0] if "," in body else body


def text_records(lines):
    out = []
    for idx, line in enumerate(lines, 1):
        cmd = command(line)
        if cmd in TEXT_COMMANDS:
            out.append((idx, cmd, line_body(line)))
    return out


def tags(s: str):
    return TAG_RE.findall(s)


def placeholders(s: str):
    return PLACEHOLDER_RE.findall(s)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    raw, src_text, bom, newline = read_text_bytes(EN_ASSET)
    src_lines = split_keep_newlines(src_text)
    ja = json.loads(JA_JSON.read_text(encoding="utf-8-sig"))
    en = json.loads(EN_JSON.read_text(encoding="utf-8-sig"))
    trans = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))

    records = text_records(src_lines)
    cmd_counts = Counter(cmd for _, cmd, _ in records)
    missing_trans = []
    unchanged = []
    applied = []
    ambiguity = []
    tag_mismatch = []
    placeholder_mismatch = []
    ascii_comma_violations = []
    non_jp_sources = []

    out_lines = src_lines[:]
    for idx, cmd, body in records:
        eol = line_eol(src_lines[idx-1])
        new_body = body
        matched_sources = [jp for jp in trans if jp in body]
        if len(matched_sources) != 1:
            ambiguity.append({"line": idx, "cmd": cmd, "matches": matched_sources, "body": body})
            continue
        jp = matched_sources[0]
        vi = trans[jp]
        if "," in vi:
            ascii_comma_violations.append({"line": idx, "jp": jp, "vi": vi})
        if tags(jp) != tags(vi):
            tag_mismatch.append({"line": idx, "jp_tags": tags(jp), "vi_tags": tags(vi), "jp": jp, "vi": vi})
        if placeholders(jp) != placeholders(vi):
            placeholder_mismatch.append({"line": idx, "jp_placeholders": placeholders(jp), "vi_placeholders": placeholders(vi), "jp": jp, "vi": vi})
        new_body = body.replace(jp, vi, 1)
        if new_body == body:
            unchanged.append({"line": idx, "cmd": cmd, "text": body})
        out_lines[idx-1] = new_body + eol
        applied.append({"line": idx, "cmd": cmd, "source": jp, "translation": vi, "status": "TRANSLATED"})
        if jp not in ja:
            non_jp_sources.append({"line": idx, "source": jp})

    out_text = "".join(out_lines)
    out_bytes = (("\ufeff" if bom else "") + out_text).encode("utf-8")
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_bytes)

    vi_raw, vi_text, vi_bom, vi_newline = read_text_bytes(VI_ASSET)
    vi_lines = split_keep_newlines(vi_text)
    structural_errors = []
    if len(src_lines) != len(vi_lines):
        structural_errors.append({"type": "line_count", "source": len(src_lines), "target": len(vi_lines)})
    for i, (s, v) in enumerate(zip(src_lines, vi_lines), 1):
        sb = line_body(s); vb = line_body(v)
        if sb.count(",") != vb.count(","):
            structural_errors.append({"line": i, "type": "delimiter_count", "source": sb.count(","), "target": vb.count(",")})
        if command(s) != command(v):
            structural_errors.append({"line": i, "type": "command", "source": command(s), "target": command(v)})
    if bom != vi_bom:
        structural_errors.append({"type": "bom", "source": bom, "target": vi_bom})
    if newline != vi_newline:
        structural_errors.append({"type": "newline", "source": newline, "target": vi_newline})

    # Build focused diff over only text command lines.
    src_focus = [f"{i}: {body}\n" for i, cmd, body in records]
    vi_records = text_records(vi_lines)
    vi_focus = [f"{i}: {body}\n" for i, cmd, body in vi_records]
    diff = "# Focused Diff: hmn_10180100001\n\n```diff\n" + "".join(
        difflib.unified_diff(src_focus, vi_focus, fromfile="EN/JP asset text records", tofile="VI asset text records", lineterm="")
    ) + "\n```\n"
    DIFF.write_text(diff, encoding="utf-8")

    qa_status = "PASS" if not (missing_trans or unchanged or ambiguity or tag_mismatch or placeholder_mismatch or ascii_comma_violations or structural_errors or non_jp_sources) and len(applied) == len(records) else "FAIL"
    notes = [
        "JP source in ja.json was primary; en.json contains blank values for this scene, so asset text order and ja.json keys were used for alignment.",
        "Speaker names and charaload asset names were preserved exactly per instruction.",
        "Gradia uses a calm, terse inventor voice; Commander↔Gradia translated mostly tôi/cô and Gradia→Commander cậu/Chỉ Huy based on source キミ/司令官.",
        "Alicia keeps polite assistant tone with em–anh toward Commander and chị for Gradia."
    ]
    qa = {
        "scene": SCENE,
        "status": qa_status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(EN_ASSET),
        "output": str(VI_ASSET),
        "text_command_counts": dict(cmd_counts),
        "total_text_records": len(records),
        "translated_records": len(applied),
        "structural_errors": structural_errors,
        "tag_mismatch": tag_mismatch,
        "placeholder_mismatch": placeholder_mismatch,
        "ascii_comma_violations": ascii_comma_violations,
        "ambiguity": ambiguity,
        "unchanged_text_records": unchanged,
        "non_jp_sources": non_jp_sources,
        "notes": notes,
        "h18_check": {"adult_confirmation": "project-confirmed all characters 18+", "h18_content_present": False},
        "independent_verify": {"status": "PENDING", "tool": str(ROOT / "dotabyss-rpg-vn-translator" / "work" / "verify_asset_translation.py")}
    }
    manifest = {
        "scene": SCENE,
        "status": qa_status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "paths": {
            "ja_json": str(JA_JSON),
            "en_json": str(EN_JSON),
            "source_asset": str(EN_ASSET),
            "output_asset": str(VI_ASSET),
            "work_dir": str(WORK),
            "focused_diff": str(DIFF),
            "qa_log": str(QA_LOG),
            "script": str(WORK / "apply_translation.py")
        },
        "source_metadata": {
            "sha256": sha256(EN_ASSET),
            "bytes": len(raw),
            "bom": bom,
            "newline": newline,
            "line_count": len(src_lines),
            "text_command_counts": dict(cmd_counts),
            "total_text_records": len(records)
        },
        "output_metadata": {
            "sha256": sha256(VI_ASSET),
            "bytes": len(vi_raw),
            "bom": vi_bom,
            "newline": vi_newline,
            "line_count": len(vi_lines),
            "text_command_counts": dict(Counter(cmd for _, cmd, _ in vi_records)),
            "total_text_records": len(vi_records)
        },
        "mapping_summary": {
            "ja_keys": len(ja),
            "en_values_blank": all(v == "" for v in en.values()),
            "translated": len(applied),
            "unmatched": len(ambiguity) + len(missing_trans)
        },
        "independent_verify": {"status": "PENDING"}
    }
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": qa_status, "records": len(records), "translated": len(applied), "output": str(VI_ASSET), "qa_log": str(QA_LOG), "manifest": str(MANIFEST), "diff": str(DIFF)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
