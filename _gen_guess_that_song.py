# -*- coding: utf-8 -*-
"""Generate /guess-that-song/ — a standalone, indexable SEO landing page for the
"guess that song" search intent. Clones the Music Quiz audio tool verbatim, then lays out
the content in search-intent order: What Is -> How To Play -> Why It Works -> FAQ (PAA) ->
Related (internal links) -> CTA. Includes HowTo + FAQPage structured data so the page can
earn rich results. Not linked from header/footer (stays off the homepage) but indexable
via sitemap. Writes CRLF to match core.autocrlf=true."""
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
               '<h1 id="songspot-heading">Guess That Song — Free Online Song Guessing Game</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>Guess That Song is a free online song guessing game. Press play, hear a tiny clip of a real song, and name the track from four answers — A, B, C or D. Unlimited rounds, no signup, no download.</p>',
               shell, flags=re.S)

# --- header: this page is not in the nav, so nothing is "active" ---
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>',
                        '<a class="songspot-site-nav-link" href="/songless/">Songless</a>')

FAQ = [
    ("What is guess that song?",
     "Guess That Song is a free online song guessing game. You hear a tiny clip of a real song — starting at 0.1 seconds — and pick the correct title from four answers before the clip grows."),
    ("How do you play guess that song?",
     "Hit play to hear a 0.1-second clip, then tap A, B, C or D. A wrong pick lengthens the clip — 0.5s, 2s, 8s, then 15s — until you name the track."),
    ("Is guess that song free?",
     "Yes. It's free in any browser — no signup, no download, no daily limit. Play unlimited rounds on desktop or phone."),
    ("Can you really guess a song from a few seconds?",
     "Yes. Familiar music is recognized almost instantly, so a fraction of a second is often enough to name a song you know — the fewer seconds you need, the better you know it."),
    ("What is the game like Heardle?",
     "Heardle gave you one song a day and six typed guesses. Guess That Song keeps the name-before-the-clip-grows idea but is unlimited, with four choices and no daily lockout."),
    ("Can I pick the songs or genre?",
     "Yes. Filter the pool by genre, decade or artist, choose a difficulty, and set your own starting clip length with the Guess after controls."),
]

STEPS = [
    ("Hit play", "Hit play and a 0.1-second sliver of a real song starts."),
    ("Tap the title", "Four titles appear — A, B, C or D. Tap the one that matches the sound."),
    ("Grow the clip on a miss", "A wrong pick lengthens the clip to 0.5s, 2s, 8s, then 15s, until you get it."),
]

SEO = '''
<section class="songspot-seo">
  <section id="what-is-guess-that-song" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">Free online &#183; no signup &#183; unlimited rounds</p>
      <h2>What Is Guess That Song?</h2>
      <p>Guess That Song is a free online game that plays you a sliver of a real song and asks you to name it. Every round starts at 0.1 seconds — a single drum hit, a breath, a chord attack — and you pick the correct title from four answers before the clip grows.</p>
      <p>It's the name-that-tune idea behind Heardle, stripped to its fastest form. No typing, no lyrics, no daily lockout — just your ear against four options, one song after another.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>4</dt><dd>answers per song</dd></div>
      <div><dt>&#8734;</dt><dd>unlimited rounds</dd></div>
    </dl>
  </section>

  <section id="how-to-play-guess-that-song" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Three steps, one sliver</p>
      <h2>How to Play Guess That Song</h2>
      <p>Every round takes about ten seconds. Here's the whole flow.</p>
    </div>
    <ol class="songspot-how-grid">
''' + ''.join(
    '<li><span>%02d</span><span class="icon">&#9654;</span><h3>%s</h3><p>%s</p></li>\n' % (i + 1, n, t)
    for i, (n, t) in enumerate(STEPS)
) + '''    </ol>
  </section>

  <section id="why-guess-that-song-works" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Built to beat a one-a-day game</p>
      <h2>Why Guess That Song Works</h2>
      <p>Most song guessing games ration you. This one doesn't.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#128293;</span><h3>Free and unlimited</h3><p>No signup, no download, no daily limit. Play one round or a hundred — the catalog keeps serving songs.</p></article>
      <article><span class="icon">&#128220;</span><h3>Four choices, no typing</h3><p>Every answer is a tap on A, B, C or D. It works on a phone one-handed and on a desktop at full speed.</p></article>
      <article><span class="icon">&#127919;</span><h3>Five difficulty lanes</h3><p>Set the difficulty from Chill to Impossible, and start each clip at 0.1s, 0.5s, 2s, 8s or 15s with the Guess after controls.</p></article>
      <article><span class="icon">&#127911;</span><h3>Genre, decade or artist</h3><p>Narrow the pool to a single genre, decade or artist so every round draws from the songs you actually know.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Frequently Asked Questions About Guess That Song</h2>
      <p>The questions people search before they press play.</p>
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
        <li><a href="/music-quiz/">Music Quiz</a> — the classic free music quiz with difficulty and genre filters</li>
        <li><a href="/songless/">Songless</a> — guess the song from 0.1 seconds, no lyrics, no titles</li>
        <li><a href="/music-guessing-game/">Music Guessing Game</a> — a name-that-tune blind test across every genre</li>
        <li><a href="/disney-guess-the-song/">Disney Guess the Song</a> — name Disney tunes from Snow White to Encanto</li>
        <li><a href="/guess-the-song-in-0-1-second/">Guess the Song in 0.1 Second</a> — the shortest-clip mode</li>
      </ul>
    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">Unlimited. Free. One tap.</p>
    <h2>Ready to guess that song?</h2>
    <p>Press play above and see how short a clip you can beat.</p>
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
    return '{"@context":"https://schema.org","@type":"HowTo","name":"How to Play Guess That Song","description":"Play the free online song guessing game in three steps: hear a 0.1-second clip, pick the song from four choices, and reveal a longer clip if you miss.","totalTime":"PT1M","step":[' + steps + ']}'

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Guess That Song — Free Online Song Guessing Game</title>
<meta name="description" content="Guess that song from a fraction of a second. Free online song guessing game — hear a tiny clip, pick the track from 4 choices, unlimited rounds, no signup." />
<link rel="canonical" href="https://www.songguesser.co/guess-that-song/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Guess That Song — Free Online Song Guessing Game" />
<meta property="og:description" content="Hear a sliver, name the track from four choices. Free online song guessing game — unlimited rounds, no signup." />
<meta property="og:url" content="https://www.songguesser.co/guess-that-song/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Guess That Song — Free Online Song Guessing Game" />
<meta name="twitter:description" content="Hear a sliver, name the track from A, B, C or D. Free, no signup, unlimited rounds." />
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
{"@context":"https://schema.org","@type":"VideoGame","name":"Guess That Song","description":"A free online song guessing game where you hear a fraction of a second of a real song and name the track from four answers before the clip grows.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/guess-that-song/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
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
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Guess That Song","item":"https://www.songguesser.co/guess-that-song/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'guess-that-song')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote guess-that-song/index.html  (%d bytes)' % len(page))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'guess-that-song' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/guess-that-song/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has guess-that-song')
