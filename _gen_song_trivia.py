# -*- coding: utf-8 -*-
"""Generate /song-trivia/ — a full TYPE-IN game page (game.js, all genres) +
an original, readable, de-AI'd SEO article targeting "song trivia".
Angle = trivia has two sides: FACT trivia (written questions) and EAR trivia
(naming a song from audio). Real, verifiable song-trivia facts deliver the
information gain the query wants, while the audio game is the "ear trivia"
product. Orphaned. Internal links: homepage + genre pages.
"""
import os
import re

SRC = "guessable-songs/k-pop/index.html"
DST_DIR = "song-trivia"
DST = os.path.join(DST_DIR, "index.html")

s = open(SRC, encoding="utf-8").read()

# --- schema: VideoGame name ---
s = s.replace(
    '"name":"K-Pop Guessable Songs"',
    '"name":"Song Trivia"',
)

# --- breadcrumb (keep one) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Genres","item":"https://www.songguesser.co/guessable-songs/"},{"@type":"ListItem","position":3,"name":"K-Pop","item":"https://www.songguesser.co/guessable-songs/k-pop/"}]}',
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Song Trivia","item":"https://www.songguesser.co/song-trivia/"}]}',
)
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"}]}',
    "",
)

# --- FAQ schema (real user questions, distinct from other pages) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to know the group to play?","acceptedAnswer":{"@type":"Answer","text":"No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."}},{"@type":"Question","name":"How many K-pop guessable songs are in the pool?","acceptedAnswer":{"@type":"Answer","text":"796 tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."}},{"@type":"Question","name":"Is the K-pop quiz in English or Korean?","acceptedAnswer":{"@type":"Answer","text":"The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."}}]}',
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is song trivia?","acceptedAnswer":{"@type":"Answer","text":"Song trivia is questions about songs — who sang them, what year, which album. It comes in two flavors: fact trivia (written questions) and ear trivia (name this from a clip). This page is the ear kind."}},{"@type":"Question","name":"Do I need to know song facts to play?","acceptedAnswer":{"@type":"Answer","text":"No. The game asks for the title, not the year or the record label. You just need to recognize the audio."}},{"@type":"Question","name":"Can I filter song trivia by decade?","acceptedAnswer":{"@type":"Answer","text":"Yes, plus genre and artist. The decade filter is handy if you want 80s or 90s trivia specifically."}},{"@type":"Question","name":"Do I type the answer or pick from choices?","acceptedAnswer":{"@type":"Answer","text":"You type it. No multiple choice — if you know part of the title, the search box matches as you go."}},{"@type":"Question","name":"What\'s a song trivia fact most people don\'t know?","acceptedAnswer":{"@type":"Answer","text":"\\\"I Will Always Love You\\\" was Dolly Parton\'s song first — she wrote it in 1973, and Whitney Houston\'s version came 19 years later."}},{"@type":"Question","name":"Is song trivia free?","acceptedAnswer":{"@type":"Answer","text":"Yes. In the browser, no signup, no download, no daily limit."}}]}',
)

# --- hero h1 + subtitle ---
s = s.replace(
    '<h1 id="songspot-heading">K-Pop Guessable Songs</h1>',
    '<h1 id="songspot-heading">Song Trivia</h1>',
)
s = s.replace(
    '<p>Group hooks, polished production, a first beat — name the K-pop <a href="/guessable-songs/">guessable songs</a> in a second flat.</p>',
    '<p>Song trivia usually asks who sang it. This one plays it — name the song from a sliver of audio.</p>',
)

# --- title / description / canonical / og / twitter (+ VideoGame desc & url) ---
s = s.replace(
    "K-Pop Guessable Songs | Song Guesser",
    "Song Trivia — Trivia for Your Ears: Name the Song From a Sliver | Song Guesser",
)
s = s.replace(
    "Name the k-pop guessable songs from a 0.1-second clip. Free browser game with 796 K-Pop guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.",
    "Song trivia with a twist: instead of written questions, name the song from a sliver of audio. Free browser game — plus real song trivia facts about the records, firsts and covers.",
)
s = s.replace(
    "https://www.songguesser.co/guessable-songs/k-pop/",
    "https://www.songguesser.co/song-trivia/",
)

# --- make the game generic (all genres) ---
s = s.replace(
    'window.SONG_INITIAL = {"genre":51}',
    'window.SONG_INITIAL = {}',
)

