# -*- coding: utf-8 -*-
"""Generate /guess-that-kpop-song/ — a full game page (3-column layout with the
K-Pop filter) + an original, readable SEO article targeting "guess that kpop song".
Orphaned (not added to nav/footer/sitemap), so it doesn't affect existing ranking.
"""
import os

SRC = "guessable-songs/k-pop/index.html"
DST_DIR = "guess-that-kpop-song"
DST = os.path.join(DST_DIR, "index.html")

s = open(SRC, encoding="utf-8").read()

# --- schema: VideoGame name ---
s = s.replace(
    '"name":"K-Pop Guessable Songs"',
    '"name":"Guess That K-Pop Song"',
)

# --- breadcrumb (keep one) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Genres","item":"https://www.songguesser.co/guessable-songs/"},{"@type":"ListItem","position":3,"name":"K-Pop","item":"https://www.songguesser.co/guessable-songs/k-pop/"}]}',
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Guess That K-Pop Song","item":"https://www.songguesser.co/guess-that-kpop-song/"}]}',
)
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"}]}',
    "",
)

# --- FAQ schema (real user questions) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to know the group to play?","acceptedAnswer":{"@type":"Answer","text":"No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."}},{"@type":"Question","name":"How many K-pop guessable songs are in the pool?","acceptedAnswer":{"@type":"Answer","text":"796 tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."}},{"@type":"Question","name":"Is the K-pop quiz in English or Korean?","acceptedAnswer":{"@type":"Answer","text":"The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."}}]}',
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"I can\'t name a song from 0.1 seconds — is it supposed to be this hard?","acceptedAnswer":{"@type":"Answer","text":"That\'s the point. The clip opens at a tenth of a second and you press play again to reveal 0.5s, 2s, 8s, then 15s. Most people don\'t get it from the first sliver — they get it from the reveal that finally clicks."}},{"@type":"Question","name":"Why do I keep getting K-pop songs I don\'t know?","acceptedAnswer":{"@type":"Answer","text":"The pool spans four idol generations, so it mixes groups you know with b-sides and newer acts. Pick Easy to stay on the title tracks everyone recognizes, or lock the artist filter to one group."}},{"@type":"Question","name":"Can I play with only BTS or BLACKPINK songs?","acceptedAnswer":{"@type":"Answer","text":"Yes. Set the artist filter to a single act, or keep the genre on K-Pop to stay across the whole scene."}},{"@type":"Question","name":"The audio won\'t play on my phone — what\'s wrong?","acceptedAnswer":{"@type":"Answer","text":"The game decodes real audio in your browser, so it needs one tap to start (browsers block autoplay) and a stable connection to load the clip. Low-power mode can also delay it."}},{"@type":"Question","name":"Is this actually free, or do I need an account?","acceptedAnswer":{"@type":"Answer","text":"It\'s free and runs right in your browser. No signup, no download, no daily limit — play as many rounds as you want."}},{"@type":"Question","name":"I\'m stuck on a song — how do I get a new one?","acceptedAnswer":{"@type":"Answer","text":"Press Skip to reveal a longer clip, or hit Reroll to swap in a fresh track. You never have to sit on a song you can\'t place."}}]}',
)

# --- hero h1 + subtitle ---
s = s.replace(
    '<h1 id="songspot-heading">K-Pop Guessable Songs</h1>',
    '<h1 id="songspot-heading">Guess That K-Pop Song</h1>',
)
s = s.replace(
    '<p>Group hooks, polished production, a first beat — name the K-pop <a href="/guessable-songs/">guessable songs</a> in a second flat.</p>',
    '<p>Four generations of idols, one tenth-of-a-second opening. Name the track before the clip gets longer.</p>',
)

# --- title / description / canonical / og / twitter (+ VideoGame desc & url) ---
s = s.replace(
    "K-Pop Guessable Songs | Song Guesser",
    "Guess That K-Pop Song — Free K-Pop Song Guessing Game | Song Guesser",
)
s = s.replace(
    "Name the k-pop guessable songs from a 0.1-second clip. Free browser game with 796 K-Pop guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.",
    "Guess that K-Pop song from a 0.1-second clip. Free browser game across BTS, BLACKPINK, TWICE, Stray Kids and more — hear 0.5s, 2s, 8s and 15s only when you need them.",
)
s = s.replace(
    "https://www.songguesser.co/guessable-songs/k-pop/",
    "https://www.songguesser.co/guess-that-kpop-song/",
)

