# -*- coding: utf-8 -*-
import io, json

P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_artists.py"
src = io.open(P, encoding="utf-8").read()

# ---- 1) fixed_faq helper ----
assert src.count("def step(n, icon, t, b):") == 1
src = src.replace(
    "def step(n, icon, t, b):",
    "def fixed_faq(slug):\n"
    "    return [[FAQFIX.get(slug, {}).get(q, q), a] for q, a in EXTRA[slug]['faq']]\n"
    "\n"
    "def step(n, icon, t, b):")

# ---- 2) about_html: use STEPX for titles + step-3 body, fixed_faq for faq ----
old_about = ("    x = dict(EXTRA[a['slug']]); x.update(P2INTRO[a['slug']])\n"
             "    steps = ''.join(step(i + 1, ic, t, b) for i, (ic, t, b) in enumerate(a['steps']))\n"
             "    faq = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, ans)\n"
             "                  for i, (q, ans) in enumerate(x['faq']))")
new_about = ("    x = dict(EXTRA[a['slug']]); x.update(P2INTRO[a['slug']])\n"
             "    sx = STEPX[a['slug']]\n"
             "    steps = ''.join(step(i + 1, ic, sx['t'][i], sx['b3'] if i == 2 else b)\n"
             "                    for i, (ic, t, b) in enumerate(a['steps']))\n"
             "    faq = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, ans)\n"
             "                  for i, (q, ans) in enumerate(fixed_faq(a['slug'])))")
assert src.count(old_about) == 1, "about_html block not found"
src = src.replace(old_about, new_about)

# ---- 3) build: use fixed_faq in structured data ----
assert src.count("faq_json(EXTRA[a['slug']]['faq'])") == 1
src = src.replace("faq_json(EXTRA[a['slug']]['faq'])", "faq_json(fixed_faq(a['slug']))")

# ---- 4) per-artist unique step titles + step-3 body ----
T = {
 "the-weeknd": ["Start on the sliver", "Name the track", "Reveal when stuck", "Play without limits"],
 "taylor-swift": ["Hear the opening tenth", "Type your guess", "Widen the clip", "Play every round"],
 "michael-jackson": ["Listen to beat one", "Put in the title", "Stretch if unsure", "No daily cap"],
 "beyonce": ["Take the first sound", "Pick the song name", "Open more if stuck", "Keep going"],
 "rihanna": ["Catch the opening beat", "Enter the title", "Grow the clip", "Play on repeat"],
 "drake": ["Open with the sliver", "Type the name", "Reveal if needed", "Endless rounds"],
 "eminem": ["Hear the first breath", "Guess the title", "Widen when stuck", "No limit on rounds"],
 "kanye-west": ["Catch the opening sample", "Name the record", "Stretch the sample", "Play all night"],
 "justin-bieber": ["Play the first instant", "Type it out", "Open up if stuck", "Rounds without end"],
 "linkin-park": ["Read the first note", "Enter your answer", "Reveal more", "Play as long as you want"],
 "lady-gaga": ["Take the opening stab", "Type the song", "Widen the reveal", "No caps here"],
 "bruno-mars": ["Hear the first horn", "Name the single", "Stretch if stuck", "Play the whole catalog"],
 "adele": ["Catch the first chord", "Put in your guess", "Open more", "Keep the run going"],
 "ariana-grande": ["Start on the hi-hat", "Type the title", "Reveal if stuck", "Unlimited rounds"],
 "billie-eilish": ["Catch the first whisper", "Enter the name", "Grow the reveal", "Play with no ceiling"],
 "ed-sheeran": ["Hear the opening loop", "Name the loop", "Widen when unsure", "Loop it forever"],
 "coldplay": ["Take the first pad", "Type the song name", "Stretch the pad", "Play without end"],
 "bts": ["Catch the opening drop", "Pick the track", "Open the clip", "Go unlimited"],
 "blackpink": ["Hear the first stomp", "Type your answer", "Reveal when unsure", "Play every comeback"],
 "gdragon": ["Read the opening neon", "Name the era", "Widen the sliver", "Rounds on demand"],
 "david-guetta": ["Catch the first stab", "Enter the single", "Stretch the stab", "Play all sets"],
 "pitbull": ["Hear the first blast", "Type the hit", "Open it up", "Party without limits"],
 "kendrick-lamar": ["Take the opening snare", "Name the joint", "Reveal the verse", "Run it back"],
 "olivia-rodrigo": ["Catch the first strum", "Type the chorus", "Grow it if stuck", "Play through the catalog"],
 "lana-del-rey": ["Read the opening mood", "Guess the record", "Widen the mood", "Play for as long as you like"],
 "maroon-5": ["Hear the first riff", "Put in the name", "Stretch the riff", "No round cap"],
 "shakira": ["Catch the opening rhythm", "Type the riff", "Open the rhythm", "Play the full set"],
 "travis-scott": ["Read the first 808", "Enter the vibe", "Reveal more when stuck", "Rage without limits"],
 "sabrina-carpenter": ["Hear the first bassline", "Name the hit", "Widen the bassline", "Play till you drop"],
 "anuel-aa": ["Catch the opening kick", "Type the track", "Stretch the kick", "Play the full rotation"],
 "don-toliver": ["Hear the first pad", "Guess the single", "Open the pad", "No limit here"],
 "tate-mcrae": ["Take the opening beat", "Enter the track", "Grow the beat", "Play back to back"],
 "playboi-carti": ["Read the first synth", "Name the banger", "Widen the 808", "Rounds with no cap"],
 "bad-bunny": ["Catch the first dembow", "Name the tune", "Stretch the dembow", "Play every banger"],
 "katy-perry": ["Hear the opening sparkle", "Type the hook", "Open the hook", "Play all the hits"],
}

