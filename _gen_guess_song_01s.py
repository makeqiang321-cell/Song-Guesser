# -*- coding: utf-8 -*-
"""Generate /guess-the-song-in-0-1-second/ — a standalone, indexable SEO page targeting
the "guess the song in 0.1 second" intent. Clones the Music Quiz audio tool verbatim, but
the landing copy is written fresh (not from the music-guessing-game or Disney template):
the "0.1-second rule", the reveal ladder, and a transient-recognition guide, for original
information gain. Not linked from header/footer, so it stays off the homepage but stays
indexable via sitemap. Writes CRLF to match core.autocrlf=true."""
import io, os, re

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
               '<h1 id="songspot-heading">Guess the Song in 0.1 Second — Name the Track from a Sliver</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>Guess the Song in 0.1 Second is Song Guesser\'s shortest mode: hear a tenth-of-a-second clip of a real song, then pick the right title from four answers — A, B, C or D. No typing, no lyrics, just one sound and your memory.</p>',
               shell, flags=re.S)

# --- header: this page is not in the nav, so nothing is "active" ---
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>',
                        '<a class="songspot-site-nav-link" href="/songless/">Songless</a>')

FAQ = [
    ("Can you really guess a song from 0.1 seconds?",
     "Yes. Your brain recognizes familiar music in a fraction of a second, so a tenth of a second is often enough to name a song you know well — and this game proves it."),
    ("How does the 0.1 second song game work?",
     "You hear a 0.1-second clip of a real song, then pick the right title from four answers — A, B, C or D. A wrong pick reveals a longer clip until you get it."),
    ("What clip lengths are there?",
     "Five — 0.1, 0.5, 2, 8 and 15 seconds. You start at 0.1s, and each wrong answer moves you one rung up the ladder."),
    ("Why is 0.1 seconds enough to guess?",
     "Because recognition is instant. You don't need the chorus — a drum hit, a breath or the first chord is often enough to recall a song you've heard before."),
    ("Is the 0.1 second song game free?",
     "Yes. Free in the browser, no signup, no download, no daily limit."),
    ("Can I set the starting length or pick a genre?",
     "Yes. Use the Guess after controls to start at any length, and the filters to narrow the pool by genre, decade or artist."),
]

