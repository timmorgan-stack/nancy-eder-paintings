#!/usr/bin/env python3
"""Import the second 'Art and Pottery' drop. Ids are bNNN (the folder was re-exported and
renumbered between drops, so aNNN and bNNN refer to different exports).
Usage: python3 tools/build_batch2.py <catalog.json> <img-prefix> <new-ids.json>"""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify_batch2 as c

cat_path, prefix, newmap = sys.argv[1], sys.argv[2], sys.argv[3]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/timmorgan/Desktop/Claude/Nancy Eder/Art and Pottery/Nancy_artwork_and_pottery - %d.jpeg"

NEW = sorted(set(json.load(open(newmap))["new"]) - set(c.EXCLUDE))

NEW_SERIES = [
 ("maine",      "Maine & Acadia", "Acadia, Mount Desert Island and the Schoodic Peninsula.", "paintings"),
 ("trees",      "Trees & Woods",  "Trunks, branches and the light between them.",            "paintings"),
 ("landscapes", "Landscapes",     "Hills, fields and coast — place not recorded.",           "paintings"),
]
SPEC = {
 "paintings": ("Ink and gouache on paper",
   [("8 × 10 in",275),("9 × 12 in",325),("11 × 14 in",425),("12 × 16 in",550)],
   "Painted on location in gouache and ink. Sold unframed; ships flat, protected between archival boards."),
 "drawings": ("Pen and ink on paper",
   [("8 × 10 in",180),("9 × 12 in",220),("11 × 14 in",280)],
   "Drawn directly in ink, without pencil first — one sitting, no reworking. Sold unframed; ships flat."),
 "prints": ("Linocut on paper",
   [("8 × 10 in",120),("11 × 14 in",160)],
   "A linocut cut and printed by the artist, each impression inked and coloured by hand, so no two are identical."),
 "collage": ("Mixed media collage on paper",
   [("11 × 14 in",395),("12 × 16 in",475)],
   "Torn paper, paint and printed fragments built up into a landscape. Sold unframed; ships flat."),
}
FEATURED = {293, 295, 281, 265, 188, 260, 197, 226, 291, 256}

def series_of(n):
    if n in c.PRINTS:   return "prints", "prints"
    if n in c.COLLAGE:  return "collage", "collage"
    if n in c.DRAWINGS: return "drawings-places", "drawings"
    if n in c.P_MARKET:    return "market", "paintings"
    if n in c.P_BOTANICAL: return "botanical", "paintings"
    if n in c.P_TREES:     return "trees", "paintings"
    if n in c.P_MAINE:     return "maine", "paintings"
    if n in c.P_FLORIDA:   return "florida", "paintings"
    if n in c.P_STUDIES:   return "studies", "paintings"
    return "landscapes", "paintings"

GENERIC = {"prints":"Linocut","collage":"Collage","drawings":"Drawing","paintings":"Study"}

cat = json.load(open(os.path.join(root, cat_path)))
have = {s["id"] for s in cat["series"]}
for sid, name, blurb, coll in NEW_SERIES:
    if sid not in have:
        cat["series"].append({"id": sid, "name": name, "blurb": blurb, "collection": coll})
sname = {s["id"]: s["name"] for s in cat["series"]}
existing = {a["id"] for a in cat["artworks"]}
counter = {}
for a in cat["artworks"]:
    counter[a["series"]] = counter.get(a["series"], 0) + 1

added = 0
for n in NEW:
    aid = f"b{n:03d}"
    if aid in existing: continue
    sid, coll = series_of(n)
    medium, sizes, desc = SPEC[coll]
    size, price = sizes[n % len(sizes)]
    place, date = c.PLACES.get(n, ("", ""))
    counter[sid] = counter.get(sid, 0) + 1
    title = c.TITLES.get(n) or f"{GENERIC[coll]} {counter[sid]}"
    subprocess.run(["sips","-Z","1800","-s","format","jpeg","-s","formatOptions","82",
                    SRC % n,"--out", os.path.join(root, f"img/large/{aid}.jpg")], capture_output=True)
    subprocess.run(["sips","-Z","700","-s","format","jpeg","-s","formatOptions","80",
                    SRC % n,"--out", os.path.join(root, f"img/thumb/{aid}.jpg")], capture_output=True)
    out = subprocess.run(["sips","-g","pixelWidth","-g","pixelHeight",
                          os.path.join(root, f"img/large/{aid}.jpg")], capture_output=True, text=True).stdout
    w = int(out.split("pixelWidth:")[1].split()[0]); h = int(out.split("pixelHeight:")[1].split()[0])
    cat["artworks"].append({
        "id": aid, "title": title, "place": place, "series": sid, "seriesName": sname[sid],
        "collection": coll, "year": int(date[-4:]) if date[-4:].isdigit() else 0,
        "date": date, "medium": medium, "size": size, "price": price,
        "status": "available", "featured": n in FEATURED, "description": desc,
        "image": {"large": f"{prefix}img/large/{aid}.jpg", "thumb": f"{prefix}img/thumb/{aid}.jpg", "w": w, "h": h},
    })
    added += 1

json.dump(cat, open(os.path.join(root, cat_path), "w"), indent=1, ensure_ascii=False)
print(f"{cat_path}: added {added}, total {len(cat['artworks'])}")
