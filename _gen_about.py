# -*- coding: utf-8 -*-
"""Build /about/ from index.html. Keeps the playable game shell; swaps the SEO section
for a brand page with AboutPage + FAQPage + BreadcrumbList + WebSite."""
import io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://www.songguesser.co/"
PAGE = "about/"
URL = DOMAIN + PAGE


def js(s):
    return json.dumps(s, ensure_ascii=False)


def build():
    h = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    # unique hero (drop shared homepage intro)
    h = h.replace(
        "<p>Song Guesser plays a tenth of a second of a real song — that's your whole clue. You know it or you don't, and you type the title before the clip grows. It's a Heardle-style song guessing game, free in the browser: no app, no login, no daily limit, and the less audio you need, the better you're playing.</p>",
        "<p>About the game behind the guesser: how a tenth-of-a-second clip of any song became the whole quiz.</p>",
    )

    h = h.replace(
        "<title>Song Guesser — Free Song Guessing Game | Guess the Song</title>",
        "<title>About Song Guesser — the Free Song Guessing Game</title>",
    )
    h = h.replace(
        '<meta name="description" content="Song Guesser is a free Heardle-style song guessing game. Name a song from a 0.1-second clip, then reveal 0.5s, 2s, 8s, 15s when you need more. Five difficulty levels, no app, no login." />',
        '<meta name="description" content="About Song Guesser: why we built a free song guessing game around a 0.1-second clip, and how 35 artist catalogs, 8 genres and 5 decades power every round." />',
    )
    h = h.replace(
        '<link rel="canonical" href="https://www.songguesser.co/" />',
        '<link rel="canonical" href="' + URL + '" />',
    )
    h = h.replace(
        '<meta property="og:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
        '<meta property="og:title" content="About Song Guesser — the Free Song Guessing Game" />',
    )
    h = h.replace(
        '<meta property="og:description" content="Name the song from a 0.1-second clip. A free Heardle-style song guessing game with five difficulty levels and unlimited rounds." />',
        '<meta property="og:description" content="The story behind the 0.1-second song guessing game — why the shortest clip makes the best quiz, and what powers the catalog." />',
    )
    h = h.replace(
        '<meta property="og:url" content="https://www.songguesser.co/" />',
        '<meta property="og:url" content="' + URL + '" />',
    )
    h = h.replace(
        '<meta name="twitter:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
        '<meta name="twitter:title" content="About Song Guesser — the Free Song Guessing Game" />',
    )
    h = h.replace(
        '<meta name="twitter:description" content="Name the song from a 0.1-second clip. Free, no signup." />',
        '<meta name="twitter:description" content="Why we built a free song guessing game around a 0.1-second clip." />',
    )

    # JSON-LD: swap 3 homepage blocks for 4
    about = {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "About Song Guesser",
        "url": URL,
        "description": "Song Guesser is a free browser song guessing game built around a 0.1-second clip. Name the track from the shortest audio you can, across 35 artist catalogs, 8 genres and 5 decades.",
        "mainEntity": {
            "@type": "VideoGame",
            "name": "Song Guesser",
            "description": "A free song guessing game where you name a track from a 0.1-second clip, then reveal longer clips only when you are stuck.",
            "applicationCategory": "Game",
            "operatingSystem": "Web",
            "url": DOMAIN,
            "playMode": "SinglePlayer",
        },
    }
    faq = [
        ("Is Song Guesser really free?",
         "Yes, completely. It is a free song guessing game in the browser with no paywall, no signup and no daily cap, so you can play as many rounds as you like."),
        ("Do I need an account to play?",
         "No. There is no account, no app and no download. Open the page on a phone or computer, press play and the next round starts."),
        ("How many songs are in the game?",
         "The catalog holds 413 tracks across 35 artist pages, plus genre pools of 96 songs and decade pools of 60 songs, so no two rounds have to feel the same."),
        ("Is there a score or a leaderboard?",
         "No. There is no score, no ranking and no streak to protect. The only goal is naming the song from the shortest clip you can."),
        ("Who is Song Guesser for?",
         "Anyone who has ever recognized a song in an instant. Casual fans and obsessive listeners both fit, because the difficulty dial runs from Easy to Impossible."),
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
            {"@type": "ListItem", "position": 2, "name": "About", "item": URL},
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
        for b in (about, faq_json, crumb, site)
    )
    a = h.index('<script type="application/ld+json">')
    b = h.index('</head>')
    h = h[:a] + blocks + h[b:]

    # nav: no active link (About is not a nav item), Play becomes inactive
    h = h.replace(
        '<a class="songspot-site-nav-link active" href="/">Play</a>',
        '<a class="songspot-site-nav-link" href="/">Play</a>',
    )

    # body: swap SEO section for the about article
    i = h.index('<section class="songspot-seo">')
    j = h.index('<footer class="songspot-site-footer">')
    h = h[:i] + article_html() + "\n\n" + h[j:]

    out = os.path.join(ROOT, "about", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(h)
    print("wrote", out, len(h), "bytes")


def article_html():
    features = [
        ("▶", "The opening is the test",
         "A round starts at 0.1 seconds and only grows to 0.5s, 2s, 8s and 15s when you ask for more. The shortest clip is the whole point."),
        ("🎚️", "Five difficulty settings",
         "Easy through Impossible changes how recognizable the opening sound is, so the game stays honest for a first-timer and a superfan alike."),
        ("🎛️", "Forty-eight pools to drill",
         "Pick from 35 artist catalogs, 8 genres and 5 decades. Narrow the feed to a lane you know, or shuffle everything at once."),
        ("💿", "A catalog of real songs",
         "413 artist tracks plus genre and decade pools of 96 and 60 songs keep the game fresh long after the singles feel too easy."),
        ("🌐", "Nothing to install",
         "It runs in any modern browser on desktop or phone. No signup, no download, no account to remember."),
        ("♾️", "Play as long as you like",
         "There is no daily limit and no streak to protect. Play one round on a coffee break or run twenty back to back."),
    ]
    faq = [
        ("Is Song Guesser really free?",
         "Yes, completely. It is a free song guessing game in the browser with no paywall, no signup and no daily cap, so you can play as many rounds as you like."),
        ("Do I need an account to play?",
         "No. There is no account, no app and no download. Open the page on a phone or computer, press play and the next round starts."),
        ("How many songs are in the game?",
         "The catalog holds 413 tracks across 35 artist pages, plus genre pools of 96 songs and decade pools of 60 songs, so no two rounds have to feel the same."),
        ("Is there a score or a leaderboard?",
         "No. There is no score, no ranking and no streak to protect. The only goal is naming the song from the shortest clip you can."),
        ("Who is Song Guesser for?",
         "Anyone who has ever recognized a song in an instant. Casual fans and obsessive listeners both fit, because the difficulty dial runs from Easy to Impossible."),
    ]
    out = ['<section class="songspot-seo">']

    out.append('''  <section class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">Why a tenth of a second</p>
      <h2>About Song Guesser</h2>
      <p>Song Guesser started with a question: how little of a song do you need before you can name it? The answer turned out to be almost nothing — a drum fill, a breath before the vocal, a single synth stab — and the smaller the clip, the better the game. We built it as a Heardle-style song guessing game, but sharper than a full second — the opener is a tenth-of-a-second sliver of audio.</p>
      <p>That is the whole idea: a free song guessing game with no signup, no download, no daily cap. You press play, hear 0.1 seconds of a track, and type the title before the reveal does the work for you.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>0.1s</dt><dd>the clip that opens every round</dd></div>
      <div><dt>48</dt><dd>playable pools across artists, genres and decades</dd></div>
      <div><dt>5</dt><dd>difficulty levels from Easy to Impossible</dd></div>
    </dl>
  </section>''')

    out.append('''  <section class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">What makes it tick</p>
      <h2>The Game Behind the Brand</h2>
      <p>Everything in the game serves one goal: name the song from as little audio as possible.</p>
    </div>
    <div class="songspot-feature-grid">''')
    for icon, title, body in features:
        out.append(
            '      <article><span class="icon">%s</span><h3>%s</h3><p>%s</p></article>'
            % (icon, title, body)
        )
    out.append('    </div>\n  </section>')

    out.append('''  <section class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">The catalog, in three lanes</p>
      <h2>How the Music Is Organized</h2>
      <p>Every round draws from a pool you choose. Open one of the three hubs to browse the whole catalog, or jump straight to the <a href="/">song guesser</a> and start playing.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">🎧</span><h3><a href="/song-guesser-artists/">Artists</a></h3><p>35 catalogs from Taylor Swift to Bad Bunny, each its own game built on one voice.</p></article>
      <article><span class="icon">🎸</span><h3><a href="/guessable-songs/">Genres</a></h3><p>8 styles — Pop, Rock, Hip-Hop, R&amp;B, K-Pop, Electronic, Country, Metal.</p></article>
      <article><span class="icon">📼</span><h3><a href="/guess-song-decades/">Decades</a></h3><p>5 eras from the 1980s to the 2020s, so the sound of any year is in reach.</p></article>
    </div>
  </section>''')

    out.append('''  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Quick answers</p>
      <h2>About Song Guesser — FAQ</h2>
      <p>The questions that come up before the first clip.</p>
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
    <p class="songspot-seo-eyebrow">The catalog is already here</p>
    <h2>Ready to hear how little you need?</h2>
    <p>Press play and guess the song from 0.1 seconds.</p>
    <a href="#play">Play Song Guesser →</a>
    <a class="songspot-cta-home" href="/">song guesser</a>
  </section>
</section>''')

    return "\n".join(out)


if __name__ == "__main__":
    build()
