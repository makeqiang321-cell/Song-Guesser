# -*- coding: utf-8 -*-
import os, io, json, re, sys, time, urllib.request, urllib.parse, zlib, html
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
CACHE = os.path.join(BASE, "_songs.json")
TEMPLATE = io.open(os.path.join(BASE, "index.html"), "r", encoding="utf-8").read()
try:
    from _page_rich import RICH
except ImportError:
    RICH = {}

ARTISTS = [
  ("taylor-swift","Taylor Swift",74), ("michael-jackson","Michael Jackson",70),
  ("beyonce","Beyoncé",55), ("rihanna","Rihanna",68), ("drake","Drake",69),
  ("eminem","Eminem",66), ("kanye-west","Kanye West",61), ("justin-bieber","Justin Bieber",69),
  ("the-weeknd","The Weeknd",65), ("linkin-park","Linkin Park",67), ("lady-gaga","Lady Gaga",69),
  ("bruno-mars","Bruno Mars",62), ("adele","Adele",50), ("ariana-grande","Ariana Grande",64),
  ("billie-eilish","Billie Eilish",58), ("ed-sheeran","Ed Sheeran",70), ("coldplay","Coldplay",68),
  ("bts","BTS",75), ("blackpink","BLACKPINK",37), ("gdragon","G-DRAGON",50),
  ("david-guetta","David Guetta",64), ("pitbull","Pitbull",68), ("kendrick-lamar","Kendrick Lamar",62),
  ("olivia-rodrigo","Olivia Rodrigo",50), ("lana-del-rey","Lana Del Rey",52), ("maroon-5","Maroon 5",72),
  ("shakira","Shakira",67), ("travis-scott","Travis Scott",77), ("sabrina-carpenter","Sabrina Carpenter",77),
  ("anuel-aa","Anuel AA",51), ("don-toliver","Don Toliver",65), ("tate-mcrae","Tate McRae",66),
  ("playboi-carti","Playboi Carti",28), ("bad-bunny","Bad Bunny",56), ("katy-perry","Katy Perry",59),
]
GENRES = [
  ("pop","Pop",14,1046), ("rock","Rock",21,672), ("hip-hop","Hip-Hop",18,631),
  ("r-and-b","R&B",15,801), ("k-pop","K-Pop",51,796), ("electronic","Electronic",7,677),
  ("country","Country",6,483), ("metal","Metal",1153,400),
]
DECADES = [
  ("1980s","1980s",103), ("1990s","1990s",133), ("2000s","2000s",204),
  ("2010s","2010s",313), ("2020s","2020s",105),
]

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def js(s):
    return json.dumps(s, ensure_ascii=False)

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode("utf-8"))

def load_songs():
    if os.path.exists(CACHE):
        try:
            return json.load(io.open(CACHE, "r", encoding="utf-8").read())
        except Exception:
            pass
    songs = {"artist":{}, "genre":{}, "decade":{}}
    # artists
    for slug, name, count in ARTISTS:
        try:
            data = fetch_json("https://itunes.apple.com/search?term=" + urllib.parse.quote(name) + "&entity=song&limit=30")
            seen, titles = set(), []
            nl = name.lower()
            for r in data.get("results", []):
                an = (r.get("artistName") or "").lower()
                t = (r.get("trackName") or "").strip()
                k = t.lower()
                if not t or k in seen: continue
                if nl not in an: continue  # skip covers/parodies by other artists
                if '"' in t: continue  # skip AI-spam entries ("From \"Movie\"") that pollute search results
                seen.add(k); titles.append(t)
                if len(titles) >= 12: break
            songs["artist"][slug] = titles
        except Exception as e:
            print("artist fail", name, e)
            songs["artist"][slug] = []
        time.sleep(0.35)
    # genres
    for slug, name, gid, count in GENRES:
        try:
            data = fetch_json("https://itunes.apple.com/us/rss/topsongs/limit=15/genre=%d/json" % gid)
            titles, seen = [], set()
            for e in data.get("feed", {}).get("entry", []):
                t = html.unescape((e.get("im:name", {}) or {}).get("label") or "")
                a = html.unescape((e.get("im:artist", {}) or {}).get("label") or "")
                if not t: continue
                k = t.lower()
                if k in seen or '"' in t: continue
                seen.add(k); titles.append([t, a])
            songs["genre"][slug] = titles[:12]
        except Exception as e:
            print("genre fail", name, e)
            songs["genre"][slug] = []
        time.sleep(0.35)
    # decades (from decades.js)
    try:
        djs = io.open(os.path.join(BASE, "decades.js"), "r", encoding="utf-8").read()
        m = re.search(r'window\.DECADE_TRACKS\s*=\s*(\{.*\});', djs, re.S)
        dd = json.loads(m.group(1))
        for slug, name, count in DECADES:
            songs["decade"][slug] = [[t.get("title",""), t.get("artist","")] for t in dd.get(name, [])][:12]
    except Exception as e:
        print("decade fail", e)
        for slug, name, count in DECADES:
            songs["decade"][slug] = []
    io.open(CACHE, "w", encoding="utf-8").write(json.dumps(songs, ensure_ascii=False))
    return songs

SONGS = load_songs()

# light title cleanup for readability (no re-fetch needed)
def _clean_title(t):
    t = re.sub(r'\s*\[[^\]]*\]', '', t).strip()  # strip [feat. X] / [with Y] credits
    if len(t) > 6 and t.isupper(): t = t.title()  # fix ALL-CAPS, keep short acronyms (DNA, L.A.)
    return t
for _slug in SONGS["artist"]:
    SONGS["artist"][_slug] = [_clean_title(t) for t in SONGS["artist"][_slug]]
for _k in ("genre", "decade"):
    for _slug in SONGS[_k]:
        SONGS[_k][_slug] = [[_clean_title(t), a] for t, a in SONGS[_k][_slug]]

