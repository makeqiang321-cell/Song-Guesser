# -*- coding: utf-8 -*-
"""Generate the compliance pages for songguesser.co — Privacy Policy, Terms of Service
and Contact — plus add footer links site-wide. Follows the section structure of the
reference site (songspot.co: /privacy-policy, /terms-of-service) but the copy is original
and written to songguesser's actual reality (no accounts, no premium, no Stripe, no live
rooms — a free static game on Vercel with local-storage preferences and Google Fonts).
Writes CRLF to match core.autocrlf=true."""
import io, os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)

about = read(os.path.join(BASE, 'about', 'index.html'))

# --- clone chrome from about (a content page, no game shell needed) ---
cs = about.index('<style>') + len('<style>')
ce = about.index('</style>', cs)
css = about[cs:ce] + '\n.songspot-seo h1{color:#f7faf8;font-size:clamp(34px,4.2vw,60px);font-weight:700;letter-spacing:-.045em;line-height:1.06;margin-bottom:24px}'

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

# footer Info column for the new pages (no #features/#faq anchors exist on them)
footer_legal = footer.replace(
    '<div><p>Info</p><a href="/about/">About</a><a href="#features">Features</a><a href="#faq">FAQ</a></div>',
    '<div><p>Info</p><a href="/about/">About</a><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/contact/">Contact</a></div>')

TODAY = '13 October 2026'

PAGES = [
    {
        'slug': 'privacy-policy',
        'title': 'Privacy Policy — Song Guesser',
        'desc': 'Song Guesser privacy policy — what data the free song guessing game does and does not collect, how your browser stores preferences, and how to contact us.',
        'og_desc': 'The privacy policy for the free song guessing game — no account, no personal data, local-storage preferences, and how to reach us.',
        'h1': 'Privacy Policy',
        'eyebrow': 'Last updated · %s' % TODAY,
        'name': 'Privacy Policy',
        'contact_schema': False,
        'sections': [
            ('', [
                'This policy explains what information Song Guesser (songguesser.co) collects when you play, and what we do with it. The short version: the game has no account and no login, so there is no name, email or password to collect.',
            ]),
            ('1. Scope', [
                'This policy applies to visitors to songguesser.co and players of the free browser game. You can play every round without creating an account, installing anything or paying anything.',
            ]),
            ('2. Information We Process', [
                '<strong>Game activity.</strong> The round itself runs in your browser. Your difficulty choice, genre, decade and artist filters, clip stage and answers are processed on your device to serve the round — none of it is tied to an account, because there is no account.',
                '<strong>Browser storage.</strong> The game remembers a few preferences — difficulty, filters, volume and your starting clip length — in your browser’s local storage. This stays on your device and is never sent to our servers. We do not set first-party cookies.',
                '<strong>Technical and usage information.</strong> Our hosting provider may keep standard server logs (such as IP address, browser type and timestamps) to keep the site secure and available.',
            ]),
            ('3. How We Use Information', [
                'We use the limited information above to deliver the game, remember your preferences between visits, keep the site online and secure, and — where advertising is enabled — serve ads.',
            ]),
            ('4. Third-Party Services', [
                '<strong>Google Fonts.</strong> The site loads its fonts from Google’s servers, which means Google may receive your IP address when a page loads.',
                '<strong>Hosting.</strong> Song Guesser is served by Vercel, which may process standard server logs for security and reliability.',
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
                'We use reasonable measures to protect the site, but no method of transmission or storage is completely secure, and we cannot guarantee absolute security.',
            ]),
            ('9. Children', [
                'Song Guesser is a general-audience music game and is not directed at children. We do not knowingly collect personal information from children. If you believe a child has provided personal information, contact us and we will delete it.',
            ]),
            ('10. Changes to This Policy', [
                'We may update this policy from time to time. The “Last updated” date at the top shows the current version, and material changes will be noted here.',
            ]),
            ('11. Contact', [
                'Privacy questions and requests go to <a href="mailto:support@songguesser.co">support@songguesser.co</a>.',
            ]),
        ],
    },
    {
        'slug': 'terms-of-service',
        'title': 'Terms of Service — Song Guesser',
        'desc': 'Song Guesser terms of service — the rules for using the free song guessing game, music and trademark ownership, and the limits of liability.',
        'og_desc': 'The terms of service for the free song guessing game — acceptable use, music ownership, disclaimers and liability.',
        'h1': 'Terms of Service',
        'eyebrow': 'Last updated · %s' % TODAY,
        'name': 'Terms of Service',
        'contact_schema': False,
        'sections': [
            ('', [
                'These terms cover your use of Song Guesser (songguesser.co), a free browser game that plays you a short clip and asks you to name the song. By using the site you agree to these terms and to our <a href="/privacy-policy/">Privacy Policy</a>. If you do not agree, please do not use the site.',
            ]),
            ('1. The Service', [
                'Song Guesser is a free online song guessing game. Each round plays a short clip of a real song — starting at 0.1 seconds — and you try to name it from four answers before the clip grows. No account, download or payment is required. Features and tracks may change or be removed at any time.',
            ]),
            ('2. Eligibility', [
                'You must be legally able to agree to these terms in your location. If you cannot, a parent or guardian must accept them on your behalf.',
            ]),
            ('3. Acceptable Use', [
                'You agree not to misuse the site: no scraping, bots or automated abuse, no bypassing or disrupting the game, no probing or reverse engineering, and no unlawful use. You may not download, redistribute, record or commercially exploit the audio previews or metadata beyond what the rights holders allow.',
            ]),
            ('4. Music, Trademarks and Third-Party Content', [
                'All song titles, artist names, recordings, artwork and marks belong to their respective owners. Playing short audio excerpts for a song-identification quiz is not a claim of ownership and grants you no license to copy them. Song Guesser is independent and is not affiliated with, sponsored by, or endorsed by any artist, label, publisher, or any similar song-guessing service.',
            ]),
            ('5. Game Results and Fair Play', [
                'Matching, scores and difficulty are provided for entertainment only and may be affected by metadata, audio behaviour, networks or catalog changes. The game is not a gambling, wagering or prize competition.',
            ]),
            ('6. Service Availability', [
                'The game is provided “as is” and “as available”. We do not guarantee uninterrupted access, the continued availability of any track, or compatibility with every device, browser or region.',
            ]),
            ('7. Intellectual Property', [
                'The site’s interface, original text, branding and software are protected and belong to Song Guesser. You receive only a limited right to use the site for its intended purpose.',
            ]),
            ('8. Disclaimers', [
                'The service is provided without warranties of any kind, express or implied, to the maximum extent permitted by law.',
            ]),
            ('9. Limitation of Liability', [
                'To the maximum extent permitted by law, Song Guesser is not liable for any indirect, incidental, special, consequential or punitive damages, or for lost data, profits or access, arising from your use of the site.',
            ]),
            ('10. Changes to These Terms', [
                'We may revise these terms from time to time. The “Last updated” date shows the current version, and continued use of the site after a change means you accept the revised terms.',
            ]),
            ('11. Contact', [
                'Questions about these terms go to <a href="mailto:support@songguesser.co">support@songguesser.co</a>.',
            ]),
        ],
    },
    {
        'slug': 'contact',
        'title': 'Contact — Song Guesser',
        'desc': 'Contact Song Guesser — reach us for bugs, feedback, song requests, copyright or takedown requests, and privacy questions.',
        'og_desc': 'How to contact Song Guesser — bugs, song requests, copyright and takedown requests, and privacy questions.',
        'h1': 'Contact Song Guesser',
        'eyebrow': 'We read everything',
        'name': 'Contact',
        'contact_schema': True,
        'sections': [
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
                'We aim to reply within a few days. Please be patient with takedown requests, which we review in the order they arrive.',
            ]),
        ],
    },
]


