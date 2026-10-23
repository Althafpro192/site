#!/usr/bin/env python3
"""split_data.py — pecah assets/js/data.js jadi dua berkas payload.

Konteks: `data.js` adalah SATU baris `window.ESKADATA = {…}` seberat ±1,24 MB,
dan ±85% di antaranya adalah kunci `FULL` (badan artikel 290 berita) yang hanya
dibutuhkan `berita.html`. Halaman lain membayar 1 MB untuk konten yang tidak
pernah mereka render.

Hasil:
  assets/js/data.js       window.ESKADATA      = semua kunci KECUALI FULL  (±187 KB)
  assets/js/data-full.js  window.ESKADATA_FULL = isi kunci FULL            (±1,05 MB)

Aturan yang diikat di sini:
  * Kedua berkas tetap SATU baris. Tidak ada pretty-print — ini payload,
    bukan sumber yang dibaca manusia; diff-nya pun tidak akan bisa dibaca.
  * `window.ESKADATA` tidak berganti nama (kontrak main.js).
  * Hanya `berita.html` yang men-load data-full.js (dijaga build.py --report).
  * Penggabungan dilakukan main.js:
      const D = Object.assign({}, window.ESKADATA,
                    {FULL: (window.ESKADATA_FULL || window.ESKADATA.FULL || {})})
    sehingga berita tetap jalan apa pun urutannya.

Perintah:  python3 _build/split_data.py          # idempoten
           python3 _build/split_data.py --verify # cek kontrak, jangan menulis
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "assets" / "js" / "data.js"
FULL = ROOT / "assets" / "js" / "data-full.js"

PREFIX = re.compile(r"^window\.ESKADATA\s*=\s*")
FULL_PREFIX = re.compile(r"^window\.ESKADATA_FULL\s*=\s*")

# Kontrak jumlah baris yang dibaca main.js.
COUNTS = {"NEWS": 300, "GALLERY": 48, "TEACHERS": 89, "STAFF": 25,
          "EKSUL": 17, "MOU": 52, "PRESTASI": 28, "MISI": 10, "TUJUAN": 9,
          "PRESTASI_LAMA": 8}
FULL_COUNT = 290
TEACHER_COLS = 7


def dumps_compact(obj) -> str:
    """JSON satu baris tanpa spasi tambahan — sama seperti gaya data aslinya."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=False)


def read_eskadata() -> dict:
    text = DATA.read_text(encoding="utf-8")
    head = PREFIX.match(text)
    if not head:
        sys.exit("split_data.py: data.js tidak diawali `window.ESKADATA = ` — "
                 "jangan sunting berkas ini tangan.")
    return json.loads(text[head.end():])


def read_eskadata_full() -> dict:
    text = FULL.read_text(encoding="utf-8")
    head = FULL_PREFIX.match(text)
    if not head:
        sys.exit("split_data.py: data-full.js tidak diawali `window.ESKADATA_FULL = `")
    return json.loads(text[head.end():])


def verify(data: dict, full: dict) -> list[str]:
    """Kembalikan daftar pelanggaran kontrak (kosong = aman)."""
    problems: list[str] = []
    for key, n in COUNTS.items():
        if len(data.get(key, [])) != n:
            problems.append(f"{key}: {len(data.get(key, []))} != {n}")
    cols = {len(row) for row in data.get("TEACHERS", [])}
    if cols != {TEACHER_COLS}:
        problems.append(f"TEACHERS kolom: {sorted(cols)} != [{TEACHER_COLS}]")
    if "FULL" in data:
        problems.append("FULL masih ada di data.js")
    if len(full) != FULL_COUNT:
        problems.append(f"FULL: {len(full)} != {FULL_COUNT}")
    for path in (DATA, FULL):
        body = path.read_text(encoding="utf-8")
        if "\n" in body.strip():
            problems.append(f"{path.name} bukan satu baris")
    # Isi FULL harus tetap utuh: kunci badan artikel = judul berita.
    titles = {row["t"] for row in data["NEWS"]}
    missing_titles = sorted(k for k in full if k not in titles)
    if missing_titles:
        problems.append(f"{len(missing_titles)} kunci FULL bukan judul NEWS, mis. {missing_titles[:3]}")
    return problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="jangan menulis, hanya cek kontrak")
    args = ap.parse_args(argv)

    if not DATA.exists():
        sys.exit(f"split_data.py: {DATA} hilang")

    if args.verify:
        data = read_eskadata()
        if not FULL.exists():
            sys.exit("split_data.py --verify: data-full.js belum ada; jalankan tanpa --verify")
        problems = verify(data, read_eskadata_full())
        print("\n".join(f"  - {p}" for p in problems) if problems else "--verify: kontrak utuh")
        return 1 if problems else 0

    data = read_eskadata()
    payload = data.pop("FULL", None)
    if payload is None and FULL.exists():
        payload = read_eskadata_full()          # sudah pernah di-split: jangan sampai hilang
    if payload is None:
        sys.exit("split_data.py: kunci FULL tidak ditemukan di data.js dan data-full.js belum ada")

    # Kunci disusun ulang supaya FULL tidak lagi berada di tengah berkas.
    slim = {k: v for k, v in data.items() if k != "FULL"}
    DATA.write_text("window.ESKADATA = " + dumps_compact(slim), encoding="utf-8")
    FULL.write_text("window.ESKADATA_FULL = " + dumps_compact(payload), encoding="utf-8")

    # Validasi ulang dari DISK, bukan dari objek di memori.
    problems = verify(read_eskadata(), read_eskadata_full())
    if problems:
        print("split_data.py: KONTRAK BOCOR setelah menulis:")
        print("\n".join(f"  - {p}" for p in problems))
        return 1

    print(f"data.js       {DATA.stat().st_size:>10,} B  (keys: {len(slim)}, NEWS/FULL "
          f"lihat --report)")
    print(f"data-full.js  {FULL.stat().st_size:>10,} B  ({len(payload)} badan artikel)")
    print("validasi json.loads + kontrak jumlah: LULUS")
    print("ingat: hanya berita.html yang memuat data-full.js (build.py menjaganya)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
