# -*- coding: utf-8 -*-
"""Generate the legal + info pages for songguesser.co — About, Privacy Policy, Terms of
Service and Contact. Structure follows the reference site (songspot.co: /about-us,
/privacy-policy, /terms-of-service) section by section, but every paragraph is original
and written to Song Guesser's actual reality (a free, accountless browser game on Vercel
with local-storage preferences, Google Fonts and optional advertising). Writes CRLF."""
import io, os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)

about = read(os.path.join(BASE, 'about', 'index.html'))

# --- clone chrome from about (header / footer / css / dropdown js) ---
cs = about.index('<style>') + len('<style>')
ce = about.index('</style>', cs)
css = about[cs:ce] + '\n.songspot-seo h1{color:#f7faf8;font-size:clamp(34px,4.2vw,60px);font-weight:700;letter-spacing:-.045em;line-height:1.06;margin-bottom:24px}\n.songspot-seo ul{margin:0 0 18px;padding-left:22px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo li{margin-bottom:8px}'

hs = about.index('<header class="songspot-site-header">')
he = about.index('</header>', hs) + len('</header>')
header = about[hs:he]

fs = about.index('<footer class="songspot-site-footer">')
fe = about.index('</footer>', fs) + len('</footer>')
footer = about[fs:fe]

m = about.index("document.querySelectorAll('.songspot-site-quiz-menu')")
djs = about.rfind('<script>', 0, m)
dje = about.index('</script>', m) + len('</script>')
dropdown_js = about[djs:dje]

footer_legal = footer.replace(
    '<div><p>Info</p><a href="/about/">About</a><a href="#features">Features</a><a href="#faq">FAQ</a></div>',
    '<div><p>Info</p><a href="/about/">About</a><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/contact/">Contact</a></div>')

TODAY = '13 October 2026'

# =====================================================================
# ABOUT — mirrors songspot.co/about-us section flow, original copy
# =====================================================================
ABOUT_BODY = '''<section class="songspot-seo">
  <section class="songspot-seo-section">
    <div class="songspot-seo-heading">
      <p class="songspot-seo-eyebrow">Last updated · ''' + TODAY + '''</p>
      <h1>About Song Guesser</h1>
    </div>
    <div class="songspot-seo-copy">
      <p>Song Guesser is a free browser game that plays you a sliver of a real song and asks you to name it. This page explains why we built it, how the rounds work, and what to do if a round does not behave the way it should.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>Hear less. Know more.</h2>
      <p>Song Guesser runs on a single question: how little of a song do you need before you know it? Every round opens with 0.1 seconds of audio — a drum hit, a breath, the attack of a chord — and you pick the correct title from four answers before the clip grows. Hear less, know more: the shorter the clip you beat, the deeper the track is filed in your memory.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>Why we built Song Guesser</h2>
      <p>There is a particular thrill in the instant before an answer lands — the half-second where the title is already in your head but not yet on the screen. We built Song Guesser to make that moment repeatable. No download, no mandatory account, and no one-song-a-day gate. Just clip after clip, whether you want a single round on a coffee break or a long session working through an artist's catalog.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>What makes it different</h2>
      <p><strong>A real 0.1-second start.</strong> The shortest clip is the whole point. Most quizzes open at a full second or more; ours opens ten times shorter, so the first sound has to carry the guess.</p>
      <p><strong>Four answers, no typing.</strong> Every round is A, B, C or D. There is no spelling and no search bar to fight — the choice is a tap, which keeps the game fast on a phone.</p>
      <p><strong>Unlimited rounds.</strong> There is no daily lockout and no score to protect. Play one round or a hundred in a row.</p>
      <p><strong>Difficulty and filters you control.</strong> Five difficulty lanes plus genre, decade and artist filters keep every round inside a pool of songs you actually know.</p>
      <p><strong>Browser-first, nothing to install.</strong> It runs in any modern browser on desktop or phone. No app, no signup, no download.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>Our product principles</h2>
      <h3>Keep the music at the center</h3>
      <p>The interface stays out of the way. A round is a play button, four titles and a timeline — everything else is secondary to listening, guessing and learning.</p>
      <h3>Make challenge settings meaningful</h3>
      <p>Difficulty changes how recognizable the opening sound is, not how obscure the song is. Filters let you explore the eras, genres and artists you care about, on your terms.</p>
      <h3>Respect players and rightsholders</h3>
      <p>We play short excerpts for a song-identification quiz. All music, artwork, names and trademarks belong to their owners, and Song Guesser is independent and unaffiliated with any artist, label or other guessing service unless we say otherwise.</p>
      <h3>Improve with real play</h3>
      <p>Catalog coverage, answer matching and clip behavior are refined continuously, guided by the songs people actually want to hear and the rounds that trip them up.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>How a round works</h2>
      <p>Press play and a 0.1-second clip plays once. Four titles appear. Pick one — if you are right, it lights up green and the round ends on the shortest clip. If you are wrong, the clip stretches to 0.5s, 2s, 8s, then 15s, so the answer arrives only when you need it. Set the difficulty from Easy to Impossible and filter by genre, decade or artist to keep each round in your lane.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>What goes into a collection</h2>
      <p>The catalog is organized into artist, genre and decade pools. Artist pages hold full catalogs, while genre and decade pools draw a curated slice of tracks. Counts reflect what is currently available and can overlap across pools, so a single track may appear in more than one collection — and a rare mismatch between the audio and its label is possible, so the reveal is always there to confirm what you heard.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>If a round does not work as expected</h2>
      <p>Press play once and wait for the clip to finish loading. Check your tab and device volume, and make sure audio is not routed to another Bluetooth device. If a title looks wrong or a track is mislabeled, email the page URL and the revealed song to support@songguesser.co so we can fix it. Never send passwords, cookies or tokens — there is no account to protect, and we will never ask for them.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>Privacy and access</h2>
      <p>The whole game works without an account. We collect only what is reasonably necessary to run it, and the details are set out in the <a href="/privacy-policy/">Privacy Policy</a> and <a href="/terms-of-service/">Terms of Service</a>.</p>
    </div>
  </section>

  <section class="songspot-seo-section">
    <div class="songspot-seo-copy">
      <h2>Contact</h2>
      <p>Questions, feedback and song suggestions go to <a href="mailto:support@songguesser.co">support@songguesser.co</a>.</p>
    </div>
  </section>
</section>'''

