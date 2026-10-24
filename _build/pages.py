"""pages.py — perakit tiap halaman. Tidak ada teks yang ditulis di sini;
semuanya diambil dari content.py dan components.py.
"""
from __future__ import annotations

import content as C
import components as H

D = C.load_data()
NEWS = D["NEWS"]
GALLERY = D["GALLERY"]
TEACHERS = D["TEACHERS"]
STAFF = D["STAFF"]
EKSUL = D["EKSUL"]
PRESTASI = D["PRESTASI"]
PRESTASI_LAMA = D["PRESTASI_LAMA"]
MOU = D["MOU"]
MITRA = D["MITRA"]
MISI = D["MISI"]
TUJUAN = D["TUJUAN"]
LSP = D["LSP"]

PROGS = {p["id"]: p for p in C.PROGRAMS}


def _programs_grid(limit: int | None = None) -> str:
    """7 kartu pada grid 3 kolom → 3 + 3 + 1. Kartu terakhir dibuat melebar
    supaya tidak ada kartu tunggal menggantung di barisnya sendiri."""
    progs = C.PROGRAMS[:limit] if limit else C.PROGRAMS
    tail = ""
    if len(progs) % 3 == 1:
        tail = H.program_card(progs[-1], wide=True)
        progs = progs[:-1]
    body = "".join(H.program_card(p) for p in progs)
    return f'<div class="grid grid--3">{body}{tail}</div>'


