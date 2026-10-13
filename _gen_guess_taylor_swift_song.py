# -*- coding: utf-8 -*-
"""Generate /guess-the-taylor-swift-song/ — a standalone, indexable SEO landing page for
the "guess the taylor swift song" search intent. Clones the Music Quiz audio tool verbatim,
then lays out original Swift-specific copy in search-intent order: What Is -> How To Play ->
Guess by the Era (information gain) -> FAQ (PAA) -> Related (internal links) -> CTA.
Includes HowTo + FAQPage structured data. Not linked from header/footer (stays off the
homepage) but indexable via sitemap. Writes CRLF to match core.autocrlf=true."""
import io, os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)

mq = read(os.path.join(BASE, 'music-quiz', 'index.html'))

# --- clone chrome + tool shell verbatim from music-quiz ---
cs = mq.index('<style>') + len('<style>')
ce = mq.index('</style>', cs)
css = mq[cs:ce]

hs = mq.index('<header class="songspot-site-header">')
he = mq.index('</header>', hs) + len('</header>')
header = mq[hs:he]

ss = mq.index('<section class="songspot-shell"')
se = mq.index('<section class="songspot-seo">')
shell = mq[ss:se]

fs = mq.index('<footer class="songspot-site-footer">')
fe = mq.index('</footer>', fs) + len('</footer>')
footer = mq[fs:fe]

m = mq.index("document.querySelectorAll('.songspot-site-quiz-menu')")
djs = mq.rfind('<script>', 0, m)
dje = mq.index('</script>', m) + len('</script>')
dropdown_js = mq[djs:dje]

# --- rebrand shell hero ---
shell = re.sub(r'<h1 id="songspot-heading">.*?</h1>',
               '<h1 id="songspot-heading">Guess the Taylor Swift Song — Free Quiz for Swifties</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>Guess the Taylor Swift Song is Song Guesser\'s Swiftie test: hear a 0.1-second clip of a real Taylor Swift track, then pick the right title from four answers — A, B, C or D. From Debut to The Tortured Poets Department, every era is in the pool.</p>',
               shell, flags=re.S)

# --- header: this page is not in the nav, so nothing is "active" ---
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>',
                        '<a class="songspot-site-nav-link" href="/songless/">Songless</a>')

FAQ = [
    ("How do you guess the Taylor Swift song?",
     "Press play to hear a 0.1-second clip of a real Taylor Swift track, then tap A, B, C or D. A wrong pick reveals a longer clip — 0.5s, 2s, 8s, then 15s — until you name it."),
    ("What Taylor Swift eras are in the quiz?",
     "All 11 — from Debut (2006) through The Tortured Poets Department (2024). Fearless, Speak Now, Red, 1989, reputation, Lover, folklore, evermore and Midnights are all in the pool."),
    ("Do I need to know the lyrics to guess the song?",
     "No. You play by ear. The clip is pure sound — a strum, a synth stab, a piano chord — so you only need to recognize the track, not remember a single line."),
    ("Is the Taylor Swift song quiz free?",
     "Yes. Free in any browser, no signup, no download, no daily limit — play unlimited rounds on desktop or phone."),
    ("Can I play just one era or album?",
     "Yes. Use the filters to narrow the pool by decade or artist, and set your starting clip length with the Guess after controls."),
    ("How many albums does the quiz cover?",
     "Eleven studio albums plus the re-recorded Taylor's Version releases — Debut in 2006 through The Tortured Poets Department in 2024, so every round can surface a single or a deep cut."),
]

STEPS = [
    ("Press play", "Press play to hear a 0.1-second clip of a Taylor Swift track."),
    ("Name the song", "Four Taylor Swift titles appear — A, B, C or D. Tap the one you heard."),
    ("Reveal more when stuck", "A wrong pick reveals a longer clip — 0.5s, 2s, 8s, then 15s — until you get it."),
]

