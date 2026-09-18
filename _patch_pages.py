# -*- coding: utf-8 -*-
import io, re
P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_pages.py"
src = io.open(P, encoding="utf-8").read()

def sub(old, new):
    global src
    assert src.count(old) == 1, "COUNT %d for: %s" % (src.count(old), old[:60])
    src = src.replace(old, new)

# 1) Decade title: drop the song-name trio (unrelated words).
sub("""    ds = SONGS["decade"].get(slug, [])
    trio = ' — ' + ', '.join(esc(s[0]) for s in ds[:3]) if ds else ''
    title = 'Guess the ' + name + ' Song' + trio + ' | Song Guesser'""",
"""    title = 'Guess the ' + name + ' Song | Song Guesser'""")

# 2) Decade "how" — remove the shared 0.1s -> 0.5/2/8/15s + no-signup skeleton.
sub('"how": "A round begins at a tenth of a second and only widens when you ask for more — 0.5s, 2s, 8s, then 15s. Guess song after song with no signup, no download and no daily cap; the only clock is the one in your ear.",',
    '"how": "Play it the way you would a mixtape in a Walkman: a tenth of a second drops, and you either know it or you do not. A quick miss is free — the clip simply widens until the year snaps into place.",')
sub('"how": "Each round opens at 0.1 seconds and grows only when you ask — 0.5s, 2s, 8s, then 15s. You guess song by song with no login and no daily limit, so a wrong answer costs you nothing but a longer clip.",',
    '"how": "Each solve is a one-second decision. Hear the fuzz, type the title, and only reach for more audio when the first attempt misses. Nothing locks and nothing asks you to sign in — a wrong answer just hands you a longer clip.",')
sub('"how": "A round starts at 0.1 seconds and steps to 0.5s, 2s, 8s and 15s only when you ask. It is a pure guess song game — no account, no app, no daily cap — so name it from the shortest clip you can and the next round is already waiting.",',
    '"how": "The loop is simple: open on the shortest clip, answer fast, and skip when a hook does not land. Nothing is time-gated, so a bad round costs you only a longer clip on the same track.",')
sub('"how": "Press play and the clip opens at 0.1 seconds; skip or miss and it grows to 0.5s, 2s, 8s and 15s. It is a guess song sprint — no signup, no download, no daily cap, just the biggest decade pool in the game.",',
    '"how": "Start each track on a sliver and let your ear do the rest. Widen the clip only when you must — the earlier you commit to a title, the more the round says about your actual recall.",')
sub('"how": "A round opens at 0.1 seconds and only widens when you ask — 0.5s, 2s, 8s, then 15s. It is a guess song round with no download and no daily cap, and because the decade is still writing itself, no two rounds land the same way.",',
    '"how": "Because today\'s hooks are engineered to catch you in a second, most rounds are over in one. Guess the track, and if the loop does not place it, the clip stretches until it does.",')

# 3) Decade "highlights" — vary the trailing cross-link instead of repeating one template.
sub('"highlights": "The pool runs 103 tracks deep, from “Billie Jean” to “Take On Me” to “I Wanna Dance with Somebody (Who Loves Me)”. It leans on gated snares and synth pads, so the first stab is often the whole answer. Want the whole catalog? The full <a href=\'/\'>song guesser</a> shuffles every artist, genre and decade together.",',
    '"highlights": "The pool runs 103 deep, from “Billie Jean” to “Take On Me” to “I Wanna Dance with Somebody (Who Loves Me)”, and leans hard on gated snares and synth pads, so the first stab is often the whole answer. When you want the entire library, the <a href=\'/\'>song guesser</a> opens every artist, genre and decade at once.",')
