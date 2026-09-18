# -*- coding: utf-8 -*-
import io, re, json

P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_artists.py"
src = io.open(P, encoding="utf-8").read()

# ---- 1) diagnose + fix paths (robust to any whitespace) ----
m = re.search(r"example\.com/(?P<q>'|\u2019|\u2018)\s*\+\s*slug\s*\+\s*(?P=q)", src)
print("path pattern matched:", bool(m), repr(m.group(0)) if m else "")
before = len(re.findall(r"example\.com/' \+ slug \+ '/", src))
src = re.sub(r"example\.com/(?P<q>'|\u2019|\u2018)\s*\+\s*slug\s*\+\s*(?P=q)", "www.songguesser.co/song-guesser-artists/' + slug + '", src)
after = len(re.findall(r"example\.com/' \+ slug \+ '/", src))
print("www.songguesser.co slug refs before/after:", before, after)

# breadcrumb position 2 -> Artists (idempotent)
src = src.replace('{"@type":"ListItem","position":2,"name":"Music Quizzes","item":"https://www.songguesser.co/music-quizzes/"}',
                  '{"@type":"ListItem","position":2,"name":"Artists","item":"https://www.songguesser.co/song-guesser-artists/"}')

# ---- 2) about_html: pull p2 / intro from a new P2INTRO dict ----
assert src.count("    x = EXTRA[a['slug']]\n") == 1, "about_html x= line not unique"
src = src.replace("    x = EXTRA[a['slug']]\n",
                  "    x = dict(EXTRA[a['slug']]); x.update(P2INTRO[a['slug']])\n")
assert src.count("a['p1'], a['p2']") == 1
src = src.replace("a['p1'], a['p2']", "a['p1'], x['p2']")
assert src.count("a['intro'], steps") == 1
src = src.replace("a['intro'], steps", "x['intro'], steps")