ABOUT_SCHEMA = ('{"@context":"https://schema.org","@type":"AboutPage","name":"About Song Guesser",'
                '"url":"https://www.songguesser.co/about/",'
                '"description":"Song Guesser is a free browser song guessing game built around a 0.1-second clip. Name the track from four answers before the clip grows, across artist, genre and decade pools.",'
                '"mainEntity":{"@type":"VideoGame","name":"Song Guesser","description":"A free song guessing game where you name a track from a 0.1-second clip, then reveal longer clips only when you are stuck.","applicationCategory":"Game","operatingSystem":"Web","url":"https://www.songguesser.co/","playMode":"SinglePlayer"}}')

# =====================================================================
# PRIVACY POLICY — mirrors songspot.co/privacy-policy, 12 sections, original
# =====================================================================
PRIVACY = [
    ('', [
        'This policy explains what information Song Guesser (songguesser.co) collects when you play, and what we do with it. The short version: the game has no account and no login, so there is no name, email or password to collect. You can play the entire game without telling us who you are.',
    ]),
    ('1. Scope', [
        'This policy applies to visitors to songguesser.co and to players of the free browser game. It covers the core game, which needs no account, and any optional feature we add later. If a feature changes the way data is handled, this policy will be updated to match.',
    ]),
    ('2. Information We Process', [
        '<strong>Game activity.</strong> Your difficulty choice, genre, decade and artist filters, clip stage, answers and skips are processed on your own device to run each round. Because there is no account, none of this is linked to an identity.',
        '<strong>Browser storage and cookies.</strong> The game keeps a few preferences — difficulty, filters, volume and your starting clip length — in your browser’s local storage, so they survive a refresh. This data never leaves your device, and we do not set first-party cookies.',
        '<strong>Technical and usage information.</strong> Our hosting provider may record standard technical data — IP address, browser and device type, timestamps and error signals — to keep the site secure and available.',
    ]),
    ('3. How We Use Information', [
        'We use the limited information above to deliver rounds, remember your preferences between visits, keep the site online and secure, and — where advertising is enabled — to serve ads.',
    ]),
    ('4. Third-Party Services', [
        '<strong>Google Fonts.</strong> The site loads its fonts from Google’s servers, which means Google may receive your IP address when a page loads.',
        '<strong>Hosting.</strong> Song Guesser is served by Vercel, which may keep standard server logs for security and reliability.',
        '<strong>Advertising.</strong> The site may display advertising served by third parties such as Google AdSense. These partners may use cookies, web beacons, IP addresses or device identifiers to serve and measure ads. You can opt out of personalised ads through Google’s Ads Settings (adssettings.google.com) or www.aboutads.info.',
    ]),
    ('5. Sharing and Disclosure', [
        'We do not sell personal information. We may disclose information only to the infrastructure and advertising providers above, or where required by law or to protect the safety and rights of the site and its users.',
    ]),
    ('6. Retention', [
        'Preferences in local storage remain on your device until you clear them in your browser. Any server logs are kept according to our hosting provider’s standard retention.',
    ]),
    ('7. Your Choices and Rights', [
        'Because we hold no account data, there is usually nothing to access or delete. You can clear your browser’s local storage at any time, block third-party cookies, and opt out of personalised ads. For any request, contact us and we will respond.',
    ]),
    ('8. Security', [
        'We use reasonable technical and organisational measures to protect the site, but no method of transmission or storage is completely secure, and we cannot guarantee absolute security.',
    ]),
    ('9. Children', [
        'Song Guesser is a general-audience music game and is not directed at children. We do not knowingly collect personal information from children. If you believe a child has provided personal information, contact us and we will delete it.',
    ]),
    ('10. International Processing', [
        'The site is served through infrastructure that may process information in other countries. Where required, appropriate safeguards are used.',
    ]),
    ('11. Changes to This Policy', [
        'We may update this policy from time to time. The “Last updated” date at the top shows the current version, and material changes will be noted in the service.',
    ]),
    ('12. Contact', [
        'Privacy questions and requests go to <a href="mailto:support@songguesser.co">support@songguesser.co</a>.',
    ]),
]

