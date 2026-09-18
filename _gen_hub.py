# -*- coding: utf-8 -*-
# Generic category-hub generator (songtrivia.io/decades-style).
# Builds /guess-song-decades/, /guessable-songs/, /guess-song-artists/ by cloning the
# /song-quiz/ hub and keeping one category lane. Replaces _gen_decades.py.
import io, os, re, json, ast

BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
SRC = io.open(os.path.join(BASE, "song-quiz", "index.html"), encoding="utf-8").read()

def js(s):
    return json.dumps(s, ensure_ascii=False)

_gp = io.open(os.path.join(BASE, "_gen_pages.py"), encoding="utf-8").read()
def parse(name):
    m = re.search(r'%s\s*=\s*\[(.*?)\]\s*\n' % name, _gp, re.S)
    return ast.literal_eval("[" + m.group(1) + "]")

ARTISTS = parse("ARTISTS")   # (slug, name, count)
GENRES  = parse("GENRES")    # (slug, name, gid, count)
DECADES = parse("DECADES")   # (slug, name, count)

ARROW = ('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="qd-card-arrow" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>')

def card(slug, name, sub, img, cls, prefix="", eager=False):
    shade = '' if eager else '<span class="qd-shade"></span>'
    load = 'eager' if eager else 'lazy'
    w, h = (320, 320) if eager else (800, 320)
    arrow = '' if eager else ARROW
    return ('<a href="/%s%s/" class="qd-card %s"><span class="qd-image">'
            '<img src="%s" alt="%s" width="%d" height="%d" loading="%s" />%s</span>'
            '<span class="qd-card-copy"><strong>%s</strong><span>%s</span></span>%s</a>'
            % (prefix, slug, cls, img, name, w, h, load, shade, name, sub, arrow))

def cards_html(spec):
    rows = [card(s, n, sub, img, 'qd-card-' + spec["kind"], spec.get("prefix", ""), spec["kind"] == "artist")
            for s, n, sub, img in spec["cards"]]
    return '\n      '.join(rows)

def faq_html(faq):
    out = []
    for i, (q, a) in enumerate(faq):
        out.append('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a))
    return '\n        '.join(out)

def faq_json_body(faq):
    return ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                    % (js(re.sub(r'<[^>]+>', '', q)), js(re.sub(r'<[^>]+>', '', a))) for q, a in faq)

def jsonld(spec):
    crumb = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
             '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},'
             '{"@type":"ListItem","position":2,"name":%s,"item":"https://www.songguesser.co/%s/"}]}'
             % (js(spec["nav"]), spec["slug"]))
    items = ','.join('{"@type":"ListItem","position":%d,"name":%s,"url":"https://www.songguesser.co/%s%s/"}'
                     % (i + 1, js(c[1]), spec.get("prefix", ""), c[0]) for i, c in enumerate(spec["cards"]))
    ilist = '{"@context":"https://schema.org","@type":"ItemList","name":%s,"itemListElement":[' % js(spec["item"]) + items + ']}'
    faqj = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + faq_json_body(spec["faq"]) + ']}'
    return ('<script type="application/ld+json">\n' + crumb + '\n</script>\n'
            '<script type="application/ld+json">\n' + ilist + '\n</script>\n'
            '<script type="application/ld+json">\n' + faqj + '\n</script>\n')

def directory_html(spec):
    return ('<section class="quiz-directory" aria-label="%s">\n'
            '  <h2 class="qd-title">%s</h2>\n'
            '  <div class="qd-grid qd-grid-%s">\n      %s\n  </div>\n'
            '</section>\n'
            % (spec["aria"], spec["dir_h2"], spec["kind"], cards_html(spec)))

