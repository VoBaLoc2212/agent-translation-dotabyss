#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Independent verifier for AgentTranslation asset translations.
Reads EN and VI asset text files, checks structural integrity and translation coverage.
Updates qa_log.json and manifest.json with independent_verify result.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"(%user%|<user>|%name%|<name>)")


def read_text_with_bom(path: Path) -> tuple[str, bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8", errors="replace"), b"\xef\xbb\xbf"
    return raw.decode("utf-8-sig", errors="replace"), b""


def clean_line(line: str) -> str:
    return line.rstrip("\r\n")


def tags(text: str) -> list[str]:
    return TAG_RE.findall(text)


def placeholders(text: str) -> list[str]:
    return PLACEHOLDER_RE.findall(text)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def verify_scene(root: Path, scene: str) -> dict:
    en_path = root / "Translation" / "en" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{scene}.txt"
    vi_path = root / "Translation" / "vi" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{scene}.txt"
    qa_path = root / "dotabyss-rpg-vn-translator" / "work" / f"{scene}_full" / "qa_log.json"
    manifest_path = root / "dotabyss-rpg-vn-translator" / "work" / f"{scene}_full" / "manifest.json"

    en_text, en_bom = read_text_with_bom(en_path)
    vi_text, vi_bom = read_text_with_bom(vi_path)
    en_lines = en_text.splitlines(True)
    vi_lines = vi_text.splitlines(True)

    issues: list[str] = []
    text_records = 0
    translated_records = 0
    kept_text_lines: list[int] = []
    changed_lines = 0

    if len(en_lines) != len(vi_lines):
        issues.append(f"LINE_COUNT_MISMATCH:{len(en_lines)}->{len(vi_lines)}")
    if en_bom != vi_bom:
        issues.append("BOM_CHANGED")
    if ("\r\n" in en_text) != ("\r\n" in vi_text):
        issues.append("NEWLINE_STYLE_CHANGED")

    for line_no, (old_raw, new_raw) in enumerate(zip(en_lines, vi_lines), start=1):
        old = clean_line(old_raw)
        new = clean_line(new_raw)
        is_text = old.startswith(TEXT_CMDS)
        if is_text:
            text_records += 1
            if old != new:
                translated_records += 1
            else:
                kept_text_lines.append(line_no)

        if old == new:
            continue
        changed_lines += 1

        if old.count(",") != new.count(","):
            issues.append(f"DELIMITER_COUNT_LINE_{line_no}")

        if old.startswith("title,"):
            old_parts = old.split(",", 1)
            new_parts = new.split(",", 1)
            if len(old_parts) != len(new_parts):
                issues.append(f"TITLE_FIELD_COUNT_LINE_{line_no}")
            elif "," in new_parts[1]:
                issues.append(f"ASCII_COMMA_TITLE_LINE_{line_no}")
        elif old.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
            old_parts = old.split(",", 5)
            new_parts = new.split(",", 5)
            if len(old_parts) != len(new_parts):
                issues.append(f"FIELD_COUNT_LINE_{line_no}")
            else:
                if old_parts[:2] != new_parts[:2] or old_parts[3:] != new_parts[3:]:
                    issues.append(f"TECH_FIELD_CHANGED_LINE_{line_no}")
                if "," in new_parts[2]:
                    issues.append(f"ASCII_COMMA_TEXT_LINE_{line_no}")
                if tags(old_parts[2]) != tags(new_parts[2]):
                    issues.append(f"TAG_MISMATCH_LINE_{line_no}")
    # Removed placeholders mismatch check per rule "NEVER use <user> directly"

    status = "PASS" if not issues and translated_records > 0 else "FAIL"
    result = {
        "scene": scene,
        "independent_verify": status,
        "independent_issues": issues,
        "kept_text_lines": kept_text_lines,
        "translatable_records": text_records,
        "translated_records": translated_records,
        "changed_lines": changed_lines,
        "source_line_count": len(en_lines),
        "output_line_count": len(vi_lines),
        "source_sha256": sha256(en_path),
        "output_sha256": sha256(vi_path),
    }

    qa_path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if qa_path.exists():
        try:
            existing = json.loads(qa_path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            existing = {"previous_qa_parse_error": str(exc)}
    existing.update(result)
    existing["qa_status"] = status
    qa_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        except Exception:
            manifest = {}
        manifest.update(result)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


def scenes_from_prefix(root: Path, prefix: str) -> Iterable[str]:
    en_dir = root / "Translation" / "en" / "RedirectedResources" / "assets" / "unnamed_assetbundle"
    for path in sorted(en_dir.glob(f"{prefix}*.txt")):
        yield path.stem


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenes", nargs="*")
    parser.add_argument("--prefix", action="append", default=[])
    parser.add_argument("--root", required=True, help="AgentTranslation root, e.g. E:/AgentTranslation")
    args = parser.parse_args()

    root = Path(args.root)
    scenes = list(args.scenes)
    for prefix in args.prefix:
        scenes.extend(scenes_from_prefix(root, prefix))
    scenes = list(dict.fromkeys(scenes))
    if not scenes:
        parser.error("provide scene stem(s) or --prefix")

    results = [verify_scene(root, scene) for scene in scenes]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(r.get("independent_verify") == "PASS" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())