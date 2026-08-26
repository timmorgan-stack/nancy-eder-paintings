# Nancy Eder — v2 (updated with real biography)

A **separate** updated version of the site, deployed alongside the original so the two can be
compared. Same code and features; the changes are factual and editorial.

* Original: https://timmorgan-stack.github.io/nancy-eder-paintings/
* This version: https://timmorgan-stack.github.io/nancy-eder-paintings/v2/

It shares the image folder with the original (paths are `../img/...`), so nothing is duplicated.
If v2 is adopted, promote these files to the repo root and change `../img/` back to `img/`
(in `*.html` and `data/catalog.json`, then re-run `python3 tools/build_catalog_js.py`).

## What changed, and where each fact came from

| Change | Source |
|---|---|
| Medium is now **"Ink and gouache on paper"** (was "ink and watercolour") across all 113 works and all page copy | Her LinkedIn lists her practice as **"Gouache Landscapes"** |
| Real biography on About — Antioch College (BA), New York University (MA); potter, art teacher, mediator for the Brooklyn courts, NYU administrator | LinkedIn + SoHo Memory Project |
| "Divides her time between New York and the south of France"; studio line now says **New York** | LinkedIn: *"Ceret, France — New York, United States"*, *"Landscape Painter in France and Spain"* |
| Exhibition credit: **Céret, France, August 2015** | LinkedIn ("Gouache Landscapes", Jul 2015–present) |
| New **"The Village years"** section: 3 Washington Square Village 1968–2007, two sons, $325/month in 1968, watching Picasso's *Bust of Sylvette* go up opposite; pull quote *"Living in the Village was my dream come true"* and the line about *"the treasures tossed and found on the street curbs"*, credited and linked to the SoHo Memory Project | https://sohomemory.org/nancy-eder/ |
| Timeline strip (1968 → today) and `#village` anchor | derived from the above |
| Home hero + meta descriptions rewritten around gouache landscapes and New York/France | as above |

## Deliberately left out
* The Etan Patz passage from the SoHo Memory Project interview — a real child's abduction; not
  appropriate on a gallery/sales page.
* Her reason for leaving NYU housing (a grievance about retirement policy) — negative framing that
  adds nothing here.
* Her sons' names/schooling beyond the bare fact that she raised two sons there.

## The 'Art and Pottery' drop (170 images)

Added from `~/Desktop/Claude/Nancy Eder/Art and Pottery`. Classified by eye from contact sheets;
the map lives in `tools/classify_art_pottery.py`, and `tools/build_new_works.py` turns it into
catalogue entries. 148 works catalogued, 22 images left out.

| Collection | Works | Series |
|---|---|---|
| Paintings | 168 | the 7 sketchbook trips + Leaves & Gardens, Florida, Markets & Table, Colour Studies |
| Drawings | 74 | Places & Streets, Trees Gardens & Leaves, Markets & Still Life |
| Prints | 4 | Linocuts |
| Pottery | 12 | Bowls & Vessels |
| Collage | 3 | Mixed Media |

**Left out (22)** — all photographs rather than works: places, buildings, rooftops, a palm, a
carousel, market and food shots, two pictures of cards on a market table, and one composite that
just duplicates two works already catalogued. One studio photograph was kept but as a *site asset*
(`img/site/nancy-eder-studio.jpg`, used on About), not as a gallery work.

**Gallery structure changed** to carry this: browsing is now Collections → Series → Works.
`data/catalog.json` gained a `collections` array, and every series and artwork carries a
`collection`. New-work ids are `aNNN` (reference `NE-aNNN`), matching the source filename number.

## Second drop (2026-08-26, +137 works)

The source folder was **re-exported and renumbered** between drops, so filenames no longer identify
a work. Already-imported images are found by perceptual hash (`ahash`) against `img/thumb/`, not by
name — matched distances were ≤4, unmatched ≥13, so the split is unambiguous. Ids from the first
drop are `aNNN`; this drop is `bNNN`. **Neither number will survive another re-export** — match by
content, don't trust the filename.

