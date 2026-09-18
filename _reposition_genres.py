# -*- coding: utf-8 -*-
"""Reposition genre pages from 'Guess the {Genre} Song' to '{Genre} Guessable Song'.
Rewrites title/desc/h1/vgname generation + GENRE_CONTENT copy in _gen_pages.py."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
P = os.path.join(BASE, "_gen_pages.py")
s = io.open(P, encoding="utf-8").read()

EM = "\u2014"  # actual em-dash

# 1. Generation lines (genre loop)
s = s.replace(
    "title = 'Guess the ' + name + ' Song in 0.1 Seconds | Song Guesser'",
    "title = name + ' Guessable Song | Song Guesser'")
s = s.replace(
    "desc = 'Guess the ' + name + ' song from a 0.1-second clip. Free browser game with ' + str(count) + ' ' + name + ' tracks " + EM + " reveal 0.5s, 2s, 8s and 15s only when you need more.'",
    "desc = 'Name the ' + name.lower() + ' guessable song from a 0.1-second clip. Free browser game with ' + str(count) + ' ' + name + ' guessable songs " + EM + " reveal 0.5s, 2s, 8s and 15s only when you need more.'")
s = s.replace(
    "h1 = 'Guess the ' + name + ' Song in 0.1 Seconds'",
    "h1 = name + ' Guessable Song'")
s = s.replace(
    "'Guess the ' + name + ' Song', genre_article(name, count",
    "name + ' Guessable Song', genre_article(name, count")

NEW = '''GENRE_CONTENT = {
  "Pop": {
    "hero": "Pop's guessable songs are built to be caught in half a second. Name the pop guessable song from a tenth of a second, before the hook lands.",
    "what": [
      "Pop turns one question into a sport: can a melody catch you before the first word? Every pop guessable song here opens on the barest slice of a real record \u2014 a synth stab, a drum fill, a key change \u2014 and your job is to name it before the chorus tells you.",
      "The pool holds {count} chart songs, so a round swings from a singalong you grew up with to a single from this month. Some are the most guessable songs ever written; others hide behind a single production trick.",
      "This is a Heardle-style song guessing game at its most direct: one hook, one guess, and the guessable song is the one your ear already knows.",
    ],
    "how": "Hear the slice, type the title, and only ask for more audio when you are truly stuck. A guessable song rewards the fast answer over the lucky one.",
    "highlights": "Pop is engineered to be recognized instantly, so its guessable songs are the fairest door into the game and the fastest pool to clear. When you want a different flavor, the <a href='/'>song guesser</a> switches you to any other genre in one click.",
    "faq": [
      ("Is pop the easiest genre to start with?", "Usually, yes. Pop's guessable songs are written to stick, so the opening slice is often enough. Start here on Easy, then push toward Impossible once the chart-toppers stop feeling like a challenge."),
      ("How many pop guessable songs can I play?", "{count} chart songs rotate through the pool, from long-running classics to the latest releases. You never know which era the next guessable song will land on."),
      ("Do the rounds ever repeat?", "Not on purpose. The pool is large enough that a full session rarely lands the same guessable song twice in a row, and difficulty controls how deep the rotation goes."),
    ],
  },
  "Rock": {
    "hero": "Riffs, drums and the first chord \u2014 a rock guessable song gives itself away before the guitar finishes the thought.",
    "what": [
      "Rock is a genre of firsts: the first chord, the first snare hit, the first bend of a solo. The guessable song is the one whose first tenth of a second names the track, and you are the proof either way.",
      "The {count}-track pool crosses every era of rock, from arena anthems to garage cuts, so a guessable song can belong to any of a dozen decades before the vocal lands.",
      "It runs as a Heardle-style song guessing game, except the clues are riffs, tone and the first hit of the drums.",
    ],
    "how": "Name the guessable song from the opening sound and reach for a longer clip only as a last resort. The riff is doing most of the work; you just have to trust it.",
    "highlights": "Rock's guessable songs give themselves away in the tone \u2014 a fuzz pedal, a clean strat or a double-kick tells you the era before the vocal can. Bored of one genre? The <a href='/'>song guesser</a> is the whole catalog under one roof.",
    "faq": [
      ("How do I get better at the rock quiz?", "Listen for the guitar tone and the drum pattern before the melody. A fuzz pedal, a clean arpeggio or a double-kick usually names the decade faster than the chorus does."),
      ("Which rock guessable songs are in the pool?", "{count} tracks across eras, from arena anthems to deep cuts. The rotation mixes classics and modern rock so no round feels the same."),
      ("Is the rock quiz harder than pop?", "Often a little. Rock spans more sub-styles, so the opening sound carries more weight. That is also what makes a fast solve on a guessable song feel earned."),
    ],
  },
  "Hip-Hop": {
    "hero": "The beat, the flow, the sample \u2014 a hip-hop guessable song announces itself in the first tenth of a second.",
    "what": [
      "Hip-hop is built from the first beat of a loop. A guessable song here starts exactly there: a tenth of a second of a real track, and your job is to name it before the flow tells on itself.",
      "Across {count} tracks, the pool runs from boom-bap to trap to the current chart, so a guessable song rarely gives up its era on the drum pattern alone \u2014 you have to place the sample too.",
      "This is a Heardle-style song guessing game driven by the beat, the sample and the first bar of a flow.",
    ],
    "how": "Let the first beat do the talking. Type your guess the moment the sample or the hi-hat feels familiar, and ask for more audio only when the era will not place itself.",
    "highlights": "The production is the tell on every guessable song: a dusty loop says one decade, a rattling hi-hat says another. When you want to roam outside the genre, the <a href='/'>song guesser</a> opens every lane at once.",
    "faq": [
      ("What should I listen for in a hip-hop clip?", "The drum pattern and the sample first. A dusty loop, a boom-bap kick or a rattling trap hi-hat usually places the era before the rapper does."),
      ("How many hip-hop guessable songs are in the rotation?", "{count} tracks, from boom-bap classics to the current chart. The pool mixes eras so the opening beat is always a fresh test."),
      ("Can I play only hip-hop?", "Yes \u2014 pick Hip-Hop and every round stays inside the genre. Head to the <a href='/'>song guesser</a> when you want to mix it with pop, R&B or anything else."),
    ],
  },
  "R&B": {
    "hero": "Vocal runs, slow grooves and a single breath \u2014 an R&B guessable song is often named by the voice alone.",
    "what": [
      "R&B is the genre of the run: a voice that bends a note before the beat even arrives. A guessable song here opens on that first breath and asks you to name the track from it.",
      "The {count}-song pool spans quiet-storm slow jams to current R&B, so a guessable song can give itself away through a chord as easily as a voice.",
      "At heart it is a Heardle-style song guessing game, but the clues arrive as a breath, a chord and a vocal run.",
    ],
    "how": "Trust the vocal first. A breath, a run or the shape of a chord is usually enough; reveal more only when the groove refuses to place itself.",
    "highlights": "R&B rewards the ear that knows a vocal as well as a hook, and its guessable songs lean on tone over texture. When you are ready to switch lanes, the <a href='/'>song guesser</a> is every genre on one page.",
    "faq": [
      ("What gives an R&B guessable song away fastest?", "The vocal. A run, a breath or the shape of a chord names the track faster than the beat does, so keep your ear on the singer."),
      ("How many R&B guessable songs can I play?", "{count} tracks, from slow jams to the current chart. The rotation stays inside the genre and never repeats on purpose."),
      ("Is R&B harder than pop?", "It can be. R&B leans on subtler clues like vocal tone and chord color, so the opening slice of a guessable song asks a little more of your ear."),
    ],
  },
  "K-Pop": {
    "hero": "Group hooks, polished production and a first beat \u2014 a K-pop guessable song is engineered to be caught in a second.",
    "what": [
      "K-pop is precision pop: every intro is engineered to catch you. A guessable song here drops a tenth of a second of a real track and waits for you to name it before the drop does.",
      "Across {count} tracks, the pool spans generations of groups and soloists, so the same synth line can make several guessable songs sound like cousins at first.",
      "It plays like a Heardle-style song guessing game, and every round stays locked to a K-pop comeback.",
    ],
    "how": "Name the guessable song from the first beat \u2014 the production, the chant or the opening note is usually enough. Ask for more audio only when the group will not give itself away.",
    "highlights": "K-pop intros are built to be recognized in a second, which makes its guessable songs fast rounds with misses that sting a little more. Want the full catalog? The <a href='/'>song guesser</a> opens every artist and genre.",
    "faq": [
      ("Do I need to know the group to play?", "No \u2014 you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."),
      ("How many K-pop guessable songs are in the pool?", "{count} tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."),
      ("Is the K-pop quiz in English or Korean?", "The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."),
    ],
  },
  "Electronic": {
    "hero": "Drops, bpm and a synth swell \u2014 an electronic guessable song is one you can name before the drop lands.",
    "what": [
      "Electronic music runs on the build and the drop. A guessable song here starts at the quietest part \u2014 a tenth of a second of a real track \u2014 and asks you to name it before the drop arrives.",
      "The {count}-track pool spans house, techno, big-room and everything between, so a guessable song rarely gives itself away on a kick pattern alone; you need the whole texture.",
      "This is a Heardle-style song guessing game where the giveaways are pads, builds and the shape of a drop.",
    ],
    "how": "Lock onto the texture: the synth, the bass and the tempo do the naming. Reveal more only when the drop refuses to arrive fast enough.",
    "highlights": "Electronic guessable songs give away their subgenre in the first beat, which makes the pool fast but unforgiving. For a change of scenery, the <a href='/'>song guesser</a> is every genre under one roof.",
    "faq": [
      ("What should I listen for in an electronic clip?", "The texture \u2014 a synth swell, a four-on-the-floor kick or the tempo. The subgenre usually announces itself before the melody of a guessable song does."),
      ("How many electronic guessable songs can I play?", "{count} tracks across house, techno and big-room. The pool stays inside the genre and rotates every round."),
      ("Is the electronic quiz free?", "Yes, like every page on <a href='/'>Song Guesser</a> \u2014 it runs in the browser with nothing to install or sign up for."),
    ],
  },
  "Country": {
    "hero": "A twang, a story and a first strum \u2014 a country guessable song names itself before the verse arrives.",
    "what": [
      "Country is storytelling first, and the story usually starts with a guitar. A guessable song here opens on that first strum and asks you to name the track from it.",
      "The {count}-song pool crosses classic twang and modern country, so a guessable song can lean on the fiddle, the steel guitar or the vocal drawl as much as the melody.",
      "It is a Heardle-style song guessing game, but the clues are a strum, a twang and a storyteller's drawl.",
    ],
    "how": "Hear the strum or the drawl and name the guessable song before the verse arrives. Reach for more audio only when the era will not place itself.",
    "highlights": "Country's fingerprints \u2014 the fiddle, the steel guitar, the drawl \u2014 usually name a guessable song before the chorus can. When you want a different sound, the <a href='/'>song guesser</a> has every genre waiting.",
    "faq": [
      ("What gives a country guessable song away?", "The instrumentation \u2014 a fiddle, a steel guitar or a twangy strum. The story takes over later, but the sound names the era first."),
      ("How many country guessable songs are in the rotation?", "{count} tracks, from classic twang to modern country. The pool stays inside the genre and never repeats on purpose."),
      ("Do I need to like country to play?", "No \u2014 you just need an ear for it. The game rewards recognizing the sound of a guessable song, not the fandom."),
    ],
  },
  "Metal": {
    "hero": "Riffs, double-kick and a growl \u2014 a metal guessable song is named from the attack alone.",
    "what": [
      "Metal is built on the riff, and the riff usually arrives in the first second. A guessable song here opens on a tenth of a second of a real track and bets you can name it from the attack alone.",
      "The {count}-track pool spans heavy, thrash, death and beyond, so a guessable song leans on its tuning, tempo and drum pattern to tell you which subgenre you are in.",
      "This is a Heardle-style song guessing game tuned for the pit, where a chug and a kick do the naming.",
    ],
    "how": "Name the guessable song from the attack \u2014 the riff, the double-kick or the growl. Ask for more audio only when the subgenre will not place itself.",
    "highlights": "Metal's signatures \u2014 the down-tuned riff, the blast beat, the growl \u2014 give a guessable song's subgenre away in an instant. For a change of pace, the <a href='/'>song guesser</a> opens every other genre.",
    "faq": [
      ("What gives a metal guessable song away fastest?", "The riff and the drum pattern. A down-tuned chug, a blast beat or a growl usually names the subgenre before the vocal does."),
      ("How many metal guessable songs can I play?", "{count} tracks across heavy, thrash, death and beyond. The rotation stays inside the genre and mixes sub-styles."),
      ("Is the metal quiz harder?", "It can be \u2014 metal subgenres share a lot of DNA, so the opening slice of a guessable song asks you to separate thrash from death by ear alone."),
    ],
  },
}
'''

# 2. Replace the whole GENRE_CONTENT block
a = s.index("GENRE_CONTENT = {")
b = s.index("\nDECADE_CONTENT = {")
s = s[:a] + NEW + s[b:]

io.open(P, "w", encoding="utf-8").write(s)

# verify the four generation edits all landed
for needle in ["title = name + ' Guessable Song | Song Guesser'",
               "desc = 'Name the ' + name.lower() + ' guessable song",
               "h1 = name + ' Guessable Song'",
               "name + ' Guessable Song', genre_article(name, count"]:
    assert needle in s, "MISSING: " + needle
print("repositioned _gen_pages.py OK")
