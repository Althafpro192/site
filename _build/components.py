"""components.py — pembangun HTML. Semua markup berasal dari sini, bukan dari
salin-tempel antar halaman. Satu kelas = satu aturan di style.css.
"""
from __future__ import annotations

from html import escape

import content as C

ICONS = {
    "check": '<path d="m4 12.5 5 5L20 6.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-up-right": '<path d="M7 17 17 7M8 7h9v9"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "play": '<path d="M8 5.5v13l11-6.5-11-6.5Z" fill="currentColor" stroke="none"/>',
    "trophy": '<path d="M8 21h8M12 17v4M7 4h10v6a5 5 0 0 1-10 0V4Z"/><path d="M7 6H4a2 2 0 0 0 2 4h1M17 6h3a2 2 0 0 1-2 4h-1"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 8 9 6 9-6"/>',
    "phone": '<path d="M6 3h3l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3Z"/>',
    "pin": '<path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor" stroke="none"/>',
    "youtube": '<path d="M22 12s0-3.3-.4-4.9a2.6 2.6 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.3a2.6 2.6 0 0 0-1.8 1.8C2 8.7 2 12 2 12s0 3.3.4 4.9a2.6 2.6 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.3a2.6 2.6 0 0 0 1.8-1.8C22 15.3 22 12 22 12Z"/><path d="M10 9.5v5l4.5-2.5z" fill="currentColor" stroke="none"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.2 2.2M16.9 16.9l2.2 2.2M19.1 4.9l-2.2 2.2M7.1 16.9l-2.2 2.2"/>',
    "moon": '<path d="M20.5 14.3A8.6 8.6 0 0 1 9.7 3.5 8.6 8.6 0 1 0 20.5 14.3Z"/>',
    "grid": '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2Z"/><path d="M4 19V5"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.5a3 3 0 0 1 0 5.6M17 14.2A5.5 5.5 0 0 1 21 20"/>',
    "leaf": '<path d="M4 20c8 1 15-5 16-16-9-1-15 4-16 16Z"/><path d="M9 15c2-3 5-5 8-6"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6Z"/><path d="m9 12 2 2 4-4"/>',
}


def icon(name: str, cls: str = "", size: int = 0) -> str:
    body = ICONS.get(name, "")
    dim = f' width="{size}" height="{size}"' if size else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false"{dim}>{body}</svg>')


def esc(s) -> str:
    return escape(str(s), quote=True)


# ------------------------------------------------------------------- chrome
def brand(href: str = "index.html") -> str:
    return f'''<a class="brand" href="{href}">
  <img src="assets/img/logo-SMK3.png" alt="Logo SMK Negeri 8 Jember" width="75" height="73">
  <span class="brand__name">{esc(C.SCHOOL["name"])}</span>
</a>'''


def nav(stem: str) -> str:
    def link(href: str, label: str, active: bool, cls: str) -> str:
        state = f'{cls} is-active' if active else cls
        cur = ' aria-current="page"' if active else ""
        return f'<a class="{state}" href="{href}"{cur}>{label}</a>'

    links = "".join(link(h, l, a, "nav__link") for h, l, a in C.nav_for(stem))
    drawer = "".join(link(h, l, a, "drawer__link") for h, l, a in C.nav_for(stem))
    return f'''<a class="skip" href="#main">Lewati ke isi</a>
<header class="site-header">
  <div class="container site-header__inner">
    {brand()}
    <nav class="nav" aria-label="Navigasi utama">{links}</nav>
    <div class="site-header__actions">
      <button class="icon-btn" id="theme-toggle" type="button" aria-pressed="false" aria-label="Ganti tema terang atau gelap">
        <span class="icon-btn__sun">{icon("sun")}</span>
        <span class="icon-btn__moon">{icon("moon")}</span>
      </button>
      <a class="btn btn--primary btn--sm nav__cta" href="ppdb.html">SPMB 2026 {icon("arrow")}</a>
      <button class="icon-btn nav__burger" id="burger" type="button" aria-label="Buka menu" aria-expanded="false" aria-controls="drawer">{icon("menu")}</button>
    </div>
  </div>
  <div class="drawer" id="drawer" hidden>
    {drawer}
    <a class="btn btn--primary drawer__cta" href="ppdb.html">SPMB 2026</a>
  </div>
</header>
<div class="ticker" aria-label="Info terbaru">
  <div class="container ticker__inner">
    <span class="ticker__label">{icon("clock")} Info terbaru</span>
    <div class="ticker__view"><div class="ticker__track" id="ticker-track"></div></div>
  </div>
</div>'''