B3 = {
 "the-weeknd": "Miss or skip and the clip opens to 0.5s, 2s, 8s, then the full 15s. Catching that neon synth on the first sliver is the whole flex.",
 "taylor-swift": "Wrong guess? The reveal widens to 0.5s, 2s, 8s and 15s. The cleanest wins still name the era from the shortest clip.",
 "michael-jackson": "A wrong call stretches the clip to 0.5s, 2s, 8s, then 15s. The point is placing that beat or breath while it is still a tenth of a second.",
 "beyonce": "Miss and the clip grows to 0.5s, 2s, 8s, then 15s \u2014 but the round is at its cleanest when you name it off the opening sliver.",
 "rihanna": "Guess wrong and the clip steps to 0.5s, 2s, 8s, then 15s. Naming the era from the first beat is the cleanest round.",
 "drake": "A miss or skip pushes the clip to 0.5s, 2s, 8s, then 15s. The earlier you call the era, the sharper the round.",
 "eminem": "Wrong? The clip widens to 0.5s, 2s, 8s, then 15s. The beat and the breath should get you there well before the bars.",
 "kanye-west": "Skip and the clip stretches to 0.5s, 2s, 8s, then 15s. The goal is reading the sample on the shortest sliver.",
 "justin-bieber": "A wrong guess stretches the clip to 0.5s, 2s, 8s, then 15s. Naming the era from the opening strum is the point.",
 "linkin-park": "Miss and the reveal grows to 0.5s, 2s, 8s, then 15s. The cleanest play is reading the keys or the riff on the first sliver.",
 "lady-gaga": "Wrong call and the clip widens to 0.5s, 2s, 8s, then 15s. Placing the synth or the piano while it is still a sliver is the goal.",
 "bruno-mars": "Skip and the clip steps to 0.5s, 2s, 8s, then 15s. Hearing the horn or the strum on the first sliver is the whole game.",
 "adele": "A miss stretches the clip to 0.5s, 2s, 8s, then 15s. The warmest wins still name the record from the first chord.",
 "ariana-grande": "Guess wrong and the clip grows to 0.5s, 2s, 8s, then 15s. Placing the era from the hi-hat and the synth is the point.",
 "billie-eilish": "Miss and the reveal widens to 0.5s, 2s, 8s, then 15s. The best rounds catch the bass or the whisper on the first sliver.",
 "ed-sheeran": "Wrong? The clip steps to 0.5s, 2s, 8s, then 15s. Naming the loop while it is still a tenth of a second is the flex.",
 "coldplay": "Skip and the clip stretches to 0.5s, 2s, 8s, then 15s. Reading the pad or the piano on the first sliver is the whole trick.",
 "bts": "A wrong guess pushes the clip to 0.5s, 2s, 8s, then 15s. Placing the beat or the chant from the shortest clip is the point.",
 "blackpink": "Miss and the clip grows to 0.5s, 2s, 8s, then 15s. Catching the stomp or the drop on the first sliver is the cleanest round.",
 "gdragon": "Wrong call and the clip widens to 0.5s, 2s, 8s, then 15s. Naming the era from the opening neon is the whole game.",
 "david-guetta": "Skip and the clip steps to 0.5s, 2s, 8s, then 15s. The best rounds catch the chord or the stab while it is still a sliver.",
 "pitbull": "A miss stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the first horn blast is the cleanest win.",
 "kendrick-lamar": "Guess wrong and the clip grows to 0.5s, 2s, 8s, then 15s. Reading the snare or the sample on the shortest clip is the point.",
 "olivia-rodrigo": "Miss and the reveal widens to 0.5s, 2s, 8s, then 15s. Placing the piano or the guitar while it is still a sliver is the flex.",
 "lana-del-rey": "Wrong? The clip steps to 0.5s, 2s, 8s, then 15s. The cleanest rounds read the mood on the first sliver.",
 "maroon-5": "Skip and the clip stretches to 0.5s, 2s, 8s, then 15s. Naming the riff or the synth from the shortest clip is the goal.",
 "shakira": "A wrong guess pushes the clip to 0.5s, 2s, 8s, then 15s. Catching the trumpet or the flute on the first sliver is the trick.",
 "travis-scott": "Miss and the clip grows to 0.5s, 2s, 8s, then 15s. Reading the 808 or the ad-lib on the shortest clip is the point.",
 "sabrina-carpenter": "Guess wrong and the clip widens to 0.5s, 2s, 8s, then 15s. Naming it from the first bassline is the cleanest round.",
 "anuel-aa": "A miss stretches the clip to 0.5s, 2s, 8s, then 15s. Placing the dembow or the rasp on the first sliver is the whole game.",
 "don-toliver": "Skip and the clip steps to 0.5s, 2s, 8s, then 15s. The best rounds read the pad on the first sliver.",
 "tate-mcrae": "Wrong call and the clip grows to 0.5s, 2s, 8s, then 15s. Naming it from the first beat or piano is the point.",
 "playboi-carti": "Miss and the reveal widens to 0.5s, 2s, 8s, then 15s. Catching the 808 or the ad-lib on the first sliver is the flex.",
 "bad-bunny": "A wrong guess stretches the clip to 0.5s, 2s, 8s, then 15s. The goal is naming the lane from the shortest clip.",
 "katy-perry": "Skip and the clip widens to 0.5s, 2s, 8s, then 15s. Naming it from the opening sparkle is the cleanest win.",
}

