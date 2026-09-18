# -*- coding: utf-8 -*-
import io, re, json

P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_pages.py"
src = io.open(P, encoding="utf-8").read()

D = {
  "1980s": {
    "hero": "Hear a gated snare and you already know the decade \u2014 that is the whole trick of the 1980s quiz. 103 tracks open at 0.1 seconds; name the song before the arena chorus lands.",
    "what": [
      "The 1980s never hid its hooks. Songs began the way a boxing bell sounds \u2014 loud, immediate, impossible to ignore. This guess-song game leans on exactly that: you get a sliver of a real 1980s record and have to name it before the first word. There is no artist credit to lean on, only the sound.",
      "Picture MTV in its first flush \u2014 the Walkman clipped to a belt, the chorus written to reach the back row of a stadium. Every one of the 103 tracks carries the same tell: gated snares, synth pads and guitars the size of an arena. The question is never whether you remember the title \u2014 it is whether your ear places the sound the moment it hits.",
    ],
    "how": "A round gives you a tenth of a second, then waits. If you know it, type the title and move on. If you do not, the clip opens to 0.5s, 2s, 8s and 15s \u2014 a miss never costs more than a longer listen.",
    "highlights": "103 tracks run from \u201cBillie Jean\u201d to \u201cTake On Me\u201d to \u201cI Wanna Dance with Somebody (Who Loves Me)\u201d. Gated snares and synth pads do most of the work, so the first stab is often the whole answer. Tired of one era? The <a href='/'>song guesser</a> folds all five decades into a single run.",
    "faq": [
      ("How is this different from a plain song quiz?", "Every round stays inside one decade, so the clue is the era itself \u2014 gated snares, synth pads, chorus-sized guitars \u2014 rather than any one artist's style. The 103-track pool opens at 0.1 seconds and only grows to 0.5s, 2s, 8s and 15s when you ask it to."),
      ("What should I listen for in a 1980s clip?", "The production before the melody. A gated drum, a synth pad or a stadium guitar usually names the year before the vocal does \u2014 the drum machine and the arena reverb are the decade's calling card."),
      ("Do I have to know 1980s artists to play?", "No. You are matching a sound to a title, not naming a singer. The pool crosses pop, rock, R&B and hip-hop's first wave, so a familiar hook is usually enough even when the artist slips your mind."),
    ],
  },
  "1990s": {
    "hero": "Flannel fuzz, boom-bap drums, a boy-band harmony \u2014 the 1990s needs about a tenth of a second to say hello. 133 tracks, each opening at 0.1s before longer clips unlock.",
    "what": [
      "The 1990s quiz is a song guessing game for people who still think in mixtapes. A grunge riff or a boom-bap loop announces the decade in a sliver of a second, and your only job is to name the song before it names itself.",
      "It is a dial-up-era time capsule \u2014 flannel and gold chains, and the last stretch of radio before streaming rewired everything. All 133 tracks share one stamp: grunge fuzz, boom-bap beats and boy-band harmonies. The quiz rewards the ear that knows the 1990s as a sound, not a stack of CD spines.",
    ],
    "how": "Every solve is a one-second decision. Hear the fuzz, type the title, and ask for more audio only when the first guess misses. Nothing locks you out and nothing asks for a login \u2014 a wrong answer just hands you a longer clip.",
    "highlights": "Across 133 tracks \u2014 \u201cSmells Like Teen Spirit\u201d, \u201c...Baby One More Time\u201d, \u201cNo Scrubs\u201d and beyond \u2014 grunge fuzz and boom-bap drums do the telling long before the vocal arrives. When you want to leave the 1990s behind, the <a href='/'>song guesser</a> shuffles all five decades on one page.",
    "faq": [
      ("How does the 1990s quiz work?", "Each round plays a 0.1-second clip of a real 1990s track, then reveals 0.5s, 2s, 8s and 15s only when you ask. The 133-song pool spans grunge, hip-hop's golden age and boy-band pop, so the opening sound usually places the era on its own."),
      ("What gives a 1990s song away fastest?", "The production stamp \u2014 grunge fuzz, boom-bap drums and boy-band harmonies. Check the guitar tone and the drum pattern before you chase the melody; the decade usually names itself in the first beat."),
      ("Is the 1990s harder than the 1980s?", "For most people, a little. The 1990s packs more genres into one decade \u2014 alternative rock, R&B, hip-hop's golden age \u2014 and the difficulty dial runs Easy to Impossible, so you control how much of a fight each decade puts up."),
    ],
  },
  "2000s": {
    "hero": "Ringtone hooks, Auto-Tuned vocals, pop-punk downstrokes \u2014 the 2000s announces itself in 0.1 seconds. 204 tracks, each opening at a tenth of a second before the clip grows.",
    "what": [
      "The 2000s quiz is a guess-song game set in the moment pop went digital, when your ringtone said who you were. The intros are short and loud \u2014 a drum fill, an Auto-Tuned vocal, a pop-punk downstroke \u2014 and you name the track from the first tenth of a second.",
      "Think TRL at its peak: ringtones, MP3 players, and the exact season the chorus got shorter and the hook got stickier. All 204 tracks lean on one sound \u2014 ringtone hooks, Auto-Tuned vocals and pop-punk downstrokes \u2014 so the real test is whether you can call the song before the chorus shows up.",
    ],
    "how": "Open on the shortest clip, answer fast, and skip when a hook will not land. Nothing is time-gated \u2014 a bad round costs you only a longer clip on the same track.",
    "highlights": "The 204-track pool reaches from \u201cLose Yourself\u201d to \u201cHey Ya!\u201d to \u201cMr. Brightside\u201d. Ringtone hooks and pop-punk downstrokes mean the opening hit usually names the song all by itself. Once the 2000s are cleared, the <a href='/'>song guesser</a> keeps the rest of the catalog on deck.",
    "faq": [
      ("What makes the 2000s quiz different?", "It is the decade where pop went digital, so the pool is thick with ringtone hooks and Auto-Tuned vocals. 204 tracks stay locked inside one decade, and each round opens at 0.1 seconds before longer reveals unlock."),
      ("What should I listen for in a 2000s track?", "The production, not the lyrics \u2014 ringtone hooks, Auto-Tuned vocals and pop-punk downstrokes are the fingerprint. A single drum fill or vocal effect often names the song before the melody does."),
      ("How many 2000s songs are in the quiz?", "204 playable songs, the second-largest decade pool. Difficulty runs Easy to Impossible and controls how many you cycle through, and every artist, genre and decade also lives on the main <a href='/'>Song Guesser</a> page."),
    ],
  },
  "2010s": {
    "hero": "EDM drops, trap hi-hats and a \u201cfeat.\u201d credit \u2014 the 2010s in a tenth of a second. 313 tracks, the biggest decade pool, each opening at 0.1s and revealing more only when you ask.",
    "what": [
      "This is a song guessing game for the streaming decade. You hear a tenth of a second of a real 2010s record and try to name it before the drop lands \u2014 and the artist credit will not save you, because only the sound will.",
      "It is a streaming-era shuffle: festival drops, guest verses, and the year every chorus learned to loop. All 313 tracks are built on one signature \u2014 EDM drops, trap hi-hats and the \u201cfeat.\u201d credit \u2014 so the quiz measures how fast you can place a song from its production alone.",
    ],
    "how": "Start each track on a sliver and let your ear drive. Widen the clip only when you must \u2014 the earlier you commit to a title, the more the round reveals about your actual recall.",
    "highlights": "At 313 tracks it is the deepest of the five, running from \u201cSomebody That I Used to Know\u201d to \u201cUptown Funk\u201d to \u201cCall Me Maybe\u201d. Trap hi-hats and EDM drops give the year away in the first beat. When one decade is not enough, the <a href='/'>song guesser</a> lets you hop between artists, genres and decades mid-run.",
    "faq": [
      ("Why does the 2010s quiz have the most songs?", "It is the biggest decade pool at 313 tracks, because the streaming era churned out more chart hits per year than any decade before it. Every round still opens at 0.1 seconds and reveals more only when you ask."),
      ("What gives a 2010s song away?", "Trap hi-hats, EDM drops and the \u201cfeat.\u201d credit. The decade built its hits on production signatures \u2014 a hi-hat roll or a build-up usually names the track before the chorus arrives."),
      ("Is the 2010s quiz free?", "Yes. Like every decade round, it runs in the browser with no signup, no download and no daily limit. You can jump between the 1980s and the 2020s in one sitting without ever logging in."),
    ],
  },
  "2020s": {
    "hero": "TikTok-sized loops, genre-blurring beats and bedroom pop \u2014 the 2020s in 0.1 seconds. 105 tracks, each opening at a tenth of a second before longer clips unlock.",
    "what": [
      "The 2020s quiz is a song guessing game for the TikTok decade: fifteen-second hooks, genre lines erased, every track built to catch you before you scroll. You hear a sliver of a real 2020s hit and name it before the loop resets.",
      "Imagine a feed that never stops \u2014 a hook that loops in fifteen seconds, a genre that refuses to sit still, a beat tuned to grab you in a heartbeat. All 105 tracks wear one badge: TikTok-sized loops, genre-blurring beats and bedroom pop, so the quiz tests how fast you can place a song that was engineered to be recognized in a second.",
    ],
    "how": "Because today's hooks are built to catch you instantly, most rounds end in one guess. Name the track, and if the loop does not place it, the clip stretches until it does.",
    "highlights": "The 105-track pool spans \u201cBlinding Lights\u201d, \u201cAs It Was\u201d and \u201cAnti-Hero\u201d. Because it leans on TikTok-sized loops and genre-blurring beats, the newest decade is the hardest to pin by style alone. The other four decades live on the <a href='/'>song guesser</a>, all playable from the same page.",
    "faq": [
      ("Why is the 2020s the hardest decade to pin down?", "Because genre lines have collapsed. The 105-song pool jumps from bedroom pop to Afrobeats to pop-punk inside a single hook, so the production is a weaker clue than in any earlier decade \u2014 which makes every 0.1-second clip a genuine test."),
      ("How does the 2020s quiz work?", "Each round plays a 0.1-second clip of a real 2020s track, then reveals 0.5s, 2s, 8s and 15s only when you ask. The pool holds 105 songs and reshuffles every round."),
      ("Do I need TikTok to play?", "No. You need nothing but a browser. The 2020s pool leans on TikTok-sized hooks, but the game itself has no app, no signup and no download \u2014 just open the page and press play."),
    ],
  },
}

new = "DECADE_CONTENT = " + json.dumps(D, ensure_ascii=False, indent=2)

src, n = re.subn(r'DECADE_CONTENT = \{.*?\n\}\n\ndef decade_article',
                 lambda m: new + '\n\ndef decade_article', src, count=1, flags=re.S)
assert n == 1, "DECADE_CONTENT block match count %d" % n

io.open(P, "w", encoding="utf-8").write(src)
print("patched DECADE_CONTENT, decades:", len(D))
