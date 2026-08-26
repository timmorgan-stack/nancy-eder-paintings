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
