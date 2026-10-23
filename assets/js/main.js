/* ============================================================
   SMKN 8 JEMBER — main.js
   Interaksi & render data (berita, galeri, guru, ekskul, prestasi)
   ============================================================ */
(function () {
  "use strict";
  const D = window.ESKADATA || {};
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));

  /* ---------- util ---------- */
  const BULAN = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"];
  const fmtDate = (iso) => {
    const [y, m, d] = (iso || "").split("-");
    return `${+d} ${BULAN[(+m || 1) - 1]} ${y}`;
  };
  const esc = (s) => String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const ph = (w) => `<div style="width:100%;height:100%;display:grid;place-items:center;background:linear-gradient(135deg,#0E4D3C,#1FA05C);color:#FFC531;font-weight:800;font-size:${w || 34}px;font-family:var(--font)">ESKALABER</div>`;

  const ICO = {
    clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    trophy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v6a5 5 0 0 1-10 0V4Z"/><path d="M7 6H4a2 2 0 0 0 2 4h1M17 6h3a2 2 0 0 1-2 4h-1"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>',
  };
  const PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg>';
  const ytId = (u) => { const m = (u || "").match(/(?:embed\/|youtu\.be\/|watch\?v=)([\w-]{11})/); return m ? m[1] : null; };
  const ytblock = (id) => {
    if ((D.VIDEOS || {})[id]) return `<div class="ytblock playing"><video controls preload="metadata" poster="assets/img/yt_${id}.webp" src="${D.VIDEOS[id]}"></video></div>`;
    const local = (D.YTIDS || []).includes(id);
    const thumb = local ? `assets/img/yt_${id}.webp` : `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
    return `<div class="ytblock" data-yt="${id}"><img loading="lazy" src="${thumb}" alt="Sampul video YouTube"><span class="play">${PLAY}</span><span class="ytlabel">YouTube · klik untuk putar</span></div>`;
  };

  /* ---------- navbar ---------- */
  const nav = $("#nav");
  const onScroll = () => {
    nav && nav.classList.toggle("scrolled", scrollY > 12);
    const tt = $("#totop");
    tt && tt.classList.toggle("show", scrollY > 600);
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const burger = $("#burger"), mmenu = $("#mmenu");
  burger && burger.addEventListener("click", () => {
    burger.classList.toggle("open");
    mmenu.classList.toggle("open");
  });
  $$("#mmenu a").forEach((a) => a.addEventListener("click", () => {
    burger.classList.remove("open"); mmenu.classList.remove("open");
  }));
  const tt = $("#totop");
  tt && tt.addEventListener("click", () => scrollTo({ top: 0, behavior: "smooth" }));

  /* ---------- reveal ---------- */
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  const revealAll = (root) => $$(".reveal", root).forEach((el) => io.observe(el));
  revealAll(document);

  /* ---------- counters ---------- */
  const cio = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    cio.unobserve(e.target);
    const el = e.target, target = +el.dataset.count, suf = el.dataset.suffix || "";
    const t0 = performance.now(), dur = 1400;
    const step = (t) => {
      const p = Math.min(1, (t - t0) / dur), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = v.toLocaleString("id-ID") + suf;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }), { threshold: 0.5 });
  $$("[data-count]").forEach((el) => cio.observe(el));

  /* ---------- ticker ---------- */
  const tick = $("#ticker-track");
  if (tick && D.NEWS) {
    const items = D.NEWS.slice(0, 8).map((n) => `<a href="berita.html#${encodeURIComponent(n.t)}">${esc(n.t)}</a>`).join("");
    tick.innerHTML = items + items;
  }

  /* ---------- kartu berita ---------- */
  const ncard = (n, feature) => `
    <article class="ncard reveal in ${feature ? "feature" : ""}">
      <div class="ph"><img loading="lazy" src="${n.i}" alt="${esc(n.t)}">${n.v ? `<span class="playbadge">${PLAY}</span>` : ""}<span class="cat">${esc(n.c[0])}</span></div>
      <div class="body">
        <time>${ICO.clock} ${fmtDate(n.d)}</time>
        <h3><a href="#" data-read="${esc(n.t)}">${esc(n.t)}</a></h3>
        <p>${esc(n.x) || "Baca selengkapnya untuk informasi lengkap kegiatan ini."}</p>
        <span class="more" data-read="${esc(n.t)}" style="cursor:pointer">Baca selengkapnya ${ICO.arrow}</span>
      </div>
    </article>`;

  /* ---------- beranda: berita terbaru ---------- */
  const homeNews = $("#home-news");
  if (homeNews && D.NEWS) {
    const list = D.NEWS.slice(0, 7);
    homeNews.innerHTML = list.map((n, i) => ncard(n, i === 0)).join("");
  }

  /* ---------- halaman berita: filter + cari + paginasi ---------- */
  const newsGrid = $("#news-grid");
  if (newsGrid && D.NEWS) {
    const PER = 9;
    let cat = "Semua", q = "", page = 1;
    const cats = ["Semua", ...new Set(D.NEWS.flatMap((n) => n.c))];
    const chipsEl = $("#news-chips"), pagerEl = $("#news-pager"), countEl = $("#news-count");
    chipsEl.innerHTML = cats.map((c) => `<button class="chip ${c === cat ? "on" : ""}" data-c="${esc(c)}">${esc(c)}</button>`).join("");
    chipsEl.addEventListener("click", (e) => {
      const b = e.target.closest(".chip"); if (!b) return;
      cat = b.dataset.c; page = 1;
      $$(".chip", chipsEl).forEach((x) => x.classList.toggle("on", x === b));
      draw();
    });
    const si = $("#news-search");
    si && si.addEventListener("input", () => { q = si.value.toLowerCase(); page = 1; draw(); });

    function filtered() {
      return D.NEWS.filter((n) =>
        (cat === "Semua" || n.c.includes(cat)) &&
        (!q || n.t.toLowerCase().includes(q) || (n.x || "").toLowerCase().includes(q)));
    }
    function draw() {
      const list = filtered();
      const pages = Math.max(1, Math.ceil(list.length / PER));
      page = Math.min(page, pages);
      countEl && (countEl.textContent = `${list.length} artikel`);
      const slice = list.slice((page - 1) * PER, page * PER);
      newsGrid.innerHTML = slice.length ? slice.map((n) => ncard(n)).join("") : `<div class="empty">Tidak ada artikel yang cocok. Coba kata kunci lain.</div>`;
      let btns = "";
      const win = [];
      for (let i = 1; i <= pages; i++) if (i === 1 || i === pages || Math.abs(i - page) <= 1) win.push(i);
      let last = 0;
      win.forEach((i) => { if (i - last > 1) btns += `<button disabled>…</button>`; btns += `<button class="${i === page ? "on" : ""}" data-p="${i}">${i}</button>`; last = i; });
      pagerEl.innerHTML = `<button data-p="${page - 1}" ${page === 1 ? "disabled" : ""}>‹</button>` + btns + `<button data-p="${page + 1}" ${page === pages ? "disabled" : ""}>›</button>`;
    }
    pagerEl.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-p]"); if (!b || b.disabled) return;
      page = +b.dataset.p; draw();
      newsGrid.scrollIntoView && newsGrid.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    draw();
    // deep-link #judul
    if (location.hash.length > 2) {
      const t = decodeURIComponent(location.hash.slice(1));
      const hit = D.NEWS.find((n) => n.t === t);
      if (hit) setTimeout(() => openReader(hit), 300);
    }
  }

  /* ---------- galeri ---------- */
  const gal = $("#galeri-grid");
  if (gal && D.GALLERY) {
    let g = "semua";
    const groups = ["semua", ...new Set(D.GALLERY.map((x) => x.g))];
    const wrap = $("#galeri-chips");
    const LABEL = { semua: "Semua", kegiatan: "Kegiatan", ekskul: "Ekstrakurikuler", jurusan: "Konsentrasi Keahlian", prestasi: "Prestasi", fasilitas: "Fasilitas", info: "Info & Desain" };
    wrap && (wrap.innerHTML = groups.map((x) => `<button class="chip ${x === g ? "on" : ""}" data-g="${x}">${LABEL[x] || x}</button>`).join(""));
    function drawG() {
      const list = D.GALLERY.filter((x) => g === "semua" || x.g === g);
      gal.innerHTML = list.map((x, i) => `<a href="#" data-lb="${i}" data-gg="${x.g}"><img loading="lazy" src="${x.s}" alt="${esc(x.c)}"><span class="cap">${esc(x.c)}</span></a>`).join("");
      $$("#galeri-grid a").forEach((a) => {
        a.addEventListener("click", (e) => {
          e.preventDefault();
          const item = list[+a.dataset.lb];
          openLB(item);
        });
      });
    }
    wrap && wrap.addEventListener("click", (e) => {
      const b = e.target.closest(".chip"); if (!b) return;
      g = b.dataset.g;
      $$(".chip", wrap).forEach((x) => x.classList.toggle("on", x === b));
      drawG();
    });
    drawG();
  }
  const lb = $("#lightbox");
  function openLB(item) {
    if (!lb) return;
    $("#lb-img").src = item.b;
    $("#lb-cap").textContent = item.c;
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  lb && $$(".x", lb).forEach((x) => x.addEventListener("click", closeLB));
  lb && lb.addEventListener("click", (e) => { if (e.target === lb) closeLB(); });
  function closeLB() { lb.classList.remove("open"); document.body.style.overflow = ""; }

  /* ---------- reader modal ---------- */
  const reader = $("#reader");
  function openReader(n) {
    if (!reader) return;
    $("#r-title").textContent = n.t;
    $("#r-meta").innerHTML = `<span>${fmtDate(n.d)}</span><span>•</span><span>${esc(n.c.join(", "))}</span>`;
    const hero = $("#r-img");
    if (n.i) { hero.src = n.i; hero.style.display = "block"; } else hero.style.display = "none";
    const full = (D.FULL || {})[n.t];
    let bodyHtml;
    if (full) {
      bodyHtml = `<div class="content">${full.replace(/<div class="video-embed" data-src="([^"]+)"><\/div>/g, (m, u) => { const id = ytId(u); return id ? ytblock(id) : m; })}</div>`;
      bodyHtml = bodyHtml.replace(/<a[^>]*href="(https?:\/\/(?:www\.)?(?:youtu\.be\/|youtube\.com\/watch\?v=|youtube\.com\/embed\/)[\w-]{11}[^"]*)"[^>]*>[\s\S]*?<\/a>/g, (m, u) => { const id = ytId(u); return id ? ytblock(id) : m; });
      if (n.v && !bodyHtml.includes("ytblock")) bodyHtml = ytblock(n.v) + bodyHtml;
    } else {
      bodyHtml = `<div class="content">${n.v ? ytblock(n.v) : ""}<p>${esc(n.x) || "Dokumentasi singkat kegiatan ini tersimpan di arsip redaksi Eskalaber."}</p></div>`;
    }
    $("#r-body").innerHTML = bodyHtml;
    reader.classList.add("open");
    document.body.style.overflow = "hidden";
    reader.querySelector(".sheet").scrollTop = 0;
  }
  document.addEventListener("click", (e) => {
    const y = e.target.closest(".ytblock");
    if (y && !y.classList.contains("playing")) {
      const id = y.dataset.yt;
      y.classList.add("playing");
      y.innerHTML = `<iframe src="https://www.youtube.com/embed/${id}?autoplay=1" title="Video YouTube SMKN 8 Jember" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
      return;
    }
    const t = e.target.closest("[data-read]");
    if (!t) return;
    e.preventDefault();
    const n = (D.NEWS || []).find((x) => x.t === t.dataset.read);
    if (n) openReader(n);
  });
  reader && $("#r-close").addEventListener("click", () => { reader.classList.remove("open"); document.body.style.overflow = ""; });
  reader && reader.addEventListener("click", (e) => { if (e.target.classList.contains("bg")) { reader.classList.remove("open"); document.body.style.overflow = ""; } });
  addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeLB(); reader && reader.classList.remove("open"); document.body.style.overflow = ""; }
  });

  /* ---------- tabel guru / karyawan ---------- */
  function renderTable(sel, rows, cols) {
    const el = $(sel); if (!el || !rows) return;
    const head = `<tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr>`;
    const body = rows.map((r) => `<tr>${cols.map((_, i) => `<td>${esc(r[i] || "-")}</td>`).join("")}</tr>`).join("");
    el.innerHTML = `<table class="data"><thead>${head}</thead><tbody>${body}</tbody></table>`;
    return el;
  }
  const gwrap = renderTable("#guru-table", D.TEACHERS, ["No", "Nama", "JK", "Pendidikan Terakhir", "Tahun Lulus", "Mata Pelajaran"]);
  const swrap = renderTable("#karyawan-table", D.STAFF, ["No", "Nama", "Jenis Kelamin", "Jabatan / Tugas"]);
  const tsearch = $("#guru-search");
  tsearch && gwrap && tsearch.addEventListener("input", () => {
    const q = tsearch.value.toLowerCase();
    const rows = D.TEACHERS.filter((r) => r.join(" ").toLowerCase().includes(q));
    gwrap.querySelector("tbody").innerHTML = rows.map((r) => `<tr>${["No","Nama","JK","Pendidikan Terakhir","Tahun Lulus","Mata Pelajaran"].map((_, i) => `<td>${esc(r[i] || "-")}</td>`).join("")}</tr>`).join("") || `<tr><td colspan="6" class="empty">Tidak ditemukan</td></tr>`;
  });

  /* ---------- ekskul ---------- */
  const xw = $("#ekskul-grid");
  if (xw && D.EKSUL) {
    const PH = {
      PRAMUKA: "PRAMUKA.webp", FUTSAL: "Futsal.webp", "BOLA VOLI": "Voli.webp",
      "PENCAK ORGANISASI": "PO.webp", "PSH \u201CTERATAI\u201D": "PSHT.webp", "BULU TANGKIS": "badminton.webp",
      "SENI MUSIK": "ekskul-musik.webp", "PADUAN SUARA": "Paduan-Suara-scaled.webp",
      "REMAJA MASJID": "TARTIL-REMAS.webp", HADRAH: "HADRAH-scaled.webp", "UKS dan PMR": "PMR.webp",
      PASKIBRA: "PASKIB.webp", "SEPAK BOLA": "Futsal.webp", "SENI TARI": "Seni-Tari-.webp",
      AEROMODELLING: "aeromodelling-2.webp",
    };
    xw.innerHTML = D.EKSUL.map((r, i) => {
      const nama = (r[1] || "").trim(), pembina = (r[2] || "").trim();
      const img = PH[nama.toUpperCase()] || PH[nama];
      return `<div class="xcard reveal in"><div>${img ? `<img loading="lazy" src="assets/img/${img}" alt="${esc(nama)}">` : `<div class="noico">${String(i + 1).padStart(2, "0")}</div>`}</div><div><b>${esc(nama)}</b><span>Pembina: ${esc(pembina || "—")}</span></div></div>`;
    }).join("");
  }

  /* ---------- prestasi ---------- */
  const pw = $("#prestasi-grid");
  if (pw && D.PRESTASI) {
    pw.innerHTML = D.PRESTASI.map((p) => `
      <div class="pcard reveal in">
        ${p.i ? `<img loading="lazy" src="${p.i}" alt="">` : `<div class="tro">${ICO.trophy}</div>`}
        <div><b>${esc(p.t)}</b><time>${fmtDate(p.d)}</time></div>
      </div>`).join("");
  }

  /* ---------- mitra marquee text ---------- */
  const mw = $("#mitra-list");
  if (mw && D.MITRA) mw.innerHTML = D.MITRA.map((m) => `<span>${esc(m)}</span>`).join("");


  /* ---------- misi & tujuan ---------- */
  const misiEl = $("#misi-list");
  if (misiEl && D.MISI) misiEl.innerHTML = D.MISI.map((x) => `<li>${esc(x)}</li>`).join("");
  const tujEl = $("#tujuan-list");
  if (tujEl && D.TUJUAN) tujEl.innerHTML = D.TUJUAN.map((x) => `<li>${esc(x)}</li>`).join("");

  /* ---------- tabel MoU ---------- */
  const mouEl = $("#mou-table");
  if (mouEl && D.MOU) {
    mouEl.innerHTML = `<table class="data"><thead><tr><th>No</th><th>Nama Dunia Usaha / Industri</th><th>Bidang Usaha</th><th>Alamat</th></tr></thead><tbody>${D.MOU.map((r) => `<tr><td>${esc(r[0])}</td><td><b>${esc(r[1])}</b></td><td>${esc(r[2] || "-")}</td><td>${esc(r[3] || "-")}</td></tr>`).join("")}</tbody></table>`;
  }

  /* ---------- prestasi lama ---------- */
  const plEl = $("#prestasi-lama");
  if (plEl && D.PRESTASI_LAMA) plEl.innerHTML = D.PRESTASI_LAMA.map((x) => `<span>${esc(x.trim())}</span>`).join("");

  /* ---------- modal video (lokal pertama, lalu YouTube) ---------- */
  const vbox = $("#videobox");
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-video]");
    if (!b || !vbox) return;
    const id = b.dataset.video;
    const cap = b.closest(".jcard") ? b.closest(".jcard").querySelector("h3").textContent : "Video SMKN 8 Jember";
    const wrap = $("#vb-wrap");
    wrap.innerHTML = (D.VIDEOS || {})[id]
      ? `<video controls autoplay poster="assets/img/yt_${id}.webp" src="${D.VIDEOS[id]}"></video>`
      : `<iframe src="https://www.youtube.com/embed/${id}?autoplay=1" title="${esc(cap)}" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
    $("#vb-cap").textContent = cap;
    vbox.classList.add("open");
    document.body.style.overflow = "hidden";
  });
  vbox && vbox.addEventListener("click", (e) => {
    if (e.target === vbox || e.target.classList.contains("x")) {
      $("#vb-wrap").innerHTML = "";
      vbox.classList.remove("open");
      document.body.style.overflow = "";
    }
  });

  /* ---------- viewer dokumen (pengumuman, e-mading) ---------- */
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-doc]");
    if (!a) return;
    e.preventDefault();
    openLB({ b: a.dataset.doc, c: a.dataset.cap || "" });
  });

  /* ---------- accordion ---------- */
  $$(".acc button").forEach((b) => b.addEventListener("click", () => {
    const acc = b.parentElement, pane = acc.querySelector(".pane");
    const open = acc.classList.toggle("open");
    pane.style.maxHeight = open ? pane.scrollHeight + "px" : 0;
  }));

  /* ---------- form kontak (demo) ---------- */
  const cf = $("#kontak-form");
  cf && cf.addEventListener("submit", (e) => {
    e.preventDefault();
    const fd = new FormData(cf);
    const body = encodeURIComponent(`Nama: ${fd.get("nama")}\nEmail: ${fd.get("email")}\nSubjek: ${fd.get("subjek")}\n\n${fd.get("pesan")}`);
    location.href = `mailto:smknegeri08jember@gmail.com?subject=${encodeURIComponent(fd.get("subjek") || "Pesan Website")}&body=${body}`;
    cf.innerHTML = `<div class="empty" style="grid-column:1/-1">Terima kasih! Aplikasi email Anda terbuka untuk mengirim pesan ke Humas SMKN 8 Jember. 📨</div>`;
  });
})();