def seo_html(spec):
    s = spec
    return ('<section class="qd-seo">\n'
            '  <div class="qd-seo-inner">\n'
            '    <section class="qd-seo-block">\n'
            '      <p class="qd-seo-eyebrow">%s</p>\n'
            '      <h2>%s</h2>\n'
            '      <p>%s</p>\n'
            '      <p>%s</p>\n'
            '    </section>\n'
            '\n'
            '    <section class="qd-seo-block">\n'
            '      <p class="qd-seo-eyebrow">%s</p>\n'
            '      <h2>%s</h2>\n'
            '      <div class="qd-seo-col">\n'
            '        %s\n'
            '      </div>\n'
            '    </section>\n'
            '\n'
            '    <section class="qd-seo-block">\n'
            '      <p class="qd-seo-eyebrow">%s</p>\n'
            '      <h2>%s</h2>\n'
            '      <div class="qd-seo-faq">\n'
            '        %s\n'
            '      </div>\n'
            '    </section>\n'
            '\n'
            '    <section class="qd-seo-cta">\n'
            '      <p class="qd-seo-eyebrow">%s</p>\n'
            '      <h2>%s</h2>\n'
            '      <p>%s</p>\n'
            '      <a href="/">Start playing \u2192</a>\n'
            '    </section>\n'
            '  </div>\n'
            '</section>\n' % (
                s["eyebrow"], s["h2"], s["p1"], s["p2"],
                s["ey2"], s["h22"], s["cols"],
                s["faq_eyebrow"], s["faq_h2"], faq_html(s["faq"]),
                s["cta_eyebrow"], s["cta_h2"], s["cta_p"]))

def build(spec):
    h = SRC
    h = h.replace('<h1>Song Quiz</h1>\n  <p>Pick a song quiz by artist, genre, or decade, then name the track from the shortest clip you can beat.</p>',
                  '<h1>%s</h1>\n  <p>%s</p>' % (spec["h1"], spec["intro"]))
    h = h.replace('<title>Song Quiz by Genre, Era & Artist | Song Guesser</title>', '<title>%s</title>' % spec["title"])
    h = h.replace('<meta name="description" content="Pick a song quiz by genre, decade, or artist and name the track from a 0.1-second clip. Free Heardle-style song guessing game with no signup." />',
                  '<meta name="description" content="%s" />' % spec["desc"])
    h = h.replace('<link rel="canonical" href="https://www.songguesser.co/song-quiz/" />', '<link rel="canonical" href="https://www.songguesser.co/%s/" />' % spec["slug"])
    h = h.replace('<meta property="og:title" content="Song Quiz by Genre, Era & Artist | Song Guesser" />', '<meta property="og:title" content="%s" />' % spec["ogtitle"])
    h = h.replace('<meta property="og:description" content="Pick a song quiz by genre, decade, or artist, then name the track from a 0.1-second clip." />',
                  '<meta property="og:description" content="%s" />' % spec["ogdesc"])
    h = h.replace('<meta property="og:url" content="https://www.songguesser.co/song-quiz/" />',
                  '<meta property="og:url" content="https://www.songguesser.co/%s/" />' % spec["slug"])
    h = h.replace('<meta name="twitter:title" content="Song Quiz by Genre, Era & Artist | Song Guesser" />',
                  '<meta name="twitter:title" content="%s" />' % spec["ogtitle"])
    h = h.replace('<meta name="twitter:description" content="Pick a song quiz by genre, decade, or artist, then name the track from a 0.1-second clip." />',
                  '<meta name="twitter:description" content="%s" />' % spec["ogdesc"])
    h = re.sub(r'(?:<script type="application/ld\+json">\s*\{[^{]*"@type":"BreadcrumbList".*?</script>\s*)?<script type="application/ld\+json">\s*\{[^{]*"@type":"FAQPage".*?</script>', jsonld(spec), h, count=1, flags=re.S)
    h = h.replace('class="songspot-site-nav-link active" href="/song-quiz/"', 'class="songspot-site-nav-link" href="/song-quiz/"')
    h = h.replace('<a class="songspot-site-nav-link" href="/#how-to-play">How to Play</a>',
                  '<a class="songspot-site-nav-link active" href="/%s/">%s</a>\n      <a class="songspot-site-nav-link" href="/#how-to-play">How to Play</a>' % (spec["slug"], spec["nav"]))
    menu_marker = "document.querySelectorAll('.songspot-site-quiz-menu')"
    mi = h.index(menu_marker)
    menu_open = h.rindex('<script>', 0, mi)
    dir_open = h.rindex('<script>', 0, menu_open)
    h = h[:dir_open] + h[menu_open:]
    start_dir = h.index('<section class="quiz-directory"')
    start_footer = h.index('<footer class="songspot-site-footer">')
    h = h[:start_dir] + directory_html(spec) + seo_html(spec) + h[start_footer:]
    d = os.path.join(BASE, spec["slug"])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(h)
    print("WROTE", spec["slug"])

