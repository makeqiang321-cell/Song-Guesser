# -*- coding: utf-8 -*-
# SEO audit: per-page keyword focus + Google-quality proxy score (0-100).
# Run: python _seo_audit.py   (after the generators have written the pages)
import io, os, re, sys, json, glob
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
KW = ["song guessing game", "guess song", "heardle-style", "song guesser"]

# artist / genre / decade topics used for keyword-focus measurement
TOPICS = (["the weeknd","taylor swift","michael jackson","beyoncé","rihanna","drake","eminem",
  "kanye west","justin bieber","linkin park","lady gaga","bruno mars","adele","ariana grande",
  "billie eilish","ed sheeran","coldplay","bts","blackpink","g-dragon","david guetta","pitbull",
  "kendrick lamar","olivia rodrigo","lana del rey","maroon 5","shakira","travis scott",
  "sabrina carpenter","anuel aa","don toliver","tate mcrae","playboi carti","bad bunny","katy perry"]
  + ["pop","rock","hip-hop","r&b","k-pop","electronic","country","metal"]
  + ["1980s","1990s","2000s","2010s","2020s"])

def strip(s):
    return re.sub(r'<[^>]+>', ' ', s or '')

def find_topic(text):
    low = text.lower()
    for t in sorted(TOPICS, key=len, reverse=True):
        if t in low:
            return t
    return None

def pages():
    out = []
    for f in glob.glob(os.path.join(BASE, "**", "index.html"), recursive=True):
        if ".claude" in f or "node_modules" in f:
            continue
        out.append(f)
    return sorted(out)