# --- swap the SEO sections (keep the game shell + scripts) ---
start = s.index('<section class="songspot-seo">')
end = s.index('<footer class="songspot-site-footer">')
article = '''<section class="songspot-seo">
<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Song trivia</p><h2>What Is Song Trivia?</h2><p>Song trivia is questions about songs — who sang it, what year, which album. It comes in two flavors. There's fact trivia: written questions with a right answer you can look up. And there's ear trivia: a sliver of the song itself, played for you, with no question on screen except "what is this?"</p></div><p>This page is the ear kind. It plays a real song from a tenth of a second and asks you to name it. No multiple choice, no written clue — just your memory against the sound. It's the same instinct as fact trivia, aimed at the part of your brain that knows a song the instant it starts. Free, no account, right here on <a href="/">Song Guesser</a>.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The fact side</p><h2>Song Trivia Facts Worth Knowing</h2><p>Before you test your ears, warm up with the other kind of song trivia — the facts. These are the ones that still surprise people.</p></div><ul class="trivia-facts">
<li><strong>"I Will Always Love You"</strong> — Dolly Parton wrote it in 1973. Whitney Houston's version came 19 years later, for The Bodyguard.</li>
<li><strong>"White Christmas"</strong> — Bing Crosby's 1942 single is still the best-selling single ever, around 50 million copies.</li>
<li><strong>"Bohemian Rhapsody"</strong> — Queen pushed it with one of the first promotional music videos, back in 1975.</li>
<li><strong>"Gangnam Style"</strong> — PSY's 2012 hit was the first YouTube video to pass a billion views.</li>
<li><strong>"Happy Birthday to You"</strong> — stayed under copyright until 2016, nearly a century after it was written.</li>
<li><strong>"Yesterday"</strong> — The Beatles' ballad is one of the most-covered songs ever, with thousands of versions.</li>
<li><strong>"Rock Around the Clock"</strong> — Bill Haley & His Comets' 1955 hit is usually called the first rock-and-roll number one.</li>
<li><strong>"Umbrella"</strong> — Rihanna's 2007 smash was offered to Britney Spears before it landed with her.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The ear side</p><h2>How Ear Trivia Works</h2><p>The rule is one sentence: hear as little as possible and name the title. The clip opens at a tenth of a second — a drum hit, a breath, a chord — and you press play again only when you have to. Each skip costs points, so the trivia question is really "how little audio do you need?"</p></div><p>There's no multiple choice. You type the title, and the search box matches as you go, so knowing part of a name is enough to get there. It's the difference between a trivia question you can guess at and one you have to actually know.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The rotation</p><h2>Song Trivia by Genre</h2><p>Eight genres anchor the pool. Each one has its own trivia flavor.</p></div><div class="songspot-feature-grid">
<article><span class="icon">💿</span><h3><a href="/guessable-songs/pop/">Pop</a></h3><p>Who sang it is half the answer. Pop trivia is chart trivia — the hits and the one-hit wonders.</p></article>
<article><span class="icon">🎤</span><h3><a href="/guessable-songs/hip-hop/">Hip-Hop</a></h3><p>Samples and producer tags. Hip-hop trivia is knowing which beat came from where.</p></article>
<article><span class="icon">🎸</span><h3><a href="/guessable-songs/rock/">Rock</a></h3><p>Lineups and riffs. Rock trivia is the band, the era, and the story behind the song.</p></article>
<article><span class="icon">🎹</span><h3><a href="/guessable-songs/r-and-b/">R&B</a></h3><p>Voices and covers. R&B trivia is knowing the original from the remake.</p></article>
<article><span class="icon">💃</span><h3><a href="/guessable-songs/electronic/">Electronic</a></h3><p>BPMs and samples. Electronic trivia is placing the sound in the right club year.</p></article>
<article><span class="icon">🤠</span><h3><a href="/guessable-songs/country/">Country</a></h3><p>Storytellers. Country trivia is remembering which song told which story.</p></article>
<article><span class="icon">🪩</span><h3><a href="/guessable-songs/k-pop/">K-Pop</a></h3><p>Generations and groups. K-pop trivia is knowing the group from the sound alone.</p></article>
<article><span class="icon">🎺</span><h3><a href="/guessable-songs/metal/">Metal</a></h3><p>Subgenres. Metal trivia is naming the style before the band.</p></article>
</div></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Get better fast</p><h2>Tips That Actually Work</h2></div><ul class="kpop-facts">
<li>Don't confuse fact trivia with ear trivia. You don't need the year — you need to catch the sound.</li>
<li>The chorus is your best clue. Most songs give themselves away there.</li>
<li>If you know the artist but not the song, lock the artist filter and narrow it down.</li>
<li>A 0.1s clip is a single sound — treat it like a hint, not a full question.</li>
<li>Play by decade to test one era's trivia specifically.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The full story</p><h2>Song Trivia Has Two Sides, and This Is the Hard One</h2></div><p>Most song trivia is facts: who sang it, what year, which album. That's the kind you can look up. Ear trivia is different — the question is a sliver of the song itself, and there's nothing to look up. You either catch it or you don't.</p><p>The fact side is a memory test. The ear side is a recognition test. Both are "trivia," but the ear kind is the one that actually tells you how well you know a song, because it strips away every clue except the sound itself.</p><p>It's free, no account, no daily limit. If you want the fact side — the years, the records, the stories — there's a lifetime of that online. This is where the ear side lives. Head back to <a href="/">Song Guesser</a> to pick a lane.</p></section>

<section id="faq" class="songspot-seo-section songspot-seo-faq"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Questions about this quiz</p><h2>Song Trivia FAQ</h2></div><div class="songspot-faq-list">
<details open><summary>What is song trivia?</summary><p>Song trivia is questions about songs — who sang them, what year, which album. It comes in two flavors: fact trivia (written questions) and ear trivia (name this from a clip). This page is the ear kind.</p></details>
<details><summary>Do I need to know song facts to play?</summary><p>No. The game asks for the title, not the year or the record label. You just need to recognize the audio.</p></details>
<details><summary>Can I filter song trivia by decade?</summary><p>Yes, plus genre and artist. The decade filter is handy if you want 80s or 90s trivia specifically.</p></details>
<details><summary>Do I type the answer or pick from choices?</summary><p>You type it. No multiple choice — if you know part of the title, the search box matches as you go.</p></details>
<details><summary>What's a song trivia fact most people don't know?</summary><p>"I Will Always Love You" was Dolly Parton's song first — she wrote it in 1973, and Whitney Houston's version came 19 years later.</p></details>
<details><summary>Is song trivia free?</summary><p>Yes. In the browser, no signup, no download, no daily limit.</p></details>
</div></section>

<section class="songspot-seo-cta">
<p class="songspot-seo-eyebrow">Trivia for your ears</p>
<h2>Song Trivia</h2>
<p>Press play and see how fast the song names itself in your head.</p>
<a href="#play">Start guessing →</a>
</section>
</section>'''