# --- swap the SEO sections (keep the game shell + scripts) ---
start = s.index('<section class="songspot-seo">')
end = s.index('<footer class="songspot-site-footer">')
article = '''<section class="songspot-seo">
<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">K-Pop guessing game</p><h2>What Is Guess That K-Pop Song?</h2><p>K-pop intros basically give the group away before anyone sings. A stomp, a chanted hook, one synth line — that's often all you need. Guess That K-Pop Song drops you into the first 0.1 seconds of a track and asks for the title.</p></div><p>Can't get it? Hit play again for a longer slice. The pool runs from the 2nd-gen groups that built the sound to the rookies still blowing up today, so some rounds are instant and some will humble you. It's one of the free quizzes over at <a href="/">Song Guesser</a>.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">K-Pop at a glance</p><h2>What Makes a K-Pop Song Guessing Game Work</h2><p>K-pop is basically built to be caught in a beat. Here's the shape of what the quiz pulls from.</p></div><dl class="songspot-seo-stats">
<div><dt>Origins</dt><dd>1990s · South Korea</dd></div>
<div><dt>Hallmarks</dt><dd>Choreography, fan chants, hook-first production, idol fandoms</dd></div>
<div><dt>Essential groups</dt><dd>BTS, BLACKPINK, TWICE, EXO, NewJeans, Stray Kids</dd></div>
<div><dt>Best-known tracks</dt><dd>Dynamite, DDU-DU DDU-DU, Gangnam Style, Cupid, Super Shy</dd></div>
<div><dt>Eras covered</dt><dd>2010s and 2020s</dd></div>
<div><dt>Why it works</dt><dd>The intro usually gives it away before the first line</dd></div>
<div><dt>Easiest to guess</dt><dd>Title tracks with a chanted hook</dd></div>
<div><dt>Trickiest to guess</dt><dd>B-sides, English versions, unit songs, EDM intros</dd></div>
</dl></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The rotation</p><h2>K-Pop Groups to Guess</h2><p>These acts anchor the pool. Each one has a sound you'll learn to catch fast.</p></div><div class="songspot-feature-grid">
<article><span class="icon">💜</span><h3>BTS</h3><p>"Dynamite" was their first US No. 1, but most of the catalog is still in Korean, and the quiz pulls from both.</p></article>
<article><span class="icon">🖤</span><h3>BLACKPINK</h3><p>Rap verse, big chorus, instrumental drop. You usually name the song by reading the shape of that drop.</p></article>
<article><span class="icon">🍭</span><h3>TWICE</h3><p>Shout-along hooks and the little hand gestures. A title track tends to give itself away on the first beat.</p></article>
<article><span class="icon">⚡</span><h3>Stray Kids</h3><p>Chant-heavy openings, rap-forward verses. The intro hits like a wall of sound before the melody shows up.</p></article>
<article><span class="icon">🐰</span><h3>NewJeans</h3><p>The 5th-gen flag-bearer. Airy, groove-led intros where the bass and the vocal do the work.</p></article>
<article><span class="icon">❄️</span><h3>EXO</h3><p>A split catalog: winter ballads like "Sing for You" on one side, tracks like "Monster" on the other.</p></article>
<article><span class="icon">💎</span><h3>SEVENTEEN</h3><p>Three units trade sections. Guessing the song often means catching which unit opens it.</p></article>
<article><span class="icon">🪐</span><h3>aespa</h3><p>Layered electronic intros, sharp production. The opening texture usually names the track, not a melody.</p></article>
</div></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Fast facts</p><h2>K-Pop Trivia Most Fans Miss</h2></div><ul class="kpop-facts">
<li>Fan chants are baked into some intros, which is why title-track openings are the fastest to name.</li>
<li>"Dynamite" was BTS's first all-English single and their first Billboard Hot 100 No. 1, in 2020.</li>
<li>PSY's "Gangnam Style" became the first YouTube video to pass one billion views, back in 2012.</li>
<li>The gap between title tracks and b-sides is exactly where casual listeners split from hardcore stans.</li>
<li>Japanese and English versions of the same song are a classic trap: the intro sounds right but the title you know is wrong.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The full story</p><h2>You Don't Guess K-Pop, You Recognize It</h2></div><p>You don't guess K-pop by remembering it. You recognize it. The lineups rotate and the production is dense, so the thing that gives a song away is rarely the melody by itself. It's one voice plus a drum pattern plus a hook, and that combo is exactly what producers tune to hit. Which is why 0.1 seconds is often plenty.</p><p>The deep cuts are where it gets mean. A b-side from a repackage, a Japanese version, a unit song nobody heard. Those are the rounds that separate the casual listener from the person with a lightstick. "Dynamite," "DDU-DU DDU-DU," and "Super Shy" live on the easy side. The album tracks don't.</p><p>Warm up with it or go for a full run. Either way, you'll find out fast how much of that first split second you actually caught. Then head back to <a href="/">Song Guesser</a> for the full guessing game.</p></section>

<section id="faq" class="songspot-seo-section songspot-seo-faq"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Questions about this quiz</p><h2>Guess That K-Pop Song FAQ</h2></div><div class="songspot-faq-list">
<details open><summary>I can't name a song from 0.1 seconds — is it supposed to be this hard?</summary><p>That's the point. The clip opens at a tenth of a second and you press play again to reveal 0.5s, 2s, 8s, then 15s. Most people don't get it from the first sliver — they get it from the reveal that finally clicks.</p></details>
<details><summary>Why do I keep getting K-pop songs I don't know?</summary><p>The pool spans four idol generations, so it mixes groups you know with b-sides and newer acts. Pick Easy to stay on the title tracks everyone recognizes, or lock the artist filter to one group.</p></details>
<details><summary>Can I play with only BTS or BLACKPINK songs?</summary><p>Yes. Set the artist filter to a single act, or keep the genre on K-Pop to stay across the whole scene.</p></details>
<details><summary>The audio won't play on my phone — what's wrong?</summary><p>The game decodes real audio in your browser, so it needs one tap to start (browsers block autoplay) and a stable connection to load the clip. Low-power mode can also delay it.</p></details>
<details><summary>Is this actually free, or do I need an account?</summary><p>It's free and runs right in your browser. No signup, no download, no daily limit — play as many rounds as you want.</p></details>
<details><summary>I'm stuck on a song — how do I get a new one?</summary><p>Press Skip to reveal a longer clip, or hit Reroll to swap in a fresh track. You never have to sit on a song you can't place.</p></details>
</div></section>
</section>'''

