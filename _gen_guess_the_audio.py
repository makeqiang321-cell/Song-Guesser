# -*- coding: utf-8 -*-
"""Generate /guess-the-audio/ — a full generic game page (all genres) + an
original, readable, de-AI'd SEO article targeting "guess the audio".
Angle = the AUDIO dimension (the physics/psychology of hearing short clips +
the audio cues that give a song away). Deliberately does NOT reuse the
clip-length reveal map, stats table, tips, genre cards or FAQ from
/name-that-song/. Orphaned. Internal links: homepage + genre pages.
"""
import os

SRC = "guessable-songs/k-pop/index.html"
DST_DIR = "guess-the-audio"
DST = os.path.join(DST_DIR, "index.html")

s = open(SRC, encoding="utf-8").read()

# --- schema: VideoGame name ---
s = s.replace(
    '"name":"K-Pop Guessable Songs"',
    '"name":"Guess the Audio"',
)

# --- breadcrumb (keep one) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Genres","item":"https://www.songguesser.co/guessable-songs/"},{"@type":"ListItem","position":3,"name":"K-Pop","item":"https://www.songguesser.co/guessable-songs/k-pop/"}]}',
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Guess the Audio","item":"https://www.songguesser.co/guess-the-audio/"}]}',
)
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"}]}',
    "",
)

# --- FAQ schema (real user questions, distinct from other pages) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to know the group to play?","acceptedAnswer":{"@type":"Answer","text":"No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."}},{"@type":"Question","name":"How many K-pop guessable songs are in the pool?","acceptedAnswer":{"@type":"Answer","text":"796 tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."}},{"@type":"Question","name":"Is the K-pop quiz in English or Korean?","acceptedAnswer":{"@type":"Answer","text":"The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."}}]}',
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is guess the audio only songs, or other sounds too?","acceptedAnswer":{"@type":"Answer","text":"Songs. Real recordings, cut short — not sound effects or re-recorded clips. The audio is the actual track you\'d hear on streaming, just trimmed down."}},{"@type":"Question","name":"Why is 0.1 seconds of audio harder than a normal song quiz?","acceptedAnswer":{"@type":"Answer","text":"Because a tenth of a second is an attack, not a melody — a drum hit, a pick, a breath. You\'re reading texture and era, not the tune. The melody only shows up once you reveal more."}},{"@type":"Question","name":"Does listening with headphones change the answer?","acceptedAnswer":{"@type":"Answer","text":"It changes what you can hear. Stereo separation and a clean low end make the mix — and therefore the era and genre — easier to place. Speakers work fine, but the bass gets muddier."}},{"@type":"Question","name":"How many songs are in the audio pool?","acceptedAnswer":{"@type":"Answer","text":"Thousands, across eight genres and five decades. There\'s no daily limit, so the rotation keeps going as long as you do."}},{"@type":"Question","name":"What counts as a correct guess?","acceptedAnswer":{"@type":"Answer","text":"The title has to match. The search box matches as you type, so getting close is usually enough to find the exact one."}},{"@type":"Question","name":"Can I guess the audio with a friend?","acceptedAnswer":{"@type":"Answer","text":"It\'s a single-player quiz, but it\'s built for passing a phone back and forth. No login, no lobby, no setup."}}]}',
)

# --- hero h1 + subtitle ---
s = s.replace(
    '<h1 id="songspot-heading">K-Pop Guessable Songs</h1>',
    '<h1 id="songspot-heading">Guess the Audio</h1>',
)
s = s.replace(
    '<p>Group hooks, polished production, a first beat — name the K-pop <a href="/guessable-songs/">guessable songs</a> in a second flat.</p>',
    '<p>No words, no title, no hints — just a tenth of a second of sound. Guess the audio, and unlock more only when you have to.</p>',
)

