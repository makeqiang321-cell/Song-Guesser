# -*- coding: utf-8 -*-
"""De-AI the shared boilerplate sentences in _gen_artists.py by rotating them
through varied phrasings (round-robin in file order). Idempotent-ish: only the
exact known boilerplate strings are touched."""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\Administrator\Desktop\guess-the-song"
p = os.path.join(BASE, "_gen_artists.py")
h = io.open(p, encoding="utf-8").read()

A_variants = [
    "Each round opens with a 0.1-second clip, and you name the track before the longer reveals do it for you.",
    "A 0.1-second clip opens every round, and you name the track before the longer reveals do it for you.",
    "Each round opens with a 0.1-second clip, and your job is to name the track before the longer reveals do it for you.",
    "Each round opens with a 0.1-second clip, and your job is to name the track before the longer reveals hand it to you.",
]
A_new = [
    "Every round starts on a sliver of audio and waits for you to call the track before it opens up.",
    "You get a tenth of a second, and you name it before the reveal starts doing your job.",
    "The round opens on the shortest clip and only widens once you've had your guess.",
    "A sliver of audio plays, and you have to name the song before more of it spills out.",
    "The clip starts at 0.1 seconds and stays there until you ask for more.",
    "You hear the opening sliver, then type the title before the longer reveals step in.",
]
B_old = "It is a Heardle-style song guessing game for "
B_new = [
    "It's the Heardle-style song guessing game for ",
    "A Heardle-style song guessing game built for ",
    "It's Heardle-style song guessing aimed at ",
    "The Heardle-style song guessing game for ",
    "It's a Heardle-style song guessing game for ",
    "A song guessing game in the Heardle style for ",
]
B2_old = "Think of it as a Heardle-style song guessing game for "
B2_new = [
    "It's a Heardle-style song guessing game made for ",
    "A Heardle-style song guessing game aimed at ",
]

i = {"n": 0}
def rot(new):
    def f(m):
        s = new[i["n"] % len(new)]
        i["n"] += 1
        return s
    return f

for v in A_variants:
    h = re.sub(re.escape(v), rot(A_new), h)
h = re.sub(re.escape(B_old), rot(B_new), h)
h = re.sub(re.escape(B2_old), rot(B2_new), h)

io.open(p, "w", encoding="utf-8").write(h)
print("rotated %d boilerplate slots" % i["n"])
