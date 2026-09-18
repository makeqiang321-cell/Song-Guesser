# -*- coding: utf-8 -*-
import io, re
P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_artists.py"
src = io.open(P, encoding="utf-8").read()

FIXED = r'''def about_html(a):
    x = EXTRA[a['slug']]
    steps = ''.join(step(i + 1, ic, t, b) for i, (ic, t, b) in enumerate(a['steps']))
    faq = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, ans)
                  for i, (q, ans) in enumerate(x['faq']))
    return ('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div>'
      '<p>%s</p><p>%s</p>'
      '</section>\n'
      '<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>How to Play</h2></div>'
      '<p>%s</p><ol class="songspot-how-grid">%s</ol>'
      '</section>\n'
      '<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><h2>Tips to Play Better</h2></div>'
      '<p>%s</p>'
      '</section>\n'
      '<section id="faq" class="songspot-seo-section songspot-seo-faq">'
      '<div class="songspot-seo-heading"><h2>%s</h2></div>'
      '<div class="songspot-faq-list">%s</div>'
      '</section>\n'
      '<section class="songspot-seo-section">%s</section>\n') % (
        a['h2'], a['p1'], a['p2'],
        a['intro'], steps,
        x['tips'],
        a['faq_h2'], faq,
        x['closing'])
'''

new_src, n = re.subn(r'def about_html\(a\):.*?\n\ndef build\(',
                     lambda m: FIXED + '\ndef build(', src, count=1, flags=re.S)
assert n == 1, "about_html match count %d" % n
io.open(P, "w", encoding="utf-8").write(new_src)
print("FIXED about_html OK")