s = s[:start] + article + "\n\n" + s[end:]

# --- styles for the new lists ---
s = s.replace(
    "</head>",
    "<style>\n.songspot-seo ul.kpop-facts{list-style:none;padding:0;margin:0;display:grid;gap:14px}\n.songspot-seo ul.kpop-facts li{position:relative;padding-left:30px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.kpop-facts li::before{content:\"\\2022\";position:absolute;left:0;top:2px;color:var(--green2)}\n.songspot-seo ul.trivia-facts{list-style:none;padding:0;margin:0;display:grid;gap:16px}\n.songspot-seo ul.trivia-facts li{color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.trivia-facts strong{color:#f2f6f3;font-weight:600}\n</style>\n</head>",
)

# drop the empty breadcrumb script tag left over from the template
s = re.sub(r'<script type="application/ld\+json">\s*</script>', "", s)

os.makedirs(DST_DIR, exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)

# --- runnable check ---
out = s
assert "Song Trivia" in out, "title/h1 missing"
assert "K-Pop Guessable Songs" not in out, "old title leaked"
assert "song-trivia" in out, "canonical missing"
assert '<section class="songspot-shell"' in out, "game shell missing"
assert "window.SONG_INITIAL" in out, "game script missing"
assert "window.SONG_INITIAL = {}" in out, "generic genre not applied"
assert '"@type":"VideoGame"' in out, "VideoGame schema missing"
assert '"name":"Song Trivia"' in out, "VideoGame name missing"
assert '"@type":"FAQPage"' in out, "FAQ schema missing"
assert out.count("<article>") == 8, "genre cards"
assert out.count("<details") == 6, "FAQ entries"
assert out.count("<h1") == 1, "h1 count"
for i in ("difficultyList", "difficultyTabs", "stageChips", "volume", "rerollBtn"):
    assert 'id="%s"' % i in out, "missing id " + i
print("OK ->", DST, len(out), "bytes")