sub('"highlights": "Across 133 tracks — “Smells Like Teen Spirit”, “...Baby One More Time”, “No Scrubs” and more — grunge fuzz and boom-bap drums do most of the telling. Prefer all five decades at once? The main <a href=\'/\'>song guesser</a> mixes them.",',
    '"highlights": "Across 133 tracks — “Smells Like Teen Spirit”, “...Baby One More Time”, “No Scrubs” and beyond — grunge fuzz and boom-bap drums do most of the telling before the vocal ever arrives. Ready to jump eras? The <a href=\'/\'>song guesser</a> is the one page that shuffles all five decades together.",')
sub('"highlights": "The 204-track pool reaches from “Lose Yourself” to “Hey Ya!” to “Mr. Brightside”, and ringtone hooks plus pop-punk downstrokes mean the opening hit is often the whole answer. Done with the 2000s? The <a href=\'/\'>song guesser</a> opens the full catalog.",',
    '"highlights": "The 204-track pool reaches from “Lose Yourself” to “Hey Ya!” to “Mr. Brightside”; ringtone hooks and pop-punk downstrokes mean the opening hit usually names the song by itself. Once the 2000s are cleared, head to the <a href=\'/\'>song guesser</a> for the rest of the catalog.",')
sub('"highlights": "At 313 tracks it is the biggest pool of the five, running from “Somebody That I Used to Know” to “Uptown Funk” to “Call Me Maybe”; trap hi-hats and EDM drops give the year away in the first beat. Want a break from one decade? The <a href=\'/\'>song guesser</a> shuffles everything.",',
    '"highlights": "At 313 tracks it is the deepest of the five, running from “Somebody That I Used to Know” to “Uptown Funk” to “Call Me Maybe”; trap hi-hats and EDM drops give the year away in the first beat. When one decade is not enough, the <a href=\'/\'>song guesser</a> lets you switch artists, genres and decades mid-run.",')
sub('"highlights": "The 105-track pool spans “Blinding Lights”, “As It Was” and “Anti-Hero”, and because it leans on TikTok-sized loops and genre-blurring beats, the newest decade is the hardest to pin by style alone. Prefer the whole field? The <a href=\'/\'>song guesser</a> plays all five decades at once.",',
    '"highlights": "The 105-track pool spans “Blinding Lights”, “As It Was” and “Anti-Hero”, and because it leans on TikTok-sized loops and genre-blurring beats, the newest decade is the hardest to pin by style alone. The other four decades live on the <a href=\'/\'>song guesser</a>, all playable from the same page.",')

# 4) Replace the templated genre_article with per-genre unique content.
new_genre_article = '''def genre_article(name, count, tracks, i):
    e = esc(name)
    pairs = tracks[:8]
    c = GENRE_CONTENT[name]
    fill = lambda s: s.replace('{count}', str(count))
    what = _sec('What it is', 'What is the %s Song Quiz?' % e, [fill(x) for x in c['what']], None)
    how = _sec('How to play', 'How to Play the %s Quiz' % e, [fill(c['how'])], None)
    hl = _sec('Game highlights', 'The %s Song Pool' % e, [fill(c['highlights'])], pairs)
    return what + how + hl
'''
src = re.sub(r'def genre_article\(name, count, tracks, i\):.*?\nDECADE_STAMP = \{', new_genre_article + '\nDECADE_STAMP = {', src, count=1, flags=re.S)