# ---- specs ----------------------------------------------------------------
DECADE_FAQ = [
    ("How is a decade quiz different from an artist quiz?", "An artist quiz asks you to know one catalog; a decade quiz asks you to know how a whole era sounds. Ten years of records share one production stamp \u2014 gated reverb in the 1980s, boom-bap drums in the 1990s, Auto-Tuned hooks in the 2000s \u2014 so a guessable song is one whose first half-second places its decade on its own. It tests your era memory, not any single artist's discography."),
    ("Which decade is the hardest?", "The one you did not live through, almost always. A decade you heard on the radio as it happened feels obvious, while an era from before your time is full of songs you know only by title. The difficulty dial runs from Easy to Impossible, so any era can be made fair or brutal \u2014 and many players find the 1980s hardest on Impossible, where even a guessable song can hide its year in a blur of synth stabs."),
    ("Do I need to know the exact year a song came out?", "No. You only need to recognize the track itself. The year matters only as a clue about the sound \u2014 the drum machine, the guitar tone, the mastering. A 1990s grunge riff and a 2010s EDM drop are decades apart, but a guessable song never asks you to name the month it dropped, just the song."),
    ("How many songs are in each decade?", "The 1980s pool holds 103 songs, the 1990s 133, the 2000s 204, the 2010s 313, and the 2020s 105. The pools grow as the streaming era deepens, which is why the 2010s is the largest. Every pool of guessable songs reshuffles each round, so the same decade rarely opens with the same song twice."),
    ("Is the decade quiz free?", "Yes. Every guessable song round is free — no signup, no download, no daily cap and nothing to install. Because the whole quiz lives in your browser, you can jump from the 1980s to the 2020s in one sitting without ever logging in or opening an app."),
]

GENRE_FAQ = [
    ("What makes a song guessable?", "The production. A guessable song has a signature in its opening half-second \u2014 a drum fill, a synth stab, a vocal breath \u2014 that pins the style before the title arrives. The genre only decides which pool of guessable songs a round is drawn from."),
    ("Which genre is the hardest?", "The one you listen to least. A sound you know well feels guessable from a tenth of a second; an unfamiliar one stays hard even at the full reveal."),
    ("Do I need to know the exact genre to answer?", "No. You only need to name the track. The genre sets the pool of guessable songs, but the answer is always the title."),
    ("How many songs are in each genre?", "Pop holds 1046, R&B 801, K-Pop 796, Electronic 677, Rock 672, Hip-Hop 631, Country 483 and Metal 400. Each pool of guessable songs reshuffles every round."),
    ("Is the genre quiz free?", "Yes \u2014 every guessable song round is free with no signup, no download and no daily limit. Like the rest of <a href=\"/\">Song Guesser</a>, it runs entirely in the browser."),
]

ARTIST_FAQ = [
    ("How is an artist quiz different from a genre quiz?", "A genre quiz mixes many artists who share a sound; an artist quiz stays inside one performer's catalog. One asks you to name the style, the other to name the track. In both, a guessable song is one you can place from its first half-second."),
    ("Which artist is the hardest?", "Whichever catalog you know least deeply. An artist you only know from the radio will stump you on album cuts, while a favorite's guessable songs feel easy from a tenth of a second."),
    ("Do I need to know the album or the year?", "No. You only need to recognize the song. The catalog sets the pool, but the answer is always the title \u2014 never the release date or the album name. A guessable song gives itself away on the recording alone."),
    ("How many songs does each artist have?", "Catalogs range from 28 songs for Playboi Carti up to 77 for Travis Scott and Sabrina Carpenter. The guessable songs in each catalog reshuffle every round."),
    ("Is the artist quiz free?", "Yes \u2014 every guessable song round is free with no account, no app, no signup and no daily limit. There is nothing to install: open any of the 35 catalogs and the first clip plays at once, straight from your browser."),
]