def breadcrumb(name, slug):
    return ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},'
            '{"@type":"ListItem","position":2,"name":"%s","item":"https://www.songguesser.co/%s/"}]}' % (name, slug))

WEBSITE = '{"@context":"https://schema.org","@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/","potentialAction":{"@type":"SearchAction","target":"https://www.songguesser.co/?q={search_term_string}","query-input":"required name=search_term_string"}}'

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

CONTACT_SCHEMA = ('{"@context":"https://schema.org","@type":"ContactPage","name":"Contact Song Guesser",'
                  '"url":"https://www.songguesser.co/contact/",'
                  '"about":{"@type":"WebSite","name":"Song Guesser","url":"https://www.songguesser.co/"}}')

for page in PAGES:
    slug = page['slug']
    parts = []
    parts.append(HEAD_TPL
                 .replace('@@TITLE@@', page['title'])
                 .replace('@@DESC@@', page['desc'])
                 .replace('@@SLUG@@', slug)
                 .replace('@@OGDESC@@', page['og_desc'])
                 .replace('@@CSS@@', css))
    parts.append(breadcrumb(page['name'], slug))
    parts.append('\n</script>\n<script type="application/ld+json">\n')
    parts.append(WEBSITE)
    parts.append('\n</script>\n')
    if page['contact_schema']:
        parts.append('<script type="application/ld+json">\n' + CONTACT_SCHEMA + '\n</script>\n')
    parts.append('</head>\n<body>\n\n')
    parts.append(header)
    parts.append('\n\n<section class="songspot-seo">\n')

    first = True
    for heading, paras in page['sections']:
        parts.append('  <section class="songspot-seo-section">\n')
        if first:
            parts.append('    <div class="songspot-seo-heading">\n      <p class="songspot-seo-eyebrow">%s</p>\n      <h1>%s</h1>\n    </div>\n' % (page['eyebrow'], page['h1']))
            first = False
        else:
            parts.append('    <div class="songspot-seo-copy">\n      <h2>%s</h2>\n' % heading)
        parts.append('    <div class="songspot-seo-copy">\n')
        for p in paras:
            parts.append('      <p>%s</p>\n' % p)
        parts.append('    </div>\n  </section>\n')

    parts.append('</section>\n\n')
    parts.append(footer_legal)
    parts.append('\n\n' + dropdown_js + '\n</body></html>\n')

    outdir = os.path.join(BASE, slug)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    write(os.path.join(outdir, 'index.html'), ''.join(parts))
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