# ===========================================================  BERANDA
def index() -> str:
    s = C.SCHOOL
    h = C.HERO
    thumbs = "".join(
        f'<a href="galeri.html"><img src="{src}" alt="{H.esc(alt)}" width="{w}" height="{ht}" loading="lazy" decoding="async"></a>'
        for src, alt, w, ht in h["thumbs"]
    )
    hero = f'''<section class="hero">
  <div class="container hero__inner">
    <div class="hero__copy">
      <p class="hero__badge"><img src="assets/img/logo-SMK3.png" alt="" width="75" height="73">{H.esc(h["badge"])}</p>
      <h1 class="hero__title">{H.esc(h["title_top"])} <em>{H.esc(h["title_accent"])}</em></h1>
      <p class="lead hero__lead">{H.esc(h["lead"])}</p>
      <div class="hero__actions">
        {H.btn("Jelajahi 7 jurusan", "jurusan.html", "primary", "arrow")}
        {H.btn("Tur virtual 360°", s["tour"], "ghost", "", external=True)}
      </div>
      <ul class="hero__points">
        {''.join(f'<li class="hero__point">{H.icon("check")}{H.esc(p)}</li>' for p in h["points"])}
      </ul>
    </div>
    <div class="hero__visual">
      <div class="hero__stage">
        <div class="hero__photo">
          <img src="{h["photo"]}" alt="{H.esc(h["photo_alt"])}" width="1200" height="720" loading="eager" fetchpriority="high" decoding="async">
          <span class="hero__scrim"></span>
          <span class="hero__crest">{H.icon("star")}{H.esc(h["crest"])}</span>
          <span class="hero__live">{H.icon("pin")}{H.esc(h["live"])}</span>
        </div>
        <div class="hero__note">
          <div class="hero__note-top">
            <div>
              <span class="hero__kicker">{H.esc(h["kicker"])}</span>
              <h2 class="hero__note-title">{H.esc(h["note"])}</h2>
            </div>
            <span class="hero__trophy">{H.icon("trophy")}</span>
          </div>
          <p class="hero__note-text">{H.esc(h["note_text"])}</p>
          <div class="hero__note-foot">
            <span>{H.esc(h["note_foot"])}</span>
            <a class="link" href="{h["note_href"]}">Lihat semua {H.icon("arrow")}</a>
          </div>
        </div>
      </div>
      <div class="hero__thumbs">{thumbs}</div>
      <div class="hero__float">
        <span class="hero__float-ico">{H.icon("users")}</span>
        <div><b>{H.esc(h["float_value"])}</b><span>{H.esc(h["float_label"])}</span></div>
      </div>
    </div>
  </div>
</section>'''

    stats = '<section class="section--tight"><div class="container"><div class="stats">' \
        + "".join(H.stat_card(v, l, i, t) for v, l, i, t in C.HEADLINE_STATS) + "</div></div></section>"

    w = C.WELCOME
    welcome = f'''<section class="section"><div class="container">
  <div class="welcome">
    <div class="welcome__photo">
      <img src="{w["photo"]}" alt="Kepala SMKN 8 Jember" width="640" height="800" loading="lazy" decoding="async">
      <div class="welcome__tag"><b>{H.esc(C.SCHOOL["head"])}</b><span>{H.esc(C.SCHOOL["head_role"])}</span></div>
    </div>
    <div>
      {H.eyebrow(w["eyebrow"])}
      <h2 class="h2">{H.esc(w["title"])}</h2>
      <blockquote class="welcome__quote">“{H.esc(w["quote"])}”</blockquote>
      <p class="lead mt-4">{H.esc(w["body"])}</p>
      <div class="sign">
        <img src="{w["photo"]}" alt="" width="640" height="800" loading="lazy" decoding="async">
        <div><b>{H.esc(C.SCHOOL["head"])}</b><span>{H.esc(C.SCHOOL["head_role"])}</span></div>
      </div>
    </div>
  </div>
</div></section>'''

    programs = f'''<section class="section section--soft" id="jurusan"><div class="container">
  {H.section_head("7 jurusan, 3 program keahlian",
                   "Teknik Otomotif, Teknik Komputer & Informatika, serta Teknologi Pertanian — semuanya dilengkapi bengkel, lab, dan lahan praktik sendiri.",
                   "Konsentrasi keahlian", H.btn("Detail semua jurusan", "jurusan.html", "ghost", "arrow"),
                   note=f"{C.SPMB['quota_total'][0]} rombel · {C.SPMB['quota_total'][1]} kursi SPMB 2026")}
  {_programs_grid()}
</div></section>'''

    bento_cells = []
    for b in C.BENTO:
        kind = b["kind"]
        cls = "bento__cell"
        if b.get("span", 1) == 2:
            cls += " bento__cell--span2"
        if kind == "dark":
            cls += " bento__cell--dark"
        elif kind == "sun":
            cls += " bento__cell--sun"
        elif kind == "photo":
            cls += " bento__cell--photo"
        bg = f'<img class="bento__bg" src="{b["img"]}" alt="" loading="lazy" decoding="async">' if kind == "photo" else ""
        big = f'<span class="bento__big">{H.esc(b["big"])}</span>' if b.get("big") else ""
        bento_cells.append(
            f'<article class="{cls}">{bg}{big}'
            f'<p class="bento__kicker">{H.esc(b["kicker"])}</p>'
            f'<h3 class="bento__title">{H.esc(b["title"])}</h3>'
            f'<p class="bento__text">{H.esc(b["body"])}</p></article>'
        )
    bento = f'''<section class="section" id="unggulan"><div class="container">
  {H.section_head("Sekolah vokasi yang benar-benar bekerja",
                   "Fasilitas, mitra, dan program yang membuat lulusan siap masuk industri.",
                   "Mengapa Eskalaber")}
  <div class="bento">{''.join(bento_cells)}</div>
</div></section>'''

    news_cards = "".join(H.news_card(n, i, feature=(i == 0)) for i, n in enumerate(NEWS[:7]))
    news = f'''<section class="section section--soft" id="berita"><div class="container">
  {H.section_head("Berita & kegiatan terbaru", "", "Eskalaber News", H.btn("Semua berita", "berita.html", "ghost", "arrow"))}
  <div class="grid grid--3">{news_cards}</div>
</div></section>'''

    tiles = "".join(H.gallery_tile(g) for g in GALLERY[:4])
    gallery = f'''<section class="section" id="galeri"><div class="container">
  {H.section_head("Sekilas suasana sekolah", "", "Galeri", H.btn("Buka galeri lengkap", "galeri.html", "ghost", "arrow"))}
  <div class="grid grid--4">{tiles}</div>
</div></section>'''

    partners = "".join(f'<span class="tag">{H.esc(m)}</span>' for m in MITRA)
    mitra = f'''<section class="section--tight"><div class="container">
  {H.section_head("Dipercaya mitra industri & akademik", "", "Kemitraan")}
  <div class="row gap-2">{partners}</div>
</div></section>'''

    cta = f'''<section class="section--tight"><div class="container">
  <div class="cta">
    <div>
      <h2 class="cta__title">Penerimaan murid baru 2026 telah dibuka</h2>
      <p class="cta__text">16 rombel · 36 murid per kelas · jalur afirmasi, nilai rapor + TKA, dan prestasi.</p>
    </div>
    <div class="cta__actions">
      {H.btn("Info SPMB 2026", "ppdb.html", "primary", "arrow")}
      {H.btn("Lihat pengumuman", "pengumuman.html", "ghost")}
    </div>
  </div>
</div></section>'''

    return H.page("index", hero + stats + welcome + programs + bento + news + gallery + mitra + cta)