# 5) Insert GENRE_CONTENT right after DECADE_MOOD (before DECADE_CONTENT).
GENRE_CONTENT = '''GENRE_CONTENT = {
  "Pop": {
    "hero": "The genre that lives on the hook — how fast can you guess the pop song from a tenth of a second?",
    "what": [
      "Pop turns one question into an art form: can a melody catch you before the first word? This guess song quiz plays that question on loop. Each round opens on the barest slice of a real pop record, and the hook, the beat or the key change is all you get.",
      "The pool holds {count} chart songs, so a round can swing from a singalong you grew up with to a single from this month. There is no safe corner of the catalog.",
    ],
    "how": "Hear the slice, type the title, and only ask the game for more audio when you are truly stuck. A fast answer beats a correct one, every round.",
    "highlights": "Pop is engineered to be recognized instantly, so it is the fairest door into the game and the fastest pool to clear. When you want a different flavor, the <a href='/'>song guesser</a> switches you to any other genre in one click.",
    "faq": [
      ("Is pop the easiest genre to start with?", "Usually, yes. Pop hooks are written to stick, so the opening slice is often enough. Start here on Easy, then push toward Impossible once the chart-toppers stop feeling like a challenge."),
      ("How many pop songs can I play?", "{count} chart songs rotate through the pool, from long-running classics to the latest releases. You never know which era the next round will land on."),
      ("Do the rounds ever repeat?", "Not on purpose. The pool is large enough that a full session rarely lands the same track twice in a row, and difficulty controls how deep the rotation goes."),
    ],
  },
  "Rock": {
    "hero": "Riffs, drums and the first chord — guess the rock song before the guitar finishes the thought.",
    "what": [
      "Rock is a genre of firsts: the first chord, the first snare hit, the first bend of a solo. This guess song quiz bets that a tenth of a second of any of them is enough to name the song, and you are the proof either way.",
      "The {count}-track pool crosses every era of rock, from arena anthems to garage cuts, so the same opening chord can belong to a dozen different decades.",
    ],
    "how": "Name the song from the opening sound and reach for a longer clip only as a last resort. The riff is doing most of the work; you just have to trust it.",
    "highlights": "Rock gives itself away in the tone — a fuzz pedal, a clean strat or a double-kick tells you the era before the vocal can. Bored of one genre? The <a href='/'>song guesser</a> is the whole catalog under one roof.",
    "faq": [
      ("How do I get better at the rock quiz?", "Listen for the guitar tone and the drum pattern before the melody. A fuzz pedal, a clean arpeggio or a double-kick usually names the decade faster than the chorus does."),
      ("Which rock songs are in the pool?", "{count} tracks across eras, from arena anthems to deep cuts. The rotation mixes classics and modern rock so no round feels the same."),
      ("Is the rock quiz harder than pop?", "Often a little. Rock spans more sub-styles, so the opening sound carries more weight. That is also what makes a fast solve feel earned."),
    ],
  },
  "Hip-Hop": {
    "hero": "The beat, the flow, the sample — guess the hip-hop song from a tenth of a second.",
    "what": [
      "Hip-hop is built from the first beat of a loop. This guess song quiz starts exactly there: a tenth of a second of a real track, and your job is to name it before the flow tells on itself.",
      "Across {count} tracks, the pool runs from boom-bap to trap to the current chart, so the drum pattern alone is rarely enough — you have to place the era too.",
    ],
    "how": "Let the first beat do the talking. Type your guess the moment the sample or the hi-hat feels familiar, and ask for more audio only when the era will not place itself.",
    "highlights": "The production is the tell: a dusty loop says one decade, a rattling hi-hat says another. When you want to roam outside the genre, the <a href='/'>song guesser</a> opens every lane at once.",
    "faq": [
      ("What should I listen for in a hip-hop clip?", "The drum pattern and the sample first. A dusty loop, a boom-bap kick or a rattling trap hi-hat usually places the era before the rapper does."),
      ("How many hip-hop songs are in the rotation?", "{count} tracks, from boom-bap classics to the current chart. The pool mixes eras so the opening beat is always a fresh test."),
      ("Can I play only hip-hop?", "Yes — pick Hip-Hop and every round stays inside the genre. Head to the <a href='/'>song guesser</a> when you want to mix it with pop, R&B or anything else."),
    ],
  },
  "R&B": {
    "hero": "Vocal runs, slow grooves and a single breath — guess the R&B song from a tenth of a second.",
    "what": [
      "R&B is the genre of the run: a voice that bends a note before the beat even arrives. This guess song quiz opens on that first breath and asks you to name the track from it.",
      "The {count}-song pool spans quiet-storm slow jams to current R&B, so the giveaway is as often a chord as it is a voice.",
    ],
    "how": "Trust the vocal first. A breath, a run or the shape of a chord is usually enough; reveal more only when the groove refuses to place itself.",
    "highlights": "R&B rewards the ear that knows a vocal as well as a hook. When you are ready to switch lanes, the <a href='/'>song guesser</a> is every genre on one page.",
    "faq": [
      ("What gives an R&B song away fastest?", "The vocal. A run, a breath or the shape of a chord names the track faster than the beat does, so keep your ear on the singer."),
      ("How many R&B songs can I play?", "{count} tracks, from slow jams to the current chart. The rotation stays inside the genre and never repeats on purpose."),
      ("Is R&B harder than pop?", "It can be. R&B leans on subtler clues like vocal tone and chord color, so the opening slice asks a little more of your ear."),
    ],
  },
  "K-Pop": {
    "hero": "Group hooks, polished production and a first beat — guess the K-pop song from a tenth of a second.",
    "what": [
      "K-pop is precision pop: every intro is engineered to catch you. This guess song quiz drops a tenth of a second of a real track and waits for you to name it before the drop does.",
      "Across {count} tracks, the pool spans generations of groups and soloists, so the same synth line can belong to several different eras of the genre.",
    ],
    "how": "Name the track from the first beat — the production, the chant or the opening note is usually enough. Ask for more audio only when the group will not give itself away.",
    "highlights": "K-pop intros are built to be recognized in a second, which makes the rounds fast and the misses sting a little more. Want the full catalog? The <a href='/'>song guesser</a> opens every artist and genre.",
    "faq": [
      ("Do I need to know the group to play?", "No — you only need to recognize the track. The production and the hook are usually enough, even if you cannot name the members."),
      ("How many K-pop songs are in the pool?", "{count} tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."),
      ("Is the K-pop quiz in English or Korean?", "The game is entirely in your browser, and you type the title either way. The clip is the same for every language."),
    ],
  },
  "Electronic": {
    "hero": "Drops, bpm and a synth swell — guess the electronic song from a tenth of a second.",
    "what": [
      "Electronic music runs on the build and the drop. This guess song quiz starts at the quietest part — a tenth of a second of a real track — and asks you to name it before the drop lands.",
      "The {count}-track pool spans house, techno, big-room and everything between, so a kick pattern alone rarely tells you the song; you need the whole texture.",
    ],
    "how": "Lock onto the texture: the synth, the bass and the tempo do the naming. Reveal more only when the drop refuses to arrive fast enough.",
    "highlights": "Electronic tracks give away their subgenre in the first beat, which makes the pool fast but unforgiving. For a change of scenery, the <a href='/'>song guesser</a> is every genre under one roof.",
    "faq": [
      ("What should I listen for in an electronic clip?", "The texture — a synth swell, a four-on-the-floor kick or the tempo. The subgenre usually announces itself before the melody does."),
      ("How many electronic songs can I play?", "{count} tracks across house, techno and big-room. The pool stays inside the genre and rotates every round."),
      ("Is the electronic quiz free?", "Yes, like every page on <a href='/'>Song Guesser</a> — it runs in the browser with nothing to install or sign up for."),
    ],
  },
  "Country": {
    "hero": "A twang, a story and a first strum — guess the country song from a tenth of a second.",
    "what": [
      "Country is storytelling first, and the story usually starts with a guitar. This guess song quiz opens on that first strum and asks you to name the track from it.",
      "The {count}-song pool crosses classic twang and modern country, so the fiddle, the steel guitar or the vocal drawl is as much the clue as the melody.",
    ],
    "how": "Hear the strum or the drawl and name the song before the verse arrives. Reach for more audio only when the era will not place itself.",
    "highlights": "Country's fingerprints — the fiddle, the steel guitar, the drawl — usually name the song before the chorus can. When you want a different sound, the <a href='/'>song guesser</a> has every genre waiting.",
    "faq": [
      ("What gives a country song away?", "The instrumentation — a fiddle, a steel guitar or a twangy strum. The story takes over later, but the sound names the era first."),
      ("How many country songs are in the rotation?", "{count} tracks, from classic twang to modern country. The pool stays inside the genre and never repeats on purpose."),
      ("Do I need to like country to play?", "No — you just need an ear for it. The game rewards recognizing the sound, not the fandom."),
    ],
  },
  "Metal": {
    "hero": "Riffs, double-kick and a growl — guess the metal song from a tenth of a second.",
    "what": [
      "Metal is built on the riff, and the riff usually arrives in the first second. This guess song quiz opens on a tenth of a second of a real track and bets you can name it from the attack alone.",
      "The {count}-track pool spans heavy, thrash, death and beyond, so the tuning, the tempo and the drum pattern do most of the telling.",
    ],
    "how": "Name the track from the attack — the riff, the double-kick or the growl. Ask for more audio only when the subgenre will not place itself.",
    "highlights": "Metal's signatures — the down-tuned riff, the blast beat, the growl — give the subgenre away in an instant. For a change of pace, the <a href='/'>song guesser</a> opens every other genre.",
    "faq": [
      ("What gives a metal song away fastest?", "The riff and the drum pattern. A down-tuned chug, a blast beat or a growl usually names the subgenre before the vocal does."),
      ("How many metal songs can I play?", "{count} tracks across heavy, thrash, death and beyond. The rotation stays inside the genre and mixes sub-styles."),
      ("Is the metal quiz harder?", "It can be — metal subgenres share a lot of DNA, so the opening slice asks you to separate thrash from death by ear alone."),
    ],
  },
}

'''
sub('DECADE_CONTENT = {', GENRE_CONTENT + 'DECADE_CONTENT = {')

