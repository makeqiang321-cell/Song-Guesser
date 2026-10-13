# -*- coding: utf-8 -*-
"""Generate /music-guesser/ — a standalone, indexable SEO landing page for the broad
"music guesser" search intent (the umbrella term for song-guessing tools). Clones the
Music Quiz audio tool verbatim, then lays out original copy in search-intent order:
What Is -> How To Use -> What Makes a Good Music Guesser (information gain) -> FAQ (PAA)
-> Related (internal links) -> CTA. Includes HowTo + FAQPage structured data. Not linked
from header/footer (stays off the homepage) but indexable via sitemap. Copy is
differentiated from the /music-guessing-game/ page. Writes CRLF to match core.autocrlf=true."""
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
               '<h1 id="songspot-heading">Music Guesser — Name the Song from 0.1 Seconds</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>A music guesser plays you a tiny clip of a real song and asks you to name it. This one starts at 0.1 seconds — a drum hit, a breath, a chord — and gives you four answers: A, B, C or D. Unlimited rounds, no signup.</p>',
               shell, flags=re.S)

# --- header: this page is not in the nav, so nothing is "active" ---
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>',
                        '<a class="songspot-site-nav-link" href="/songless/">Songless</a>')

FAQ = [
    ("What is a music guesser?",
     "A music guesser is a game that plays you a short clip and asks you to name the song. This one compresses the idea to its fastest form — a 0.1-second clip and four answers."),
    ("How does a music guesser work?",
     "Start the clip and tap A, B, C or D. A wrong pick stretches the clip — 0.5s, 2s, 8s, then 15s — until you name the song."),
    ("Is this music guesser free?",
     "Yes. It's free in the browser with no account, no download and no cap — play as many rounds as you like on desktop or phone."),
    ("Can I play a music guesser with friends?",
     "This one is single-player, so the easiest way to play together is pass-and-play — hand the screen over after each round and race for the shortest clip. No lobby or signup needed."),
    ("What's the difference between a music guesser and Heardle?",
     "Heardle rationed one song a day with six typed guesses. A music guesser like this one is unlimited, with four tap-answers and no daily limit."),
    ("Can I pick the genre or era?",
     "Yes. Filter the pool by genre, decade or artist, choose a difficulty, and set your starting clip length with the Guess after controls."),
]

STEPS = [
    ("Start the clip", "Start the clip to hear 0.1 seconds of a real song."),
    ("Choose A, B, C or D", "Four answers appear. Choose the one you think you heard."),
    ("Reveal more when unsure", "Unsure? A wrong answer stretches the clip to 0.5s, 2s, 8s, then 15s."),
]

SEO = '''
<section class="songspot-seo">
  <section id="what-is-a-music-guesser" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">The tool everyone calls a music guesser</p>
      <h2>What Is a Music Guesser?</h2>
      <p>A music guesser is any game or tool that plays you a short clip of a song and asks you to name it. This one compresses the idea to its fastest form: every round starts at 0.1 seconds — a single drum hit, a breath, a chord attack — and you pick the correct title from four answers before the clip grows.</p>
      <p>It's the format Heardle made famous in 2022, stripped of the daily limit. No typing, no lyrics, no account — just your ear against four options, one song after another.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>5</dt><dd>clip lengths</dd></div>
      <div><dt>&#8734;</dt><dd>unlimited rounds</dd></div>
    </dl>
  </section>

  <section id="how-to-use" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Three steps, one sliver</p>
      <h2>How to Use This Music Guesser</h2>
      <p>Every round takes about ten seconds. Here's the whole flow.</p>
    </div>
    <ol class="songspot-how-grid">
''' + ''.join(
    '<li><span>%02d</span><span class="icon">&#9654;</span><h3>%s</h3><p>%s</p></li>\n' % (i + 1, n, t)
    for i, (n, t) in enumerate(STEPS)
) + '''    </ol>
  </section>

  <section id="what-makes-a-good-music-guesser" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">The features that separate the good ones</p>
      <h2>What Makes a Good Music Guesser</h2>
      <p>A music guesser is only as good as its clips and its controls. Here's what to look for.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#9200;</span><h3>A real 0.1-second start</h3><p>Many claim the shortest clip, few deliver it. A true 0.1-second start is a single sound — that's where the challenge lives.</p></article>
      <article><span class="icon">&#128220;</span><h3>Four choices, not typing</h3><p>Taps beat typed titles. A, B, C or D keeps the game fast on a phone and fair for songs whose spelling is a puzzle of its own.</p></article>
      <article><span class="icon">&#127919;</span><h3>Difficulty lanes</h3><p>Chill to Impossible, with a starting clip you control — 0.1s for experts, 2s or 8s while you warm up.</p></article>
      <article><span class="icon">&#127911;</span><h3>Genre, decade or artist filters</h3><p>Narrow the pool to the songs you actually know, so every round is a fair fight instead of a random deep cut.</p></article>
      <article><span class="icon">&#128293;</span><h3>Unlimited, no account</h3><p>No daily lockout, no signup, no download. The best music guesser is the one that's there the second you want a round.</p></article>
      <article><span class="icon">&#127908;</span><h3>A fair reveal ladder</h3><p>0.5s, 2s, 8s, 15s — each wrong pick doubles the context, so no round is a dead end.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Music Guesser — FAQ</h2>
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
        <li><a href="/guess-that-song/">Guess That Song</a> — the free online song guessing game across every genre</li>
        <li><a href="/music-quiz/">Music Quiz</a> — the classic free music quiz with difficulty and genre filters</li>
        <li><a href="/songless/">Songless</a> — guess the song from 0.1 seconds, no lyrics, no titles</li>
        <li><a href="/music-guessing-game/">Music Guessing Game</a> — a name-that-tune blind test across every decade</li>
        <li><a href="/guess-the-taylor-swift-song/">Guess the Taylor Swift Song</a> — all 11 eras, one sliver</li>
      </ul>
    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">Unlimited. Free. One tap.</p>
    <h2>Ready to test your music guesser instinct?</h2>
    <p>Press play above and name the song from a sliver.</p>
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
    return '{"@context":"https://schema.org","@type":"HowTo","name":"How to Use This Music Guesser","description":"Use the free music guesser in three steps: hear a 0.1-second clip, pick the song from four choices, and reveal a longer clip if you miss.","totalTime":"PT1M","step":[' + steps + ']}'

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Music Guesser — Name the Song from 0.1 Seconds</title>
<meta name="description" content="Music guesser: hear a fraction of a second of a real song and name it from four choices. Free online song guessing game — unlimited rounds, no signup." />
<link rel="canonical" href="https://www.songguesser.co/music-guesser/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Music Guesser — Name the Song from 0.1 Seconds" />
<meta property="og:description" content="Hear a sliver, name the song from four choices. A free online music guesser — unlimited rounds, no signup." />
<meta property="og:url" content="https://www.songguesser.co/music-guesser/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Music Guesser — Name the Song from 0.1 Seconds" />
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
{"@context":"https://schema.org","@type":"VideoGame","name":"Music Guesser","description":"A free online music guesser where you hear a fraction of a second of a real song and name the track from four answers before the clip grows.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/music-guesser/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
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
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Music Guesser","item":"https://www.songguesser.co/music-guesser/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'music-guesser')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote music-guesser/index.html  (%d bytes)' % len(page))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'music-guesser' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/music-guesser/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has music-guesser')