# ===========================================================  JURUSAN
def jurusan() -> str:
    clusters = []
    for key, cl in C.CLUSTERS.items():
        names = " · ".join(PROGS[i]["short"] for i in cl["ids"])
        clusters.append(f'''<article class="card" data-cluster="{key}">
  <div class="card__body">
    <p class="card__kicker">{cl["rombel"]} rombel</p>
    <h3 class="card__title">{H.esc(cl["label"])}</h3>
    <p class="card__text">{H.esc(names)}</p>
  </div>
</article>''')
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Jurusan</strong></nav>
  <h1 class="page-head__title">7 Konsentrasi Keahlian</h1>
  <p class="lead">Tiga program keahlian — Teknik Otomotif, Teknik Komputer &amp; Informatika, serta Teknologi Pertanian — dengan bengkel, lab, dan lahan praktik sendiri.</p>
</div></header>'''
    summary = f'<section class="section--tight"><div class="container"><div class="grid grid--3">{"".join(clusters)}</div></div></section>'
    grid = f'<section class="section--tight flush-top"><div class="container" id="program">{_programs_grid()}</div></section>'
    cta = f'''<section class="section--tight"><div class="container">
  <div class="cta">
    <div><h2 class="cta__title">Masih bingung memilih jurusan?</h2>
    <p class="cta__text">Ikuti tur virtual 360° sekolah atau tanyakan langsung ke panitia — kami bantu petakan minatmu.</p></div>
    <div class="cta__actions">{H.btn("Tur virtual", C.SCHOOL["tour"], "primary", "", external=True)}{H.btn("Tanya panitia", "kontak.html", "ghost")}</div>
  </div>
</div></section>'''
    return H.page("jurusan", head + summary + grid + cta)


# ===========================================================  BERITA
def berita() -> str:
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Berita</strong></nav>
  <h1 class="page-head__title">Berita &amp; Artikel</h1>
  <p class="lead">Arsip lengkap kegiatan, prestasi, dan pengumuman Eskalaber — teks penuh, foto, dan video tersimpan lokal.</p>
</div></header>'''
    cats = []
    for n in NEWS:
        for c in (n.get("c") or []):
            if c not in cats:
                cats.append(c)
    chips = '<button class="chip is-on" type="button" data-cat="Semua" aria-pressed="true">Semua</button>' + \
        "".join(f'<button class="chip" type="button" data-cat="{H.esc(c)}" aria-pressed="false">{H.esc(c)}</button>' for c in cats)
    first = "".join(H.news_card(n, i) for i, n in enumerate(NEWS[:9]))
    body = f'''<section class="section--tight"><div class="container">
  <div class="toolbar">
    <div class="chips" id="news-chips" role="group" aria-label="Filter kategori">{chips}</div>
    <label class="search">{H.icon("search")}<input type="search" id="news-search" placeholder="Cari artikel…" aria-label="Cari artikel"></label>
  </div>
  <p class="card__kicker" id="news-count" aria-live="polite">{len(NEWS)} artikel</p>
  <div class="grid grid--3" id="news-grid" aria-live="polite" class="mt-4">{first}</div>
  <nav class="pager" id="news-pager" aria-label="Halaman berita"></nav>
</div></section>'''
    return H.page("berita", head + body, extra_js='\n<script defer src="assets/js/data-full.js"></script>')