# 6) Genre hero: use GENRE_CONTENT.
sub('''    hero = [
      'Guess the %s song from the shortest clip you can. This round pulls from %d %s tracks across eras, opening each at 0.1s and revealing 0.5s, 2s, 8s and 15s only when you need another clue.' % (name, count, name),
      '%d %s songs, one 0.1-second clip at a time. A wrong guess or skip reveals 0.5s, 2s, 8s and 15s in steps until the track is named.' % (count, name),
      'Can you name a %s song from a tenth of a second? %d tracks are in play, each opening at 0.1s before longer clips unlock in steps.' % (name, count),
    ][i % 3]''',
'''    hero = GENRE_CONTENT[name]['hero'].replace('{count}', str(count))''')

# 7) Drop the templated tips_section from both loops.
sub("genre_article(name, count, SONGS[\"genre\"].get(slug, []), i) + tips_section('genre', name, i, SONGS[\"genre\"].get(slug, []))",
    "genre_article(name, count, SONGS[\"genre\"].get(slug, []), i)")
sub("decade_article(name, count, SONGS[\"decade\"].get(slug, []), i) + tips_section('decade', name, i, SONGS[\"decade\"].get(slug, []))",
    "decade_article(name, count, SONGS[\"decade\"].get(slug, []), i)")

# 8) faq_qa: genre -> GENRE_CONTENT.
sub('''def faq_qa(cat, name, count, i):
    e = esc(name)
    if cat == 'decade' and name in DECADE_CONTENT:
        return DECADE_CONTENT[name]['faq']
    if cat == 'artist':''',
'''def faq_qa(cat, name, count, i):
    e = esc(name)
    if cat == 'decade' and name in DECADE_CONTENT:
        return DECADE_CONTENT[name]['faq']
    if cat == 'genre' and name in GENRE_CONTENT:
        return [(q, a.replace('{count}', str(count))) for q, a in GENRE_CONTENT[name]['faq']]
    if cat == 'artist':''')

io.open(P, "w", encoding="utf-8").write(src)
print("PATCHED _gen_pages.py OK")
