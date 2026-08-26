#!/usr/bin/env python3
"""Add the 'Art and Pottery' drop to a catalogue: new collections (drawings, prints,
pottery, collage) alongside the existing trip-based paintings.
Usage: python3 tools/build_new_works.py <catalog.json> <img-prefix>"""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify_art_pottery as c

cat_path, prefix = sys.argv[1], sys.argv[2]          # e.g. data/catalog.json  ""   |  ../
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL   = sorted((set(range(1, 172)) - {58}) - set(c.EXCLUDE))
PAINT = [n for n in ALL if n not in c.POTTERY | c.PRINTS | c.COLLAGE | c.DRAWINGS]

COLLECTIONS = [
    ("paintings", "Paintings", "Gouache and ink on paper, painted on location."),
    ("drawings",  "Drawings",  "Pen and ink, drawn straight into the sketchbook."),
    ("prints",    "Prints",    "Linocuts, hand-printed and hand-coloured."),
    ("pottery",   "Pottery",   "Hand-built bowls and vessels, thrown and glazed by the artist."),
    ("collage",   "Collage",   "Mixed media — torn paper, paint and print."),
]
NEW_SERIES = [
    ("botanical",       "Leaves & Gardens",       "Plants, leaves and garden corners, close up.",        "paintings"),
    ("florida",         "Florida",               "Gardens and streets in the American South.",           "paintings"),
    ("market",          "Markets & Table",       "Market stalls, fish counters and the kitchen table.",  "paintings"),
    ("studies",         "Colour Studies",        "Landscape reduced to bands and blocks of colour.",     "paintings"),
    ("drawings-places", "Places & Streets",      "Houses, streets and rooftops, mostly around Céret.",   "drawings"),
    ("drawings-trees",  "Trees, Gardens & Leaves","Woods, branches and growing things in line alone.",   "drawings"),
    ("drawings-market", "Markets & Still Life",  "Sardines, merlu and the fromage counter.",             "drawings"),
    ("prints",          "Linocuts",              "Rabbits, reeds and moons — cut, printed and coloured.","prints"),
    ("pottery",         "Bowls & Vessels",       "Hand-built earthenware, glazed in strong colour.",     "pottery"),
    ("collage",         "Mixed Media",           "Torn and painted paper, built up in layers.",          "collage"),
]

SPEC = {  # medium, [(size, price)], description
 "paintings": ("Ink and gouache on paper",
   [("8 × 10 in",275),("9 × 12 in",325),("11 × 14 in",425),("12 × 16 in",550)],
   "Painted on location in gouache and ink. Sold unframed; ships flat, protected between archival boards."),
 "drawings": ("Pen and ink on paper",
   [("8 × 10 in",180),("9 × 12 in",220),("11 × 14 in",280)],
   "Drawn directly in ink, without pencil first — one sitting, no reworking. Sold unframed; ships flat."),
 "prints": ("Linocut on paper",
   [("8 × 10 in",120),("11 × 14 in",160)],
   "A linocut cut and printed by the artist, each impression inked and coloured by hand, so no two are identical."),
 "pottery": ("Hand-built glazed ceramic",
   [("5 in diameter",85),("6 in diameter",120),("7 in diameter",165)],
   "A hand-built bowl, glazed and fired by the artist. Small variations in rim and glaze are part of the making."),
 "collage": ("Mixed media collage on paper",
   [("11 × 14 in",395),("12 × 16 in",475)],
   "Torn paper, paint and printed fragments built up into a landscape. Sold unframed; ships flat."),
}
FEATURED = {107, 121, 45, 34, 158, 164, 99, 143, 64, 108, 5, 128}

def series_of(n):
    if n in c.POTTERY: return "pottery", "pottery"
    if n in c.PRINTS:  return "prints", "prints"
    if n in c.COLLAGE: return "collage", "collage"
    if n in c.DRAWINGS:
        if n in c.D_MARKET: return "drawings-market", "drawings"
        if n in c.D_TREES:  return "drawings-trees", "drawings"
        return "drawings-places", "drawings"
    if n in c.P_FLORIDA:   return "florida", "paintings"
    if n in c.P_BOTANICAL: return "botanical", "paintings"
    if n in c.P_MARKET:    return "market", "paintings"
    if n in c.P_STUDIES:   return "studies", "paintings"
    return "france", "paintings"                      # remaining colour works are Céret/Roussillon

GENERIC = {"pottery":"Bowl","prints":"Linocut","collage":"Collage",
           "drawings":"Drawing","paintings":"Study"}

cat = json.load(open(os.path.join(root, cat_path)))
existing = {a["id"] for a in cat["artworks"]}
by_series_count = {}

# collections: existing trip series all belong to "paintings"
for s in cat["series"]:
    s.setdefault("collection", "paintings")
cat["collections"] = [{"id": i, "name": n, "blurb": b} for i, n, b in COLLECTIONS]
have = {s["id"] for s in cat["series"]}
for sid, name, blurb, coll in NEW_SERIES:
    if sid not in have:
        cat["series"].append({"id": sid, "name": name, "blurb": blurb, "collection": coll})
sname = {s["id"]: s["name"] for s in cat["series"]}

added = 0
for n in ALL:
    aid = f"a{n:03d}"
    if aid in existing: continue
    sid, coll = series_of(n)
    medium, sizes, desc = SPEC[coll]
    size, price = sizes[n % len(sizes)]
    place, date = c.PLACES.get(n, ("", ""))
    if not place and coll in ("paintings", "drawings") and sid in ("france","drawings-places","drawings-trees","drawings-market","studies","botanical","market"):
        place = "Céret, France" if sid in ("france","drawings-places") else ""
    by_series_count[sid] = by_series_count.get(sid, 0) + 1
    title = c.TITLES.get(n) or f"{GENERIC[coll]} {by_series_count[sid]}"
    f = os.path.join(root, f"img/large/{aid}.jpg")
    out = subprocess.run(["sips","-g","pixelWidth","-g","pixelHeight",f], capture_output=True, text=True).stdout
    w = int(out.split("pixelWidth:")[1].split()[0]); h = int(out.split("pixelHeight:")[1].split()[0])
    cat["artworks"].append({
        "id": aid, "title": title, "place": place, "series": sid, "seriesName": sname[sid],
        "collection": coll, "year": int(date[-4:]) if date[-4:].isdigit() else 0,
        "date": date, "medium": medium, "size": size, "price": price,
        "status": "available", "featured": n in FEATURED,
        "description": desc,
        "image": {"large": f"{prefix}img/large/{aid}.jpg", "thumb": f"{prefix}img/thumb/{aid}.jpg", "w": w, "h": h},
    })
    added += 1

for a in cat["artworks"]:
    a.setdefault("collection", "paintings")
json.dump(cat, open(os.path.join(root, cat_path), "w"), indent=1, ensure_ascii=False)
print(f"{cat_path}: added {added}, total {len(cat['artworks'])}")
