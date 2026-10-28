# -*- coding: utf-8 -*-
"""Generate /name-that-song/ — a full generic game page (all genres) + an
original, readable, de-AI'd SEO article targeting "name that song".
Angle = WHY YOU RECOGNIZE A SONG BUT CAN'T NAME IT (recognition vs recall,
tip-of-the-tongue). Deliberately does NOT reuse the reveal-ladder
(guess-the-song-in-0-1-second) or the audio-cues list (guess-the-audio).
Orphaned. Internal links: homepage + genre pages.
"""
import os

SRC = "guessable-songs/k-pop/index.html"
DST_DIR = "name-that-song"
DST = os.path.join(DST_DIR, "index.html")

s = open(SRC, encoding="utf-8").read()

# --- schema: VideoGame name ---
s = s.replace(
    '"name":"K-Pop Guessable Songs"',
    '"name":"Name That Song"',
)

# --- breadcrumb (keep one) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Genres","item":"https://www.songguesser.co/guessable-songs/"},{"@type":"ListItem","position":3,"name":"K-Pop","item":"https://www.songguesser.co/guessable-songs/k-pop/"}]}',
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Name That Song","item":"https://www.songguesser.co/name-that-song/"}]}',
)
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"}]}',
    "",
)

# --- FAQ schema (real user questions, distinct from other pages) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to know the group to play?","acceptedAnswer":{"@type":"Answer","text":"No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."}},{"@type":"Question","name":"How many K-pop guessable songs are in the pool?","acceptedAnswer":{"@type":"Answer","text":"796 tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."}},{"@type":"Question","name":"Is the K-pop quiz in English or Korean?","acceptedAnswer":{"@type":"Answer","text":"The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."}}]}',
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Why can I recognize a song but not remember its title?","acceptedAnswer":{"@type":"Answer","text":"Recognition and recall are different brain jobs. Recognition is instant; recall is a search. You can know the tune cold and still draw a blank on the name — that\'s the tip-of-the-tongue state, and this game is practice pulling the name out."}},{"@type":"Question","name":"Is this a lyrics quiz or an audio quiz?","acceptedAnswer":{"@type":"Answer","text":"Audio. You name the song from what you hear, not from printed words. There\'s no lyric to read and no question on screen."}},{"@type":"Question","name":"What if I only know part of the title?","acceptedAnswer":{"@type":"Answer","text":"Type the part you know. The search box matches as you go, so one word — or even a few letters — is often enough."}},{"@type":"Question","name":"Does naming the artist help me name the song?","acceptedAnswer":{"@type":"Answer","text":"Usually, yes. Your brain files music by artist first, so locking the artist narrows the search and the title comes faster."}},{"@type":"Question","name":"Why do I blank on titles I clearly know?","acceptedAnswer":{"@type":"Answer","text":"Because you almost never rehearse the title. Streaming shows it, but you don\'t read it — you hear the song. The title is the least practiced part of the memory."}},{"@type":"Question","name":"Is it free, or do I need to sign up?","acceptedAnswer":{"@type":"Answer","text":"Free, in the browser, no signup, no download, no daily limit."}}]}',
)

# --- hero h1 + subtitle ---
s = s.replace(
    '<h1 id="songspot-heading">K-Pop Guessable Songs</h1>',
    '<h1 id="songspot-heading">Name That Song</h1>',
)
s = s.replace(
    '<p>Group hooks, polished production, a first beat — name the K-pop <a href="/guessable-songs/">guessable songs</a> in a second flat.</p>',
    '<p>You know the tune. You can hum it. The title is right there and won\'t come out — name it anyway.</p>',
)

# --- title / description / canonical / og / twitter (+ VideoGame desc & url) ---
s = s.replace(
    "K-Pop Guessable Songs | Song Guesser",
    "Name That Song — Why You Know the Tune but Can't Name It | Song Guesser",
)
s = s.replace(
    "Name the k-pop guessable songs from a 0.1-second clip. Free browser game with 796 K-Pop guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.",
    "Name that song from a sliver of audio. Free browser quiz that trains the one skill that matters: pulling a title out of memory when you know the tune cold.",
)
s = s.replace(
    "https://www.songguesser.co/guessable-songs/k-pop/",
    "https://www.songguesser.co/name-that-song/",
)

# --- make the game generic (all genres) instead of K-Pop ---
s = s.replace(
    'window.SONG_INITIAL = {"genre":51}',
    'window.SONG_INITIAL = {}',
)

