#!/usr/bin/env python3
"""Import the third drop (files named '... - N (1).jpeg'). Ids are cNNN."""
import json, subprocess, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify_batch3 as c

cat_path, prefix, listfile = sys.argv[1], sys.argv[2], sys.argv[3]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/timmorgan/Desktop/Claude/Nancy Eder/Art and Pottery/Nancy_artwork_and_pottery - %d (1).jpeg"
NUMS = sorted({int(re.search(r'- (\d+) \(1\)', f).group(1)) for f in json.load(open(listfile))} - set(c.EXCLUDE))

NEW_SERIES = [("rabbits", "Run, Rabbit, Run", "Linocut rabbits, cut up and collaged back together.", "collage")]
SPEC = {
 "paintings": ("Ink and gouache on paper",
   [("8 × 10 in",275),("9 × 12 in",325),("11 × 14 in",425),("12 × 16 in",550)],
   "Painted on location in gouache and ink. Sold unframed; ships flat, protected between archival boards."),
 "drawings": ("Pen and ink on paper", [("8 × 10 in",180),("9 × 12 in",220),("11 × 14 in",280)],
   "Drawn directly in ink, without pencil first — one sitting, no reworking. Sold unframed; ships flat."),
 "prints": ("Linocut on paper", [("8 × 10 in",120),("11 × 14 in",160)],
   "A linocut cut and printed by the artist, each impression inked and coloured by hand, so no two are identical."),
 "collage": ("Linocut and gouache collage on paper", [("11 × 14 in",395),("12 × 16 in",475)],
   "Hand-printed linocut, cut up and collaged with gouache — a one-off built from her own prints."),
}
FEATURED = {40, 7, 21, 26, 12, 33}

def series_of(n):
    if n in c.PRINTS:   return "prints", "prints"
    if n in c.DRAWINGS: return "drawings-places", "drawings"
    if n in c.RABBITS:  return "rabbits", "collage"
    if n in c.P_CUBA:   return "cuba", "paintings"
    if n in c.P_SPAIN:  return "spain", "paintings"
    if n in c.P_FRANCE: return "france", "paintings"
    if n in c.P_MARKET: return "market", "paintings"
    if n in c.P_BOTANY: return "botanical", "paintings"
    return "landscapes", "paintings"

GENERIC = {"prints":"Linocut","collage":"Rabbits","drawings":"Drawing","paintings":"Study"}
cat = json.load(open(os.path.join(root, cat_path)))
have = {s["id"] for s in cat["series"]}
for sid, name, blurb, coll in NEW_SERIES:
    if sid not in have: cat["series"].append({"id": sid, "name": name, "blurb": blurb, "collection": coll})
sname = {s["id"]: s["name"] for s in cat["series"]}
existing = {a["id"] for a in cat["artworks"]}
counter = {}
for a in cat["artworks"]: counter[a["series"]] = counter.get(a["series"], 0) + 1

added = 0
for n in NUMS:
    aid = f"c{n:03d}"
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