# ---- template anchors ----
T_TITLE = '<title>Song Guesser — Free Song Guessing Game | Guess the Song</title>'
T_DESC = '<meta name="description" content="Song Guesser is a free Heardle-style song guessing game. Name the song from a 0.1-second clip, reveal more when stuck. Five levels, no app, no login." />'
T_CANON = '<link rel="canonical" href="https://www.songguesser.co/" />'
T_OGT = '<meta property="og:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />'
T_OGD = '<meta property="og:description" content="Name the song from a 0.1-second clip. A free Heardle-style song guessing game with five difficulty levels and unlimited rounds." />'
T_OGU = '<meta property="og:url" content="https://www.songguesser.co/" />'
T_TWT = '<meta name="twitter:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />'
T_TWD = '<meta name="twitter:description" content="Name the song from a 0.1-second clip. Free, no signup." />'
T_H1 = '<h1 id="songspot-heading">Song Guesser — Guess the Song in 0.1 Seconds</h1>'
T_HERO = "<p>Song Guesser plays a tenth of a second of a real song — that's your whole clue. You know it or you don't, and you type the title before the clip grows. It's a Heardle-style song guessing game, free in the browser: no app, no login, no daily limit, and the less audio you need, the better you're playing.</p>"
T_VG = '"@type":"VideoGame","name":"Song Guesser","description":"A free Heardle-style song guessing game where you name a track from a 0.1-second clip, then reveal longer clips when you need more."'
T_FAQ_OPEN = '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['

CLOUD_CSS = ('<style>.songspot-song-cloud{list-style:none;display:flex;flex-wrap:wrap;gap:10px;padding:0;margin:6px 0 0}'
  '.songspot-song-cloud li{background:#0b2415;border:1px solid #19df7055;color:#d6f6e1;border-radius:999px;padding:8px 16px;font-size:14px;line-height:1.4}'
  '.songspot-song-cloud li b{color:#19df70;font-weight:600}'
  '.songspot-song-cloud a{color:#d6f6e1;text-decoration:none}'
  '.songspot-song-cloud a:hover{color:#19df70}'
  '.songspot-seo-section+.songspot-seo-section{border-top:1px solid #ffffff0f}</style>\n')

def song_cloud(titles):
    if not titles: return ""
    items = "".join('<li><b>%s</b> — %s</li>' % (esc(t), esc(a)) for t, a in titles)
    return '<ul class="songspot-song-cloud">%s</ul>' % items

def breadcrumb(name, url, mid_name, mid_url):
    return ('<script type="application/ld+json">'
      '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
      '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},'
      '{"@type":"ListItem","position":2,"name":' + js(mid_name) + ',"item":' + js(mid_url) + '},'
      '{"@type":"ListItem","position":3,"name":' + js(name) + ',"item":' + js(url) + '}]}</script>\n')

def _sec(eyebrow, h2, paras, songs):
    ps = ''.join('<p>%s</p>' % p for p in paras)
    c = song_cloud(songs) if songs else ''
    return ('<section class="songspot-seo-section"><div class="songspot-seo-heading">'
      '<p class="songspot-seo-eyebrow">%s</p><h2>%s</h2></div>%s%s</section>\n' % (eyebrow, h2, ps, c))

def challenge_html(name):
    c = RICH.get(name, {}).get('challenge')
    if not c: return ""
    rows = ''.join('<article><span class="icon">%s</span><h3>%s</h3><p>%s</p></article>' % r for r in c['rows'])
    return ('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2><p>%s</p></div>'
      '<div class="songspot-feature-grid">%s</div></section>\n' % (c['eyebrow'], c['h2'], c['intro'], rows))

def listen_html(name):
    l = RICH.get(name, {}).get('listen')
    if not l: return ""
    tips = ''.join('<article><span class="icon">%s</span><h3>%s</h3><p>%s</p></article>' % r for r in l['rows'])
    return ('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2></div>'
      '<div class="songspot-feature-grid">%s</div></section>\n' % (l['eyebrow'], l['h2'], tips))

def _seed(slug):
    return zlib.crc32(slug.encode("utf-8"))

def _trio(ts):
    if len(ts) >= 3: return '“%s”, “%s” and “%s”' % (ts[0], ts[1], ts[2])
    if len(ts) == 2: return '“%s” and “%s”' % (ts[0], ts[1])
    if len(ts) == 1: return '“%s”' % ts[0]
    return ''

def artist_article(name, count, titles, i):
    e = esc(name)
    ts = [esc(t) for t in titles][:8]
    s = _seed(name)
    trio = _trio(ts)
    p1 = [
      'Every %s round pulls from %d tracks, and each one starts at the same length: a tenth of a second. Nothing about the catalog is off limits, so the opening sound has to do the real work.' % (e, count),
      'This %s song quiz keeps one rule: name the track from the shortest clip you can. %d songs are in play, and none of them hands you the chorus first.' % (e, count),
      'How many %s songs can you name from a tenth of a second? The quiz lines up %d of them, from the career-defining hit to the album cut.' % (e, count),
      'The %s pool holds %d songs. That breadth is the test — knowing the singles is not enough once the deep cuts start rolling.' % (e, count),
    ][s % 4]
    if trio:
        p1 += ' Expect %s.' % trio
    p2 = [
      'The first clue is a 0.1-second clip, not a chorus. Miss it and the round opens to 0.5s, 2s, 8s and 15s only when you ask for more.',
      'A %s song can announce itself in a single drum hit, a vocal breath or a synth swell — the trick is catching which before the longer clips give it away.' % e,
      'You will not get the hook first. A tenth of a second opens each round, and every extra reveal you take is a hint you did not need.',
    ][(s >> 3) % 3]
    p3 = [
      'There is no signup, no download and no daily limit. Pick a difficulty, press play, and each solve starts a fresh track from the same %d-song pool.' % count,
      'The game is free in the browser and resets nothing — every round is another shot at naming a %s track from the shortest possible clip.' % e,
    ][(s >> 5) % 2]
    return _sec('The %s song pool' % e, 'Songs in the %s Quiz' % e, [p1, p2, p3], [(x, name) for x in titles[:8]])

def genre_article(name, count, tracks, i):
    e = esc(name)
    pairs = tracks[:8]
    c = GENRE_CONTENT[name]
    fill = lambda s: s.replace('{count}', str(count))
    what = _sec('What they are', 'What Are %s Guessable Songs?' % e, [fill(x) for x in c['what']], None)
    how = _sec('How to play', 'How to Play the %s Quiz' % e, [fill(c['how'])], None)
    hl = _sec('Game highlights', 'The %s Song Pool' % e, [fill(c['highlights'])], pairs)
    return what + challenge_html(name) + hl + listen_html(name) + how