# =====================================================================
# TERMS OF SERVICE — mirrors songspot.co/terms-of-service, 15 sections, original
# =====================================================================
TERMS = [
    ('', [
        'These terms cover your use of Song Guesser (songguesser.co), a free browser game that plays you a short clip and asks you to name the song. By using the site you agree to these terms and to our <a href="/privacy-policy/">Privacy Policy</a>. If you do not agree, please do not use the site.',
    ]),
    ('1. Agreement', [
        'Using songguesser.co means you accept these Terms of Service together with the <a href="/privacy-policy/">Privacy Policy</a>. If you do not agree to either, do not use the site.',
    ]),
    ('2. The Service', [
        'Song Guesser plays short clips of real songs as clues to identify a track. A round starts at 0.1 seconds and offers four answers; features such as difficulty, filters and clip length may change, and tracks or features may be added or removed at any time. The game needs no account to play.',
    ]),
    ('3. Eligibility', [
        'You must be legally able to accept these terms in your location. If you cannot, a parent or guardian must accept them on your behalf.',
    ]),
    ('4. Accounts', [
        'Song Guesser requires no account, and there is no username, password or profile to create or protect. You are responsible for the device and browser you use to play.',
    ]),
    ('5. Subscriptions and Payments', [
        'Song Guesser is free. There is no paid tier, no subscription and no in-app purchase. If we ever introduce a paid feature, these terms will be updated to describe it before it takes effect.',
    ]),
    ('6. Acceptable Use', [
        'You agree not to misuse the site: no scraping, bots or automated abuse, no bypassing or disrupting the game, no probing or reverse engineering, and no unlawful use. You may not download, redistribute, record or commercially exploit the audio previews or metadata beyond what the rights holders allow.',
    ]),
    ('7. Music, Trademarks and Third-Party Content', [
        'All song titles, artist names, recordings, artwork and marks belong to their respective owners. Playing short audio excerpts for a song-identification quiz is not a claim of ownership and grants you no license to copy them. Song Guesser is independent and is not affiliated with, sponsored by, or endorsed by any artist, label, publisher, or any similar song-guessing service.',
    ]),
    ('8. Game Results and Fair Play', [
        'Matching, scores and difficulty are provided for entertainment only and may be affected by metadata, audio behaviour, networks or catalog changes. The game is not a gambling, wagering or prize competition.',
    ]),
    ('9. Service Availability', [
        'The game is provided “as is” and “as available”. We do not guarantee uninterrupted access, the continued availability of any track, or compatibility with every device, browser or region.',
    ]),
    ('10. Intellectual Property', [
        'The site’s interface, original text, branding and software are protected and belong to Song Guesser. You receive only a limited right to use the site for its intended purpose.',
    ]),
    ('11. Suspension and Termination', [
        'You may stop using the site at any time. We may suspend or terminate access for enforcement, safety, legal or discontinuation reasons.',
    ]),
    ('12. Disclaimers', [
        'The service is provided without warranties of any kind, express or implied, to the maximum extent permitted by law.',
    ]),
    ('13. Limitation of Liability', [
        'To the maximum extent permitted by law, Song Guesser is not liable for any indirect, incidental, special, consequential or punitive damages, or for lost data, profits or access, arising from your use of the site.',
    ]),
    ('14. Changes to These Terms', [
        'We may revise these terms from time to time. The “Last updated” date shows the current version, and continued use of the site after a change means you accept the revised terms.',
    ]),
    ('15. Contact', [
        'Questions about these terms go to <a href="mailto:support@songguesser.co">support@songguesser.co</a>.',
    ]),
]

