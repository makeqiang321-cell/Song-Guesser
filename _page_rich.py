# -*- coding: utf-8 -*-
# Competitor-style "Choose Your Challenge" + "What to Listen For" content for
# the 8 genre pages and 5 decade pages, keyed by display name.
# Difficulty tiers mirror game.js POOL_LIMIT: easy=12, medium=25, hard/expert/impossible=50.
# Every sentence below is hand-written and structurally unique to its page.

RICH = {
"Pop": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial only decides how far past the chorus you are willing to dig — the chart itself never changes.",
    "rows": [
     ("🟢", "Easy", "Start on the hooks everyone already owns: a dozen songs that name themselves from the first synth stab."),
     ("🟡", "Medium", "Drop the dial one notch and twenty-five near-hits join in, the ones that almost topped the chart."),
     ("🟠", "Hard", "At fifty you are on your own with a B-side from years back — place it from the opening chord, nothing more."),
     ("🔴", "Expert", "Fifty again, but the clip is shaved down to a filter sweep, so the melody is not even in the room yet."),
     ("💀", "Impossible", "Here a tenth of a second is the whole song: no warm-up, no chorus — you know it or you reach for the reveal."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎛️", "Follow the hook to its payoff", "Pop hands you the chorus up front, so the first sound is a map — a piano run promises one kind of song, a trap-lite snap another. Trust where the intro is pointing."),
     ("🥁", "Date it by the drum machine", "A gated snare and a soft-clipped 808 are different decades, even when the melody is brand new. The beat is the older witness."),
     ("🎤", "Read the key and the lift", "The chorus moves up, the verse stays low, and the distance between them is a signature. That jump is often the fastest tell before the words arrive."),
    ]},
},
"Rock": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial walks you off the singalong hits toward the bootleg-era deep cuts nobody covers.",
    "rows": [
     ("🟢", "Easy", "A dozen anthems the bar can finish for you, caught from the very first power chord."),
     ("🟡", "Medium", "One step down and twenty-five second-string singles join the pile — still loud, just less famous."),
     ("🟠", "Hard", "At fifty, the album side does the talking: a lone guitar tone has to place the record."),
     ("🔴", "Expert", "That same fifty, now decided by the amp buzz before the drummer even counts in."),
     ("💀", "Impossible", "No riff, no beat — just the tenth-of-a-second hiss before the song starts, and the fifty wait."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎸", "Let the guitar tone speak", "Every player has a fingerprint — the fuzz, the chug, the chorus pedal — and the tone usually lands before the melody. Name the texture and the song follows."),
     ("🥁", "Count the drummer's pocket", "A double-kick run and a lazy backbeat are two different bands entirely. The way the drums sit tells you the subgenre in half a second."),
     ("🎤", "Hear the singer's entry", "A rasp, a wail or a spoken-word intro all carry different eras. The first breath of the vocal is a timestamp."),
    ]},
},
"Hip-Hop": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial is a depth gauge — from the records everyone can quote to the mixtape cuts only the heads still own.",
    "rows": [
     ("🟢", "Easy", "Open with the twelve tracks the block already knows, spotted from the first looped sample."),
     ("🟡", "Medium", "Widen it to twenty-five and the slept-on follow-ups start showing up next to the smashes."),
     ("🟠", "Hard", "Fifty records now, where a producer tag or a drum pattern is all you get to place the era."),
     ("🔴", "Expert", "Same fifty, thinner air: solve it from the hi-hat hiss before the drums lock."),
     ("💀", "Impossible", "A tenth of a second of a sample flip, no runway — and you are on your own."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎛️", "Trust the sample", "Most classic records open on a recognizable loop — a soul chop, a piano stab, a vinyl crackle — and the sample usually outruns the rapper to the answer."),
     ("🥁", "Read the drum era", "Dusty boom-bap and rattling trap hi-hats are decades apart. The swing of the first beat is a more honest date than the lyrics."),
     ("🎤", "Catch the first ad-lib", "A signature ad-lib or a producer tag is the modern credit reel. Lock it and the title is often already half-typed."),
    ]},
},
"R&B": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "Deeper just means further from the wedding-playlist staples, toward the quiet-storm album cuts.",
    "rows": [
     ("🟢", "Easy", "Ease in with the twelve songs the room already knows, caught the moment the first vocal run bends."),
     ("🟡", "Medium", "Push to twenty-five and the charted-but-forgotten singles come back into the rotation."),
     ("🟠", "Hard", "Now fifty, and the chord color alone has to tell you which slow jam is playing."),
     ("🔴", "Expert", "That same fifty, but you solve from the breath before the run — the melody is still unannounced."),
     ("💀", "Impossible", "The sliver holds at a tenth of a second and the fifty give up nothing for free."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎹", "Listen for the chord color", "A warm quiet-storm progression is a different record from a bright, clean one. The harmony tags the era faster than the singer."),
     ("🎤", "Follow the run to its home", "The opening run often quotes the chorus melody, so a single bend can be the whole answer. Keep your ear on the singer, not the beat."),
     ("🥁", "Feel the pocket, not the tempo", "Two slow jams can sit at the same speed and swing differently. The groove is the tell, not the BPM."),
    ]},
},
"K-Pop": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial only decides how far from the title tracks you wander — toward the b-sides even a stan has to dig for.",
    "rows": [
     ("🟢", "Easy", "Twelve songs the crowd can chant back, and each one opens on the marching stomp that gives it away."),
     ("🟡", "Medium", "Twenty-five comebacks, counting the ones that won the week without ever becoming the group's defining moment."),
     ("🟠", "Hard", "At fifty the production itself has to name the group, because the vocal has not arrived yet."),
     ("🔴", "Expert", "The fifty return, but the clip stops on the opening synth before the drop takes shape."),
     ("💀", "Impossible", "A chant you barely hear, no drop to catch you — that is the whole clue."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎛️", "Read the comeback intro", "K-pop intros are engineered like movie trailers — a stomp, a chanted hook, a synth stab. The first second is a logo, not a note."),
     ("🥁", "Feel the drop shape", "A hard chanted drop and a soft melodic lift belong to different kinds of song. The shape, not the loudness, is the clue."),
     ("🎤", "Split the vocal lines", "Who sings first — the rapper or the vocalist — is a decision, and it usually tags the era and the group in one breath."),
    ]},
},
"Electronic": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial drops you past the festival anthems into the set-deep records only the genre faithful can place.",
    "rows": [
     ("🟢", "Easy", "Begin with the twelve the whole floor can name from the first piano lift."),
     ("🟡", "Medium", "Move up and twenty-five singalongs join, the ones that headlined a summer and then quietly left the rotation."),
     ("🟠", "Hard", "Fifty now, where texture alone has to name the subgenre — house, trance or hardstyle."),
     ("🔴", "Expert", "Expert keeps only the first filter sweep; the kick never gets to land."),
     ("💀", "Impossible", "No build, no drop, no warning — a tenth of a second of a pad and the fifty wait."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎛️", "Read the texture before the melody", "A rave stab, a piano lift or a saw bass are different rooms entirely. The first patch names the subgenre faster than any note."),
     ("🥁", "Watch how the build climbs", "The length and shape of the build is a period detail — a slow piano rise and a hard riser are years apart even at the same BPM."),
     ("🎤", "Catch the vocal entry", "A full diva hook means one school, a chopped-and-stuttered vocal another. The treatment of the voice is the tell."),
    ]},
},
"Country": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial walks you from the radio smashes back to the honky-tonk and story-song deep cuts.",
    "rows": [
     ("🟢", "Easy", "The top of the dial is twelve songs the room can name from one clean acoustic strum."),
     ("🟡", "Medium", "Twenty-five tracks next, the singles that charted without ever becoming a bar-room standard."),
     ("🟠", "Hard", "At fifty the lead instrument alone has to name the era — the steel from the fiddle."),
     ("🔴", "Expert", "The first twang is all you get, before the verse tells you anything."),
     ("💀", "Impossible", "A tenth of a second of string noise, and nothing else — that is the whole round."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎻", "Name the lead instrument", "A fiddle and a steel guitar are two different generations, and a twangy electric is a third. The first instrument is the whole map."),
     ("🎤", "Hear the drawl", "A relaxed storytelling drawl and a sharper, radio-ready tone belong to different years. The first phrase dates the record."),
     ("🥁", "Feel the two-step or the stomp", "A shuffle says traditional, a stomp-and-clap says crossover. The groove declares its allegiance before the chorus."),
    ]},
},
"Metal": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The dial only changes how far past the festival anthems you are willing to dig, toward the deep-catalog rarities.",
    "rows": [
     ("🟢", "Easy", "Start on the twelve the crowd knows from the first down-tuned chug."),
     ("🟡", "Medium", "Then twenty-five, the singles that carried the album without ever opening the set."),
     ("🟠", "Hard", "Fifty songs now, where the tuning and the drum style have to name the subgenre on their own."),
     ("🔴", "Expert", "The opening chug is the whole clue now, before the blast beat arrives."),
     ("💀", "Impossible", "Nothing but the noise floor to go on — a tenth of a second and no groove yet."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎸", "Read the riff like a fingerprint", "A thrash gallop, a melodic sweep and a slam riff are three different bands. The riff is a more honest ID than the band photo."),
     ("🥁", "Hear the drum choice", "Double-kick and blast-beat are not the same school. The first drum fill declares the subgenre before the vocal."),
     ("🎤", "Clock the vocal register", "A growl, a scream and a clean belt live in different rooms of the same genre. The voice is the fastest filter."),
    ]},
},
"1980s": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "A 103-track decade sits behind the dial — turn it past the arena anthems toward the one-hit wonders nobody mentions anymore.",
    "rows": [
     ("🟢", "Easy", "You begin with twelve songs the room knows from the first gated snare and the pad underneath."),
     ("🟡", "Medium", "The next stop is twenty-five follow-up singles that rode the MTV wave without becoming the decade's signature."),
     ("🟠", "Hard", "At fifty, a synth pad on its own has to pin down the exact year."),
     ("🔴", "Expert", "The clip stops on the opening drum and the chorus never shows up."),
     ("💀", "Impossible", "A tenth of a second of a drum machine, no warm-up — the fifty make no concessions."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🥁", "Lock the drum sound first", "The gated snare is the decade's fingerprint — once you hear it, the chorus is almost redundant. The drum machine is the honest witness."),
     ("🎹", "Read the pad and the stab", "A shimmering pad and a staccato stab are different years within the same decade. The opening texture dates the record to the season."),
     ("🎤", "Hear the arena vocal", "A reverb-soaked belt says stadium, a cooler, thinner delivery says new wave. The first line tags the lane."),
    ]},
},
"1990s": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "A 133-track decade is on the other side of the dial — from the radio staples everyone owns to the album cuts the decade forgot.",
    "rows": [
     ("🟢", "Easy", "Open on twelve songs everyone knows, whether from the first grunge fuzz or the first boom-bap kick."),
     ("🟡", "Medium", "Widen the pool to twenty-five singles that moved units without defining the decade's sound."),
     ("🟠", "Hard", "Fifty now, where the fuzz or the 808 alone has to tell you which lane you are in."),
     ("🔴", "Expert", "Expert hands you the opening bar and nothing after it — the hook never arrives."),
     ("💀", "Impossible", "A tenth of a second of feedback, nothing else — you are committed."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎸", "Split the fuzz from the 808", "The decade ran two lanes at once — a grunge fuzz and a boom-bap 808. The first sound tells you which room the song grew up in."),
     ("🎤", "Hear the harmony or the rasp", "A stacked boy-band harmony and a lone raspy voice are opposites. The texture of the first line is the whole genre."),
     ("🥁", "Feel the swing of the loop", "A swung boom-bap loop and a straight rock beat are two different decades pretending to share one. The pocket is the tell."),
    ]},
},
"2000s": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "A 204-track decade hides behind the dial — turn it past the ringtone hooks toward the deep cuts of the download era.",
    "rows": [
     ("🟢", "Easy", "Start on the twelve the room knows from the first drum fill, the ringtone hook already half-sung."),
     ("🟡", "Medium", "Then twenty-five, the singles everyone had on an MP3 player and forgot anyway."),
     ("🟠", "Hard", "At fifty, the Auto-Tuned vocal on its own has to name the exact year."),
     ("🔴", "Expert", "The opening hook is all you get, and the chorus never arrives to help."),
     ("💀", "Impossible", "A tenth of a second of a downstroke, no second chances — the fifty offer nothing."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎛️", "Read the production stamp", "A ringtone hook, a pitch-corrected vocal and a pop-punk downstroke are three different years. The production is the timestamp."),
     ("🥁", "Feel the drum fill", "A clean, loud fill says radio rock, a looped beat says R&B and pop. The fill dates the record faster than the singer."),
     ("🎤", "Hear the Auto-Tune", "A pitch-corrected vocal points one way, a raw shouty tone another. The register of the first phrase tags the lane."),
    ]},
},
"2010s": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "The deepest pool on the site — 313 tracks — sits behind a dial that only changes how far past the festival drops you cut.",
    "rows": [
     ("🟢", "Easy", "Begin on twelve songs everyone knows, caught from the first trap hi-hat roll."),
     ("🟡", "Medium", "Twenty-five next, the hits that streamed forever without ever becoming the decade's anthem."),
     ("🟠", "Hard", "At fifty a drop on its own has to name the year it was built."),
     ("🔴", "Expert", "The roll is the whole clue; the drop never gets its shape."),
     ("💀", "Impossible", "A tenth of a second of a hi-hat, no intro — the fifty wait silently."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🥁", "Read the hi-hat roll", "A rattling trap hi-hat and a four-on-the-floor kick are two different rooms of the same decade. The drums date the track."),
     ("🎛️", "Feel the drop's shape", "A festival EDM drop and a soft looped build are years apart. The contour of the drop, not its volume, names the year."),
     ("🎤", "Catch the feat. credit", "A guest verse or a featured hook is the decade's signature. The first voice often names the collab before the title."),
    ]},
},
"2020s": {
  "challenge": {"eyebrow": "Turn the dial", "h2": "Choose Your Challenge",
    "intro": "A 105-track decade sits behind the dial — turn it past the TikTok loops toward the deep cuts of a still-unfinished era.",
    "rows": [
     ("🟢", "Easy", "Start on twelve songs everyone knows from the first fifteen-second loop, the one that is already stuck."),
     ("🟡", "Medium", "Twenty-five more, the songs that trended for a week and then vanished from every feed."),
     ("🟠", "Hard", "At fifty the loop on its own has to name the year it went viral."),
     ("🔴", "Expert", "Expert stops on the opening hook before the beat even commits."),
     ("💀", "Impossible", "A tenth of a second before the loop resets, and it is on you."),
    ]},
  "listen": {"eyebrow": "Train the ear", "h2": "What to Listen For",
    "rows": [
     ("🎛️", "Read the loop like a watermark", "A TikTok-sized loop and a bedroom-pop hush are the decade's two fonts. The first sound is a more honest ID than the artist."),
     ("🎤", "Hear the bedroom hush", "A close-mic, whispery vocal and a fuller belt are different ends of the same era. The first phrase tags the lane."),
     ("🥁", "Feel the genre-blur", "A beat that jumps from Afrobeats to pop-punk inside one hook is normal now. The surprise of the first bar is usually the whole clue."),
    ]},
},
}
