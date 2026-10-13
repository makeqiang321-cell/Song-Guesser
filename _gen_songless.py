# -*- coding: utf-8 -*-
"""Generate the Songless Unlimited page (/songless/) as a verbatim clone of the Music Quiz
audio tool (play key, 0.1s-15s timeline, guess-after seconds chips, volume, difficulty,
filters, A/B/C/D options), reusing decades.js + mcq.js. Only the page chrome + landing
copy + FAQ are rebranded to Songless Unlimited. Writes CRLF to match core.autocrlf=true."""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)

mq = read(os.path.join(BASE, 'music-quiz', 'index.html'))

# --- reuse chrome + tool shell verbatim from music-quiz ---
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
               '<h1 id="songspot-heading">Songless Unlimited — Guess the Song from a 0.1s Clip</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>Songless Unlimited is Song Guesser\'s unlimited multiple-choice mode: hear a 0.1-second clip of a real song, then pick the right title from four answers — A, B, C or D — round after round, with no daily limit.</p>',
               shell, flags=re.S)

# --- adapt header: Songless active, Music Quiz inactive ---
header = header.replace('<a class="songspot-site-nav-link" href="/songless/">Songless</a>', '')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>', '')
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace(
    '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>',
    '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>\n      '
    '<a class="songspot-site-nav-link active" href="/songless/">Songless</a>')

# --- footer: ensure Songless present once (idempotent) ---
footer = footer.replace('<a href="/songless/">Songless</a>', '')
footer = footer.replace(
    '<a href="/music-quiz/">Music Quiz</a>',
    '<a href="/music-quiz/">Music Quiz</a><a href="/songless/">Songless</a>')

FAQ = [
    ("What is Songless Unlimited?",
     "Songless Unlimited is Song Guesser's unlimited multiple-choice song quiz. You hear a 0.1-second clip of a real song, then pick the right title from four answers — A, B, C or D — with no daily limit and no song cap."),
    ("Does Songless Unlimited play audio?",
     "Yes. Every round opens with a real 0.1-second clip. A wrong pick reveals a longer clip — 0.5s, 2s, 8s, then 15s — until you name the song or run out of reveals."),
    ("How do the seconds work?",
     "The clip length is the difficulty inside each round. You start at 0.1s and guess as early as you can; the Guess after controls let you pick 0.1s, 0.5s, 2s, 8s or 15s as your starting point."),
    ("What difficulty levels are there?",
     "Easy to Impossible. Difficulty changes the song pool, not the rules — Easy draws from a small set of widely known hooks, and Impossible pulls from the full catalog."),
    ("Can I filter the songs?",
     "Yes. Narrow the library to one genre, one decade or a single artist, and the unlimited rounds keep drawing from that slice until you clear it."),
    ("Is it really unlimited?",
     "Yes. No daily gate, no login and no song cap — guess song after song for as long as you like, free in the browser."),
]

