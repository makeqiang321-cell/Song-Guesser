# -*- coding: utf-8 -*-
"""Regenerate sitemap.xml from the directory tree. Every index.html becomes a URL.
Priorities follow the established map: home 1.0, song-quiz/music-quiz 0.9,
keyword pages 0.85, artist pages 0.8, genre/decade pages 0.7, info pages 0.3-0.7.
Deterministic and complete — no manual edits needed.
"""
import os

BASE = "https://www.songguesser.co"
SKIP = {".git", ".vercel", "__pycache__", "images", "node_modules", ".claude"}
# Pages canonicalized to a stronger URL (keyword-cannibalization consolidation):
# omit from sitemap so Google only gets the canonical set.
CONSOLIDATED = {
    "guess-the-song-in-0-1-second",
    "guess-song-online",
    "guess-that-song",
    "name-that-song",
    "music-guesser",
    "music-guessing-game",
    "song-quiz",
    "music-trivia-game",
    "song-trivia",
    "guess-the-taylor-swift-song",
}


def url(rel):
    return BASE + "/" if rel == "." else BASE + "/" + rel.replace("\\", "/") + "/"


def priority(rel):
    if rel == ".":
        return "1.0"
    if rel in ("song-quiz", "music-quiz"):
        return "0.9"
    if rel in ("guessable-songs", "song-guesser-artists", "guess-song-decades"):
        return "0.85"
    if rel.startswith("song-guesser-artists/"):
        return "0.8"
    if rel.startswith("guessable-songs/") or rel.startswith("guess-song-decades/"):
        return "0.7"
    if rel == "guess-song-online":
        return "0.6"
    if rel == "how-to-play":
        return "0.7"
    if rel == "about":
        return "0.6"
    if rel in ("privacy-policy", "terms-of-service", "contact"):
        return "0.3"
    return "0.85"


pages = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP]
    if "index.html" in files:
        rel = os.path.relpath(root, ".").replace("\\", "/")
        if rel in CONSOLIDATED:
            continue
        pages.append("." if rel == "." else rel)

pages.sort(key=lambda p: (p != ".", p))

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages:
    out.append('  <url><loc>%s</loc><priority>%s</priority></url>' % (url(p), priority(p)))
out.append('</urlset>')

open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("OK ->", len(pages), "urls")
