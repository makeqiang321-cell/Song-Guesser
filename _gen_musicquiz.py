# -*- coding: utf-8 -*-
"""Build /music-quiz/ from index.html. Same songspot shell; swaps the search box for
four A/B/C/D option buttons, loads mcq.js, and writes a multiple-choice SEO section
with FAQPage + BreadcrumbList + WebSite."""
import io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://www.songguesser.co/"
PAGE = "music-quiz/"
URL = DOMAIN + PAGE


def js(s):
    return json.dumps(s, ensure_ascii=False)


FAQ = [
    ("How does the Music Quiz multiple choice work?",
     "You hear a 0.1-second clip of a song, then pick the right title from four answers labelled A, B, C and D. A wrong pick or Skip reveals a longer clip — 0.5s, 2s, 8s, then 15s — until you land the song or run out of clips."),
    ("Is the Music Quiz the same as the clip challenge?",
     "It is the same Heardle-style song guessing game with a different answer style. Instead of typing a song or artist, you choose from four options. The reveal ladder, the five difficulty levels and the genre, decade and artist filters are identical."),
    ("What happens when I pick a wrong answer?",
     "Nothing is lost. The clip grows to the next length and you try again with the remaining choices. There is no score and no penalty in this song guessing game — only the satisfaction of naming the song from the shortest clip you can."),
    ("Do I need to type anything?",
     "No. Every answer is one tap on A, B, C or D. The multiple choice song quiz is built for phones and quick rounds, so you never open a keyboard to play."),
    ("Can I filter the songs in Music Quiz?",
     "Yes. Pick a genre like Pop or Rock, a decade like the 1990s, or an artist like Taylor Swift, and every round draws its four choices from that pool until you change the setting."),
]


