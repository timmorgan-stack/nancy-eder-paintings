/* Nancy Eder — shared site runtime
   Loads the catalogue, renders header/footer, manages the cart (localStorage) and small UI helpers.
   Integration hooks for codanomix are marked with data-hook="…" attributes and window.NE.* APIs. */

document.documentElement.classList.add('js');
window.NE = (function () {
  const CART_KEY = 'ne_cart_v1';
  const SHIPPING_FLAT = 25;               // USD, domestic flat rate (placeholder)
  const state = { catalog: null, byId: new Map() };

  /* ---------- Money ---------- */
  const fmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  const money = (n) => fmt.format(n);

  /* ---------- Catalogue ---------- */
  async function loadCatalog() {
    if (state.catalog) return state.catalog;
    let data = window.NE_CATALOG;               // embedded copy (works from file:// too)
    if (!data) {
      const res = await fetch('data/catalog.json', { cache: 'no-cache' });
      data = await res.json();
    }
    state.catalog = data;
    data.artworks.forEach(a => state.byId.set(a.id, a));
    return data;
  }
  const getArt = (id) => state.byId.get(String(id));

  /* ---------- Cart ---------- */
  function readCart() {
    try { return JSON.parse(localStorage.getItem(CART_KEY) || '[]'); } catch { return []; }
  }
  function writeCart(ids) {
    localStorage.setItem(CART_KEY, JSON.stringify(ids));
    document.dispatchEvent(new CustomEvent('ne:cart', { detail: { ids } }));
    renderCartCount();
  }
  const cart = {
    ids: () => readCart(),
    has: (id) => readCart().includes(String(id)),
    add(id) {
      id = String(id);
      const ids = readCart();
      if (!ids.includes(id)) { ids.push(id); writeCart(ids); }
      return ids;
    },
    remove(id) { writeCart(readCart().filter(x => x !== String(id))); },
    clear() { writeCart([]); },
    items() { return readCart().map(getArt).filter(Boolean); },
    totals() {
      const items = this.items();
      const subtotal = items.reduce((s, a) => s + (a.price || 0), 0);
      const shipping = items.length ? SHIPPING_FLAT : 0;
      return { items, subtotal, shipping, total: subtotal + shipping };
    }
  };
  function renderCartCount() {
    const n = readCart().length;
    document.querySelectorAll('[data-cart-count]').forEach(el => {
      el.textContent = n; el.dataset.empty = n === 0 ? 'true' : 'false';
    });
  }

  /* ---------- Toast ---------- */
  let toastTimer;
  function toast(html, ms = 3200) {
    let el = document.querySelector('.toast');
    if (!el) { el = document.createElement('div'); el.className = 'toast'; el.setAttribute('role', 'status'); document.body.appendChild(el); }
    el.innerHTML = html;
    requestAnimationFrame(() => el.classList.add('is-on'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('is-on'), ms);
  }

  /* ---------- Chrome (header / footer) ---------- */
  const ICON_CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 7h12l1 13H5L6 7z"/><path d="M9 10V6a3 3 0 0 1 6 0v4"/></svg>';
  const ICON_ZOOM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M11 8v6M8 11h6"/></svg>';

  function renderHeader() {
    const host = document.querySelector('[data-region="header"]');
    if (!host) return;
    const page = document.body.dataset.page || '';
    const nav = [['gallery.html', 'Work', 'gallery'], ['about.html', 'About', 'about'], ['contact.html', 'Contact', 'contact']];
    host.innerHTML = `
      <header class="site-header" data-hook="site-header">
        <div class="wrap">
          <a class="brand" href="index.html" data-hook="brand">Nancy Eder <small>Paintings</small></a>
          <button class="nav-toggle" aria-label="Menu" aria-expanded="false" data-nav-toggle><span></span></button>
          <nav class="nav" data-hook="primary-nav" aria-label="Primary">
            ${nav.map(([href, label, key]) => `<a href="${href}" ${page === key ? 'aria-current="page"' : ''}>${label}</a>`).join('')}
            <a href="cart.html" class="cart-link" ${page === 'cart' ? 'aria-current="page"' : ''} aria-label="Cart">${ICON_CART}<span class="cart-label">Cart</span><span class="cart-count" data-cart-count data-empty="true">0</span></a>
          </nav>
        </div>
      </header>`;
    host.querySelector('[data-nav-toggle]').addEventListener('click', (e) => {
      const open = document.body.classList.toggle('nav-open');
      e.currentTarget.setAttribute('aria-expanded', open);
    });
  }

  function renderFooter() {
    const host = document.querySelector('[data-region="footer"]');
    if (!host) return;
    host.innerHTML = `
      <footer class="site-footer" data-hook="site-footer">
        <div class="wrap">
          <div class="cols">
            <div>
              <a class="brand" href="index.html">Nancy Eder</a>
              <p style="margin-top:12px;max-width:34ch">Gouache and ink landscapes, painted on location in France, Spain and beyond. Original works available to purchase.</p>
            </div>
            <div><h4>Explore</h4><ul>
              <li><a href="gallery.html">All work</a></li>
              <li><a href="gallery.html?status=available">Available</a></li>
              <li><a href="about.html">About the artist</a></li>
              <li><a href="about.html#village">The Village years</a></li>
            </ul></div>
            <div><h4>Buying</h4><ul>
              <li><a href="contact.html">Enquiries &amp; commissions</a></li>
              <li><a href="about.html#shipping">Shipping &amp; returns</a></li>
              <li><a href="cart.html">Cart</a></li>
            </ul></div>
            <div><h4>Follow</h4><ul>
              <li><a href="https://www.instagram.com/nancyoeder/" target="_blank" rel="noopener">Instagram</a></li>
              <li><a href="https://www.linkedin.com/in/nancy-eder-a63a3529/" target="_blank" rel="noopener">LinkedIn</a></li>
            </ul></div>
          </div>
          <div class="legal">
            <span>&copy; ${new Date().getFullYear()} Nancy Eder. All artwork and images are the copyright of the artist.</span>
            <span>Prices in USD.</span>
          </div>
        </div>
      </footer>`;
  }

  /* ---------- Cards ---------- */
  function cardHTML(a, opts = {}) {
    const { w, h } = a.image;
    const sold = a.status === 'sold';
    return `
      <article class="card reveal" data-id="${a.id}" style="--ar:${w} / ${h}">
        <a class="card__frame" href="artwork.html?id=${a.id}" aria-label="${a.title}">
          ${sold ? '<span class="badge badge--sold card__badge">Sold</span>' : ''}
          <img src="${a.image.thumb}" alt="${a.title}, ${a.medium}" width="${w}" height="${h}" loading="lazy" decoding="async">
        </a>
        <button class="card__zoom" data-lightbox="${a.id}" aria-label="View ${a.title} larger">${ICON_ZOOM}</button>
        <div class="card__meta">
          <div>
            <div class="card__title">${a.title}</div>
            <div class="card__sub">${a.place} · ${a.date}</div>
          </div>
          <div class="card__price">${sold ? '<span class="muted">Sold</span>' : money(a.price)}</div>
        </div>
      </article>`;
  }

  /* Masonry via grid row-span, computed from real heights after layout. */
  function layoutGrid(grid) {
    if (!grid) return;
    const rowH = parseFloat(getComputedStyle(grid).gridAutoRows) || 8;
    grid.querySelectorAll('.card').forEach(card => {
      card.style.gridRowEnd = 'span 1';
      const h = card.getBoundingClientRect().height + 28; // + vertical breathing room
      card.style.gridRowEnd = `span ${Math.ceil(h / rowH)}`;
    });
  }
  function watchGrid(grid) {
    if (!grid) return;
    const relayout = () => layoutGrid(grid);
    grid.querySelectorAll('img').forEach(img => { if (!img.complete) img.addEventListener('load', relayout, { once: true }); });
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(relayout, 80); });
    relayout();
    revealAll();
  }

  /* ---------- Reveal on scroll ----------
     Deliberately simple: position checks on scroll/resize + a hard fallback timer, so content
     can never be left hidden (IntersectionObserver is unreliable in embedded/background views). */
  function revealCheck() {
    const vh = window.innerHeight || 800;
    document.querySelectorAll('.reveal:not(.is-in)').forEach(e => {
      const r = e.getBoundingClientRect();
      if (r.top < vh * 0.96 && r.bottom > 0) e.classList.add('is-in');
    });
  }
  let revealBound = false;
  function revealAll() {
    if (!revealBound) {
      revealBound = true;
      ['scroll', 'resize', 'load'].forEach(ev => window.addEventListener(ev, () => requestAnimationFrame(revealCheck), { passive: true }));
    }
    revealCheck();
    requestAnimationFrame(revealCheck);
    setTimeout(revealCheck, 300);
    // Hard fallback: whatever hasn't animated in by now just shows.
    setTimeout(() => document.querySelectorAll('.reveal:not(.is-in)').forEach(e => e.classList.add('is-in')), 1500);
  }

  /* ---------- Query helpers ---------- */
  const qs = (k) => new URLSearchParams(location.search).get(k);
  const setQs = (obj) => {
    const p = new URLSearchParams(location.search);
    Object.entries(obj).forEach(([k, v]) => (v == null || v === '' || v === 'all') ? p.delete(k) : p.set(k, v));
    history.replaceState(null, '', (p.toString() ? `?${p}` : location.pathname) + location.hash);
  };

  /* ---------- Image loading state ----------
     Every <img> gets a quiet centred spinner behind it (on its parent) until it loads, then fades in.
     Works for images rendered later too (grids, cart) via a MutationObserver. Lightbox handles its own. */
  function watchImages(root = document) {
    root.querySelectorAll('img:not([data-ld]):not(.lb__img)').forEach(img => {
      img.dataset.ld = '1';
      const p = img.parentElement; if (!p) return;
      const done = () => { p.classList.remove('img-loading'); p.classList.add('is-loaded'); };
      if (img.complete && img.naturalWidth) { p.classList.add('is-loaded'); return; }
      p.classList.add('img-loading');
      img.addEventListener('load', done, { once: true });
      img.addEventListener('error', done, { once: true });
    });
  }
  new MutationObserver((muts) => {
    for (const m of muts) for (const n of m.addedNodes) if (n.nodeType === 1) { if (n.tagName === 'IMG') watchImages(n.parentElement || document); else if (n.querySelector) watchImages(n); }
  }).observe(document.documentElement, { childList: true, subtree: true });

  /* ---------- Hash jump for JS-rendered sections ---------- */
  function jumpToHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const go = () => {
      const el = document.getElementById(id); if (!el) return;
      const offset = parseFloat(getComputedStyle(el).scrollMarginTop) || 0;
      window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - offset, behavior: 'instant' }); // instant on load
    };
    go(); requestAnimationFrame(go); setTimeout(go, 250);
  }
  window.addEventListener('hashchange', jumpToHash);

  /* ---------- Boot ---------- */
  document.addEventListener('DOMContentLoaded', () => {
    renderHeader(); renderFooter(); renderCartCount(); revealAll(); watchImages();
    document.addEventListener('click', (e) => {
      const add = e.target.closest('[data-add-to-cart]');
      if (add) {
        const id = add.dataset.addToCart;
        cart.add(id);
        toast(`Added to cart · <a href="cart.html">View cart</a>`);
        document.querySelectorAll(`[data-add-to-cart="${id}"]`).forEach(b => { b.textContent = 'In cart — view'; b.setAttribute('href', 'cart.html'); b.removeAttribute('data-add-to-cart'); if (b.tagName === 'BUTTON') b.onclick = () => location.href = 'cart.html'; });
      }
    });
  });

  return { loadCatalog, getArt, cart, money, toast, cardHTML, layoutGrid, watchGrid, revealAll, jumpToHash, qs, setQs, ICON_ZOOM, SHIPPING_FLAT };
})();
