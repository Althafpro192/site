/* ============================================================
   SMKN 8 Jember — main.js
   Satu IIFE, tanpa modul (type="module" gagal di file://).
   Semua penulisan style dari JS dibatasi ke custom property,
   max-height akordeon, dan lebar bar boot.
   ============================================================ */
(function () {
  "use strict";

  var D = Object.assign({}, window.ESKADATA, {
    FULL: window.ESKADATA_FULL || (window.ESKADATA && window.ESKADATA.FULL) || {}
  });
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var BULAN = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"];

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function fmtDate(iso) {
    var p = String(iso || "").split("-");
    return p.length === 3 ? (+p[2]) + " " + BULAN[(+p[1] || 1) - 1] + " " + p[0] : (iso || "");
  }
  function ytId(u) {
    var m = String(u || "").match(/(?:embed\/|youtu\.be\/|watch\?v=)([\w-]{11})/);
    return m ? m[1] : null;
  }
  var PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg>';

  /* ---------- boot ---------- */
  (function boot() {
    var root = document.documentElement;
    var el = $("#boot"), bar = $("#boot-bar"), pct = $("#boot-pct"), st = $("#boot-status");
    var done = false;
    function release() {
      if (done) return;
      done = true;
      root.classList.remove("is-loading");
      if (!el) return;
      el.classList.add("is-done");
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 700);
    }
    /* Kunci gulir hanya berlaku untuk html.js.is-loading, jadi skrip yang
       gagal dimuat tidak akan pernah membekukan halaman. */
    root.classList.add("js");
    var seen = null;
    try { seen = sessionStorage.getItem("eskalaber-boot"); sessionStorage.setItem("eskalaber-boot", "1"); } catch (e) {}
    if (!el || RM || seen) return release();

    var p = 0;
    function to(v, msg) {
      p = Math.max(p, v);
      if (bar) bar.style.width = p + "%";
      if (pct) pct.textContent = Math.round(p) + "%";
      if (msg && st) st.textContent = msg;
    }
    to(14, "Menyiapkan halaman…");
    if (document.fonts) document.fonts.ready.then(function () { to(72); });
    window.addEventListener("load", function () { to(100); }, { once: true });
    ["click", "keydown", "touchstart"].forEach(function (ev) {
      window.addEventListener(ev, function () { to(100); }, { once: true, passive: true });
    });
    setTimeout(function () { to(100); }, 1100);
    var t = setInterval(function () { if (p >= 100) { clearInterval(t); release(); } }, 80);
  })();

  /* ---------- tema ---------- */
  (function theme() {
    var root = document.documentElement, btn = $("#theme-toggle");
    if (!btn) return;
    function sync() { btn.setAttribute("aria-pressed", String(root.getAttribute("data-theme") === "dark")); }
    sync();
    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("eskalaber-theme", next); } catch (e) {}
      sync();
    });
  })();

  /* ---------- drawer ---------- */
  (function drawer() {
    var btn = $("#burger"), panel = $("#drawer");
    if (!btn || !panel) return;
    btn.addEventListener("click", function () {
      var open = panel.classList.toggle("is-open");
      panel.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Tutup menu" : "Buka menu");
    });
    $$("a", panel).forEach(function (a) {
      a.addEventListener("click", function () {
        panel.classList.remove("is-open"); panel.hidden = true;
        btn.setAttribute("aria-expanded", "false");
      });
    });
  })();

  /* ---------- scroll: nav, totop, parallax ---------- */
  var totop = $("#totop");
  var heroStack = $(".hero__stack");
  var ticking = false, hx = 0, hy = 0;
  var fine = window.matchMedia("(hover: hover) and (min-width: 900px)");

  function paint() {
    ticking = false;
    if (totop) totop.classList.toggle("is-show", window.scrollY > 700);
    if (!heroStack || RM || !fine.matches) return;
    var r = heroStack.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight) return;
    var prog = (window.innerHeight - r.top) / (window.innerHeight + r.height);
    heroStack.style.transform = "rotateX(" + ((prog - .5) * 5).toFixed(2) + "deg) rotateY(" + (hx * .5).toFixed(2) + "deg)";
  }
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(paint);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  if (heroStack && fine.matches && !RM) {
    heroStack.addEventListener("pointermove", function (e) {
      var r = heroStack.getBoundingClientRect();
      hx = ((e.clientX - r.left) / r.width - .5) * 8;
      hy = ((e.clientY - r.top) / r.height - .5) * 8;
    });
  }
  paint();
  if (totop) totop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: RM ? "auto" : "smooth" });
  });

  /* ---------- reveal ---------- */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-in");
      io.unobserve(e.target);
    });
  }, { threshold: .12, rootMargin: "0px 0px -6% 0px" }) : null;

  function observe(root) {
    var nodes = $$(".reveal:not(.is-in)", root || document);
    if (!io) { nodes.forEach(function (n) { n.classList.add("is-in"); }); return; }
    nodes.forEach(function (n) { io.observe(n); });
  }
  observe();

  /* ---------- tilt ---------- */
  if (fine.matches && !RM) {
    var tilt = null;
    document.addEventListener("pointermove", function (e) {
      var t = e.target && e.target.closest ? e.target.closest("[data-tilt]") : null;
      if (t !== tilt) {
        if (tilt) tilt.classList.remove("is-tilt");
        tilt = t;
        if (tilt) tilt.classList.add("is-tilt");
        return;
      }
      if (!t) return;
      var r = t.getBoundingClientRect();
      t.style.setProperty("--ty", (((e.clientX - r.left) / r.width - .5) * 5).toFixed(2) + "deg");
      t.style.setProperty("--tx", (((e.clientY - r.top) / r.height - .5) * -5).toFixed(2) + "deg");
    }, { passive: true });
  }

  /* ---------- counter ---------- */
  (function counters() {
    var nodes = $$("[data-count]");
    if (!nodes.length) return;
    if (RM || !("IntersectionObserver" in window)) {
      nodes.forEach(function (n) { n.textContent = (+n.dataset.count).toLocaleString("id-ID"); });
      return;
    }
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        co.unobserve(e.target);
        var el = e.target, target = +el.dataset.count, t0 = performance.now(), dur = 1200;
        (function step(t) {
          var p = Math.min(1, (t - t0) / dur);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString("id-ID");
          if (p < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: .5 });
    nodes.forEach(function (n) { co.observe(n); });
  })();

  /* ---------- ticker ---------- */
  (function ticker() {
    var track = $("#ticker-track");
    if (!track || !D.NEWS) return;
    var html = D.NEWS.slice(0, 8).map(function (n) {
      return '<a class="tk" href="berita.html#' + encodeURIComponent(n.t) + '">' + esc(n.t) + "</a>";
    }).join("");
    track.innerHTML = html + html;
  })();

  /* ---------- kartu berita ---------- */
  function newsCard(n, idx, feature) {
    var cat = (n.c && n.c[0]) || "Berita";
    var href = "berita.html#" + encodeURIComponent(n.t);
    return '<article class="card card--news reveal' + (feature ? " card--feature" : "") + '">' +
      '<a class="card__media" href="' + href + '" data-read="' + esc(n.t) + '" data-i="' + idx + '">' +
        '<img src="' + esc(n.i) + '" alt="" loading="lazy" decoding="async">' +
        (n.v ? '<span class="card__play">' + PLAY + "</span>" : "") +
        '<span class="card__cat">' + esc(cat) + "</span></a>" +
      '<div class="card__body">' +
        '<p class="card__kicker">' + fmtDate(n.d) + "</p>" +
        '<h3 class="card__title"><a href="' + href + '" data-read="' + esc(n.t) + '" data-i="' + idx + '">' + esc(n.t) + "</a></h3>" +
        '<p class="card__text">' + esc(n.x || "Baca selengkapnya untuk informasi lengkap kegiatan ini.") + "</p>" +
        '<div class="card__foot"><a class="link" href="' + href + '" data-read="' + esc(n.t) + '" data-i="' + idx + '">Baca selengkapnya' + arrow() + "</a></div>" +
      "</div></article>";
  }
  function arrow() {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  }

  /* ---------- berita: filter + cari + paginasi ---------- */
  (function berita() {
    var grid = $("#news-grid"), chips = $("#news-chips"), pager = $("#news-pager");
    var search = $("#news-search"), count = $("#news-count");
    if (!grid || !chips || !D.NEWS) return;

    var PER = 9, page = 1, cat = "Semua", q = "";
    var cats = ["Semua"];
    D.NEWS.forEach(function (n) {
      (n.c || []).forEach(function (c) { if (cats.indexOf(c) < 0) cats.push(c); });
    });
    chips.innerHTML = cats.map(function (c) {
      return '<button class="chip' + (c === cat ? " is-on" : "") + '" type="button" data-cat="' + esc(c) + '" aria-pressed="' + (c === cat) + '">' + esc(c) + "</button>";
    }).join("");

    function filtered() {
      var needle = q.toLowerCase();
      return D.NEWS.map(function (n, i) { return { n: n, i: i }; }).filter(function (o) {
        var n = o.n;
        var okCat = cat === "Semua" || (n.c || []).indexOf(cat) >= 0;
        var okQ = !needle || (n.t + " " + (n.x || "")).toLowerCase().indexOf(needle) >= 0;
        return okCat && okQ;
      });
    }

    function render() {
      var list = filtered();
      var pages = Math.max(1, Math.ceil(list.length / PER));
      if (page > pages) page = pages;
      var slice = list.slice((page - 1) * PER, page * PER);
      grid.innerHTML = slice.length
        ? slice.map(function (o, k) { return newsCard(o.n, o.i, false); }).join("")
        : '<p class="empty">Tidak ada artikel yang cocok. Coba kata kunci lain.</p>';
      if (count) count.textContent = list.length + " artikel";
      observe(grid);
      if (pager) pager.innerHTML = pagerHtml(pages);
    }

    function pagerHtml(pages) {
      if (pages < 2) return "";
      var out = ['<button type="button" data-p="' + Math.max(1, page - 1) + '" aria-label="Sebelumnya">‹</button>'];
      var win = [1, pages, page - 1, page, page + 1].filter(function (n) { return n >= 1 && n <= pages; });
      win = win.filter(function (n, i) { return win.indexOf(n) === i; }).sort(function (a, b) { return a - b; });
      var last = 0;
      win.forEach(function (n) {
        if (last && n - last > 1) out.push('<span class="pager__gap">…</span>');
        out.push('<button type="button" data-p="' + n + '"' + (n === page ? ' class="is-on" aria-current="page"' : "") + ">" + n + "</button>");
        last = n;
      });
      out.push('<button type="button" data-p="' + Math.min(pages, page + 1) + '" aria-label="Berikutnya">›</button>');
      return out.join("");
    }

    chips.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      cat = b.dataset.cat; page = 1;
      $$(".chip", chips).forEach(function (c) {
        var on = c === b;
        c.classList.toggle("is-on", on);
        c.setAttribute("aria-pressed", String(on));
      });
      render();
    });

    if (search) {
      var tmr;
      search.addEventListener("input", function () {
        clearTimeout(tmr);
        tmr = setTimeout(function () { q = search.value.trim(); page = 1; render(); }, 140);
      });
    }

    if (pager) pager.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-p]");
      if (!b) return;
      page = +b.dataset.p; render();
      grid.scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "start" });
    });

    render();
  })();

  /* ---------- galeri ---------- */
  (function galeri() {
    var grid = $("#galeri-grid"), chips = $("#galeri-chips");
    if (!grid || !chips) return;
    chips.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      var g = b.dataset.g;
      $$(".chip", chips).forEach(function (c) {
        var on = c === b;
        c.classList.toggle("is-on", on);
        c.setAttribute("aria-pressed", String(on));
      });
      $$(".tile", grid).forEach(function (t) {
        t.hidden = !(g === "Semua" || t.dataset.gg === g);
      });
    });
  })();

  /* ---------- pencarian guru ---------- */
  (function guru() {
    var input = $("#guru-search"), table = $("#guru-table");
    if (!input || !table) return;
    var rows = $$("tbody tr", table);
    input.addEventListener("input", function () {
      var q = input.value.toLowerCase().trim();
      var shown = 0;
      rows.forEach(function (r) {
        var ok = !q || r.textContent.toLowerCase().indexOf(q) >= 0;
        r.hidden = !ok;
        if (ok) shown++;
      });
      var empty = $(".empty-row", table.tBodies[0]);
      if (!shown && !empty) {
        var tr = document.createElement("tr");
        tr.className = "empty-row";
        tr.innerHTML = '<td colspan="7">Tidak ada guru yang cocok.</td>';
        table.tBodies[0].appendChild(tr);
      } else if (shown && empty) {
        empty.remove();
      }
    });
  })();

  /* ---------- akordeon ---------- */
  (function accordion() {
    $$(".acc").forEach(function (acc) {
      var btn = $(".acc__q", acc), pane = $(".acc__pane", acc);
      if (!btn || !pane) return;
      btn.addEventListener("click", function () {
        var open = acc.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", String(open));
        pane.style.maxHeight = open ? pane.scrollHeight + "px" : "0px";
      });
    });
    window.addEventListener("resize", function () {
      $$(".acc.is-open .acc__pane").forEach(function (p) { p.style.maxHeight = p.scrollHeight + "px"; });
    });
  })();

  /* ---------- overlay: satu stack kunci ---------- */
  var LOCK = [];
  function lock(el) { if (el && LOCK.indexOf(el) < 0) LOCK.push(el); document.documentElement.classList.add("locked"); }
  function unlock(el) {
    var i = LOCK.indexOf(el);
    if (i > -1) LOCK.splice(i, 1);
    if (!LOCK.length) document.documentElement.classList.remove("locked");
  }
  var lastFocus = null;

  function openOverlay(el) {
    if (!el) return;
    lastFocus = document.activeElement;
    el.classList.add("is-open");
    lock(el);
    var f = el.querySelector("button, [href], input");
    if (f) f.focus();
  }
  function closeOverlay(el) {
    if (!el) return;
    el.classList.remove("is-open");
    unlock(el);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function closeTop() {
    var top = LOCK[LOCK.length - 1];
    if (top) closeOverlay(top);
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && LOCK.length) closeTop();
  });

  /* ---------- lightbox foto & dokumen ---------- */
  (function lightbox() {
    var box = $("#lightbox"), img = $("#lb-img"), cap = $("#lb-cap");
    if (!box || !img) return;
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lb], [data-doc]");
      if (!a) return;
      e.preventDefault();
      img.src = a.getAttribute("href") || (a.querySelector("img") || {}).src || "";
      if (cap) cap.textContent = a.dataset.cap || a.dataset.gg || (a.querySelector("img") || {}).alt || "";
      openOverlay(box);
    });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.closest(".modal__close")) closeOverlay(box);
    });
  })();

  /* ---------- video ---------- */
  (function video() {
    var box = $("#videobox"), wrap = $("#vb-wrap"), cap = $("#vb-cap");
    if (!box || !wrap) return;
    function player(id) {
      if (D.VIDEOS && D.VIDEOS[id]) {
        return '<video controls preload="metadata" poster="assets/img/yt_' + id + '.webp" src="' + D.VIDEOS[id] + '"></video>';
      }
      return '<iframe src="https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&rel=0" title="Video profil" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>';
    }
    document.addEventListener("click", function (e) {
      var b = e.target.closest("[data-video]");
      if (!b) return;
      e.preventDefault();
      var id = b.dataset.video;
      wrap.innerHTML = player(id);
      if (cap) cap.textContent = b.dataset.title || "Video profil jurusan";
      openOverlay(box);
    });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.closest(".modal__close")) {
        closeOverlay(box);
        wrap.innerHTML = "";
      }
    });
    var origClose = closeOverlay;
    closeOverlay = function (el) {
      if (el === box) wrap.innerHTML = "";
      origClose(el);
    };
  })();

  /* ---------- reader artikel ---------- */
  (function reader() {
    var sheet = $("#reader"), title = $("#r-title"), meta = $("#r-meta");
    var body = $("#r-body"), hero = $("#r-img");
    if (!sheet || !body) return;

    function sanitize(html) {
      return String(html || "")
        .replace(/<script[\s\S]*?<\/script>/gi, "")
        .replace(/\son\w+\s*=\s*"[^"]*"/gi, "")
        .replace(/\son\w+\s*=\s*'[^']*'/gi, "")
        .replace(/href\s*=\s*"javascript:[^"]*"/gi, 'href="#"');
    }

    function open(idx, fallbackTitle) {
      var n = D.NEWS[idx];
      if (!n && fallbackTitle) {
        n = D.NEWS.filter(function (x) { return x.t === fallbackTitle; })[0];
        idx = D.NEWS.indexOf(n);
      }
      if (!n) return;
      var full = (D.FULL || {})[n.t];
      sheet.classList.toggle("has-img", !!n.i);
      if (hero) hero.src = n.i || "";
      if (title) title.textContent = n.t;
      if (meta) {
        var cats = (n.c || []).join(", ");
        meta.innerHTML = "<span>" + esc(fmtDate(n.d)) + "</span>" + (cats ? "<span>" + esc(cats) + "</span>" : "");
      }
      body.innerHTML = full
        ? '<div class="prose">' + sanitize(full) + "</div>"
        : '<div class="prose"><p>' + esc(n.x || "Dokumentasi singkat kegiatan ini tersimpan di arsip redaksi Eskalaber.") + "</p></div>";
      openOverlay(sheet);
    }

    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-read]");
      if (!a) return;
      /* Di halaman berita kita tampilkan reader di tempat; di halaman lain
         tautan dibiarkan bernavigasi ke berita.html#judul. */
      if (!$("#news-grid")) return;
      e.preventDefault();
      open(+a.dataset.i, a.dataset.read);
    });

    var close = $("#r-close");
    if (close) close.addEventListener("click", function () { closeOverlay(sheet); });
    sheet.addEventListener("click", function (e) {
      if (e.target.classList.contains("reader__scrim")) closeOverlay(sheet);
    });

    function fromHash() {
      var h = decodeURIComponent(location.hash.replace(/^#/, ""));
      if (!h || !D.NEWS) return;
      var idx = -1;
      for (var i = 0; i < D.NEWS.length; i++) { if (D.NEWS[i].t === h) { idx = i; break; } }
      if (idx > -1) open(idx);
    }
    if ($("#news-grid")) {
      setTimeout(fromHash, 250);
      window.addEventListener("hashchange", fromHash);
    }
  })();

  /* ---------- form kontak ---------- */
  (function form() {
    var f = $("#kontak-form");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(f);
      var body = "Nama: " + fd.get("nama") + "\nEmail: " + fd.get("email") +
        "\nSubjek: " + fd.get("subjek") + "\n\n" + fd.get("pesan");
      window.location.href = "mailto:smknegeri08jember@gmail.com?subject=" +
        encodeURIComponent(fd.get("subjek") || "Pesan Website") + "&body=" + encodeURIComponent(body);
      var note = document.createElement("div");
      note.className = "form__note";
      note.setAttribute("role", "status");
      note.textContent = "Terima kasih. Aplikasi email Anda terbuka untuk mengirim pesan ke Humas SMKN 8 Jember.";
      f.innerHTML = "";
      f.appendChild(note);
    });
  })();
})();
