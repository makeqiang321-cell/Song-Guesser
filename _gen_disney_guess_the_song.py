# -*- coding: utf-8 -*-
"""Generate /disney-guess-the-song/ — a standalone, indexable SEO page targeting the
"disney guess the song" search intent. Clones the Music Quiz audio tool verbatim (play
key, timeline, guess-after seconds, volume, difficulty, filters, A/B/C/D options) but the
landing copy is written fresh — not from the music-guessing-game template — with a Disney
music-era timeline and "Disney sound" guide for information gain. Not linked from the
header/footer, so it stays off the homepage but still indexable via sitemap. Writes CRLF
to match core.autocrlf=true."""
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
               '<h1 id="songspot-heading">Disney Guess the Song — Name the Tune in 0.1 Seconds</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>Disney Guess the Song is Song Guesser\'s name-that-tune mode for the Disney catalog: hear a 0.1-second clip of a real Disney song, then pick the right title from four answers — A, B, C or D. From Snow White to Frozen and Encanto, just your ear against four options.</p>',
               shell, flags=re.S)

# --- header: this page is not in the nav, so nothing is "active" ---
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>',
                        '<a class="songspot-site-nav-link" href="/songless/">Songless</a>')

FAQ = [
    ("What is Disney Guess the Song?",
     "Disney Guess the Song is a name-that-tune game built around Disney songs. Hear a 0.1-second clip of a real Disney song, then pick the right title from four answers — A, B, C or D."),
    ("Which Disney songs can I guess?",
     "Songs from the whole Disney catalog — from Snow White and Mary Poppins through The Lion King and Frozen to Encanto and Wish. Every era of Disney music is in the pool."),
    ("Do I need to know the lyrics?",
     "No. You play by ear. The clip is pure melody and orchestration, so you only need to recognize the tune, not remember a single line."),
    ("Is the Disney song quiz free to play?",
     "Yes. It's free in the browser, with no signup, no download and no daily limit — guess Disney tunes for as long as you like."),
    ("Can I pick a Disney era or movie?",
     "Yes. Use the filters to narrow the pool by decade or artist, so you can stick to the Renaissance, the 1990s, or one soundtrack if you prefer."),
    ("What if I can't name it from 0.1 seconds?",
     "A wrong pick reveals a longer clip — 0.5s, 2s, 8s, then 15s — so the song comes into focus one step at a time until you get it."),
]

