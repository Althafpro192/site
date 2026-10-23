/* ============================================================
   SMKN 8 JEMBER — main.js · interaksi & render data
   Satu IIFE, tanpa modul (type="module" gagal di file://).
   Banner: BOOT · OVERLAYS · RENDER · FORMS
   ============================================================ */
(function () {
  "use strict";

  /* data.js membawa semua key kecuali FULL; data-full.js (hanya berita.html)
     membawa window.ESKADATA_FULL. Merge ini toleran terhadap keduanya. */
  const D = Object.assign({}, window.ESKADATA, { FULL: (window.ESKADATA_FULL || (window.ESKADATA && window.ESKADATA.FULL) || {}) });
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  const htmlEl = document.documentElement;
  const RM = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- util ---------- */
  const BULAN = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"];
  const fmtDate = (iso) => {
    const [y, m, d] = (iso || "").split("-");
    return `${+d} ${BULAN[(+m || 1) - 1]} ${y}`;
  };
  const esc = (s) => String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  /* kutip lengkung + spasi ganda dinormalisasi agar PSH “TERATAI” selalu cocok */
  const normKey = (s) => String(s || "").replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/\s+/g, " ").trim().toUpperCase();
  const ICO = {
    clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    trophy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v6a5 5 0 0 1-10 0V4Z"/><path d="M7 6H4a2 2 0 0 0 2 4h1M17 6h3a2 2 0 0 1-2 4h-1"/></svg>',
  };
  const PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg>';
  const ytId = (u) => { const m = (u || "").match(/(?:embed\/|youtu\.be\/|watch\?v=)([\w-]{11})/); return m ? m[1] : null; };
  const ytblock = (id) => {
    const local = (D.VIDEOS || {})[id];
    if (local) return `<div class="ytblock playing"><video controls preload="metadata" referrerpolicy="strict-origin-when-cross-origin" poster="assets/img/yt_${id}.webp" src="${local}"></video></div>`;
    const thumb = (D.YTIDS || []).includes(id) ? `assets/img/yt_${id}.webp` : `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
    return `<div class="ytblock" data-yt="${id}"><img loading="lazy" decoding="async" src="${thumb}" alt="Sampul video YouTube"><span class="play">${PLAY}</span><span class="ytlabel">YouTube · klik untuk putar</span></div>`;
  };
  const pickChip = (wrap, b) => $$(".chip", wrap).forEach((x) => { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", String(x === b)); });

  /* ===== BOOT — preloader · nav · reveal · counter ===== */
  (function boot() {
    const el = $("#boot"), bar = $("#boot-bar"), pct = $("#boot-pct"), st = $("#boot-status");
    let done = false;
    const release = () => {
      if (done) return;
      done = true;
      htmlEl.classList.remove("is-loading");
      if (!el) return;
      el.classList.add("done");
      setTimeout(() => el.remove(), 700);
    };
    /* Stylesheet mengunci scroll hanya untuk html.js.is-loading, jadi .js di sini
       adalah sakelarnya: script gagal parse → halaman tetap bisa digulir. */
    htmlEl.classList.add("js");
    let revisited = null;
    try { revisited = sessionStorage.getItem("eskalaber-boot"); sessionStorage.setItem("eskalaber-boot", "1"); } catch (e) {}
    if (!el || RM || revisited) return release();
    let p = 0;
    const to = (v, msg) => {
      p = Math.max(p, v);
      if (bar) bar.style.width = p + "%";
      if (pct) pct.textContent = Math.round(p) + "%";
      if (msg && st) st.textContent = msg;
    };
    to(12, "Memuat konten…");
    if (document.fonts) document.fonts.ready.then(() => to(70));
    addEventListener("load", () => to(100), { once: true });
    ["click", "keydown", "touchstart"].forEach((ev) => addEventListener(ev, () => to(100), { once: true, passive: true }));
    /* Plafon keras: situs tidak menyandera pengunjung pada layar dekoratif. */
    setTimeout(() => to(100), 1200);
    const t = setInterval(() => { if (p >= 100) { clearInterval(t); release(); } }, 80);
  })();

  const nav = $("#nav"), burger = $("#burger"), mmenu = $("#mmenu"), totop = $("#totop");

  /* Satu pass rAF gabungan: nav, tombol atas, dan kedalaman hero semuanya
     dibaca dari siklus yang sama — tidak ada listener scroll kedua. Tanpa
     guard .js pada CSS, hook yang tak bertuan ini akan jadi ornamen mati. */
  const heroVisual = $(".hero-visual");
  const finePointer = matchMedia("(hover: hover) and (min-width: 900px)");
  let ticking = false, hx = 0, hy = 0;

  const paint = () => {
    ticking = false;
    nav && nav.classList.toggle("scrolled", scrollY > 12);
    totop && totop.classList.toggle("show", scrollY > 600);
    if (!heroVisual || RM || !finePointer.matches) return;
    const r = heroVisual.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;   // di luar layar: jangan menulis
    const prog = (innerHeight - r.top) / (innerHeight + r.height);
    heroVisual.style.setProperty("--sy", (prog * 26).toFixed(2));
    heroVisual.style.setProperty("--px", hx.toFixed(2));
    heroVisual.style.setProperty("--py", hy.toFixed(2));
  };
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(paint);
  };
  addEventListener("scroll", onScroll, { passive: true });
  if (heroVisual) heroVisual.addEventListener("pointermove", (e) => {
    if (RM || !finePointer.matches) return;
    const r = heroVisual.getBoundingClientRect();
    hx = ((e.clientX - r.left) / r.width - .5) * 12;
    hy = ((e.clientY - r.top) / r.height - .5) * 12;
  });
  paint();
  /* Tilt kartu: SATU listener delegasi untuk semua [data-tilt], bukan satu
     per kartu. --tx/--ty dibaca oleh aturan [data-tilt] di stylesheet; tanpa
     driver ini aturan itu cuma ornamen yang tak pernah menyala. */
  let tiltEl = null;
  addEventListener("pointermove", (e) => {
    if (RM || !finePointer.matches) return;
    const t = e.target && e.target.closest ? e.target.closest("[data-tilt]") : null;
    if (t !== tiltEl) {
      if (tiltEl) { tiltEl.style.removeProperty("--tx"); tiltEl.style.removeProperty("--ty"); }
      tiltEl = t;
      return;
    }
    if (!t) return;
    const r = t.getBoundingClientRect();
    t.style.setProperty("--ty", (((e.clientX - r.left) / r.width - .5) * 6).toFixed(2));
    t.style.setProperty("--tx", ((((e.clientY - r.top) / r.height - .5) * -6)).toFixed(2));
  }, { passive: true });

  burger && burger.addEventListener("click", () => {
    burger.classList.toggle("open"); mmenu && mmenu.classList.toggle("open");
  });
  $$("#mmenu a").forEach((a) => a.addEventListener("click", () => {
    burger.classList.remove("open"); mmenu && mmenu.classList.remove("open");
  }));
  totop && totop.addEventListener("click", () => scrollTo({ top: 0, behavior: RM ? "auto" : "smooth" }));

  /* Reveal + stagger. Satu-satunya penulisan style dari JS yang diizinkan adalah
     custom property runtime (--rd) dan pane.style.maxHeight accordion. */
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    const el = e.target, sibs = $$(".reveal", el.parentElement || document);
    el.style.setProperty("--rd", (sibs.indexOf(el) % 8) * 70 + "ms");
    el.classList.add("in"); io.unobserve(el);
  }), { threshold: 0.12 });
  /* Dipanggil lagi setelah tiap render list. Node yang sudah .in dilewati: list
     hasil render JS membawa class="reveal in" baked in, supaya filter dan
     paginasi tidak menganimasi ulang 9 kartu. */
  function observeReveals(root) {
    $$(".reveal", root || document).forEach((el) => {
      if (el.classList.contains("in")) return;
      if (RM) { el.classList.add("in"); return; }
      io.observe(el);
    });
  }
  observeReveals(document);

  const countUp = (el) => {
    const target = +el.dataset.count, suf = el.dataset.suffix || "";
    if (RM) { el.textContent = target.toLocaleString("id-ID") + suf; return; }  /* tanpa rAF sama sekali */
    const t0 = performance.now(), dur = 1400;
    const step = (t) => {
      const p = Math.min(1, (t - t0) / dur), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = v.toLocaleString("id-ID") + suf;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const cio = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    cio.unobserve(e.target); countUp(e.target);
  }), { threshold: 0.5 });
  $$("[data-count]").forEach((el) => cio.observe(el));

  /* ===== OVERLAYS — lightbox · videobox · reader =====
     Scroll-lock berupa stack: lightbox yang dibuka dari dalam reader tidak
     lagi membekukan halaman setelah ditutup. */
  const LOCK = [];
  const lock = (el) => { if (el && !LOCK.includes(el)) LOCK.push(el); htmlEl.classList.add("locked"); };
  const unlock = (el) => { const i = LOCK.indexOf(el); if (i > -1) LOCK.splice(i, 1); if (!LOCK.length) htmlEl.classList.remove("locked"); };
  const lb = $("#lightbox"), vbWrap = $("#vb-wrap"), vbox = $("#videobox"), reader = $("#reader");

  /* Siblings non-dialog di belakang dialog dibekukan dari pointer + a11y tree. */
  const syncInert = () => {
    const top = LOCK[LOCK.length - 1];
    $$("body > *").forEach((el) => {
      const keep = !top || el === top || el.contains(top);
      keep ? el.removeAttribute("inert") : el.setAttribute("inert", "");
    });
  };
  const focusables = (el) => $$('a[href], button:not([disabled]), input, select, textarea, video, iframe, [tabindex]:not([tabindex="-1"])', el)
    .filter((x) => x.offsetParent !== null || x === document.activeElement);
  const focusInto = (el) => {
    const f = focusables(el);
    if (f[0]) f[0].focus({ preventScroll: true }); else el.focus && el.focus({ preventScroll: true });
  };

  function openDialog(el) {
    if (!el) return;
    el.__opener = document.activeElement;
    el.classList.add("open"); lock(el); syncInert();
    focusInto(el);
  }
  function closeDialog(el) {
    if (!el || !el.classList.contains("open")) return;
    if (el === vbox && vbWrap) vbWrap.innerHTML = "";   /* tiap jalur tutup memutus audio */
    el.classList.remove("open"); unlock(el); syncInert();
    const op = el.__opener;
    el.__opener = null;
    if (op && document.contains(op) && op.focus) op.focus({ preventScroll: true });
    else if (LOCK.length) focusInto(LOCK[LOCK.length - 1]);  /* pemicunya sudah hilang → masuk dialog di bawahnya */
  }

  /* Chrome dialog dipasang dari JS — halaman yang belum ter-rewrite tetap aman. */
  [[lb, "lb-cap", "Galeri foto"], [vbox, "vb-cap", "Video"], [reader, "r-title", "Baca artikel"]].forEach(([el, labelId, fallback]) => {
    if (!el) return;
    el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); el.setAttribute("tabindex", "-1");
    if ($("#" + labelId)) el.setAttribute("aria-labelledby", labelId); else el.setAttribute("aria-label", fallback);
  });

  /* Satu keydown: hanya dialog paling atas yang tertutup (termasuk #videobox). */
  addEventListener("keydown", (e) => {
    const top = LOCK[LOCK.length - 1];
    if (!top) return;
    if (e.key === "Escape") { e.preventDefault(); closeDialog(top); return; }
    if (e.key !== "Tab") return;
    const f = focusables(top), first = f[0], last = f[f.length - 1], cur = document.activeElement;
    if (!f.length) { e.preventDefault(); top.focus && top.focus(); return; }
    if (!top.contains(cur)) { e.preventDefault(); (e.shiftKey ? last : first).focus(); return; }
    if (e.shiftKey && cur === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && cur === last) { e.preventDefault(); first.focus(); }
  });

  function openLB(item) {
    if (!lb) return;
    const img = $("#lb-img"), cap = $("#lb-cap");
    if (img) { img.src = item.b; img.alt = item.c || ""; }
    if (cap) cap.textContent = item.c || "";
    openDialog(lb);
  }
  lb && $$(".x", lb).forEach((x) => x.addEventListener("click", () => closeDialog(lb)));
  lb && lb.addEventListener("click", (e) => { if (e.target === lb || e.target.classList.contains("bg")) closeDialog(lb); });

  /* FULL = prosa HTML pihak pertama (artikel sekolah) yang disuntik apa adanya,
     hanya disaring dari <script>, handler on*= dan url javascript:. */
  const sanitize = (html) => String(html || "")
    .replace(/<script\b[\s\S]*?<\/script\s*>|<script\b[^>]*>|<\/script>/gi, "")
    .replace(/\son[a-z]+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)/gi, "")
    .replace(/\s(href|src)\s*=\s*(?:"|')\s*javascript:[^"']*(?:"|')/gi, ' $1="#"')
    .replace(/<a\b([^>]*\bhref="https?:\/\/[^"]*"[^>]*)>/gi, (m, a) => (/\brel=/i.test(a) ? m : `<a${a} rel="noopener" target="_blank">`));

  function openReader(n) {
    if (!reader || !n) return;
    const t = $("#r-title"), meta = $("#r-meta"), hero = $("#r-img"), body = $("#r-body");
    if (t) t.textContent = n.t;
    if (meta) meta.innerHTML = `<span>${fmtDate(n.d)}</span><span>•</span><span>${esc((n.c || []).join(", "))}</span>`;
    if (hero && n.i) hero.src = n.i;
    /* CSS menyembunyikan .heroimg lewat .reader:not(.has-img) — bukan style.display. */
    reader.classList.toggle("has-img", !!n.i);
    const embed = (m, u) => { const id = ytId(u); return id ? ytblock(id) : m; };
    const full = (D.FULL || {})[n.t];
    let html = full
      ? `<div class="content">${sanitize(full).replace(/<div class="video-embed" data-src="([^"]+)"><\/div>/g, embed)}</div>`
      : `<div class="content">${n.v ? ytblock(n.v) : ""}<p>${esc(n.x) || "Dokumentasi singkat kegiatan ini tersimpan di arsip redaksi Eskalaber."}</p></div>`;
    if (full) html = html.replace(/<a[^>]*href="(https?:\/\/(?:www\.)?(?:youtu\.be\/|youtube\.com\/watch\?v=|youtube\.com\/embed\/)[\w-]{11}[^"]*)"[^>]*>[\s\S]*?<\/a>/g, embed);
    if (n.v && !html.includes("ytblock")) html = ytblock(n.v) + html;
    if (body) body.innerHTML = html;
    openDialog(reader);
    const sheet = $(".sheet", reader);
    if (sheet) sheet.scrollTop = 0;
    observeReveals(reader);
  }

  function openVideo(id, cap) {
    if (!vbox || !vbWrap) return;
    const local = (D.VIDEOS || {})[id], RP = 'referrerpolicy="strict-origin-when-cross-origin"';
    vbWrap.innerHTML = local
      ? `<video controls autoplay ${RP} poster="assets/img/yt_${id}.webp" src="${local}"></video>`
      : `<iframe src="https://www.youtube.com/embed/${id}?autoplay=1" ${RP} title="${esc(cap)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
    const c = $("#vb-cap"); if (c) c.textContent = cap;
    openDialog(vbox);
  }
  vbox && $$(".x", vbox).forEach((x) => x.addEventListener("click", () => closeDialog(vbox)));
  vbox && vbox.addEventListener("click", (e) => { if (e.target === vbox || e.target.classList.contains("bg")) closeDialog(vbox); });
  reader && $("#r-close") && $("#r-close").addEventListener("click", () => closeDialog(reader));
  reader && reader.addEventListener("click", (e) => { if (e.target.classList.contains("bg")) closeDialog(reader); });

  /* Klik ter-delegasi: ytblock · video · dokumen · galeri · read. Reader hanya
     memotong navigasi di halaman yang bisa merendernya (berita.html); di halaman
     lain href asli dipakai → navigasi nyata, middle/copy-link tetap jujur. */
  const canReadHere = () => !!reader && !!newsGrid;
  document.addEventListener("click", (e) => {
    const y = e.target.closest(".ytblock");
    if (y && !y.classList.contains("playing")) {
      y.classList.add("playing");
      y.innerHTML = `<iframe src="https://www.youtube.com/embed/${y.dataset.yt}?autoplay=1" referrerpolicy="strict-origin-when-cross-origin" title="Video YouTube SMKN 8 Jember" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
      return;
    }
    const v = e.target.closest("[data-video]");
    if (v && vbox) {
      /* 4 tombol video duduk di luar .jcard → fallback eksplisit, bukan throw. */
      openVideo(v.dataset.video, v.closest(".jcard")?.querySelector("h3")?.textContent.trim() || "Video SMKN 8 Jember");
      return;
    }
    const doc = e.target.closest("[data-doc]");
    if (doc) { e.preventDefault(); openLB({ b: doc.dataset.doc, c: doc.dataset.cap || "" }); return; }
    const g = e.target.closest("#galeri-grid a[data-lb]");
    if (g) { e.preventDefault(); if (galList[+g.dataset.lb]) openLB(galList[+g.dataset.lb]); return; }
    const t = e.target.closest("[data-read]");
    if (!t || !canReadHere()) return;
    e.preventDefault();
    const N = D.NEWS || [];
    /* data-i = indeks global di D.NEWS: tak ambigu untuk 3 judul kembar "TTD
       Elektronik Lembar Pengesahan"; pencocokan judul hanya fallback. */
    const byI = t.dataset.i !== undefined ? N[+t.dataset.i] : null;
    const n = (byI && byI.t === t.dataset.read ? byI : null) || N.find((x) => x.t === t.dataset.read);
    if (n) openReader(n);
  });

  /* ===== RENDER — ticker · kartu · galeri · tabel · ekskul · prestasi ===== */
  const tickEl = $("#ticker-track");
  if (tickEl && D.NEWS) {
    /* Setengah kedua hanyalah ilusi marquee: aria-hidden, plus tabindex -1 agar
       konten tersembunyi tidak ikut urutan Tab. */
    const tk = (n, dup) => `<a class="tk" href="berita.html#${encodeURIComponent(n.t)}"${dup ? ' aria-hidden="true" tabindex="-1"' : ""}>${esc(n.t)}</a>`;
    const head = D.NEWS.slice(0, 8);
    tickEl.innerHTML = head.map((n) => tk(n)).join("") + head.map((n) => tk(n, true)).join("");
  }

  /* .ph memotong gambar pada 16/10 (aspect-ratio CSS); data.js tidak menyimpan
     dimensi per berkas, jadi atribut ini menyatakan kotak potongnya. */
  const IMG_W = 760, IMG_H = 475;
  const ncard = (n, feature, idx) => {
    const slug = encodeURIComponent(n.t);
    return `
    <article class="ncard reveal in${feature ? " feature" : ""}">
      <div class="ph"><img src="${n.i}" alt="" loading="lazy" decoding="async" width="${IMG_W}" height="${IMG_H}">${n.v ? `<span class="playbadge">${PLAY}</span>` : ""}<span class="cat">${esc((n.c || [])[0] || "Berita")}</span></div>
      <div class="body">
        <time>${ICO.clock} ${fmtDate(n.d)}</time>
        <h3><a href="berita.html#${slug}" data-read="${esc(n.t)}" data-i="${idx}">${esc(n.t)}</a></h3>
        <p>${esc(n.x) || "Baca selengkapnya untuk informasi lengkap kegiatan ini."}</p>
        <a class="more" href="berita.html#${slug}" data-read="${esc(n.t)}" data-i="${idx}">Baca selengkapnya ${ICO.arrow}</a>
      </div>
    </article>`;
  };

  const homeNews = $("#home-news");
  if (homeNews && D.NEWS) {
    homeNews.innerHTML = D.NEWS.slice(0, 7).map((n, i) => ncard(n, i === 0, i)).join("");
    observeReveals(homeNews);
  }

  /* ---------- halaman berita: filter + cari + paginasi + deep link ---------- */
  const newsGrid = $("#news-grid");
  if (newsGrid && D.NEWS) {
    const PER = 9;
    let cat = "Semua", q = "", page = 1;
    const ALL = D.NEWS.map((n, i) => ({ n, i }));   /* indeks global → data-i */
    const cats = ["Semua", ...new Set(D.NEWS.flatMap((n) => n.c || []))];
    const chipsEl = $("#news-chips"), pagerEl = $("#news-pager"), countEl = $("#news-count");
    if (chipsEl) chipsEl.innerHTML = cats.map((c) => `<button class="chip ${c === cat ? "on" : ""}" data-c="${esc(c)}" aria-pressed="${c === cat}">${esc(c)}</button>`).join("");
    chipsEl && chipsEl.addEventListener("click", (e) => {
      const b = e.target.closest(".chip"); if (!b) return;
      cat = b.dataset.c; page = 1; pickChip(chipsEl, b); draw();
    });
    const si = $("#news-search");
    si && si.addEventListener("input", () => { q = si.value.toLowerCase(); page = 1; draw(); });
    const filtered = () => ALL.filter(({ n }) => (cat === "Semua" || (n.c || []).includes(cat)) &&
      (!q || (n.t || "").toLowerCase().includes(q) || (n.x || "").toLowerCase().includes(q)));

    function draw() {
      const list = filtered(), pages = Math.max(1, Math.ceil(list.length / PER));
      page = Math.min(page, pages);
      if (countEl) countEl.textContent = `${list.length} artikel`;
      const slice = list.slice((page - 1) * PER, page * PER);
      newsGrid.innerHTML = slice.length ? slice.map(({ n, i }) => ncard(n, false, i)).join("")
        : `<div class="empty">Tidak ada artikel yang cocok. Coba kata kunci lain.</div>`;
      let btns = "", last = 0;
      const win = [];
      for (let i = 1; i <= pages; i++) if (i === 1 || i === pages || Math.abs(i - page) <= 1) win.push(i);
      win.forEach((i) => { if (i - last > 1) btns += `<button disabled>…</button>`; btns += `<button class="${i === page ? "on" : ""}" data-p="${i}" aria-current="${i === page ? "page" : "false"}">${i}</button>`; last = i; });
      if (pagerEl) pagerEl.innerHTML = `<button data-p="${page - 1}" ${page === 1 ? "disabled" : ""} aria-label="Halaman sebelumnya">‹</button>` + btns + `<button data-p="${page + 1}" ${page === pages ? "disabled" : ""} aria-label="Halaman berikutnya">›</button>`;
      observeReveals(newsGrid);
    }
    pagerEl && pagerEl.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-p]"); if (!b || b.disabled) return;
      page = +b.dataset.p; draw();
      newsGrid.scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "start" });
    });
    draw();
    /* Deep link: cold load DAN perubahan hash setelah load. Lewat hash, judul
       kembar tidak terbedakan → match pertama menang (by design). */
    const openFromHash = () => {
      if (location.hash.length < 3) return;
      let t;
      try { t = decodeURIComponent(location.hash.slice(1)); } catch (e) { return; }
      const hit = (D.NEWS || []).find((n) => n.t === t);
      if (hit) openReader(hit);
    };
    addEventListener("hashchange", openFromHash);
    if (location.hash.length > 2) setTimeout(openFromHash, 300);
  }

  /* ---------- galeri + lightbox ---------- */
  const gal = $("#galeri-grid");
  let galList = [];
  if (gal && D.GALLERY) {
    let g = "semua";
    const groups = ["semua", ...new Set(D.GALLERY.map((x) => x.g))];
    const wrap = $("#galeri-chips");
    const LABEL = { semua: "Semua", kegiatan: "Kegiatan", ekskul: "Ekstrakurikuler", jurusan: "Konsentrasi Keahlian", prestasi: "Prestasi", fasilitas: "Fasilitas", info: "Info & Desain" };
    if (wrap) wrap.innerHTML = groups.map((x) => `<button class="chip ${x === g ? "on" : ""}" data-g="${x}" aria-pressed="${x === g}">${esc(LABEL[x] || x)}</button>`).join("");
    const drawG = () => {
      galList = D.GALLERY.filter((x) => g === "semua" || x.g === g);
      /* href asli ke berkas besar → middle-click membuka foto penuh. */
      gal.innerHTML = galList.map((x, i) => `<a href="${esc(x.b)}" data-lb="${i}" data-gg="${esc(x.g)}" aria-label="Perbesar: ${esc(x.c)}"><img loading="lazy" decoding="async" src="${esc(x.s)}" alt="${esc(x.c)}"><span class="cap">${esc(x.c)}</span></a>`).join("");
      observeReveals(gal);
    };
    wrap && wrap.addEventListener("click", (e) => {
      const b = e.target.closest(".chip"); if (!b) return;
      g = b.dataset.g; pickChip(wrap, b); drawG();
    });
    drawG();
  }

  /* ---------- tabel data (.tablewrap > table.data) ----------
     89 baris TEACHERS berlebar 7, header dulu cuma 6 → kolom ke-5 salah label
     dan mata pelajaran (kolom 7) hilang. Satu const TEACHER_COLS dipakai render
     awal DAN pencarian lewat tableRows() yang sama: tidak bisa drift lagi. */
  const TEACHER_COLS = ["No", "Nama", "JK", "Almamater", "Tahun Lulus", "Jenjang", "Mata Pelajaran"];
  const tableRows = (rows, cols) => rows.map((r) => `<tr>${cols.map((_, i) => `<td>${esc(r[i] || "-")}</td>`).join("")}</tr>`).join("");
  function renderTable(sel, rows, cols) {
    const el = $(sel); if (!el || !rows) return null;
    el.innerHTML = `<table class="data"><thead><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${tableRows(rows, cols)}</tbody></table>`;
    return el;
  }
  const gwrap = renderTable("#guru-table", D.TEACHERS, TEACHER_COLS);
  renderTable("#karyawan-table", D.STAFF, ["No", "Nama", "Jenis Kelamin", "Jabatan / Tugas"]);
  const tsearch = $("#guru-search");
  tsearch && gwrap && tsearch.addEventListener("input", () => {
    const tb = gwrap.querySelector("tbody"); if (!tb) return;
    const s = tsearch.value.toLowerCase();
    const rows = (D.TEACHERS || []).filter((r) => r.join(" ").toLowerCase().includes(s));
    tb.innerHTML = tableRows(rows, TEACHER_COLS) || `<tr><td colspan="${TEACHER_COLS.length}" class="empty">Tidak ditemukan</td></tr>`;
  });

  /* ---------- ekskul ---------- */
  const xw = $("#ekskul-grid");
  if (xw && D.EKSUL) {
    /* Peta display-only tinggal di main.js: data.js payload hasil generate yang
       tertimpa pada regen berikutnya. Nilai [berkas, lebar, tinggi].
       SEPAK BOLA & BAHASA ASING sengaja tiada — fotonya tidak ada di assets/img/,
       jadi jatuh ke tile numeral .noico yang memang dirancang untuk itu. */
    const PH = {
      "PRAMUKA": ["PRAMUKA.webp", 1000, 562], "PRAMUKA REGULER": ["PRAMUKA.webp", 1000, 562],
      "PRAMUKA WAJIB": ["PRAMUKA.webp", 1000, 562], "FUTSAL": ["Futsal.webp", 1000, 469],
      "BOLA VOLI": ["Voli.webp", 1400, 787], "PENCAK ORGANISASI": ["PO.webp", 1000, 450],
      'PSH "TERATAI"': ["PSHT.webp", 1400, 1050], "BULU TANGKIS": ["badminton.webp", 1400, 645],
      "SENI MUSIK": ["ekskul-musik.webp", 1400, 787], "PADUAN SUARA": ["Paduan-Suara-scaled.webp", 1000, 561],
      "REMAJA MASJID": ["TARTIL-REMAS.webp", 1400, 1050], "HADRAH": ["HADRAH-scaled.webp", 1000, 750],
      "UKS DAN PMR": ["PMR.webp", 1280, 576], "PASKIBRA": ["PASKIB.webp", 1000, 562],
      "SENI TARI": ["Seni-Tari-.webp", 1080, 1080], "AEROMODELLING": ["aeromodelling-2.webp", 1280, 960],
    };
    xw.innerHTML = D.EKSUL.map((r, i) => {
      const nama = (r[1] || "").trim(), pembina = (r[2] || "").trim(), pic = PH[normKey(nama)];
      const thumb = pic ? `<img loading="lazy" decoding="async" src="assets/img/${pic[0]}" alt="${esc(nama)}" width="${pic[1]}" height="${pic[2]}">`
        : `<div class="noico">${String(i + 1).padStart(2, "0")}</div>`;
      return `<div class="xcard reveal in"><div>${thumb}</div><div><h3>${esc(nama)}</h3><p>Pembina: ${esc(pembina || "—")}</p></div></div>`;
    }).join("");
    observeReveals(xw);
  }

  /* ---------- prestasi ---------- */
  const pw = $("#prestasi-grid");
  if (pw && D.PRESTASI) {
    pw.innerHTML = D.PRESTASI.map((p) => `
      <div class="pcard reveal in">
        ${p.i ? `<img loading="lazy" decoding="async" src="${p.i}" alt="${esc(p.t)}">` : `<div class="tro">${ICO.trophy}</div>`}
        <div><h4>${esc(p.t)}</h4><p>${fmtDate(p.d)}</p></div>
      </div>`).join("");
    observeReveals(pw);
  }

  const mw = $("#mitra-list");
  if (mw && D.MITRA) mw.innerHTML = D.MITRA.map((m) => `<span>${esc(m)}</span>`).join("");
  const misiEl = $("#misi-list");
  if (misiEl && D.MISI) misiEl.innerHTML = D.MISI.map((x) => `<li>${esc(x)}</li>`).join("");
  const tujEl = $("#tujuan-list");
  if (tujEl && D.TUJUAN) tujEl.innerHTML = D.TUJUAN.map((x) => `<li>${esc(x)}</li>`).join("");
  const mouEl = $("#mou-table");
  if (mouEl && D.MOU) {
    mouEl.innerHTML = `<table class="data"><thead><tr><th>No</th><th>Nama Dunia Usaha / Industri</th><th>Bidang Usaha</th><th>Alamat</th></tr></thead><tbody>${D.MOU.map((r) => `<tr><td>${esc(r[0])}</td><td><b>${esc(r[1])}</b></td><td>${esc(r[2] || "-")}</td><td>${esc(r[3] || "-")}</td></tr>`).join("")}</tbody></table>`;
  }
  const plEl = $("#prestasi-lama");
  if (plEl && D.PRESTASI_LAMA) plEl.innerHTML = D.PRESTASI_LAMA.map((x) => `<span>${esc((x || "").trim())}</span>`).join("");

  /* ---------- accordion FAQ ----------
     pane.style.maxHeight dipertahankan (CSS bergantung padanya), ditambah
     aria-expanded dan re-measure saat resize agar tablet berotasi tak memotong teks. */
  let accSeq = 0;
  $$(".acc button").forEach((b) => {
    const acc = b.parentElement, pane = acc && $(".pane", acc);
    if (!pane) return;
    if (!pane.id) pane.id = "faq-" + (++accSeq);
    if (!b.getAttribute("aria-controls")) b.setAttribute("aria-controls", pane.id);
    b.setAttribute("aria-expanded", String(acc.classList.contains("open")));
    b.addEventListener("click", () => {
      const open = acc.classList.toggle("open");
      b.setAttribute("aria-expanded", String(open));
      pane.style.maxHeight = open ? pane.scrollHeight + "px" : "0";
    });
  });
  addEventListener("resize", () => $$(".acc.open .pane").forEach((p) => { p.style.maxHeight = p.scrollHeight + "px"; }));

  /* ===== THEME — terang selalu default, gelap opt-in eksplisit =====
     Atribut data-theme sudah dipasang theme-init di <head> sebelum
     paint, jadi tidak ada flash. .theme-fade hanya menghidupkan
     transisi pada daftar permukaan yang diizinkan oleh stylesheet. */
  (function theme() {
    const root = document.documentElement;
    const btn = $("#theme-toggle");
    if (!btn) return;
    const set = (t) => {
      root.classList.add("theme-fade");
      root.setAttribute("data-theme", t);
      btn.setAttribute("aria-pressed", String(t === "dark"));
      try { localStorage.setItem("eskalaber-theme", t); } catch (e) {}
      setTimeout(() => root.classList.remove("theme-fade"), 240);
    };
    btn.setAttribute("aria-pressed", String(root.getAttribute("data-theme") === "dark"));
    btn.addEventListener("click", () =>
      set(root.getAttribute("data-theme") === "dark" ? "light" : "dark"));
  })();

  /* ===== FORMS — form kontak (demo mailto) ===== */
  const cf = $("#kontak-form");
  cf && cf.addEventListener("submit", (e) => {
    e.preventDefault();
    const fd = new FormData(cf);
    const body = encodeURIComponent(`Nama: ${fd.get("nama")}\nEmail: ${fd.get("email")}\nSubjek: ${fd.get("subjek")}\n\n${fd.get("pesan")}`);
    const note = document.createElement("div");
    note.className = "form-note";
    note.setAttribute("role", "status");
    note.textContent = "Terima kasih! Aplikasi email Anda terbuka untuk mengirim pesan ke Humas SMKN 8 Jember.";
    cf.innerHTML = ""; cf.appendChild(note);   /* konfirmasi dulu, lalu serahkan ke mailto */
    location.href = `mailto:smknegeri08jember@gmail.com?subject=${encodeURIComponent(fd.get("subjek") || "Pesan Website")}&body=${body}`;
  });
})();
