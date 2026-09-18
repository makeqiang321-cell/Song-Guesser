# -*- coding: utf-8 -*-
import io, re
P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_artists.py"
src = io.open(P, encoding="utf-8").read()

# 1) Replace about_html: render only unique content (p1, steps[:2], who_p, faq[:1]),
#    drop the duplicated p2/intro/steps[2:]/faq[1:] and make the CTA name-unique.
new_about = '''def about_html(a):
    nm = a['name'][4:] if a['name'].startswith('The ') else a['name']
    steps = ''.join(step(i + 1, ic, t, b) for i, (ic, t, b) in enumerate(a['steps'][:2]))
    faq = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, ans)
                  for i, (q, ans) in enumerate(a['faq'][:1]))
    return ('<section class="songspot-seo-section">'
      '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2></div>'
      '<h3>%s</h3><p>%s</p>'
      '<h3>%s</h3><ol class="songspot-how-grid">%s</ol>'
      '<h3>%s</h3><p>%s</p>'
      '</section>\\n'
      '<section id="faq" class="songspot-seo-section songspot-seo-faq">'
      '<div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">%s</p><h2>%s</h2></div>'
      '<div class="songspot-faq-list">%s</div>'
      '</section>\\n'
      '<section class="songspot-seo-cta">'
      '<p class="songspot-seo-eyebrow">%s songs, one clip at a time</p>'
      '<h2>Ready to guess the %s song in 0.1 seconds?</h2>'
      '<a href="#play">Start playing \u2192</a>'
      '<a class="songspot-cta-home" href="/">Open the full song guesser \u2192</a>'
      '</section>\\n') % (
        a['eyebrow'], a['h2'], a['what_h3'], a['p1'],
        a['how_h3'], steps, a['who_h3'], a['who_p'],
        a['faq_eyebrow'], a['faq_h2'], faq,
        nm, nm)
'''

assert re.search(r'def about_html\(a\):.*?\n\ndef build\(', src, re.S), "about_html not found"
src = re.sub(r'def about_html\(a\):.*?\n\ndef build\(', new_about + '\ndef build(', src, count=1, flags=re.S)

# 2) faq_json mirrors the visible single FAQ.
assert src.count("faq_json(a['faq'])") == 1, "faq_json ref count %d" % src.count("faq_json(a['faq'])")
src = src.replace("faq_json(a['faq'])", "faq_json(a['faq'][:1])")

# 3) The three identical "Try to guess ... fast" heroes (literal \\u2014 in file).
heroes = [
  ("'hero': 'Try to guess the Weeknd song fast \\u2014 every round opens with just 0.1 seconds of audio.',",
   "'hero': 'Name the Weeknd track from the shortest clip you can \\u2014 the neon synth glow usually gives him away before the vocal does.',"),
  ("'hero': 'Try to guess the Taylor Swift song fast \\u2014 every round opens with just 0.1 seconds of audio.',",
   "'hero': 'How fast can you place the Taylor Swift song? A tenth of a second is all the intro you get.',"),
  ("'hero': 'Try to guess the Michael Jackson song fast \\u2014 every round opens with just 0.1 seconds of audio.',",
   "'hero': 'Name the Michael Jackson track from a tenth of a second \\u2014 the beat and the breath give the King of Pop away.',"),
]
for old, new in heroes:
    assert src.count(old) == 1, "HERO COUNT %d: %s" % (src.count(old), old[:50])
    src = src.replace(old, new)

io.open(P, "w", encoding="utf-8").write(src)
print("PATCHED _gen_artists.py OK")
