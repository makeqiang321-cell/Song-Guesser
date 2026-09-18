# -*- coding: utf-8 -*-
# One-shot upgrade of _gen_artists.py -> Heardle-Online template style.
# 1) 5-section body (About / How to Play / Tips / FAQ / Closing)
# 2) title "{Name} Song Guesser - Play {Name} Song Guesser Online", H1 "{Name} Song Guesser"
# 3) paths -> song-guesser-artists/{slug}/
# 4) unique tips / closing / faq per artist (EXTRA dict)
import io, re, json

P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_artists.py"
src = io.open(P, encoding="utf-8").read()

# ---- 1) new about_html -----------------------------------------------------
NEW_ABOUT = r'''def about_html(a):
    x = EXTRA[a['slug']]
    steps = ''.join(step(i + 1, ic, t, b) for i, (ic, t, b) in enumerate(a['steps']))
    faq = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, ans)
                  for i, (q, ans) in enumerate(x['faq']))
    return ('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div>'
      '<p>%s</p><p>%s</p>'
      '</section>\n'
      '<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>How to Play</h2></div>'
      '<p>%s</p><ol class="songspot-how-grid">%s</ol>'
      '</section>\n'
      '<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>Tips to Play Better</h2></div>'
      '<p>%s</p>'
      '</section>\n'
      '<section id="faq" class="songspot-seo-section songspot-seo-faq">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div>'
      '<div class="songspot-faq-list">%s</div>'
      '</section>\n'
      '<section class="songspot-seo-section">%s</section>\n') % (
        a['h2'], a['p1'], a['p2'],
        a['intro'], steps,
        x['tips'],
        a['faq_h2'], faq,
        x['closing'])
'''
assert re.search(r'def about_html\(a\):.*?\n\ndef build\(', src, re.S)
src = re.sub(r'def about_html\(a\):.*?\n\ndef build\(', NEW_ABOUT + '\ndef build(', src, count=1, flags=re.S)

# ---- 2) faq_json + paths ---------------------------------------------------
assert src.count("faq_json(a['faq'])") == 1
src = src.replace("faq_json(a['faq'])", "faq_json(EXTRA[a['slug']]['faq'])")
src = src.replace("www.songguesser.co/' + slug + '/'", "www.songguesser.co/song-guesser-artists/' + slug + '/'")
src = src.replace('href="/%s/"', 'href="/song-guesser-artists/%s/"')
src = src.replace("d = os.path.join(BASE, slug)", 'd = os.path.join(BASE, "song-guesser-artists", slug)')

