# -*- coding: utf-8 -*-
"""Per-page Google quality score: technical SEO (seo-auditor plugin) + content
quality (helpful-content heuristics mapped to this site's copy constraints)."""
import io, os, re, sys, subprocess, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
AUDIT = r"C:\Users\Administrator\.claude\skills\seo-auditor\resources\audit_rules.js"
KW = ("heardle-style song guessing game", "song guessing game", "guess song")


def body_text(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    return re.sub(r"<[^>]+>", " ", h)


def content_score(h):
    txt = body_text(h).lower()
    words = txt.split()
    s = 0

    # 1. required keywords (30)
    for kw in KW:
        s += 10 if kw in txt else 0

    # 2. FAQ depth + JSON-LD match (25)
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    faq_js = visible = 0
    for block in ld:
        if '"@type":"FAQPage"' in block or '"@type": "FAQPage"' in block:
            faq_js = len(re.findall(r'"@type":\s*"Question"', block))
    visible = len(re.findall(r"<details", h))
    if faq_js >= 5:
        s += 10
    elif faq_js > 0:
        s += 5
    if faq_js > 0 and faq_js == visible:
        s += 15
    elif faq_js > 0:
        s += 8

    # 3. BreadcrumbList (10)
    if '"@type":"BreadcrumbList"' in h or '"@type": "BreadcrumbList"' in h:
        s += 10

    # 4. content depth (25)
    w = len(words)
    s += 25 if w >= 700 else 20 if w >= 500 else 15 if w >= 350 else 10 if w >= 250 else 5

    # 5. anti-stuffing (10)
    def density(phrase):
        c = txt.count(phrase)
        return c * len(phrase.split()) / max(1, w) * 100
    gs = density("guessable song")   # matches "guessable song" and "guessable songs"
    sg = density("song guessing game")
    s += 5 if gs <= 2.0 else 3 if gs <= 3.0 else 1
    s += 5 if sg <= 2.5 else 3 if sg <= 4.0 else 1

    return s, w, faq_js, visible


def tech_score(path):
    out = subprocess.run(["node", AUDIT, path], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    m = re.search(r"SCORE: (\d+)/\d+ \((\d+)%\) - Grade ([A-F])", out)
    return int(m.group(2)) if m else 0


pages = []
for root, _, files in os.walk(BASE):
    if "_" in root.split(os.sep)[-1] or "node_modules" in root:
        continue
    if "index.html" in files:
        pages.append(os.path.join(root, "index.html"))

rows = []
for p in sorted(pages):
    rel = os.path.relpath(p, BASE).replace("\\", "/")
    h = io.open(p, encoding="utf-8").read()
    cs, w, faq_js, vis = content_score(h)
    ts = tech_score(p)
    combined = round(0.5 * ts + 0.5 * cs)
    grade = "A" if combined >= 90 else "B" if combined >= 80 else "C" if combined >= 70 else "D"
    kind = ("artist" if "/song-guesser-artists/" in rel and rel.count("/") == 2 else
            "genre" if "/guessable-songs/" in rel and rel.count("/") == 2 else
            "decade" if "/guess-song-decades/" in rel and rel.count("/") == 2 else
            "hub" if rel.count("/") == 1 else "page")
    rows.append((kind, rel, ts, cs, combined, grade, w, faq_js, vis))

print("KIND\tPAGE\tTECH\tCONTENT\tGOOGLE\tGRADE\tWORDS\tFAQ_JS/VIS")
for kind, rel, ts, cs, combined, grade, w, fjs, vis in rows:
    print("%s\t%s\t%d\t%d\t%d\t%s\t%d\t%d/%d" % (kind, rel, ts, cs, combined, grade, w, fjs, vis))

# aggregate
from collections import defaultdict
agg = defaultdict(lambda: [0, 0, 0])
for kind, *_rest, combined in [(r[0], r[4]) for r in rows]:
    pass
by_kind = defaultdict(list)
for kind, rel, ts, cs, combined, grade, w, fjs, vis in rows:
    by_kind[kind].append(combined)
print("\nAVERAGE GOOGLE SCORE BY TYPE:")
for k, v in sorted(by_kind.items()):
    print("  %-7s n=%2d  avg=%d  min=%d  max=%d" % (k, len(v), round(sum(v)/len(v)), min(v), max(v)))
