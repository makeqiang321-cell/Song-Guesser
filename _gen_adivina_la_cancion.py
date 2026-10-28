# -*- coding: utf-8 -*-
"""Generate /adivina-la-cancion-en-espanol/ — a full generic game page (all genres) + an
original, readable, de-AI'd Spanish SEO article targeting "adivina la canción en español".
Orphaned (not in nav/footer/sitemap). Internal links: homepage + genre pages.
"""
import os

SRC = "guessable-songs/k-pop/index.html"
DST_DIR = "adivina-la-cancion-en-espanol"
DST = os.path.join(DST_DIR, "index.html")

s = open(SRC, encoding="utf-8").read()

# --- language ---
s = s.replace('<html lang="en">', '<html lang="es">')

# --- schema: VideoGame name ---
s = s.replace(
    '"name":"K-Pop Guessable Songs"',
    '"name":"Adivina la Canción en Español"',
)

# --- breadcrumb (keep one) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Genres","item":"https://www.songguesser.co/guessable-songs/"},{"@type":"ListItem","position":3,"name":"K-Pop","item":"https://www.songguesser.co/guessable-songs/k-pop/"}]}',
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"},{"@type":"ListItem","position":2,"name":"Adivina la Canción en Español","item":"https://www.songguesser.co/adivina-la-cancion-en-espanol/"}]}',
)
s = s.replace(
    '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.songguesser.co/"}]}',
    "",
)

# --- FAQ schema (real user questions, Spanish) ---
s = s.replace(
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to know the group to play?","acceptedAnswer":{"@type":"Answer","text":"No — you only need to recognize the guessable song. The production and the hook are usually enough, even if you cannot name the members."}},{"@type":"Question","name":"How many K-pop guessable songs are in the pool?","acceptedAnswer":{"@type":"Answer","text":"796 tracks across generations of groups and soloists. The rotation stays inside the genre and mixes eras."}},{"@type":"Question","name":"Is the K-pop quiz in English or Korean?","acceptedAnswer":{"@type":"Answer","text":"The game is entirely in your browser, and you type the title either way. The clip of a guessable song is the same for every language."}}]}',
    '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"No puedo adivinar una canción desde 0,1 segundos — ¿se supone que es tan difícil?","acceptedAnswer":{"@type":"Answer","text":"Sí. El fragmento abre en una décima de segundo y le das a play otra vez para revelar 0,5s, 2s, 8s y luego 15s. Casi nadie la saca desde el primer instante; la sacan en la pista que por fin encaja."}},{"@type":"Question","name":"¿Es lo mismo que Heardle?","acceptedAnswer":{"@type":"Answer","text":"Misma mecánica, pero no es un juego diario. Heardle te da una canción al día; este es ilimitado, con niveles de dificultad y filtros de género, década y artista."}},{"@type":"Question","name":"¿Escribo la respuesta o elijo entre opciones?","acceptedAnswer":{"@type":"Answer","text":"La escribes. No hay opción múltiple. Si sabes parte del título, el buscador se estrecha mientras escribes."}},{"@type":"Question","name":"¿Por qué no suena el audio en mi móvil?","acceptedAnswer":{"@type":"Answer","text":"El juego decodifica audio real en tu navegador, así que necesita un toque para empezar (los navegadores bloquean el autoplay) y una conexión estable. El modo de ahorro de batería también puede retrasarlo."}},{"@type":"Question","name":"¿Es gratis o necesito una cuenta?","acceptedAnswer":{"@type":"Answer","text":"Gratis, en el navegador, sin registro, sin descarga, sin límite diario."}},{"@type":"Question","name":"Estoy atascado en una canción — ¿cómo consigo otra?","acceptedAnswer":{"@type":"Answer","text":"Pulsa Skip para revelar un fragmento más largo, o Reroll para cambiar a una canción nueva."}}]}',
)

# --- hero h1 + subtitle ---
s = s.replace(
    '<h1 id="songspot-heading">K-Pop Guessable Songs</h1>',
    '<h1 id="songspot-heading">Adivina la Canción en Español</h1>',
)
s = s.replace(
    '<p>Group hooks, polished production, a first beat — name the K-pop <a href="/guessable-songs/">guessable songs</a> in a second flat.</p>',
    '<p>Tienes una décima de segundo. Adivina la canción en español desde el primer instante y desbloquea más audio solo si lo necesitas.</p>',
)