CONTACT = [
    ('', [
        'Questions, bugs, song requests or a takedown request — here is how to reach us.',
    ]),
    ('Email', [
        'The fastest way to reach us is <a href="mailto:support@songguesser.co">support@songguesser.co</a>.',
    ]),
    ('What to Contact Us About', [
        '<strong>Feedback and bugs.</strong> If something breaks or a round behaves oddly, tell us what browser and device you were using.',
        '<strong>Song requests.</strong> If an artist or track you love is missing from the catalog, send it our way.',
        '<strong>Copyright and takedown.</strong> If you hold rights to a recording and want it handled differently, email the title and your rights information and we will act promptly.',
        '<strong>Privacy.</strong> Anything covered by our <a href="/privacy-policy/">Privacy Policy</a> — questions, requests or concerns.',
    ]),
    ('Response Time', [
        'We aim to reply within a few days. Takedown requests are reviewed in the order they arrive.',
    ]),
]

# =====================================================================
# render + write
# =====================================================================
def breadcrumb(name, slug):
    return ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},'
            '{"@type":"ListItem","position":2,"name":"%s","item":"https://www.songguesser.co/%s/"}]}' % (name, slug))

WEBSITE = '{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}'

CONTACT_SCHEMA = ('{"@context":"https://schema.org","@type":"ContactPage","name":"Contact Song Guesser",'
                  '"url":"https://www.songguesser.co/contact/",'
                  '"about":{"@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/"}}')