DECADE_STAMP = {
    "1980s": "gated snares, synth pads and chorus-sized guitars",
    "1990s": "grunge fuzz, boom-bap beats and boy-band harmonies",
    "2000s": "ringtone hooks, Auto-Tuned vocals and pop-punk downstrokes",
    "2010s": "EDM drops, trap hi-hats and the “feat.” credit",
    "2020s": "TikTok-sized loops, genre-blurring beats and bedroom pop",
}
DECADE_MOOD = {
    "1980s": "an MTV-era singalong — the decade of the Walkman, the shoulder pad and the arena chorus",
    "1990s": "a dial-up-era time capsule — flannel and gold chains, mixtapes and the last pre-streaming radio",
    "2000s": "a TRL-era countdown — ringtones, MP3 players and the exact moment pop went digital",
    "2010s": "a streaming-era shuffle — festival drops, the “feat.” tag and the year every chorus learned to loop",
    "2020s": "a TikTok-era feed — fifteen-second hooks, genre lines gone and every track built to catch you instantly",
}

GENRE_CONTENT = {
  "Pop": {
    "hero": "Pop songs are built to be caught in half a second. Name the pop guessable songs from a tenth of a second, before the hook gets there first.",
    "what": [
      "Pop is engineered for the half-second test. Songwriters front-load the catchy part — the 'oh-oh-oh', the synth line, the first word of the chorus — because radio and playlists decide in a blink. That's the whole game here: a tenth of a second, and you either know it or you don't.",
      "The pool holds {count} chart songs, so a round swings from a singalong you grew up on to a single from this month. Some open on the catchiest bar on the record; others hide the hook behind a drum fill and make you work for it.",
      "It's a Heardle-style song guessing game at its most direct: one hook, one guess, and the fastest ear wins.",
    ],
    "how": "Hear the slice, type the title, and only reach for more audio when you're truly stuck. Pop rewards the fast answer — your first instinct is usually the right one.",
    "highlights": "Pop's {count} tracks are the fairest door into the game and the fastest pool to clear, because the hooks were literally written to be recognized. When you want a different flavor, the <a href='/'>song guesser</a> switches you to any other genre in one click.",
    "faq": [
      ("Is pop the easiest genre to start with?", "Usually, yes. Pop's guessable songs are written to stick, so the opening slice is often enough. Start here on Easy, then push toward Impossible once the chart-toppers stop feeling like a challenge."),
      ("How many pop guessable songs can I play?", "{count} chart songs rotate through the pool, from long-running classics to the latest releases. You never know which era the next guessable song will land on."),
      ("Do the rounds ever repeat?", "Not on purpose. The pool is large enough that a full session rarely lands the same guessable song twice in a row, and difficulty controls how deep the rotation goes."),
    ],
  },
  "Rock": {
    "hero": "Riffs, drums and a first chord — name the rock guessable songs before the guitar finishes the thought.",
    "what": [
      "Rock gives itself away on the first hit: the chord, the snare, the bend of a solo. A tenth of a second is often enough to tell a Marshall from a Fender, a stadium anthem from a garage cut. Your job is to name the track before the vocal gets a word in.",
      "The {count}-track pool crosses every era of rock, so a round can land on an arena anthem, a grunge growl or a three-chord stomper. The tone does most of the telling — a fuzz pedal, a clean arpeggio, a double-kick.",
      "It's a Heardle-style song guessing game where the clues are riffs, tone and the first hit of the drums, not the lyric.",
    ],
    "how": "Name the song from the opening sound and reach for a longer clip only as a last resort. The riff is doing most of the work; trust it and type.",
    "highlights": "Rock's {count} tracks give themselves away in the tone — a fuzz pedal, a clean Strat or a double-kick names the era before the vocal can. When one genre isn't enough, the <a href='/'>song guesser</a> has the whole catalog under one roof.",
    "faq": [
      ("How do I get better at the rock quiz?", "Listen for the guitar tone and the drum pattern before the melody. A fuzz pedal, a clean arpeggio or a double-kick usually names the decade faster than the chorus does."),
      ("Which rock guessable songs are in the pool?", "{count} tracks across eras, from arena anthems to deep cuts. The rotation mixes classics and modern rock so no round feels the same."),
      ("Is the rock quiz harder than pop?", "Often a little. Rock spans more sub-styles, so the opening sound carries more weight. That is also what makes a fast solve on a guessable song feel earned."),
    ],
  },
  "Hip-Hop": {
    "hero": "The beat, the sample, the producer tag — name the hip-hop guessable songs from the first tenth of a second.",
    "what": [
      "Hip-hop lives in the first beat of the loop. A tenth of a second can give you the snare pattern, the 808, or a producer tag before the rapper even clears their throat — and that's usually enough to name the track.",
      "The {count}-track pool runs from boom-bap to trap to whatever's charting now, so the drum pattern alone won't always place the era. You have to read the sample and the mix too: a dusty loop says one decade, a rattling hi-hat says another.",
      "It's a Heardle-style song guessing game driven by the beat and the bar — the flow only confirms what the drums already told you.",
    ],
    "how": "Let the first beat talk. Type your guess the moment the sample or the hi-hat feels familiar, and ask for more audio only when the era won't place itself.",
    "highlights": "The production is the tell on every hip-hop track: a dusty loop, a boom-bap kick, a rattling trap hi-hat. When you want to roam outside the genre, the <a href='/'>song guesser</a> opens every lane at once.",
    "faq": [
      ("What should I listen for in a hip-hop clip?", "The drum pattern and the sample first. A dusty loop, a boom-bap kick or a rattling trap hi-hat usually places the era before the rapper does."),
      ("How many hip-hop guessable songs are in the rotation?", "{count} tracks, from boom-bap classics to the current chart. The pool mixes eras so the opening beat is always a fresh test."),
      ("Can I play only hip-hop?", "Yes — pick Hip-Hop and every round stays inside the genre. Head to the <a href='/'>song guesser</a> when you want to mix it with pop, R&B or anything else."),
    ],
  },
  "R&B": {
    "hero": "A vocal run, a slow groove, a single breath — name the R&B guessable songs from the voice alone.",
    "what": [
      "R&B is the genre of the run — a voice bending a note before the beat even lands. A tenth of a second is often just that: a breath at the mic, the start of a melisma, a warm chord. If you know the voice, you've already got the song.",
      "The {count}-song pool spans quiet-storm slow jams to current R&B, so a round can lean on the singer, the chord bed, or the pocket of the groove. Some tracks give themselves away on the first hum.",
      "It's a Heardle-style song guessing game where the clue is texture — a breath, a chord, a run — not a lyric.",
    ],
    "how": "Trust the vocal first. A breath, a run or the shape of a chord is usually enough; reveal more only when the groove won't place itself.",
    "highlights": "R&B rewards an ear that knows a voice as well as a hook — its {count} tracks lean on tone over texture. When you're ready to switch lanes, the <a href='/'>song guesser</a> is every genre on one page.",
    "faq": [
      ("What gives an R&B guessable song away fastest?", "The vocal. A run, a breath or the shape of a chord names the track faster than the beat does, so keep your ear on the singer."),
      ("How many R&B guessable songs can I play?", "{count} tracks, from slow jams to the current chart. The rotation stays inside the genre and never repeats on purpose."),
      ("Is R&B harder than pop?", "It can be. R&B leans on subtler clues like vocal tone and chord color, so the opening slice of a guessable song asks a little more of your ear."),
    ],
  },
  "K-Pop": {
    "hero": "Group hooks, polished production, a first beat — name the K-pop guessable songs in a second flat.",
    "what": [
      "K-pop is precision pop: the intro is built to catch you before the first line. A tenth of a second can hand you the synth stab, the chant or the drum hit that gives away the group — sometimes before you even register which track it is.",
      "The {count}-track pool spans generations of groups and soloists, so two songs can share a production trick and still be worlds apart. The tell is in the details: whose voice, whose beat, whose signature drop.",
      "It's a Heardle-style song guessing game locked to a K-pop comeback — the intro is the whole test.",
    ],
    "how": "Name the song from the first beat — the production, the chant or the opening note is usually enough. Ask for more audio only when the group won't give itself away.",
    "highlights": "K-pop intros are built to be recognized in a second, which makes its {count} tracks fast rounds with misses that sting a little more. Want the full catalog? The <a href='/'>song guesser</a> opens every artist and genre.",
    "faq": [
      ("Do I need to know the group to play?", "No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."),
      ("How many K-pop guessable songs are in the pool?", "{count} tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."),
      ("Is the K-pop quiz in English or Korean?", "The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."),
    ],
  },
  "Electronic": {
    "hero": "A build, a bpm, a synth swell — name the electronic guessable songs before the drop lands.",
    "what": [
      "Electronic music runs on tension and release. A tenth of a second at the quiet end of the track still tells you plenty: the tempo (128 says house, 140 says dubstep, 174 says drum and bass), the texture of the bass, the shape of the build. Name it before the drop does.",
      "The {count}-track pool spans house, techno, big-room and everything between, so a kick pattern alone rarely settles it. You have to read the whole texture — the pads, the sidechain pump, the supersaw.",
      "It's a Heardle-style song guessing game where the giveaways are pads, builds and the shape of a drop.",
    ],
    "how": "Lock onto the texture: the synth, the bass and the tempo do the naming. Reveal more only when the drop won't arrive fast enough.",
    "highlights": "Electronic tracks give away their subgenre in the first beat — that's what makes the {count}-track pool fast but unforgiving. For a change of scenery, the <a href='/'>song guesser</a> is every genre under one roof.",
    "faq": [
      ("What should I listen for in an electronic clip?", "The texture — a synth swell, a four-on-the-floor kick or the tempo. The subgenre usually announces itself before the melody of a guessable song does."),
      ("How many electronic guessable songs can I play?", "{count} tracks across house, techno and big-room. The pool stays inside the genre and rotates every round."),
      ("Is the electronic quiz free?", "Yes, like every page on <a href='/'>Song Guesser</a> — it runs in the browser with nothing to install or sign up for."),
    ],
  },
  "Country": {
    "hero": "A twang, a strum, a story — name the country guessable songs before the verse arrives.",
    "what": [
      "Country is storytelling first, and the story usually opens with a guitar. A tenth of a second is often a pedal-steel lick, a fiddle run or a drawled first word — enough to name the track if you know the sound.",
      "The {count}-song pool crosses classic twang and modern country, so a round can lean on the fiddle, the steel guitar or the vocal drawl as much as the melody. The instrumentation usually names the era before the chorus can.",
      "It's a Heardle-style song guessing game where the clues are a strum, a twang and a storyteller's drawl.",
    ],
    "how": "Hear the strum or the drawl and name the song before the verse arrives. Reach for more audio only when the era won't place itself.",
    "highlights": "Country's fingerprints — the fiddle, the steel guitar, the drawl — usually name a track before the chorus can. When you want a different sound, the <a href='/'>song guesser</a> has every genre waiting.",
    "faq": [
      ("What gives a country guessable song away?", "The instrumentation — a fiddle, a steel guitar or a twangy strum. The story takes over later, but the sound names the era first."),
      ("How many country guessable songs are in the rotation?", "{count} tracks, from classic twang to modern country. The pool stays inside the genre and never repeats on purpose."),
      ("Do I need to like country to play?", "No — you just need an ear for it. The game rewards recognizing the sound of a guessable song, not the fandom."),
    ],
  },
  "Metal": {
    "hero": "A riff, a double-kick, a growl — name the metal guessable songs from the attack alone.",
    "what": [
      "Metal is built on the riff, and the riff usually arrives in the first second. A tenth of a second hands you the attack — a down-tuned chug, a blast beat, a growl — and asks you to name the track from it.",
      "The {count}-track pool spans heavy, thrash, death and beyond, so the subgenre is the real test: the tuning, the tempo and the drum pattern tell you whether you're in thrash or death before the vocal does.",
      "It's a Heardle-style song guessing game tuned for the pit, where a chug and a kick do the naming.",
    ],
    "how": "Name the song from the attack — the riff, the double-kick or the growl. Ask for more audio only when the subgenre won't place itself.",
    "highlights": "Metal's signatures — the down-tuned riff, the blast beat, the growl — give a subgenre away in an instant across all {count} tracks. For a change of pace, the <a href='/'>song guesser</a> opens every other genre.",
    "faq": [
      ("What gives a metal guessable song away fastest?", "The riff and the drum pattern. A down-tuned chug, a blast beat or a growl usually names the subgenre before the vocal does."),
      ("How many metal guessable songs can I play?", "{count} tracks across heavy, thrash, death and beyond. The rotation stays inside the genre and mixes sub-styles."),
      ("Is the metal quiz harder?", "It can be — metal subgenres share a lot of DNA, so the opening slice of a guessable song asks you to separate thrash from death by ear alone."),
    ],
  },
}