# ===========================================================  GALERI
def galeri() -> str:
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Galeri</strong></nav>
  <h1 class="page-head__title">Galeri Sekolah</h1>
  <p class="lead">48 foto kurasi: kegiatan, ekstrakurikuler, jurusan, prestasi, fasilitas, dan informasi sekolah.</p>
</div></header>'''
    groups = []
    for g in GALLERY:
        if g["g"] not in groups:
            groups.append(g["g"])
    chips = '<button class="chip is-on" type="button" data-g="Semua" aria-pressed="true">Semua</button>' + \
        "".join(f'<button class="chip" type="button" data-g="{H.esc(g)}" aria-pressed="false">{H.esc(g.capitalize())}</button>' for g in groups)
    grid = "".join(H.gallery_tile(g) for g in GALLERY)
    body = f'''<section class="section--tight"><div class="container">
  <div class="chips" id="galeri-chips" role="group" aria-label="Filter galeri" class="chips mb-6">{chips}</div>
  <div class="masonry" id="galeri-grid">{grid}</div>
</div></section>'''
    return H.page("galeri", head + body)


# ===========================================================  KEGIATAN
def kegiatan() -> str:
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Kegiatan</strong></nav>
  <h1 class="page-head__title">Kegiatan, Ekskul &amp; Prestasi</h1>
  <p class="lead">Kehidupan siswa Eskalaber di luar jam pelajaran: 17 ekstrakurikuler, kegiatan karakter, dan prestasi kabupaten hingga internasional.</p>
</div></header>'''

    def ekskul_card(row, i):
        nama, pembina = row[1], row[2]
        return f'''<article class="card reveal">
  <div class="card__body">
    <p class="card__kicker">{i + 1:02d}</p>
    <h3 class="card__title">{H.esc(nama)}</h3>
    <p class="card__text">Pembina: {H.esc(pembina)}</p>
  </div>
</article>'''

    eks = "".join(ekskul_card(r, i) for i, r in enumerate(EKSUL))

    def prestasi_card(p):
        return f'''<article class="card reveal">
  <div class="card__body">
    <p class="card__kicker">{H.esc(H._date(p["d"]))}</p>
    <h3 class="card__title">{H.esc(p["t"])}</h3>
  </div>
</article>'''

    pres = "".join(prestasi_card(p) for p in PRESTASI)
    lama = "".join(f'<span class="tag">{H.esc(x)}</span>' for x in PRESTASI_LAMA)

    body = f'''<section class="section--tight"><div class="container">
  {H.section_head("17 wadah bakat & minat", "Kegiatan non-akademik untuk mengembangkan kepribadian, bakat, dan kemampuan siswa.", "Ekstrakurikuler")}
  <div class="grid grid--4" id="ekskul-grid">{eks}</div>
</div></section>
<section class="section section--soft"><div class="container">
  {H.section_head("Papan prestasi 2024–2026", "Dari LKS provinsi, SEASO Penang Malaysia, olimpiade sains, hingga kejuaraan pencak silat dan e-sport.", "Prestasi")}
  <div class="grid grid--3" id="prestasi-grid">{pres}</div>
  <h3 class="h3 mt-8">Prestasi periode sebelumnya</h3>
  <div class="row" id="prestasi-lama" >{lama}</div>
</div></section>'''
    return H.page("kegiatan", head + body)


# ===========================================================  PROFIL
def _rows_teachers() -> str:
    out = []
    for r in TEACHERS:
        cells = "".join(f'<td>{H.esc(c)}</td>' for c in r[1:])
        out.append(f'<tr><td class="is-num">{H.esc(r[0])}</td>{cells}</tr>')
    return "".join(out)


def _rows_staff() -> str:
    out = []
    for r in STAFF:
        cells = "".join(f'<td>{H.esc(c)}</td>' for c in r[1:])
        out.append(f'<tr><td class="is-num">{H.esc(r[0])}</td>{cells}</tr>')
    return "".join(out)


def _rows_mou() -> str:
    out = []
    for r in MOU:
        cells = "".join(f'<td>{H.esc(c)}</td>' for c in r[1:])
        out.append(f'<tr><td class="is-num">{H.esc(r[0])}</td>{cells}</tr>')
    return "".join(out)


