# -*- coding: utf-8 -*-
"""Generate /music-trivia-game/ — a full TYPE-IN game page (game.js, all genres)
+ an original, readable, de-AI'd SEO article targeting "music trivia game".
Angle = the ROUND TYPES a music trivia game can run (name the artist / finish
the lyric / name the year / cover-or-original / name the song from audio), with
this game being the audio round. Deliberately distinct from song-trivia (facts),
guess-the-audio (audio cues), name-that-song (recognition vs recall), and
guess-the-song-in-0-1-second (reveal ladder). Orphaned. Internal links: home + genres.
"""
import os

SRC = "guessable-songs/k-pop/index.html"
DST_DIR = "music-trivia-game"
DST = os.path.join(DST_DIR, "index.html")

s = open(SRC, encoding="utf-8").read()

# --- schema: VideoGame name ---
s = s.replace(
    '"name":"K-Pop Guessable Songs"',
    '"name":"Music Trivia Game"',
)

# --- breadcrumb (keep one) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Genres","item":"https://www.songguesser.co/guessable-songs/"},{"@type":"ListItem","position":3,"name":"K-Pop","item":"https://www.songguesser.co/guessable-songs/k-pop/"}]}',
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Music Trivia Game","item":"https://www.songguesser.co/music-trivia-game/"}]}',
)
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"}]}',
    "",
)

# --- FAQ schema (real user questions, distinct from other pages) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to know the group to play?","acceptedAnswer":{"@type":"Answer","text":"No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."}},{"@type":"Question","name":"How many K-pop guessable songs are in the pool?","acceptedAnswer":{"@type":"Answer","text":"796 tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."}},{"@type":"Question","name":"Is the K-pop quiz in English or Korean?","acceptedAnswer":{"@type":"Answer","text":"The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."}}]}',
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What rounds does a music trivia game have?","acceptedAnswer":{"@type":"Answer","text":"Most mix five kinds of questions: name the artist, finish the lyric, name the year, cover-or-original, and name the song from audio. This game is all-in on the last one."}},{"@type":"Question","name":"Is naming a song from audio really trivia?","acceptedAnswer":{"@type":"Answer","text":"Yes — it\'s the listening version. You\'re answering a question about a song; the question is just the song itself instead of a written clue."}},{"@type":"Question","name":"What\'s the hardest round in a music trivia game?","acceptedAnswer":{"@type":"Answer","text":"The audio round. There\'s nothing to guess at — you either recognize the sliver or you don\'t. Written questions at least give you the words to work with."}},{"@type":"Question","name":"Can I play with different genres?","acceptedAnswer":{"@type":"Answer","text":"Yes. Filter by genre, decade or artist, so every round draws from the music you actually know."}},{"@type":"Question","name":"Do I type the answer or pick from choices?","acceptedAnswer":{"@type":"Answer","text":"You type the title. If you know part of it, the search box matches as you go."}},{"@type":"Question","name":"Is the music trivia game free?","acceptedAnswer":{"@type":"Answer","text":"Yes. In the browser, no signup, no download, no daily limit."}}]}',
)

# --- hero h1 + subtitle ---
s = s.replace(
    '<h1 id="songspot-heading">K-Pop Guessable Songs</h1>',
    '<h1 id="songspot-heading">Music Trivia Game</h1>',
)
s = s.replace(
    '<p>Group hooks, polished production, a first beat — name the K-pop <a href="/guessable-songs/">guessable songs</a> in a second flat.</p>',
    '<p>A music trivia game can ask five different things. This one asks the hardest — name the song from a sliver of audio.</p>',
)

