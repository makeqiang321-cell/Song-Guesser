# -*- coding: utf-8 -*-
"""Generate /music-guessing-game/ — a standalone, indexable SEO landing page that clones
the Music Quiz audio tool (play key, timeline, guess-after seconds, volume, difficulty,
filters, A/B/C/D options). Unlike Songless, it is NOT linked from the header/footer and
does not modify any other page, so it stays hidden from the homepage but still indexable
via sitemap. Copy is differentiated from music-quiz and songless to avoid duplicate
content. Writes CRLF to match core.autocrlf=true."""
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
               '<h1 id="songspot-heading">Music Guessing Game — Name the Tune in 0.1 Seconds</h1>',
               shell, flags=re.S)
shell = re.sub(r'<p>Music Quiz is Song Guesser.*?</p>',
               '<p>The Music Guessing Game is Song Guesser\'s name-that-tune blind test: hear a 0.1-second clip of a real song, then pick the right title from four answers — A, B, C or D. No typing, no signup, no download, just your ear against four options.</p>',
               shell, flags=re.S)

# --- header: this page is not in the nav, so nothing is "active" ---
header = header.replace('<a class="songspot-site-nav-link active" href="/">Play</a>',
                        '<a class="songspot-site-nav-link" href="/">Play</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
                        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>')
header = header.replace('<a class="songspot-site-nav-link active" href="/songless/">Songless</a>',
                        '<a class="songspot-site-nav-link" href="/songless/">Songless</a>')

FAQ = [
    ("What is a music guessing game?",
     "A music guessing game plays you a very short clip of a real song and asks you to name the tune. On this one, you hear a 0.1-second sample, then pick the right title from four answers — A, B, C or D."),
    ("How does a name-that-tune game work?",
     "You hear a short clip and try to name the song. A wrong pick reveals a longer clip — 0.5s, 2s, 8s, then 15s — so the tune comes into focus one step at a time until you get it."),
    ("Why do the clips start so short?",
     "A tenth of a second strips a song down to its fingerprint — a drum hit, a breath, a synth stab. It tests recognition rather than memory, and the reveal ladder keeps it fair when you're stuck."),
    ("What songs are in the guessing game?",
     "Thousands of songs across genres and decades — pop, rock, hip-hop, R&B, electronic, country, metal and K-pop, from the 70s through today. Every round draws a fresh track and four choices."),
    ("Is the music guessing game free to play?",
     "Yes. It's free to play in any browser, with no signup, no download and no daily limit — name tunes one after another on desktop or phone."),
    ("Can I play by artist, decade or genre?",
     "Yes. Set a lane (a genre, a decade or an artist) and the blind test keeps serving four choices from that lane until you switch lanes."),
]

SEO = '''
<section class="songspot-seo">
  <section id="what-is-a-music-guessing-game" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">Hear a sliver, name the tune</p>
      <h2>What Is a Music Guessing Game?</h2>
      <p>A music guessing game plays you a tiny clip of a real song and asks you to name it. This one is a blind test: hear a 0.1-second sample, then pick the right title from four answers — A, B, C or D. No typing, no artwork, just your ear against the sound.</p>
      <p>It's the name-that-tune format Heardle made famous, built for quick rounds. Every clip is a real song preview, and every round is a fresh track from a catalog of thousands of songs across genres and decades — from the 70s through today, with no download or sign-up.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the first clip you hear</dd></div>
      <div><dt>4</dt><dd>choices per tune</dd></div>
      <div><dt>5</dt><dd>difficulty lanes</dd></div>
    </dl>
  </section>

  <section id="how-the-blind-test-works" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Three taps, one sliver</p>
      <h2>How the Blind Test Works</h2>
      <p>Press play, hear whatever tenth of a second you get, and decide on the spot: tap now, or let a wrong answer reveal more of the track.</p>
    </div>
    <ol class="songspot-how-grid">
      <li><span>01</span><span class="icon">&#9654;</span><h3>Hear the sliver</h3><p>A tenth-of-a-second sample of a real song plays. There's no title, no artwork — just sound and four options.</p></li>
      <li><span>02</span><span class="icon">A</span><h3>Tap the tune you hear</h3><p>Four titles with their artists appear. Tap the one that matches; the right pick lights up green instantly.</p></li>
      <li><span>03</span><span class="icon">&#9197;</span><h3>Reveal on a miss</h3><p>A wrong answer stretches the clip to 0.5s, 2s, 8s, then 15s, so the tune comes into focus one step at a time.</p></li>
    </ol>
  </section>

  <section id="why-short-clip" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">The shortest clip is the whole game</p>
      <h2>Why a 0.1-Second Clip Works</h2>
      <p>A tenth of a second strips a song down to its fingerprint. That's the point — it rewards the ear, not the memory of lyrics.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">&#127911;</span><h3>Recognition, not recall</h3><p>You don't need to remember a chorus. A drum hit, a breath, a synth stab is often enough to name the tune.</p></article>
      <article><span class="icon">&#127925;</span><h3>A fair reveal ladder</h3><p>Missed it? Each reveal doubles the context — 0.5s, 2s, 8s, 15s — so no round is a dead end.</p></article>
      <article><span class="icon">&#127908;</span><h3>Any ear can play</h3><p>No music theory, no typing. Pick A, B, C or D and the answer comes from the sound alone.</p></article>
    </div>
  </section>

  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Short answers</p>
      <h2>Music Guessing Game — FAQ</h2>
      <p>The questions people ask before the first blind clip.</p>
    </div>
    <div class="songspot-faq-list">
''' + ''.join(
    '<details%s><summary>%s</summary><p>%s</p></details>\n' % (' open' if i == 0 else '', q, a)
    for i, (q, a) in enumerate(FAQ)
) + '''    </div>
  </section>

  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">Blind test, every decade</p>
    <h2>Ready to name the tune from a blind clip?</h2>
    <p>Press play above and start the blind test — thousands of songs, one sliver at a time.</p>
    <a href="#play">Start the blind test &rarr;</a>
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
<title>Music Guessing Game — Name That Tune in 0.1 Seconds</title>
<meta name="description" content="A free online music guessing game: hear a 0.1-second blind-test clip and name the tune from four choices. Thousands of songs, five difficulties, no signup." />
<link rel="canonical" href="https://www.songguesser.co/music-guessing-game/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Music Guessing Game — Name That Tune in 0.1 Seconds" />
<meta property="og:description" content="Hear a 0.1-second clip and name the tune from four choices. A free online music guessing game — no signup, no download." />
<meta property="og:url" content="https://www.songguesser.co/music-guessing-game/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Music Guessing Game — Name That Tune in 0.1 Seconds" />
<meta name="twitter:description" content="Hear a 0.1-second clip, name the tune from A, B, C or D. Free, no signup." />
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
{"@context":"https://schema.org","@type":"VideoGame","name":"Music Guessing Game","description":"A free online name-that-tune guessing game where you hear a 0.1-second blind-test clip and pick the song title from four answers.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/music-guessing-game/","playMode":"SinglePlayer","genre":["Music","Trivia"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>
<script type="application/ld+json">
''' + faq_schema() + '''
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Music Guessing Game","item":"https://www.songguesser.co/music-guessing-game/"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Song Guesser","url":"https://www.songguesser.co/","logo":{"@type":"ImageObject","url":"https://www.songguesser.co/images/logo.png","width":512,"height":512}}
</script>
</head>
<body>

'''

page = HEAD + header + shell + SEO + footer + '\n<script src="/decades.js"></script>\n<script src="/mcq.js?v=2"></script>\n' + dropdown_js + '\n</body></html>\n'

outdir = os.path.join(BASE, 'music-guessing-game')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), page)
print('wrote music-guessing-game/index.html  (%d bytes)' % len(page))

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/music-quiz/</loc><priority>0.9</priority></url>'
if 'music-guessing-game' not in s:
    s = s.replace(anchor, anchor + '\n  <url><loc>https://www.songguesser.co/music-guessing-game/</loc><priority>0.85</priority></url>')
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has music-guessing-game')