STEPX = {k: {"t": T[k], "b3": B3[k]} for k in T}
assert len(STEPX) == 35

# ---- 5) unique FAQ questions ----
FAQFIX = {
 "anuel-aa": {
   "Do I need to know Spanish to play?": "Will I need to read the lyrics to score?",
   "What gives his songs away fastest?": "What is the fastest tell on an Anuel AA intro?",
 },
 "david-guetta": {
   "What gives his songs away fastest?": "Which part of a Guetta track gives it away first?",
 },
 "playboi-carti": {
   "What gives his songs away fastest?": "What separates one Carti intro from another?",
 },
 "bad-bunny": {
   "Do I need to know Spanish to play?": "Do I have to speak Spanish to guess correctly?",
   "What is the strongest clue on his songs?": "What gives a Bad Bunny track away first?",
 },
 "don-toliver": {
   "What is the strongest clue on his songs?": "Which sound is the best clue on a Don Toliver track?",
   "Why does Easy help casual fans here?": "Why is Easy the right place to start here?",
 },
 "kendrick-lamar": {
   "What is the strongest clue on his songs?": "What should you listen for first in a Kendrick intro?",
 },
 "billie-eilish": {
   "What trips players up on her songs?": "Which Billie songs are the hardest to place?",
 },
 "olivia-rodrigo": {
   "Do the acoustic versions appear?": "Do the acoustic takes show up in the game?",
   "What trips players up on her songs?": "Where do players get stuck the most?",
 },
 "tate-mcrae": {
   "What trips players up on her songs?": "What makes some Tate rounds trickier than others?",
 },
 "bruno-mars": {
   "What is the hardest thing to place here?": "Which Bruno Mars songs are hardest to name?",
 },
 "pitbull": {
   "What is the hardest thing to place here?": "Which Pitbull tracks are the toughest?",
 },
 "sabrina-carpenter": {
   "What is the hardest thing to place here?": "Which Sabrina tracks trip players up?",
 },
 "maroon-5": {
   "Why does Easy help casual fans here?": "Which difficulty should a casual fan begin on?",
 },
 "katy-perry": {
   "Do the acoustic versions appear?": "Are stripped-down versions part of the pool?",
 },
}

assert "\nfor p in PAGES:" in src
src = src.replace("\nfor p in PAGES:",
    "\nSTEPX = " + json.dumps(STEPX, ensure_ascii=False, indent=1) +
    "\n\nFAQFIX = " + json.dumps(FAQFIX, ensure_ascii=False, indent=1) +
    "\n\nfor p in PAGES:")

io.open(P, "w", encoding="utf-8").write(src)
print("patched STEPX:", len(STEPX), "FAQFIX:", sum(len(v) for v in FAQFIX.values()))