def profil() -> str:
    P = C.PROFIL
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Profil</strong></nav>
  <h1 class="page-head__title">{H.esc(P["hero"]["title"])}</h1>
  <p class="lead">{H.esc(P["hero"]["lead"])}</p>
</div></header>'''

    pts = "".join(f'<li class="info-item"><span class="info-item__ico">{H.icon("check")}</span><div><h3>{H.esc(a)}</h3><p>{H.esc(b)}</p></div></li>' for a, b in P["about"]["points"])
    about = f'''<section class="section--tight"><div class="container">
  <div class="split">
    <div>{H.eyebrow(P["about"]["eyebrow"])}<h2 class="h2">{H.esc(P["about"]["title"])}</h2>
      <p class="lead mt-4">{H.esc(P["about"]["body"])}</p></div>
    <ul class="info-list">{pts}</ul>
  </div>
</div></section>'''

    tl = "".join(
        f'<li class="timeline__item"><p class="timeline__year">{H.esc(y)}</p><h3 class="timeline__title">{H.esc(t)}</h3><p class="timeline__text">{H.esc(d)}</p></li>'
        for y, t, d in P["timeline"])
    history = f'''<section class="section section--soft"><div class="container">
  {H.section_head("Arah langkah Eskalaber", "Perjalanan sejak 2008 hingga menjadi SMK Pusat Keunggulan.", "Sejarah singkat")}
  <ol class="timeline">{tl}</ol>
</div></section>'''

    misi = "".join(f"<li>{H.esc(m)}</li>" for m in MISI)
    tujuan = "".join(f"<li>{H.esc(t)}</li>" for t in TUJUAN)
    vision = f'''<section class="section--tight"><div class="container">
  <div class="split items-start">
    <div>{H.eyebrow("Visi")}<h2 class="h2">{H.esc(P["vision"])}</h2></div>
    <div>
      <h3 class="h3">Misi</h3><ul class="stack mt-3">{misi}</ul>
      <h3 class="h3 mt-7">Tujuan</h3><ul class="stack mt-3">{tujuan}</ul>
    </div>
  </div>
</div></section>'''

    sar = "".join(
        f'''<article class="card"><div class="card__media"><img src="{img}" alt="" loading="lazy" decoding="async"></div>
        <div class="card__body"><h3 class="card__title">{H.esc(t)}</h3><p class="card__text">{H.esc(d)}</p></div></article>'''
        for t, d, img in P["sarpras"])
    sarpras = f'''<section class="section section--soft"><div class="container">
  {H.section_head("Sarana & prasarana", "Fasilitas yang dipakai setiap hari oleh siswa.", "Fasilitas")}
  <div class="grid grid--3">{sar}</div>
</div></section>'''

    siswa_rows = "".join(f'<tr><td>{H.esc(k)}</td><td class="is-num">{H.esc(v)}</td></tr>' for k, v in P["students"])
    data = f'''<section class="section--tight"><div class="container">
  {H.section_head(f'{P["students_total"]} peserta didik', P["students_year"], "Data siswa")}
  <div class="split items-start">
    <div class="table-wrap mw-sm"><table class="table"><thead><tr><th>Tingkat</th><th class="is-num">Jumlah</th></tr></thead>
      <tbody>{siswa_rows}</tbody><tfoot><tr><td>Total</td><td class="is-num">{P["students_total"]}</td></tr></tfoot></table></div>
    <div class="info-item lsp"><span class="info-item__ico">{H.icon("shield")}</span><div class="lsp__body"><h3>LSP P-1</h3>{H.lsp_blocks(LSP)}</div></div>
  </div>
