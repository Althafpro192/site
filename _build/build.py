#!/usr/bin/env python3
"""build.py — hasilkan 10 halaman dari content + components + pages.

    python3 _build/build.py            # tulis 10 halaman
    python3 _build/build.py --check    # exit 1 kalau file di disk beda dari hasil build
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pages  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

JOBS = {
    "index.html": pages.index,
    "profil.html": pages.profil,
    "jurusan.html": pages.jurusan,
    "berita.html": pages.berita,
    "galeri.html": pages.galeri,
    "kegiatan.html": pages.kegiatan,
    "ppdb.html": pages.ppdb,
    "pengumuman.html": pages.pengumuman,
    "e-mading.html": pages.emading,
    "kontak.html": pages.kontak,
}


def main() -> int:
    check = "--check" in sys.argv
    drift = []
    for name, fn in JOBS.items():
        html = fn()
        path = ROOT / name
        if check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != html:
                drift.append(name)
        else:
            path.write_text(html, encoding="utf-8")

    if check:
        if drift:
            print("DRIFT: " + ", ".join(drift))
            print("jalankan: python3 _build/build.py")
            return 1
        print(f"--check: {len(JOBS)} halaman sinkron dengan templat")
        return 0

    print(f"build: {len(JOBS)} halaman ditulis")
    for name in JOBS:
        print(f"  {name:18s} {(ROOT / name).stat().st_size / 1024:6.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
