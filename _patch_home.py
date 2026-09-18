# -*- coding: utf-8 -*-
"""Rewrite homepage copy in songspot.org style (original words), and keep the
4 generators' find-target strings in sync so future regeneration still works."""
import io, re, json, os

ROOT = r"C:\Users\Administrator\Desktop\guess-the-song"
js = lambda s: json.dumps(s, ensure_ascii=False)

# ---------- new homepage head/hero strings ----------
NEW_TITLE = "<title>Guess the Song From a Short Clip | Song Guesser Music Quiz</title>"
NEW_DESC = '<meta name="description" content="Name the song from a 0.1-second clip in Song Guesser, a free Heardle-style song guessing game. Reveal 0.5s, 2s, 8s, 15s when you need more. Five difficulty levels, no app, no login." />'
NEW_OGT = '<meta property="og:title" content="Guess the Song From a Short Clip with Song Guesser" />'
NEW_OGD = '<meta property="og:description" content="Name the song from a 0.1-second clip. A free Heardle-style song guessing game with five difficulty levels and unlimited rounds." />'
NEW_TWT = '<meta name="twitter:title" content="Guess the Song From a Short Clip with Song Guesser" />'
NEW_H1 = '<h1 id="songspot-heading">Guess the Song From a Short Clip with Song Guesser</h1>'
NEW_HERO = '<p>Hear a tenth of a second of a real song, then name it before the clip grows. Song Guesser is a free Heardle-style song guessing game — five difficulty levels, no app and no login. The shorter the clip you beat, the sharper the round.</p>'
NEW_VG_DESC = "A free Heardle-style song guessing game where you name a track from a 0.1-second clip, then reveal longer clips when you need more."

# ---------- old homepage strings (literal em-dash) ----------
OLD = {
    "title": "<title>Song Guesser — Free Song Guessing Game | Guess the Song in 0.1 Seconds</title>",
    "desc": '<meta name="description" content="Play Song Guesser free in your browser: name a song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A song guessing game with 5 difficulty levels, no signup, no download." />',
    "ogt": '<meta property="og:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
    "ogd": '<meta property="og:description" content="Name the song from a 0.1-second clip. Free browser song guessing game with difficulty levels, genre filters and unlimited rounds." />',
    "twt": '<meta name="twitter:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
    "h1": '<h1 id="songspot-heading">Song Guesser — Guess the Song in 0.1 Seconds</h1>',
    "hero": '<p>The free song guesser — name a song from a 0.1-second clip. A song guessing game with no login and no app. Hear 0.1s, then 0.5s, 2s, 8s, 15s; the shorter the clip you beat, the sharper the guess.</p>',
    "vg": "A free browser song guessing game where you name a track from a 0.1-second clip, then reveal longer clips if you need more.",
}
NEW = {
    "title": NEW_TITLE,
    "desc": NEW_DESC,
    "ogt": NEW_OGT,
    "ogd": NEW_OGD,
    "twt": NEW_TWT,
    "h1": NEW_H1,
    "hero": NEW_HERO,
    "vg": NEW_VG_DESC,
}
MARK = {"title": "T_TITLE", "desc": "T_DESC", "ogt": "T_OGT", "ogd": "T_OGD",
        "twt": "T_TWT", "h1": "T_H1", "hero": "T_HERO", "vg": "T_VG"}

# ---------- FAQ (single source of truth: visible FAQ + JSON-LD) ----------
FAQ = [
    ("Is Song Guesser free to play?",
     "Yes — it runs free in any modern browser, with no paywall and no download. The only thing you have to do is press play."),
    ("How much of a song do I actually hear?",
     "A round opens on a tenth of a second. Every wrong guess or skip widens the clip to 0.5s, 2s, 8s, then 15s — more of the track only arrives when you ask for it."),
    ("Do I need an account or a streaming app?",
     "No. Song Guesser has no signup and no streaming login. Open the page on a phone or desktop and the first clip is ready."),
    ("Can I choose the difficulty or the music?",
     "Yes. Set a difficulty from Easy to Impossible and filter by genre or artist, and the next song loads with those settings."),
    ("Where does the music come from?",
     "The game uses short public song previews, so a round starts the moment you press play — nothing to install, nothing to queue."),
]

faq_html = '\n'.join(
    '<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a)
    for i, (q, a) in enumerate(FAQ))
faq_json = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' +
            ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (js(q), js(a))
                     for q, a in FAQ) + ']}')
faq_ld = '<script type="application/ld+json">\n' + faq_json + '\n</script>'