</div></section>'''

    teachers = f'''<section class="section section--soft"><div class="container">
  {H.section_head("Guru & tenaga kependidikan", "89 guru dan 25 karyawan, dengan pencarian langsung.", "Data PTK")}
  <label class="search mb-4">{H.icon("search")}<input type="search" id="guru-search" placeholder="Cari nama, mapel, atau almamater…" aria-label="Cari guru"></label>
  <p class="table-hint">{H.icon("arrow")} Geser ke samping untuk melihat kolom lainnya</p>
  <div class="table-wrap table--scroll" tabindex="0" role="region" aria-label="Tabel guru dan tenaga kependidikan, dapat digulir mendatar">
    <table class="table" id="guru-table">
      <thead><tr><th>No</th><th>Nama</th><th>JK</th><th>Almamater</th><th>Tahun lulus</th><th>Jenjang</th><th>Mata pelajaran</th></tr></thead>
      <tbody>{_rows_teachers()}</tbody>
    </table>
  </div>
  <h3 class="h3 mt-7">Tenaga kependidikan</h3>
  <div class="table-wrap table--scroll mt-3">
    <table class="table" id="karyawan-table">
      <thead><tr><th>No</th><th>Nama</th><th>JK</th><th>Jabatan</th></tr></thead>
      <tbody>{_rows_staff()}</tbody>
    </table>
  </div>
</div></section>'''

    mou = f'''<section class="section--tight"><div class="container">
  {H.section_head("52 kerja sama MoU", "Dunia usaha, dunia industri, dan lembaga pendidikan mitra.", "Kemitraan")}
  <div class="table-wrap table--scroll">
    <table class="table" id="mou-table">
      <thead><tr><th>No</th><th>Mitra</th><th>Bidang</th><th>Kota</th></tr></thead>
      <tbody>{_rows_mou()}</tbody>
    </table>
  </div>
</div></section>'''

    return H.page("profil", head + about + history + vision + sarpras + data + teachers + mou)


# ===========================================================  SPMB
def ppdb() -> str:
    P = C.SPMB
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>SPMB</strong></nav>
  <h1 class="page-head__title">{H.esc(P["hero"]["title"])}</h1>
  <p class="lead">{H.esc(P["hero"]["lead"])}</p>
</div></header>'''

    qrows = "".join(
        f'<tr><td>{H.esc(n)}</td><td class="is-num">{r}</td><td class="is-num">{k}</td></tr>'
        for n, r, k in P["quota"])
    quota = f'''<section class="section--tight" id="kuota"><div class="container">
  <div class="split items-start">
    <div>
      {H.eyebrow("Kuota 2026")}
      <h2 class="h2">576 kursi murid baru</h2>
      <p class="lead mt-3">{H.esc(P["quota_note"])}</p>
      {H.btn("Lihat pengumuman hasil", "pengumuman.html", "primary", "arrow")}
    </div>
    <div class="table-wrap">
      <table class="table">
        <thead><tr><th>Konsentrasi keahlian</th><th class="is-num">Rombel</th><th class="is-num">Kuota</th></tr></thead>
        <tbody>{qrows}</tbody>
        <tfoot><tr><td>Total</td><td class="is-num">{P["quota_total"][0]}</td><td class="is-num">{P["quota_total"][1]}</td></tr></tfoot>
      </table>
    </div>
  </div>
</div></section>'''

    steps = "".join(
        f'<li class="timeline__item"><p class="timeline__year">{H.esc(a)}</p><h3 class="timeline__title">{H.esc(b)}</h3><p class="timeline__text">{H.esc(c)}</p></li>'
        for a, b, c in P["steps"])
    alur = f'''<section class="section section--soft"><div class="container">
  {H.section_head("Alur pendaftaran", "Empat tahap dari pendaftaran sampai MPLS.", "Tahapan")}
  <ol class="timeline" id="alur">{steps}</ol>
</div></section>'''

    docs = "".join(
        f'''<article class="card"><div class="card__body"><h3 class="card__title">{H.esc(t)}</h3>
        <p class="card__text">{H.esc(d)}</p>
        <div class="card__foot"><a class="link" href="{u}">Buka {H.icon("arrow")}</a></div></div></article>'''
        for t, d, u in P["docs"])
    dok = f'''<section class="section--tight" id="dokumen"><div class="container">
  {H.section_head("Dokumen resmi", "Semua tautan mengarah ke halaman di situs ini.", "Pengumuman & survei")}
  <div class="grid grid--4">{docs}</div>
</div></section>'''

    faq = "".join(
        f'''<div class="acc"><button class="acc__q" type="button" aria-expanded="false">{H.esc(q)}<span class="acc__pm">+</span></button>
        <div class="acc__pane"><div>{H.esc(a)}</div></div></div>'''
        for q, a in P["faq"])
    faq_sec = f'''<section class="section section--soft" id="faq"><div class="container mw-md">
  {H.section_head("Pertanyaan yang sering diajukan", "", "FAQ", center=True)}
  <div class="accordion">{faq}</div>
</div></section>'''

    return H.page("ppdb", head + quota + alur + dok + faq_sec)


