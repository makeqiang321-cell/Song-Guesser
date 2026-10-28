# -*- coding: utf-8 -*-
"""Copy the self-contained authored page into the deployable path (CRLF)
and keep the sitemap entry. The authored file 外链插件1/guess-song-online.html
already carries the full homepage CSS/header/footer + game.js, so this is a
straight copy — preview and deploy are the same page."""
import io, os

SRC = r"C:\Users\Administrator\Desktop\外链插件1\guess-song-online.html"
BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\r\n').write(s)

outdir = os.path.join(BASE, 'guess-song-online')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
write(os.path.join(outdir, 'index.html'), read(SRC))
print('wrote guess-song-online/index.html')

# --- sitemap entry (idempotent) ---
sp = os.path.join(BASE, 'sitemap.xml')
s = read(sp)
entry = '<url><loc>https://www.songguesser.co/guess-song-online/</loc><priority>0.6</priority></url>'
if '/guess-song-online/' not in s:
    s = s.replace('<url><loc>https://www.songguesser.co/how-to-play/</loc>',
                  entry + '\n  <url><loc>https://www.songguesser.co/how-to-play/</loc>', 1)
    write(sp, s)
    print('sitemap updated')
else:
    print('sitemap already has guess-song-online')