# ---------- new SEO section ----------
SEO = '''<section class="songspot-seo">
  <section id="what-is-song-guesser" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">Sound first, titles later</p>
      <h2>What Is Song Guesser?</h2>
      <p>Song Guesser is a browser game built on one idea — the front of a song is enough. Each round plays the first tenth of a second of a real track: a drum hit, a vocal breath, a synth stab, the room around the recording. Your job is to name the song before the clip gives any more away.</p>
      <p>There is no trivia, no dates and no artwork to lean on. You work from sound alone, typing the title the moment the recording clicks. It's a Heardle-style song guessing game, only faster — a sliver to start, and every longer reveal after that is yours to take or refuse.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the only clue you start with</dd></div>
      <div><dt>5</dt><dd>clip lengths from 0.1s to 15s</dd></div>
      <div><dt>15s</dt><dd>the full reveal, if you ask</dd></div>
    </dl>
  </section>

  <section id="how-to-play" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Three moves, one sliver</p>
      <h2>How does the guess-the-song game work?</h2>
      <p>Press play, hear what you get, and decide in the moment whether to answer now or ask for a little more of the track.</p>
    </div>
    <ol class="songspot-how-grid">
      <li><span>01</span><span class="icon">▶</span><h3>Listen to the sliver</h3><p>The first sound lasts a tenth of a second. Headphones help — a drum fill, a vocal breath or a single synth stab is often the whole clue you need.</p></li>
      <li><span>02</span><span class="icon">⌕</span><h3>Name the track</h3><p>Type part of the title and pick from the suggestions. A rhythm, a melody or a production texture can point you to the answer before the clip reveals it.</p></li>
      <li><span>03</span><span class="icon">⏭</span><h3>Widen only when stuck</h3><p>Wrong answer or skip? The clip steps to 0.5s, 2s, 8s, then 15s. Naming the song from the shortest clip is the whole point.</p></li>
    </ol>
  </section>

  <section id="recognition" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">An ear, not a search bar</p>
      <h2>Why can 0.1 seconds be enough?</h2>
      <p>A tenth of a second carries no lyric and no full melody, but a recording you know has a fingerprint. The attack of a snare, the grain of a voice, the size of the room, the exact timbre of a synth — any of these can fire the answer before you can put it into words. Longer clips only add what the first one hinted at: rhythm, then harmony, then the melody itself.</p>
      <p>That is why every round starts easy and lets you climb. New ears warm up on widely known hooks, then work toward rarer tracks as their recognition sharpens. Five difficulty levels mean a casual listener and a serious one can play the same <a href="#play">song guesser</a> without sharing the same catalog.</p>
    </div>
  </section>

  <section id="features" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Small clips, real replay value</p>
      <h2>Song Guesser Features</h2>
      <p>The name-that-tune loop, kept fast and focused, with control over how hard each round lands.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">🎵</span><h3>Reveals on your terms</h3><p>Open on a tenth of a second and grow the clip only when you ask.</p></article>
      <article><span class="icon">🎚️</span><h3>Easy to Impossible</h3><p>Five difficulty levels that change the pool, not the rules.</p></article>
      <article><span class="icon">🎛️</span><h3>Play your music</h3><p>Filter by genre or artist and guess the songs you already know.</p></article>
      <article><span class="icon">♾️</span><h3>No daily gate</h3><p>Free in the browser — unlimited rounds, no app, no login.</p></article>
      <article><span class="icon">🔍</span><h3>Type, don't spell</h3><p>A few letters bring up the title; you stay in the game instead of in a search.</p></article>
      <article><span class="icon">⚡</span><h3>Verdict in a beat</h3><p>See whether you nailed it and how early, then the next track loads.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Before you press play</p>
      <h2>Song Guesser FAQ</h2>
      <p>The short version, so your first clip isn't your first question.</p>
    </div>
    <div class="songspot-faq-list">
''' + faq_html + '''
    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">How little audio do you need?</p>
    <h2>Ready to guess the song in 0.1 seconds?</h2>
    <p>Press play and find out how much of a song your ear really needs.</p>
    <a href="#play">Start playing →</a>
  </section>
</section>

'''

# ---------- 1) rewrite index.html ----------
ip = os.path.join(ROOT, "index.html")
h = io.open(ip, encoding="utf-8").read()
for k in OLD:
    assert h.count(OLD[k]) == 1, ("index.html", k, h.count(OLD[k]))
    h = h.replace(OLD[k], NEW[k])
# FAQ JSON-LD (matches visible FAQ)
h, n = re.subn(r'<script type="application/ld\+json">\s*\{[^{]*"@type":"FAQPage".*?</script>',
               faq_ld, h, count=1, flags=re.S)
assert n == 1, "FAQPage JSON-LD swap %d" % n
# SEO section
start = h.index('<section class="songspot-seo">')
end = h.index('<footer class="songspot-site-footer">')
h = h[:start] + SEO + h[end:]
io.open(ip, "w", encoding="utf-8").write(h)
print("index.html rewritten:", len(h), "bytes")

# ---------- 2) sync marker constants in _gen_artists.py / _gen_pages.py ----------
for f in ("_gen_artists.py", "_gen_pages.py"):
    p = os.path.join(ROOT, f)
    src = io.open(p, encoding="utf-8").read()
    for k in OLD:
        m = MARK[k]
        pat = re.compile(re.escape(m) + r"\s*=\s*'[^']*'")
        src, n = pat.subn(lambda mm: m + " = " + repr(NEW[k]), src, count=1)
        assert n == 1, (f, k, n)
    io.open(p, "w", encoding="utf-8").write(src)
    print("synced", f)

# ---------- 3) sync hardcoded find-targets in _gen_about.py / _gen_howto.py ----------
for f in ("_gen_about.py", "_gen_howto.py"):
    p = os.path.join(ROOT, f)
    src = io.open(p, encoding="utf-8").read()
    for k in ("title", "desc", "ogt", "ogd", "twt"):
        old_lit = OLD[k]
        old_esc = old_lit.replace("—", "\\u2014")
        n = 0
        for o in (old_lit, old_esc):
            c = src.count(o)
            if c:
                src = src.replace(o, NEW[k])
                n += c
        assert n >= 1, (f, k, n)
    io.open(p, "w", encoding="utf-8").write(src)
    print("synced", f)

print("DONE")