DECADE_CONTENT = {
  "1980s": {
    "hero": "Name the 1980s song from a tenth of a second — 103 tracks, one rule: catch the gated snare or the synth pad before the arena chorus gives it away.",
    "what": [
      "The 1980s quiz is a Heardle-style song guessing game locked to a single decade. Each round plays a tenth of a second of a real 1980s record — a gated drum, a synth swell, a guitar built for the back row of a stadium — and you name the song before the first word lands. There is no album art, no artist credit and no lyric to lean on, only the sound of the era.",
      "The 1980s is the fairest decade to guess because its production was engineered to announce itself instantly. Gated reverb threw every snare through a cathedral, drum machines kept the tempo rigid, and synth pads filled every gap behind the vocal. If the opening stab sounds bigger than a garage, you are almost certainly in the 1980s.",
      "The pool spans 103 tracks across synth-pop, new wave, glam metal and hip-hop's first wave. The real test is not whether you remember the title — it is whether your ear places the production the instant it hits, before the melody confirms what the drum machine already told you."
    ],
    "how": "Open every round on the shortest clip and trust the first sound before the melody arrives. A gated snare names the 1980s faster than the chorus does, so commit to the title early and type it as it forms. If the first guess misses, the clip steps to 0.5s, 2s, 8s, then 15s — a wrong answer costs you a longer listen, never a restart.",
    "highlights": "The 103-track pool reaches from the synth hook of “Take On Me” to the drum intro of “Billie Jean” to the chorus-sized guitars of “Livin' On a Prayer”. Gated snares and synth pads do most of the telling, so the first stab is often the whole answer. When one decade is not enough, the <a href='/'>song guesser</a> folds all five into a single run.",
    "faq": [
      [
        "How is the 1980s quiz different from a general song quiz?",
        "Every round stays inside one decade, so the clue is the era's production — gated snares, synth pads and arena-sized reverb — rather than any one artist's style. The 103-song pool opens at 0.1 seconds and only widens when you ask."
      ],
      [
        "What should I listen for in a 1980s clip?",
        "The drum sound before the melody. A gated snare or a rigid drum machine usually names the year before the vocal does, because 1980s mixes pushed the drums to the front of the record."
      ],
      [
        "Do I need to know 1980s artists to play?",
        "No. You are matching a sound to a title, not naming a singer. The pool crosses synth-pop, rock, R&B and hip-hop's first wave, so a familiar hook is usually enough even when the artist slips your mind."
      ],
      [
        "Is the 1980s a good decade for beginners?",
        "Yes. The production is loud and the hooks are immediate, so a familiar track usually lands in one or two reveals. Start on Easy and climb toward Impossible once the arena anthems stop feeling like a challenge."
      ]
    ]
  },
  "1990s": {
    "hero": "Flannel fuzz, a boom-bap drum, a boy-band harmony — guess the 1990s song from 0.1 seconds across 133 tracks.",
    "what": [
      "The 1990s quiz is a Heardle-style song guessing game for anyone who still thinks in mixtapes. A grunge riff or a boom-bap loop announces the decade in a sliver of a second, and your only job is to name the track before it names itself.",
      "It is a dial-up-era time capsule — flannel and gold chains, CD booklets and the last stretch of radio before streaming rewired how we listen. All 133 tracks share one stamp: grunge fuzz, boom-bap beats and boy-band harmonies. The quiz rewards an ear that knows the 1990s as a sound, not as a shelf of jewel cases.",
      "Every clip lands somewhere between grunge and the end of the CD era.",
      "What makes the decade tricky is its range. Alternative rock, golden-age hip-hop, R&B and bubblegum pop all charted side by side, so the same opening chord can belong to a mosh pit or a slow jam. You have to place the production, not just recognize the hook."
    ],
    "how": "Treat every solve as a one-second decision. Hear the fuzz or the 808, type the title, and ask for more audio only when the first guess misses. Nothing locks you out and nothing asks for a login — a wrong answer simply hands you a longer clip on the same track.",
    "highlights": "Across 133 tracks — “Smells Like Teen Spirit”, “...Baby One More Time”, “No Scrubs” and beyond — grunge fuzz and boom-bap drums do the telling long before the vocal arrives. When you are ready to leave the decade behind, the <a href='/'>song guesser</a> shuffles all five eras on one page.",
    "faq": [
      [
        "How does the 1990s quiz work?",
        "Each round plays a 0.1-second clip of a real 1990s track, then reveals 0.5s, 2s, 8s and 15s only when you ask. The 133-song pool spans grunge, hip-hop's golden age and boy-band pop, so the opening sound usually places the era on its own."
      ],
      [
        "What gives a 1990s song away fastest?",
        "The production stamp — grunge fuzz, boom-bap drums and boy-band harmonies. Check the guitar tone and the drum pattern before you chase the melody; the decade usually names itself in the first beat."
      ],
      [
        "Is the 1990s harder than the 1980s?",
        "For most people, a little. The 1990s packs more genres into one decade — alternative rock, R&B and hip-hop's golden age — and the difficulty dial runs Easy to Impossible, so you control how hard each round lands."
      ],
      [
        "What if I only know 1990s rap, or only 1990s pop?",
        "The pool mixes grunge, golden-age hip-hop, R&B and boy-band pop, but the difficulty setting steers which songs you cycle through. Pick a level you are comfortable with and the rotation leans toward tracks you already recognize."
      ]
    ]
  },
  "2000s": {
    "hero": "Ringtone hooks, Auto-Tuned vocals, pop-punk downstrokes — guess the 2000s song from 0.1 seconds across 204 tracks.",
    "what": [
      "The 2000s quiz is a guess-song game set in the moment pop went digital, when your ringtone said who you were and the chorus got shorter so the hook could stick faster. The intros are short and loud — a drum fill, an Auto-Tuned vocal, a pop-punk downstroke — and you name the track from the first tenth of a second.",
      "Think TRL at its peak: MP3 players, ringtone sales and the exact season the bridge disappeared. All 204 tracks lean on one sound — ringtone hooks, Auto-Tuned vocals and pop-punk downstrokes — so the real test is whether you can call the song before the chorus shows up to confirm it.",
      "It is a Heardle-style song guessing game pinned to the ringtone-and-MP3 decade.",
      "The 2000s sits between two worlds. Its production still carries the polish of radio, but the loops and vocal effects already point toward streaming. That makes it a fast, loud pool where a single drum fill or a pitch-corrected note often names the year before the melody does."
    ],
    "how": "Open on the shortest clip, answer fast, and skip when a hook will not land. Nothing is time-gated and nothing repeats on purpose — a bad round costs you only a longer clip on the same track, and a good one ends in a single guess.",
    "highlights": "The 204-track pool reaches from “Lose Yourself” to “Hey Ya!” to “Mr. Brightside”. Ringtone hooks and pop-punk downstrokes mean the opening hit usually names the song all by itself. Once the 2000s are cleared, the <a href='/'>song guesser</a> keeps the rest of the catalog on deck.",
    "faq": [
      [
        "What makes the 2000s quiz different?",
        "It is the decade where pop went digital, so the pool is thick with ringtone hooks and Auto-Tuned vocals. 204 tracks stay locked inside one decade, and each round opens at 0.1 seconds before longer reveals unlock."
      ],
      [
        "What should I listen for in a 2000s track?",
        "The production, not the lyrics — ringtone hooks, Auto-Tuned vocals and pop-punk downstrokes are the fingerprint. A single drum fill or a pitch-corrected vocal often names the song before the melody does."
      ],
      [
        "Is the 2000s a good decade to start with?",
        "Yes, especially if you grew up with it. The hooks are loud and the production is clean, so a familiar track usually lands in one or two reveals. New ears can start on Easy and climb from there."
      ],
      [
        "Why do 2000s intros sound so short?",
        "Because pop went digital and the hook was pushed to the front. Ringtone clips and MP3 players trained listeners to decide in seconds, so the intros are short and loud — which happens to suit a 0.1-second opening perfectly."
      ]
    ]
  },
  "2010s": {
    "hero": "EDM drops, trap hi-hats, a “feat.” credit — guess the 2010s song from a tenth of a second across 313 tracks, the biggest decade pool.",
    "what": [
      "This is a Heardle-style song guessing game for the streaming decade. You hear a tenth of a second of a real 2010s record and try to name it before the drop lands — and the artist credit will not save you, because only the sound will.",
      "It is a streaming-era shuffle: festival drops, guest verses, and the year every chorus learned to loop. All 313 tracks are built on one signature — EDM drops, trap hi-hats and the “feat.” credit — so the quiz measures how fast you can place a song from its production alone.",
      "It is a song guessing game aimed at the decade itself, where the drop and the feat. give it away.",
      "The 2010s churned out more chart hits per year than any decade before it, which is why this is the deepest pool by a wide margin. The challenge is not finding a song you know — it is pinning down which of the hundreds of similar drops is the one you are hearing."
    ],
    "how": "Start each track on a sliver and let your ear drive. Widen the clip only when you must — the earlier you commit to a title, the more the round reveals about your actual recall. A hi-hat roll is often enough; the build-up usually settles it.",
    "highlights": "At 313 tracks it is the deepest of the five, running from “Somebody That I Used to Know” to “Uptown Funk” to “Call Me Maybe”. Trap hi-hats and EDM drops give the year away in the first beat. When one decade is not enough, the <a href='/'>song guesser</a> lets you hop between artists, genres and decades mid-run.",
    "faq": [
      [
        "Why does the 2010s quiz have the most songs?",
        "It is the biggest decade pool at 313 tracks, because the streaming era churned out more chart hits per year than any decade before it. Every round still opens at 0.1 seconds and reveals more only when you ask."
      ],
      [
        "What gives a 2010s song away?",
        "Trap hi-hats, EDM drops and the “feat.” credit. The decade built its hits on production signatures — a hi-hat roll or a build-up usually names the track before the chorus arrives."
      ],
      [
        "Is the 2010s quiz free?",
        "Yes. Like every decade round, it runs in the browser with no signup, no download and no daily limit. You can jump between the 1980s and the 2020s in one sitting without ever logging in."
      ],
      [
        "Is the 2010s harder than the 2000s?",
        "In a different way. The sounds sit closer together — so many trap hi-hats and EDM builds — that the real challenge is telling near-identical productions apart, not recognizing the decade itself."
      ]
    ]
  },
  "2020s": {
    "hero": "TikTok-sized loops, genre-blurring beats, bedroom pop — guess the 2020s song from 0.1 seconds across 105 tracks.",
    "what": [
      "The 2020s quiz is a Heardle-style song guessing game for the TikTok decade: fifteen-second hooks, genre lines erased, every track built to catch you before you scroll. You hear a sliver of a real 2020s hit and name it before the loop resets.",
      "Imagine a feed that never stops — a hook that loops in fifteen seconds, a genre that refuses to sit still, a beat tuned to grab you in a heartbeat. All 105 tracks wear one badge: TikTok-sized loops, genre-blurring beats and bedroom pop, so the quiz tests how fast you can place a song that was engineered to be recognized in a second.",
      "It is a song guessing game sized for the feed, where a fifteen-second loop is the whole clue.",
      "What makes the 2020s the hardest decade is that its productions refuse to be pinned down. A single hook can jump from Afrobeats to pop-punk to a whispered bedroom chorus, so the sound is a weaker clue than in any earlier era — and every 0.1-second clip is a genuine test."
    ],
    "how": "Because today's hooks are built to catch you instantly, most rounds end in one guess. Name the track, and if the loop does not place it, the clip stretches until it does. There is no penalty for a miss beyond a longer listen.",
    "highlights": "The 105-track pool spans “Blinding Lights”, “As It Was” and “Anti-Hero”. Because it leans on TikTok-sized loops and genre-blurring beats, the newest decade is the hardest to pin by style alone. The other four decades live on the <a href='/'>song guesser</a>, all playable from the same page.",
    "faq": [
      [
        "Why is the 2020s the hardest decade to pin down?",
        "Because genre lines have collapsed. The 105-song pool jumps from bedroom pop to Afrobeats to pop-punk inside a single hook, so the production is a weaker clue than in any earlier decade — which makes every 0.1-second clip a genuine test."
      ],
      [
        "How does the 2020s quiz work?",
        "Each round plays a 0.1-second clip of a real 2020s track, then reveals 0.5s, 2s, 8s and 15s only when you ask. The pool holds 105 songs and reshuffles every round."
      ],
      [
        "Do I need TikTok to play?",
        "No. You need nothing but a browser. The 2020s pool leans on TikTok-sized hooks, but the game itself has no app, no signup and no download — just open the page and press play."
      ],
      [
        "Why is the 2020s pool smaller than the 2010s?",
        "The decade is still being written. 105 tracks are in rotation today, but the catalog keeps growing as new hits land — which also means the pool refreshes faster than any other era."
      ]
    ]
  }
}

