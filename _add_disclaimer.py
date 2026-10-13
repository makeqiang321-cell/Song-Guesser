# -*- coding: utf-8 -*-
"""Add a copyright/trademark disclaimer to the footer site-wide (every index.html).
Addresses the P0 copyright/trademark-risk audit item. Idempotent. Writes CRLF."""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))

DISCLAIMER = (
    '    <p class="songspot-footer-disclaimer">Song Guesser is an independent game and is not '
    'affiliated with, endorsed by, or sponsored by Spotify, Apple Music, YouTube Music, or any '
    'record label, artist, or publisher. All song titles, artist names, and trademarks are the '
    'property of their respective owners. Short clips are played briefly for a song-identification quiz.</p>')

CSS_RULE = '\n.songspot-footer-disclaimer{grid-column:1/-1;font-size:12px;color:#7f8b83;line-height:1.75;max-width:820px;margin:0}\n'

FOOTER_OPEN = '<footer class="songspot-site-footer">'

changed = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        s = io.open(p, encoding='utf-8').read()
        if 'songspot-footer-disclaimer' in s:
            continue
        # insert CSS before </style>
        if '.songspot-footer-disclaimer{' not in s:
            s = s.replace('</style>', CSS_RULE + '</style>', 1)
        # insert disclaimer into footer (after nav, before footer-main close)
        fi = s.find(FOOTER_OPEN)
        if fi == -1:
            continue
        fj = s.find('</footer>', fi)
        foot = s[fi:fj]
        nav = foot.find('</nav>')
        if nav == -1:
            continue
        s = s[:fi + nav + len('</nav>')] + '\n' + DISCLAIMER + s[fi + nav + len('</nav>'):]
        io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)
        changed += 1

print('disclaimer added to %d pages' % changed)