SEO = '''
<section class="songspot-seo">
  <section id="guess-the-disney-song" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">From Snow White to Encanto, in one sliver</p>
      <h2>Guess the Disney Song</h2>
      <p>Disney songs are the most recognizable tunes on Earth — a two-second orchestral swell is usually enough to name the movie. This quiz turns that instinct into a game: hear a 0.1-second clip of a real Disney song, then pick the right title from four answers. No typing, no lyrics, just the melody against four options.</p>
      <p>Every era is here, from the 1937 classic Snow White and the Seven Dwarfs to Frozen, Moana, Encanto and Wish. If you can hum it, you can probably name it from the first sliver.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>4</dt><dd>choices per song</dd></div>
      <div><dt>1937</dt><dd>the year Disney songs began</dd></div>
    </dl>
  </section>

  <section id="disney-music-eras" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">A century, five chapters</p>
      <h2>Every Era of Disney Music</h2>
      <p>Disney songs fall into five distinct eras, each with its own sound and its own anthem. Knowing the eras is half the game.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127775;</span><h3>Golden Age · 1937–1959</h3><p>The orchestra-and-choir sound of Snow White's "Someday My Prince Will Come", Pinocchio's "When You Wish Upon a Star" and Sleeping Beauty's "Once Upon a Dream".</p></article>
      <article><span class="icon">&#127916;</span><h3>Silver Age · 1960–1988</h3><p>The Sherman Brothers era: Mary Poppins' "Supercalifragilisticexpialidocious" and "Chim Chim Cher-ee", plus The Jungle Book's "The Bare Necessities".</p></article>
      <article><span class="icon">&#127912;</span><h3>Renaissance · 1989–1999</h3><p>The Alan Menken and Howard Ashman decade — "Part of Your World", "Be Our Guest", "A Whole New World", "Circle of Life", "Colors of the Wind" and "Go the Distance".</p></article>
      <article><span class="icon">&#10052;</span><h3>Revival · 2009–2019</h3><p>Tangled's "I See the Light", Frozen's "Let It Go" and Moana's "How Far I'll Go" — the Robert and Kristen Anderson-Lopez and Lin-Manuel Miranda wave.</p></article>
      <article><span class="icon">&#127881;</span><h3>Modern · 2020–today</h3><p>Encanto's record-breaking "We Don't Talk About Bruno" and Wish's "This Wish" — Disney's newest earworms, already quiz staples.</p></article>
    </div>
  </section>

  <section id="how-it-works" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">One sliver, three moves</p>
      <h2>How the Disney Song Quiz Works</h2>
      <p>Press play, hear whatever tenth of a second you get, and decide on the spot: tap now, or let a wrong answer reveal more of the tune.</p>
    </div>
    <ol class="songspot-how-grid">
      <li><span>01</span><span class="icon">&#9654;</span><h3>Hear the sliver</h3><p>A tenth of a second of a real Disney song plays. The orchestral swell, the first chord, the breath before the chorus — that's your clue.</p></li>
      <li><span>02</span><span class="icon">A</span><h3>Tap the Disney tune</h3><p>Four song titles appear — one is right. Tap your answer and the correct pick lights up green instantly.</p></li>
      <li><span>03</span><span class="icon">&#9197;</span><h3>Reveal only when stuck</h3><p>A wrong pick stretches the clip to 0.5s, 2s, 8s, then 15s, so the song comes into focus one step at a time.</p></li>
    </ol>
  </section>

  <section id="disney-sound" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Learn the tell, own the game</p>
      <h2>The Disney Sound: How to Recognize It</h2>
      <p>Disney songs share a few signature shapes. Once you can hear them, a sliver is usually all you need.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127925;</span><h3>The "I Want" song</h3><p>Nearly every heroine opens with a longing ballad — "Part of Your World", "A Whole New World", "How Far I'll Go". Hear a soaring, wishful melody and it's almost always the lead's anthem.</p></article>
      <article><span class="icon">&#128520;</span><h3>The villain song</h3><p>Minor key, theatrical and menacing — "Poor Unfortunate Souls", "Be Prepared", "Mother Knows Best". A dark, stomping tune gives the baddie away fast.</p></article>
      <article><span class="icon">&#127926;</span><h3>The sidekick comic song</h3><p>Up-tempo, bouncy and wordy — "Under the Sea", "Hakuna Matata", "You're Welcome". If it swings, it's the comic-relief number.</p></article>
      <article><span class="icon">&#127932;</span><h3>The full-orchestra swell</h3><p>Disney choruses land on a big symphonic lift. The strings-and-choir wall of sound is the studio's oldest signature, from 1937 to today.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Disney Guess the Song — FAQ</h2>
      <p>What Disney fans ask before the first clip.</p>
    </div>
    <div class="songspot-faq-list">
''' + ''.join(
    '<details%s><summary>%s</summary><p>%s</p></details>\n' % (' open' if i == 0 else '', q, a)
    for i, (q, a) in enumerate(FAQ)
) + '''    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">Snow White to Encanto, in a sliver</p>
    <h2>Ready to name the Disney tune?</h2>
    <p>Press play above and name the Disney song from the shortest clip you can.</p>
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
<title>Disney Guess the Song — Name the Disney Tune in 0.1 Seconds</title>
<meta name="description" content="Guess the Disney song from a 0.1-second clip and pick the right tune from four answers — Snow White to Frozen and Encanto. Free, no signup." />
<link rel="canonical" href="https://www.songguesser.co/disney-guess-the-song/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Disney Guess the Song — Name the Disney Tune in 0.1 Seconds" />
<meta property="og:description" content="Hear a 0.1-second clip and name the Disney song from four choices. Every era, from Snow White to Encanto — free, no signup." />
<meta property="og:url" content="https://www.songguesser.co/disney-guess-the-song/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Disney Guess the Song — Name the Disney Tune in 0.1 Seconds" />
<meta name="twitter:description" content="Hear a 0.1-second clip, name the Disney tune from A, B, C or D. Free, no signup." />
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
{"@context":"https://schema.org","@type":"VideoGame","name":"Disney Guess the Song","description":"A free name-that-tune game where you hear a 0.1-second clip of a Disney song and pick the right title from four answers.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/disney-guess-the-song/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>
<script type="application/ld+json">
''' + faq_schema() + '''
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Disney Guess the Song","item":"https://www.songguesser.co/disney-guess-the-song/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'disney-guess-the-song')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote disney-guess-the-song/index.html  (%d bytes)' % len(page))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'disney-guess-the-song' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/disney-guess-the-song/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has disney-guess-the-song')
