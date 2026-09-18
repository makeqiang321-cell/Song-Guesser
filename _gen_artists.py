# -*- coding: utf-8 -*-
# Hand-written artist pages in the Heardle-Online template style.
# Run: python _gen_artists.py  -> writes only the artists listed in PAGES below.
import io, os, re, json, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
try:
    from _artist_rich import RICH
except ImportError:
    RICH = {}

BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
TPL = io.open(os.path.join(BASE, "index.html"), encoding="utf-8").read()

def js(s):
    return json.dumps(s, ensure_ascii=False)

T_TITLE = '<title>Song Guesser — Free Song Guessing Game | Guess the Song</title>'
T_DESC = '<meta name="description" content="Song Guesser is a free Heardle-style song guessing game. Name a song from a 0.1-second clip, then reveal 0.5s, 2s, 8s, 15s when you need more. Five difficulty levels, no app, no login." />'
T_CANON = '<link rel="canonical" href="https://www.songguesser.co/" />'
T_OGT = '<meta property="og:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />'
T_OGD = '<meta property="og:description" content="Name the song from a 0.1-second clip. A free Heardle-style song guessing game with five difficulty levels and unlimited rounds." />'
T_OGU = '<meta property="og:url" content="https://www.songguesser.co/" />'
T_TWT = '<meta name="twitter:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />'
T_TWD = '<meta name="twitter:description" content="Name the song from a 0.1-second clip. Free, no signup." />'
T_H1 = '<h1 id="songspot-heading">Song Guesser — Guess the Song in 0.1 Seconds</h1>'
T_HERO = '<p>Song Guesser plays a tenth of a second of a real song, then you name it before the clip grows. A free Heardle-style song guessing game — five difficulty levels, no app and no login. The shorter the clip you beat, the sharper the round.</p>'
T_VG = '"@type":"VideoGame","name":"Song Guesser","description":"A free Heardle-style song guessing game where you name a track from a 0.1-second clip, then reveal longer clips when you need more."'

CLOUD_CSS = ('<style>.songspot-song-cloud{list-style:none;display:flex;flex-wrap:wrap;gap:10px;padding:0;margin:6px 0 0}'
  '.songspot-song-cloud li{background:#0b2415;border:1px solid #19df7055;color:#d6f6e1;border-radius:999px;padding:8px 16px;font-size:14px;line-height:1.4}'
  '.songspot-song-cloud li b{color:#19df70;font-weight:600}'
  '.songspot-song-cloud a{color:#d6f6e1;text-decoration:none}'
  '.songspot-song-cloud a:hover{color:#19df70}'
  '.songspot-seo-section+.songspot-seo-section{border-top:1px solid #ffffff0f}</style>\n')

def related_html(slug):
    arts = [(p['slug'], p['name']) for p in PAGES]
    idx = next(i for i, (s, n) in enumerate(arts) if s == slug)
    picked = [arts[(idx + k) % len(arts)] for k in range(1, 7)]
    links = ''.join('<li><a href="/song-guesser-artists/%s/">%s song quiz</a></li>' % (s, n) for s, n in picked)
    return ('<section id="more-quizzes" class="songspot-seo-section">'
      '<div class="songspot-seo-heading">'
      '<p class="songspot-seo-eyebrow">Keep playing</p>'
      '<h2>More song quizzes</h2></div>'
      '<ul class="songspot-song-cloud">%s</ul>'
      '</section>\n' % links)

def breadcrumb(name, slug):
    return ('<script type="application/ld+json">'
      '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
      '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},'
      '{"@type":"ListItem","position":2,"name":"Artists","item":"https://www.songguesser.co/song-guesser-artists/"},'
      '{"@type":"ListItem","position":3,"name":' + js(name) + ',"item":"https://www.songguesser.co/song-guesser-artists/' + slug + '/"}]}</script>\n')

def faq_json(qs):
    body = ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (js(re.sub(r'<[^>]+>', '', q)), js(re.sub(r'<[^>]+>', '', a))) for q, a in qs)
    return '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + body + ']}\n</script>\n'

def fixed_faq(slug):
    return [[FAQFIX.get(slug, {}).get(q, q), a] for q, a in EXTRA[slug]['faq']]

def step(n, icon, t, b):
    return '<li><span>%02d</span><span class="icon">%s</span><h3>%s</h3><p>%s</p></li>' % (n, icon, t, b)

def about_html(a):
    a = dict(a); a.update(RICH.get(a['slug'], {}))
    x = dict(EXTRA[a['slug']]); x.update(P2INTRO[a['slug']])
    sx = STEPX[a['slug']]
    steps = ''.join(step(i + 1, ic, sx['t'][i], sx['b3'] if i == 2 else b)
                    for i, (ic, t, b) in enumerate(a['steps']))
    faq = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, ans)
                  for i, (q, ans) in enumerate(fixed_faq(a['slug'])))
    out = ['<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2></div>'
      '<p>%s</p><p>%s</p></section>\n' % (a['eyebrow'], a['what_h3'], a['p1'], x['p2'])]
    c = a.get('challenge')
    if c:
        rows = ''.join('<article><span class="icon">%s</span><h3>%s</h3><p>%s</p></article>' % r for r in c['rows'])
        out.append('<section class="songspot-seo-section">'
          '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2><p>%s</p></div>'
          '<div class="songspot-feature-grid">%s</div></section>\n' % (c['eyebrow'], c['h2'], c['intro'], rows))
    s = a.get('samples')
    if s:
        pills = ''.join('<li><b>%02d</b> %s</li>' % (i + 1, t) for i, t in enumerate(s['songs']))
        out.append('<section class="songspot-seo-section">'
          '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2><p>%s</p></div>'
          '<ul class="songspot-song-cloud">%s</ul></section>\n' % (s['eyebrow'], s['h2'], s['intro'], pills))
    l = a.get('listen')
    if l:
        tips = ''.join('<article><span class="icon">%s</span><h3>%s</h3><p>%s</p></article>' % r for r in l['rows'])
        out.append('<section class="songspot-seo-section">'
          '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2></div>'
          '<div class="songspot-feature-grid">%s</div></section>\n' % (l['eyebrow'], l['h2'], tips))
    else:
        out.append('<section class="songspot-seo-section">'
          '<div class="songspot-seo-heading"><h2>Tips to Play Better</h2></div><p>%s</p></section>\n' % x['tips'])
    out.append('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div><p>%s</p><ol class="songspot-how-grid">%s</ol></section>\n' % (a['how_h3'], x['intro'], steps))
    out.append('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div><p>%s</p></section>\n' % (a['who_h3'], a['who_p']))
    out.append('<section id="faq" class="songspot-seo-section songspot-seo-faq">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div><div class="songspot-faq-list">%s</div></section>\n' % (a['faq_h2'], faq))
    out.append('<section class="songspot-seo-section">%s</section>\n' % x['closing'])
    return ''.join(out)

def build(slug, name, count, title, desc, h1, hero, vgdesc, a):
    h = TPL
    h = h.replace(T_TITLE, '<title>' + title + '</title>')
    h = h.replace(T_DESC, '<meta name="description" content="' + desc + '" />')
    h = h.replace(T_CANON, '<link rel="canonical" href="https://www.songguesser.co/song-guesser-artists/' + slug + '/" />')
    og = ('\n<meta property="og:image" content="https://www.songguesser.co/images/artists/' + slug + '.jpg" />'
          '\n<meta name="twitter:card" content="summary_large_image" />'
          '\n<meta name="twitter:image" content="https://www.songguesser.co/images/artists/' + slug + '.jpg" />')
    h = h.replace(T_OGT, '<meta property="og:title" content="' + title + '" />' + og)
    h = h.replace(T_OGD, '<meta property="og:description" content="' + desc + '" />')
    h = h.replace(T_OGU, '<meta property="og:url" content="https://www.songguesser.co/song-guesser-artists/' + slug + '/" />')
    h = h.replace(T_TWT, '<meta name="twitter:title" content="' + title + '" />')
    h = h.replace(T_TWD, '<meta name="twitter:description" content="' + desc + '" />')
    h = h.replace('"url":"https://www.songguesser.co/"', '"url":"https://www.songguesser.co/song-guesser-artists/' + slug + '/"', 1)
    h = h.replace(T_VG, '"@type":"VideoGame","name":' + js(name + ' Song Guesser') + ',"description":' + js(vgdesc))
    h = h.replace(T_H1, '<h1 id="songspot-heading">' + h1 + '</h1>')
    h = h.replace(T_HERO, '<p>' + hero + '</p>')
    h = h.replace('<script src="/decades.js"></script>', '<script>window.SONG_INITIAL = ' + js({'artist': name}) + ';</script>\n<script src="/decades.js"></script>')
    h = re.sub(r'<script type="application/ld\+json">\s*\{[^{]*"@type":"FAQPage".*?</script>',
               breadcrumb(name, slug) + faq_json(fixed_faq(a['slug'])), h, count=1, flags=re.S)
    start = h.index('<section class="songspot-seo">')
    end = h.index('<footer class="songspot-site-footer">')
    h = h[:start] + '<section class="songspot-seo">\n' + about_html(a) + related_html(slug) + '</section>\n\n' + h[end:]
    h = h.replace('</head>', CLOUD_CSS + '</head>')
    return h

def write(slug, h):
    d = os.path.join(BASE, "song-guesser-artists", slug)
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(h)

