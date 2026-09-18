# -*- coding: utf-8 -*-
import io
P = r"C:\Users\Administrator\Desktop\guess-the-song\_gen_artists.py"
src = io.open(P, encoding="utf-8").read()

before = src.count("www.songguesser.co/' + slug + '/'")
src = src.replace("www.songguesser.co/' + slug + '/'", "www.songguesser.co/song-guesser-artists/' + slug + '/'")
after = src.count("www.songguesser.co/' + slug + '/'")
assert after == 0, "still %d unpatched www.songguesser.co slug refs" % after

# breadcrumb position 2: Music Quizzes -> Artists, /music-quizzes/ -> /song-guesser-artists/
src = src.replace('{"@type":"ListItem","position":2,"name":"Music Quizzes","item":"https://www.songguesser.co/music-quizzes/"}',
                  '{"@type":"ListItem","position":2,"name":"Artists","item":"https://www.songguesser.co/song-guesser-artists/"}')

io.open(P, "w", encoding="utf-8").write(src)
print("PATCHED www.songguesser.co slug refs: %d" % before)