# --- swap the SEO sections (keep the game shell + scripts) ---
start = s.index('<section class="songspot-seo">')
end = s.index('<footer class="songspot-site-footer">')
article = '''<section class="songspot-seo">
<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Name that song</p><h2>What Is Name That Song?</h2><p>Name That Song is a quiz about the gap between knowing a song and naming it. Every round plays a sliver of a real track, and your job is to type the title. Not pick it from four buttons — actually type it, straight from whatever your memory hands you.</p></div><p>That gap is the interesting part. You'll recognize songs you can't name, and you'll name songs you'd swear you'd forgotten. Each round starts short and opens up when you press play again, so the real score is how little audio you needed before the title finally dropped. It runs right here on <a href="/">Song Guesser</a>, free and unlimited.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The stuck feeling</p><h2>Why You Recognize a Song but Can't Name It</h2><p>If you've ever hummed a chorus at a friend and drawn a total blank on the title, this is why.</p></div><ul class="recall-map">
<li><strong>Recognition</strong><span>Recognizing a song is instant and automatic. The melody matches a pattern in your head and you just know it's familiar — no effort, no words needed.</span></li>
<li><strong>Recall</strong><span>Naming it is a search. Your brain has to retrieve a specific label, and that's a slower, fiddlier job than recognizing the tune.</span></li>
<li><strong>Tip of the tongue</strong><span>That stuck feeling where the song is fully there but the title won't come. It's not a broken memory — the label is just temporarily out of reach.</span></li>
<li><strong>The title</strong><span>You almost never rehearse a song's title. You hear the song, you read nothing. So the title is the least practiced part of the memory, and the first to go blank.</span></li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Unstick it</p><h2>How to Pull the Title Out</h2><p>When the tune is there and the name won't surface, these are the moves that get it back.</p></div><ul class="kpop-facts">
<li>Name the era first, then the artist, then the title. Memory files songs in that order.</li>
<li>Sing the next line. The lyric that follows the clip usually drags the title along with it.</li>
<li>Think of the album cover or the music video. A title lives in context, not in isolation.</li>
<li>If the title won't come, type part of it. The search box finishes what your memory starts.</li>
<li>Don't force it. Tip-of-the-tongue clears the moment you stop pressing.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The rotation</p><h2>What Each Genre's Titles Sound Like</h2><p>Eight genres anchor the pool. Each one names its songs in a different way.</p></div><div class="songspot-feature-grid">
<article><span class="icon">💿</span><h3><a href="/guessable-songs/pop/">Pop</a></h3><p>Titles are built to be chanted. One word, repeated — that's the hook and the name in one.</p></article>
<article><span class="icon">🎤</span><h3><a href="/guessable-songs/hip-hop/">Hip-Hop</a></h3><p>Titles usually come from the hook or the ad-lib. Say the phrase and you've typed the name.</p></article>
<article><span class="icon">🎸</span><h3><a href="/guessable-songs/rock/">Rock</a></h3><p>Titles lean on imagery. One strong image sticks even when the riff doesn't.</p></article>
<article><span class="icon">🎹</span><h3><a href="/guessable-songs/r-and-b/">R&B</a></h3><p>Titles are the most-sung line. The melody and the name are the same thing.</p></article>
<article><span class="icon">💃</span><h3><a href="/guessable-songs/electronic/">Electronic</a></h3><p>Titles are short and abstract. Easy to hear, annoying to spell.</p></article>
<article><span class="icon">🤠</span><h3><a href="/guessable-songs/country/">Country</a></h3><p>Titles are a whole story in four words. The punchline is the name.</p></article>
<article><span class="icon">🪩</span><h3><a href="/guessable-songs/k-pop/">K-Pop</a></h3><p>Titles mix Korean and English. You'll know the hook and blank on the romanized spelling.</p></article>
<article><span class="icon">🎺</span><h3><a href="/guessable-songs/metal/">Metal</a></h3><p>Titles are long and specific. You remember the one word that stuck, not the full name.</p></article>
</div></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Get better fast</p><h2>Tips That Actually Work</h2></div><ul class="kpop-facts">
<li>If you can sing the hook but not the title, the title is usually inside the hook. Say the words out loud.</li>
<li>Name the artist first. The title comes faster once the artist is in place.</li>
<li>The search box isn't cheating. Type the first syllable and let it match.</li>
<li>Don't sit on a stuck title. Skip once, hear more, and it usually drops in.</li>
<li>Lock the decade filter to narrow the search without giving yourself the answer.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The full story</p><h2>Naming a Song Is the Skill, Not Knowing It</h2></div><p>The songs you can't name aren't the ones you don't know. They're usually the ones you know best — the chorus is right there, you can hum the whole thing, and the title just won't surface. That's the odd part of how music memory works: the tune and the label are stored separately, and the label is always the weaker one.</p><p>The game leans on exactly that gap. The clip plays, you feel the recognition click, and then the work starts — pulling the name out before the audio runs out. Some rounds the title comes instantly. Some rounds you'll sit there knowing you know it, which is a different kind of stuck.</p><p>It's free, no account, no daily limit. Warm up with a few rounds, or keep going until the names come easier. When you want the genre-by-genre version, head back to <a href="/">Song Guesser</a> and pick a lane.</p></section>

<section id="faq" class="songspot-seo-section songspot-seo-faq"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Questions about this quiz</p><h2>Name That Song FAQ</h2></div><div class="songspot-faq-list">
<details open><summary>Why can I recognize a song but not remember its title?</summary><p>Recognition and recall are different brain jobs. Recognition is instant; recall is a search. You can know the tune cold and still draw a blank on the name — that's the tip-of-the-tongue state, and this game is practice pulling the name out.</p></details>
<details><summary>Is this a lyrics quiz or an audio quiz?</summary><p>Audio. You name the song from what you hear, not from printed words. There's no lyric to read and no question on screen.</p></details>
<details><summary>What if I only know part of the title?</summary><p>Type the part you know. The search box matches as you go, so one word — or even a few letters — is often enough.</p></details>
<details><summary>Does naming the artist help me name the song?</summary><p>Usually, yes. Your brain files music by artist first, so locking the artist narrows the search and the title comes faster.</p></details>
<details><summary>Why do I blank on titles I clearly know?</summary><p>Because you almost never rehearse the title. Streaming shows it, but you don't read it — you hear the song. The title is the least practiced part of the memory.</p></details>
<details><summary>Is it free, or do I need to sign up?</summary><p>Free, in the browser, no signup, no download, no daily limit.</p></details>
</div></section>

<section class="songspot-seo-cta">
<p class="songspot-seo-eyebrow">Know the tune, name the song</p>
<h2>Name That Song</h2>
<p>Press play and see how fast the title surfaces from your own memory.</p>
<a href="#play">Start playing →</a>
</section>
</section>'''

