# Nancy Eder — Paintings (static site)

Contemporary portfolio + shop for Nancy Orans Eder's ink-and-watercolour sketchbook paintings.
Pure HTML/CSS/JS, no build step, catalogue-driven from one JSON file. Built to be lifted into
codanomix later — every integration point is marked.

## Run locally

```bash
python3 -m http.server 8791 --directory /Users/timmorgan/Desktop/Claude/nancy-eder-site
```
Then open http://localhost:8791/ (a `nancy` entry is also in `.claude/launch.json`).

## Pages

| Page | What it does |
|---|---|
| `index.html` | Hero, featured works, browse-by-trip tiles, buying info, newsletter (placeholder) |
| `gallery.html` | Work: sketchbook (trip) tiles + search at top; overview shows 6 per trip with “View all”; opening a trip gives a paginated grid (10/20/40/all per page, remembered), availability + sort, sticky chip bar with search, prev/next sketchbook. Search is scoped to the open sketchbook (with a “search everything” link). URL-synced: `?series=portugal&q=porto&status=available&sort=price-asc&per=20&page=2`; `?view=<id>` deep-links the lightbox |
| `artwork.html?id=<id>` | Single work: large image (click → lightbox/zoom), specs, price, add-to-cart / enquire, related works |
| `about.html` | Portrait of Nancy (`img/site/nancy-eder-portrait.jpg`) + artist statement (**placeholder copy — Nancy to replace**), stats, a rotating featured painting (random landscape work each visit), `#shipping` policy section |
| `contact.html` | Enquiry form (mailto fallback), prefillable via `?ref=NE-5613&subject=commission` |
| `cart.html` | localStorage cart (`ne_cart_v1`), one-of-a-kind items so qty is always 1 |
| `checkout.html` | Contact + shipping form, order summary, **payment placeholder** (`#payment-element`) |
| `thanks.html` | Order confirmation, reads `sessionStorage.ne_last_order` |

## Deep links / anchors
Home: `#featured`, `#sketchbooks`, `#buying`, `#newsletter`. Work overview: `gallery.html#cuba|france|spain|portugal|italy|england|norway`
(anchors are honoured after the JS render, with an offset for the sticky header). Trip view: `gallery.html?series=portugal`.

## Lightbox
`js/lightbox.js` — any `[data-lightbox="<id>"]` opens it over the current gallery set. Prev/next
(buttons, ← →, swipe), Esc/backdrop/swipe-down to close, click image to zoom (scroll to pan),
neighbours preloaded, thumb shown while large loads, add-to-cart from inside.

## Catalogue — `data/catalog.json`
```json
{ "id": "5613", "title": "Hurrying Café in Porto", "place": "Porto, Portugal",
  "series": "portugal", "seriesName": "Portugal", "year": 2016, "date": "July 2016",
  "medium": "Ink and watercolour on paper", "size": "9 × 12 in", "price": 325,
  "status": "available" | "sold", "featured": true, "description": "…",
  "image": { "large": "img/large/5613.jpg", "thumb": "img/thumb/5613.jpg", "w": 1800, "h": 1350 } }
```
* Titles / places / dates were transcribed from Nancy's handwritten captions on each painting.
  Three had none (5667 "Squash Blossoms", 5673 "France, Two Skies", 5604 "Norway") — worth confirming.
  Reference `NE-<id>` matches the original `IMG_<id>.jpg` filename.
* **Sizes and prices are placeholders** (random from 8×10 $275 · 9×12 $325 · 11×14 $425 · 12×16 $550,
  diptychs $475). Five works are marked `sold` purely to demo the state (5567, 5599, 5617, 5628, 5658).
* Series = trip: cuba, france, spain, portugal, italy, england, norway. `series[].blurb` is available for a strip caption.
* Images: `img/large` (1800px, ~700 KB) and `img/thumb` (700px). 5674 dropped (duplicate of 5673).

## codanomix integration map
Everything the CMS needs to own is tagged; nothing else needs to change.

| Hook | Where | Replace with |
|---|---|---|
| `data-region="header"` / `"footer"` | every page | rendered chrome (currently injected by `NE.renderHeader/renderFooter` in `js/app.js`) |
| `data-hook="primary-nav"` | header | nav from the CMS |
| `data-hook="hero"`, `"featured"`, `"series"`, `"buying"`, `"newsletter"` | index | page sections / widgets |
| `data/catalog.json` | fetched by `NE.loadCatalog()` | an endpoint returning the same shape (or a DB-backed JSON) |
| `data-hook="enquiry-form"` | contact | POST to the mailer; the mailto block is the only thing to swap |
| `data-hook="newsletter-form"` | index | list signup |
| `data-hook="checkout-form"` + `#payment-element[data-hook="payment-element"]` | checkout | mount the payment provider element here; the submit handler currently simulates success and redirects to `thanks.html` after writing `ne_last_order` |
| `NE.cart.*` (`js/app.js`) | all | server-side cart/reservation if you want holds; today it's localStorage only |
| `NE.SHIPPING_FLAT` | `js/app.js` | shipping rules ($25 US flat; non-US shows "quoted") |

Field names in checkout (`firstName`, `lastName`, `email`, `phone`, `address1`, `address2`, `city`,
`state`, `postalCode`, `country`, `notes`) map 1:1 to a normal order record.

## Still placeholder / to confirm with Nancy
* About-page statement, contact email (`hello@nancyeder.com`), studio location line
* Sizes, prices, sold status, which works are `featured`
* Shipping/returns policy wording ($25 flat, 14-day returns)
* Newsletter and payments are UI-only until wired