Map in `tools/classify_batch2.py`, importer in `tools/build_batch2.py`.
New series: **Maine & Acadia** (Acadia, Mount Desert Island, Schoodic Peninsula — several signed 2024),
**Trees & Woods**, **Landscapes** (used where no place is recorded, so the site doesn't claim one).
Collage went 3 → 31 and Prints 4 → 12.

**Left out of this drop (45):**
* 38 photographs — places, food, market stalls, a museum wall label, and family/friends snapshots.
* **3 paintings by other artists**, photographed in gilt frames at a museum (nos. 235–237 of that
  export). They are not Nancy's work and must not be listed as hers.
* 4 composites — several works in one photograph, so not sellable as a single piece.
* **One photograph of personal insurance documents** showing her name, member numbers and dates.
  Not imported. **It should be deleted from the source folder** — it doesn't belong in a folder
  that gets handed to anyone building the site.

## Third drop (+48 works, 446 total)

52 files arrived alongside the others, named `... - N (1).jpeg`. All 52 were confirmed new content
by perceptual hash, but **two turned out to be re-photographs of works already listed** (different
crop and lighting, so the hash missed them) — caught by eye and excluded. Also out: one composite
and one worktable photo. New series **Run, Rabbit, Run** (21 linocut-and-gouache collages), plus
Cuba, Spain and Céret paintings from 2017–2019 with the artist's captions.

Map in `tools/classify_batch3.py`, importer in `tools/build_batch3.py`. Ids are `cNNN`.

## Sketchbooks — the second way through the work

`tools/build_sketchbooks.py` adds a `sketchbook` field and a `sketchbooks` array to the catalogue.
It is **supplementary to, and independent of, the collections**: collections group by *medium*
(Paintings, Drawings, Prints, Pottery, Collage), sketchbooks group by *place*, so one sketchbook
holds paintings and drawings and prints from the same trip together.

* Nine sketchbooks: Cuba, France & the Roussillon, Spain, Portugal, Italy, England, Norway,
  Maine & Acadia, Florida — 208 of 446 works.
* Assignment is from the **recorded place first**, series second (several works sit in the France
  series but were painted in Spain — place wins). Works with no identifiable place are simply left
  out of this navigation rather than guessed into a trip.
* URLs: `?sketchbook=cuba`, and `?sketchbook=france&collection=drawings` to pin one to a medium.
* Re-run it after any import: `python3 tools/build_sketchbooks.py v2/data/catalog.json`.

## Marking work sold

`status` on each artwork is `"available"` or `"sold"`. Use the tool rather than hand-editing —
it rewrites `data/catalog.json` **and** regenerates `data/catalog.js` in one go:

```bash
python3 tools/mark_sold.py a121 c039        # mark these sold (ids are the NE- reference, minus the prefix)
python3 tools/mark_sold.py --available a121 # put one back on sale
python3 tools/mark_sold.py --list           # what's sold right now
python3 tools/mark_sold.py --sample 2       # demo data: N per collection, resets everything else
```

**Two per collection are currently marked sold as samples** (via `--sample 2`) so the state is
visible everywhere — change them whenever the real ones are known.

What a sold work does:
* grid card gets a **SOLD** badge and the price is replaced with "Sold";
* the artwork page shows the badge, drops the price, hides the shipping note, and swaps
  *Add to cart* for *Ask about a similar piece* (pre-filled contact form);
* the lightbox shows "Sold" and no cart button;
* it is excluded from the home hero, the featured three and the About page's rotating painting;
* the availability filter (`?status=sold` / `?status=available`) works in every gallery view.

Because these are one-offs, the cart is defensive: `NE.cart.add()` refuses a sold work outright,
and `NE.cart.prune()` — called on both the cart and checkout pages — silently drops anything that
sold while it sat in a visitor's cart, telling them which work it was. Checkout bounces back to the
cart if that happens, so a sold original can't be bought twice.

## Still to confirm with Nancy
* **Gouache vs watercolour per work** — the catalogue now says gouache for everything; some pages
  are plainly watercolour washes. Ideally each work is tagged individually.
* Whether she wants the Village material on the site at all, and the SoHo Memory Project quotes used.
* Sizes, prices, sold status, contact email (`hello@nancyeder.com`) — unchanged placeholders.
* The three uncaptioned works (5667, 5673, 5604).
* **Titles for the new drop** — about half carry her handwritten caption (transcribed verbatim);
  the rest are placeholders like "Bowl 4" or "Study 7" and need her names.
* **Prices and sizes for the new work are placeholders**: drawings $180–280, linocuts $120–160,
  pottery $85–165, collage $395–475. Pottery sizes are guessed diameters — they need measuring.
* Whether the linocuts are **editioned** (the description says each is hand-coloured and unique).
* Two works (a047, a135) look like framed/board paintings rather than sketchbook pages — worth
  checking their medium.
* **Maine & Acadia**: only 7 of the 11 carry a caption naming the place; the other 4 were grouped by
  eye from the same body of work and may belong elsewhere.
* **Landscapes** (17 works) is a holding series for paintings with no recorded place — most are
  probably Céret or Maine, but they need her to say which.
* The tropical foliage studies (agaves, palms, fronds) are in **Leaves & Gardens**; several are
  likely Florida and could move there.
* Collage vs painting is a judgement call on about a dozen pieces where torn paper and gouache are
  mixed — worth her eye.
* **238 works have no sketchbook** because no place is recorded — the botanical studies, the
  markets, the pottery, the rabbit collages. If she can place any of them, they join a sketchbook
  automatically on the next run.
* Watch the **repo size**: the images are now ~350 MB and the history about the same. Another drop
  or two and this wants Git LFS or an image CDN rather than plain Pages.