# --- title / description / canonical / og / twitter (+ VideoGame desc & url) ---
s = s.replace(
    "K-Pop Guessable Songs | Song Guesser",
    "Adivina la Canción en Español — Adivina Canciones desde 0,1 Segundos | Song Guesser",
)
s = s.replace(
    "Name the k-pop guessable songs from a 0.1-second clip. Free browser game with 796 K-Pop guessable songs — reveal 0.5s, 2s, 8s and 15s only when you need more.",
    "Adivina la canción en español desde 0,1 segundos de audio. Juego gratis e ilimitado en el navegador — escucha 0,5s, 2s, 8s y 15s solo cuando te atascas, y filtra por género, década o artista.",
)
s = s.replace(
    "https://www.songguesser.co/guessable-songs/k-pop/",
    "https://www.songguesser.co/adivina-la-cancion-en-espanol/",
)

# --- make the game generic (all genres) ---
s = s.replace(
    'window.SONG_INITIAL = {"genre":51}',
    'window.SONG_INITIAL = {}',
)

# --- swap the SEO sections (keep the game shell + scripts) ---
start = s.index('<section class="songspot-seo">')
end = s.index('<footer class="songspot-site-footer">')
article = '''<section class="songspot-seo">
<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Adivina la canción</p><h2>¿Qué es Adivina la Canción?</h2><p>Cada ronda empieza con 0,1 segundos de audio. A veces es un golpe de caja, a veces el aire que toma el cantante antes de entrar. Escribes el título de la canción desde ese instante, y si no puedes, le das a play otra vez y el fragmento crece: 0,5 segundos, 2, 8, y luego 15. Cada pista extra te quita puntos, así que el juego es decidir con cuánto audio te basta para acertar.</p></div><p>No hay botones de opción múltiple. Escribes la respuesta tú mismo, y por eso acertar una canción desde una décima de segundo se siente como un logro de verdad. Es la misma idea que los juegos diarios tipo Heardle, pero aquí no te bloquea después de una canción: puedes jugar rondas seguidas, sin cuenta y sin límite diario, aquí mismo en <a href="/">Song Guesser</a>.</p></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Adivina la canción de un vistazo</p><h2>Cómo funciona una ronda</h2><p>Las reglas caben en una frase: escucha lo mínimo posible y escribe el título. Así es una ronda.</p></div><dl class="songspot-seo-stats">
<div><dt>Fragmento inicial</dt><dd>0,1 segundos</dd></div>
<div><dt>Pistas</dt><dd>0,5s → 2s → 8s → 15s</dd></div>
<div><dt>Respuesta</dt><dd>Escribes el título, sin opciones</dd></div>
<div><dt>Puntos</dt><dd>Cada pista que pides baja tu puntuación</dd></div>
<div><dt>Dificultad</dt><dd>Fácil / Media / Difícil / Experto</dd></div>
<div><dt>Filtros</dt><dd>Género, década, artista</dd></div>
<div><dt>Rondas</dt><dd>Ilimitadas, sin bloqueo diario</dd></div>
<div><dt>Dispositivos</dt><dd>Móvil u ordenador, en el navegador</dd></div>
</dl></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Las pistas</p><h2>Qué escuchas de verdad en cada pista</h2><p>El truco no es adivinar. Es saber qué te da cada longitud de fragmento. Esto es lo que suele oírse en cada paso.</p></div><ul class="reveal-map">
<li><strong>0,1s</strong><span>Un transitorio, no una melodía. Un golpe de batería, un acorde de sintetizador, una primera respiración. Juzga la textura y la época, no la melodía.</span></li>
<li><strong>0,5s</strong><span>La primera palabra o el primer acorde del estribillo. Si conoces la canción, aquí suele encajar.</span></li>
<li><strong>2s</strong><span>Una frase completa o el arranque del estribillo. Suficiente para ubicar el género y a menudo el artista.</span></li>
<li><strong>8s</strong><span>Estrofa que entra en el preestribillo, o casi todo un estribillo. La melodía ya es evidente, y también la época.</span></li>
<li><strong>15s</strong><span>El panorama completo. Si todavía no la tienes, es una canción que no conoces. Salta y sigue.</span></li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">El repertorio</p><h2>Qué hay en el repertorio</h2><p>Ocho géneros anclan el repertorio. Cada uno tiene un sonido que aprendes a pillar en medio segundo.</p></div><div class="songspot-feature-grid">
<article><span class="icon">💿</span><h3><a href="/guessable-songs/pop/">Pop</a></h3><p>Éxitos de radio y número uno. Si un estribillo entró en el top 40, probablemente está aquí.</p></article>
<article><span class="icon">🎤</span><h3><a href="/guessable-songs/hip-hop/">Hip-Hop</a></h3><p>Un drop de beat, un "yeah", una firma de productor. La pista de 0,1s suele ser una batería o un ad-lib.</p></article>
<article><span class="icon">🎸</span><h3><a href="/guessable-songs/rock/">Rock</a></h3><p>Un golpe de guitarra o un fill de batería. Los riffs están hechos para pillarse en el primer beat.</p></article>
<article><span class="icon">🎹</span><h3><a href="/guessable-songs/r-and-b/">R&B</a></h3><p>Un acorde suave antes de que entre la voz. El timbre hace casi todo el trabajo.</p></article>
<article><span class="icon">💃</span><h3><a href="/guessable-songs/electronic/">Electrónica</a></h3><p>Un swell de sintetizador o un patrón de bombo. Juzga la textura, no la melodía.</p></article>
<article><span class="icon">🤠</span><h3><a href="/guessable-songs/country/">Country</a></h3><p>Un lick de guitarra slide o un rasgueo acústico. Los estribillos narrativos se delatan solos.</p></article>
<article><span class="icon">🪩</span><h3><a href="/guessable-songs/k-pop/">K-Pop</a></h3><p>Un golpe seco y un estribillo gritado. Las intros están hechas para pillarse antes de la primera línea.</p></article>
<article><span class="icon">🎺</span><h3><a href="/guessable-songs/metal/">Metal</a></h3><p>Un doble bombo y un riff con palm mute. Los agresivos se descubren rápido.</p></article>
</div></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Mejora rápido</p><h2>Consejos que de verdad funcionan</h2></div><ul class="kpop-facts">
<li>El fragmento de 0,1s casi nunca es una melodía. Escucha la textura, la batería, la época de la producción.</li>
<li>Salta pronto en las canciones que no conoces. La pista de 0,5s es donde suele aparecer el estribillo.</li>
<li>La dificultad Fácil se queda en éxitos de radio; Experto mete caras B y canciones de álbum.</li>
<li>El filtro de artista es un atajo: si conoces la voz pero no el título, cierra el rango a un solo artista.</li>
<li>Escribe el título, no el artista. La respuesta necesita el nombre de la canción.</li>
<li>Usa el buscador cuando recuerdes parte de un título. Se va estrechando mientras escribes.</li>
</ul></section>

<section class="songspot-seo-section"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">La historia completa</p><h2>Adivina la Canción es un juego de oído, no de memoria</h2></div><p>No adivinas una canción recordándola. La adivinas reconociendo medio segundo de sonido, y eso es otra habilidad. Un fill de batería, un swell de sintetizador, la forma en que entra una voz: esas son las pistas, y 0,1 segundos solo alcanza para una de ellas. Por eso el juego sigue siendo difícil aunque sepas mucha música.</p><p>Lo difícil de verdad es lo que nunca sonó en la radio: temas de álbum, caras B, la canción que oíste una vez en una playlist y olvidaste. El modo Fácil te mantiene en lo que todo el mundo conoce. Experto te mete en el fondo del cajón. La mayoría empieza en Fácil y sube cuando las pistas empiezan a caer más rápido.</p><p>Es gratis, no hay cuenta y no hay límite diario. Juega una ronda para calentar o cincuenta seguidas. Luego vuelve a <a href="/">Song Guesser</a> para los juegos por género y década. La primera décima de segundo es todo el juego.</p></section>

<section id="faq" class="songspot-seo-section songspot-seo-faq"><div class="songspot-seo-heading"><p class="songspot-seo-eyebrow">Preguntas sobre este quiz</p><h2>Adivina la Canción FAQ</h2></div><div class="songspot-faq-list">
<details open><summary>No puedo adivinar una canción desde 0,1 segundos — ¿se supone que es tan difícil?</summary><p>Sí. El fragmento abre en una décima de segundo y le das a play otra vez para revelar 0,5s, 2s, 8s y luego 15s. Casi nadie la saca desde el primer instante; la sacan en la pista que por fin encaja.</p></details>
<details><summary>¿Es lo mismo que Heardle?</summary><p>Misma mecánica, pero no es un juego diario. Heardle te da una canción al día; este es ilimitado, con niveles de dificultad y filtros de género, década y artista.</p></details>
<details><summary>¿Escribo la respuesta o elijo entre opciones?</summary><p>La escribes. No hay opción múltiple. Si sabes parte del título, el buscador se estrecha mientras escribes.</p></details>
<details><summary>¿Por qué no suena el audio en mi móvil?</summary><p>El juego decodifica audio real en tu navegador, así que necesita un toque para empezar (los navegadores bloquean el autoplay) y una conexión estable. El modo de ahorro de batería también puede retrasarlo.</p></details>
<details><summary>¿Es gratis o necesito una cuenta?</summary><p>Gratis, en el navegador, sin registro, sin descarga, sin límite diario.</p></details>
<details><summary>Estoy atascado en una canción — ¿cómo consigo otra?</summary><p>Pulsa Skip para revelar un fragmento más largo, o Reroll para cambiar a una canción nueva.</p></details>
</div></section>

<section class="songspot-seo-cta">
<p class="songspot-seo-eyebrow">¿Cuánto audio necesitas?</p>
<h2>Adivina la Canción en Español</h2>
<p>Dale a play en Song Guesser y descubre cuánto necesita tu oído.</p>
<a href="#play">Empezar a jugar →</a>
</section>
</section>'''