# ===========================================================  PENGUMUMAN
def pengumuman() -> str:
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Pengumuman</strong></nav>
  <h1 class="page-head__title">Pengumuman Resmi SPMB 2026</h1>
  <p class="lead">Dokumen hasil seleksi tersimpan lokal. Klik untuk membaca layar penuh per halaman.</p>
</div></header>'''

    def doc_tile(path: str, no: int, cap: str) -> str:
        return f'''<a class="tile" href="{path}" data-doc data-cap="{H.esc(cap)}">
  <img src="{path}" alt="{H.esc(cap)}" loading="lazy" decoding="async">
  <span class="doc-no">{no:02d}</span>
  <span class="tile__cap">{H.esc(cap)}</span>
</a>'''

    af = "".join(doc_tile(f"assets/img/Pengumuman-Afirmasi_page-{i:04d}.webp", i,
                          f"Hasil SPMB jalur afirmasi — halaman {i}") for i in range(1, 8))
    rp = "".join(doc_tile(f"assets/img/Pengumuman-Penerimaan-Nilai-Prestasi-Akademik-SMK-20554690_page-{i:04d}.webp", i,
                          f"Hasil SPMB jalur nilai rapor + TKA — halaman {i}") for i in range(1, 14))

    body = f'''<section class="section--tight" id="afirmasi"><div class="container">
  {H.section_head("Jalur afirmasi", "7 halaman dokumen resmi.", "Afirmasi")}
  <div class="docs">{af}</div>
</div></section>
<section class="section section--soft" id="rapor"><div class="container">
  {H.section_head("Jalur nilai rapor + TKA", "13 halaman dokumen resmi.", "Nilai rapor + TKA")}
  <div class="docs">{rp}</div>
</div></section>
<section class="section--tight"><div class="container">
  <div class="cta"><div><h2 class="cta__title">Butuh bantuan membaca hasil?</h2>
  <p class="cta__text">Hubungi panitia SPMB pada jam layanan Senin–Jumat 07.00–15.30 WIB.</p></div>
  <div class="cta__actions">{H.btn("Hubungi panitia", "kontak.html", "primary", "arrow")}{H.btn("Kembali ke SPMB", "ppdb.html", "ghost")}</div></div>
</div></section>'''
    return H.page("pengumuman", head + body)


# ===========================================================  E-MADING
def emading() -> str:
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>E-Mading</strong></nav>
  <h1 class="page-head__title">E-Mading Eskalaber</h1>
  <p class="lead">Majalah dinding digital karya tim jurnalistik dan DKV siswa — delapan edisi, dibaca layar penuh.</p>
</div></header>'''

    files = [f"Capture-{i}.webp" for i in range(1, 8)] + ["Screenshot-2024-11-08-102608.webp"]
    tiles = "".join(
        f'''<a class="tile" href="assets/img/{f}" data-doc data-cap="E-Mading edisi {i}">
  <img src="assets/img/{f}" alt="E-Mading edisi {i}" loading="lazy" decoding="async">
  <span class="doc-no">{i:02d}</span><span class="tile__cap">Edisi {i}</span>
</a>''' for i, f in enumerate(files, 1))

    body = f'''<section class="section--tight"><div class="container">
  {H.section_head("Delapan edisi", "Klik edisi untuk membaca layar penuh.", "Arsip", H.btn("Arsip Drive lengkap", D["EMADING"], "ghost", "", external=True))}
  <div class="docs">{tiles}</div>
</div></section>
<section class="section--tight"><div class="container">
  <div class="cta"><div><h2 class="cta__title">Punya karya tulis, foto, atau desain?</h2>
  <p class="cta__text">Bergabung dengan ekstrakurikuler jurnalistik atau DKV dan terbitkan karyamu di E-Mading.</p></div>
  <div class="cta__actions">{H.btn("Lihat ekstrakurikuler", "kegiatan.html", "primary", "arrow")}</div></div>
</div></section>'''
    return H.page("e-mading", head + body)