def decade_article(name, count, tracks, i):
    e = esc(name)
    pairs = tracks[:8]
    c = DECADE_CONTENT[name]
    what = _sec('What it is', 'What is the %s Song Quiz?' % e, c['what'], None)
    how = _sec('How to play', 'How to Play the %s Quiz' % e, [c['how']], None)
    hl = _sec('Game highlights', 'The %s Song Pool' % e, [c['highlights']], pairs)
    return what + challenge_html(name) + hl + listen_html(name) + how

def tips_section(cat, name, i, tracks):
    e = esc(name)
    s = _seed(name)
    if cat == 'artist':
        t2 = 'Place the track by its era. %s has moved through several sounds, and the production usually tells you which one you are hearing.' % e
        _ts = [esc(t) for t in tracks]
    elif cat == 'genre':
        t2 = 'Place the track by its subgenre. %s spans many styles, and the drum pattern or synth tone points to the right one.' % e
        _ts = [esc(t) for t, a in tracks]
    else:
        t2 = 'Place the track by its decade. The %s pool is built on %s, so the production usually gives the year away.' % (e, DECADE_STAMP.get(name, "the hooks, drums and synths that defined the decade"))
        _ts = [esc(t) for t, a in tracks]
    first = 'Catch the first sound, not the melody you expect. A drum hit, a vocal breath or a synth swell is often the giveaway.'
    if _ts:
        first += ' In this pool, “%s” is a good test of that opening.' % _ts[0]
    t1v = [
      first,
      'Forget the chorus for a beat and lock onto the very first sound. A drum, a breath or a synth swell usually names the track before the melody does.',
    ][s % 2]
    t4v = [
      'Start typing before you are sure. Suggestions autocomplete from the pool, so part of a title can finish the answer.',
      'Trust your first instinct and type the title as it forms. Autocomplete fills the rest, so a half-remembered name is often enough.',
    ][(s >> 3) % 2]
    tips = [
      ('🎯', 'Catch the first sound', t1v),
      ('🕰️', 'Think in eras', t2),
      ('⏭', 'Reveal sparingly', 'Reveal more only when you must. The 0.5s clip is often enough, and 2s usually settles it.'),
      ('⌨️', 'Type as you listen', t4v),
    ]
    lis = ''.join('<li><span>%02d</span><span class="icon">%s</span><h3>%s</h3><p>%s</p></li>' % (n, ic, h, b) for n, (ic, h, b) in enumerate(tips, 1))
    return ('<section id="how-to-play" class="songspot-seo-section"><div class="songspot-seo-heading">'
      '<p class="songspot-seo-eyebrow">Get better, fast</p>'
      '<h2>How to guess %s songs faster</h2></div>'
      '<ol class="songspot-how-grid">%s</ol></section>\n' % (e, lis))