# ---- 3) per-artist unique content ------------------------------------------
EXTRA = {
 "the-weeknd": {
  "tips": "Lock onto the first synth color before the vocal lands — “Blinding Lights” opens with a rising arp, while “Starboy” leans on a low filtered pulse. If the sliver is dry and drum-free, you are usually inside one of the slower After Hours ballads, so reach for those titles first.",
  "closing": "The Weeknd Song Guesser turns his catalog into a tenth-of-a-second test — neon synths, bruised falsetto and all. When the 65-track pool starts to feel familiar, the main Song Guesser opens the door to every other artist, genre and decade on the site.",
  "faq": [
   ["Do the clips always start at the song intro?", "They open at the real start of each track, not a random spot, so the first 0.1 seconds is always the record's actual intro. That keeps it fair — you are naming the song from the same first impression a radio listener gets."],
   ["Why are there 65 Weeknd songs and not the full discography?", "The pool is curated around the intros that read best in a split second — the hits plus the most recognizable album cuts. Obscure b-sides are left out so a casual fan still has a fair chance."],
   ["Does it play the whole track after I guess?", "No. It is an identification game, not a streamer, so the round ends the moment you name it and the next clip loads. That is exactly why guessing from the shortest clip is the real flex."],
  ],
 },
 "taylor-swift": {
  "tips": "Place the era first. A twangy acoustic strum points to her early country records, while a slick 808 and a half-whispered cadence point to reputation and after. Naming the era usually cuts the search in half before you reveal more audio.",
  "closing": "Taylor Swift Song Guesser runs from Nashville twang to synth-pop and the hushed textures of folklore, all at a tenth of a second. When you have worn out her 74-song pool, the main Song Guesser has 34 more artists plus genre and decade quizzes waiting.",
  "faq": [
   ["How are her re-recorded versions handled?", "The pool uses the original recordings, not Taylor's Versions, so the intros you hear are the ones that first hit the radio. That keeps the guess fair for people who memorized the originals years ago."],
   ["Does it separate her albums or mix them?", "It mixes every era into one rotating pool, so Fearless can follow Midnights back to back. There is no album filter on this page, which means you have to be ready for any era in a single sitting."],
   ["What if I only know the singles?", "Easy difficulty leans the rotation toward the radio hits such as Love Story, Shake It Off and Anti-Hero. Deeper album cuts surface more often as you raise the difficulty."],
  ],
 },
 "michael-jackson": {
  "tips": "Lock onto the drum pattern and the breath. Jackson's intros are famously rhythmic — a beatboxed groove, a gated snare or a sharp intake — and each one is distinct. If the first sound is pure percussion, you can usually place the era before any vocal arrives.",
  "closing": "Michael Jackson Song Guesser tests the King of Pop's 70 most recognizable grooves from a tenth of a second. When you can call Billie Jean from its first beat, the main Song Guesser is there with every other artist, genre and decade to keep the streak going.",
  "faq": [
   ["Are live versions or remixes in the rotation?", "No. The pool sticks to the studio recordings you know from the albums and radio, so every intro is instantly recognizable instead of relying on a remix most fans never heard."],
   ["Why do the clips start so short?", "The 0.1-second opening is the whole point — Jackson's intros were engineered to be iconic, so a single beat or breath is often enough. The longer reveals only exist as a fallback when you are stuck."],
   ["Which era is represented most?", "The pool draws from the Off the Wall through HIStory singles and the biggest album cuts, weighted toward the songs people can actually place. Obscure b-sides are left out on purpose."],
  ],
 },
 "beyonce": {
  "tips": "Her vocal runs are the fastest tell, but the arrangement usually names the song first — a horn stab means Crazy in Love, a marching-band snare means Single Ladies. Trust the production before you reach for the melody.",
  "closing": "Beyoncé Song Guesser spans the horn-heavy strut of her early hits to the stadium choruses and album-deep cuts, all at a tenth of a second. When her 55-track pool feels conquered, the main Song Guesser has every other artist and genre ready to go.",
  "faq": [
   ["How far into her discography does the pool reach?", "From the Destiny's Child era through Renaissance and Cowboy Carter, weighted toward the solo singles people can place fast. The deep cuts that appear are the ones with the most recognizable openings."],
   ["Do the visuals matter for guessing?", "Not at all — the game is audio only, a single clip and a search box. You never see a video or a lyric snippet, which keeps it about the ear rather than the eye."],
   ["Can I pick a specific album to drill?", "This page mixes her whole catalog in one rotation. If you want era-specific practice, the difficulty dial is the closest thing to a filter — Easy favors the biggest singles."],
  ],
 },
 "rihanna": {
  "tips": "Separate the dance-floor records from the ballads by the first hit — a steel drum or a four-on-the-floor kick points to her club era, a lone piano points to the torch songs. That one distinction solves most rounds before the vocal arrives.",
  "closing": "Rihanna Song Guesser runs from the steel-drum pulse of Umbrella to the pounding chorus of Diamonds, all at a tenth of a second. When her 68-track pool starts to feel automatic, the main Song Guesser is waiting with every other artist, genre and decade.",
  "faq": [
   ["Do collaborations count in the rotation?", "Yes — the pool includes her biggest features and duets, not just solo singles. If she leads the record, it can appear, so expect the occasional guest verse to help place the track."],
   ["What happens when I skip a round?", "Skipping simply reveals the next-longest clip — 0.5s, 2s, 8s, then 15s — and never locks the round. There is no penalty, so a skip is really just a request for more audio."],
   ["Is the song list the same every day?", "No. There is no daily puzzle and no fixed order — the pool reshuffles every time you play, so two visits to the page never start the same way."],
  ],
 },
 "drake": {
  "tips": "His eras are separated by mood and drums — a sparse piano and a slow knock point to the Take Care years, a brighter island bounce points to More Life and after. Name the era first and the title usually follows from the opening ad-lib.",
  "closing": "Drake Song Guesser tests the moody piano, the shimmering hooks and the island bounce of his 69-track pool at a tenth of a second. Once you have it down cold, the main Song Guesser opens up every other artist, genre and decade on the site.",
  "faq": [
   ["How are features handled in the pool?", "The rotation includes the records Drake leads, and guest verses stay in the clip, so a recognizable voice can hand you the song. You are still naming the Drake track, not the feature."],
   ["Why do some rounds feel harder than others?", "The rotation mixes deep album cuts with the radio hits on purpose. On Easy it leans to the singles; on Impossible it reaches for the mixtape cuts only devoted fans will know."],
   ["Does the 0.1-second clip favor producers or singers?", "Both, but production usually wins — Drake's beat changes are famous. A drum fill or a piano note often names the song before the vocal does, which is what the game is built on."],
  ],
 },
 "eminem": {
  "tips": "The beat is the giveaway before the bars. A tense piano loop means Lose Yourself, a rainy guitar figure means Stan, a cartoonish bounce means Without Me. Hear the production first and the cadence just confirms it.",
  "closing": "Eminem Song Guesser tests 66 tracks — the tense pianos, the rainy-night gloom and the cartoon bounce — at a tenth of a second. When his catalog is in your ear, the main Song Guesser keeps the streak alive across every other artist and decade.",
  "faq": [
   ["Do the instrumental intros give too much away?", "On purpose — Eminem's intros are some of the most recognizable in rap, so the game leans on them. The difficulty is not in the clue but in how little of it you allow yourself before guessing."],
   ["Are skits and interludes included?", "No. Only actual songs appear in the rotation, never the album skits, so every round is a real track you could name from its opening."],
   ["What separates Easy from Impossible here?", "Easy surfaces the radio staples like Lose Yourself and Stan more often and reveals longer clips sooner. Impossible reaches for album cuts and expects you to solve from the barest sliver."],
  ],
 },
 "kanye-west": {
  "tips": "His samples and drums changed every album, so the first sound is a timestamp — a sped-up soul chip means the College era, a Daft Punk stomp means Graduation, a spare 808 means Yeezus. Identify the era and the title is usually one guess away.",
  "closing": "Kanye West Song Guesser runs from chipmunk soul to the 808 era across 61 tracks at a tenth of a second. When his catalog is memorized, the main Song Guesser has every other artist, genre and decade ready to test you next.",
  "faq": [
   ["Does the pool change because albums keep getting reworked?", "The pool is fixed to the original studio versions you know, not the re-edits. That keeps the intros stable and recognizable instead of shifting every time an album gets a new cut."],
   ["Which songs are hardest to place?", "The sparest productions — a lone 808 or a single sample flip — are the hardest because they give you almost no melody. Those surface mostly on Impossible difficulty."],
   ["Can I practice one era at a time?", "Not on this page; it shuffles the whole catalog. The main Song Guesser home page is where you can hop between artists and decades to narrow your focus."],
  ],
 },
 "justin-bieber": {
  "tips": "The production is the timeline — a glossy R&B strum means his early teen-pop years, a trop-house shaker means the Purpose era, a laid-back acoustic loop means Changes and after. Lock the era from the first hit and the search narrows fast.",
  "closing": "Justin Bieber Song Guesser spans the pop-soul of Baby to the soft bounce of Peaches across 69 tracks at a tenth of a second. When his pool is mastered, the main Song Guesser opens the full catalog of artists, genres and decades.",
  "faq": [
   ["Do remixes like the Kid Laroi duet appear?", "The rotation uses the original recordings, so you hear the album and single versions rather than remixes. That keeps the intros consistent with what most listeners memorized."],
   ["Why is the difficulty dial useful here?", "His catalog shifted genres several times, so Easy favors the biggest singles and Impossible reaches for the album cuts across all eras. It is the cleanest way to match the game to how deep a fan you are."],
   ["Are acoustic versions in the mix?", "No — only the studio tracks are used, which means the opening you hear is always the one that charted rather than a stripped-back live take."],
  ],
 },
 "linkin-park": {
  "tips": "Their signature is the blend, so listen for the balance — a clean keyboard loop with no guitar means the early nu-metal era, a heavier chug with electronics means the later albums. The ratio of guitar to synth is the era stamp.",
  "closing": "Linkin Park Song Guesser tests the keys, the riffs and the electronics of their 67-track catalog at a tenth of a second. When you can name In the End from a single note, the main Song Guesser has every other artist, genre and decade waiting.",
  "faq": [
   ["Does the pool include the newer vocal era?", "It spans the full catalog, including the later recordings, but it is weighted toward the songs people can actually place from an intro. The riffs and the electronics are the giveaways either way."],
   ["What if I only know the radio hits?", "Easy difficulty leans on the singles — In the End, Numb, One Step Closer — so a casual fan can still play. The deeper cuts surface more as you turn the dial up."],
   ["Why does a tenth of a second work for a rock band?", "Their intros are built from distinctive synth lines and guitar figures that read instantly. A single keyboard stab or a chugging riff is often enough to name the track."],
  ],
 },
 "lady-gaga": {
  "tips": "Her catalog flips between dance-pop, jazz and stripped ballads, so the first sound tells you which Gaga you are dealing with — a pulsing synth means the club era, a lone piano means the ballads and duets. Use that split before you reveal anything.",
  "closing": "Lady Gaga Song Guesser runs from the electro stomp of Poker Face to the stripped-down Shallow across 69 tracks at a tenth of a second. When her eras are all in your ear, the main Song Guesser has every other artist and decade ready next.",
  "faq": [
   ["Do the jazz and soundtrack records appear?", "A few of the most recognizable ones do, but the pool is weighted toward the pop singles and the duets people know cold. The point is to be tested on what you can actually place."],
   ["Which songs trip people up most?", "The mid-tempo bridges and the less-played album cuts, because they lack the signature synth hook. Those are the rounds where the longer reveals actually earn their keep."],
   ["Is there a way to hear more without guessing wrong?", "Yes — skipping is not a failure. It advances the clip to the next length without locking anything, so you can use skips purely to buy more audio when you are close."],
  ],
 },
 "bruno-mars": {
  "tips": "His sound is a live band, so listen for the instrument that leads — a horn blast means the funk records, a finger-picked guitar means the ballads, a doo-wop sway means the early singles. The lead instrument usually names the song.",
  "closing": "Bruno Mars Song Guesser tests the horns, the doo-wop and the falsetto of his 62-track catalog at a tenth of a second. When his grooves are memorized, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Do the Silk Sonic duets count?", "They are kept separate, so this pool stays focused on his solo records and the hits he leads. That keeps the intros consistent with his own catalog rather than a side project."],
   ["What is the hardest thing to place here?", "The ballads, because they share a similar piano-and-voice opening. The funk records are the easiest — a horn or a snare usually gives the whole thing away."],
   ["Why does the game suit his music so well?", "His intros are built like radio stings — short, bright and distinctive. A tenth of a second is often the whole intro of a Bruno Mars hook, which makes the game fast and fair."],
  ],
 },
 "adele": {
  "tips": "The piano is the fingerprint — each ballad opens with its own chord voicing and tempo, and the albums have distinct feels from 19 to 30. If the sliver is a low, slow chord, think 25 and the later records; if it is a stomping snare, think Rolling in the Deep.",
  "closing": "Adele Song Guesser tests the stomp and the hush of her 50-track catalog at a tenth of a second. When her ballads are all in your ear, the main Song Guesser has every other artist, genre and decade ready to keep you guessing.",
  "faq": [
   ["Why is the pool only 50 songs?", "Her catalog is deliberately small and carefully sequenced, so 50 tracks already covers the albums and the biggest singles. The pool favors quality of intros over raw count."],
   ["Do the live versions appear?", "No — only the studio recordings are used, so the piano opening you hear is the one from the album, not a live arrangement that changes from night to night."],
   ["What is the best clue on an Adele round?", "The tempo and the key of the opening piano. 19 is sparser, 21 is bigger, 25 and 30 are warmer — that one difference usually points you to the right album before any vocal lands."],
  ],
 },
 "ariana-grande": {
  "tips": "The vocal runs are famous but the production is the faster tell — a trap-lite hi-hat means the thank u, next era, a glossy synth means the earlier pop years. Hear the beat texture first and let the whistle tone just confirm it.",
  "closing": "Ariana Grande Song Guesser spans the trap-lite bounce and the glossy pop of her 64-track catalog at a tenth of a second. When her runs are all in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   ["Does the pool lean toward recent albums?", "It balances the whole career, from the early pop singles through the R&B-leaning recent records. Easy favors the biggest radio hits; Impossible reaches for the album deep cuts."],
   ["Are collabs and features in the rotation?", "Only the songs she leads, so the guess is always an Ariana Grande track rather than a feature. Guest verses can still appear inside the clip to help you place it."],
   ["What gives a song away fastest?", "The beat texture — her production shifts clearly between eras. A whistle tone is a strong clue, but the hi-hat and the synth usually name the song even before she sings."],
  ],
 },
 "billie-eilish": {
  "tips": "Her sound lives in the bass and the breath, so listen below the melody — a slinky sub-bass means bad guy, a soft reverb wash means the ballads, a blown-out guitar means Happier Than Ever. The low end is the whole clue.",
  "closing": "Billie Eilish Song Guesser tests the hushed verses and the blown-out choruses of her 58-track catalog at a tenth of a second. When her low end is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Why do the clips feel so quiet to start?", "Because her records are built on quiet, bass-heavy intros rather than loud hooks. The 0.1-second opening is a whisper or a bass thump, which is exactly the signature the game wants you to catch."],
   ["Do the music-video versions differ?", "The game uses the studio audio, not the video edits, so the clip is always the track as it was released. You never have to match a specific visual moment."],
   ["What trips players up on her songs?", "The ballads share a similar reverb-soaked opening, so a quiet sliver can sound like several tracks. Letting the clip reach 2s or 8s on those rounds is the smart play."],
  ],
 },
 "ed-sheeran": {
  "tips": "The loop is the signature — his songs are built on a single looped guitar or percussion figure, and each one is distinct. Lock the rhythm of the loop before the melody and you can usually name the track from the first strum.",
  "closing": "Ed Sheeran Song Guesser tests the loop-pedal pop of his 70-track catalog at a tenth of a second. When his loops are all in your ear, the main Song Guesser has every other artist, genre and decade ready to keep you guessing.",
  "faq": [
   ["Are the acoustic and pop versions separated?", "The pool uses the studio singles as released, so you hear the chart version rather than a live loop-pedal take. That keeps the intros consistent with what most listeners know."],
   ["Why do some rounds feel like the same song?", "His loops are close cousins across albums, which is part of the challenge. The difficulty dial helps — Easy leans on the unmistakable hits like Shape of You and Thinking Out Loud."],
   ["Do collaborations appear?", "The rotation includes the duets he leads, so a guest voice can sometimes hand you the track. The guess is always an Ed Sheeran song."],
  ],
 },
 "coldplay": {
  "tips": "Their two eras are split by instrumentation — a clean piano or an acoustic strum means the early records, a synth pad and a digital sheen means the later ones. Identify the era from the first chord and the title is usually one guess away.",
  "closing": "Coldplay Song Guesser spans the reverb-washed rock and the electronic later records across 68 tracks at a tenth of a second. When their catalog is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Does the pool span the whole career?", "Yes, from Parachutes through the recent records, weighted toward the songs people can place fast. The early piano-led tracks and the later synth tracks sit side by side in the same rotation."],
   ["What gives a Coldplay song away fastest?", "The opening texture — a piano figure, a string swell or a synth pad. Their intros are atmospheres first, melodies second, so the first sound is usually the strongest clue."],
   ["Are the collaborations in the mix?", "A few of the most recognizable ones appear, but the pool centers on their own songs so the guess stays focused on the band."],
  ],
 },
 "bts": {
  "tips": "Their catalog mixes Korean and English singles, so the production is the first tell — a disco sparkle means the English-era hits, a layered hip-hop beat means the earlier records. Place the era and the language of the hook follows naturally.",
  "closing": "BTS Song Guesser tests the beat drops and the layered pop of their 75-track catalog at a tenth of a second. When their discography is in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   ["Are solo tracks from the members included?", "The rotation focuses on group songs rather than the solo records, so every round is a BTS track you can name from the band's signature. That keeps the pool consistent."],
   ["How are Korean and English versions handled?", "The pool uses the released versions as they charted, so a track appears in the form listeners actually know. You never have to distinguish between a Korean and an English take of the same song."],
   ["What is the strongest clue on their songs?", "The intro beat — BTS records open with distinctive synth stabs, chants and drops. A single drum or a vocal sample usually names the track before the chorus arrives."],
  ],
 },
 "blackpink": {
  "tips": "Every comeback has its own signature opening — a marching stomp, a chanted drop, a bass thump — so the first half-second is a timestamp. Learn the opening of each single and the 37-track pool shrinks to a handful of easy rounds.",
  "closing": "BLACKPINK Song Guesser tests the stomp and the chants of their 37-track catalog at a tenth of a second. When every comeback is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Why is the pool smaller than other artists?", "Their catalog is compact on purpose — fewer songs, each with a huge, distinct intro. A smaller pool means the game leans on recognition of each single rather than volume."],
   ["Do the solo releases appear?", "No — the rotation stays focused on the group's songs, so every round is a BLACKPINK track. The solo records are kept separate."],
   ["What separates their intros from each other?", "Each title track was built around a signature opening — a marching snare, a bass growl or a chanted hook. That is exactly why a tenth of a second is usually enough to place it."],
  ],
 },
 "gdragon": {
  "tips": "His sound kept mutating, so the first beat is a timestamp — a neon synth burst means the early solo years, a self-lacerating guitar means the later records, a BIGBANG-era bounce means the group work. Identify the era and the title follows.",
  "closing": "G-DRAGON Song Guesser spans the neon bursts and the shape-shifting pop of his 50-track catalog at a tenth of a second. When his solo and group eras are all in your ear, the main Song Guesser has every other artist and decade waiting.",
  "faq": [
   ["Are BIGBANG songs in the pool?", "A few of his most recognizable group-era tracks appear alongside the solo records, since his sound crosses both. The guess is always a G-DRAGON record either way."],
   ["How do I tell his eras apart by ear?", "The production palette changed almost every album — early records are neon and electro, later ones are more minimal and melodic. The first synth or drum usually names the era."],
   ["Why does Easy help more here?", "His catalog is deep and varied, so Easy surfaces the best-known tracks like Crayon and Crooked more often. Impossible reaches for the solo deep cuts and features."],
  ],
 },
 "david-guetta": {
  "tips": "His records live on the build and the drop, so the first sound is a genre stamp — a piano lift means the vocal-house era, a big-room synth means the festival years. Name the era from the opening and the title is usually one guess away.",
  "closing": "David Guetta Song Guesser spans the piano lifts and the festival drops of his 64-track catalog at a tenth of a second. When his build-ups are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Are the collabs and features included?", "Yes — the rotation includes his biggest collaborations, since they are the records he leads. A guest vocal often hands you the song, but the guess is still a David Guetta track."],
   ["What gives his songs away fastest?", "The opening chord or synth before the vocal drops in. His intros are built as radio stings, so a single piano note or a synth stab usually names the record."],
   ["Do the remixes count as separate songs?", "No — the pool uses the original single versions, not the countless remixes. That keeps the intros consistent with the songs people actually remember."],
  ],
 },
 "pitbull": {
  "tips": "The horn and the shout are the calling card — a brass blast means the party records, a four-on-the-floor kick means the club crossovers. Lock the lead instrument first and the title usually lands from the opening shout.",
  "closing": "Pitbull Song Guesser tests the horns and the party-starting bounce of his 68-track catalog at a tenth of a second. When his anthems are in your ear, the main Song Guesser has every other artist, genre and decade ready to keep the streak alive.",
  "faq": [
   ["Do the guest verses stay in the clip?", "Yes — his biggest hits are collaborations, so a guest vocal or a borrowed hook often appears. You are still naming the Pitbull track, but the feature can hand it to you."],
   ["What is the hardest thing to place here?", "The deep album cuts that never got the single treatment, because they lack the signature horn. Those mostly surface on Impossible difficulty."],
   ["Why does a tenth of a second suit his music?", "His intros are built to start a party instantly — a horn blast or a kick drum on beat one. The very first sound is usually the giveaway."],
  ],
 },
 "kendrick-lamar": {
  "tips": "His albums each have a sonic stamp, so the first sound names the record — a jittery piano means To Pimp a Butterfly, a jazz-funk bounce means DAMN., a g-funk shimmer means the recent era. Place the album and the title follows.",
  "closing": "Kendrick Lamar Song Guesser spans the jazz-inflected beats and the beat switches of his 62-track catalog at a tenth of a second. When his eras are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Do the beat switches affect the clips?", "The clips stay at the intro, so you hear the first 0.1 seconds of the track as recorded — even on songs that switch later. The switch never jumps you forward mid-round."],
   ["Which albums are covered?", "From Section.80 through the recent releases, weighted toward the tracks people can place from an intro. The deeper narrative cuts appear mostly on harder difficulties."],
   ["What is the strongest clue on his songs?", "The drum pattern and the vocal bend. His intros are production-first, so a snare or a sample flip usually names the record before the verse begins."],
  ],
 },
 "olivia-rodrigo": {
  "tips": "Her two modes are easy to separate — a lone piano means the ballads, a crunchy guitar downstroke means the pop-punk cuts. The very first instrument names the song family, and the title is usually one guess from there.",
  "closing": "Olivia Rodrigo Song Guesser spans the diary-style ballads and the pop-punk sneer of her 50-track catalog at a tenth of a second. When her hooks are in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   ["Why is the pool 50 songs across two albums?", "Her catalog is still compact, so 50 tracks covers both records plus the biggest singles and non-album cuts. The pool will grow as her discography does."],
   ["Do the acoustic versions appear?", "No — the game uses the studio recordings, so you hear the album production rather than a stripped-back take. That keeps every intro consistent."],
   ["What trips players up on her songs?", "The ballads share a similar piano opening, so a quiet sliver can sound like several tracks. Waiting for the 2s reveal on those rounds is usually the smarter move."],
  ],
 },
 "lana-del-rey": {
  "tips": "Her records live in atmosphere — a string swell means the cinematic singles, a sparse guitar means the later folk-leaning records, a dreamy synth means the Born to Die era. Identify the texture and the title usually follows.",
  "closing": "Lana Del Rey Song Guesser spans the cinematic sweep and the Americana turn of her 52-track catalog at a tenth of a second. When her moods are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Why do her intros all sound alike?", "They share a reverb-soaked, cinematic texture on purpose, which is part of the challenge. The tell is the lead instrument — strings, guitar or synth — and the tempo of the opening."],
   ["Do the unreleased tracks appear?", "No — the pool sticks to officially released songs, so every round is a track you could have heard on an album. That keeps the game fair."],
   ["What is the hardest era to place?", "The mid-career ballads, because they blur together at a tenth of a second. The Born to Die era is the easiest thanks to its distinct synth-and-strings opening."],
  ],
 },
 "maroon-5": {
  "tips": "Their sound drifted from rock to radio pop, so the first instrument is a timestamp — a funky guitar means the early records, a glossy synth means the later singles. Name the era from the opening and the title is usually one guess away.",
  "closing": "Maroon 5 Song Guesser spans the funky guitar and the polished pop of their 72-track catalog at a tenth of a second. When their singles are in your ear, the main Song Guesser has every other artist, genre and decade ready to keep you guessing.",
  "faq": [
   ["Do the Adam Levine features appear?", "The pool stays focused on Maroon 5 songs, so his solo features and side records are kept out. The guess is always a Maroon 5 track."],
   ["What gives their songs away fastest?", "The opening riff or the synth — their singles are built around a single hook that leads the track. A funky strum or a falsetto note usually names the record."],
   ["Why does Easy help casual fans here?", "Their catalog is deep, so Easy leans on the unmistakable hits like Moves Like Jagger and Sugar. Impossible reaches for the album cuts only devoted fans will know."],
  ],
 },
 "shakira": {
  "tips": "Her catalog splits between Latin rock and global pop, and the lead instrument names the lane — a trumpet means the big singles, an Andean flute means the earlier rock records. Identify the instrument first and the title follows.",
  "closing": "Shakira Song Guesser spans the Latin rock and the global pop of her 67-track catalog at a tenth of a second. When her rhythm is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Are the Spanish and English tracks mixed together?", "Yes — the pool mixes both catalogs into one rotation, so a Spanish deep cut can follow an English smash back to back. That bilingual range is part of the challenge."],
   ["What is the strongest clue on her songs?", "The rhythm and the lead instrument — a trumpet hook, a flute line or a percussion figure. Her intros are rhythmic first, so the first beat usually names the record."],
   ["Do the World Cup anthems appear?", "The most recognizable ones do, alongside the hits and album cuts. The pool is weighted toward the songs people can actually place from an intro."],
  ],
 },
 "travis-scott": {
  "tips": "His sound is texture — an 808 with a pitched-down vocal means the mixtape era, a woozy synth drone means Astroworld, a harder, rage-leaning beat means the recent records. Name the texture from the first hit and the title follows.",
  "closing": "Travis Scott Song Guesser spans the woozy 808s and the beat switches of his 77-track catalog at a tenth of a second. When his textures are in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   ["Do the ad-libs give the song away?", "Often, yes — his ad-libs are a signature, and a single “It's lit!” or the auto-tuned hum can name the era instantly. The game leans on them just as much as the beat."],
   ["Are features included in the pool?", "The rotation includes the records he leads, and guest verses stay in the clip. The guess is always a Travis Scott track, but a feature voice can hand it to you."],
   ["Why is his catalog the biggest on this list?", "At 77 tracks, his pool is deep because his mixtapes and albums each produced recognizable intros. The harder difficulties reach for the leaks and the deep cuts."],
  ],
 },
 "sabrina-carpenter": {
  "tips": "Her sound is sharp and hook-first, so the opening is the whole clue — a disco bassline means the recent singles, a guitar strum means the earlier pop, a playful vocal means the wink-and-a-smile records. Trust the first sound.",
  "closing": "Sabrina Carpenter Song Guesser spans the disco basslines and the sharp hooks of her 77-track catalog at a tenth of a second. When her singles are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Why is the pool 77 songs?", "Her catalog stretches across several albums and EPs, and the pool pulls the intros that read best in a split second — the singles plus the most recognizable deep cuts."],
   ["Do the non-album singles appear?", "Yes — the rotation includes the standalone hits alongside the album tracks, since they are often her most recognizable records."],
   ["What is the hardest thing to place here?", "The mid-tempo tracks without the disco bounce, because they share a similar pop texture. The recent singles are the easiest thanks to their distinct basslines."],
  ],
 },
 "anuel-aa": {
  "tips": "His lane is the dembow and the rasp, so the first sound is the stamp — a reggaeton dembow means the club records, a darker trap beat means the street anthems. Identify the beat first and the title usually follows.",
  "closing": "Anuel AA Song Guesser spans the Latin trap and the reggaeton of his 51-track catalog at a tenth of a second. When his beats are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Are the collabs in the rotation?", "Yes — his biggest records are collaborations, so a guest voice or a borrowed hook often appears in the clip. The guess is always an Anuel AA track."],
   ["Do I need to know Spanish to play?", "No — you are matching the audio to a title, not reading lyrics. If you know the beat, the language of the vocal is irrelevant to the guess."],
   ["What gives his songs away fastest?", "The dembow pattern and the rasp of his voice. His intros are rhythmic first, so the first kick drum or synth line usually names the record."],
  ],
 },
 "don-toliver": {
  "tips": "His sound is wavy and melodic, so the first texture is the tell — a hazy synth wash means the early hits, a brighter bounce means the recent records, a woozy falsetto means the ballads. Name the texture and the title follows.",
  "closing": "Don Toliver Song Guesser spans the woozy synths and the falsetto of his 65-track catalog at a tenth of a second. When his melodies are in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   ["Do the features appear in the pool?", "The rotation includes the records he leads, and guest verses stay in the clip. The guess is always a Don Toliver track, but a feature voice can hand it to you."],
   ["What is the strongest clue on his songs?", "The synth wash and the falsetto note — his intros are atmospheric before they are rhythmic. A single swelling pad usually names the era."],
   ["Why does Easy help casual fans here?", "His catalog is deep and the textures blur together, so Easy leans on the unmistakable hits like No Idea and After Party. Impossible reaches for the deep cuts."],
  ],
 },
 "tate-mcrae": {
  "tips": "Her two modes are easy to split — a stomping beat means the dance-pop singles, a sparse piano means the ballads. The first sound names the lane, and the title is usually one guess from there.",
  "closing": "Tate McRae Song Guesser spans the dancer-ready pop and the wounded ballads of her 66-track catalog at a tenth of a second. When her hooks are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Why is the pool larger than her album count suggests?", "It pulls the singles, the EPs and the album deep cuts together, so 66 tracks covers her full catalog rather than just one record. The pool is weighted toward the songs people know."],
   ["Do the dance mixes appear?", "No — the game uses the studio versions, so you hear the original production rather than a remix. That keeps the intros consistent with the released tracks."],
   ["What trips players up on her songs?", "The ballads share a similar sparse opening, so a quiet sliver can sound like several tracks. Letting the clip reach 2s on those rounds is the smart play."],
  ],
 },
 "playboi-carti": {
  "tips": "His eras are separated by energy — a bouncy, minimal beat means the early records, a rage-driven wall of 808s means the recent era. The first hit names the phase, and the ad-lib confirms it.",
  "closing": "Playboi Carti Song Guesser spans the bounce and the rage of his 28-track catalog at a tenth of a second. When his eras are in your ear, the main Song Guesser has every other artist, genre and decade ready to keep the streak alive.",
  "faq": [
   ["Why is the pool only 28 songs?", "His catalog is small but dense, so 28 tracks already covers the albums and the biggest singles. A compact pool keeps every round about recognizing each record's distinct texture."],
   ["Are leaks and unreleased tracks included?", "No — the rotation sticks to officially released songs only, so every round is a track you could have heard on an album or mixtape."],
   ["What gives his songs away fastest?", "The beat energy and the baby-voice ad-lib. His intros are minimal on purpose, so the first 808 or vocal catch usually names the record."],
  ],
 },
 "bad-bunny": {
  "tips": "His sound bends reggaeton, trap and pop, so the first beat is a lane marker — a breezy dembow means the reggaeton hits, a darker synth means the trap records, a dreamy loop means the pop crossovers. Name the lane and the title follows.",
  "closing": "Bad Bunny Song Guesser spans the reggaeton, trap and pop of his 56-track catalog at a tenth of a second. When his lanes are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Do I need to know Spanish to play?", "No — you are matching audio to a title, not reading lyrics. If you know the beat, the language of the vocal does not matter for the guess."],
   ["Are the feature-heavy records included?", "Yes — his biggest records are collaborations, so a guest voice often appears in the clip. The guess is always a Bad Bunny track."],
   ["What is the strongest clue on his songs?", "The dembow pattern and the vocal bend. His intros are rhythmic first, so the first kick or synth line usually names the record before any words land."],
  ],
 },
 "katy-perry": {
  "tips": "Her hits are hook-first, so the opening is the whole clue — a stadium chant means Roar, a candy-synth sparkle means the Teenage Dream era, a slinky trap beat means Dark Horse. Trust the first sound and reach for the chorus it belongs to.",
  "closing": "Katy Perry Song Guesser spans the candy-colored pop and the stadium anthems of her 59-track catalog at a tenth of a second. When her hooks are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   ["Why is the pool 59 songs?", "It pulls the singles and the most recognizable album cuts across her whole career, weighted toward the songs people can actually place from an intro. The deepest b-sides are left out."],
   ["Do the acoustic versions appear?", "No — the game uses the studio singles, so you hear the chart production rather than a stripped-back take. That keeps every intro consistent."],
   ["What gives her songs away fastest?", "The chorus texture — her hits were built around a single unmistakable hook. A synth sparkle or a drum fill usually names the record before the verse starts."],
  ],
 },
}

extra_literal = json.dumps(EXTRA, ensure_ascii=False, indent=1)

old_loop = "for p in PAGES:\n    write(p['slug'], build(p['slug'], p['name'], p['count'], p['title'], p['desc'], p['h1'], p['hero'], p['vgdesc'], p))\n    print('WROTE', p['slug'])\nprint('DONE', len(PAGES))\n"
new_loop = ("for p in PAGES:\n"
            "    p['title'] = p['name'] + ' Song Guesser - Play ' + p['name'] + ' Song Guesser Online'\n"
            "    p['h1'] = p['name'] + ' Song Guesser'\n"
            "    write(p['slug'], build(p['slug'], p['name'], p['count'], p['title'], p['desc'], p['h1'], p['hero'], p['vgdesc'], p))\n"
            "    print('WROTE', p['slug'])\n"
            "print('DONE', len(PAGES))\n")
assert old_loop in src, "loop block not found"
src = src.replace(old_loop, "EXTRA = " + extra_literal + "\n\n" + new_loop)

io.open(P, "w", encoding="utf-8").write(src)
print("UPGRADED OK. EXTRA artists:", len(EXTRA))