# --- title / description / canonical / og / twitter (+ VideoGame desc & url) ---
s = s.replace(
    "K-Pop Guessable Songs | Song Guesser",
    "Guess the Audio — Guess Songs From a 0.1-Second Audio Clip | Song Guesser",
)
s = s.replace(
    "Name the k-pop guessable songs from a 0.1-second clip. Free browser game with 796 K-Pop guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.",
    "Guess the audio from a tenth of a second of real sound. Free browser quiz — identify the song from the mix, the drums and the timbre, and unlock more audio only when you're stuck.",
)
s = s.replace(
    "https://www.songguesser.co/guessable-songs/k-pop/",
    "https://www.songguesser.co/guess-the-audio/",
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
<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Guess the audio</p><h2>What Is Guess the Audio?</h2><p>Guess the Audio is a listening quiz, not a trivia quiz. There's no question on screen, no multiple choice, no lyric to read. There's just audio — a tenth of a second of a real song, cut from the actual recording. You listen, and you type the title it belongs to.</p></div><p>If you can't get it, press play again and the clip opens up: 0.5 seconds, 2, 8, then 15. Each reveal costs points, so a good run is a run where you need as little audio as possible. The game doesn't stop after one song, either — no daily lock, no account. It's one of the free quizzes over at <a href="/">Song Guesser</a>.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The science</p><h2>Why a Tenth of a Second Is So Hard</h2><p>Your ear hears more than your brain can name, and that gap is the whole game.</p></div><ul class="audio-cues">
<li><strong>Echoic memory</strong><span>Your brain keeps raw sound for a few seconds after it stops. That's why a tenth of a second keeps ringing in your head even after the clip cuts.</span></li>
<li><strong>The transient</strong><span>The first hundred milliseconds of a recording is an attack — a drum hit, a pick, a breath. You're reading texture, not tune.</span></li>
<li><strong>Hook window</strong><span>Pop hooks are engineered to land in one to two seconds. That's why 2s feels so much easier than 0.5s — you've crossed into the hook.</span></li>
<li><strong>Headphones</strong><span>Stereo separation and a clean low end change what you can hear. On speakers the bass goes muddy; on headphones the era comes through.</span></li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The audio cues</p><h2>The Audio Cues That Give a Song Away</h2><p>A tenth of a second is never enough for a melody. What it does give you is a cue — one detail of the recording. Here are the ones that do the heavy lifting.</p></div><ul class="audio-cues">
<li><strong>Drums</strong><span>A drum fill or a kick pattern names the genre and era before anything else. A boom-bap loop is 90s hip-hop; a four-on-the-floor kick is dance.</span></li>
<li><strong>Bass</strong><span>The bass line is the fingerprint. Funk, hip-hop and disco are identified by the low end before the melody shows up.</span></li>
<li><strong>Synth patch</strong><span>A signature synth sound or preset can name the producer or the decade. The 80s gated snare, the 2010s supersaw — one stab is enough.</span></li>
<li><strong>Vocal timbre</strong><span>The first breath or syllable gives away the singer faster than any lyric. You know the voice before you know the words.</span></li>
<li><strong>Production era</strong><span>The reverb, the loudness, the drum machine — how a track is produced dates it instantly, even on a fragment you've never heard.</span></li>
<li><strong>Intro type</strong><span>A cold open, a fade-in, a chant, a count-in. The way a song starts is a tell all by itself.</span></li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The rotation</p><h2>What Each Genre's Audio Sounds Like</h2><p>Eight genres anchor the pool. Each one leaves a fingerprint in the first half second.</p></div><div class="songspot-feature-grid">
<article><span class="icon">💿</span><h3><a href="/guessable-songs/pop/">Pop</a></h3><p>Mixed loud and compressed, so the vocal sits right on top. You usually hear the hook before you hear the band.</p></article>
<article><span class="icon">🎤</span><h3><a href="/guessable-songs/hip-hop/">Hip-Hop</a></h3><p>An 808 and a hi-hat roll. The drum pattern is the signature — more identifying than the melody.</p></article>
<article><span class="icon">🎸</span><h3><a href="/guessable-songs/rock/">Rock</a></h3><p>Mic'd amps and a live room. You hear the space the band recorded in, not just the notes.</p></article>
<article><span class="icon">🎹</span><h3><a href="/guessable-songs/r-and-b/">R&B</a></h3><p>Reverb and a breathy vocal. The singer breathes into the mic, and that breath is the tell.</p></article>
<article><span class="icon">💃</span><h3><a href="/guessable-songs/electronic/">Electronic</a></h3><p>A filter sweep or a sidechain pump. The mix moves in a way acoustic instruments never do.</p></article>
<article><span class="icon">🤠</span><h3><a href="/guessable-songs/country/">Country</a></h3><p>Open strings and twang. The guitar is tuned and played to say "country" in a single note.</p></article>
<article><span class="icon">🪩</span><h3><a href="/guessable-songs/k-pop/">K-Pop</a></h3><p>Production that never sits still — the intro is a hook, the pre-chorus is a hook, and the drop is another one.</p></article>
<article><span class="icon">🎺</span><h3><a href="/guessable-songs/metal/">Metal</a></h3><p>Speed and gain. The rhythm guitar carries the melody, and the tempo names the subgenre before the vocal does.</p></article>
</div></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Get better fast</p><h2>How to Get Better at Guessing Audio</h2></div><ul class="kpop-facts">
<li>Turn the volume up before you skip. At 0.1s, the bass is doing more identifying than the melody.</li>
<li>Use headphones. Stereo separation and a clean low end make the era obvious.</li>
<li>Name the genre and decade first, then the title. Two small guesses are easier than one big one.</li>
<li>If the first thing you hear is bass, it's usually hip-hop, funk, or dance. Narrow from there.</li>
<li>A breath before the vocal means the singer is a beat away — the 0.5s reveal is worth taking.</li>
<li>On Expert, the audio is a deep cut on purpose. Guessing the era is a better bet than guessing the title cold.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">The full story</p><h2>You Hear the Song Before You Remember It</h2></div><p>Guessing audio works backwards from how we normally know music. You don't start from a title and find the sound — you start from half a second of sound and work back to the title. It's the same reason you can recognize a song on the radio before you can name it. The ear gets there first; the words catch up.</p><p>That's why the game is less about how many songs you know and more about how much of the recording your ear has learned to read. A compressed pop mix, an 808, a roomy rock drum — those are signatures. Once your ear knows them, a tenth of a second stops being random noise and turns into a clue.</p><p>It's free, there's no account, and there's no daily limit. Run a few rounds to warm up your ear or go until you stop. When you want the genre-by-genre version, head back to <a href="/">Song Guesser</a> and pick a lane.</p></section>

<section id="faq" class="songspot-seo-section songspot-seo-faq"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Questions about this quiz</p><h2>Guess the Audio FAQ</h2></div><div class="songspot-faq-list">
<details open><summary>Is "guess the audio" only songs, or other sounds too?</summary><p>Songs. Real recordings, cut short — not sound effects or re-recorded clips. The audio is the actual track you'd hear on streaming, just trimmed down.</p></details>
<details><summary>Why is 0.1 seconds of audio harder than a normal song quiz?</summary><p>Because a tenth of a second is an attack, not a melody — a drum hit, a pick, a breath. You're reading texture and era, not the tune. The melody only shows up once you reveal more.</p></details>
<details><summary>Does listening with headphones change the answer?</summary><p>It changes what you can hear. Stereo separation and a clean low end make the mix — and therefore the era and genre — easier to place. Speakers work fine, but the bass gets muddier.</p></details>
<details><summary>How many songs are in the audio pool?</summary><p>Thousands, across eight genres and five decades. There's no daily limit, so the rotation keeps going as long as you do.</p></details>
<details><summary>What counts as a correct guess?</summary><p>The title has to match. The search box matches as you type, so getting close is usually enough to find the exact one.</p></details>
<details><summary>Can I guess the audio with a friend?</summary><p>It's a single-player quiz, but it's built for passing a phone back and forth. No login, no lobby, no setup.</p></details>
</div></section>

<section class="songspot-seo-cta">
<p class="songspot-seo-eyebrow">How little audio do you need?</p>
<h2>Guess the Audio</h2>
<p>Open the quiz and see how much of a recording your ear can actually read.</p>
<a href="#play">Start playing →</a>
</section>
</section>'''

s = s[:start] + article + "\n\n" + s[end:]

# --- styles for the new lists ---
s = s.replace(
    "</head>",
    "<style>\n.songspot-seo ul.kpop-facts{list-style:none;padding:0;margin:0;display:grid;gap:14px}\n.songspot-seo ul.kpop-facts li{position:relative;padding-left:30px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.kpop-facts li::before{content:\"\\2022\";position:absolute;left:0;top:2px;color:var(--green2)}\n.songspot-seo ul.audio-cues{list-style:none;padding:0;margin:0;display:grid;gap:16px}\n.songspot-seo ul.audio-cues li{display:grid;grid-template-columns:120px 1fr;gap:14px;align-items:start}\n.songspot-seo ul.audio-cues strong{color:var(--green2);font-size:15px;font-weight:600}\n.songspot-seo ul.audio-cues span{color:#9da8a0;font-size:15px;line-height:1.8}\n</style>\n</head>",
)

os.makedirs(DST_DIR, exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)

# --- runnable check ---
out = s
assert "Guess the Audio" in out, "title/h1 missing"
assert "K-Pop Guessable Songs" not in out, "old title leaked"
assert "guess-the-audio" in out, "canonical missing"
assert '<section class="songspot-shell"' in out, "game shell missing"
assert "window.SONG_INITIAL" in out, "game script missing"
assert "window.SONG_INITIAL = {}" in out, "generic genre not applied"
assert '"@type":"VideoGame"' in out, "VideoGame schema missing"
assert '"name":"Guess the Audio"' in out, "VideoGame name missing"
assert '"@type":"FAQPage"' in out, "FAQ schema missing"
assert out.count("<article>") == 8, "genre cards"
assert out.count("<details") == 6, "FAQ entries"
assert out.count("<h1") == 1, "h1 count"
for i in ("difficultyList", "difficultyTabs", "stageChips", "volume", "rerollBtn"):
    assert 'id="%s"' % i in out, "missing id " + i
print("OK ->", DST, len(out), "bytes")