def faq_qa(cat, name, count, i):
    e = esc(name)
    if cat == 'decade' and name in DECADE_CONTENT:
        return DECADE_CONTENT[name]['faq']
    if cat == 'genre' and name in GENRE_CONTENT:
        return [(q, a.replace('{count}', str(count))) for q, a in GENRE_CONTENT[name]['faq']]
    if cat == 'artist':
        hear = 'Focus on the opening sound — a drum hit, a synth pulse, a piano tone or the shape of the vocal. %s shifts between eras and sounds, so a single instrument rarely settles it alone.' % e
    elif cat == 'genre':
        hear = 'Focus on the opening sound — a drum hit, a synth pulse, a piano tone or the shape of the vocal. %s spans many sub-styles, so the drum pattern and synth tone usually pin it down.' % e
    else:
        hear = 'Focus on the opening sound — a drum hit, a synth pulse, a piano tone or the shape of the vocal. The %s pool is built on %s, so listen for the production stamp of the decade.' % (e, DECADE_STAMP.get(name, "the hooks, drums and synths of that era"))
    q1 = ('How does the %s song game work?' % e,
          'Each round starts with a 0.1-second clip of a %s track and reveals 0.5s, 2s, 8s and 15s only when you ask. The search box stays inside the %s pool of %d songs.' % (e, e, count))
    q2 = ('What should I hear for in a %s music quiz?' % e, hear)
    q3 = ('How many %s songs are in the quiz?' % e,
          '%d playable songs. Difficulty controls how many you cycle through, from Easy to Impossible. Every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.' % count)
    return [q1, q2, q3]