s = s[:start] + article + "\n\n" + s[end:]

# --- styles for the new lists ---
s = s.replace(
    "</head>",
    "<style>\n.songspot-seo ul.kpop-facts{list-style:none;padding:0;margin:0;display:grid;gap:14px}\n.songspot-seo ul.kpop-facts li{position:relative;padding-left:30px;color:#9da8a0;font-size:15px;line-height:1.8}\n.songspot-seo ul.kpop-facts li::before{content:\"\\2022\";position:absolute;left:0;top:2px;color:var(--green2)}\n.songspot-seo ul.reveal-map{list-style:none;padding:0;margin:0;display:grid;gap:16px}\n.songspot-seo ul.reveal-map li{display:grid;grid-template-columns:68px 1fr;gap:14px;align-items:start}\n.songspot-seo ul.reveal-map strong{color:var(--green2);font-size:15px;font-weight:600}\n.songspot-seo ul.reveal-map span{color:#9da8a0;font-size:15px;line-height:1.8}\n</style>\n</head>",
)

os.makedirs(DST_DIR, exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)

# --- runnable check ---
out = s
assert "Adivina la Canción en Español" in out, "title/h1 missing"
assert "K-Pop Guessable Songs" not in out, "old title leaked"
assert "adivina-la-cancion-en-espanol" in out, "canonical missing"
assert '<html lang="es">' in out, "lang not set to es"
assert '<section class="songspot-shell"' in out, "game shell missing"
assert "window.SONG_INITIAL" in out, "game script missing"
assert "window.SONG_INITIAL = {}" in out, "generic genre not applied"
assert '"@type":"VideoGame"' in out, "VideoGame schema missing"
assert '"name":"Adivina la Canción en Español"' in out, "VideoGame name missing"
assert '"@type":"FAQPage"' in out, "FAQ schema missing"
assert out.count("<article>") == 8, "genre cards"
assert out.count("<details") == 6, "FAQ entries"
assert out.count("<h1") == 1, "h1 count"
for i in ("difficultyList", "difficultyTabs", "stageChips", "volume", "rerollBtn"):
    assert 'id="%s"' % i in out, "missing id " + i
print("OK ->", DST, len(out), "bytes")