SEO = '''
<section class="songspot-seo">
  <section id="guess-the-song-in-01-second" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">A tenth of a second. That's all you get.</p>
      <h2>Guess the Song in 0.1 Second</h2>
      <p>A tenth of a second is shorter than a camera shutter, shorter than a heartbeat. Yet it's often enough to name a song you know — and that's the whole game. Hear a 0.1-second clip of a real track, then pick the right title from four answers.</p>
      <p>It's the Heardle idea pushed to its limit: Heardle started its clips at one second, and this game starts ten times shorter. No typing, no lyrics — just a sliver of sound and your memory. There's no scoreboard, because the score is self-evident: the less you hear, the deeper the song is filed in your head.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>4</dt><dd>choices per song</dd></div>
      <div><dt>5</dt><dd>rungs on the ladder</dd></div>
    </dl>
  </section>

  <section id="the-01-second-rule" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Less than a blink</p>
      <h2>The 0.1-Second Rule</h2>
      <p>In a tenth of a second you hear almost nothing — and that's exactly the point.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127911;</span><h3>One sound</h3><p>A tenth of a second holds a single sound — a snare crack, a hi-hat tick, a breath, the attack of a piano chord. That sound is the fingerprint.</p></article>
      <article><span class="icon">&#9889;</span><h3>Instant recognition</h3><p>Your brain names familiar music in milliseconds, before you can say why. The 0.1-second clip just gives that reflex room to fire.</p></article>
      <article><span class="icon">&#127925;</span><h3>A memory test</h3><p>It isn't trivia. It's a question of how deeply the song is filed in your head — the deeper the file, the shorter the clip you need.</p></article>
    </div>
  </section>

  <section id="reveal-ladder" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Five rungs, five kinds of clue</p>
      <h2>From 0.1s to 15s: The Reveal Ladder</h2>
      <p>Every wrong answer moves you up one rung, and each rung reveals a different kind of clue.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#9654;</span><h3>0.1s — one sound</h3><p>A transient, a breath, a chord attack. Enough for a song you know cold.</p></article>
      <article><span class="icon">&#9654;</span><h3>0.5s — the first note</h3><p>The opening note or the start of a riff. The shape of the melody begins.</p></article>
      <article><span class="icon">&#9654;</span><h3>2s — the intro</h3><p>The intro groove, the first line, the texture of the production.</p></article>
      <article><span class="icon">&#9654;</span><h3>8s — the verse</h3><p>The beat and the vocal settle in. Most songs are named by now.</p></article>
      <article><span class="icon">&#9654;</span><h3>15s — the hook</h3><p>The chorus. If you needed this long, the song wasn't filed deep.</p></article>
    </div>
  </section>

  <section id="how-to-guess-from-nothing" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Train the ear, not the trivia</p>
      <h2>How to Guess from Almost Nothing</h2>
      <p>Recognition is a skill, and it sharpens fast. These four habits turn a sliver into an answer.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127908;</span><h3>Listen for the transient</h3><p>The first 100ms is mostly attack — a snare, a synth stab, a piano hammer. That's the production's fingerprint.</p></article>
      <article><span class="icon">&#127926;</span><h3>Ride the contour</h3><p>The shape of a melody — up, down, a leap — survives even a 0.1s slice. Follow the direction.</p></article>
      <article><span class="icon">&#127916;</span><h3>Date the production</h3><p>An 80s gated snare, a 90s boom-bap loop, a 2010s 808. The era's sound gives the song away.</p></article>
      <article><span class="icon">&#9889;</span><h3>Trust the flash</h3><p>Recognition arrives before explanation. The first answer is usually the right one.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Guess the Song in 0.1 Second — FAQ</h2>
      <p>The questions people ask before the shortest clip.</p>
    </div>
    <div class="songspot-faq-list">
''' + ''.join(
    '<details%s><summary>%s</summary><p>%s</p></details>\n' % (' open' if i == 0 else '', q, a)
    for i, (q, a) in enumerate(FAQ)
) + '''    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">A tenth of a second. That's the test.</p>
    <h2>Ready to name a song from 0.1 second?</h2>
    <p>Press play above and see how deep the songs are filed.</p>
    <a href="#play">Start guessing &rarr;</a>
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
<title>Guess the Song in 0.1 Second — Free Song Guessing Game</title>
<meta name="description" content="Guess the song in 0.1 second: hear a tenth-of-a-second clip and name the track from four answers. Free online song guessing game — no signup, no download." />
<link rel="canonical" href="https://www.songguesser.co/guess-the-song-in-0-1-second/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Guess the Song in 0.1 Second — Free Song Guessing Game" />
<meta property="og:description" content="Hear a 0.1-second clip and name the song from four choices. The less you hear, the better you guessed." />
<meta property="og:url" content="https://www.songguesser.co/guess-the-song-in-0-1-second/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Guess the Song in 0.1 Second — Free Song Guessing Game" />
<meta name="twitter:description" content="Hear a 0.1-second clip, name the track from A, B, C or D. Free, no signup." />
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
{"@context":"https://schema.org","@type":"VideoGame","name":"Guess the Song in 0.1 Second","description":"A free song guessing game where you hear a 0.1-second clip and name the track from four answers.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/guess-the-song-in-0-1-second/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>
<script type="application/ld+json">
''' + faq_schema() + '''
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Guess the Song in 0.1 Second","item":"https://www.songguesser.co/guess-the-song-in-0-1-second/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'guess-the-song-in-0-1-second')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote guess-the-song-in-0-1-second/index.html  (%d bytes)' % len(page))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'guess-the-song-in-0-1-second' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/guess-the-song-in-0-1-second/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has guess-the-song-in-0-1-second')