def faq_json(qs):
    import re as _re
    body = ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                    % (js(_re.sub(r'<[^>]+>', '', q)), js(_re.sub(r'<[^>]+>', '', a))) for q, a in qs)
    return '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + body + ']}\n</script>\n'

def faq_extra(cat, name, count, i):
    e = esc(name)
    qa = faq_qa(cat, name, count, i)
    details = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if j == 0 else '', q, a) for j, (q, a) in enumerate(qa))
    return ('<section id="faq" class="songspot-seo-section songspot-seo-faq">'
      '<div class="songspot-seo-heading">'
      '<p class="songspot-seo-eyebrow">Questions about this quiz</p>'
      '<h2>%s song quiz FAQ</h2></div>'
      '<div class="songspot-faq-list">%s</div>'
      '</section>\n' % (e, details))

def related_section(cat, i):
    items = {'artist': ARTISTS, 'genre': GENRES, 'decade': DECADES}[cat]
    n = len(items)
    prefix = "guess-song-decades/" if cat == "decade" else ("guessable-songs/" if cat == "genre" else "")
    links = []
    for k in range(1, 7):
        slug, name = items[(i + k) % n][0], items[(i + k) % n][1]
        links.append('<li><a href="/%s%s/">%s song quiz</a></li>' % (prefix, slug, esc(name)))
    return ('<section id="more-quizzes" class="songspot-seo-section">'
      '<div class="songspot-seo-heading">'
      '<p class="songspot-seo-eyebrow">Keep playing</p>'
      '<h2>More song quizzes</h2></div>'
      '<ul class="songspot-song-cloud">%s</ul>'
      '</section>\n' % ''.join(links))