SEO = '''
<section class="songspot-seo">
  <section id="what-is-guess-the-taylor-swift-song" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">All 11 eras, one sliver</p>
      <h2>What Is Guess the Taylor Swift Song?</h2>
      <p>Guess the Taylor Swift Song is a free online quiz that plays you a sliver of a real Taylor Swift track and asks you to name it. Every round starts at 0.1 seconds — a breath, a strum, a synth stab — and you pick the right title from four answers before the clip grows.</p>
      <p>It covers the whole catalog, from the 2006 country debut to The Tortured Poets Department in 2024. No typing, no lyrics, no daily lockout — just your ear against four options, one track after another.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>11</dt><dd>eras in the pool</dd></div>
      <div><dt>4</dt><dd>answers per song</dd></div>
    </dl>
  </section>

  <section id="how-to-play" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Three steps, one sliver</p>
      <h2>How to Play Guess the Taylor Swift Song</h2>
      <p>Every round takes about ten seconds. Here's the whole flow.</p>
    </div>
    <ol class="songspot-how-grid">
''' + ''.join(
    '<li><span>%02d</span><span class="icon">&#9654;</span><h3>%s</h3><p>%s</p></li>\n' % (i + 1, n, t)
    for i, (n, t) in enumerate(STEPS)
) + '''    </ol>
  </section>

  <section id="guess-by-the-era" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Learn the tell, own the game</p>
      <h2>Guess Taylor Swift by the Era</h2>
      <p>Every era has its own sound. Once you can hear the tells, a sliver is usually enough.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127931;</span><h3>The Country Years · 2006–2010</h3><p>Debut, Fearless and Speak Now open on an acoustic strum, banjo and fiddle — a teenage voice over a bare guitar. "Tim McGraw", "Love Story", "Mine".</p></article>
      <article><span class="icon">&#128640;</span><h3>The Pop Pivot · 2012–2014</h3><p>Red and 1989 swap the fiddle for a dubstep drop ("I Knew You Were Trouble") and an 80s synth stab ("Blank Space").</p></article>
      <article><span class="icon">&#127911;</span><h3>The Dark Turn · 2017–2019</h3><p>reputation opens on a bass thump ("...Ready For It?"), Lover on a pastel synth ("Cruel Summer"). Dark to sweet in two albums.</p></article>
      <article><span class="icon">&#127932;</span><h3>The Folk Duet · 2020</h3><p>folklore and evermore are one piano chord and strings — "cardigan" and "willow" both start soft, sparse and deliberate.</p></article>
      <article><span class="icon">&#127769;</span><h3>Midnights · 2022</h3><p>Synth-pop with a late-night haze — "Anti-Hero" and "Lavender Haze" open on a moody, arpeggiated synth.</p></article>
      <article><span class="icon">&#9992;</span><h3>The Tortured Poets Department · 2024</h3><p>Soft rock and folk-pop, confessional from the first word — "Fortnight" and "Down Bad" open quiet and build.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Guess the Taylor Swift Song — FAQ</h2>
      <p>What Swifties search before they press play.</p>
    </div>
    <div class="songspot-faq-list">
''' + ''.join(
    '<details%s><summary>%s</summary><p>%s</p></details>\n' % (' open' if i == 0 else '', q, a)
    for i, (q, a) in enumerate(FAQ)
) + '''    </div>
  </section>

  <section id="related" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Keep playing</p>
      <h2>More Song Guessing Games</h2>
    </div>
    <div class="songspot-seo-copy">
      <ul>
        <li><a href="/guess-that-song/">Guess That Song</a> — the free online song guessing game across every genre</li>
        <li><a href="/music-quiz/">Music Quiz</a> — the classic free music quiz with difficulty and genre filters</li>
        <li><a href="/songless/">Songless</a> — guess the song from 0.1 seconds, no lyrics, no titles</li>
        <li><a href="/music-guessing-game/">Music Guessing Game</a> — a name-that-tune blind test across every decade</li>
        <li><a href="/disney-guess-the-song/">Disney Guess the Song</a> — name Disney tunes from Snow White to Encanto</li>
      </ul>
    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">All 11 eras. One tap.</p>
    <h2>Ready to name the Taylor Swift song?</h2>
    <p>Press play above and see how short a clip a real Swiftie needs.</p>
    <a href="#play">Start guessing &rarr;</a>
    <a class="songspot-cta-home" href="/">Back to the main song guesser</a>
  </section>
</section>
'''

def faq_schema():
    items = ','.join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (json.dumps(q), json.dumps(a))
        for q, a in FAQ)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + items + ']}'

def howto_schema():
    steps = ','.join(
        '{"@type":"HowToStep","name":%s,"text":%s}' % (json.dumps(n), json.dumps(t)) for n, t in STEPS)
    return '{"@context":"https://schema.org","@type":"HowTo","name":"How to Play Guess the Taylor Swift Song","description":"Play the free Taylor Swift song guessing quiz in three steps: hear a 0.1-second clip, pick the song from four choices, and reveal a longer clip if you miss.","totalTime":"PT1M","step":[' + steps + ']}'

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Guess the Taylor Swift Song — Free Quiz for Swifties</title>
<meta name="description" content="Guess the Taylor Swift song from a fraction of a second. Hear a tiny clip and name the track from four choices across all 11 eras — free, no signup." />
<link rel="canonical" href="https://www.songguesser.co/guess-the-taylor-swift-song/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Guess the Taylor Swift Song — Free Quiz for Swifties" />
<meta property="og:description" content="Hear a sliver, name the Taylor Swift track from four choices. All 11 eras, free and unlimited." />
<meta property="og:url" content="https://www.songguesser.co/guess-the-taylor-swift-song/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Guess the Taylor Swift Song — Free Quiz for Swifties" />
<meta name="twitter:description" content="Hear a sliver, name the track from A, B, C or D. All 11 eras, free, no signup." />
<meta property="og:image" content="https://www.songguesser.co/images/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:image" content="https://www.songguesser.co/images/og.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;1,700;1,800&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
''' + css + '''</style>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"VideoGame","name":"Guess the Taylor Swift Song","description":"A free online quiz where you hear a fraction of a second of a Taylor Swift track and name it from four answers before the clip grows.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/guess-the-taylor-swift-song/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>
<script type="application/ld+json">
''' + faq_schema() + '''
</script>
<script type="application/ld+json">
''' + howto_schema() + '''
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Guess the Taylor Swift Song","item":"https://www.songguesser.co/guess-the-taylor-swift-song/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'guess-the-taylor-swift-song')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote guess-the-taylor-swift-song/index.html  (%d bytes)' % len(page))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'guess-the-taylor-swift-song' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/guess-the-taylor-swift-song/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has guess-the-taylor-swift-song')