# ===========================================================  KONTAK
def kontak() -> str:
    s = C.SCHOOL
    head = f'''<header class="page-head"><div class="container">
  <nav class="crumb" aria-label="Remah"><a href="index.html">Beranda</a><span>/</span><strong>Kontak</strong></nav>
  <h1 class="page-head__title">Hubungi Kami</h1>
  <p class="lead">Pertanyaan seputar sekolah, SPMB, kerja sama industri, atau liputan kegiatan — kami senang mendengarnya.</p>
</div></header>'''

    info = f'''<ul class="info-list">
  <li class="info-item"><span class="info-item__ico">{H.icon("pin")}</span><div><h3>Alamat sekolah</h3><p>{H.esc(s["address"])}</p></div></li>
  <li class="info-item"><span class="info-item__ico">{H.icon("mail")}</span><div><h3>Email &amp; telepon</h3><p><a href="mailto:{s["email"]}">{H.email_text(s["email"])}</a> · <a href="tel:{s["phone"].replace("-","")}">{s["phone"]}</a><br><a href="mailto:{s["lsp_email"]}">{H.email_text(s["lsp_email"])}</a> (LSP P-1)</p></div></li>
  <li class="info-item"><span class="info-item__ico">{H.icon("instagram")}</span><div><h3>Instagram — {s["instagram_followers"]}</h3><p><a href="{s["instagram"]}" target="_blank" rel="noopener">{s["instagram_handle"]}</a> · {s["instagram_posts"]}</p></div></li>
  <li class="info-item"><span class="info-item__ico">{H.icon("clock")}</span><div><h3>Jam layanan</h3><p>{H.esc(s["hours"])}</p></div></li>
</ul>'''

    form = f'''<form class="form" id="kontak-form" novalidate>
  <div class="form__row">
    <div class="field"><label for="kf-n">Nama <span class="req">*</span></label><input id="kf-n" name="nama" type="text" required autocomplete="name"></div>
    <div class="field"><label for="kf-e">Email <span class="req">*</span></label><input id="kf-e" name="email" type="email" required autocomplete="email"></div>
  </div>
  <div class="field"><label for="kf-s">Subjek <span class="req">*</span></label><input id="kf-s" name="subjek" type="text" required></div>
  <div class="field"><label for="kf-p">Isi pesan <span class="req">*</span></label><textarea id="kf-p" name="pesan" required></textarea></div>
  <button class="btn btn--primary" type="submit">Kirim pesan {H.icon("arrow")}</button>
</form>'''

    forms = D["FORMS"]
    labels = ["Umpan balik pelanggan", "Kepuasan siswa", "Orang tua / wali siswa", "Dunia usaha & dunia industri", "Internal guru / karyawan"]
    survey = "".join(
        f'''<article class="card"><div class="card__body"><p class="card__kicker">Google Form resmi</p>
        <h3 class="card__title">{H.esc(l)}</h3><p class="card__text">Anonim · ± 3 menit</p>
        <div class="card__foot"><a class="link" href="{u}" target="_blank" rel="noopener">Isi survei {H.icon("arrow")}</a></div></div></article>'''
        for l, u in zip(labels, forms))

    body = f'''<section class="section--tight"><div class="container">
  <div class="split items-start">
    <div class="stack">{info}
      <div class="map"><iframe src="{s["maps"]}" title="Peta lokasi SMKN 8 Jember" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
    {form}
  </div>
</div></section>
<section class="section section--soft" id="survei"><div class="container">
  {H.section_head("Suara Anda membangun sekolah", "Kuesioner anonim untuk peningkatan mutu berkelanjutan — pilih sesuai peran Anda.", "Survei kepuasan")}
  <div class="grid grid--3">{survey}</div>
</div></section>'''
    return H.page("kontak", head + body)