s = s[:start] + article + "\n\n" + s[end:]

# --- facts-list styles ---
s = s.replace(
    "</head>",
    "<style>\n.songspot-seo ul.kpop-facts{list-style:none;padding:0;margin:0;display:grid;gap:14px}\n.songspot-seo ul.kpop-facts li{position:relative;padding-left:30px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.kpop-facts li::before{content:\"\\2022\";position:absolute;left:0;top:2px;color:var(--green2)}\n</style>\n</head>",
)

os.makedirs(DST_DIR, exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)

# --- runnable check ---
out = s
assert "Guess That K-Pop Song" in out, "title/h1 missing"
assert "K-Pop Guessable Songs" not in out, "old title leaked"
assert "guess-that-kpop-song" in out, "canonical missing"
assert '<section class="songspot-shell"' in out, "game shell missing"
assert "window.SONG_INITIAL" in out, "game script missing"
assert '"@type":"VideoGame"' in out, "VideoGame schema missing"
assert '"@type":"FAQPage"' in out, "FAQ schema missing"
assert out.count("<article>") == 8, "artist cards"
assert out.count("<details") == 6, "FAQ entries"
assert out.count("<h1") == 1, "h1 count"
for i in ("difficultyList", "difficultyTabs", "stageChips", "volume", "rerollBtn"):
    assert 'id="%s"' % i in out, "missing id " + i
print("OK ->", DST, len(out), "bytes")