def build(slug, title, desc, h1, hero, init, vgname, topical, ogimg, related, faq, faq_qas, prefix="", mid=("Song Quiz", "https://www.songguesser.co/song-quiz/")):
    h = TEMPLATE
    path = prefix + slug
    url = "https://www.songguesser.co/" + path + "/"
    h = h.replace(T_TITLE, '<title>' + title + '</title>')
    h = h.replace(T_DESC, '<meta name="description" content="' + desc + '" />')
    h = h.replace(T_CANON, '<link rel="canonical" href="' + url + '" />')
    og_extra = ('\n<meta property="og:image" content="https://www.songguesser.co' + ogimg + '" />'
                '\n<meta name="twitter:card" content="summary_large_image" />'
                '\n<meta name="twitter:image" content="https://www.songguesser.co' + ogimg + '" />') if ogimg else ''
    h = h.replace(T_OGT, '<meta property="og:title" content="' + title + '" />' + og_extra)
    h = h.replace(T_OGD, '<meta property="og:description" content="' + desc + '" />')
    h = h.replace(T_OGU, '<meta property="og:url" content="' + url + '" />')
    h = h.replace(T_TWT, '<meta name="twitter:title" content="' + title + '" />')
    h = h.replace(T_TWD, '<meta name="twitter:description" content="' + desc + '" />')
    h = h.replace('"url":"https://www.songguesser.co/"', '"url":"' + url + '"', 1)
    h = h.replace(T_VG, '"@type":"VideoGame","name":' + js(vgname) + ',"description":' + js(desc))
    h = h.replace(T_H1, '<h1 id="songspot-heading">' + h1 + '</h1>')
    h = h.replace(T_HERO, '<p>' + hero + '</p>')
    h = h.replace('<script src="/decades.js"></script>', '<script>window.SONG_INITIAL = ' + init + ';</script>\n<script src="/decades.js"></script>')
    # replace homepage FAQPage JSON-LD with this page's FAQ + BreadcrumbList
    topic = vgname[:-len(" Guessable Songs")] if vgname.endswith(" Guessable Songs") else vgname[len("Guess the "):-len(" Song")]
    h = re.sub(r'<script type="application/ld\+json">\s*\{[^{]*"@type":"FAQPage".*?</script>',
               breadcrumb(topic, url, mid[0], mid[1]) + faq_json(faq_qas), h, count=1, flags=re.S)
    start = h.index('<section class="songspot-seo">')
    end = h.index('<footer class="songspot-site-footer">')
    h = h[:start] + '<section class="songspot-seo">\n' + topical + faq + related + '</section>\n\n' + h[end:]
    h = h.replace('</head>', CLOUD_CSS + '</head>')
    return h

def write(slug, html, prefix=""):
    d = os.path.join(BASE, prefix + slug)
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)

pages = 0
# Artist pages are now generated by _gen_artists.py (Heardle-style template).
# This script now writes genres + decades only, so it no longer overwrites them.

for i, (slug, name, gid, count) in enumerate(GENRES):
    title = name + ' Guessable Songs | Song Guesser'
    desc = 'Name the ' + name.lower() + ' guessable songs from a 0.1-second clip. Free browser game with ' + str(count) + ' ' + name + ' guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.'
    h1 = name + ' Guessable Songs'
    hero = GENRE_CONTENT[name]['hero'].replace('{count}', str(count)).replace('guessable songs', '<a href="/guessable-songs/">guessable songs</a>', 1)
    init = '{"genre":' + str(gid) + '}'
    write(slug, build(slug, title, desc, h1, hero, init, name + ' Guessable Songs', genre_article(name, count, SONGS["genre"].get(slug, []), i), None, related_section('genre', i), faq_extra('genre', name, count, i), faq_qa('genre', name, count, i), prefix="guessable-songs/", mid=("Genres", "https://www.songguesser.co/guessable-songs/")), prefix="guessable-songs/")
    pages += 1

for i, (slug, name, count) in enumerate(DECADES):
    title = 'Guess the ' + name + ' Song | Song Guesser'
    desc = 'Guess the ' + name + ' song from a 0.1-second clip. Free ' + name + ' song guessing game with ' + str(count) + ' tracks — reveal longer clips only when you ask.'
    h1 = 'Guess the ' + name + ' Song'
    hero = DECADE_CONTENT[name]['hero']
    init = '{"decade":"' + name + '"}'
    write(slug, build(slug, title, desc, h1, hero, init, 'Guess the ' + name + ' Song', decade_article(name, count, SONGS["decade"].get(slug, []), i), None, related_section('decade', i), faq_extra('decade', name, count, i), faq_qa('decade', name, count, i), prefix="guess-song-decades/", mid=("Decades", "https://www.songguesser.co/guess-song-decades/")), prefix="guess-song-decades/")
    pages += 1

print("PAGES", pages)

# Rewrite directory cards to link to the new subpages.
mq = os.path.join(BASE, "song-quiz", "index.html")
m = io.open(mq, "r", encoding="utf-8").read()
for slug, name, count in ARTISTS:
    m = m.replace('href="/?artist=' + urllib.parse.quote(name) + '"', 'href="/song-guesser-artists/' + slug + '/"')
for slug, name, gid, count in GENRES:
    m = m.replace('href="/' + slug + '/"', 'href="/guessable-songs/' + slug + '/"')
for slug, name, count in DECADES:
    m = m.replace('href="/?decade=' + name + '"', 'href="/guess-song-decades/' + slug + '/"')
io.open(mq, "w", encoding="utf-8").write(m)
print("DIRECTORY REWRITTEN")
