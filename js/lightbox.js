/* Nancy Eder — Lightbox
   Usage: NE.lightbox.open(items, index)  where items = array of artwork objects.
   Any element with [data-lightbox="<id>"] opens the lightbox over the current gallery set
   (set via NE.lightbox.setItems, or defaults to the whole catalogue). */

(function () {
  const SVG = {
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    prev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
    next: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>'
  };

  let root, img, stage, counter, title, sub, price, actions, items = [], idx = 0, lastFocus;

  function build() {
    if (root) return;
    root = document.createElement('div');
    root.className = 'lb';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', 'Artwork viewer');
    root.innerHTML = `
      <div class="lb__counter" data-lb-counter></div>
      <button class="lb__btn lb__close" data-lb-close aria-label="Close">${SVG.close}</button>
      <button class="lb__btn lb__prev" data-lb-prev aria-label="Previous">${SVG.prev}</button>
      <button class="lb__btn lb__next" data-lb-next aria-label="Next">${SVG.next}</button>
      <div class="lb__stage" data-lb-stage>
        <img class="lb__img" data-lb-img alt="">
      </div>
      <div class="lb__bar">
        <div>
          <div class="lb__title" data-lb-title></div>
          <div class="lb__sub" data-lb-sub></div>
        </div>
        <div class="lb__actions" data-lb-actions></div>
      </div>`;
    document.body.appendChild(root);
    img = root.querySelector('[data-lb-img]');
    stage = root.querySelector('[data-lb-stage]');
    counter = root.querySelector('[data-lb-counter]');
    title = root.querySelector('[data-lb-title]');
    sub = root.querySelector('[data-lb-sub]');
    actions = root.querySelector('[data-lb-actions]');

    root.querySelector('[data-lb-close]').addEventListener('click', close);
    root.querySelector('[data-lb-prev]').addEventListener('click', () => step(-1));
    root.querySelector('[data-lb-next]').addEventListener('click', () => step(1));
    stage.addEventListener('click', (e) => { if (e.target === stage) close(); });
    img.addEventListener('click', toggleZoom);

    // Keyboard
    document.addEventListener('keydown', (e) => {
      if (!root.hasAttribute('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') step(1);
      else if (e.key === 'ArrowLeft') step(-1);
      else if (e.key === ' ' || e.key === 'Enter') { if (document.activeElement === img || document.activeElement === document.body) { e.preventDefault(); toggleZoom(); } }
    });

    // Touch swipe
    let sx = 0, sy = 0, moved = false;
    stage.addEventListener('touchstart', (e) => { const t = e.touches[0]; sx = t.clientX; sy = t.clientY; moved = false; }, { passive: true });
    stage.addEventListener('touchmove', () => { moved = true; }, { passive: true });
    stage.addEventListener('touchend', (e) => {
      if (root.classList.contains('is-zoomed')) return;
      const t = e.changedTouches[0]; const dx = t.clientX - sx, dy = t.clientY - sy;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) step(dx < 0 ? 1 : -1);
      else if (!moved && Math.abs(dy) > 80) close();
    });
  }

  function toggleZoom() {
    const zoomed = root.classList.toggle('is-zoomed');
    if (zoomed) {
      // Zoom to natural size (capped at 2.2× the fitted size), centre the viewport
      const fitW = img.getBoundingClientRect().width;
      requestAnimationFrame(() => {
        const nat = img.naturalWidth || fitW * 2;
        const target = Math.min(nat, fitW * 2.2);
        img.style.width = target + 'px';
        stage.scrollLeft = (stage.scrollWidth - stage.clientWidth) / 2;
        stage.scrollTop = (stage.scrollHeight - stage.clientHeight) / 2;
      });
    } else {
      img.style.width = '';
    }
  }

  function render() {
    const a = items[idx];
    if (!a) return;
    root.classList.remove('is-zoomed'); img.style.width = '';
    root.classList.add('is-loading');
    const large = new Image();
    large.onload = () => { img.src = a.image.large; root.classList.remove('is-loading'); };
    large.src = a.image.large;
    img.src = a.image.thumb; // instant placeholder
    img.alt = `${a.title} — ${a.medium}`;
    counter.textContent = `${idx + 1} / ${items.length}`;
    title.textContent = a.title;
    sub.textContent = `${a.place} · ${a.date} · ${a.medium}, ${a.size}`;
    const sold = a.status === 'sold';
    const inCart = NE.cart.has(a.id);
    actions.innerHTML = `
      <span class="lb__price">${sold ? 'Sold' : NE.money(a.price)}</span>
      <a class="btn btn--sm" href="artwork.html?id=${a.id}">Details</a>
      ${sold ? '' : (inCart
        ? `<a class="btn btn--sm btn--accent" href="cart.html">In cart — view</a>`
        : `<button class="btn btn--sm btn--accent" data-add-to-cart="${a.id}">Add to cart</button>`)}`;
    // preload neighbours
    [idx + 1, idx - 1].forEach(i => { const n = items[(i + items.length) % items.length]; if (n) { const p = new Image(); p.src = n.image.large; } });
    root.querySelector('[data-lb-prev]').style.visibility = items.length > 1 ? '' : 'hidden';
    root.querySelector('[data-lb-next]').style.visibility = items.length > 1 ? '' : 'hidden';
  }

  function step(d) { if (!items.length) return; idx = (idx + d + items.length) % items.length; render(); }

  function open(list, i = 0) {
    build();
    items = list; idx = i;
    lastFocus = document.activeElement;
    root.setAttribute('open', '');
    document.body.classList.add('lb-open');
    render();
    root.querySelector('[data-lb-close]').focus();
  }
  function close() {
    if (!root) return;
    root.removeAttribute('open');
    root.classList.remove('is-zoomed'); img.style.width = '';
    document.body.classList.remove('lb-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  let currentSet = null;
  function setItems(list) { currentSet = list; }

  // Delegate: any [data-lightbox] opener
  document.addEventListener('click', async (e) => {
    const t = e.target.closest('[data-lightbox]');
    if (!t) return;
    e.preventDefault();
    const id = t.dataset.lightbox;
    const cat = await NE.loadCatalog();
    const set = currentSet || cat.artworks;
    const i = Math.max(0, set.findIndex(a => a.id === id));
    open(set, i);
  });

  // Keep "add to cart" state fresh inside the lightbox
  document.addEventListener('ne:cart', () => { if (root && root.hasAttribute('open')) render(); });

  NE.lightbox = { open, close, setItems };
})();