HEAD_TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@" />
<link rel="canonical" href="https://www.songguesser.co/@@SLUG@@/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<link rel="icon" type="image/png" sizes="512x512" href="/images/logo.png" />
<link rel="apple-touch-icon" href="/images/logo.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="@@TITLE@@" />
<meta property="og:description" content="@@OGDESC@@" />
<meta property="og:url" content="https://www.songguesser.co/@@SLUG@@/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="@@TITLE@@" />
<meta name="twitter:description" content="@@OGDESC@@" />
<meta property="og:image" content="https://www.songguesser.co/images/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:image" content="https://www.songguesser.co/images/og.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;1,700;1,800&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
@@CSS@@</style>
<script type="application/ld+json">
'''

def render_body(intro, sections):
    """intro: dict with eyebrow/h1; sections: list of (heading, [paras])."""
    parts = ['<section class="songspot-seo">\n']
    parts.append('  <section class="songspot-seo-section">\n    <div class="songspot-seo-heading">\n      <p class="songspot-seo-eyebrow">%s</p>\n      <h1>%s</h1>\n    </div>\n' % (intro['eyebrow'], intro['h1']))
    first_paras = sections[0][1]
    parts.append('    <div class="songspot-seo-copy">\n')
    for p in first_paras:
        parts.append('      <p>%s</p>\n' % p)
    parts.append('    </div>\n  </section>\n')
    for heading, paras in sections[1:]:
        parts.append('  <section class="songspot-seo-section">\n    <div class="songspot-seo-copy">\n      <h2>%s</h2>\n' % heading)
        for p in paras:
            parts.append('      <p>%s</p>\n' % p)
        parts.append('    </div>\n  </section>\n')
    parts.append('</section>\n')
    return ''.join(parts)

def build_page(slug, meta, body, extra_schema=None):
    head = (HEAD_TPL
            .replace('@@TITLE@@', meta['title'])
            .replace('@@DESC@@', meta['desc'])
            .replace('@@SLUG@@', slug)
            .replace('@@OGDESC@@', meta['og_desc'])
            .replace('@@CSS@@', css))
    out = [head, breadcrumb(meta['name'], slug), '\n</script>\n<script type="application/ld+json">\n', WEBSITE, '\n</script>\n']
    if extra_schema:
        out.append('<script type="application/ld+json">\n' + extra_schema + '\n</script>\n')
    out.append('</head>\n<body>\n\n')
    out.append(header)
    out.append('\n\n')
    out.append(body)
    out.append('\n')
    out.append(footer_legal)
    out.append('\n\n' + dropdown_js + '\n</body></html>\n')
    return ''.join(out)

# about (hand-built body, AboutPage schema)
about_meta = {
    'title': 'About Song Guesser — the Free Song Guessing Game',
    'desc': 'Why Song Guesser exists, how the 0.1-second song guessing game works, what makes it different, and how to contact us.',
    'og_desc': 'Why we built a free song guessing game around a 0.1-second clip, and how the rounds work.',
    'name': 'About',
}
write(os.path.join(BASE, 'about', 'index.html'), build_page('about', about_meta, ABOUT_BODY, ABOUT_SCHEMA))
print('wrote about/index.html')

# privacy / terms / contact (section model)
pages = [
    ('privacy-policy', {
        'title': 'Privacy Policy — Song Guesser',
        'desc': 'Song Guesser privacy policy — what data the free song guessing game does and does not collect, browser storage, third-party services and your rights.',
        'og_desc': 'The privacy policy for the free song guessing game — no account, no personal data, local-storage preferences, and how to reach us.',
        'name': 'Privacy Policy',
        'h1': 'Privacy Policy',
        'eyebrow': 'Last updated · %s' % TODAY,
    }, PRIVACY, None),
    ('terms-of-service', {
        'title': 'Terms of Service — Song Guesser',
        'desc': 'Song Guesser terms of service — the rules for using the free song guessing game, music and trademark ownership, disclaimers and liability.',
        'og_desc': 'The terms of service for the free song guessing game — acceptable use, music ownership, disclaimers and liability.',
        'name': 'Terms of Service',
        'h1': 'Terms of Service',
        'eyebrow': 'Last updated · %s' % TODAY,
    }, TERMS, None),
    ('contact', {
        'title': 'Contact — Song Guesser',
        'desc': 'Contact Song Guesser — reach us for bugs, feedback, song requests, copyright or takedown requests, and privacy questions.',
        'og_desc': 'How to contact Song Guesser — bugs, song requests, copyright and takedown requests, and privacy questions.',
        'name': 'Contact',
        'h1': 'Contact Song Guesser',
        'eyebrow': 'We read everything',
    }, CONTACT, CONTACT_SCHEMA),
]
for slug, meta, sections, extra in pages:
    body = render_body({'eyebrow': meta['eyebrow'], 'h1': meta['h1']}, sections)
    outdir = os.path.join(BASE, slug)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    write(os.path.join(outdir, 'index.html'), build_page(slug, meta, body, extra))
    print('wrote %s/index.html' % slug)

# --- add footer links site-wide (idempotent) ---
OLD_A = '<div><p>Info</p><a href="/about/">About</a><a href="#features">Features</a><a href="#faq">FAQ</a></div>'
NEW_A = '<div><p>Info</p><a href="/about/">About</a><a href="#features">Features</a><a href="#faq">FAQ</a><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/contact/">Contact</a></div>'
OLD_B = '<div><p>Info</p><a href="/about/">About</a><a href="/#features">Features</a><a href="/#faq">FAQ</a></div>'
NEW_B = '<div><p>Info</p><a href="/about/">About</a><a href="/#features">Features</a><a href="/#faq">FAQ</a><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/contact/">Contact</a></div>'

changed = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        s = read(p)
        if 'href="/privacy-policy/"' in s:
            continue
        s2 = s.replace(OLD_A, NEW_A).replace(OLD_B, NEW_B)
        if s2 != s:
            write(p, s2)
            changed += 1
print('footer links added to %d pages' % changed)

# --- sitemap entries (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
anchor = '<url><loc>https://www.songguesser.co/about/</loc>'
added = []
for slug in ('privacy-policy', 'terms-of-service', 'contact'):
    entry = '<url><loc>https://www.songguesser.co/%s/</loc><priority>0.3</priority></url>' % slug
    if ('/%s/' % slug) not in s:
        s = s.replace(anchor, entry + '\n  ' + anchor, 1)
        added.append(slug)
if added:
    write(sp, s)
    print('sitemap updated: %s' % ', '.join(added))
else:
    print('sitemap already has all compliance pages')