SEO = '''
<section class="songspot-seo">
  <section id="what-is-songless" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">Hear it, name it, keep going</p>
      <h2>What Is Songless Unlimited?</h2>
      <p>Songless Unlimited is a multiple-choice song quiz with no daily gate: hear a 0.1-second clip of a real song, then tap the right title from four answers — A, B, C or D. No typing, just your ear against four options.</p>
      <p>The name is the promise — no daily gate, no song cap, no reset waiting at midnight. You guess song after song from the shortest clip you can manage, and the library never runs dry.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>4</dt><dd>answers per round</dd></div>
      <div><dt>&infin;</dt><dd>unlimited rounds</dd></div>
    </dl>
  </section>

  <section id="how-to-play" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Three moves, one sliver</p>
      <h2>How to Play Songless Unlimited</h2>
      <p>Press play, hear whatever tenth of a second you get, and decide on the spot: tap now, or reveal a little more of the track.</p>
    </div>
    <ol class="songspot-how-grid">
      <li><span>01</span><span class="icon">&#9654;</span><h3>Hear the clip</h3><p>A tenth of a second of a real song plays once — that sliver is the entire clue.</p></li>
      <li><span>02</span><span class="icon">A</span><h3>Pick A, B, C or D</h3><p>Four titles appear, one correct. Tap your pick and it turns green the moment you land it.</p></li>
      <li><span>03</span><span class="icon">&#9197;</span><h3>Reveal only when stuck</h3><p>A wrong pick stretches the clip to 0.5s, 2s, 8s, then 15s, so the answer arrives only when you need it.</p></li>
    </ol>
  </section>

  <section id="tips" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">An ear, not a search bar</p>
      <h2>Tips to name more songs in 0.1 seconds</h2>
      <p>Recognition is a fingerprint. These four habits turn a tenth of a second into an answer.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127911;</span><h3>Listen for the attack</h3><p>The first strike of a drum, a breath at the mic, the grain of a voice — that is often the whole clue.</p></article>
      <article><span class="icon">&#127925;</span><h3>Hear it in your head</h3><p>Replay the melody the sliver sits on before you look at the four choices. The tune usually arrives first.</p></article>
      <article><span class="icon">&#127908;</span><h3>Let the artist break the tie</h3><p>Every choice shows its title with the artist. If two titles feel equally right, the artist is the giveaway.</p></article>
      <article><span class="icon">&#9889;</span><h3>Trust the first instinct</h3><p>Recognition is fast and mostly correct. Over-thinking a sliver is how you talk yourself out of a right answer.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Songless Unlimited — FAQ</h2>
      <p>The questions people ask before an unlimited run.</p>
    </div>
    <div class="songspot-faq-list">
''' + ''.join(
    '<details%s><summary>%s</summary><p>%s</p></details>\n' % (' open' if i == 0 else '', q, a)
    for i, (q, a) in enumerate(FAQ)
) + '''    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">No daily gate. No song cap.</p>
    <h2>Ready to run Songless Unlimited?</h2>
    <p>Press play above and name the song from the sliver — round after round, no limit.</p>
    <a href="#play">Start playing &rarr;</a>
    <a class="songspot-cta-home" href="/">Back to song guesser</a>
  </section>
</section>
'''

def faq_schema():
    items = ','.join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a)
        for q, a in FAQ)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + items + ']}'

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Songless Unlimited — Guess the Song in 0.1 Seconds</title>
<meta name="description" content="Songless Unlimited is a free unlimited song guessing game. Hear a 0.1-second clip and pick the song from four answers — no daily limit, no signup." />
<link rel="canonical" href="https://www.songguesser.co/songless/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Songless Unlimited — Guess the Song in 0.1 Seconds" />
<meta property="og:description" content="Hear a 0.1-second clip, pick the song from four answers. A free unlimited song guessing game with no daily limit." />
<meta property="og:url" content="https://www.songguesser.co/songless/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Songless Unlimited — Guess the Song in 0.1 Seconds" />
<meta name="twitter:description" content="Hear a 0.1-second clip, pick A, B, C or D. Free, unlimited, no signup." />
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
{"@context":"https://schema.org","@type":"VideoGame","name":"Songless Unlimited","description":"A free unlimited multiple-choice song guessing game where you hear a 0.1-second clip and pick the song title from four answers.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/songless/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>
<script type="application/ld+json">
''' + faq_schema() + '''
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Songless Unlimited","item":"https://www.songguesser.co/songless/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'songless')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote songless/index.html  (%d bytes)' % len(page))

# --- add the Songless nav + footer link to every other page (idempotent) ---
nav_pattern = re.compile(r'(<a class="songspot-site-nav-link[^"]*" href="/music-quiz/">Music Quiz</a>)')
nav_rep = r'\1\n      <a class="songspot-site-nav-link" href="/songless/">Songless</a>'
foot_pattern = re.compile(r'(<a href="/song-quiz/">Song Quiz</a><a href="/music-quiz/">Music Quiz</a>)')
foot_rep = r'\1<a href="/songless/">Songless</a>'
changed_nav = changed_foot = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        if 'songless' in p:
            continue
        s = read(p)
        s2 = s
        if 'href="/songless/"' not in s2:
            s2, n = nav_pattern.subn(nav_rep, s2)
            if n == 1:
                changed_nav += 1
        if '<a href="/songless/">Songless</a>' not in s2:
            s2, n = foot_pattern.subn(foot_rep, s2)
            if n == 1:
                changed_foot += 1
        if s2 != s:
            write(p, s2)
print('nav link added to %d pages, footer link added to %d pages' % (changed_nav, changed_foot))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'songless' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/songless/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has songless')
