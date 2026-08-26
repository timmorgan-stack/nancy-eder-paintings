#!/usr/bin/env python3
"""Mark works sold or available, and regenerate data/catalog.js.

  python3 tools/mark_sold.py 5613 a045 c040          # mark these sold
  python3 tools/mark_sold.py --available 5613        # put one back on sale
  python3 tools/mark_sold.py --list                  # show what's currently sold
  python3 tools/mark_sold.py --sample 2              # mark N per collection (demo data)

Ids are the reference shown on each artwork page, without the "NE-" prefix.
"""
import json, os, random, sys, subprocess

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(root, "data", "catalog.json")

def load(): return json.load(open(CAT))
def save(c):
    json.dump(c, open(CAT, "w"), indent=1, ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(root, "tools", "build_catalog_js.py")], check=True)

def main(argv):
    cat = load()
    by_id = {a["id"]: a for a in cat["artworks"]}

    if "--list" in argv:
        sold = [a for a in cat["artworks"] if a["status"] == "sold"]
        print(f"{len(sold)} sold")
        for a in sorted(sold, key=lambda x: (x["collection"], x["title"])):
            print(f"  {a['id']:<6} {a['collection']:<10} {a['title']}")
        return 0

    if "--sample" in argv:
        n = int(argv[argv.index("--sample") + 1])
        rng = random.Random(42)          # stable, so re-running doesn't churn the catalogue
        for a in cat["artworks"]: a["status"] = "available"
        for col in cat["collections"]:
            pool = [a for a in cat["artworks"] if a["collection"] == col["id"]]
            for a in rng.sample(pool, min(n, len(pool))): a["status"] = "sold"
        save(cat)
        sold = [a for a in cat["artworks"] if a["status"] == "sold"]
        print(f"marked {len(sold)} sold ({n} per collection)")
        for a in sold: print(f"  {a['id']:<6} {a['collection']:<10} {a['title']}")
        return 0

    status = "available" if "--available" in argv else "sold"
    ids = [x for x in argv if not x.startswith("-") and x != str(argv[argv.index("--sample") + 1] if "--sample" in argv else "")]
    if not ids:
        print(__doc__); return 1
    missing = [i for i in ids if i not in by_id]
    if missing:
        print(f"unknown id(s): {', '.join(missing)}"); return 1
    for i in ids:
        by_id[i]["status"] = status
        print(f"{i} -> {status}  ({by_id[i]['title']})")
    save(cat)
    return 0

sys.exit(main(sys.argv[1:]))