def footer() -> str:
    navs = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in C.NAV)
    programs = "".join(f'<li><a href="jurusan.html#{p["id"]}">{p["name"]}</a></li>' for p in C.PROGRAMS)
    s = C.SCHOOL
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="assets/img/logo-SMK3.png" alt="" width="75" height="73">
        <p class="footer__name">{esc(s["name"])}</p>
        <p class="footer__meta">{esc(s["kind"])} · {esc(s["region"])}</p>
        <p class="footer__addr">{esc(s["address"])}</p>
        <div class="footer__social">
          <a href="{s["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
          <a href="{s["youtube"]}" target="_blank" rel="noopener" aria-label="YouTube">{icon("youtube")}</a>
          <a href="mailto:{s["email"]}" aria-label="Email">{icon("mail")}</a>
        </div>
      </div>
      <div><h2 class="footer__h">Navigasi</h2><ul class="footer__links">{navs}</ul></div>
      <div><h2 class="footer__h">Konsentrasi</h2><ul class="footer__links">{programs}</ul></div>
      <div>
        <h2 class="footer__h">Kontak</h2>
        <ul class="footer__links">
          <li><a href="mailto:{s["email"]}">{s["email"]}</a></li>
          <li><a href="tel:{s["phone"].replace("-", "")}">{s["phone"]}</a></li>
          <li><a href="mailto:{s["lsp_email"]}">LSP P-1: {s["lsp_email"]}</a></li>
          <li><a href="{s["tour"]}" target="_blank" rel="noopener">Tur virtual 360°</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {C.SCHOOL["founded"]}–2026 {esc(s["name"])}. Seluruh konten tersimpan lokal.</span>
      <span>{esc(s["tagline"])} · {esc(s["status"])}</span>
    </div>
  </div>
</footer>
<button class="totop" id="totop" type="button" aria-label="Kembali ke atas">{icon("arrow")}</button>
<div class="modal" id="lightbox" role="dialog" aria-modal="true" aria-label="Pratinjau foto" tabindex="-1">
  <button class="modal__close" type="button" aria-label="Tutup">{icon("close")}</button>
  <figure class="modal__figure"><img id="lb-img" src="" alt=""><figcaption id="lb-cap"></figcaption></figure>
</div>
<div class="modal" id="videobox" role="dialog" aria-modal="true" aria-label="Pemutar video" tabindex="-1">
  <button class="modal__close" type="button" aria-label="Tutup">{icon("close")}</button>
  <div class="modal__video" id="vb-wrap"></div>
  <p class="modal__cap" id="vb-cap"></p>
</div>
<div class="reader" id="reader" role="dialog" aria-modal="true" aria-labelledby="r-title" tabindex="-1">
  <div class="reader__scrim"></div>
  <article class="reader__sheet">
    <button class="modal__close" id="r-close" type="button" aria-label="Tutup artikel">{icon("close")}</button>
    <img class="reader__hero" id="r-img" src="" alt="">
    <div class="reader__inner">
      <p class="eyebrow" id="r-kicker">Eskalaber News</p>
      <h2 class="reader__title" id="r-title"></h2>
      <div class="reader__meta" id="r-meta"></div>
      <div class="prose" id="r-body"></div>
    </div>
  </article>
</div>'''


# ---------------------------------------------------------------- primitives
def btn(label: str, href: str, kind: str = "primary", ico: str = "", external: bool = False) -> str:
    attrs = ' target="_blank" rel="noopener"' if external else ""
    ico_html = f" {icon(ico)}" if ico else ""
    return f'<a class="btn btn--{kind}" href="{href}"{attrs}>{label}{ico_html}</a>'


def eyebrow(text: str, dot: bool = True) -> str:
    d = '<span class="eyebrow__dot"></span>' if dot else ""
    return f'<p class="eyebrow">{d}{esc(text)}</p>'


def section_head(title: str, lead: str = "", kicker: str = "", action: str = "", center: bool = False) -> str:
    cls = "section-head section-head--center" if center else "section-head"
    k = eyebrow(kicker) if kicker else ""
    l = f'<p class="lead">{esc(lead)}</p>' if lead else ""
    a = f'<div class="section-head__action">{action}</div>' if action else ""
    return f'''<div class="{cls}">
  <div class="section-head__copy">{k}<h2 class="h2">{esc(title)}</h2>{l}</div>
  {a}
</div>'''


def tag(text: str, kind: str = "") -> str:
    return f'<span class="tag{" tag--" + kind if kind else ""}">{esc(text)}</span>'


# --------------------------------------------------------------------- cards
def program_card(p: dict, wide: bool = False) -> str:
    cls = "card card--program card--wide" if wide else "card card--program"
    tags = "".join(tag(t) for t in p["marks"])
    return f'''<article class="{cls}" data-cluster="{p["cluster"]}" data-tilt id="{p["id"]}">
  <a class="card__media" href="jurusan.html#{p["id"]}" aria-label="{esc(p["name"])}">
    <img src="{p["img"]}" alt="" loading="lazy" decoding="async">
    <span class="card__no">{p["no"]}</span>
    <span class="card__cluster">{esc(p["cluster_label"])}</span>
  </a>
  <div class="card__body">
    <h3 class="card__title"><a href="jurusan.html#{p["id"]}">{esc(p["name"])}</a></h3>
    <p class="card__text">{esc(p["desc"])}</p>
    <div class="card__tags">{tags}</div>
    <div class="card__foot">
      <button class="link" type="button" data-video="{p["video"]}" data-title="{esc(p["name"])}">{icon("play")} Video profil</button>
      <a class="link" href="jurusan.html#{p["id"]}">Selengkapnya {icon("arrow")}</a>
    </div>
  </div>