# ---- hand-written content (unique per artist, no shared sentences) ----
PAGES = [
 {
  'slug': 'the-weeknd', 'name': 'The Weeknd', 'count': 65,
  'title': 'The Weeknd Song Guesser \u2014 Guess the Weeknd Song in 0.1 Seconds',
  'desc': 'Name the Weeknd song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Weeknd song guessing game with 65 tracks \u2014 no signup, no download.',
  'h1': 'The Weeknd Song Guesser',
  'hero': 'Try to guess the Weeknd song fast \u2014 every round opens with just 0.1 seconds of audio.',
  'vgdesc': 'A free browser song guessing game on 65 The Weeknd tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Weeknd song game',
  'h2': 'About The Weeknd Song Guesser',
  'what_h3': 'What Is The Weeknd Song Guesser?',
  'p1': 'The Weeknd Song Guesser is a free audio game built on Abel Tesfaye\u2019s catalog \u2014 the neon-synth glow of \u201cBlinding Lights\u201d, the slow-burn swagger of \u201cStarboy\u201d, and the bruised falsetto of \u201cSave Your Tears\u201d. You get a tenth of a second, and you name it before the reveal starts doing your job. It’s a Heardle-style song guessing game made for Weeknd fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser \u2014 no app, no login, no daily limit. Miss or skip, and the clip steps up to 0.5s, 2s, 8s, then 15s; but the earlier you solve it, the sharper the round.',
  'how_h3': 'How to Play The Weeknd Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you are stuck.',
  'steps': [
    ('\u25b6', 'Start at 0.1 seconds', 'A tenth of a second of a Weeknd track is the whole first clue. Headphones catch the synth swell or the falsetto breath.'),
    ('\u2315', 'Type the title', 'Type part of the name and pick from the suggestions. A rhythm, a melody, or that Weeknd production sheen can place it.'),
    ('\u23ed', 'Reveal only when stuck', 'A wrong guess or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('\u267e', 'Play without limits', 'Unlimited rounds across 65 Weeknd tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Anyone who can already place a Weeknd song from its first synth hit \u2014 plus listeners who want to learn the catalog by ear. The difficulty dial runs from Easy to Impossible, so a casual fan and an obsessive fan both get a fair fight.',
  'faq_eyebrow': 'Questions about this quiz',
  'faq_h2': 'The Weeknd Song Guesser FAQ',
  'faq': [
    ('How does The Weeknd Song Guesser work?', 'Each round plays a 0.1-second clip of a Weeknd track and reveals 0.5s, 2s, 8s and 15s only when you ask. The search box stays inside the 65-song Weeknd pool.'),
    ('Is The Weeknd Song Guesser free?', 'Yes. It is a free browser game with no signup and no download \u2014 open the page and start guessing.'),
    ('Which Weeknd songs will I hear?', 'A rotating pool of 65 tracks, from \u201cBlinding Lights\u201d and \u201cStarboy\u201d to deeper album cuts.'),
  ],
 },
 {
  'slug': 'taylor-swift', 'name': 'Taylor Swift', 'count': 74,
  'title': 'Taylor Swift Song Guesser \u2014 Guess the Taylor Swift Song in 0.1 Seconds',
  'desc': 'Name the Taylor Swift song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Taylor Swift song guessing game with 74 songs \u2014 no signup, no download.',
  'h1': 'Taylor Swift Song Guesser',
  'hero': 'Can you name a Taylor Swift song from its first tenth of a second \u2014 before a single lyric lands? Every round opens on a sliver of real audio: a strum, a synth, the shape of her voice. 74 songs in the pool, five difficulty levels, no signup.',
  'vgdesc': 'A free browser song guessing game on 74 Taylor Swift songs. Name each track from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Taylor Swift song game',
  'h2': 'About Taylor Swift Song Guesser',
  'what_h3': 'What Is Taylor Swift Song Guesser?',
  'p1': 'Taylor Swift Song Guesser is a free audio game built on a catalog that keeps changing shape \u2014 the acoustic storytelling of her country years, the synth-pop gloss of \u201c1989\u201d, and the hushed indie textures of \u201cfolklore\u201d. A 0.1-second clip opens each round, and you name the track before the longer reveals do it for you. It is the Taylor Swift take on a Heardle-style song guessing game — the clip opens at 0.1 seconds, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser \u2014 no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the cleaner the round.',
  'how_h3': 'How to Play Taylor Swift Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you are stuck.',
  'steps': [
    ('\u25b6', 'Start at 0.1 seconds', 'A tenth of a second of a Swift track is the first clue \u2014 a guitar strum, a synth pulse, or the shape of her vocal.'),
    ('\u2315', 'Type the title', 'Type part of the name and pick from the suggestions. Her eras sound different, so the production usually tells you which one you are in.'),
    ('\u23ed', 'Reveal only when stuck', 'A wrong guess or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('\u267e', 'Play without limits', 'Unlimited rounds across 74 Swift songs, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who know \u201cLove Story\u201d from \u201cCruel Summer\u201d in a heartbeat, and listeners who want to trace how her sound moved from Nashville to synth-pop to folklore. Easy welcomes newcomers; Impossible is for the people who never skip a Taylor track.',
  'faq_eyebrow': 'Questions about this quiz',
  'faq_h2': 'Taylor Swift Song Guesser FAQ',
  'faq': [
    ('How does Taylor Swift Song Guesser work?', 'Each round plays a 0.1-second clip of a Taylor Swift song and reveals 0.5s, 2s, 8s and 15s only when you ask. The search box stays inside the 74-song Swift pool.'),
    ('Is Taylor Swift Song Guesser free?', 'Yes. It is a free browser game with no signup and no download.'),
    ('Which Taylor Swift songs will I hear?', 'A rotating pool of 74 tracks, from \u201cLove Story\u201d and \u201cShake It Off\u201d to \u201cAnti-Hero\u201d and deeper cuts.'),
  ],
  'challenge': {
    'eyebrow': 'Turn the dial',
    'h2': 'Choose Your Challenge',
    'intro': 'The dial digs deeper into the 74-song pool \u2014 it never changes the rules, only how far past the hits it reaches.',
    'rows': [
      ('\U0001f7e2', 'Easy', 'A dozen songs so famous they name themselves \u2014 a banjo roll or a synth pulse and you are already at the title.'),
      ('\U0001f7e1', 'Medium', 'Twenty-five tracks join the board, the era-defining singles that never became the one she opens a stadium with.'),
      ('\U0001f7e0', 'Hard', 'Fifty songs, and now the first sound alone has to tell you which era you are standing in.'),
      ('\U0001f534', 'Expert', 'The same fifty, chased to the shortest reveal you can still name.'),
      ('\U0001f480', 'Impossible', 'The deep fifty with no warm-up: the clip stays at a tenth of a second until you ask for more.'),
    ],
  },
  'samples': {
    'eyebrow': 'The rotation',
    'h2': 'Songs in the Taylor Swift Song Guesser',
    'intro': 'Eight of the 74 tracks in the pool \u2014 every era, from the twang of her first records to the synth-pop of Midnights.',
    'songs': ['Love Story', 'You Belong with Me', 'Shake It Off', 'Blank Space', 'Style', 'Cruel Summer', 'Cardigan', 'Anti-Hero'],
  },
  'listen': {
    'eyebrow': 'Train the ear',
    'h2': 'What to Listen For',
    'rows': [
      ('\U0001f3b8', 'The era is the first clue', 'A twangy acoustic strum and a pulsing synth are not the same chapter of her career. Place the decade first and the title usually falls out of the pool.'),
      ('\U0001f3a4', 'Her vocal shape is a timestamp', 'She half-whispers on reputation, confesses on folklore, and belts on 1989. The first tenth of a second often carries the whole era in her delivery.'),
      ('\U0001f3b9', 'The opening motif is the door', 'Banjo roll, door-knock beat, pulsing 808 \u2014 each era opens on its own signature. One clean sound separates Love Story from Cruel Summer.'),
    ],
  },
 },
 {
  'slug': 'michael-jackson', 'name': 'Michael Jackson', 'count': 70,
  'title': 'Michael Jackson Song Guesser \u2014 Guess the Michael Jackson Song in 0.1 Seconds',
  'desc': 'Name the Michael Jackson song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Michael Jackson song guessing game with 70 songs \u2014 no signup, no download.',
  'h1': 'Michael Jackson Song Guesser',
  'hero': 'Try to guess the Michael Jackson song fast \u2014 every round opens with just 0.1 seconds of audio.',
  'vgdesc': 'A free browser song guessing game on 70 Michael Jackson songs. Name each track from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Michael Jackson song game',
  'h2': 'About Michael Jackson Song Guesser',
  'what_h3': 'What Is Michael Jackson Song Guesser?',
  'p1': 'Michael Jackson Song Guesser is a free audio game built on a catalog defined by precision \u2014 the sharp breath before the groove, the locked-in bass line, and the stacked backing vocals of \u201cBillie Jean\u201d, \u201cBeat It\u201d and \u201cThriller\u201d. Every round starts on a sliver of audio and waits for you to call the track before it opens up. Think Heardle-style song guessing game, but for the King of Pop — and the opening clip is a tenth of a second, not a full second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser \u2014 no app, no login, no daily limit. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the sharper the round.',
  'how_h3': 'How to Play Michael Jackson Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you are stuck.',
  'steps': [
    ('\u25b6', 'Start at 0.1 seconds', 'A tenth of a second of a Jackson track is the first clue \u2014 a beatboxed intro, a bass figure, or that signature vocal.'),
    ('\u2315', 'Type the title', 'Type part of the name and pick from the suggestions. Rhythm and voice are equally strong clues in his catalog.'),
    ('\u23ed', 'Reveal only when stuck', 'A wrong guess or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('\u267e', 'Play without limits', 'Unlimited rounds across 70 Jackson tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name \u201cBillie Jean\u201d from a single beat, and listeners who want to hear how the grooves were built. Easy is a warm-up; Impossible is for the people who know the deep cuts and the ad-libs.',
  'faq_eyebrow': 'Questions about this quiz',
  'faq_h2': 'Michael Jackson Song Guesser FAQ',
  'faq': [
    ('How does Michael Jackson Song Guesser work?', 'Each round plays a 0.1-second clip of a Michael Jackson song and reveals 0.5s, 2s, 8s and 15s only when you ask. The search box stays inside the 70-song Jackson pool.'),
    ('Is Michael Jackson Song Guesser free?', 'Yes. It is a free browser game with no signup and no download.'),
    ('Which Michael Jackson songs will I hear?', 'A rotating pool of 70 tracks, from \u201cBillie Jean\u201d and \u201cBeat It\u201d to \u201cSmooth Criminal\u201d and deeper cuts.'),
  ],
 },
 {
  'slug': 'beyonce', 'name': 'Beyoncé', 'count': 55,
  'title': 'Beyoncé Song Guesser — Guess the Beyoncé Song in 0.1 Seconds',
  'desc': 'Name the Beyoncé song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Beyoncé song guessing game with 55 tracks — no signup, no download.',
  'h1': 'Beyoncé Song Guesser',
  'hero': 'Name the Beyoncé track from the shortest clip you can — every round opens on a tenth of a second.',
  'vgdesc': 'A free browser song guessing game on 55 Beyoncé tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Beyoncé song game',
  'h2': 'About Beyoncé Song Guesser',
  'what_h3': 'What Is Beyoncé Song Guesser?',
  'p1': 'Beyoncé Song Guesser is a free audio game built on a catalog that moves from the horn-heavy strut of “Crazy in Love” to the stadium-sized chorus of “Halo” and the marching-band snap of “Single Ladies”. The round opens on the shortest clip and only widens once you’ve had your guess. The Heardle-style song guessing game for Beyoncé fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily limit. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place the track, the cleaner the round.',
  'how_h3': 'How to Play Beyoncé Song Guesser',
  'intro': 'Hear the sliver, trust your ear, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open with a tenth of a second', 'A 0.1-second slice of a Beyoncé track is the whole first clue — a horn stab, a drum snap, or the first note of a run.'),
    ('⌕', 'Name the track', 'Type part of the title and pick from the suggestions. Her vocal runs and the production sheen usually give it away.'),
    ('⏭', 'Ask for more audio', 'A miss or skip stretches the clip to 0.5s, 2s, 8s and 15s. Solving it from the shortest clip is the real flex.'),
    ('♾', 'No daily cap', 'Unlimited rounds across 55 Beyoncé tracks, from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Beyoncé song from a single horn hit, and listeners who want to trace how her sound moved from Destiny’s Child to the deep album cuts. Easy warms you up; Impossible is for the people who know every bridge.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Questions About the Beyoncé Game',
  'faq': [
    ('Do I need to know her whole catalog?', 'No. You can type part of a title and pick from suggestions, and the Easy setting keeps the clips forgiving. If you know the hits such as “Crazy in Love”, you already have a head start.'),
    ('What if I keep guessing wrong?', 'Nothing locks. Every miss or skip opens the clip one step further — 0.5s, 2s, 8s, then 15s — so more of the track only arrives when you ask for it.'),
    ('Is this part of a bigger game?', 'Yes. Like every page on <a href="/">Song Guesser</a>, it is free in the browser with no signup and no download.'),
  ],
 },
 {
  'slug': 'rihanna', 'name': 'Rihanna', 'count': 68,
  'title': 'Rihanna Song Guesser — Guess the Rihanna Song in 0.1 Seconds',
  'desc': 'Name the Rihanna song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Rihanna song guessing game with 68 tracks — no signup, no download.',
  'h1': 'Rihanna Song Guesser',
  'hero': 'Guess the Rihanna song from a tenth of a second — the intro usually does the telling.',
  'vgdesc': 'A free browser song guessing game on 68 Rihanna tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Rihanna song game',
  'h2': 'About Rihanna Song Guesser',
  'what_h3': 'What Is Rihanna Song Guesser?',
  'p1': 'Rihanna Song Guesser is a free audio game built on a career that swings from the steel-drum pulse of “Umbrella” to the pounding chorus of “Diamonds” and the dance-floor charge of “We Found Love”. The clip starts at 0.1 seconds and stays there until you ask for more. It’s a Heardle-style song guessing game for Rihanna fans — but the clip starts at a tenth of a second, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily cap. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Rihanna Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you need it.',
  'steps': [
    ('▶', 'Begin at 0.1s', 'A tenth of a second of a Rihanna track is the first clue — a steel drum, a synth, or the shape of that voice.'),
    ('⌕', 'Type your guess', 'Type part of the title and pick from the suggestions. Her singles each open a little differently, so the production is a strong tell.'),
    ('⏭', 'Reveal sparingly', 'A wrong guess or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play every round', 'Unlimited rounds across 68 Rihanna tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Anyone who can name “Umbrella” from a single hi-hat, and listeners who want to learn how her pop, R&B and dance eras differ by ear. Easy welcomes newcomers; Impossible is for the fans who never missed a single.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Rihanna Song Guesser FAQ',
  'faq': [
    ('How many Rihanna songs are in the rotation?', 'Sixty-eight tracks, from the early dancehall-flavored singles to “Diamonds” and beyond. The pool rotates, so a round can land on a classic or a deep cut.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily limit.'),
    ('Can I switch to other artists later?', 'Yes. Head to the main <a href="/">Song Guesser</a> page to pick any artist, genre or decade.'),
  ],
 },
 {
  'slug': 'drake', 'name': 'Drake', 'count': 69,
  'title': 'Drake Song Guesser — Guess the Drake Song in 0.1 Seconds',
  'desc': 'Name the Drake song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Drake song guessing game with 69 tracks — no signup, no download.',
  'h1': 'Drake Song Guesser',
  'hero': 'How fast can you name the Drake track? Each round starts with a tenth of a second.',
  'vgdesc': 'A free browser song guessing game on 69 Drake tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Drake song game',
  'h2': 'About Drake Song Guesser',
  'what_h3': 'What Is Drake Song Guesser?',
  'p1': 'Drake Song Guesser is a free audio game built on a catalog that runs from the moody piano of “God’s Plan” to the shimmering hook of “Hotline Bling” and the island bounce of “One Dance”. You get a tenth of a second, and you name it before the reveal starts doing your job. A Heardle-style song guessing game aimed at Drake fans — except the opening is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the sharper the round.',
  'how_h3': 'How to Play Drake Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you are stuck.',
  'steps': [
    ('▶', 'Hear 0.1s first', 'A tenth of a second of a Drake track is the whole first clue — a piano note, a beat switch, or a vocal ad-lib.'),
    ('⌕', 'Write the title', 'Type part of the name and pick from the suggestions. His era tells you a lot — the mood and the drums shift from album to album.'),
    ('⏭', 'Unlock more only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Solving it from the shortest clip is the goal.'),
    ('♾', 'Keep going', 'Unlimited rounds across 69 Drake tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Drake song from its opening piano or a single ad-lib, and listeners who want to hear how his moody, dancehall and trap eras differ. Easy is a warm-up; Impossible is for the people who know the deep cuts.',
  'faq_eyebrow': 'Good to know',
  'faq_h2': 'Drake Song Guesser FAQ',
  'faq': [
    ('Which Drake songs will I hear?', 'A rotating pool of 69 tracks, from “God’s Plan” and “Hotline Bling” to album cuts and features. The rotation mixes eras so no round feels predictable.'),
    ('Is it really free?', 'Completely. It runs in the browser with no signup and no download, and there is no daily limit on how many rounds you play.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'eminem', 'name': 'Eminem', 'count': 66,
  'title': 'Eminem Song Guesser — Guess the Eminem Song in 0.1 Seconds',
  'desc': 'Name the Eminem song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Eminem song guessing game with 66 tracks — no signup, no download.',
  'h1': 'Eminem Song Guesser',
  'hero': 'Name the Eminem track from a tenth of a second — the beat and the breath give him away.',
  'vgdesc': 'A free browser song guessing game on 66 Eminem tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Eminem song game',
  'h2': 'About Eminem Song Guesser',
  'what_h3': 'What Is Eminem Song Guesser?',
  'p1': 'Eminem Song Guesser is a free audio game built on a catalog defined by cadence — the tense piano of “Lose Yourself”, the rainy-night gloom of “Stan”, and the cartoon bounce of “Without Me”. A 0.1-second clip opens each round, and you name the track before the longer reveals do it for you. A song guessing game in the Heardle style for Eminem fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the sharper the guess.',
  'how_h3': 'How to Play Eminem Song Guesser',
  'intro': 'Hear the sliver, trust the rhythm, and reveal more only when you must.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of an Eminem track is the first clue — a snare, a keyboard stab, or a breath before the verse.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His flow and the beat style usually place the era.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 66 Eminem tracks, from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Marshall Mathers song from a single snare hit, and listeners who want to learn the difference between his horrorcore, stadium and introspective eras. Easy is for casual fans; Impossible is for the people who know every bar.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Eminem Song Guesser FAQ',
  'faq': [
    ('How many Eminem songs are in the pool?', 'Sixty-six tracks, from the radio staples such as “Lose Yourself” and “Stan” to album cuts. The rotation mixes eras so no round is predictable.'),
    ('What happens if I keep guessing wrong?', 'Nothing locks. Each miss or skip opens the clip one step further — 0.5s, 2s, 8s, then 15s — so more of the track arrives only when you ask.'),
    ('Can I change artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'kanye-west', 'name': 'Kanye West', 'count': 61,
  'title': 'Kanye West Song Guesser — Guess the Kanye West Song in 0.1 Seconds',
  'desc': 'Name the Kanye West song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Kanye West song guessing game with 61 tracks — no signup, no download.',
  'h1': 'Kanye West Song Guesser',
  'hero': 'Guess the Kanye song from a tenth of a second — the sample and the drums usually tell.',
  'vgdesc': 'A free browser song guessing game on 61 Kanye West tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Kanye song game',
  'h2': 'About Kanye West Song Guesser',
  'what_h3': 'What Is Kanye West Song Guesser?',
  'p1': 'Kanye West Song Guesser is a free audio game built on a catalog that flips between the chipmunk-soul sample of “Gold Digger”, the Daft Punk stomp of “Stronger” and the synth-soaked ache of “Heartless”. The round opens on the shortest clip and only widens once you’ve had your guess. It’s the Heardle-style song guessing game for Kanye fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the cleaner the round.',
  'how_h3': 'How to Play Kanye West Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you are stuck.',
  'steps': [
    ('▶', 'Start at a tenth of a second', 'A 0.1-second slice of a Kanye track is the first clue — a sped-up sample, a drum fill, or a synth wash.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. The production tells you which era you are in.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Keep playing', 'Unlimited rounds across 61 Kanye tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Kanye song from its opening sample or a single drum hit, and listeners who want to hear how his sound kept reinventing itself. Easy welcomes newcomers; Impossible is for the people who know the deep cuts and the leaks.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Kanye West Song Guesser FAQ',
  'faq': [
    ('Which Kanye songs will I hear?', 'A rotating pool of 61 tracks, from “Stronger” and “Gold Digger” to album cuts. The rotation spans his whole career, so no round feels predictable.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'justin-bieber', 'name': 'Justin Bieber', 'count': 69,
  'title': 'Justin Bieber Song Guesser — Guess the Justin Bieber Song in 0.1 Seconds',
  'desc': 'Name the Justin Bieber song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Justin Bieber song guessing game with 69 tracks — no signup, no download.',
  'h1': 'Justin Bieber Song Guesser',
  'hero': 'Name the Justin Bieber track from a tenth of a second — the falsetto and the groove do the telling.',
  'vgdesc': 'A free browser song guessing game on 69 Justin Bieber tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Justin Bieber song game',
  'h2': 'About Justin Bieber Song Guesser',
  'what_h3': 'What Is Justin Bieber Song Guesser?',
  'p1': 'Justin Bieber Song Guesser is a free audio game built on a career that moved from the pop-soul of “Baby” to the trop-house ease of “Sorry” and the soft bounce of “Peaches”. You hear the opening sliver, then type the title before the longer reveals step in. A Heardle-style song guessing game built for Beliebers — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Justin Bieber Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you need it.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Bieber track is the first clue — a guitar strum, a synth pad, or that falsetto.'),
    ('⌕', 'Type your guess', 'Type part of the title and pick from the suggestions. His pop, R&B and dance eras each sound a little different.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play every round', 'Unlimited rounds across 69 Justin Bieber tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Bieber song from a single synth swell, and listeners who want to trace how his sound grew from teen pop to R&B and dance. Easy is a warm-up; Impossible is for the people who know every deep cut.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Justin Bieber Song Guesser FAQ',
  'faq': [
    ('How many Justin Bieber songs are in the pool?', 'Sixty-nine tracks, from “Baby” and “Sorry” to “Peaches” and album cuts. The rotation mixes his eras so no round feels predictable.'),
    ('Do I need an account?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'linkin-park', 'name': 'Linkin Park', 'count': 67,
  'title': 'Linkin Park Song Guesser — Guess the Linkin Park Song in 0.1 Seconds',
  'desc': 'Name the Linkin Park song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Linkin Park song guessing game with 67 tracks — no signup, no download.',
  'h1': 'Linkin Park Song Guesser',
  'hero': 'Guess the Linkin Park song from a tenth of a second — the riff and the electronics give it away.',
  'vgdesc': 'A free browser song guessing game on 67 Linkin Park tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Linkin Park song game',
  'h2': 'About Linkin Park Song Guesser',
  'what_h3': 'What Is Linkin Park Song Guesser?',
  'p1': 'Linkin Park Song Guesser is a free audio game built on a catalog that fuses rap and rock — the atmospheric keys of “In the End”, the crushing riff of “One Step Closer”, and the slow-burn build of “Numb”. A sliver of audio plays, and you have to name the song before more of it spills out. It’s Heardle-style song guessing aimed at Linkin Park fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Linkin Park Song Guesser',
  'intro': 'Hear the sliver, trust the riff, and reveal more only when you must.',
  'steps': [
    ('▶', 'Hear 0.1s first', 'A tenth of a second of a Linkin Park track is the whole first clue — a synth line, a guitar chug, or a drum fill.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. The blend of electronics and guitar tells you the era.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 67 Linkin Park tracks, from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Linkin Park song from a single keyboard stab, and listeners who want to learn how their nu-metal, electronic and later eras differ. Easy welcomes newcomers; Impossible is for the people who know every bridge and breakdown.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Linkin Park Song Guesser FAQ',
  'faq': [
    ('How many Linkin Park songs are in the rotation?', 'Sixty-seven tracks, from “In the End” and “Numb” to deeper album cuts. The pool rotates so a round can land on a hit or a deep cut.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other bands too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'lady-gaga', 'name': 'Lady Gaga', 'count': 69,
  'title': 'Lady Gaga Song Guesser — Guess the Lady Gaga Song in 0.1 Seconds',
  'desc': 'Name the Lady Gaga song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Lady Gaga song guessing game with 69 tracks — no signup, no download.',
  'h1': 'Lady Gaga Song Guesser',
  'hero': 'Name the Lady Gaga track from a tenth of a second — the synth and the drama do the telling.',
  'vgdesc': 'A free browser song guessing game on 69 Lady Gaga tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Lady Gaga song game',
  'h2': 'About Lady Gaga Song Guesser',
  'what_h3': 'What Is Lady Gaga Song Guesser?',
  'p1': 'Lady Gaga Song Guesser is a free audio game built on a catalog that spans the electro stomp of “Poker Face”, the gothic pop of “Bad Romance” and the stripped-down duet “Shallow”. Every round starts on a sliver of audio and waits for you to call the track before it opens up. The Heardle-style song guessing game for Little Monsters — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Lady Gaga Song Guesser',
  'intro': 'Hear the sliver, make a guess, and only reveal more when you are stuck.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a Gaga track is the first clue — a synth stab, a piano chord, or the start of a vocal run.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Her dance-pop, jazz and rock eras each have a distinct sound.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Keep playing', 'Unlimited rounds across 69 Lady Gaga tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Gaga song from a single synth hit, and listeners who want to hear how her pop, jazz and ballads eras differ. Easy is a warm-up; Impossible is for the people who know every deep cut and demo.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Lady Gaga Song Guesser FAQ',
  'faq': [
    ('Which Lady Gaga songs will I hear?', 'A rotating pool of 69 tracks, from “Poker Face” and “Bad Romance” to “Shallow” and album cuts. The rotation spans her whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'bruno-mars', 'name': 'Bruno Mars', 'count': 62,
  'title': 'Bruno Mars Song Guesser — Guess the Bruno Mars Song in 0.1 Seconds',
  'desc': 'Name the Bruno Mars song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Bruno Mars song guessing game with 62 tracks — no signup, no download.',
  'h1': 'Bruno Mars Song Guesser',
  'hero': 'Guess the Bruno Mars song from a tenth of a second — the groove and the falsetto give him away.',
  'vgdesc': 'A free browser song guessing game on 62 Bruno Mars tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Bruno Mars song game',
  'h2': 'About Bruno Mars Song Guesser',
  'what_h3': 'What Is Bruno Mars Song Guesser?',
  'p1': 'Bruno Mars Song Guesser is a free audio game built on a catalog that leans on live-band funk — the horn blast of “Uptown Funk”, the doo-wop sweetness of “Just the Way You Are” and the silky bounce of “That’s What I Like”. The clip starts at 0.1 seconds and stays there until you ask for more. It’s a Heardle-style song guessing game for Bruno Mars fans — but the opening is a tenth of a second, not one second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the cleaner the round.',
  'how_h3': 'How to Play Bruno Mars Song Guesser',
  'intro': 'Hear the sliver, trust the groove, and reveal more only when you must.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Bruno track is the first clue — a horn stab, a snare, or the top of a falsetto line.'),
    ('⌕', 'Type your guess', 'Type part of the title and pick from the suggestions. His pop, funk and R&B modes each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play every round', 'Unlimited rounds across 62 Bruno Mars tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Bruno Mars song from a single horn hit, and listeners who want to learn how his doo-wop, funk and R&B modes differ. Easy welcomes newcomers; Impossible is for the people who know every ad-lib.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Bruno Mars Song Guesser FAQ',
  'faq': [
    ('How many Bruno Mars songs are in the pool?', 'Sixty-two tracks, from “Uptown Funk” and “Just the Way You Are” to “That’s What I Like” and album cuts. The rotation mixes his eras.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily limit.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'adele', 'name': 'Adele', 'count': 50,
  'title': 'Adele Song Guesser — Guess the Adele Song in 0.1 Seconds',
  'desc': 'Name the Adele song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Adele song guessing game with 50 tracks — no signup, no download.',
  'h1': 'Adele Song Guesser',
  'hero': 'Name the Adele track from a tenth of a second — the piano and that voice do the telling.',
  'vgdesc': 'A free browser song guessing game on 50 Adele tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Adele song game',
  'h2': 'About Adele Song Guesser',
  'what_h3': 'What Is Adele Song Guesser?',
  'p1': 'Adele Song Guesser is a free audio game built on a catalog of ballads and torch songs — the stomp of “Rolling in the Deep”, the piano hush of “Someone Like You” and the soaring title “Hello”. You get a tenth of a second, and you name it before the reveal starts doing your job. A song guessing game in the Heardle style for Adele fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the sharper the round.',
  'how_h3': 'How to Play Adele Song Guesser',
  'intro': 'Hear the sliver, trust the piano, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of an Adele track is the first clue — a piano chord, a snare roll, or the intake before the vocal.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. Her ballads each open a little differently, so the piano pattern is a strong tell.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 50 Adele tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place an Adele song from a single piano chord, and listeners who want to learn the difference between her “19”, “21”, “25” and “30” eras by ear. Easy is a warm-up; Impossible is for the people who know every bridge.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Adele Song Guesser FAQ',
  'faq': [
    ('How many Adele songs are in the rotation?', 'Fifty tracks, from “Rolling in the Deep” and “Hello” to “Easy on Me” and album cuts. The pool rotates so a round can land on a hit or a deep cut.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'ariana-grande', 'name': 'Ariana Grande', 'count': 64,
  'title': 'Ariana Grande Song Guesser — Guess the Ariana Grande Song in 0.1 Seconds',
  'desc': 'Name the Ariana Grande song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Ariana Grande song guessing game with 64 tracks — no signup, no download.',
  'h1': 'Ariana Grande Song Guesser',
  'hero': 'Guess the Ariana Grande song from a tenth of a second — the whistle tone and the beat give her away.',
  'vgdesc': 'A free browser song guessing game on 64 Ariana Grande tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Ariana Grande song game',
  'h2': 'About Ariana Grande Song Guesser',
  'what_h3': 'What Is Ariana Grande Song Guesser?',
  'p1': 'Ariana Grande Song Guesser is a free audio game built on a catalog of glossy pop-R&B — the trap-lite bounce of “thank u, next”, the shimmer of “7 rings” and the airy “No Tears Left to Cry”. You hear the opening sliver, then type the title before the longer reveals step in. It’s the Heardle-style song guessing game for Ariana fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the cleaner the round.',
  'how_h3': 'How to Play Ariana Grande Song Guesser',
  'intro': 'Hear the sliver, trust the run, and reveal more only when you must.',
  'steps': [
    ('▶', 'Hear 0.1s first', 'A tenth of a second of an Ariana track is the whole first clue — a whistle tone, a synth pad, or a hi-hat.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Her vocal runs and the production sheen usually place the era.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Keep playing', 'Unlimited rounds across 64 Ariana Grande tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name an Ariana song from a single whistle note, and listeners who want to trace how her sound moved from Broadway-influenced pop to trap-lite R&B. Easy welcomes newcomers; Impossible is for the people who know every ad-lib.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Ariana Grande Song Guesser FAQ',
  'faq': [
    ('Which Ariana Grande songs will I hear?', 'A rotating pool of 64 tracks, from “thank u, next” and “7 rings” to album cuts. The rotation spans her whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'billie-eilish', 'name': 'Billie Eilish', 'count': 58,
  'title': 'Billie Eilish Song Guesser — Guess the Billie Eilish Song in 0.1 Seconds',
  'desc': 'Name the Billie Eilish song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Billie Eilish song guessing game with 58 tracks — no signup, no download.',
  'h1': 'Billie Eilish Song Guesser',
  'hero': 'Name the Billie Eilish track from a tenth of a second — the bass and the whisper give her away.',
  'vgdesc': 'A free browser song guessing game on 58 Billie Eilish tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Billie Eilish song game',
  'h2': 'About Billie Eilish Song Guesser',
  'what_h3': 'What Is Billie Eilish Song Guesser?',
  'p1': 'Billie Eilish Song Guesser is a free audio game built on a catalog of hushed, bass-heavy pop — the slinky groove of “bad guy”, the dreamy “Ocean Eyes” and the blown-out chorus of “Happier Than Ever”. The round opens on the shortest clip and only widens once you’ve had your guess. A Heardle-style song guessing game built for Billie Eilish fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Billie Eilish Song Guesser',
  'intro': 'Hear the sliver, trust the bass, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Billie track is the first clue — a bass thump, a whisper, or a synth swell.'),
    ('⌕', 'Type your guess', 'Type part of the title and pick from the suggestions. Her hushed verses and bigger choruses each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 58 Billie Eilish tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Billie Eilish song from a single bass note, and listeners who want to hear how her whisper-pop grew into arena-sized choruses. Easy is a warm-up; Impossible is for the people who know every interlude.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Billie Eilish Song Guesser FAQ',
  'faq': [
    ('How many Billie Eilish songs are in the pool?', 'Fifty-eight tracks, from “bad guy” and “Ocean Eyes” to “Happier Than Ever” and album cuts. The rotation mixes her eras.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'ed-sheeran', 'name': 'Ed Sheeran', 'count': 70,
  'title': 'Ed Sheeran Song Guesser — Guess the Ed Sheeran Song in 0.1 Seconds',
  'desc': 'Name the Ed Sheeran song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Ed Sheeran song guessing game with 70 tracks — no signup, no download.',
  'h1': 'Ed Sheeran Song Guesser',
  'hero': 'Guess the Ed Sheeran song from a tenth of a second — the guitar and the loop do the telling.',
  'vgdesc': 'A free browser song guessing game on 70 Ed Sheeran tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Ed Sheeran song game',
  'h2': 'About Ed Sheeran Song Guesser',
  'what_h3': 'What Is Ed Sheeran Song Guesser?',
  'p1': 'Ed Sheeran Song Guesser is a free audio game built on a catalog of loop-pedal pop — the acoustic warmth of “Thinking Out Loud”, the percussive hook of “Shape of You” and the big ballad “Perfect”. Every round starts on a sliver of audio and waits for you to call the track before it opens up. It’s Heardle-style song guessing aimed at Ed Sheeran fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Ed Sheeran Song Guesser',
  'intro': 'Hear the sliver, trust the loop, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of an Ed track is the first clue — a guitar strum, a loop, or the start of a melody.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His acoustic and pop modes each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 70 Ed Sheeran tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name an Ed Sheeran song from a single guitar strum, and listeners who want to hear how his loop-pedal folk grew into stadium pop. Easy welcomes newcomers; Impossible is for the people who know every deep cut.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Ed Sheeran Song Guesser FAQ',
  'faq': [
    ('How many Ed Sheeran songs are in the rotation?', 'Seventy tracks, from “Shape of You” and “Thinking Out Loud” to “Bad Habits” and album cuts. The pool rotates so a round can land on a hit or a deep cut.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'coldplay', 'name': 'Coldplay', 'count': 68,
  'title': 'Coldplay Song Guesser — Guess the Coldplay Song in 0.1 Seconds',
  'desc': 'Name the Coldplay song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Coldplay song guessing game with 68 tracks — no signup, no download.',
  'h1': 'Coldplay Song Guesser',
  'hero': 'Name the Coldplay track from a tenth of a second — the piano and the reverb give them away.',
  'vgdesc': 'A free browser song guessing game on 68 Coldplay tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Coldplay song game',
  'h2': 'About Coldplay Song Guesser',
  'what_h3': 'What Is Coldplay Song Guesser?',
  'p1': 'Coldplay Song Guesser is a free audio game built on a catalog of sweeping, reverb-washed rock — the strum of “Yellow”, the string-soaked “Viva la Vida” and the piano build of “Fix You”. A sliver of audio plays, and you have to name the song before more of it spills out. The Heardle-style song guessing game for Coldplay fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Coldplay Song Guesser',
  'intro': 'Hear the sliver, trust the atmosphere, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Coldplay track is the first clue — a piano note, a guitar wash, or a synth pad.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Their piano-led and electronic eras each have a distinct sound.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 68 Coldplay tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Coldplay song from a single piano chord, and listeners who want to hear how their quiet rock grew into stadium-sized pop. Easy is a warm-up; Impossible is for the people who know every B-side.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Coldplay Song Guesser FAQ',
  'faq': [
    ('Which Coldplay songs will I hear?', 'A rotating pool of 68 tracks, from “Yellow” and “Viva la Vida” to “Fix You” and album cuts. The rotation spans their whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'bts', 'name': 'BTS', 'count': 75,
  'title': 'BTS Song Guesser — Guess the BTS Song in 0.1 Seconds',
  'desc': 'Name the BTS song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free BTS song guessing game with 75 tracks — no signup, no download.',
  'h1': 'BTS Song Guesser',
  'hero': 'Guess the BTS song from a tenth of a second — the beat drop and the chant give them away.',
  'vgdesc': 'A free browser song guessing game on 75 BTS tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this BTS song game',
  'h2': 'About BTS Song Guesser',
  'what_h3': 'What Is BTS Song Guesser?',
  'p1': 'BTS Song Guesser is a free audio game built on a catalog that blends K-pop, hip-hop and EDM — the disco-pop sparkle of “Dynamite”, the butter-smooth “Butter” and the layered “DNA”. You get a tenth of a second, and you name it before the reveal starts doing your job. It’s a Heardle-style song guessing game for ARMY — but the opening is a tenth of a second, not one second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you solve it, the cleaner the round.',
  'how_h3': 'How to Play BTS Song Guesser',
  'intro': 'Hear the sliver, trust the beat, and reveal more only when you must.',
  'steps': [
    ('▶', 'Hear 0.1s first', 'A tenth of a second of a BTS track is the whole first clue — a synth stab, a chant, or the start of a drop.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Their Korean and English singles each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Keep playing', 'Unlimited rounds across 75 BTS tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a BTS song from a single beat drop, and listeners who want to learn how their hip-hop roots grew into global pop. Easy welcomes newcomers; Impossible is for the ARMY who know every B-side and solo track.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'BTS Song Guesser FAQ',
  'faq': [
    ('How many BTS songs are in the pool?', 'Seventy-five tracks, from “Dynamite” and “Butter” to “DNA” and album cuts. The rotation spans their Korean and English releases.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'blackpink', 'name': 'BLACKPINK', 'count': 37,
  'title': 'BLACKPINK Song Guesser — Guess the BLACKPINK Song in 0.1 Seconds',
  'desc': 'Name the BLACKPINK song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free BLACKPINK song guessing game with 37 tracks — no signup, no download.',
  'h1': 'BLACKPINK Song Guesser',
  'hero': 'Name the BLACKPINK track from a tenth of a second — the bass and the hook give them away.',
  'vgdesc': 'A free browser song guessing game on 37 BLACKPINK tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this BLACKPINK song game',
  'h2': 'About BLACKPINK Song Guesser',
  'what_h3': 'What Is BLACKPINK Song Guesser?',
  'p1': 'BLACKPINK Song Guesser is a free audio game built on a catalog of fierce, bass-heavy K-pop — the marching stomp of “DDU-DU DDU-DU”, the chanted drop of “How You Like That” and the anthemic “Kill This Love”. The clip starts at 0.1 seconds and stays there until you ask for more. A song guessing game in the Heardle style for BLINKs — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play BLACKPINK Song Guesser',
  'intro': 'Hear the sliver, trust the drop, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a BLACKPINK track is the first clue — a bass thump, a synth, or a chant.'),
    ('⌕', 'Type your guess', 'Type part of the title and pick from the suggestions. Each single has its own signature opening.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 37 BLACKPINK tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a BLACKPINK song from a single bass drop, and listeners who want to learn how their sound sharpened across every comeback. Easy is a warm-up; Impossible is for the BLINKs who know every b-side.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'BLACKPINK Song Guesser FAQ',
  'faq': [
    ('How many BLACKPINK songs are in the rotation?', 'Thirty-seven tracks, from “DDU-DU DDU-DU” and “How You Like That” to “Pink Venom” and b-sides. The pool rotates across their comebacks.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'gdragon', 'name': 'G-DRAGON', 'count': 50,
  'title': 'G-DRAGON Song Guesser — Guess the G-DRAGON Song in 0.1 Seconds',
  'desc': 'Name the G-DRAGON song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free G-DRAGON song guessing game with 50 tracks — no signup, no download.',
  'h1': 'G-DRAGON Song Guesser',
  'hero': 'Guess the G-DRAGON song from a tenth of a second — the beat and the swagger give him away.',
  'vgdesc': 'A free browser song guessing game on 50 G-DRAGON tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this G-DRAGON song game',
  'h2': 'About G-DRAGON Song Guesser',
  'what_h3': 'What Is G-DRAGON Song Guesser?',
  'p1': 'G-DRAGON Song Guesser is a free audio game built on a catalog of shape-shifting K-hip-hop — the neon burst of “Crayon”, the self-lacerating “Crooked” and the electro “Heartbreaker”. The round opens on the shortest clip and only widens once you’ve had your guess. It’s the Heardle-style song guessing game for G-DRAGON fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play G-DRAGON Song Guesser',
  'intro': 'Hear the sliver, trust the beat, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a G-DRAGON track is the first clue — a synth line, a drum, or an ad-lib.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His solo and BIGBANG-era sounds each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 50 G-DRAGON tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a G-DRAGON song from a single synth hit, and listeners who want to trace how his sound kept mutating across albums. Easy welcomes newcomers; Impossible is for the people who know every solo and feature.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'G-DRAGON Song Guesser FAQ',
  'faq': [
    ('Which G-DRAGON songs will I hear?', 'A rotating pool of 50 tracks, from “Crayon” and “Crooked” to solo and group-era cuts. The rotation spans his whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'david-guetta', 'name': 'David Guetta', 'count': 64,
  'title': 'David Guetta Song Guesser — Guess the David Guetta Song in 0.1 Seconds',
  'desc': 'Name the David Guetta song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free David Guetta song guessing game with 64 tracks — no signup, no download.',
  'h1': 'David Guetta Song Guesser',
  'hero': 'Name the David Guetta track from a tenth of a second — the drop and the vocal give him away.',
  'vgdesc': 'A free browser song guessing game on 64 David Guetta tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this David Guetta song game',
  'h2': 'About David Guetta Song Guesser',
  'what_h3': 'What Is David Guetta Song Guesser?',
  'p1': 'David Guetta Song Guesser is a free audio game built on a catalog of festival-sized EDM — the piano lift of “When Love Takes Over”, the towering “Titanium” and the singalong “Memories”. You hear the opening sliver, then type the title before the longer reveals step in. A Heardle-style song guessing game built for David Guetta fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play David Guetta Song Guesser',
  'intro': 'Hear the sliver, trust the drop, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Guetta track is the first clue — a piano chord, a synth stab, or the start of a build.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. His vocal-house and big-room eras each have a distinct sound.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 64 David Guetta tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a David Guetta song from a single synth stab, and listeners who want to hear how his club sound evolved from house to pop-EDM. Easy is a warm-up; Impossible is for the people who know every remix.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'David Guetta Song Guesser FAQ',
  'faq': [
    ('How many David Guetta songs are in the pool?', 'Sixty-four tracks, from “Titanium” and “When Love Takes Over” to “Memories” and more. The rotation spans his collabs and solo releases.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'pitbull', 'name': 'Pitbull', 'count': 68,
  'title': 'Pitbull Song Guesser — Guess the Pitbull Song in 0.1 Seconds',
  'desc': 'Name the Pitbull song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Pitbull song guessing game with 68 tracks — no signup, no download.',
  'h1': 'Pitbull Song Guesser',
  'hero': 'Guess the Pitbull song from a tenth of a second — the horn and the shout give him away.',
  'vgdesc': 'A free browser song guessing game on 68 Pitbull tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Pitbull song game',
  'h2': 'About Pitbull Song Guesser',
  'what_h3': 'What Is Pitbull Song Guesser?',
  'p1': 'Pitbull Song Guesser is a free audio game built on a catalog of party-starting Latin-pop — the stomp of “Timber”, the shoulder-shimmy of “Fireball” and the global smash “Give Me Everything”. A sliver of audio plays, and you have to name the song before more of it spills out. It’s Heardle-style song guessing aimed at Pitbull fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Pitbull Song Guesser',
  'intro': 'Hear the sliver, trust the beat, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a Pitbull track is the first clue — a horn blast, a four-on-the-floor kick, or a shout.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His dance, Latin and hip-hop crossovers each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 68 Pitbull tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Pitbull song from a single horn hit, and listeners who want to hear how his Miami club sound crossed into pop and reggaeton. Easy welcomes newcomers; Impossible is for the people who know every feature.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Pitbull Song Guesser FAQ',
  'faq': [
    ('How many Pitbull songs are in the rotation?', 'Sixty-eight tracks, from “Timber” and “Give Me Everything” to “Fireball” and album cuts. The pool rotates across his hits and collabs.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'kendrick-lamar', 'name': 'Kendrick Lamar', 'count': 62,
  'title': 'Kendrick Lamar Song Guesser — Guess the Kendrick Lamar Song in 0.1 Seconds',
  'desc': 'Name the Kendrick Lamar song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Kendrick Lamar song guessing game with 62 tracks — no signup, no download.',
  'h1': 'Kendrick Lamar Song Guesser',
  'hero': 'Name the Kendrick track from a tenth of a second — the beat switch and the cadence give him away.',
  'vgdesc': 'A free browser song guessing game on 62 Kendrick Lamar tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Kendrick Lamar song game',
  'h2': 'About Kendrick Lamar Song Guesser',
  'what_h3': 'What Is Kendrick Lamar Song Guesser?',
  'p1': 'Kendrick Lamar Song Guesser is a free audio game built on a catalog of dense, jazz-inflected hip-hop — the jittery “HUMBLE.”, the righteous “Alright” and the summer-echo “Not Like Us”. Every round starts on a sliver of audio and waits for you to call the track before it opens up. The Heardle-style song guessing game for Kendrick fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Kendrick Lamar Song Guesser',
  'intro': 'Hear the sliver, trust the rhythm, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Kendrick track is the first clue — a drum fill, a vocal bend, or a beat switch.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. His albums each have their own sonic stamp.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 62 Kendrick Lamar tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Kendrick song from a single drum fill, and listeners who want to learn how his sound moved from Compton narratives to jazz and funk. Easy is a warm-up; Impossible is for the people who know every bar.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Kendrick Lamar Song Guesser FAQ',
  'faq': [
    ('Which Kendrick Lamar songs will I hear?', 'A rotating pool of 62 tracks, from “HUMBLE.” and “Alright” to “Not Like Us” and album cuts. The rotation spans his whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'olivia-rodrigo', 'name': 'Olivia Rodrigo', 'count': 50,
  'title': 'Olivia Rodrigo Song Guesser — Guess the Olivia Rodrigo Song in 0.1 Seconds',
  'desc': 'Name the Olivia Rodrigo song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Olivia Rodrigo song guessing game with 50 tracks — no signup, no download.',
  'h1': 'Olivia Rodrigo Song Guesser',
  'hero': 'Guess the Olivia Rodrigo song from a tenth of a second — the piano and the snarl give her away.',
  'vgdesc': 'A free browser song guessing game on 50 Olivia Rodrigo tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Olivia Rodrigo song game',
  'h2': 'About Olivia Rodrigo Song Guesser',
  'what_h3': 'What Is Olivia Rodrigo Song Guesser?',
  'p1': 'Olivia Rodrigo Song Guesser is a free audio game built on a catalog of sharp, diary-style pop-rock — the breathy “drivers license”, the pop-punk sneer of “good 4 u” and the brooding “vampire”. The clip starts at 0.1 seconds and stays there until you ask for more. It’s a Heardle-style song guessing game for Olivia Rodrigo fans — but the opening is a tenth of a second, not one second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Olivia Rodrigo Song Guesser',
  'intro': 'Hear the sliver, trust the hook, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of an Olivia track is the first clue — a piano chord, a guitar chug, or a breath.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. Her ballads and pop-punk cuts each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 50 Olivia Rodrigo tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name an Olivia Rodrigo song from a single piano chord, and listeners who want to hear how her heartbreak pop grew into pop-punk and rock. Easy welcomes newcomers; Impossible is for the people who know every bridge.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Olivia Rodrigo Song Guesser FAQ',
  'faq': [
    ('How many Olivia Rodrigo songs are in the pool?', 'Fifty tracks, from “drivers license” and “good 4 u” to “vampire” and album cuts. The rotation spans her two albums.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'lana-del-rey', 'name': 'Lana Del Rey', 'count': 52,
  'title': 'Lana Del Rey Song Guesser — Guess the Lana Del Rey Song in 0.1 Seconds',
  'desc': 'Name the Lana Del Rey song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Lana Del Rey song guessing game with 52 tracks — no signup, no download.',
  'h1': 'Lana Del Rey Song Guesser',
  'hero': 'Name the Lana Del Rey track from a tenth of a second — the strings and the sigh give her away.',
  'vgdesc': 'A free browser song guessing game on 52 Lana Del Rey tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Lana Del Rey song game',
  'h2': 'About Lana Del Rey Song Guesser',
  'what_h3': 'What Is Lana Del Rey Song Guesser?',
  'p1': 'Lana Del Rey Song Guesser is a free audio game built on a catalog of cinematic, nostalgia-soaked pop — the dreamy “Video Games”, the swooning “Summertime Sadness” and the Hollywood ache of “Young and Beautiful”. You get a tenth of a second, and you name it before the reveal starts doing your job. A song guessing game in the Heardle style for Lana Del Rey fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Lana Del Rey Song Guesser',
  'intro': 'Hear the sliver, trust the mood, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Lana track is the first clue — a string swell, a piano note, or that sigh.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Her lush arrangements and sparse ballads each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 52 Lana Del Rey tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Lana Del Rey song from a single string swell, and listeners who want to hear how her sad-girl pop matured into folk and Americana. Easy is a warm-up; Impossible is for the people who know every unreleased cut.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Lana Del Rey Song Guesser FAQ',
  'faq': [
    ('How many Lana Del Rey songs are in the rotation?', 'Fifty-two tracks, from “Video Games” and “Summertime Sadness” to “Young and Beautiful” and album cuts. The pool rotates across her albums.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'maroon-5', 'name': 'Maroon 5', 'count': 72,
  'title': 'Maroon 5 Song Guesser — Guess the Maroon 5 Song in 0.1 Seconds',
  'desc': 'Name the Maroon 5 song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Maroon 5 song guessing game with 72 tracks — no signup, no download.',
  'h1': 'Maroon 5 Song Guesser',
  'hero': 'Guess the Maroon 5 song from a tenth of a second — the falsetto and the groove give them away.',
  'vgdesc': 'A free browser song guessing game on 72 Maroon 5 tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Maroon 5 song game',
  'h2': 'About Maroon 5 Song Guesser',
  'what_h3': 'What Is Maroon 5 Song Guesser?',
  'p1': 'Maroon 5 Song Guesser is a free audio game built on a catalog of polished pop-rock — the strut of “Moves Like Jagger”, the sweet “Sugar” and the falsetto-led “She Will Be Loved”. You hear the opening sliver, then type the title before the longer reveals step in. It’s the Heardle-style song guessing game for Maroon 5 fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Maroon 5 Song Guesser',
  'intro': 'Hear the sliver, trust the groove, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a Maroon 5 track is the first clue — a funky guitar, a synth, or that falsetto.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. Their rock, funk and pop eras each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 72 Maroon 5 tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Maroon 5 song from a single funky guitar hit, and listeners who want to hear how their rock roots melted into radio pop. Easy welcomes newcomers; Impossible is for the people who know every deep cut.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Maroon 5 Song Guesser FAQ',
  'faq': [
    ('Which Maroon 5 songs will I hear?', 'A rotating pool of 72 tracks, from “Moves Like Jagger” and “Sugar” to “Payphone” and album cuts. The rotation spans their whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'shakira', 'name': 'Shakira', 'count': 67,
  'title': 'Shakira Song Guesser — Guess the Shakira Song in 0.1 Seconds',
  'desc': 'Name the Shakira song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Shakira song guessing game with 67 tracks — no signup, no download.',
  'h1': 'Shakira Song Guesser',
  'hero': 'Name the Shakira track from a tenth of a second — the rhythm and the voice give her away.',
  'vgdesc': 'A free browser song guessing game on 67 Shakira tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Shakira song game',
  'h2': 'About Shakira Song Guesser',
  'what_h3': 'What Is Shakira Song Guesser?',
  'p1': 'Shakira Song Guesser is a free audio game built on a catalog that swings between Latin rock and global pop — the trumpet hook of “Hips Don’t Lie”, the Andean flute of “Whenever, Wherever” and the World Cup anthem “Waka Waka”. The round opens on the shortest clip and only widens once you’ve had your guess. A Heardle-style song guessing game built for Shakira fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Shakira Song Guesser',
  'intro': 'Hear the sliver, trust the rhythm, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Shakira track is the first clue — a trumpet, a flute, or the start of that voice.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Her Spanish and English singles each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 67 Shakira tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Shakira song from a single trumpet hit, and listeners who want to hear how her Latin rock and global pop eras differ. Easy is a warm-up; Impossible is for the people who know every Spanish deep cut.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Shakira Song Guesser FAQ',
  'faq': [
    ('How many Shakira songs are in the pool?', 'Sixty-seven tracks, from “Hips Don’t Lie” and “Whenever, Wherever” to “Waka Waka” and album cuts. The rotation spans her Spanish and English catalogs.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'travis-scott', 'name': 'Travis Scott', 'count': 77,
  'title': 'Travis Scott Song Guesser — Guess the Travis Scott Song in 0.1 Seconds',
  'desc': 'Name the Travis Scott song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Travis Scott song guessing game with 77 tracks — no signup, no download.',
  'h1': 'Travis Scott Song Guesser',
  'hero': 'Guess the Travis Scott song from a tenth of a second — the bass and the ad-lib give him away.',
  'vgdesc': 'A free browser song guessing game on 77 Travis Scott tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Travis Scott song game',
  'h2': 'About Travis Scott Song Guesser',
  'what_h3': 'What Is Travis Scott Song Guesser?',
  'p1': 'Travis Scott Song Guesser is a free audio game built on a catalog of woozy, bass-heavy rap — the shape-shifting “SICKO MODE”, the hazy “Goosebumps” and the rattling “Antidote”. Every round starts on a sliver of audio and waits for you to call the track before it opens up. It’s Heardle-style song guessing aimed at Travis Scott fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Travis Scott Song Guesser',
  'intro': 'Hear the sliver, trust the bass, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a Travis track is the first clue — an 808, a synth drone, or a pitched-down vocal.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His mixtape and album eras each have their own texture.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 77 Travis Scott tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Travis Scott song from a single 808, and listeners who want to hear how his psychedelic trap sound evolved. Easy welcomes newcomers; Impossible is for the people who know every feature and leak.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Travis Scott Song Guesser FAQ',
  'faq': [
    ('How many Travis Scott songs are in the rotation?', 'Seventy-seven tracks, from “SICKO MODE” and “Goosebumps” to “Antidote” and album cuts. The pool rotates across his mixtapes and albums.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'sabrina-carpenter', 'name': 'Sabrina Carpenter', 'count': 77,
  'title': 'Sabrina Carpenter Song Guesser — Guess the Sabrina Carpenter Song in 0.1 Seconds',
  'desc': 'Name the Sabrina Carpenter song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Sabrina Carpenter song guessing game with 77 tracks — no signup, no download.',
  'h1': 'Sabrina Carpenter Song Guesser',
  'hero': 'Name the Sabrina Carpenter track from a tenth of a second — the bassline and the wink give her away.',
  'vgdesc': 'A free browser song guessing game on 77 Sabrina Carpenter tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Sabrina Carpenter song game',
  'h2': 'About Sabrina Carpenter Song Guesser',
  'what_h3': 'What Is Sabrina Carpenter Song Guesser?',
  'p1': 'Sabrina Carpenter Song Guesser is a free audio game built on a catalog of sharp, wink-and-a-smile pop — the frothy “Espresso”, the country-kissed “Please Please Please” and the slinky “Taste”. A sliver of audio plays, and you have to name the song before more of it spills out. The Heardle-style song guessing game for Sabrina Carpenter fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Sabrina Carpenter Song Guesser',
  'intro': 'Hear the sliver, trust the hook, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Sabrina track is the first clue — a disco bassline, a guitar, or a playful vocal.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Her tongue-in-cheek pop and ballads each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 77 Sabrina Carpenter tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Sabrina Carpenter song from a single bassline, and listeners who want to hear how her bubbly pop sharpened into something wittier. Easy is a warm-up; Impossible is for the people who know every deep cut.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Sabrina Carpenter Song Guesser FAQ',
  'faq': [
    ('Which Sabrina Carpenter songs will I hear?', 'A rotating pool of 77 tracks, from “Espresso” and “Please Please Please” to “Taste” and album cuts. The rotation spans her whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'anuel-aa', 'name': 'Anuel AA', 'count': 51,
  'title': 'Anuel AA Song Guesser — Guess the Anuel AA Song in 0.1 Seconds',
  'desc': 'Name the Anuel AA song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Anuel AA song guessing game with 51 tracks — no signup, no download.',
  'h1': 'Anuel AA Song Guesser',
  'hero': 'Guess the Anuel AA song from a tenth of a second — the dembow and the rasp give him away.',
  'vgdesc': 'A free browser song guessing game on 51 Anuel AA tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Anuel AA song game',
  'h2': 'About Anuel AA Song Guesser',
  'what_h3': 'What Is Anuel AA Song Guesser?',
  'p1': 'Anuel AA Song Guesser is a free audio game built on a catalog of Latin trap and reggaeton — the collab-heavy “China”, the slow-burn “Ella Quiere Beber” and the confessional “Secreto”. You get a tenth of a second, and you name it before the reveal starts doing your job. It’s a Heardle-style song guessing game for Anuel AA fans — but the opening is a tenth of a second, not one second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Anuel AA Song Guesser',
  'intro': 'Hear the sliver, trust the dembow, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of an Anuel track is the first clue — a dembow kick, a synth, or that rasp.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His trap and reggaeton modes each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 51 Anuel AA tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name an Anuel AA song from a single dembow hit, and listeners who want to hear how his Latin trap and reggaeton eras differ. Easy welcomes newcomers; Impossible is for the people who know every feature.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Anuel AA Song Guesser FAQ',
  'faq': [
    ('How many Anuel AA songs are in the pool?', 'Fifty-one tracks, from “China” and “Ella Quiere Beber” to “Secreto” and album cuts. The rotation spans his trap and reggaeton catalogs.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'don-toliver', 'name': 'Don Toliver', 'count': 65,
  'title': 'Don Toliver Song Guesser — Guess the Don Toliver Song in 0.1 Seconds',
  'desc': 'Name the Don Toliver song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Don Toliver song guessing game with 65 tracks — no signup, no download.',
  'h1': 'Don Toliver Song Guesser',
  'hero': 'Name the Don Toliver track from a tenth of a second — the falsetto and the haze give him away.',
  'vgdesc': 'A free browser song guessing game on 65 Don Toliver tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Don Toliver song game',
  'h2': 'About Don Toliver Song Guesser',
  'what_h3': 'What Is Don Toliver Song Guesser?',
  'p1': 'Don Toliver Song Guesser is a free audio game built on a catalog of wavy, melodic trap — the woozy “No Idea”, the hazy “After Party” and the falsetto-led “Cardigan”. The clip starts at 0.1 seconds and stays there until you ask for more. A song guessing game in the Heardle style for Don Toliver fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Don Toliver Song Guesser',
  'intro': 'Hear the sliver, trust the haze, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Don Toliver track is the first clue — a synth wash, an 808, or a falsetto note.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. His melodic hooks and features each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 65 Don Toliver tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Don Toliver song from a single synth swell, and listeners who want to hear how his wavy melodic trap sound evolved. Easy is a warm-up; Impossible is for the people who know every feature and leak.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Don Toliver Song Guesser FAQ',
  'faq': [
    ('How many Don Toliver songs are in the rotation?', 'Sixty-five tracks, from “No Idea” and “After Party” to “Cardigan” and album cuts. The pool rotates across his albums and features.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'tate-mcrae', 'name': 'Tate McRae', 'count': 66,
  'title': 'Tate McRae Song Guesser — Guess the Tate McRae Song in 0.1 Seconds',
  'desc': 'Name the Tate McRae song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Tate McRae song guessing game with 66 tracks — no signup, no download.',
  'h1': 'Tate McRae Song Guesser',
  'hero': 'Guess the Tate McRae song from a tenth of a second — the beat and the breath give her away.',
  'vgdesc': 'A free browser song guessing game on 66 Tate McRae tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Tate McRae song game',
  'h2': 'About Tate McRae Song Guesser',
  'what_h3': 'What Is Tate McRae Song Guesser?',
  'p1': 'Tate McRae Song Guesser is a free audio game built on a catalog of dark, dancer-ready pop — the stomping “greedy”, the wounded “You Broke Me First” and the restless “Exes”. The round opens on the shortest clip and only widens once you’ve had your guess. It’s the Heardle-style song guessing game for Tate McRae fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Tate McRae Song Guesser',
  'intro': 'Hear the sliver, trust the beat, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a Tate track is the first clue — a bass thump, a synth, or a breath.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. Her ballads and dance-pop cuts each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 66 Tate McRae tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Tate McRae song from a single bass thump, and listeners who want to hear how her vulnerable ballads grew into dancer-ready pop. Easy welcomes newcomers; Impossible is for the people who know every deep cut.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Tate McRae Song Guesser FAQ',
  'faq': [
    ('Which Tate McRae songs will I hear?', 'A rotating pool of 66 tracks, from “greedy” and “You Broke Me First” to “Exes” and album cuts. The rotation spans her whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'playboi-carti', 'name': 'Playboi Carti', 'count': 28,
  'title': 'Playboi Carti Song Guesser — Guess the Playboi Carti Song in 0.1 Seconds',
  'desc': 'Name the Playboi Carti song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Playboi Carti song guessing game with 28 tracks — no signup, no download.',
  'h1': 'Playboi Carti Song Guesser',
  'hero': 'Name the Playboi Carti track from a tenth of a second — the ad-lib and the rage give him away.',
  'vgdesc': 'A free browser song guessing game on 28 Playboi Carti tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Playboi Carti song game',
  'h2': 'About Playboi Carti Song Guesser',
  'what_h3': 'What Is Playboi Carti Song Guesser?',
  'p1': 'Playboi Carti Song Guesser is a free audio game built on a catalog of minimal, high-energy rap — the bouncy “Magnolia”, the rage-driven “Rockstar Made” and the woozy “Sky”. You hear the opening sliver, then type the title before the longer reveals step in. A Heardle-style song guessing game built for Playboi Carti fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'This is a <a href="/">song guesser</a> you play right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Playboi Carti Song Guesser',
  'intro': 'Hear the sliver, trust the beat, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Carti track is the first clue — an 808, a synth, or a baby-voice ad-lib.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. His minimalist and rage eras each have their own texture.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 28 Playboi Carti tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Playboi Carti song from a single ad-lib, and listeners who want to hear how his sound jumped from bouncy minimalism to rage. Easy is a warm-up; Impossible is for the people who know every leak.',
  'faq_eyebrow': 'Before you play',
  'faq_h2': 'Playboi Carti Song Guesser FAQ',
  'faq': [
    ('How many Playboi Carti songs are in the pool?', 'Twenty-eight tracks, from “Magnolia” and “Rockstar Made” to “Sky” and album cuts. The rotation spans his mixtapes and albums.'),
    ('Do I need an account to play?', 'No account, no app and no download. Open the page and the first 0.1-second clip plays — there is no paywall and no daily cap.'),
    ('Can I switch artists later?', 'Yes. Every artist, genre and decade is on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'bad-bunny', 'name': 'Bad Bunny', 'count': 56,
  'title': 'Bad Bunny Song Guesser — Guess the Bad Bunny Song in 0.1 Seconds',
  'desc': 'Name the Bad Bunny song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Bad Bunny song guessing game with 56 tracks — no signup, no download.',
  'h1': 'Bad Bunny Song Guesser',
  'hero': 'Guess the Bad Bunny song from a tenth of a second — the dembow and the swagger give him away.',
  'vgdesc': 'A free browser song guessing game on 56 Bad Bunny tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Bad Bunny song game',
  'h2': 'About Bad Bunny Song Guesser',
  'what_h3': 'What Is Bad Bunny Song Guesser?',
  'p1': 'Bad Bunny Song Guesser is a free audio game built on a catalog that bends reggaeton, trap and pop — the playful “Tití Me Preguntó”, the breezy “Me Porto Bonito” and the dreamy “Dákiti”. A sliver of audio plays, and you have to name the song before more of it spills out. It’s Heardle-style song guessing aimed at Bad Bunny fans — but the opening is a tenth of a second, not one second.',
  'p2': 'Open this <a href="/">song guesser</a> in any browser — no app, no login, no daily cap. Miss or skip and the clip steps up to 0.5s, 2s, 8s, then 15s; the earlier you place it, the sharper the round.',
  'how_h3': 'How to Play Bad Bunny Song Guesser',
  'intro': 'Hear the sliver, trust the dembow, and reveal more only when you must.',
  'steps': [
    ('▶', 'Start at 0.1 seconds', 'A tenth of a second of a Bad Bunny track is the first clue — a dembow kick, a synth, or a vocal bend.'),
    ('⌕', 'Name the title', 'Type part of the name and pick from the suggestions. His reggaeton, trap and pop crossovers each open a little differently.'),
    ('⏭', 'Reveal only when stuck', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the point.'),
    ('♾', 'Play without limits', 'Unlimited rounds across 56 Bad Bunny tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can name a Bad Bunny song from a single dembow hit, and listeners who want to hear how his sound crossed from trap to global pop. Easy welcomes newcomers; Impossible is for the people who know every feature.',
  'faq_eyebrow': 'Before your first round',
  'faq_h2': 'Bad Bunny Song Guesser FAQ',
  'faq': [
    ('How many Bad Bunny songs are in the rotation?', 'Fifty-six tracks, from “Tití Me Preguntó” and “Me Porto Bonito” to “Dákiti” and album cuts. The pool rotates across his albums.'),
    ('Is it free to play?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — the full catalog lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
 {
  'slug': 'katy-perry', 'name': 'Katy Perry', 'count': 59,
  'title': 'Katy Perry Song Guesser — Guess the Katy Perry Song in 0.1 Seconds',
  'desc': 'Name the Katy Perry song from a 0.1-second clip, then reveal 0.5s, 2s, 8s and 15s. A free Katy Perry song guessing game with 59 tracks — no signup, no download.',
  'h1': 'Katy Perry Song Guesser',
  'hero': 'Name the Katy Perry track from a tenth of a second — the chorus and the gloss give her away.',
  'vgdesc': 'A free browser song guessing game on 59 Katy Perry tracks. Name each song from a 0.1-second clip, revealing longer clips only when you need more.',
  'eyebrow': 'About this Katy Perry song game',
  'h2': 'About Katy Perry Song Guesser',
  'what_h3': 'What Is Katy Perry Song Guesser?',
  'p1': 'Katy Perry Song Guesser is a free audio game built on a catalog of candy-colored pop — the sparkler “Firework”, the stadium chant of “Roar” and the slinky “Dark Horse”. Every round starts on a sliver of audio and waits for you to call the track before it opens up. The Heardle-style song guessing game for Katy Perry fans — except the opening clip is a tenth of a second, not a whole second.',
  'p2': 'Play this <a href="/">song guesser</a> right in the browser — no app, no login, no daily limit. Wrong or skip and the clip grows to 0.5s, 2s, 8s, then 15s; the shorter the clip you beat, the better the round.',
  'how_h3': 'How to Play Katy Perry Song Guesser',
  'intro': 'Hear the sliver, trust the hook, and reveal more only when you are stuck.',
  'steps': [
    ('▶', 'Open at 0.1s', 'A tenth of a second of a Katy track is the first clue — a synth pop, a drum fill, or the start of a chorus.'),
    ('⌕', 'Type the title', 'Type part of the name and pick from the suggestions. Her big pop and ballad modes each open a little differently.'),
    ('⏭', 'Reveal sparingly', 'A miss or skip stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the shortest clip is the goal.'),
    ('♾', 'Play every round', 'Unlimited rounds across 59 Katy Perry tracks, with difficulty from Easy to Impossible.'),
  ],
  'who_h3': 'Who Will Love This Game?',
  'who_p': 'Fans who can place a Katy Perry song from a single synth pop, and listeners who want to hear how her bubblegum pop matured across eras. Easy is a warm-up; Impossible is for the people who know every deep cut.',
  'faq_eyebrow': 'Good to know first',
  'faq_h2': 'Katy Perry Song Guesser FAQ',
  'faq': [
    ('Which Katy Perry songs will I hear?', 'A rotating pool of 59 tracks, from “Firework” and “Roar” to “Dark Horse” and album cuts. The rotation spans her whole career.'),
    ('Is the game actually free?', 'Yes. It runs in the browser with no signup and no download, and there is no daily limit on rounds.'),
    ('Can I play other artists too?', 'Yes — every artist, genre and decade lives on the main <a href="/">Song Guesser</a> page.'),
  ],
 },
]

EXTRA = {
 "the-weeknd": {
  "tips": "Lock onto the first synth color before the vocal lands — “Blinding Lights” opens with a rising arp, while “Starboy” leans on a low filtered pulse. If the sliver is dry and drum-free, you are usually inside one of the slower After Hours ballads, so reach for those titles first.",
  "closing": "The Weeknd Song Guesser turns his catalog into a tenth-of-a-second test — neon synths, bruised falsetto and all. When the 65-track pool starts to feel familiar, the main Song Guesser opens the door to every other artist, genre and decade on the site.",
  "faq": [
   [
    "Do the clips always start at the song intro?",
    "They open at the real start of each track, not a random spot, so the first 0.1 seconds is always the record's actual intro. That keeps it fair — you are naming the song from the same first impression a radio listener gets."
   ],
   [
    "Why are there 65 Weeknd songs and not the full discography?",
    "The pool is curated around the intros that read best in a split second — the hits plus the most recognizable album cuts. Obscure b-sides are left out so a casual fan still has a fair chance."
   ],
   [
    "Does it play the whole track after I guess?",
    "No. It is an identification game, not a streamer, so the round ends the moment you name it and the next clip loads. That is exactly why guessing from the shortest clip is the real flex."
   ]
  ]
 },
 "taylor-swift": {
  "tips": "Place the era first. A twangy acoustic strum points to her early country records, while a slick 808 and a half-whispered cadence point to reputation and after. Naming the era usually cuts the search in half before you reveal more audio.",
  "closing": "Taylor Swift Song Guesser runs from Nashville twang to synth-pop and the hushed textures of folklore, all at a tenth of a second. When you have worn out her 74-song pool, the main Song Guesser has 34 more artists plus genre and decade quizzes waiting.",
  "faq": [
   [
    "How are her re-recorded versions handled?",
    "The pool uses the original recordings, not Taylor's Versions, so the intros you hear are the ones that first hit the radio. That keeps the guess fair for people who memorized the originals years ago."
   ],
   [
    "Does it separate her albums or mix them?",
    "It mixes every era into one rotating pool, so Fearless can follow Midnights back to back. There is no album filter on this page, which means you have to be ready for any era in a single sitting."
   ],
   [
    "What if I only know the singles?",
    "Easy difficulty leans the rotation toward the radio hits such as Love Story, Shake It Off and Anti-Hero. Deeper album cuts surface more often as you raise the difficulty."
   ]
  ]
 },
 "michael-jackson": {
  "tips": "Lock onto the drum pattern and the breath. Jackson's intros are famously rhythmic — a beatboxed groove, a gated snare or a sharp intake — and each one is distinct. If the first sound is pure percussion, you can usually place the era before any vocal arrives.",
  "closing": "Michael Jackson Song Guesser tests the King of Pop's 70 most recognizable grooves from a tenth of a second. When you can call Billie Jean from its first beat, the main Song Guesser is there with every other artist, genre and decade to keep the streak going.",
  "faq": [
   [
    "Are live versions or remixes in the rotation?",
    "No. The pool sticks to the studio recordings you know from the albums and radio, so every intro is instantly recognizable instead of relying on a remix most fans never heard."
   ],
   [
    "Why do the clips start so short?",
    "The 0.1-second opening is the whole point — Jackson's intros were engineered to be iconic, so a single beat or breath is often enough. The longer reveals only exist as a fallback when you are stuck."
   ],
   [
    "Which era is represented most?",
    "The pool draws from the Off the Wall through HIStory singles and the biggest album cuts, weighted toward the songs people can actually place. Obscure b-sides are left out on purpose."
   ]
  ]
 },
 "beyonce": {
  "tips": "Her vocal runs are the fastest tell, but the arrangement usually names the song first — a horn stab means Crazy in Love, a marching-band snare means Single Ladies. Trust the production before you reach for the melody.",
  "closing": "Beyoncé Song Guesser spans the horn-heavy strut of her early hits to the stadium choruses and album-deep cuts, all at a tenth of a second. When her 55-track pool feels conquered, the main Song Guesser has every other artist and genre ready to go.",
  "faq": [
   [
    "How far into her discography does the pool reach?",
    "From the Destiny's Child era through Renaissance and Cowboy Carter, weighted toward the solo singles people can place fast. The deep cuts that appear are the ones with the most recognizable openings."
   ],
   [
    "Do the visuals matter for guessing?",
    "Not at all — the game is audio only, a single clip and a search box. You never see a video or a lyric snippet, which keeps it about the ear rather than the eye."
   ],
   [
    "Can I pick a specific album to drill?",
    "This page mixes her whole catalog in one rotation. If you want era-specific practice, the difficulty dial is the closest thing to a filter — Easy favors the biggest singles."
   ]
  ]
 },
 "rihanna": {
  "tips": "Separate the dance-floor records from the ballads by the first hit — a steel drum or a four-on-the-floor kick points to her club era, a lone piano points to the torch songs. That one distinction solves most rounds before the vocal arrives.",
  "closing": "Rihanna Song Guesser runs from the steel-drum pulse of Umbrella to the pounding chorus of Diamonds, all at a tenth of a second. When her 68-track pool starts to feel automatic, the main Song Guesser is waiting with every other artist, genre and decade.",
  "faq": [
   [
    "Do collaborations count in the rotation?",
    "Yes — the pool includes her biggest features and duets, not just solo singles. If she leads the record, it can appear, so expect the occasional guest verse to help place the track."
   ],
   [
    "What happens when I skip a round?",
    "Skipping simply reveals the next-longest clip — 0.5s, 2s, 8s, then 15s — and never locks the round. There is no penalty, so a skip is really just a request for more audio."
   ],
   [
    "Is the song list the same every day?",
    "No. There is no daily puzzle and no fixed order — the pool reshuffles every time you play, so two visits to the page never start the same way."
   ]
  ]
 },
 "drake": {
  "tips": "His eras are separated by mood and drums — a sparse piano and a slow knock point to the Take Care years, a brighter island bounce points to More Life and after. Name the era first and the title usually follows from the opening ad-lib.",
  "closing": "Drake Song Guesser tests the moody piano, the shimmering hooks and the island bounce of his 69-track pool at a tenth of a second. Once you have it down cold, the main Song Guesser opens up every other artist, genre and decade on the site.",
  "faq": [
   [
    "How are features handled in the pool?",
    "The rotation includes the records Drake leads, and guest verses stay in the clip, so a recognizable voice can hand you the song. You are still naming the Drake track, not the feature."
   ],
   [
    "Why do some rounds feel harder than others?",
    "The rotation mixes deep album cuts with the radio hits on purpose. On Easy it leans to the singles; on Impossible it reaches for the mixtape cuts only devoted fans will know."
   ],
   [
    "Does the 0.1-second clip favor producers or singers?",
    "Both, but production usually wins — Drake's beat changes are famous. A drum fill or a piano note often names the song before the vocal does, which is what the game is built on."
   ]
  ]
 },
 "eminem": {
  "tips": "The beat is the giveaway before the bars. A tense piano loop means Lose Yourself, a rainy guitar figure means Stan, a cartoonish bounce means Without Me. Hear the production first and the cadence just confirms it.",
  "closing": "Eminem Song Guesser tests 66 tracks — the tense pianos, the rainy-night gloom and the cartoon bounce — at a tenth of a second. When his catalog is in your ear, the main Song Guesser keeps the streak alive across every other artist and decade.",
  "faq": [
   [
    "Do the instrumental intros give too much away?",
    "On purpose — Eminem's intros are some of the most recognizable in rap, so the game leans on them. The difficulty is not in the clue but in how little of it you allow yourself before guessing."
   ],
   [
    "Are skits and interludes included?",
    "No. Only actual songs appear in the rotation, never the album skits, so every round is a real track you could name from its opening."
   ],
   [
    "What separates Easy from Impossible here?",
    "Easy surfaces the radio staples like Lose Yourself and Stan more often and reveals longer clips sooner. Impossible reaches for album cuts and expects you to solve from the barest sliver."
   ]
  ]
 },
 "kanye-west": {
  "tips": "His samples and drums changed every album, so the first sound is a timestamp — a sped-up soul chip means the College era, a Daft Punk stomp means Graduation, a spare 808 means Yeezus. Identify the era and the title is usually one guess away.",
  "closing": "Kanye West Song Guesser runs from chipmunk soul to the 808 era across 61 tracks at a tenth of a second. When his catalog is memorized, the main Song Guesser has every other artist, genre and decade ready to test you next.",
  "faq": [
   [
    "Does the pool change because albums keep getting reworked?",
    "The pool is fixed to the original studio versions you know, not the re-edits. That keeps the intros stable and recognizable instead of shifting every time an album gets a new cut."
   ],
   [
    "Which songs are hardest to place?",
    "The sparest productions — a lone 808 or a single sample flip — are the hardest because they give you almost no melody. Those surface mostly on Impossible difficulty."
   ],
   [
    "Can I practice one era at a time?",
    "Not on this page; it shuffles the whole catalog. The main Song Guesser home page is where you can hop between artists and decades to narrow your focus."
   ]
  ]
 },
 "justin-bieber": {
  "tips": "The production is the timeline — a glossy R&B strum means his early teen-pop years, a trop-house shaker means the Purpose era, a laid-back acoustic loop means Changes and after. Lock the era from the first hit and the search narrows fast.",
  "closing": "Justin Bieber Song Guesser spans the pop-soul of Baby to the soft bounce of Peaches across 69 tracks at a tenth of a second. When his pool is mastered, the main Song Guesser opens the full catalog of artists, genres and decades.",
  "faq": [
   [
    "Do remixes like the Kid Laroi duet appear?",
    "The rotation uses the original recordings, so you hear the album and single versions rather than remixes. That keeps the intros consistent with what most listeners memorized."
   ],
   [
    "Why is the difficulty dial useful here?",
    "His catalog shifted genres several times, so Easy favors the biggest singles and Impossible reaches for the album cuts across all eras. It is the cleanest way to match the game to how deep a fan you are."
   ],
   [
    "Are acoustic versions in the mix?",
    "No — only the studio tracks are used, which means the opening you hear is always the one that charted rather than a stripped-back live take."
   ]
  ]
 },
 "linkin-park": {
  "tips": "Their signature is the blend, so listen for the balance — a clean keyboard loop with no guitar means the early nu-metal era, a heavier chug with electronics means the later albums. The ratio of guitar to synth is the era stamp.",
  "closing": "Linkin Park Song Guesser tests the keys, the riffs and the electronics of their 67-track catalog at a tenth of a second. When you can name In the End from a single note, the main Song Guesser has every other artist, genre and decade waiting.",
  "faq": [
   [
    "Does the pool include the newer vocal era?",
    "It spans the full catalog, including the later recordings, but it is weighted toward the songs people can actually place from an intro. The riffs and the electronics are the giveaways either way."
   ],
   [
    "What if I only know the radio hits?",
    "Easy difficulty leans on the singles — In the End, Numb, One Step Closer — so a casual fan can still play. The deeper cuts surface more as you turn the dial up."
   ],
   [
    "Why does a tenth of a second work for a rock band?",
    "Their intros are built from distinctive synth lines and guitar figures that read instantly. A single keyboard stab or a chugging riff is often enough to name the track."
   ]
  ]
 },
 "lady-gaga": {
  "tips": "Her catalog flips between dance-pop, jazz and stripped ballads, so the first sound tells you which Gaga you are dealing with — a pulsing synth means the club era, a lone piano means the ballads and duets. Use that split before you reveal anything.",
  "closing": "Lady Gaga Song Guesser runs from the electro stomp of Poker Face to the stripped-down Shallow across 69 tracks at a tenth of a second. When her eras are all in your ear, the main Song Guesser has every other artist and decade ready next.",
  "faq": [
   [
    "Do the jazz and soundtrack records appear?",
    "A few of the most recognizable ones do, but the pool is weighted toward the pop singles and the duets people know cold. The point is to be tested on what you can actually place."
   ],
   [
    "Which songs trip people up most?",
    "The mid-tempo bridges and the less-played album cuts, because they lack the signature synth hook. Those are the rounds where the longer reveals actually earn their keep."
   ],
   [
    "Is there a way to hear more without guessing wrong?",
    "Yes — skipping is not a failure. It advances the clip to the next length without locking anything, so you can use skips purely to buy more audio when you are close."
   ]
  ]
 },
 "bruno-mars": {
  "tips": "His sound is a live band, so listen for the instrument that leads — a horn blast means the funk records, a finger-picked guitar means the ballads, a doo-wop sway means the early singles. The lead instrument usually names the song.",
  "closing": "Bruno Mars Song Guesser tests the horns, the doo-wop and the falsetto of his 62-track catalog at a tenth of a second. When his grooves are memorized, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Do the Silk Sonic duets count?",
    "They are kept separate, so this pool stays focused on his solo records and the hits he leads. That keeps the intros consistent with his own catalog rather than a side project."
   ],
   [
    "What is the hardest thing to place here?",
    "The ballads, because they share a similar piano-and-voice opening. The funk records are the easiest — a horn or a snare usually gives the whole thing away."
   ],
   [
    "Why does the game suit his music so well?",
    "His intros are built like radio stings — short, bright and distinctive. A tenth of a second is often the whole intro of a Bruno Mars hook, which makes the game fast and fair."
   ]
  ]
 },
 "adele": {
  "tips": "The piano is the fingerprint — each ballad opens with its own chord voicing and tempo, and the albums have distinct feels from 19 to 30. If the sliver is a low, slow chord, think 25 and the later records; if it is a stomping snare, think Rolling in the Deep.",
  "closing": "Adele Song Guesser tests the stomp and the hush of her 50-track catalog at a tenth of a second. When her ballads are all in your ear, the main Song Guesser has every other artist, genre and decade ready to keep you guessing.",
  "faq": [
   [
    "Why is the pool only 50 songs?",
    "Her catalog is deliberately small and carefully sequenced, so 50 tracks already covers the albums and the biggest singles. The pool favors quality of intros over raw count."
   ],
   [
    "Do the live versions appear?",
    "No — only the studio recordings are used, so the piano opening you hear is the one from the album, not a live arrangement that changes from night to night."
   ],
   [
    "What is the best clue on an Adele round?",
    "The tempo and the key of the opening piano. 19 is sparser, 21 is bigger, 25 and 30 are warmer — that one difference usually points you to the right album before any vocal lands."
   ]
  ]
 },
 "ariana-grande": {
  "tips": "The vocal runs are famous but the production is the faster tell — a trap-lite hi-hat means the thank u, next era, a glossy synth means the earlier pop years. Hear the beat texture first and let the whistle tone just confirm it.",
  "closing": "Ariana Grande Song Guesser spans the trap-lite bounce and the glossy pop of her 64-track catalog at a tenth of a second. When her runs are all in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   [
    "Does the pool lean toward recent albums?",
    "It balances the whole career, from the early pop singles through the R&B-leaning recent records. Easy favors the biggest radio hits; Impossible reaches for the album deep cuts."
   ],
   [
    "Are collabs and features in the rotation?",
    "Only the songs she leads, so the guess is always an Ariana Grande track rather than a feature. Guest verses can still appear inside the clip to help you place it."
   ],
   [
    "What gives a song away fastest?",
    "The beat texture — her production shifts clearly between eras. A whistle tone is a strong clue, but the hi-hat and the synth usually name the song even before she sings."
   ]
  ]
 },
 "billie-eilish": {
  "tips": "Her sound lives in the bass and the breath, so listen below the melody — a slinky sub-bass means bad guy, a soft reverb wash means the ballads, a blown-out guitar means Happier Than Ever. The low end is the whole clue.",
  "closing": "Billie Eilish Song Guesser tests the hushed verses and the blown-out choruses of her 58-track catalog at a tenth of a second. When her low end is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Why do the clips feel so quiet to start?",
    "Because her records are built on quiet, bass-heavy intros rather than loud hooks. The 0.1-second opening is a whisper or a bass thump, which is exactly the signature the game wants you to catch."
   ],
   [
    "Do the music-video versions differ?",
    "The game uses the studio audio, not the video edits, so the clip is always the track as it was released. You never have to match a specific visual moment."
   ],
   [
    "What trips players up on her songs?",
    "The ballads share a similar reverb-soaked opening, so a quiet sliver can sound like several tracks. Letting the clip reach 2s or 8s on those rounds is the smart play."
   ]
  ]
 },
 "ed-sheeran": {
  "tips": "The loop is the signature — his songs are built on a single looped guitar or percussion figure, and each one is distinct. Lock the rhythm of the loop before the melody and you can usually name the track from the first strum.",
  "closing": "Ed Sheeran Song Guesser tests the loop-pedal pop of his 70-track catalog at a tenth of a second. When his loops are all in your ear, the main Song Guesser has every other artist, genre and decade ready to keep you guessing.",
  "faq": [
   [
    "Are the acoustic and pop versions separated?",
    "The pool uses the studio singles as released, so you hear the chart version rather than a live loop-pedal take. That keeps the intros consistent with what most listeners know."
   ],
   [
    "Why do some rounds feel like the same song?",
    "His loops are close cousins across albums, which is part of the challenge. The difficulty dial helps — Easy leans on the unmistakable hits like Shape of You and Thinking Out Loud."
   ],
   [
    "Do collaborations appear?",
    "The rotation includes the duets he leads, so a guest voice can sometimes hand you the track. The guess is always an Ed Sheeran song."
   ]
  ]
 },
 "coldplay": {
  "tips": "Their two eras are split by instrumentation — a clean piano or an acoustic strum means the early records, a synth pad and a digital sheen means the later ones. Identify the era from the first chord and the title is usually one guess away.",
  "closing": "Coldplay Song Guesser spans the reverb-washed rock and the electronic later records across 68 tracks at a tenth of a second. When their catalog is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Does the pool span the whole career?",
    "Yes, from Parachutes through the recent records, weighted toward the songs people can place fast. The early piano-led tracks and the later synth tracks sit side by side in the same rotation."
   ],
   [
    "What gives a Coldplay song away fastest?",
    "The opening texture — a piano figure, a string swell or a synth pad. Their intros are atmospheres first, melodies second, so the first sound is usually the strongest clue."
   ],
   [
    "Are the collaborations in the mix?",
    "A few of the most recognizable ones appear, but the pool centers on their own songs so the guess stays focused on the band."
   ]
  ]
 },
 "bts": {
  "tips": "Their catalog mixes Korean and English singles, so the production is the first tell — a disco sparkle means the English-era hits, a layered hip-hop beat means the earlier records. Place the era and the language of the hook follows naturally.",
  "closing": "BTS Song Guesser tests the beat drops and the layered pop of their 75-track catalog at a tenth of a second. When their discography is in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   [
    "Are solo tracks from the members included?",
    "The rotation focuses on group songs rather than the solo records, so every round is a BTS track you can name from the band's signature. That keeps the pool consistent."
   ],
   [
    "How are Korean and English versions handled?",
    "The pool uses the released versions as they charted, so a track appears in the form listeners actually know. You never have to distinguish between a Korean and an English take of the same song."
   ],
   [
    "What is the strongest clue on their songs?",
    "The intro beat — BTS records open with distinctive synth stabs, chants and drops. A single drum or a vocal sample usually names the track before the chorus arrives."
   ]
  ]
 },
 "blackpink": {
  "tips": "Every comeback has its own signature opening — a marching stomp, a chanted drop, a bass thump — so the first half-second is a timestamp. Learn the opening of each single and the 37-track pool shrinks to a handful of easy rounds.",
  "closing": "BLACKPINK Song Guesser tests the stomp and the chants of their 37-track catalog at a tenth of a second. When every comeback is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Why is the pool smaller than other artists?",
    "Their catalog is compact on purpose — fewer songs, each with a huge, distinct intro. A smaller pool means the game leans on recognition of each single rather than volume."
   ],
   [
    "Do the solo releases appear?",
    "No — the rotation stays focused on the group's songs, so every round is a BLACKPINK track. The solo records are kept separate."
   ],
   [
    "What separates their intros from each other?",
    "Each title track was built around a signature opening — a marching snare, a bass growl or a chanted hook. That is exactly why a tenth of a second is usually enough to place it."
   ]
  ]
 },
 "gdragon": {
  "tips": "His sound kept mutating, so the first beat is a timestamp — a neon synth burst means the early solo years, a self-lacerating guitar means the later records, a BIGBANG-era bounce means the group work. Identify the era and the title follows.",
  "closing": "G-DRAGON Song Guesser spans the neon bursts and the shape-shifting pop of his 50-track catalog at a tenth of a second. When his solo and group eras are all in your ear, the main Song Guesser has every other artist and decade waiting.",
  "faq": [
   [
    "Are BIGBANG songs in the pool?",
    "A few of his most recognizable group-era tracks appear alongside the solo records, since his sound crosses both. The guess is always a G-DRAGON record either way."
   ],
   [
    "How do I tell his eras apart by ear?",
    "The production palette changed almost every album — early records are neon and electro, later ones are more minimal and melodic. The first synth or drum usually names the era."
   ],
   [
    "Why does Easy help more here?",
    "His catalog is deep and varied, so Easy surfaces the best-known tracks like Crayon and Crooked more often. Impossible reaches for the solo deep cuts and features."
   ]
  ]
 },
 "david-guetta": {
  "tips": "His records live on the build and the drop, so the first sound is a genre stamp — a piano lift means the vocal-house era, a big-room synth means the festival years. Name the era from the opening and the title is usually one guess away.",
  "closing": "David Guetta Song Guesser spans the piano lifts and the festival drops of his 64-track catalog at a tenth of a second. When his build-ups are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Are the collabs and features included?",
    "Yes — the rotation includes his biggest collaborations, since they are the records he leads. A guest vocal often hands you the song, but the guess is still a David Guetta track."
   ],
   [
    "What gives his songs away fastest?",
    "The opening chord or synth before the vocal drops in. His intros are built as radio stings, so a single piano note or a synth stab usually names the record."
   ],
   [
    "Do the remixes count as separate songs?",
    "No — the pool uses the original single versions, not the countless remixes. That keeps the intros consistent with the songs people actually remember."
   ]
  ]
 },
 "pitbull": {
  "tips": "The horn and the shout are the calling card — a brass blast means the party records, a four-on-the-floor kick means the club crossovers. Lock the lead instrument first and the title usually lands from the opening shout.",
  "closing": "Pitbull Song Guesser tests the horns and the party-starting bounce of his 68-track catalog at a tenth of a second. When his anthems are in your ear, the main Song Guesser has every other artist, genre and decade ready to keep the streak alive.",
  "faq": [
   [
    "Do the guest verses stay in the clip?",
    "Yes — his biggest hits are collaborations, so a guest vocal or a borrowed hook often appears. You are still naming the Pitbull track, but the feature can hand it to you."
   ],
   [
    "What is the hardest thing to place here?",
    "The deep album cuts that never got the single treatment, because they lack the signature horn. Those mostly surface on Impossible difficulty."
   ],
   [
    "Why does a tenth of a second suit his music?",
    "His intros are built to start a party instantly — a horn blast or a kick drum on beat one. The very first sound is usually the giveaway."
   ]
  ]
 },
 "kendrick-lamar": {
  "tips": "His albums each have a sonic stamp, so the first sound names the record — a jittery piano means To Pimp a Butterfly, a jazz-funk bounce means DAMN., a g-funk shimmer means the recent era. Place the album and the title follows.",
  "closing": "Kendrick Lamar Song Guesser spans the jazz-inflected beats and the beat switches of his 62-track catalog at a tenth of a second. When his eras are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Do the beat switches affect the clips?",
    "The clips stay at the intro, so you hear the first 0.1 seconds of the track as recorded — even on songs that switch later. The switch never jumps you forward mid-round."
   ],
   [
    "Which albums are covered?",
    "From Section.80 through the recent releases, weighted toward the tracks people can place from an intro. The deeper narrative cuts appear mostly on harder difficulties."
   ],
   [
    "What is the strongest clue on his songs?",
    "The drum pattern and the vocal bend. His intros are production-first, so a snare or a sample flip usually names the record before the verse begins."
   ]
  ]
 },
 "olivia-rodrigo": {
  "tips": "Her two modes are easy to separate — a lone piano means the ballads, a crunchy guitar downstroke means the pop-punk cuts. The very first instrument names the song family, and the title is usually one guess from there.",
  "closing": "Olivia Rodrigo Song Guesser spans the diary-style ballads and the pop-punk sneer of her 50-track catalog at a tenth of a second. When her hooks are in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   [
    "Why is the pool 50 songs across two albums?",
    "Her catalog is still compact, so 50 tracks covers both records plus the biggest singles and non-album cuts. The pool will grow as her discography does."
   ],
   [
    "Do the acoustic versions appear?",
    "No — the game uses the studio recordings, so you hear the album production rather than a stripped-back take. That keeps every intro consistent."
   ],
   [
    "What trips players up on her songs?",
    "The ballads share a similar piano opening, so a quiet sliver can sound like several tracks. Waiting for the 2s reveal on those rounds is usually the smarter move."
   ]
  ]
 },
 "lana-del-rey": {
  "tips": "Her records live in atmosphere — a string swell means the cinematic singles, a sparse guitar means the later folk-leaning records, a dreamy synth means the Born to Die era. Identify the texture and the title usually follows.",
  "closing": "Lana Del Rey Song Guesser spans the cinematic sweep and the Americana turn of her 52-track catalog at a tenth of a second. When her moods are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Why do her intros all sound alike?",
    "They share a reverb-soaked, cinematic texture on purpose, which is part of the challenge. The tell is the lead instrument — strings, guitar or synth — and the tempo of the opening."
   ],
   [
    "Do the unreleased tracks appear?",
    "No — the pool sticks to officially released songs, so every round is a track you could have heard on an album. That keeps the game fair."
   ],
   [
    "What is the hardest era to place?",
    "The mid-career ballads, because they blur together at a tenth of a second. The Born to Die era is the easiest thanks to its distinct synth-and-strings opening."
   ]
  ]
 },
 "maroon-5": {
  "tips": "Their sound drifted from rock to radio pop, so the first instrument is a timestamp — a funky guitar means the early records, a glossy synth means the later singles. Name the era from the opening and the title is usually one guess away.",
  "closing": "Maroon 5 Song Guesser spans the funky guitar and the polished pop of their 72-track catalog at a tenth of a second. When their singles are in your ear, the main Song Guesser has every other artist, genre and decade ready to keep you guessing.",
  "faq": [
   [
    "Do the Adam Levine features appear?",
    "The pool stays focused on Maroon 5 songs, so his solo features and side records are kept out. The guess is always a Maroon 5 track."
   ],
   [
    "What gives their songs away fastest?",
    "The opening riff or the synth — their singles are built around a single hook that leads the track. A funky strum or a falsetto note usually names the record."
   ],
   [
    "Why does Easy help casual fans here?",
    "Their catalog is deep, so Easy leans on the unmistakable hits like Moves Like Jagger and Sugar. Impossible reaches for the album cuts only devoted fans will know."
   ]
  ]
 },
 "shakira": {
  "tips": "Her catalog splits between Latin rock and global pop, and the lead instrument names the lane — a trumpet means the big singles, an Andean flute means the earlier rock records. Identify the instrument first and the title follows.",
  "closing": "Shakira Song Guesser spans the Latin rock and the global pop of her 67-track catalog at a tenth of a second. When her rhythm is in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Are the Spanish and English tracks mixed together?",
    "Yes — the pool mixes both catalogs into one rotation, so a Spanish deep cut can follow an English smash back to back. That bilingual range is part of the challenge."
   ],
   [
    "What is the strongest clue on her songs?",
    "The rhythm and the lead instrument — a trumpet hook, a flute line or a percussion figure. Her intros are rhythmic first, so the first beat usually names the record."
   ],
   [
    "Do the World Cup anthems appear?",
    "The most recognizable ones do, alongside the hits and album cuts. The pool is weighted toward the songs people can actually place from an intro."
   ]
  ]
 },
 "travis-scott": {
  "tips": "His sound is texture — an 808 with a pitched-down vocal means the mixtape era, a woozy synth drone means Astroworld, a harder, rage-leaning beat means the recent records. Name the texture from the first hit and the title follows.",
  "closing": "Travis Scott Song Guesser spans the woozy 808s and the beat switches of his 77-track catalog at a tenth of a second. When his textures are in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   [
    "Do the ad-libs give the song away?",
    "Often, yes — his ad-libs are a signature, and a single “It's lit!” or the auto-tuned hum can name the era instantly. The game leans on them just as much as the beat."
   ],
   [
    "Are features included in the pool?",
    "The rotation includes the records he leads, and guest verses stay in the clip. The guess is always a Travis Scott track, but a feature voice can hand it to you."
   ],
   [
    "Why is his catalog the biggest on this list?",
    "At 77 tracks, his pool is deep because his mixtapes and albums each produced recognizable intros. The harder difficulties reach for the leaks and the deep cuts."
   ]
  ]
 },
 "sabrina-carpenter": {
  "tips": "Her sound is sharp and hook-first, so the opening is the whole clue — a disco bassline means the recent singles, a guitar strum means the earlier pop, a playful vocal means the wink-and-a-smile records. Trust the first sound.",
  "closing": "Sabrina Carpenter Song Guesser spans the disco basslines and the sharp hooks of her 77-track catalog at a tenth of a second. When her singles are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Why is the pool 77 songs?",
    "Her catalog stretches across several albums and EPs, and the pool pulls the intros that read best in a split second — the singles plus the most recognizable deep cuts."
   ],
   [
    "Do the non-album singles appear?",
    "Yes — the rotation includes the standalone hits alongside the album tracks, since they are often her most recognizable records."
   ],
   [
    "What is the hardest thing to place here?",
    "The mid-tempo tracks without the disco bounce, because they share a similar pop texture. The recent singles are the easiest thanks to their distinct basslines."
   ]
  ]
 },
 "anuel-aa": {
  "tips": "His lane is the dembow and the rasp, so the first sound is the stamp — a reggaeton dembow means the club records, a darker trap beat means the street anthems. Identify the beat first and the title usually follows.",
  "closing": "Anuel AA Song Guesser spans the Latin trap and the reggaeton of his 51-track catalog at a tenth of a second. When his beats are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Are the collabs in the rotation?",
    "Yes — his biggest records are collaborations, so a guest voice or a borrowed hook often appears in the clip. The guess is always an Anuel AA track."
   ],
   [
    "Do I need to know Spanish to play?",
    "No — you are matching the audio to a title, not reading lyrics. If you know the beat, the language of the vocal is irrelevant to the guess."
   ],
   [
    "What gives his songs away fastest?",
    "The dembow pattern and the rasp of his voice. His intros are rhythmic first, so the first kick drum or synth line usually names the record."
   ]
  ]
 },
 "don-toliver": {
  "tips": "His sound is wavy and melodic, so the first texture is the tell — a hazy synth wash means the early hits, a brighter bounce means the recent records, a woozy falsetto means the ballads. Name the texture and the title follows.",
  "closing": "Don Toliver Song Guesser spans the woozy synths and the falsetto of his 65-track catalog at a tenth of a second. When his melodies are in your ear, the main Song Guesser has every other artist, genre and decade waiting next.",
  "faq": [
   [
    "Do the features appear in the pool?",
    "The rotation includes the records he leads, and guest verses stay in the clip. The guess is always a Don Toliver track, but a feature voice can hand it to you."
   ],
   [
    "What is the strongest clue on his songs?",
    "The synth wash and the falsetto note — his intros are atmospheric before they are rhythmic. A single swelling pad usually names the era."
   ],
   [
    "Why does Easy help casual fans here?",
    "His catalog is deep and the textures blur together, so Easy leans on the unmistakable hits like No Idea and After Party. Impossible reaches for the deep cuts."
   ]
  ]
 },
 "tate-mcrae": {
  "tips": "Her two modes are easy to split — a stomping beat means the dance-pop singles, a sparse piano means the ballads. The first sound names the lane, and the title is usually one guess from there.",
  "closing": "Tate McRae Song Guesser spans the dancer-ready pop and the wounded ballads of her 66-track catalog at a tenth of a second. When her hooks are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Why is the pool larger than her album count suggests?",
    "It pulls the singles, the EPs and the album deep cuts together, so 66 tracks covers her full catalog rather than just one record. The pool is weighted toward the songs people know."
   ],
   [
    "Do the dance mixes appear?",
    "No — the game uses the studio versions, so you hear the original production rather than a remix. That keeps the intros consistent with the released tracks."
   ],
   [
    "What trips players up on her songs?",
    "The ballads share a similar sparse opening, so a quiet sliver can sound like several tracks. Letting the clip reach 2s on those rounds is the smart play."
   ]
  ]
 },
 "playboi-carti": {
  "tips": "His eras are separated by energy — a bouncy, minimal beat means the early records, a rage-driven wall of 808s means the recent era. The first hit names the phase, and the ad-lib confirms it.",
  "closing": "Playboi Carti Song Guesser spans the bounce and the rage of his 28-track catalog at a tenth of a second. When his eras are in your ear, the main Song Guesser has every other artist, genre and decade ready to keep the streak alive.",
  "faq": [
   [
    "Why is the pool only 28 songs?",
    "His catalog is small but dense, so 28 tracks already covers the albums and the biggest singles. A compact pool keeps every round about recognizing each record's distinct texture."
   ],
   [
    "Are leaks and unreleased tracks included?",
    "No — the rotation sticks to officially released songs only, so every round is a track you could have heard on an album or mixtape."
   ],
   [
    "What gives his songs away fastest?",
    "The beat energy and the baby-voice ad-lib. His intros are minimal on purpose, so the first 808 or vocal catch usually names the record."
   ]
  ]
 },
 "bad-bunny": {
  "tips": "His sound bends reggaeton, trap and pop, so the first beat is a lane marker — a breezy dembow means the reggaeton hits, a darker synth means the trap records, a dreamy loop means the pop crossovers. Name the lane and the title follows.",
  "closing": "Bad Bunny Song Guesser spans the reggaeton, trap and pop of his 56-track catalog at a tenth of a second. When his lanes are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Do I need to know Spanish to play?",
    "No — you are matching audio to a title, not reading lyrics. If you know the beat, the language of the vocal does not matter for the guess."
   ],
   [
    "Are the feature-heavy records included?",
    "Yes — his biggest records are collaborations, so a guest voice often appears in the clip. The guess is always a Bad Bunny track."
   ],
   [
    "What is the strongest clue on his songs?",
    "The dembow pattern and the vocal bend. His intros are rhythmic first, so the first kick or synth line usually names the record before any words land."
   ]
  ]
 },
 "katy-perry": {
  "tips": "Her hits are hook-first, so the opening is the whole clue — a stadium chant means Roar, a candy-synth sparkle means the Teenage Dream era, a slinky trap beat means Dark Horse. Trust the first sound and reach for the chorus it belongs to.",
  "closing": "Katy Perry Song Guesser spans the candy-colored pop and the stadium anthems of her 59-track catalog at a tenth of a second. When her hooks are in your ear, the main Song Guesser opens every other artist, genre and decade on the site.",
  "faq": [
   [
    "Why is the pool 59 songs?",
    "It pulls the singles and the most recognizable album cuts across her whole career, weighted toward the songs people can actually place from an intro. The deepest b-sides are left out."
   ],
   [
    "Do the acoustic versions appear?",
    "No — the game uses the studio singles, so you hear the chart production rather than a stripped-back take. That keeps every intro consistent."
   ],
   [
    "What gives her songs away fastest?",
    "The chorus texture — her hits were built around a single unmistakable hook. A synth sparkle or a drum fill usually names the record before the verse starts."
   ]
  ]
 }
}

P2INTRO = {
 "the-weeknd": {
  "intro": "Every round is one question — how little of that neon synth do you actually need?",
  "p2": "The fun of a <a href=\"/\">song guesser</a> built on Abel Tesfaye's music is that his productions are instantly recognizable yet easy to confuse — “Save Your Tears” and “Blinding Lights” share a family resemblance until the second note tells them apart."
 },
 "taylor-swift": {
  "intro": "Work from the shortest clip outward, and let each reveal confirm or correct your first instinct.",
  "p2": "Because her eras sound nothing alike, this <a href=\"/\">song guesser</a> doubles as a tour through her whole career — a twang here, a synth there, and suddenly you are naming the album before the song."
 },
 "michael-jackson": {
  "intro": "Each round opens on a sliver and waits for your first call.",
  "p2": "Jackson's intros were built to stop a room, which makes them ideal for a <a href=\"/\">song guesser</a> — one beat or one breath is often all you need to separate “Billie Jean” from everything around it."
 },
 "beyonce": {
  "intro": "Start at the shortest clip and let the horns, the drums and the runs point the way.",
  "p2": "What makes this <a href=\"/\">song guesser</a> work is how much her arrangements changed over the years — a horn stab, a marching snare and a vocal run each belong to a different Beyoncé, and the opening usually tells you which one you are hearing."
 },
 "rihanna": {
  "intro": "Each round gives you a sliver and a single question: which Rihanna is this?",
  "p2": "Her catalog swings from dance-floor bangers to piano ballads, so this <a href=\"/\">song guesser</a> is really a test of how fast you can sort one era from another — the first beat is usually enough."
 },
 "drake": {
  "intro": "Work the sliver, then confirm against the era's mood and drums.",
  "p2": "Drake's sound kept shifting from moody to bouncy to island-smooth, so a <a href=\"/\">song guesser</a> built on him rewards anyone who knows which album each drum pattern belongs to."
 },
 "eminem": {
  "intro": "Each round opens on a sliver and asks you to name it before the bars arrive.",
  "p2": "Because his intros are famous in their own right, this <a href=\"/\">song guesser</a> leans on the beat and the breath — the vocal only confirms what the production already told you."
 },
 "kanye-west": {
  "intro": "Hear the sample, the drums or the 808, and place the era from that first sound.",
  "p2": "Kanye reinvented his sound on almost every album, so a <a href=\"/\">song guesser</a> built on him is as much a history quiz as a music game — the opening sound is a timestamp."
 },
 "justin-bieber": {
  "intro": "Start at the shortest clip and let the production name the era.",
  "p2": "His sound moved from teen pop to trop-house to soft R&B, so this <a href=\"/\">song guesser</a> rewards the fan who can hear which Bieber is which from the first strum or shaker."
 },
 "linkin-park": {
  "intro": "Each round opens on a sliver of keys, guitar or drums.",
  "p2": "Their whole identity is the blend of electronics and guitars, which makes a <a href=\"/\">song guesser</a> built on Linkin Park a test of how fast you can read that balance — a clean keyboard loop is a different era from a chugging riff."
 },
 "lady-gaga": {
  "intro": "Start from the shortest clip and let the synth, the piano or the drama guide you.",
  "p2": "Gaga's catalog jumps from club pop to jazz to stripped ballads, so this <a href=\"/\">song guesser</a> asks you to name the Gaga first — the first sound usually does it."
 },
 "bruno-mars": {
  "intro": "Each round opens on a sliver and lets the lead instrument do the talking.",
  "p2": "His music is built on live-band hooks — a horn, a strum or a doo-wop sway — so a <a href=\"/\">song guesser</a> made of Bruno Mars songs is really a test of how fast you can hear the band."
 },
 "adele": {
  "intro": "Work from the shortest clip and let the piano tell you which album you are in.",
  "p2": "Adele's four albums each carry their own weight and warmth, so this <a href=\"/\">song guesser</a> rewards the ear that can place the era — the tempo and the key usually name the record."
 },
 "ariana-grande": {
  "intro": "Start at the shortest clip and let the beat texture and the runs guide you.",
  "p2": "Her sound shifted from glossy pop to trap-lite R&B, so a <a href=\"/\">song guesser</a> built on Ariana Grande is a study in production — the hi-hat and the synth usually name the era before she does."
 },
 "billie-eilish": {
  "intro": "Each round opens on a whisper, a bass thump or a blown-out chorus.",
  "p2": "Because her records live in the low end and the breath, this <a href=\"/\">song guesser</a> is a test of how well you listen below the melody — the bass is the whole clue."
 },
 "ed-sheeran": {
  "intro": "Start from the shortest clip and let the loop do the identifying.",
  "p2": "His songs are built on single looped figures, so a <a href=\"/\">song guesser</a> made of Ed Sheeran tracks is really a rhythm test — the strum or the loop usually names the song."
 },
 "coldplay": {
  "intro": "Each round opens on an atmosphere — a piano, a string swell or a synth pad.",
  "p2": "Their sound moved from quiet rock to stadium-sized electronica, so this <a href=\"/\">song guesser</a> rewards the fan who can read the texture — the opening chord is the era's signature."
 },
 "bts": {
  "intro": "Start from the shortest clip and let the drop or the chant lead.",
  "p2": "Their discography blends K-pop, hip-hop and EDM, so a <a href=\"/\">song guesser</a> built on BTS is a test of how fast you can place the beat — a synth stab or a chant usually names the record."
 },
 "blackpink": {
  "intro": "Each round opens on a stomp, a drop or a chant.",
  "p2": "Their comebacks each came with a signature opening, which makes a <a href=\"/\">song guesser</a> built on BLACKPINK a sprint — the first half-second is usually the whole answer."
 },
 "gdragon": {
  "intro": "Start at the shortest clip and let the neon or the beat name the era.",
  "p2": "G-DRAGON's sound kept mutating album to album, so this <a href=\"/\">song guesser</a> is a map of his reinventions — the first synth or drum tells you which G-DRAGON you are dealing with."
 },
 "david-guetta": {
  "intro": "Each round opens on a chord, a stab or the start of a build.",
  "p2": "His records are built on the build and the drop, so a <a href=\"/\">song guesser</a> made of David Guetta tracks rewards the ear that knows a piano lift from a big-room synth."
 },
 "pitbull": {
  "intro": "Start at the shortest clip and let the horn or the shout lead.",
  "p2": "Pitbull's hits are built to start a party on beat one, so this <a href=\"/\">song guesser</a> is a test of how fast you can catch the horn — the first blast usually names the record."
 },
 "kendrick-lamar": {
  "intro": "Each round opens on a drum, a vocal bend or a beat switch.",
  "p2": "His albums each carry a distinct sonic stamp, so a <a href=\"/\">song guesser</a> built on Kendrick Lamar is a study in production — the first snare or sample usually names the era."
 },
 "olivia-rodrigo": {
  "intro": "Start from the shortest clip and let the piano or the guitar sort it.",
  "p2": "Her two modes are easy to hear — a lone piano is a ballad, a crunchy guitar is the punk — so this <a href=\"/\">song guesser</a> rewards the fan who trusts the first instrument."
 },
 "lana-del-rey": {
  "intro": "Each round opens on an atmosphere — strings, guitar or a dreamy synth.",
  "p2": "Her records live in mood more than melody, so a <a href=\"/\">song guesser</a> built on Lana Del Rey asks you to read the texture — the lead instrument usually names the era."
 },
 "maroon-5": {
  "intro": "Start from the shortest clip and let the riff or the synth name the era.",
  "p2": "Their sound drifted from rock to radio pop, so this <a href=\"/\">song guesser</a> rewards the fan who can hear which Maroon 5 is which — a funky guitar is a different era from a glossy synth."
 },
 "shakira": {
  "intro": "Each round opens on a rhythm — a trumpet, a flute or a percussion figure.",
  "p2": "Her catalog splits between Latin rock and global pop, so a <a href=\"/\">song guesser</a> built on Shakira is a test of the lead instrument — the first sound usually names the lane."
 },
 "travis-scott": {
  "intro": "Start at the shortest clip and let the 808 or the ad-lib name it.",
  "p2": "His sound is texture first — a pitched-down vocal, a woozy drone, a hard 808 — so this <a href=\"/\">song guesser</a> rewards the fan who can read the haze from the first hit."
 },
 "sabrina-carpenter": {
  "intro": "Each round opens on a bassline, a strum or a wink.",
  "p2": "Her hooks are sharp and immediate, so a <a href=\"/\">song guesser</a> built on Sabrina Carpenter is a sprint — the disco bassline or the playful vocal usually gives the whole thing away."
 },
 "anuel-aa": {
  "intro": "Start from the shortest clip and let the dembow or the rasp lead.",
  "p2": "His lane is the dembow and the street anthem, so this <a href=\"/\">song guesser</a> rewards the fan who can separate the reggaeton from the trap — the first kick usually does it."
 },
 "don-toliver": {
  "intro": "Each round opens on a synth wash, an 808 or a falsetto.",
  "p2": "His sound is wavy and melodic, so a <a href=\"/\">song guesser</a> built on Don Toliver asks you to read the haze — the swelling pad usually names the era."
 },
 "tate-mcrae": {
  "intro": "Start at the shortest clip and let the beat or the piano sort it.",
  "p2": "Her two modes split cleanly — a stomping beat is the dance pop, a sparse piano is the ballad — so this <a href=\"/\">song guesser</a> rewards the fan who trusts the first sound."
 },
 "playboi-carti": {
  "intro": "Each round opens on an 808, a synth or a baby-voice ad-lib.",
  "p2": "His eras are separated by energy — minimal bounce versus a wall of 808s — so a <a href=\"/\">song guesser</a> built on Playboi Carti is a test of how fast you can read that shift."
 },
 "bad-bunny": {
  "intro": "Start from the shortest clip and let the dembow or the vocal bend lead.",
  "p2": "His sound bends reggaeton, trap and pop, so this <a href=\"/\">song guesser</a> rewards the fan who can name the lane from the first beat — the dembow is the fastest tell."
 },
 "katy-perry": {
  "intro": "Each round opens on a hook — a chant, a sparkle or a slinky beat.",
  "p2": "Her hits were built around one unmistakable chorus, so a <a href=\"/\">song guesser</a> made of Katy Perry songs is a test of the opening — the synth sparkle or the drum fill usually names the record."
 }
}

STEPX = {
 "the-weeknd": {
  "t": [
   "Start on the sliver",
   "Name the track",
   "Reveal when stuck",
   "Play without limits"
  ],
  "b3": "Miss or skip and the clip opens to 0.5s, 2s, 8s, then the full 15s. Catching that neon synth on the first sliver is the whole flex."
 },
 "taylor-swift": {
  "t": [
   "Hear the opening tenth",
   "Type your guess",
   "Widen the clip",
   "Play every round"
  ],
  "b3": "Wrong guess? The reveal widens to 0.5s, 2s, 8s and 15s. The cleanest wins still name the era from the shortest clip."
 },
 "michael-jackson": {
  "t": [
   "Listen to beat one",
   "Put in the title",
   "Stretch if unsure",
   "No daily cap"
  ],
  "b3": "A wrong call stretches the clip to 0.5s, 2s, 8s, then 15s. The point is placing that beat or breath while it is still a tenth of a second."
 },
 "beyonce": {
  "t": [
   "Take the first sound",
   "Pick the song name",
   "Open more if stuck",
   "Keep going"
  ],
  "b3": "Miss and the clip grows to 0.5s, 2s, 8s, then 15s — but the round is at its cleanest when you name it off the opening sliver."
 },
 "rihanna": {
  "t": [
   "Catch the opening beat",
   "Enter the title",
   "Grow the clip",
   "Play on repeat"
  ],
  "b3": "Guess wrong and the clip steps to 0.5s, 2s, 8s, then 15s. Naming the era from the first beat is the cleanest round."
 },
 "drake": {
  "t": [
   "Open with the sliver",
   "Type the name",
   "Reveal if needed",
   "Endless rounds"
  ],
  "b3": "A miss or skip pushes the clip to 0.5s, 2s, 8s, then 15s. The earlier you call the era, the sharper the round."
 },
 "eminem": {
  "t": [
   "Hear the first breath",
   "Guess the title",
   "Widen when stuck",
   "No limit on rounds"
  ],
  "b3": "Wrong? The clip widens to 0.5s, 2s, 8s, then 15s. The beat and the breath should get you there well before the bars."
 },
 "kanye-west": {
  "t": [
   "Catch the opening sample",
   "Name the record",
   "Stretch the sample",
   "Play all night"
  ],
  "b3": "Skip and the clip stretches to 0.5s, 2s, 8s, then 15s. The goal is reading the sample on the shortest sliver."
 },
 "justin-bieber": {
  "t": [
   "Play the first instant",
   "Type it out",
   "Open up if stuck",
   "Rounds without end"
  ],
  "b3": "A wrong guess stretches the clip to 0.5s, 2s, 8s, then 15s. Naming the era from the opening strum is the point."
 },
 "linkin-park": {
  "t": [
   "Read the first note",
   "Enter your answer",
   "Reveal more",
   "Play as long as you want"
  ],
  "b3": "Miss and the reveal grows to 0.5s, 2s, 8s, then 15s. The cleanest play is reading the keys or the riff on the first sliver."
 },
 "lady-gaga": {
  "t": [
   "Take the opening stab",
   "Type the song",
   "Widen the reveal",
   "No caps here"
  ],
  "b3": "Wrong call and the clip widens to 0.5s, 2s, 8s, then 15s. Placing the synth or the piano while it is still a sliver is the goal."
 },
 "bruno-mars": {
  "t": [
   "Hear the first horn",
   "Name the single",
   "Stretch if stuck",
   "Play the whole catalog"
  ],
  "b3": "Skip and the clip steps to 0.5s, 2s, 8s, then 15s. Hearing the horn or the strum on the first sliver is the whole game."
 },
 "adele": {
  "t": [
   "Catch the first chord",
   "Put in your guess",
   "Open more",
   "Keep the run going"
  ],
  "b3": "A miss stretches the clip to 0.5s, 2s, 8s, then 15s. The warmest wins still name the record from the first chord."
 },
 "ariana-grande": {
  "t": [
   "Start on the hi-hat",
   "Type the title",
   "Reveal if stuck",
   "Unlimited rounds"
  ],
  "b3": "Guess wrong and the clip grows to 0.5s, 2s, 8s, then 15s. Placing the era from the hi-hat and the synth is the point."
 },
 "billie-eilish": {
  "t": [
   "Catch the first whisper",
   "Enter the name",
   "Grow the reveal",
   "Play with no ceiling"
  ],
  "b3": "Miss and the reveal widens to 0.5s, 2s, 8s, then 15s. The best rounds catch the bass or the whisper on the first sliver."
 },
 "ed-sheeran": {
  "t": [
   "Hear the opening loop",
   "Name the loop",
   "Widen when unsure",
   "Loop it forever"
  ],
  "b3": "Wrong? The clip steps to 0.5s, 2s, 8s, then 15s. Naming the loop while it is still a tenth of a second is the flex."
 },
 "coldplay": {
  "t": [
   "Take the first pad",
   "Type the song name",
   "Stretch the pad",
   "Play without end"
  ],
  "b3": "Skip and the clip stretches to 0.5s, 2s, 8s, then 15s. Reading the pad or the piano on the first sliver is the whole trick."
 },
 "bts": {
  "t": [
   "Catch the opening drop",
   "Pick the track",
   "Open the clip",
   "Go unlimited"
  ],
  "b3": "A wrong guess pushes the clip to 0.5s, 2s, 8s, then 15s. Placing the beat or the chant from the shortest clip is the point."
 },
 "blackpink": {
  "t": [
   "Hear the first stomp",
   "Type your answer",
   "Reveal when unsure",
   "Play every comeback"
  ],
  "b3": "Miss and the clip grows to 0.5s, 2s, 8s, then 15s. Catching the stomp or the drop on the first sliver is the cleanest round."
 },
 "gdragon": {
  "t": [
   "Read the opening neon",
   "Name the era",
   "Widen the sliver",
   "Rounds on demand"
  ],
  "b3": "Wrong call and the clip widens to 0.5s, 2s, 8s, then 15s. Naming the era from the opening neon is the whole game."
 },
 "david-guetta": {
  "t": [
   "Catch the first stab",
   "Enter the single",
   "Stretch the stab",
   "Play all sets"
  ],
  "b3": "Skip and the clip steps to 0.5s, 2s, 8s, then 15s. The best rounds catch the chord or the stab while it is still a sliver."
 },
 "pitbull": {
  "t": [
   "Hear the first blast",
   "Type the hit",
   "Open it up",
   "Party without limits"
  ],
  "b3": "A miss stretches the clip to 0.5s, 2s, 8s, then 15s. Naming it from the first horn blast is the cleanest win."
 },
 "kendrick-lamar": {
  "t": [
   "Take the opening snare",
   "Name the joint",
   "Reveal the verse",
   "Run it back"
  ],
  "b3": "Guess wrong and the clip grows to 0.5s, 2s, 8s, then 15s. Reading the snare or the sample on the shortest clip is the point."
 },
 "olivia-rodrigo": {
  "t": [
   "Catch the first strum",
   "Type the chorus",
   "Grow it if stuck",
   "Play through the catalog"
  ],
  "b3": "Miss and the reveal widens to 0.5s, 2s, 8s, then 15s. Placing the piano or the guitar while it is still a sliver is the flex."
 },
 "lana-del-rey": {
  "t": [
   "Read the opening mood",
   "Guess the record",
   "Widen the mood",
   "Play for as long as you like"
  ],
  "b3": "Wrong? The clip steps to 0.5s, 2s, 8s, then 15s. The cleanest rounds read the mood on the first sliver."
 },
 "maroon-5": {
  "t": [
   "Hear the first riff",
   "Put in the name",
   "Stretch the riff",
   "No round cap"
  ],
  "b3": "Skip and the clip stretches to 0.5s, 2s, 8s, then 15s. Naming the riff or the synth from the shortest clip is the goal."
 },
 "shakira": {
  "t": [
   "Catch the opening rhythm",
   "Type the riff",
   "Open the rhythm",
   "Play the full set"
  ],
  "b3": "A wrong guess pushes the clip to 0.5s, 2s, 8s, then 15s. Catching the trumpet or the flute on the first sliver is the trick."
 },
 "travis-scott": {
  "t": [
   "Read the first 808",
   "Enter the vibe",
   "Reveal more when stuck",
   "Rage without limits"
  ],
  "b3": "Miss and the clip grows to 0.5s, 2s, 8s, then 15s. Reading the 808 or the ad-lib on the shortest clip is the point."
 },
 "sabrina-carpenter": {
  "t": [
   "Hear the first bassline",
   "Name the hit",
   "Widen the bassline",
   "Play till you drop"
  ],
  "b3": "Guess wrong and the clip widens to 0.5s, 2s, 8s, then 15s. Naming it from the first bassline is the cleanest round."
 },
 "anuel-aa": {
  "t": [
   "Catch the opening kick",
   "Type the track",
   "Stretch the kick",
   "Play the full rotation"
  ],
  "b3": "A miss stretches the clip to 0.5s, 2s, 8s, then 15s. Placing the dembow or the rasp on the first sliver is the whole game."
 },
 "don-toliver": {
  "t": [
   "Hear the first pad",
   "Guess the single",
   "Open the pad",
   "No limit here"
  ],
  "b3": "Skip and the clip steps to 0.5s, 2s, 8s, then 15s. The best rounds read the pad on the first sliver."
 },
 "tate-mcrae": {
  "t": [
   "Take the opening beat",
   "Enter the track",
   "Grow the beat",
   "Play back to back"
  ],
  "b3": "Wrong call and the clip grows to 0.5s, 2s, 8s, then 15s. Naming it from the first beat or piano is the point."
 },
 "playboi-carti": {
  "t": [
   "Read the first synth",
   "Name the banger",
   "Widen the 808",
   "Rounds with no cap"
  ],
  "b3": "Miss and the reveal widens to 0.5s, 2s, 8s, then 15s. Catching the 808 or the ad-lib on the first sliver is the flex."
 },
 "bad-bunny": {
  "t": [
   "Catch the first dembow",
   "Name the tune",
   "Stretch the dembow",
   "Play every banger"
  ],
  "b3": "A wrong guess stretches the clip to 0.5s, 2s, 8s, then 15s. The goal is naming the lane from the shortest clip."
 },
 "katy-perry": {
  "t": [
   "Hear the opening sparkle",
   "Type the hook",
   "Open the hook",
   "Play all the hits"
  ],
  "b3": "Skip and the clip widens to 0.5s, 2s, 8s, then 15s. Naming it from the opening sparkle is the cleanest win."
 }
}

FAQFIX = {
 "anuel-aa": {
  "Do I need to know Spanish to play?": "Will I need to read the lyrics to score?",
  "What gives his songs away fastest?": "What is the fastest tell on an Anuel AA intro?"
 },
 "david-guetta": {
  "What gives his songs away fastest?": "Which part of a Guetta track gives it away first?"
 },
 "playboi-carti": {
  "What gives his songs away fastest?": "What separates one Carti intro from another?"
 },
 "bad-bunny": {
  "Do I need to know Spanish to play?": "Do I have to speak Spanish to guess correctly?",
  "What is the strongest clue on his songs?": "What gives a Bad Bunny track away first?"
 },
 "don-toliver": {
  "What is the strongest clue on his songs?": "Which sound is the best clue on a Don Toliver track?",
  "Why does Easy help casual fans here?": "Why is Easy the right place to start here?"
 },
 "kendrick-lamar": {
  "What is the strongest clue on his songs?": "What should you listen for first in a Kendrick intro?"
 },
 "billie-eilish": {
  "What trips players up on her songs?": "Which Billie songs are the hardest to place?"
 },
 "olivia-rodrigo": {
  "Do the acoustic versions appear?": "Do the acoustic takes show up in the game?",
  "What trips players up on her songs?": "Where do players get stuck the most?"
 },
 "tate-mcrae": {
  "What trips players up on her songs?": "What makes some Tate rounds trickier than others?"
 },
 "bruno-mars": {
  "What is the hardest thing to place here?": "Which Bruno Mars songs are hardest to name?"
 },
 "pitbull": {
  "What is the hardest thing to place here?": "Which Pitbull tracks are the toughest?"
 },
 "sabrina-carpenter": {
  "What is the hardest thing to place here?": "Which Sabrina tracks trip players up?"
 },
 "maroon-5": {
  "Why does Easy help casual fans here?": "Which difficulty should a casual fan begin on?"
 },
 "katy-perry": {
  "Do the acoustic versions appear?": "Are stripped-down versions part of the pool?"
 }
}

SUFFIX_NAME = {"kanye-west": "Kanye"}

for p in PAGES:
    p['title'] = p['name'] + ' Song Guesser - Guess the ' + SUFFIX_NAME.get(p['slug'], p['name']) + ' Song'
    p['h1'] = p['name'] + ' Song Guesser'
    write(p['slug'], build(p['slug'], p['name'], p['count'], p['title'], p['desc'], p['h1'], p['hero'], p['vgdesc'], p))
    print('WROTE', p['slug'])
print('DONE', len(PAGES))