def build():
    h = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

    # hero copy
    h = h.replace(
        "Song Guesser plays a tenth of a second of a real song — that's your whole clue. You know it or you don't, and you type the title before the clip grows. It's a Heardle-style song guessing game, free in the browser: no app, no login, no daily limit, and the less audio you need, the better you're playing.",
        "Music Quiz is Song Guesser's multiple-choice mode: hear a 0.1-second clip of a real song, then pick the right title from four answers — A, B, C or D. No keyboard, no spelling, just your ear against four options. It's the same Heardle-style song guessing game, wrapped in a faster, tap-friendly format.",
    )
    h = h.replace(
        '<h1 id="songspot-heading">Song Guesser — Guess the Song in 0.1 Seconds</h1>',
        '<h1 id="songspot-heading">Music Quiz — Guess the Song from Four Choices</h1>',
    )

    # head meta
    h = h.replace(
        "<title>Song Guesser — Free Song Guessing Game | Guess the Song</title>",
        "<title>Music Quiz — Song Guessing Game | Guess the Song Title</title>",
    )
    h = h.replace(
        '<meta name="description" content="Song Guesser is a free Heardle-style song guessing game. Name the song from a 0.1-second clip, reveal more when stuck. Five levels, no app, no login." />',
        '<meta name="description" content="Play the Song Guesser Music Quiz: hear a 0.1-second clip and pick the right song from four answers. A/B/C/D multiple choice, five difficulties, no typing, no signup." />',
    )
    h = h.replace(
        '<link rel="canonical" href="https://www.songguesser.co/" />',
        '<link rel="canonical" href="' + URL + '" />',
    )
    h = h.replace(
        '<meta property="og:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
        '<meta property="og:title" content="Music Quiz — Song Guessing Game | Guess the Song Title" />',
    )
    h = h.replace(
        '<meta property="og:description" content="Name the song from a 0.1-second clip. A free Heardle-style song guessing game with five difficulty levels and unlimited rounds." />',
        '<meta property="og:description" content="Hear a 0.1-second clip and pick the song from four answers. A free Heardle-style multiple choice song quiz with five difficulties." />',
    )
    h = h.replace(
        '<meta property="og:url" content="https://www.songguesser.co/" />',
        '<meta property="og:url" content="' + URL + '" />',
    )
    h = h.replace(
        '<meta name="twitter:title" content="Song Guesser — Guess the Song in 0.1 Seconds" />',
        '<meta name="twitter:title" content="Music Quiz — Song Guessing Game | Guess the Song Title" />',
    )
    h = h.replace(
        '<meta name="twitter:description" content="Name the song from a 0.1-second clip. Free, no signup." />',
        '<meta name="twitter:description" content="Hear a 0.1-second clip, pick A, B, C or D. Free multiple choice song quiz, no signup." />',
    )

    # JSON-LD: FAQPage + BreadcrumbList + WebSite
    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ
        ],
    }
    crumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "Music Quiz", "item": URL},
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
        for b in (faq_json, crumb, site)
    )
    a = h.index('<script type="application/ld+json">')
    b = h.index('</head>')
    h = h[:a] + blocks + h[b:]

    # nav: Play inactive, Music Quiz active
    h = h.replace(
        '<a class="songspot-site-nav-link active" href="/">Play</a>',
        '<a class="songspot-site-nav-link" href="/">Play</a>',
    )
    h = h.replace(
        '<a class="songspot-site-nav-link" href="/music-quiz/">Music Quiz</a>',
        '<a class="songspot-site-nav-link active" href="/music-quiz/">Music Quiz</a>',
    )

    # swap search bar for A/B/C/D options + skip (index-slice so it fails loud if moved)
    i = h.index('<div class="songspot-search-bar">')
    j = h.index('<div class="songspot-answer-banner" id="answerBanner"></div>')
    mcq = ('<div class="songspot-mcq-options" id="mcqOptions" role="group" aria-label="Song choices"></div>\n'
           '          <button type="button" class="songspot-mcq-skip" id="skipBtn">\n'
           '            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4l10 8-10 8V4z" fill="currentColor" stroke="none"></path><path d="M19 5v14"></path></svg>\n'
           '            Skip\n'
           '          </button>\n'
           '          ')
    h = h[:i] + mcq + h[j:]

    # load mcq.js instead of game.js
    h = h.replace('<script src="/game.js?v=3"></script>',
                  '<script src="/mcq.js?v=1"></script>')

    # body: swap SEO section for multiple-choice article
    i = h.index('<section class="songspot-seo">')
    j = h.index('<footer class="songspot-site-footer">')
    h = h[:i] + article_html() + "\n\n" + h[j:]

    out = os.path.join(ROOT, "music-quiz", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(h)

    # sanity checks — fail loud on a missed swap
    assert 'id="mcqOptions"' in h and 'id="searchInput"' not in h, "search bar not swapped"
    assert '/mcq.js' in h and '/game.js' not in h, "script not swapped"
    assert 'Music Quiz' in h and 'music-quiz/' in h, "meta/nav not swapped"
    print("wrote", out, len(h), "bytes")


def article_html():
    out = ['<section class="songspot-seo">']

    out.append('''  <section id="music-quiz" class="songspot-seo-section songspot-seo-intro">
    <div class="songspot-seo-copy">
      <p class="songspot-seo-eyebrow">Multiple choice, no typing</p>
      <h2>What Is the Music Quiz?</h2>
      <p>The Music Quiz is Song Guesser's multiple-choice mode: hear a 0.1-second clip of a real song, then pick the right title from four answers — A, B, C or D. No keyboard, no spelling, just your ear against four options.</p>
      <p>It is the same Heardle-style song guessing game you know, in a faster, tap-friendly format. Guess the song from the shortest clip you can, and reveal more only when the four choices leave you stuck.</p>
    </div>
    <dl class="songspot-seo-stats">
      <div><dt>4</dt><dd>answers per round</dd></div>
      <div><dt>0.1s</dt><dd>the clip you start with</dd></div>
      <div><dt>5</dt><dd>reveal lengths up to 15s</dd></div>
    </dl>
  </section>''')

    out.append('''  <section class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Tap, don't type</p>
      <h2>How Multiple Choice Works</h2>
      <p>Every round follows the same four beats. Master the loop and the shortest clip is all you need.</p>
    </div>
    <div class="songspot-feature-grid">
      <article><span class="icon">▶</span><h3>Hear the clip</h3><p>Press play and a tenth of a second of a real song plays once. That tiny sliver is your only clue to start.</p></article>
      <article><span class="icon">A</span><h3>Pick A, B, C or D</h3><p>Four song titles appear — one is correct. Tap your answer and the right pick lights up green instantly.</p></article>
      <article><span class="icon">⏭</span><h3>Reveal only when stuck</h3><p>A wrong pick or Skip stretches the clip to 0.5s, 2s, 8s, then 15s, so the answer arrives only when you need it.</p></article>
      <article><span class="icon">🎚️</span><h3>Tune difficulty and filters</h3><p>Choose Easy to Impossible, and narrow the pool by genre, decade or artist so the four choices stay in your lane.</p></article>
    </div>
  </section>''')

    out.append('''  <section id="faq" class="songspot-seo-section songspot-seo-faq">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Before you tap</p>
      <h2>Music Quiz — FAQ</h2>
      <p>The answers that come up most before the first round.</p>
    </div>
    <div class="songspot-faq-list">''')
    first = True
    for q, a in FAQ:
        open_attr = ' open' if first else ''
        out.append('      <details%s><summary>%s</summary><p>%s</p></details>'
                   % (open_attr, q, a))
        first = False
    out.append('    </div>\n  </section>')

    out.append('''  <section class="songspot-seo-cta">
    <p class="songspot-seo-eyebrow">No typing, just listening</p>
    <h2>Ready to pick the right song from four choices?</h2>
    <p>Press play above and put the shortest clip to the test.</p>
    <a href="#play">Play the Music Quiz →</a>
    <a class="songspot-cta-home" href="/">Back to song guesser</a>
  </section>
</section>''')

    return "\n".join(out)


if __name__ == "__main__":
    build()