decade_tags = {
    "1980s": "synth-pop, glam metal, hip-hop's first wave",
    "1990s": "grunge, boy bands, hip-hop's golden age",
    "2000s": "TRL hits, ringtones, pop-punk",
    "2010s": "streaming, EDM drops, the feat. era",
    "2020s": "TikTok virality, genre-blurring pop",
}
genre_tags = {
    "pop": "hooks, choruses, chart toppers", "rock": "riffs, power chords, anthems",
    "hip-hop": "beats, bars, 808s", "r-and-b": "grooves, falsettos, slow jams",
    "k-pop": "groups, choreo, fan chants", "electronic": "drops, synths, four-on-the-floor",
    "country": "twang, storytelling, pedal steel", "metal": "riffs, screams, double kick",
}

SPECS = {
    "decades": dict(
        slug="guess-song-decades", kind="decade", nav="Decades", item="Guessable Songs by Decade", prefix="guess-song-decades/",
        title="Guessable Songs by Decade | Song Guesser",
        desc="Guessable songs by decade: 1980s, 1990s, 2000s, 2010s and 2020s quizzes. Name the track from a 0.1-second clip, free with no signup.",
        ogtitle="Guessable Songs by Decade | Song Guesser",
        ogdesc="Guessable songs by decade from a 0.1-second clip \u2014 1980s, 1990s, 2000s, 2010s and 2020s music quizzes.",
        h1="Guessable Songs by Decade", intro="Guess the song of every era \u2014 the 1980s, 1990s, 2000s, 2010s and 2020s. Pick a decade and name the guessable song from the shortest clip you can beat.",
        aria="Choose a decade", dir_h2="Choose your decade",
        cards=[(s, n, '%d songs \u00b7 %s' % (c, decade_tags[s]), '/images/cards/decade-%s.svg' % s) for s, n, c in DECADES],
        eyebrow="Hear the era", h2="What makes a decade's songs guessable?",
        p1="A decade quiz pulls every round from one era, and the guessable songs are the ones stamped by their time \u2014 a gated drum from 1985, a grunge riff from 1994, a ringtone hook from 2006. You hear a tenth of a second of a real track and name it before the longer reveals give it away. The tell is not who was charting, it is the production.",
        p2="Because the pool spans many artists at once, the giveaway is the era itself \u2014 the reverb, the drum machine, the mastering. This is a Heardle-style song guessing game, and the opening clip is a tenth of a second, not a full one, with 858 tracks across the five decades. Play them all as a <a href=\"/\">song guesser</a> \u2014 no account, no download, no daily cap.",
        ey2="Five decades, five tells", h22="The five decades, one by one",
        cols=('<article><h3>The 1980s \u2014 103 songs</h3><p>Gated snares, synth pads, and arena-sized guitars are the 1980s calling card, from new wave to glam metal. If the drum sounds like it is hitting the back wall of a stadium, you are in the right decade.</p></article>'
              '<article><h3>The 1990s \u2014 133 songs</h3><p>Grunge fuzz, boom-bap drums, and boy-band harmonies fill the 1990s pool. Check the guitar tone and the drum loop first \u2014 the decade usually announces itself before the chorus does.</p></article>'
              '<article><h3>The 2000s \u2014 204 songs</h3><p>Ringtone hooks, Auto-Tuned vocals, and pop-punk downstrokes run through 204 tracks. The intros are short and loud, so a single drum fill or vocal effect often names the year before the melody.</p></article>'
              '<article><h3>The 2010s \u2014 313 songs</h3><p>The largest pool, built on trap hi-hats, EDM drops, and the "feat." credit. A hi-hat roll or a build-up usually gives the track away before the chorus lands.</p></article>'
              '<article><h3>The 2020s \u2014 105 songs</h3><p>TikTok-sized loops and genre-blurring beats fill the smallest and wildest pool. One hook can jump from Afrobeats to pop-punk, which makes this the hardest era to pin by style alone.</p></article>'),
        faq_eyebrow="Before you play", faq_h2="Decade guessable songs FAQ",
        cta_eyebrow="Pick your era", cta_h2="Ready to name a guessable song by decade?", cta_p="Choose a decade and start each guessable song round from the shortest clip.",
        faq=DECADE_FAQ,
    ),
    "genres": dict(
        slug="guessable-songs", kind="genre", nav="Genres", item="Guessable Songs", prefix="guessable-songs/",
        title="Guessable Songs | Song Guesser",
        desc="Guessable songs by genre: Pop, Rock, Hip-Hop, R&B, K-Pop, Electronic, Country and Metal. Name the track from a 0.1-second clip, no signup.",
        ogtitle="Guessable Songs | Song Guesser",
        ogdesc="Guessable songs by genre from a 0.1-second clip \u2014 Pop, Rock, Hip-Hop, R&B, K-Pop, Electronic, Country and Metal music quizzes.",
        h1="Guessable Songs", intro="Eight pools of guessable songs \u2014 Pop through Metal. Pick a sound and name the guessable song from the shortest clip you can beat.",
        aria="Choose a genre", dir_h2="Choose your genre",
        cards=[(s, n, '%d songs \u00b7 %s' % (c, genre_tags[s]), '/images/cards/genre-%s.svg' % s) for s, n, g, c in GENRES],
        eyebrow="Hear the style", h2="What makes a song guessable?",
        p1="Some songs you can place in a tenth of a second \u2014 a single drum hit, a synth swell, or a breath is all it takes. Every pool here collects those from one sound: Pop, Rock, Hip-Hop, R&B, K-Pop, Electronic, Country or Metal. You hear a sliver of a real track and name it before the longer reveals hand you the answer.",
        p2="Each pool mixes many artists at once, so the game tests whether you can read a sound from its production alone \u2014 the guitar tone, the drum pattern, the vocal register. It is a Heardle-style song guessing game, so a track's first half-second should tell you it could not belong to any other style. Play it as a <a href=\"/\">song guesser</a> for whichever sound fits your mood, with no account and no download.",
        ey2="Eight genres, eight tells", h22="The eight genres of guessable songs, one by one",
        cols=('<article><h3>Pop \u2014 1046 songs</h3><p>The biggest pool, built on hooks and choruses you have heard a thousand times. The first tenth of a second usually front-loads the catchiest part, so the synth or the breath gives it away.</p></article>'
              '<article><h3>Rock \u2014 672 songs</h3><p>Power chords, crashing riffs, and arena-sized anthems. The guitar tone is the tell \u2014 a clean intro, a fuzz lick, or a palm-muted build names the era and the band.</p></article>'
              '<article><h3>Hip-Hop \u2014 631 songs</h3><p>808s, bars, and the drum loop that anchors the whole track. Catch the snare pattern or the producer tag and the song usually names itself.</p></article>'
              '<article><h3>R&B \u2014 801 songs</h3><p>Grooves, falsettos, and slow-jam pacing. The vocal run or the warm chord bed is usually enough to separate R&B from its neighbors.</p></article>'
              '<article><h3>K-Pop \u2014 796 songs</h3><p>Groups, choreo-sized drops, and fan chants baked into the mix. The production jumps between sections fast, so one effect can name both the track and the group.</p></article>'
              '<article><h3>Electronic \u2014 677 songs</h3><p>Drops, synths, and a four-on-the-floor kick. The build-up is the giveaway \u2014 count the bars and the drop usually lands on the title you are typing.</p></article>'
              '<article><h3>Country \u2014 483 songs</h3><p>Twang, storytelling, and pedal steel. A steel lick or a drawled opening word is usually the whole clue.</p></article>'
              '<article><h3>Metal \u2014 400 songs</h3><p>Riffs, screams, and double-kick drums. The guitar attack is the tell \u2014 a down-tuned chug or a blast beat identifies the sub-genre before the vocal does.</p></article>'),
        faq_eyebrow="Before you play", faq_h2="Guessable songs FAQ",
        cta_eyebrow="Pick your sound", cta_h2="Ready to name a guessable song?", cta_p="Pick a genre and start each guessable song round from the shortest clip.",
        faq=GENRE_FAQ,
    ),
    "artists": dict(
        slug="song-guesser-artists", kind="artist", nav="Artists", item="Guessable Songs by Artist", prefix="song-guesser-artists/",
        title="Guessable Songs by Artist | Song Guesser",
        desc="Guessable songs by artist: 35 catalogs, The Weeknd to Taylor Swift, BTS to Bad Bunny. Name the track from a 0.1-second clip, no signup.",
        ogtitle="Guessable Songs by Artist | Song Guesser",
        ogdesc="Guessable songs by artist from a 0.1-second clip \u2014 35 catalogs, from The Weeknd to Taylor Swift, BTS to Bad Bunny.",
        h1="Guessable Songs by Artist", intro="Pick a catalog \u2014 35 artists \u2014 and name each guessable song from its real opening sound, before the chorus hands you the answer.",
        aria="Choose an artist", dir_h2="Choose your artist",
        cards=[(s, n, '%d songs' % c, '/images/artists/%s.jpg' % s) for s, n, c in ARTISTS],
        eyebrow="Know the catalog", h2="What makes an artist's songs guessable?",
        p1="An artist quiz pulls every round from one performer's catalog \u2014 The Weeknd, Taylor Swift, BTS, Bad Bunny and thirty-one more. You hear real preview audio, not written trivia: a tenth of a second of a track, and longer reveals only when you ask. A song here is a recording you can place the moment it starts, because the voice, the ad-lib or the production gives the artist away before the title does.",
        p2="Because every round is one artist, the quiz rewards the ear that knows the deep cuts, not just the radio hits. The fastest solves are the ones whose first half-second could only belong to that one catalog. Reveal the 0.5, 2, 8 and 15-second stages of this Heardle-style song guessing game in order, and answer the moment the track becomes clear. Play it as a <a href=\"/\">song guesser</a> for whichever catalog you can quote by heart \u2014 no account, no app, no download.",
        ey2="Pick a lane", h22="Thirty-five catalogs, four lanes",
        cols=('<article><h3>Pop catalogs</h3><p>Taylor Swift (74), Rihanna (68), Ariana Grande (64) and Adele (50). Hooks written to be recognized in a beat, so a tenth of a second is usually enough.</p></article>'
              '<article><h3>Rap and R&B</h3><p>Travis Scott (77), Drake (69), Eminem (66) and Kendrick Lamar (62). Bars, 808s and ad-libs, where the opening beat gives the catalog away.</p></article>'
              '<article><h3>K-pop</h3><p>BTS (75), G-DRAGON (50) and BLACKPINK (37). Group chants and choreo-sized drops the fans can name in a single beat.</p></article>'
              '<article><h3>Latin and global</h3><p>Bad Bunny (56), Shakira (67), Anuel AA (51) and Pitbull (68). Bilingual hooks and reggaeton rhythms that cross languages and hemispheres.</p></article>'),
        faq_eyebrow="Before you play", faq_h2="Artist guessable songs FAQ",
        cta_eyebrow="Pick your catalog", cta_h2="Ready to name a guessable song by artist?", cta_p="Choose an artist and name each guessable song from a tenth of a second.",
        faq=ARTIST_FAQ,
    ),
}

for k in SPECS:
    build(SPECS[k])
print("DONE", len(SPECS))
