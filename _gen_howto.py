# -*- coding: utf-8 -*-
"""Build /how-to-play/ from index.html. Keeps the playable game shell; swaps the SEO
section for a dedicated how-to article with HowTo + FAQPage + BreadcrumbList + WebSite."""
import io, json, re, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://www.songguesser.co/"
PAGE = "how-to-play/"
URL = DOMAIN + PAGE


def js(s):
    return json.dumps(s, ensure_ascii=False)


def build():
    h = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    # unique hero (drop shared homepage intro)
    h = h.replace(
        "<p>Song Guesser plays a tenth of a second of a real song — that's your whole clue. You know it or you don't, and you type the title before the clip grows. It's a Heardle-style song guessing game, free in the browser: no app, no login, no daily limit, and the less audio you need, the better you're playing.</p>",
        "<p>This is how to play the song guessing game: hear a 0.1-second clip and name the song before the reveal does the work.</p>",
    )

    # --- heading ---
    h = h.replace(
        '<h1 id="songspot-heading">Song Guesser — Guess the Song in 0.1 Seconds</h1>',
        '<h1 id="songspot-heading">How to Play Song Guesser — Guess the Song in 0.1 Seconds</h1>',
    )

    # --- head meta ---
    h = h.replace(
        "<title>Song Guesser — Free Song Guessing Game | Guess the Song</title>",
        "<title>How to Play Song Guesser — Guess the Song in 0.1 Seconds</title>",
    )
    h = h.replace(
        '<meta name="description" content="Song Guesser is a free Heardle-style song guessing game. Name the song from a 0.1-second clip, reveal more when stuck. Five levels, no app, no login." />',
        '<meta name="description" content="Learn how to play Song Guesser: hear a 0.1-second clip, type the title, reveal more only when stuck. Full rules, tips and difficulty guide." />',
    )
    h = h.replace(
        '<link rel="canonical" href="https://www.songguesser.co/" />',
        '<link rel="canonical" href="' + URL + '" />',
    )
    h = h.replace(
        '<meta property="og:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
        '<meta property="og:title" content="How to Play Song Guesser — Guess the Song in 0.1 Seconds" />',
    )
    h = h.replace(
        '<meta property="og:description" content="Name the song from a 0.1-second clip. A free Heardle-style song guessing game with five difficulty levels and unlimited rounds." />',
        '<meta property="og:description" content="A one-minute guide to the 0.1-second song guessing game: how clips reveal, how to answer, and how to tune the difficulty." />',
    )
    h = h.replace(
        '<meta property="og:url" content="https://www.songguesser.co/" />',
        '<meta property="og:url" content="' + URL + '" />',
    )
    h = h.replace(
        '<meta name="twitter:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
        '<meta name="twitter:title" content="How to Play Song Guesser — Guess the Song in 0.1 Seconds" />',
    )
    h = h.replace(
        '<meta name="twitter:description" content="Name the song from a 0.1-second clip. Free, no signup." />',
        '<meta name="twitter:description" content="How to play the 0.1-second song guessing game — rules, reveal ladder and difficulty guide." />',
    )

    # --- JSON-LD: replace 3 homepage blocks with 4 ---
    steps = [
        ("Press play to hear 0.1 seconds",
         "The round opens on a tenth-of-a-second sliver of a track. Put on headphones and listen for one signature — a drum fill, a vocal breath, a synth stab, a producer's signature — before the clip grows."),
        ("Type the song title",
         "Start typing any part of the title and pick the match from the suggestions. If a rhythm or melody rings a bell, commit to the name now; naming it from the shortest clip is the goal."),
        ("Reveal more audio only when stuck",
         "A wrong answer or a Skip stretches the clip to 0.5s, then 2s, 8s and 15s. Each step costs you the bragging point of a short clip, so reveal only when you have no guess left."),
        ("Set your difficulty and filters",
         "Choose from Easy, Medium, Hard, Expert and Impossible, and narrow the feed to a genre or an artist you know cold. The next round loads with those settings."),
        ("Start a new round and repeat",
         "There is no daily cap. Play solo, race a friend, or run round after round to train your ear until the shortest clip is all you need."),
    ]
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to Play Song Guesser",
        "description": "Name a song from a 0.1-second clip, then reveal longer clips only when you are stuck. A free browser song guessing game with five difficulty levels.",
        "url": URL,
        "totalTime": "PT1M",
        "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t}
                 for i, (n, t) in enumerate(steps)],
    }
    faq = [
        ("What do the reveal lengths 0.1s to 15s mean?",
         "They are the five clip sizes the song guessing game uses. A round starts at 0.1s and only steps up to 0.5s, 2s, 8s and 15s when you skip or answer wrong."),
        ("Do I lose anything for using a longer clip?",
         "Nothing is tracked and there is no score in this song guessing game. The only thing a longer clip costs is the satisfaction of naming the song from the shortest clip you can."),
        ("How do the difficulty levels change the game?",
         "The five levels change how recognizable the opening sound is and how long you get before the reveal. Easy to Impossible, each step of the song guessing game asks for a finer ear."),
        ("Can I filter which songs I get?",
         "Yes. Pick a genre like Pop or Rock, or a specific artist, and every round draws from that pool until you change the setting."),
        ("Is there a daily limit?",
         "No. Song Guesser is free in the browser with no signup, no download and no cap, so you can play this song guessing game for as many rounds as you like."),
    ]
    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }
    crumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "How to Play", "item": URL},
        ],
    }
    site = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Song Guesser",
        "url": DOMAIN,
        "potentialAction": {"@type": "SearchAction",
                            "target": DOMAIN + "?q={search_term_string}",
                            "query-input": "required name=search_term_string"},
    }
    blocks = "".join(
        '<script type="application/ld+json">\n' + js(b) + "\n</script>\n"
        for b in (howto, faq_json, crumb, site)
    )
    # replace the 3 homepage JSON-LD blocks (first <script> .. </head>) wholesale
    a = h.index('<script type="application/ld+json">')
    b = h.index('</head>')
    h = h[:a] + blocks + h[b:]

    # --- nav: Play inactive, How to Play active + point at this page ---
    h = h.replace(
        '<a class="songspot-site-nav-link active" href="/">Play</a>',
        '<a class="songspot-site-nav-link" href="/">Play</a>',
    )
    h = h.replace(
        '<a class="songspot-site-nav-link" href="/how-to-play/">How to Play</a>',
        '<a class="songspot-site-nav-link active" href="/how-to-play/">How to Play</a>',
    )
    # footer how-to-play link
    h = h.replace('<a href="#how-to-play">How to Play</a>',
                  '<a href="/how-to-play/">How to Play</a>')

    # --- body: swap SEO section for how-to article ---
    i = h.index('<section class="songspot-seo">')
    j = h.index('<footer class="songspot-site-footer">')
    h = h[:i] + article_html() + "\n\n" + h[j:]

    out = os.path.join(ROOT, "how-to-play", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(h)
    print("wrote", out, len(h), "bytes")


def article_html():
    steps = [
        ("01", "▶", "Press play",
         "The round starts the moment you hit the play key. A tenth of a second of audio plays once — and that is all you get to start."),
        ("02", "⌕", "Hear a signature",
         "Close your eyes and listen for one detail: a snare pattern, a breath at the top of a vocal, a bass slide. One detail is often enough to place the track."),
        ("03", "⏭", "Type the title",
         "Start typing any part of the song name and pick the match from the suggestions. Commit to it — a short clip answer is the win."),
        ("04", "↻", "Reveal only when stuck",
         "No guess? Skip or answer wrong and the clip grows to 0.5s, 2s, 8s and 15s. Longer clips make it easier, so reveal only when you have to."),
        ("05", "🎚️", "Tune the difficulty",
         "Pick Easy through Impossible, and filter by genre or artist. The next round loads your settings so you can drill exactly what you want to learn."),
        ("06", "♾️", "Go again",
         "There is no daily limit and no account. It never runs out, so chain rounds back to back and watch how much less audio you need as your ear sharpens."),
    ]
    tips = [
        ("🎧", "Headphones first", "The shortest clips are buried in reverb and low end. Headphones pull out a drum fill or a breath that speakers swallow."),
        ("🎯", "Know your lane", "Filter to an artist or genre you know cold, then widen out. You train faster when every guess is one you can check."),
        ("🧠", "Trust the production", "A hi-hat pattern, a chord voicing or a mixing quirk names a producer faster than a melody names a song."),
        ("⚡", "Answer early", "The whole skill is confidence at 0.1s. If it sounds right, type it — second-guessing is what costs you the clip."),
        ("📻", "Play the intro", "Tracks open on their very first sound. Hum the intro of a song you love and the game starts to feel easy."),
        ("🔁", "Repeat the ones you miss", "Miss a title? Note it and play that artist again next round. Here, recognition beats memory every time."),
    ]
    faq = [
        ("What do the reveal lengths 0.1s to 15s mean?",
         "They are the five clip sizes the song guessing game uses. A round starts at 0.1s and only steps up to 0.5s, 2s, 8s and 15s when you skip or answer wrong."),
        ("Do I lose anything for using a longer clip?",
         "Nothing is tracked and there is no score in this song guessing game. The only thing a longer clip costs is the satisfaction of naming the song from the shortest clip you can."),
        ("How do the difficulty levels change the game?",
         "The five levels change how recognizable the opening sound is and how long you get before the reveal. Easy to Impossible, each step of the song guessing game asks for a finer ear."),
        ("Can I filter which songs I get?",
         "Yes. Pick a genre like Pop or Rock, or a specific artist, and every round draws from that pool until you change the setting."),
        ("Is there a daily limit?",
         "No. Song Guesser is free in the browser with no signup, no download and no cap, so you can play this song guessing game for as many rounds as you like."),
    ]
    out = ['<section class="songspot-seo">']

    out.append('''  <section id="how-to-play" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">The rules take one minute</p>
      <h2>How to Play Song Guesser</h2>
      <p>Every round is the same tiny puzzle: a 0.1-second sliver of a real song plays, and you name the track before the clip gives away more. It is a Heardle-style song guessing game — guess the song from the shortest clip you can — except the opener is a tenth of a second, not a full one.</p>
      <p>The game never forces a longer clip on you. It stays at 0.1s until you ask for more. That one decision — answer now, or reveal more — is the entire game.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>5</dt><dd>reveal lengths from 0.1s to 15s</dd></div>
      <div><dt>6</dt><dd>steps from play to round over</dd></div>
    </dl>
  </section>''')

    out.append('''  <section class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Six steps, start to finish</p>
      <h2>The Round, Step by Step</h2>
      <p>Follow these in order the first time through. After two or three rounds, the loop runs itself.</p>
    </div>
    <ol class="songspot-how-grid">''')
    for n, icon, title, body in steps:
        out.append(
            '      <li><span>%s</span><span class="icon">%s</span><h3>%s</h3><p>%s</p></li>'
            % (n, icon, title, body)
        )
    out.append('    </ol>\n  </section>')

    out.append('''  <section id="tips" class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Get good faster</p>
      <h2>Tips to Name It Sooner</h2>
      <p>These habits close the gap between hearing 0.1s and naming the track.</p>
    </div>
    <div class="songspot-feature-grid">''')
    for icon, title, body in tips:
        out.append(
            '      <article><span class="icon">%s</span><h3>%s</h3><p>%s</p></article>'
            % (icon, title, body)
        )
    out.append('    </div>\n  </section>')

    out.append('''  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Before you press play</p>
      <h2>How to Play — FAQ</h2>
      <p>The details that come up most before your first round.</p>
    </div>
    <div class="songspot-faq-list">''')
    first = True
    for q, a in faq:
        open_attr = ' open' if first else ''
        out.append('      <details%s><summary>%s</summary><p>%s</p></details>'
                   % (open_attr, q, a))
        first = False
    out.append('    </div>\n  </section>')

    out.append('''  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">You know the rules now</p>
    <h2>Ready to name a song from 0.1 seconds?</h2>
    <p>Press play above and put the shortest clip to the test.</p>
    <a href="#play">Play Song Guesser →</a>
    <a class="songspot-cta-home" href="/">Back to song guesser</a>
  </section>
</section>''')

    return "\n".join(out)


if __name__ == "__main__":
    build()
