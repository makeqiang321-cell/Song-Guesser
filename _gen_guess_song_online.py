# -*- coding: utf-8 -*-
"""Build /guess-song-online/ — an informational guide page for songguesser.co.
Uses the site's header/footer/dropdown chrome but a NEW "guide" article template
(quick-answer card, TOC, step cards, decision table, callouts, FAQ accordion),
distinct from the songspot-seo section rhythm. Content is read from the authored
source file. Writes CRLF."""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\Administrator\Desktop\外链插件1\guess-song-online.html"

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)

# --- site chrome from about/index.html ---
about = read(os.path.join(BASE, 'about', 'index.html'))
site_css = about[about.index('<style>') + len('<style>'):about.index('</style>')]
hs = about.index('<header class="songspot-site-header">')
header = about[hs:about.index('</header>', hs) + len('</header>')]
fs = about.index('<footer class="songspot-site-footer">')
footer = about[fs:about.index('</footer>', fs) + len('</footer>')]
m = about.index("document.querySelectorAll('.songspot-site-quiz-menu')")
djs = about[about.rfind('<script>', 0, m):about.index('</script>', m) + len('</script>')]

# --- authored article: guide css + schemas + body ---
src = read(SRC)
guide_css = src[src.index('<style>') + len('<style>'):src.index('</style>')]
schemas = re.findall(r'<script type="application/ld\+json">\n.*?\n</script>', src, re.S)
body = src[src.index('<main class="wrap">'):src.index('</main>') + len('</main>')]
body = body.replace('<main class="wrap">', '<main class="guide-article">')

# scope the guide CSS: drop global body/a rules, keep only component + scoped rules
guide_css = re.sub(r'body\{[^}]*\}', '', guide_css)
guide_css = re.sub(r'a:hover\{[^}]*\}', '', guide_css)
guide_css = re.sub(r'a\{[^}]*\}', '', guide_css)
guide_css = guide_css.replace('.wrap{width:min(760px,100% - 40px);margin:0 auto}',
                              '.guide-article{width:min(760px,100% - 40px);margin:0 auto}')
guide_css += '\n.guide-article a{color:var(--guide-accent-2);text-decoration:none}\n.guide-article a:hover{text-decoration:underline}\n'

TITLE = 'Guess Song: How to Play &amp; Get Better'
DESC = 'How to play guess song and get better. Rules, the 0.1-second reveal mechanic, and what your ear reads in a short clip.'

head = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%s</title>
<meta name="description" content="%s" />
<link rel="canonical" href="https://www.songguesser.co/guess-song-online/" />
<link rel="icon" type="image/svg+xml" href="/images/logo.svg" />
<meta property="og:type" content="article" />
<meta property="og:title" content="%s" />
<meta property="og:description" content="%s" />
<meta property="og:url" content="https://www.songguesser.co/guess-song-online/" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="%s" />
<meta name="twitter:description" content="%s" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;1,700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
%s
%s</style>
''' % (TITLE, DESC, TITLE, DESC, TITLE, DESC, site_css, guide_css)

out = [head]
for s in schemas:
    out.append(s + '\n')
out.append('</head>\n<body>\n\n')
out.append(header)
out.append('\n\n')
out.append(body)
out.append('\n\n')
out.append(footer)
out.append('\n\n' + djs + '\n</body></html>\n')

outdir = os.path.join(BASE, 'guess-song-online')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), ''.join(out))
print('wrote guess-song-online/index.html')

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
entry = '<url><loc>https://www.songguesser.co/guess-song-online/</loc><priority>0.6</priority></url>'
if '/guess-song-online/' not in s:
    s = s.replace('<url><loc>https://www.songguesser.co/how-to-play/</loc>', entry + '\n  <url><loc>https://www.songguesser.co/how-to-play/</loc>', 1)
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has guess-song-online')