s = s[:start] + article + "\n\n" + s[end:]

# --- styles for the new lists ---
s = s.replace(
    "</head>",
    "<style>\n.songspot-seo ul.kpop-facts{list-style:none;padding:0;margin:0;display:grid;gap:14px}\n.songspot-seo ul.kpop-facts li{position:relative;padding-left:30px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.kpop-facts li::before{content:\"\\2022\";position:absolute;left:0;top:2px;color:var(--green2)}\n.songspot-seo ul.recall-map{list-style:none;padding:0;margin:0;display:grid;gap:16px}\n.songspot-seo ul.recall-map li{display:grid;grid-template-columns:140px 1fr;gap:14px;align-items:start}\n.songspot-seo ul.recall-map strong{color:var(--green2);font-size:15px;font-weight:600}\n.songspot-seo ul.recall-map span{color:#9da8a0;font-size:15px;line-height:1.8}\n</style>\n</head>",
)

os.makedirs(DST_DIR, exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)

# --- runnable check ---
out = s
assert "Name That Song" in out, "title/h1 missing"
assert "K-Pop Guessable Songs" not in out, "old title leaked"
assert "name-that-song" in out, "canonical missing"
assert '<section class="songspot-shell"' in out, "game shell missing"
assert "window.SONG_INITIAL" in out, "game script missing"
assert "window.SONG_INITIAL = {}" in out, "generic genre not applied"
assert '"@type":"VideoGame"' in out, "VideoGame schema missing"
assert '"name":"Name That Song"' in out, "VideoGame name missing"
assert '"@type":"FAQPage"' in out, "FAQ schema missing"
assert "reveal" not in out.lower(), "reveal-ladder content leaked"
assert out.count("<article>") == 8, "genre cards"
assert out.count("<details") == 6, "FAQ entries"
assert out.count("<h1") == 1, "h1 count"
for i in ("difficultyList", "difficultyTabs", "stageChips", "volume", "rerollBtn"):
    assert 'id="%s"' % i in out, "missing id " + i
print("OK ->", DST, len(out), "bytes")
