from pathlib import Path
import hashlib, json, re

scene = "hmn_10030100002"
en = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10030100002.txt")
vi = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10030100002.txt")
qa_path = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10030100002_full/qa_log.json")
manifest_path = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10030100002_full/manifest.json")

def dec(b):
    return b.decode("utf-8-sig" if b.startswith(b"\xef\xbb\xbf") else "utf-8")

def body(line):
    return line.rstrip("\r\n")

def newline_kind(data):
    return "CRLF" if b"\r\n" in data else "LF"

def tags(s):
    return re.findall(r"<[^>]+>", s)

def placeholders(s):
    return re.findall(r"%(?:\d+\$)?[sd]|\{[^{}]+\}|\$\{[^{}]+\}|\\[nrt]|%%", s)

ed = en.read_bytes(); vd = vi.read_bytes()
el = dec(ed).splitlines(True); vl = dec(vd).splitlines(True)
rec = {"title": 1, "message": 2, "messageTextUnder": 2, "messageTextCenter": 2}
result = {
    "scene": scene,
    "status": "PASS",
    "en_sha256": hashlib.sha256(ed).hexdigest(),
    "vi_sha256": hashlib.sha256(vd).hexdigest(),
    "line_count_en": len(el),
    "line_count_vi": len(vl),
    "bom_match": ed.startswith(b"\xef\xbb\xbf") == vd.startswith(b"\xef\xbb\xbf"),
    "newline_en": newline_kind(ed),
    "newline_vi": newline_kind(vd),
    "candidate_records": 0,
    "changed_text_records": 0,
    "delimiter_mismatches": [],
    "technical_mismatches": [],
    "tag_mismatches": [],
    "placeholder_mismatches": [],
    "ascii_commas_in_text": [],
    "unchanged_text_records": [],
    "targeted_english_leftovers": [],
    "qa_log_status": None,
    "qa_log_blockers": None,
}
patterns = [r"\bHoney\b", r"\bhoney\b", r"\bgold\b", r"\bCommander\b", r"\bFrontline\b", r"\bAuction\b", r"\bHall\b", r"\bAncient\b", r"\bOrb\b", r"\bGuardian\b", r"\bStone\b", r"\bLantern\b", r"\bUgh\b", r"\bTch\b", r"\bYes\b", r"\bNo\b", r"\bOh dear\b", r"\bThank you\b", r"\bWait\b", r"\bbid\b", r"\bauction\b", r"\bmonster\b"]

if len(el) != len(vl): result["status"] = "FAIL"
for i, (a, b) in enumerate(zip(el, vl), 1):
    ab = body(a); vb = body(b)
    ap = ab.split(','); bp = vb.split(',')
    idx = rec.get(ap[0])
    if idx is None or len(ap) <= idx:
        if ap != bp:
            result["technical_mismatches"].append(i)
        continue
    result["candidate_records"] += 1
    if ab.count(',') != vb.count(','):
        result["delimiter_mismatches"].append(i); continue
    if len(bp) <= idx or ap[0] != bp[0] or ap[:idx] + ap[idx+1:] != bp[:idx] + bp[idx+1:]:
        result["technical_mismatches"].append(i)
    if ap[idx] != bp[idx]:
        result["changed_text_records"] += 1
    else:
        result["unchanged_text_records"].append(i)
    if tags(ap[idx]) != tags(bp[idx]):
        result["tag_mismatches"].append(i)
    if placeholders(ap[idx]) != placeholders(bp[idx]):
        result["placeholder_mismatches"].append(i)
    if ',' in bp[idx]:
        result["ascii_commas_in_text"].append(i)
    vt = re.sub(r"<[^>]+>", " ", bp[idx])
    hits = [p for p in patterns if re.search(p, vt)]
    if hits:
        result["targeted_english_leftovers"].append({"line": i, "patterns": hits, "text": bp[idx]})

qa = json.loads(qa_path.read_text(encoding="utf-8"))
result["qa_log_status"] = qa.get("qa_status")
result["qa_log_blockers"] = len(qa.get("blockers", []))
if any(result[k] for k in ["delimiter_mismatches", "technical_mismatches", "tag_mismatches", "placeholder_mismatches", "ascii_commas_in_text", "unchanged_text_records", "targeted_english_leftovers"]):
    result["status"] = "FAIL"
if not result["bom_match"] or result["newline_en"] != result["newline_vi"] or result["line_count_en"] != result["line_count_vi"] or result["qa_log_status"] != "PASS" or result["qa_log_blockers"] != 0:
    result["status"] = "FAIL"

# Add to QA log and manifest for audit trail.
qa["independent_verify"] = result
qa["qa_status"] = result["status"]
qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["independent_verify"] = result
manifest["qa_status"] = result["status"]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
