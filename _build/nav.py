#!/usr/bin/env python3
"""nav.py — SATU sumber kebenaran untuk menu situs Eskalaber.

Semua daftar tautan (nav desktop `.menu`, drawer mobile `#mmenu`, kolom
"Navigasi" di footer) dirender dari modul ini, sehingga `class="active"` +
`aria-current="page"` tidak lagi dikelola tangan (16 slot per halaman dulu).

Aturan yang diikat di sini:
  * ppdb.html berlabel "SPMB" di navigasi, tapi NAME FILE-nya tidak pernah
    berubah — mengganti nama file memutus tautan yang sudah sekolah sebar.
  * e-mading.html dan pengumuman.html ada di PRIMARY + SECONDARY sekaligus
    dan dirender ke `.menu` maupun `#mmenu`: keduanya dulu tak terlihat di
    nav desktop <=820px.
  * 10 tautan flat, tanpa popover "Lainnya" (dipangkas sebagai scope creep).

Halaman lain tidak boleh menyalin ulang markup ini; jalankan
`python3 _build/build.py` supaya blok @GENERATED tersinkron.
"""

# (href, label) — urutan tampil di navigasi.
PRIMARY = [
    ("index.html", "Beranda"),
    ("profil.html", "Profil"),
    ("jurusan.html", "Jurusan"),
    ("berita.html", "Berita"),
    ("galeri.html", "Galeri"),
    ("kegiatan.html", "Kegiatan"),
    ("ppdb.html", "SPMB"),
    ("kontak.html", "Kontak"),
]

# Halaman yang tautannya dulu cuma muncul di drawer mobile.
SECONDARY = [
    ("e-mading.html", "E-Mading"),
    ("pengumuman.html", "Pengumuman SPMB"),
]

NAV = PRIMARY + SECONDARY

# Label untuk breadcrumb/tajuk halaman turunan; diambil dari NAV supaya konsisten.
BY_HREF = {href: label for href, label in NAV}

PAGES = [href for href, _ in NAV]


def link(page: str, href: str, label: str) -> str:
    """Satu `<a>` navigasi; halaman aktif mendapat .active + aria-current."""
    if href == page:
        return f'<a href="{href}" class="active" aria-current="page">{label}</a>'
    return f'<a href="{href}">{label}</a>'


def menu(page: str) -> str:
    """<ul class="menu"> — 10 tautan flat untuk nav desktop."""
    items = "".join(f"<li>{link(page, href, label)}</li>" for href, label in NAV)
    return f'<ul class="menu">{items}</ul>'


def mmenu_links(page: str) -> str:
    """Blok tautan drawer mobile (CTA ditambahkan partial chrome.html)."""
    return "".join(link(page, href, label) for href, label in NAV)


def footer_links(page: str) -> str:
    """Kolom "Navigasi" di footer."""
    items = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in NAV)
    return f'<ul>{items}</ul>'


def crumb(page: str) -> str:
    """<div class="crumb"> untuk <header class="phero"> sebuah halaman.

    CSS memisah dengan `.crumb span[aria-hidden]` dan menandai halaman
    aktif lewat `.crumb b`, jadi tanda "/" dibungkus span dan judul
    halaman jadi <b>. Teks yang terbaca tetap sama: "Beranda / Jurusan".
    """
    if page == "index.html":
        return ""
    return ('<div class="crumb"><a href="index.html">Beranda</a>'
            f'<span aria-hidden="true">/</span><b>{BY_HREF[page]}</b></div>')