# ---- 3) unique second paragraph + intro per artist ----
P2INTRO = {
 "the-weeknd": {
  "intro": "Every round is one question — how little of that neon synth do you actually need?",
  "p2": "The fun of a <a href=\"/\">song guesser</a> built on Abel Tesfaye's music is that his productions are instantly recognizable yet easy to confuse — “Save Your Tears” and “Blinding Lights” share a family resemblance until the second note tells them apart.",
 },
 "taylor-swift": {
  "intro": "Work from the shortest clip outward, and let each reveal confirm or correct your first instinct.",
  "p2": "Because her eras sound nothing alike, this <a href=\"/\">song guesser</a> doubles as a tour through her whole career — a twang here, a synth there, and suddenly you are naming the album before the song.",
 },
 "michael-jackson": {
  "intro": "Each round opens on a sliver and waits for your first call.",
  "p2": "Jackson's intros were built to stop a room, which makes them ideal for a <a href=\"/\">song guesser</a> — one beat or one breath is often all you need to separate “Billie Jean” from everything around it.",
 },
 "beyonce": {
  "intro": "Start at the shortest clip and let the horns, the drums and the runs point the way.",
  "p2": "What makes this <a href=\"/\">song guesser</a> work is how much her arrangements changed over the years — a horn stab, a marching snare and a vocal run each belong to a different Beyoncé, and the opening usually tells you which one you are hearing.",
 },
 "rihanna": {
  "intro": "Each round gives you a sliver and a single question: which Rihanna is this?",
  "p2": "Her catalog swings from dance-floor bangers to piano ballads, so this <a href=\"/\">song guesser</a> is really a test of how fast you can sort one era from another — the first beat is usually enough.",
 },
 "drake": {
  "intro": "Work the sliver, then confirm against the era's mood and drums.",
  "p2": "Drake's sound kept shifting from moody to bouncy to island-smooth, so a <a href=\"/\">song guesser</a> built on him rewards anyone who knows which album each drum pattern belongs to.",
 },
 "eminem": {
  "intro": "Each round opens on a sliver and asks you to name it before the bars arrive.",
  "p2": "Because his intros are famous in their own right, this <a href=\"/\">song guesser</a> leans on the beat and the breath — the vocal only confirms what the production already told you.",
 },
 "kanye-west": {
  "intro": "Hear the sample, the drums or the 808, and place the era from that first sound.",
  "p2": "Kanye reinvented his sound on almost every album, so a <a href=\"/\">song guesser</a> built on him is as much a history quiz as a music game — the opening sound is a timestamp.",
 },
 "justin-bieber": {
  "intro": "Start at the shortest clip and let the production name the era.",
  "p2": "His sound moved from teen pop to trop-house to soft R&B, so this <a href=\"/\">song guesser</a> rewards the fan who can hear which Bieber is which from the first strum or shaker.",
 },
 "linkin-park": {
  "intro": "Each round opens on a sliver of keys, guitar or drums.",
  "p2": "Their whole identity is the blend of electronics and guitars, which makes a <a href=\"/\">song guesser</a> built on Linkin Park a test of how fast you can read that balance — a clean keyboard loop is a different era from a chugging riff.",
 },
 "lady-gaga": {
  "intro": "Start from the shortest clip and let the synth, the piano or the drama guide you.",
  "p2": "Gaga's catalog jumps from club pop to jazz to stripped ballads, so this <a href=\"/\">song guesser</a> asks you to name the Gaga first — the first sound usually does it.",
 },
 "bruno-mars": {
  "intro": "Each round opens on a sliver and lets the lead instrument do the talking.",
  "p2": "His music is built on live-band hooks — a horn, a strum or a doo-wop sway — so a <a href=\"/\">song guesser</a> made of Bruno Mars songs is really a test of how fast you can hear the band.",
 },
 "adele": {
  "intro": "Work from the shortest clip and let the piano tell you which album you are in.",
  "p2": "Adele's four albums each carry their own weight and warmth, so this <a href=\"/\">song guesser</a> rewards the ear that can place the era — the tempo and the key usually name the record.",
 },
 "ariana-grande": {
  "intro": "Start at the shortest clip and let the beat texture and the runs guide you.",
  "p2": "Her sound shifted from glossy pop to trap-lite R&B, so a <a href=\"/\">song guesser</a> built on Ariana Grande is a study in production — the hi-hat and the synth usually name the era before she does.",
 },
 "billie-eilish": {
  "intro": "Each round opens on a whisper, a bass thump or a blown-out chorus.",
  "p2": "Because her records live in the low end and the breath, this <a href=\"/\">song guesser</a> is a test of how well you listen below the melody — the bass is the whole clue.",
 },
 "ed-sheeran": {
  "intro": "Start from the shortest clip and let the loop do the identifying.",
  "p2": "His songs are built on single looped figures, so a <a href=\"/\">song guesser</a> made of Ed Sheeran tracks is really a rhythm test — the strum or the loop usually names the song.",
 },
 "coldplay": {
  "intro": "Each round opens on an atmosphere — a piano, a string swell or a synth pad.",
  "p2": "Their sound moved from quiet rock to stadium-sized electronica, so this <a href=\"/\">song guesser</a> rewards the fan who can read the texture — the opening chord is the era's signature.",
 },
 "bts": {
  "intro": "Start from the shortest clip and let the drop or the chant lead.",
  "p2": "Their discography blends K-pop, hip-hop and EDM, so a <a href=\"/\">song guesser</a> built on BTS is a test of how fast you can place the beat — a synth stab or a chant usually names the record.",
 },
 "blackpink": {
  "intro": "Each round opens on a stomp, a drop or a chant.",
  "p2": "Their comebacks each came with a signature opening, which makes a <a href=\"/\">song guesser</a> built on BLACKPINK a sprint — the first half-second is usually the whole answer.",
 },
 "gdragon": {
  "intro": "Start at the shortest clip and let the neon or the beat name the era.",
  "p2": "G-DRAGON's sound kept mutating album to album, so this <a href=\"/\">song guesser</a> is a map of his reinventions — the first synth or drum tells you which G-DRAGON you are dealing with.",
 },
 "david-guetta": {
  "intro": "Each round opens on a chord, a stab or the start of a build.",
  "p2": "His records are built on the build and the drop, so a <a href=\"/\">song guesser</a> made of David Guetta tracks rewards the ear that knows a piano lift from a big-room synth.",
 },
 "pitbull": {
  "intro": "Start at the shortest clip and let the horn or the shout lead.",
  "p2": "Pitbull's hits are built to start a party on beat one, so this <a href=\"/\">song guesser</a> is a test of how fast you can catch the horn — the first blast usually names the record.",
 },
 "kendrick-lamar": {
  "intro": "Each round opens on a drum, a vocal bend or a beat switch.",
  "p2": "His albums each carry a distinct sonic stamp, so a <a href=\"/\">song guesser</a> built on Kendrick Lamar is a study in production — the first snare or sample usually names the era.",
 },
 "olivia-rodrigo": {
  "intro": "Start from the shortest clip and let the piano or the guitar sort it.",
  "p2": "Her two modes are easy to hear — a lone piano is a ballad, a crunchy guitar is the punk — so this <a href=\"/\">song guesser</a> rewards the fan who trusts the first instrument.",
 },
 "lana-del-rey": {
  "intro": "Each round opens on an atmosphere — strings, guitar or a dreamy synth.",
  "p2": "Her records live in mood more than melody, so a <a href=\"/\">song guesser</a> built on Lana Del Rey asks you to read the texture — the lead instrument usually names the era.",
 },
 "maroon-5": {
  "intro": "Start from the shortest clip and let the riff or the synth name the era.",
  "p2": "Their sound drifted from rock to radio pop, so this <a href=\"/\">song guesser</a> rewards the fan who can hear which Maroon 5 is which — a funky guitar is a different era from a glossy synth.",
 },
 "shakira": {
  "intro": "Each round opens on a rhythm — a trumpet, a flute or a percussion figure.",
  "p2": "Her catalog splits between Latin rock and global pop, so a <a href=\"/\">song guesser</a> built on Shakira is a test of the lead instrument — the first sound usually names the lane.",
 },
 "travis-scott": {
  "intro": "Start at the shortest clip and let the 808 or the ad-lib name it.",
  "p2": "His sound is texture first — a pitched-down vocal, a woozy drone, a hard 808 — so this <a href=\"/\">song guesser</a> rewards the fan who can read the haze from the first hit.",
 },
 "sabrina-carpenter": {
  "intro": "Each round opens on a bassline, a strum or a wink.",
  "p2": "Her hooks are sharp and immediate, so a <a href=\"/\">song guesser</a> built on Sabrina Carpenter is a sprint — the disco bassline or the playful vocal usually gives the whole thing away.",
 },
 "anuel-aa": {
  "intro": "Start from the shortest clip and let the dembow or the rasp lead.",
  "p2": "His lane is the dembow and the street anthem, so this <a href=\"/\">song guesser</a> rewards the fan who can separate the reggaeton from the trap — the first kick usually does it.",
 },
 "don-toliver": {
  "intro": "Each round opens on a synth wash, an 808 or a falsetto.",
  "p2": "His sound is wavy and melodic, so a <a href=\"/\">song guesser</a> built on Don Toliver asks you to read the haze — the swelling pad usually names the era.",
 },
 "tate-mcrae": {
  "intro": "Start at the shortest clip and let the beat or the piano sort it.",
  "p2": "Her two modes split cleanly — a stomping beat is the dance pop, a sparse piano is the ballad — so this <a href=\"/\">song guesser</a> rewards the fan who trusts the first sound.",
 },
 "playboi-carti": {
  "intro": "Each round opens on an 808, a synth or a baby-voice ad-lib.",
  "p2": "His eras are separated by energy — minimal bounce versus a wall of 808s — so a <a href=\"/\">song guesser</a> built on Playboi Carti is a test of how fast you can read that shift.",
 },
 "bad-bunny": {
  "intro": "Start from the shortest clip and let the dembow or the vocal bend lead.",
  "p2": "His sound bends reggaeton, trap and pop, so this <a href=\"/\">song guesser</a> rewards the fan who can name the lane from the first beat — the dembow is the fastest tell.",
 },
 "katy-perry": {
  "intro": "Each round opens on a hook — a chant, a sparkle or a slinky beat.",
  "p2": "Her hits were built around one unmistakable chorus, so a <a href=\"/\">song guesser</a> made of Katy Perry songs is a test of the opening — the synth sparkle or the drum fill usually names the record.",
 },
}

lit = json.dumps(P2INTRO, ensure_ascii=False, indent=1)
assert "\nfor p in PAGES:" in src
src = src.replace("\nfor p in PAGES:", "\nP2INTRO = " + lit + "\n\nfor p in PAGES:")

io.open(P, "w", encoding="utf-8").write(src)
print("CONTENT patched. artists:", len(P2INTRO))