def score(f):
    h = io.open(f, encoding="utf-8").read()
    rel = os.path.relpath(f, BASE).replace("\\", "/")
    title = re.search(r'<title>(.*?)</title>', h, re.S)
    title = strip(title.group(1)).strip() if title else ""
    md = re.search(r'<meta name="description" content="([^"]*)"', h)
    md = md.group(1) if md else ""
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    h2 = re.findall(r'<h2[^>]*>(.*?)</h2>', h, re.S)
    body = strip(re.sub(r'<script.*?</script>', ' ', h, flags=re.S))
    low = body.lower()
    words = len(body.split())
    topic = find_topic(title) or find_topic(h1[0] if h1 else "")

    sc = 0
    checks = []

    # 1. Title (12): length 40-70, brand + topic
    tl = len(title)
    t_ok = (40 <= tl <= 70) and "song guesser" in title.lower()
    t_topic = topic and topic in title.lower()
    sc += (6 if t_ok else (3 if tl >= 30 else 0)) + (6 if t_topic else 0)
    checks.append(("title", t_ok, t_topic, "%dch" % tl))

    # 2. Meta description (10): present, 70-160, has topic
    ml = len(md)
    m_ok = 70 <= ml <= 160
    m_topic = topic and topic.lower() in md.lower()
    sc += (5 if md else 0) + (3 if m_ok else 0) + (2 if m_topic else 0)
    checks.append(("meta", bool(md), m_ok, "%dch" % ml))

    # 3. H1 (10): exactly one, brand + topic
    h1n = len(h1)
    h1_ok = h1n == 1 and "song guesser" in strip(h1[0]).lower() if h1 else False
    h1_topic = h1 and topic and topic in strip(h1[0]).lower()
    sc += (4 if h1n == 1 else (2 if h1n else 0)) + (4 if h1_ok else 0) + (2 if h1_topic else 0)
    checks.append(("h1", h1n == 1, h1_ok, "%d" % h1n))

    # 4. Heading structure (5): has >=4 h2
    sc += min(5, len(h2) // 2)
    checks.append(("h2", len(h2) >= 4, False, "%d" % len(h2)))

    # 5. Keyword focus (20): topic density + the 4 target keywords
    focus_term = topic if topic else "song guessing game"
    tc = low.count(focus_term)
    density = tc / max(1, words)
    den_ok = 0.004 <= density <= 0.04
    kw_hits = sum(1 for k in KW if k in low)
    sc += (8 if den_ok else (4 if density > 0 else 0)) + (8 if kw_hits >= 3 else (4 if kw_hits >= 1 else 0)) + (4 if kw_hits == 4 else 0)
    checks.append(("focus", den_ok, kw_hits >= 3, "%.2f%%/%d" % (density * 100, kw_hits)))

    # 6. Content depth (15): word count
    sc += 15 if words >= 700 else (10 if words >= 450 else (5 if words >= 250 else 0))
    checks.append(("depth", words >= 700, words >= 450, "%dw" % words))

    # 7. JSON-LD (12): BreadcrumbList + FAQPage, FAQ matches visible
    has_bc = '"BreadcrumbList"' in h or '"@type":"BreadcrumbList"' in h or '"@type": "BreadcrumbList"' in h
    has_faq = '"FAQPage"' in h or '"@type":"FAQPage"' in h or '"@type": "FAQPage"' in h
    sc += (6 if has_bc else 0) + (6 if has_faq else 0)
    checks.append(("jsonld", has_bc, has_faq, ""))

    # 8. Internal link (6): lowercase 'song guesser' -> '/'
    has_link = re.search(r'>\s*song guesser\s*</a>', h, re.I) is not None
    sc += 6 if has_link else 0
    checks.append(("link", has_link, False, ""))

    # 9. Readability (5): avg sentence length < 26
    sents = [s for s in re.split(r'[.!?]', body) if len(s.split()) > 3]
    avg = (words / max(1, len(sents)))
    sc += 5 if avg < 26 else (3 if avg < 34 else 0)
    checks.append(("read", avg < 26, avg < 34, "%.0fw" % avg))

    # 10. Uniqueness (5, filled in by caller via dup set) — default 5
    checks.append(("dup", None, None, ""))
    return dict(rel=rel, topic=topic, words=words, score=sc, checks=checks, body=body)

def main():
    rows = []
    seen_ps = {}
    for f in pages():
        r = score(f)
        rows.append(r)
    # uniqueness: exact-duplicate <p> sentences across pages
    all_ps = {}
    for r in rows:
        ps = re.findall(r'<p>(.*?)</p>', r['body'], re.S)
        for p in ps:
            p = re.sub(r'\s+', ' ', strip(p)).strip()
            if len(p) > 40:
                all_ps.setdefault(p, set()).add(r['rel'])
    for r in rows:
        # recompute dup penalty: count sentences this page shares with others
        ps = re.findall(r'<p>(.*?)</p>', r['body'], re.S)
        shared = sum(1 for p in ps if len(re.sub(r'\s+',' ',strip(p)).strip()) > 40 and len(all_ps.get(re.sub(r'\s+',' ',strip(p)).strip(), set())) > 1)
        r['dup_shared'] = shared
        r['score'] -= min(5, shared)
        # fix the dup check label
        r['checks'] = [(a, (False if shared == 0 else True) if a == 'dup' else b,
                         None if a == 'dup' else c, ("%d" % shared) if a == 'dup' else d)
                       for (a, b, c, d) in r['checks']]

    rows.sort(key=lambda r: -r['score'])
    print("%-46s %-16s %5s %6s" % ("page", "topic", "words", "score"))
    print("-" * 78)
    for r in rows:
        print("%-46s %-16s %5d %6d" % (r['rel'], r['topic'] or '-', r['words'], r['score']))
    print("-" * 78)
    tot = len(rows)
    avg = sum(r['score'] for r in rows) / max(1, tot)
    lo = [r for r in rows if r['score'] < 75]
    print("pages=%d  avg=%.0f  below75=%d" % (tot, avg, len(lo)))
    if lo:
        print("\nWeakest pages:")
        for r in lo:
            bad = [(a, d) for a, b, c, d in r['checks'] if b is False or c is False]
            print("  %-40s %3d  %s" % (r['rel'], r['score'], bad))

if __name__ == "__main__":
    main()