# --- title / description / canonical / og / twitter (+ VideoGame desc & url) ---
s = s.replace(
    "K-Pop Guessable Songs | Song Guesser",
    "Music Trivia Game — Name the Song From a Sliver of Audio | Song Guesser",
)
s = s.replace(
    "Name the k-pop guessable songs from a 0.1-second clip. Free browser game with 796 K-Pop guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.",
    "What rounds does a music trivia game run? Name the artist, finish the lyric, name the year, cover-or-original — and name the song from audio. Play the audio round free.",
)
s = s.replace(
    "https://www.songguesser.co/guessable-songs/k-pop/",
    "https://www.songguesser.co/music-trivia-game/",
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
<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Music trivia game</p><h2>What Is a Music Trivia Game?</h2><p>A music trivia game is any game that turns what you know about music into a score. The questions can be about anything — a voice, a year, a lyric, a cover. What makes it a game instead of a quiz is the loop: a question, an answer, points, and the pull to go one more round.</p></div><p>This one runs the audio round. It plays a sliver of a real song and you name the title. No written clue, no multiple choice — just the sound and your memory. Free, in the browser, no account. It lives on <a href="/">Song Guesser</a>.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The round types</p><h2>The Rounds a Music Trivia Game Can Run</h2><p>Every music trivia game is a mix of five kinds of questions. Most games pick a few; this one is all-in on the fifth.</p></div><ul class="round-map">
<li><strong>Name the artist</strong><span>The most common round: hear a voice or a band and name who it is. Recognition, one step removed from the song.</span></li>
<li><strong>Finish the lyric</strong><span>One line, cut off. You supply the next word. A memory test, not a listening test.</span></li>
<li><strong>Name the year</strong><span>The song plays or the title's given, and you date it. This is where the trivia nerds clean up.</span></li>
<li><strong>Cover or original</strong><span>Two versions of one song. The question is which came first — or which one you're hearing.</span></li>
<li><strong>Name the song</strong><span>The audio round. A sliver of a real track, and you name the title. The hardest of the five, because there's no clue but the sound itself.</span></li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The audio round</p><h2>How the Audio Round Works</h2><p>Every round starts at a tenth of a second — a drum hit, a breath, a chord attack. You type the title, and the clip only gets longer if you ask for it. Each extra length costs points, so the whole round is a bet on how little you need to hear.</p></div><p>The difference from a written question is that there's nothing to guess at. You either recognize it or you don't. That's what makes it the hardest round in the mix.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The rotation</p><h2>The Audio Round, by Genre</h2><p>Eight genres anchor the rotation. Here's how hard the audio round hits in each.</p></div><div class="songspot-feature-grid">
<article><span class="icon">💿</span><h3><a href="/guessable-songs/pop/">Pop</a></h3><p>The easiest round. Hooks are engineered to be caught, so most pop songs name themselves fast.</p></article>
<article><span class="icon">🎤</span><h3><a href="/guessable-songs/hip-hop/">Hip-Hop</a></h3><p>A fair round. The beat and the ad-lib are strong tells, but deep cuts still trip you.</p></article>
<article><span class="icon">🎸</span><h3><a href="/guessable-songs/rock/">Rock</a></h3><p>The riff round. A recognizable riff is an instant answer; a mid-tempo verse is anyone's guess.</p></article>
<article><span class="icon">🎹</span><h3><a href="/guessable-songs/r-and-b/">R&B</a></h3><p>The voice round. Distinct voices make it easy; the era is the hard part.</p></article>
<article><span class="icon">💃</span><h3><a href="/guessable-songs/electronic/">Electronic</a></h3><p>The hardest round. Texture is subtle, and one synth sounds like a hundred others.</p></article>
<article><span class="icon">🤠</span><h3><a href="/guessable-songs/country/">Country</a></h3><p>The story round. Strong openings make it fair, but the catalog runs deep.</p></article>
<article><span class="icon">🪩</span><h3><a href="/guessable-songs/k-pop/">K-Pop</a></h3><p>The drop round. Idol production is loud and distinct, but the group is the real question.</p></article>
<article><span class="icon">🎺</span><h3><a href="/guessable-songs/metal/">Metal</a></h3><p>The speed round. Tempo and gain name the subgenre fast, then you're guessing the band.</p></article>
</div></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Get better fast</p><h2>Tips That Actually Work</h2></div><ul class="kpop-facts">
<li>Know which round you're weak at. If you can name artists but not years, the audio round will expose it.</li>
<li>In the audio round, the first half second is a texture, not a melody. Read the drums and the era.</li>
<li>Lock a genre to make it fair. The audio round is brutal across a random mix.</li>
<li>The artist filter turns a five-question game into one: you're just matching the voice.</li>
<li>Don't treat points as the score. The real score is how little audio you needed.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The full story</p><h2>Every Trivia Game Is One Question, Asked Five Ways</h2></div><p>Strip a music trivia game down and it's one question — what do you know about this music — asked five different ways. Who's singing, what's the line, when was it, which version, and what's the song. The first four give you words. The fifth gives you nothing but sound.</p><p>That's the audio round, and it's the honest one. A written question can be reasoned out. A lyric can be sung through. But a tenth of a second of audio can't be faked — you know it or you don't. It's why the audio round is the one people remember.</p><p>It's free, no account, no daily limit. When you want to narrow it to a genre or decade, head back to <a href="/">Song Guesser</a> and pick a lane.</p></section>

<section id="faq" class="songspot-seo-section songspot-seo-faq"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Questions about this quiz</p><h2>Music Trivia Game FAQ</h2></div><div class="songspot-faq-list">
<details open><summary>What rounds does a music trivia game have?</summary><p>Most mix five kinds of questions: name the artist, finish the lyric, name the year, cover-or-original, and name the song from audio. This game is all-in on the last one.</p></details>
<details><summary>Is naming a song from audio really trivia?</summary><p>Yes — it's the listening version. You're answering a question about a song; the question is just the song itself instead of a written clue.</p></details>
<details><summary>What's the hardest round in a music trivia game?</summary><p>The audio round. There's nothing to guess at — you either recognize the sliver or you don't. Written questions at least give you the words to work with.</p></details>
<details><summary>Can I play with different genres?</summary><p>Yes. Filter by genre, decade or artist, so every round draws from the music you actually know.</p></details>
<details><summary>Do I type the answer or pick from choices?</summary><p>You type the title. If you know part of it, the search box matches as you go.</p></details>
<details><summary>Is the music trivia game free?</summary><p>Yes. In the browser, no signup, no download, no daily limit.</p></details>
</div></section>

<section class="songspot-seo-cta">
<p class="songspot-seo-eyebrow">The fifth round</p>
<h2>Music Trivia Game</h2>
<p>Press play and run the one round that can't be faked — name the song from a sliver.</p>
<a href="#play">Start guessing →</a>
</section>
</section>'''

s = s[:start] + article + "\n\n" + s[end:]

# --- styles for the new lists ---
s = s.replace(
    "</head>",
    "<style>\n.songspot-seo ul.kpop-facts{list-style:none;padding:0;margin:0;display:grid;gap:14px}\n.songspot-seo ul.kpop-facts li{position:relative;padding-left:30px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.kpop-facts li::before{content:\"\\2022\";position:absolute;left:0;top:2px;color:var(--green2)}\n.songspot-seo ul.round-map{list-style:none;padding:0;margin:0;display:grid;gap:16px}\n.songspot-seo ul.round-map li{display:grid;grid-template-columns:140px 1fr;gap:14px;align-items:start}\n.songspot-seo ul.round-map strong{color:var(--green2);font-size:15px;font-weight:600}\n.songspot-seo ul.round-map span{color:#9da8a0;font-size:15px;line-height:1.8}\n</style>\n</head>",
)

os.makedirs(DST_DIR, exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)

# --- runnable check ---
out = s
assert "Music Trivia Game" in out, "title/h1 missing"
assert "K-Pop Guessable Songs" not in out, "old title leaked"
assert "music-trivia-game" in out, "canonical missing"
assert '<section class="songspot-shell"' in out, "game shell missing"
assert "window.SONG_INITIAL" in out, "game script missing"
assert "window.SONG_INITIAL = {}" in out, "generic genre not applied"
assert '"@type":"VideoGame"' in out, "VideoGame schema missing"
assert '"name":"Music Trivia Game"' in out, "VideoGame name missing"
assert '"@type":"FAQPage"' in out, "FAQ schema missing"
assert out.count("<article>") == 8, "genre cards"
assert out.count("<details") == 6, "FAQ entries"
assert out.count("<h1") == 1, "h1 count"
for i in ("difficultyList", "difficultyTabs", "stageChips", "volume", "rerollBtn"):
    assert 'id="%s"' % i in out, "missing id " + i
print("OK ->", DST, len(out), "bytes")