</article>'''


def news_card(n: dict, idx: int, feature: bool = False, base: str = "berita.html") -> str:
    cats = n.get("c") or []
    cat = cats[0] if cats else "Berita"
    href = f"{base}#{_q(n['t'])}"
    cls = "card card--news" + (" card--feature" if feature else "")
    play = f'<span class="card__play">{icon("play")}</span>' if n.get("v") else ""
    img = n.get("i") or ""
    return f'''<article class="{cls} reveal">
  <a class="card__media" href="{href}" data-read="{esc(n["t"])}" data-i="{idx}">
    <img src="{img}" alt="" loading="lazy" decoding="async">{play}
    <span class="card__cat">{esc(cat)}</span>
  </a>
  <div class="card__body">
    <p class="card__kicker">{_date(n["d"])}</p>
    <h3 class="card__title"><a href="{href}" data-read="{esc(n["t"])}" data-i="{idx}">{esc(n["t"])}</a></h3>
    <p class="card__text">{esc(clean_excerpt(n.get("x")))}</p>
    <div class="card__foot">
      <a class="link" href="{href}" data-read="{esc(n["t"])}" data-i="{idx}">Baca selengkapnya {icon("arrow")}</a>
    </div>
  </div>
</article>'''


def stat_card(value: str, label: str, note: str = "") -> str:
    n = f'<span class="stat__note">{esc(note)}</span>' if note else ""
    return f'''<div class="stat">
  <b class="stat__value" data-count="{value.replace(".", "")}">{esc(value)}</b>
  <span class="stat__label">{esc(label)}</span>{n}
</div>'''


def gallery_tile(g: dict) -> str:
    return f'''<a class="tile" href="{g["b"]}" data-lb data-gg="{esc(g["g"])}" aria-label="Perbesar: {esc(g["c"])}">
  <img src="{g["s"]}" alt="" loading="lazy" decoding="async">
  <span class="tile__cap">{esc(g["c"])}</span>
</a>'''


def clean_excerpt(text: str | None) -> str:
    """Ringkasan dari data.js kadang membawa URL mentah atau penanda [VIDEO].
    Tampilkan sebagai kalimat, bukan sebagai tautan setengah jadi."""
    import re as _re
    if not text:
        return "Baca selengkapnya untuk informasi lengkap kegiatan ini."
    t = _re.sub(r"\[(?:VIDEO|AUDIO|GALERI)\]\s*", "", text, flags=_re.I)
    t = _re.sub(r"https?://\S+", "", t)
    t = _re.sub(r"\s{2,}", " ", t).strip(" -–—·")
    return t or "Baca selengkapnya untuk informasi lengkap kegiatan ini."


def _date(iso: str) -> str:
    bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    try:
        y, m, d = iso.split("-")
        return f"{int(d)} {bulan[int(m) - 1]} {y}"
    except Exception:  # noqa: BLE001 — tanggal rusak tidak boleh menghentikan build
        return iso or ""


def _q(title: str) -> str:
    from urllib.parse import quote
    return quote(title)


# --------------------------------------------------------------------- shell
def page(stem: str, body: str, body_class: str = "", extra_js: str = "") -> str:
    meta = C.page_meta(stem)
    return f'''<!DOCTYPE html>
<html lang="id" class="is-loading">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(meta["title"])}</title>
<meta name="description" content="{esc(meta["desc"])}">
<meta property="og:title" content="{esc(meta["title"])}">
<meta property="og:description" content="{esc(meta["desc"])}">
<meta property="og:image" content="assets/img/logo-SMK3.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="id_ID">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="assets/img/logo-SMK3.png">
<link rel="apple-touch-icon" href="assets/img/logo-SMK3.png">
<script>(function(){{try{{document.documentElement.setAttribute("data-theme",localStorage.getItem("eskalaber-theme")==="dark"?"dark":"light")}}catch(e){{document.documentElement.setAttribute("data-theme","light")}}}})();</script>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="{body_class}">
<div class="boot" id="boot" aria-hidden="true">
  <div class="boot__inner">
    <p class="boot__brand">SMKN 8 JEMBER <b>ESKALABER</b></p>
    <div class="boot__bar"><i id="boot-bar"></i></div>
    <p class="boot__pct" id="boot-pct">0%</p>
    <p class="boot__status" id="boot-status">Menyiapkan halaman…</p>
  </div>
</div>
{nav(stem)}
<main id="main">
{body}
</main>
{footer()}
<script defer src="assets/js/data.js"></script>{extra_js}
<script defer src="assets/js/main.js"></script>
</body>
</html>'''
