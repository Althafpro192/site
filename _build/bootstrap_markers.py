#!/usr/bin/env python3
"""bootstrap_markers.py — tanam sepasang marker @GENERATED per region ke 10 halaman.

MENGAPA FILE INI ADA
-------------------
build.py::place() sengaja menolak bekerja kalau markernya tidak ada tepat
satu pasang — pilihan yang benar, karena menebak batas region adalah cara
paling cepat untuk merusak halaman. Konsekuensinya: build.py tidak bisa
memulai. Skrip ini melakukan sekali jalan (bootstrap) penanaman marker di
batas yang sudah dipetakan manual terhadap struktur halaman yang memang
identik, lalu build.py mengambil alih selamanya.

Setelah marker terpasang, file ini tidak perlu dijalankan lagi.

    python3 _build/bootstrap_markers.py            # dry-run, tidak menulis
    python3 _build/bootstrap_markers.py --write    # terapkan
    python3 _build/build.py --check                # buktinya
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (nama region, regex pembatas-awal, regex pembatas-akhir) — tiap pasangan
# harus match TEPAT SATU kali, dan akhir harus berada setelah awal.
BOUNDS = {
    "theme-init": (r"(?<=^<head>\n)", r"$"),
    "head-tail": (r"(?=^<link rel=\"icon\")", r"(?=^</head>$)"),
    "chrome": (r"(?=<a class=\"skip\")", r"(?=<main id=\"main\">)"),
    "boot": (r"^(?=<div class=\"boot\")", r"(?=<a class=\"skip\")"),
    "footer": (r"^(?=<footer>)", r"(?<=^</footer>$)"),
    "overlays": (r"(?=<button class=\"totop\")", r"(?=<script)"),
    "scripts": (r"(?=<script)", r"$"),
}

MARKER_HINT = "edit site/_build/partials/{name}.html, lalu: python3 _build/build.py"


def begin(name: str) -> str:
    return f"<!-- @GENERATED:BEGIN {name} — {MARKER_HINT.format(name=name)} -->"


def end(name: str) -> str:
    return f"<!-- @GENERATED:END {name} -->"


def region_span(text: str, name: str):
    """(start, end) karakter region, atau None kalau tidak unik."""
    if name == "theme-init":
        i = text.index("<head>\n") + len("<head>\n")
        return i, i
    if name == "head-tail":
        i = text.index('<link rel="icon"')
        j = text.index("</head>")
        return i, j
    if name == "chrome":
        i = text.index('<a class="skip"')
        j = text.index('<div class="boot"')
        return i, j
    if name == "boot":
        i = text.index('<div class="boot"')
        j = text.index('<main id="main">')
        return i, j
    if name == "footer":
        i = text.index("<footer>")
        j = text.index("</footer>") + len("</footer>")
        return i, j
    if name == "overlays":
        i = text.index('<button class="totop"')
        j = text.index("<script")
        return i, j
    if name == "scripts":
        i = text.index("<script")
        j = text.index("</body>")
        return i, j
    raise KeyError(name)


def process(path: Path, write: bool) -> str:
    text = orig = path.read_text(encoding="utf-8")

    if "@GENERATED:BEGIN" in text:
        return "sudah ada marker — lewati"

    # boot adalah overlay position:fixed, jadi urutan DOM-nya tidak
    # mempengaruhi tampilan. Dipindah ke tepat sebelum <main> supaya region
    # chrome (skip..boot) dan region boot (boot..main) saling lepas — kalau
    # boot dibiarkan di kiri skip link, kedua region bertumpuk dan marker
    # yang dihasilkan saling menyilang sehingga build.py menolaknya.
    bi = text.index('<div class="boot"')
    bj = text.index('<a class="skip"')
    boot_block = text[bi:bj]
    text = text[:bi] + text[bj:]
    mi = text.index('<main id="main">')
    text = text[:mi] + boot_block + text[mi:]

    # Urut maju mengikuti dokumen. region_span() mencari anchornya ulang pada
    # teks terkini, jadi penyisipan sebelumnya tidak membuat offset basi —
    # dan menyisipkan terbalik justru membuat END overlays jatuh ke dalam
    # region scripts, karena keduanya berbagi anchor "<script".
    order = ["theme-init", "head-tail", "chrome", "boot", "footer", "overlays", "scripts"]
    for name in order:
        i, j = region_span(text, name)
        if i < j:
            text = text[:j] + "\n" + end(name) + "\n" + text[j:]
            text = text[:i] + begin(name) + "\n" + text[i:]
        else:
            text = text[:i] + begin(name) + "\n" + end(name) + "\n" + text[i:]

    if write:
        path.write_text(text, encoding="utf-8")
    return f"{len(text) - len(orig):+d} B marker"


if __name__ == "__main__":
    write = "--write" in sys.argv
    for p in sorted(ROOT.glob("*.html")):
        print(f"  {p.name:18s} {process(p, write)}")
    print("MODE:", "TERTULIS — jalankan: python3 _build/build.py --check"
          if write else "dry-run (tambahkan --write)")
