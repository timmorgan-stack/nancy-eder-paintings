#!/usr/bin/env python3
"""Add the sketchbook dimension: a place/trip grouping that cuts ACROSS the medium
collections, so one sketchbook can hold paintings, drawings, prints and collage together.
Only assigned where the place is actually identifiable — works with no recorded place are
left out of this navigation rather than guessed at.
Usage: python3 tools/build_sketchbooks.py <catalog.json>"""
import json, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat_path = sys.argv[1]

SKETCHBOOKS = [
 ("cuba",     "Cuba",                "Baracoa, Bayamo, Santiago and San Antonio."),
 ("france",   "France & the Roussillon","Céret, Collioure, the Tech valley and the coast."),
 ("spain",    "Spain",               "Empúries, L'Escala and the Costa Brava."),
 ("portugal", "Portugal",            "Porto and the Douro valley."),
 ("italy",    "Italy",               "Umbria and the hills near Perugia."),
 ("england",  "England",             "Cheshire, Staffordshire, Hertfordshire and London."),
 ("norway",   "Norway",              "Rygge and Østfold."),
 ("maine",    "Maine & Acadia",      "Acadia, Mount Desert Island and the Schoodic Peninsula."),
 ("florida",  "Florida",             "Gardens and streets in the American South."),
]
# checked in order; first hit wins
KEYS = [
 ("cuba",     ["cuba", "baracoa", "bayamo", "santiago", "san antonio"]),
 ("spain",    ["spain", "espagne", "escala", "empúries", "emporias", "figueres", "catalu"]),
 ("portugal", ["portugal", "porto", "douro", "régua", "regua"]),
 ("italy",    ["italy", "umbria", "canalicchio", "perugia"]),
 ("england",  ["england", "cheshire", "london", "stoke", "staffordshire", "ayot", "tatton", "dunham"]),
 ("norway",   ["norway", "rygge", "østfold", "ostfold", "halmstad"]),
 ("maine",    ["maine", "acadia", "schoodic", "bar harbor", "mount desert", "spruce"]),
 ("florida",  ["florida", "petersburg", "lakeland", "davie", "plantation gardens", "hollis"]),
 ("france",   ["france", "céret", "ceret", "perpignan", "banyuls", "collioure", "arles-sur-tech",
               "racou", "laroque", "argelès", "cyprien", "figueres"]),
]
SERIES_TO_BOOK = {s: s for s in ("cuba","france","spain","portugal","italy","england","norway","maine","florida")}

cat = json.load(open(os.path.join(root, cat_path)))
cat["sketchbooks"] = [{"id": i, "name": n, "blurb": b} for i, n, b in SKETCHBOOKS]

def book_for(a):
    # the recorded place wins: several works sit in a trip series but were painted elsewhere
    # (e.g. "La Playa en L'Escala" is filed under the France series but is in Spain)
    hay = f"{a.get('place','')} {a.get('title','')}".lower()
    for bid, words in KEYS:
        if any(w in hay for w in words): return bid
    if a["series"] in SERIES_TO_BOOK: return SERIES_TO_BOOK[a["series"]]
    return None

counts, unassigned = {}, 0
for a in cat["artworks"]:
    b = book_for(a)
    if b: a["sketchbook"] = b; counts[b] = counts.get(b, 0) + 1
    else: a.pop("sketchbook", None); unassigned += 1
# drop empty sketchbooks
cat["sketchbooks"] = [s for s in cat["sketchbooks"] if counts.get(s["id"])]
json.dump(cat, open(os.path.join(root, cat_path), "w"), indent=1, ensure_ascii=False)
print(f"assigned {sum(counts.values())} of {len(cat['artworks'])}; {unassigned} have no identifiable place")
for s in cat["sketchbooks"]:
    print(f"   {s['name']:<26} {counts[s['id']]:>4}")
