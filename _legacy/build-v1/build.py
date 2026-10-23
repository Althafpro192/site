#!/usr/bin/env python3
"""build.py — injector parsial waktu-build untuk situs SMKN 8 Jember "Eskalaber".

MENGAPA build-time dan bukan runtime
------------------------------------
Hasil akhirnya harus tetap jalan saat pengguna mengganda-klik `index.html`
(protocol `file://`) dan saat JavaScript dimatikan. Karena itu `fetch()` parsial
dan ES modules dilarang: chrome (skip link, topbar, nav, drawer, ticker, boot,
footer, overlay, tag script) DISALIN ke dalam 10 halaman pada waktu-build,
sehingga tiap halaman tetap dokumen mandiri.

Idempoten
---------
Tiap blok dibatasi sepasang marker:

    <!-- @GENERATED:BEGIN chrome — edit site/_build/partials/chrome.html, lalu: python3 _build/build.py -->
    ...isi hasil render...
    <!-- @GENERATED:END chrome -->

Menjalankan ulang build hanya menimpa daerah di antara marker — tidak ada
penumpukan duplikat seperti pada `_legacy_inject_boot.py` (arsip).

Perintah
--------
    python3 _build/build.py                  # bangun semua 10 halaman
    python3 _build/build.py --only berita.html
    python3 _build/build.py --check          # exit 1 kalau ada drift (gerbang commit)
    python3 _build/build.py --report         # gerbang mutu, exit 1 kalau ada yang gagal
    python3 _build/build.py imgsizes         # width/height intrinsik semua <img> via Pillow
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PARTIALS = ROOT / "_build" / "partials"
JS = ROOT / "assets" / "js"

PAGES = nav.PAGES

# Daerah yang di-generate, dalam urutan kemunculan di dokumen.
REGIONS = ("theme-init", "head-tail", "chrome", "boot", "footer", "overlays", "scripts")

# Hanya halaman berita yang memuat arsip penuh (±1,05 MB).
FULL_PAGES = ("berita.html",)

# Kelas yang diset JS pada runtime: sah kalau tidak muncul di markup.
# Kelas yang diset JS pada runtime: sah kalau tidak muncul di markup.
# ".locked"/".js" dipasang stylesheet-driven dari main.js, ".has-img" dan
# ".theme-fade" likewise, ".form-note" dibuat lewat createElement.
UNUSED_ALLOWLIST = {".in", ".on", ".open", ".scrolled", ".show", ".done",
                    ".playing", ".feature", ".locked", ".js", ".has-img",
                    ".theme-fade", ".form-note",
                    # alias sadar: markup memakai .section-head, .sec-head
                    # dipertahankan supaya kedua nama menyusun.
                    ".sec-head", ".sec-head--mid"}

MARKER_HINT = "edit site/_build/partials/{name}.html, lalu: python3 _build/build.py"


def begin_marker(name: str) -> str:
    return f"<!-- @GENERATED:BEGIN {name} — {MARKER_HINT.format(name=name)} -->"


def end_marker(name: str) -> str:
    return f"<!-- @GENERATED:END {name} -->"


# ---------------------------------------------------------------- rendering --
def render(name: str, page: str) -> str:
    """Isi partial + substitusi placeholder, siap disalin ke dalam halaman."""
    path = PARTIALS / f"{name}.html"
    if not path.exists():
        sys.exit(f"build.py: partial hilang: {path}")
    text = path.read_text(encoding="utf-8").rstrip("\n")
    extra = ""
    if page in FULL_PAGES:
        extra = '<script defer src="assets/js/data-full.js"></script>\n'
    subs = {
        "MENU": nav.menu(page),
        "MMENU_LINKS": nav.mmenu_links(page),
        "FOOTER_NAV": nav.footer_links(page),
        "DATA_EXTRA": extra,
    }
    for key, val in subs.items():
        text = text.replace("{{" + key + "}}", val)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if leftover:
        sys.exit(f"build.py: placeholder tidak terisi di {name}.html: {leftover}")
    return text


def place(doc: str, name: str, payload: str) -> str:
    """Ganti daerah antara marker dengan payload. Marker harus sudah ada."""
    beg, fin = begin_marker(name), end_marker(name)
    if doc.count(beg) != 1 or doc.count(fin) != 1:
        raise MarkerError(
            f"marker @{name.upper()} harus ada tepat satu pasang "
            f"(BEGIN={doc.count(beg)}, END={doc.count(fin)}); "
            f"tempel ulang sepasang marker di {name}.html")
    i = doc.index(beg) + len(beg)
    j = doc.index(fin, i)
    if j < i:
        raise MarkerError(f"marker @{name.upper()} tersusun terbalik")
    return doc[:i] + "\n" + payload + "\n" + doc[j:]


class MarkerError(RuntimeError):
    pass


def build_page(page: str) -> tuple[str, bool]:
    """Bangun satu halaman; kembalikan (isi_baru, berubah)."""
    path = ROOT / page
    doc = path.read_text(encoding="utf-8")
    out = doc
    for name in REGIONS:
        out = place(out, name, render(name, page))
    return out, out != doc


def check_page(page: str) -> list[str]:
    """Daftar nama daerah yang menyimpang dari partialnya (tanpa menulis file)."""
    doc = (ROOT / page).read_text(encoding="utf-8")
    bad = []
    for name in REGIONS:
        beg, fin = begin_marker(name), end_marker(name)
        if doc.count(beg) != 1 or doc.count(fin) != 1:
            bad.append(f"{name} (marker hilang/dobel)")
            continue
        inner = doc[doc.index(beg) + len(beg): doc.index(fin, doc.index(beg))]
        if inner.strip("\n") != render(name, page).strip("\n"):
            bad.append(name)
    return bad


# ------------------------------------------------------------ img dimensions --
IMGTAG = re.compile(r"<img\b[^>]*>", re.S)
SRCRE = re.compile(r'src="([^"]*)"')
DIMRE = re.compile(r'\b(width|height)="(\d+)"')


def image_size(src: str, cache: dict):
    """(w, h) dari file aset, atau None kalau tidak bisa dibaca."""
    if src in cache:
        return cache[src]
    path = ROOT / src
    value = None
    if path.exists():
        try:
            from PIL import Image
            with Image.open(path) as im:
                value = im.size
        except Exception as exc:  # noqa: BLE001 — aset rusak tidak boleh menghentikan build
            print(f"  imgsizes: {src} tidak terbaca ({exc.__class__.__name__})")
    cache[src] = value
    return value


def fix_imgs(text: str, cache: dict) -> tuple[str, int]:
    """Pasang width/height intrinsik + loading/decoding pada tiap <img> yang belum punya."""
    touched = [0]

    def repl(m: re.Match) -> str:
        tag = m.group(0)
        src_m = SRCRE.search(tag)
        src = src_m.group(1) if src_m else ""
        if not src or "{" in src or src.endswith("_"):
            return tag                                    # placeholder runtime / template JS
        add: list[str] = []
        size = image_size(src, cache)
        if size:
            w, h = size
            if not re.search(r'\bwidth="\d+"', tag):
                add.append(f'width="{w}"')
            if not re.search(r'\bheight="\d+"', tag):
                add.append(f'height="{h}"')
        if "loading=" not in tag:
            add.append('loading="lazy"')
        if "decoding=" not in tag:
            add.append('decoding="async"')
        if not add:
            return tag
        touched[0] += 1
        at = src_m.end()
        return tag[:at] + " " + " ".join(add) + tag[at:]

    return IMGTAG.sub(repl, text), touched[0]


def cmd_imgsizes(pages: list[str]) -> int:
    """Tambal width/height intrinsik di halaman DAN di partial chrome."""
    cache: dict = {}
    total = 0
    targets = [PARTIALS / f"{n}.html" for n in REGIONS if (PARTIALS / f"{n}.html").exists()]
    targets += [ROOT / p for p in pages]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        new, n = fix_imgs(text, cache)
        if new != text:
            path.write_text(new, encoding="utf-8")
            total += n
            print(f"  {path.relative_to(ROOT)}: {n} <img> ditambal")
    print(f"imgsizes: {len(cache)} berkas baca ukurannya, {total} tag <img> berubah")
    if any(p.parent == PARTIALS for p in targets):
        print("imgsizes: kalau partial chrome berubah, jalankan lagi `python3 _build/build.py`")
    return total


# ------------------------------------------------------------------- report --
CLS_IN_SELECTOR = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")
CLASS_ATTR = re.compile(r'\bclass="([^"]*)"')
CLASSLIST = re.compile(r"classList\.(?:add|remove|toggle|contains)\(([^)]*)\)")
STRING = re.compile(r'"([^"]*)"|\'([^\']*)\'')
ASSET = re.compile(r"assets/(?:img|video)/[A-Za-z0-9._\-]+")


def css_selector_text(css: str) -> str:
    """Buang komentar dan isi blok deklarasi, sisakan hanya selektor."""
    text = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for _ in range(12):
        shorter = re.sub(r"\{[^{}]*\}", "{}", text)
        if shorter == text:
            break
        text = shorter
    return text


def defined_classes() -> set[str]:
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    return {"." + c for c in CLS_IN_SELECTOR.findall(css_selector_text(css))}


def used_classes(pages: list[str]) -> set[str]:
    found: set[str] = set()
    for path in [ROOT / p for p in pages] + list(PARTIALS.glob("*.html")):
        for attr in CLASS_ATTR.findall(path.read_text(encoding="utf-8")):
            found |= {"." + c for c in attr.split() if c}
    main = (JS / "main.js").read_text(encoding="utf-8")
    for attr in CLASS_ATTR.findall(main):
        # Buang seluruh ekspresi ${ ... } lebih dulu. Menguji per token tidak
        # cukup: "chip ${x === g ? \"on\" : \"\"}" dipecah spasi menjadi token
        # bersih bernama "g" dan "page", yang lalu dilaporkan sebagai kelas
        # tanpa gaya. Gerbang yang menjerit palsu akan diabaikan orang.
        stripped = re.sub(r"\$\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", " ", attr)
        # CLASS_ATTR berhenti di kutip pertama, jadi "chip ${x === g ? \"on\""
        # menyisakan ${ yang tidak tertutup dan variabel g lolos sebagai kelas.
        # Apa pun sesudah ${ yang menggantung bukan nama kelas.
        stripped = stripped.split("${")[0]
        for token in stripped.split():
            if re.fullmatch(r"[_a-zA-Z][\w-]*", token):
                found.add("." + token)
    for args in CLASSLIST.findall(main):
        for s in STRING.findall(args):
            for tok in [x for x in s if x]:
                for c in tok.split():
                    if re.fullmatch(r"[_a-zA-Z][\w-]*", c):
                        found.add("." + c)
    return found


def asset_refs() -> tuple[list[str], int, int]:
    """(daftar bolong, jumlah dinamis, jumlah referensi) atas aset di HTML/JS/data."""
    blobs = []
    for path in [ROOT / p for p in PAGES] + list(PARTIALS.glob("*.html")) + \
            [JS / "main.js", JS / "data.js"]:
        if path.exists():
            blobs.append(path.read_text(encoding="utf-8"))
    refs: list[str] = []
    for blob in blobs:
        refs += ASSET.findall(blob)
    missing, dynamic = [], 0
    for ref in refs:
        if ref.endswith("_"):
            dynamic += 1                  # template JS seperti assets/img/yt_${id}.webp
            continue
        if not (ROOT / ref).exists():
            missing.append(ref)
    return sorted(set(missing)), dynamic, len(refs)


def orphan_assets() -> list[str]:
    """Berkas gambar/video di repo yang tidak dirujuk mana pun (dilaporkan, tidak dihapus)."""
    referenced = set()
    for path in [ROOT / p for p in PAGES] + list(PARTIALS.glob("*.html")) + \
            [JS / "main.js", JS / "data.js"]:
        if path.exists():
            referenced |= set(ASSET.findall(path.read_text(encoding="utf-8")))
    on_disk = set()
    for folder in ("img", "video"):
        on_disk |= {f"assets/{folder}/{p.name}" for p in (ROOT / "assets" / folder).iterdir()}
    return sorted(on_disk - referenced)


def inline_styles(pages: list[str]) -> dict[str, int]:
    return {p: (ROOT / p).read_text(encoding="utf-8").count('style="') for p in pages}


def h1_counts(pages: list[str]) -> dict[str, int]:
    return {p: len(re.findall(r"<h1\b", (ROOT / p).read_text(encoding="utf-8"))) for p in pages}


def img_dimension_gaps(pages: list[str]) -> tuple[list[str], list[str], list[str]]:
    no_dims, no_lazy, runtime = [], [], []
    for p in pages:
        for tag in IMGTAG.findall((ROOT / p).read_text(encoding="utf-8")):
            src_m = SRCRE.search(tag)
            src = src_m.group(1) if src_m else ""
            ident = f"{p} {src or tag[:40]}"
            if not src or src.endswith("_"):
                runtime.append(ident)
                continue
            if not re.search(r'\bwidth="\d+"', tag) or not re.search(r'\bheight="\d+"', tag):
                no_dims.append(ident)
            if "loading=" not in tag or "decoding=" not in tag:
                no_lazy.append(ident)
    return no_dims, no_lazy, runtime


def load_global(js_path: Path, prefix: re.Pattern) -> dict | None:
    """Baca `window.X = {…}` jadi dict; None kalau prefiks tidak cocok."""
    text = js_path.read_text(encoding="utf-8")
    head = prefix.match(text)
    if not head:
        return None
    return json.loads(text[head.end():])


def data_checks() -> list[tuple[str, bool, str]]:
    """Validasi hasil split_data.py: JSON lolos + jumlah baris kontrak."""
    base = JS / "data.js"
    full = JS / "data-full.js"
    if not base.exists():
        return [("data.js ada", False, "hilang")]
    try:
        data = load_global(base, re.compile(r"^window\.ESKADATA\s*=\s*"))
    except json.JSONDecodeError as exc:
        return [("data.js JSON valid", False, str(exc))]
    if data is None:
        return [("data.js berprefiks window.ESKADATA =", False, "prefiks tidak dikenali")]
    rows = [("data.js JSON valid", True, f"{base.stat().st_size:,} B")]
    want = {"NEWS": 300, "GALLERY": 48, "TEACHERS": 89, "STAFF": 25,
            "EKSUL": 17, "MOU": 52}
    for key, n in want.items():
        got = len(data.get(key, []))
        rows.append((f"{key} = {n}", got == n, f"{got}"))
    cols = {len(t) for t in data.get("TEACHERS", [])}
    rows.append(("TEACHERS 7 kolom", cols == {7}, f"{sorted(cols)}"))
    rows.append(("FULL tidak ada di data.js", "FULL" not in data,
                 "masih ada" if "FULL" in data else "bersih"))
    if not full.exists():
        return rows + [("data-full.js ada", False, "jalankan split_data.py")]
    try:
        payload = load_global(full, re.compile(r"^window\.ESKADATA_FULL\s*=\s*"))
    except json.JSONDecodeError as exc:
        return rows + [("data-full.js JSON valid", False, str(exc))]
    if payload is None:
        return rows + [("data-full.js berprefiks window.ESKADATA_FULL =", False, "prefiks tidak dikenali")]
    return rows + [
        ("data-full.js JSON valid", True, f"{full.stat().st_size:,} B"),
        ("FULL = 290", len(payload) == 290, f"{len(payload)}"),
    ]


def print_report(pages: list[str], strict: bool) -> int:
    fails: list[str] = []
    soft: list[str] = []
    print("build.py --report — gerbang mutu")
    print("=" * 72)

    # 1. drift marker
    drift = {p: check_page(p) for p in pages if check_page(p)}
    ok = not drift
    print(f"[{'ok  ' if ok else 'GAGG'}] drift          {len(drift)} halaman menyimpang dari partial")
    for p, names in drift.items():
        print(f"        {p}: {', '.join(names)}")
    if not ok:
        fails.append("drift")

    # 2. inline style
    styles = inline_styles(pages)
    total = sum(styles.values())
    print(f"[{'ok  ' if total == 0 else 'GAGG'}] inline-styles  {total} buah")
    for p, n in styles.items():
        if n:
            print(f"        {p}: {n}")
    if total:
        fails.append("inline-styles")

    # 3. h1 per halaman
    h1 = h1_counts(pages)
    bad_h1 = {p: n for p, n in h1.items() if n != 1}
    print(f"[{'ok  ' if not bad_h1 else 'GAGG'}] h1             "
          f"{sum(h1.values())} di {len(pages)} halaman; 1 per halaman = {not bad_h1}")
    for p, n in bad_h1.items():
        print(f"        {p}: {n}")
    if bad_h1:
        fails.append("h1")

    # 4. kelas dipakai tapi tidak didefinisikan CSS
    defined = defined_classes()
    used = used_classes(pages)
    undef = sorted(used - defined)
    print(f"[{'ok  ' if not undef else 'GAGG'}] undefined-class {len(undef)} dipakai, "
          f"{len(used)} total; CSS mendefinisikan {len(defined)}")
    print(f"        {' '.join(undef) if undef else '—'}")
    if undef:
        (soft if not strict else fails).append("undefined-classes")

    # 5. kelas didefinisikan tapi tidak dipakai
    unused = sorted(defined - used - UNUSED_ALLOWLIST)
    print(f"[{'ok  ' if not unused else 'GAGG'}] defined-unused {len(unused)} dari {len(defined)}")
    print(f"        {' '.join(unused) if unused else '—'}")
    if unused:
        (soft if not strict else fails).append("defined-unused")

    # 6. width/height <img>
    no_dims, no_lazy, runtime = img_dimension_gaps(pages)
    n_img = sum(len(IMGTAG.findall((ROOT / p).read_text(encoding="utf-8"))) for p in pages)
    print(f"[{'ok  ' if not no_dims else 'GAGG'}] img-dims        {n_img} <img>; "
          f"{n_img - len(no_dims) - len(runtime)} bersukuran, {len(runtime)} placeholder runtime, "
          f"{len(no_dims)} bolong")
    for x in no_dims[:12]:
        print(f"        {x}")
    if no_dims:
        fails.append("img-dims")
    print(f"[{'ok  ' if not no_lazy else 'GAGG'}] lazy/decoding   {len(no_lazy)} tanpa loading|decoding")
    for x in no_lazy[:12]:
        print(f"        {x}")
    if no_lazy:
        fails.append("lazy")

    # 7. referensi aset
    missing, dynamic, n_refs = asset_refs()
    print(f"[{'ok  ' if not missing else 'GAGG'}] aset resolve    {n_refs} referensi "
          f"({dynamic} dinamis dari template JS), {len(missing)} bolong")
    for x in missing[:12]:
        print(f"        {x}")
    if missing:
        fails.append("aset")
    orphans = orphan_assets()
    print(f"[info ] aset tak dirujuk {len(orphans)} berkas di assets/img|video "
          f"(dibiarkan — butuh masukan sekolah, lihat README)")

    # 8. data split
    for label, ok_row, detail in data_checks():
        print(f"[{'ok  ' if ok_row else 'GAGG'}] data            {label} ({detail})")
        if not ok_row:
            fails.append(label)

    # 9. data-full.js hanya di berita.html
    leaks = [p for p in pages
             if ("data-full.js" in (ROOT / p).read_text(encoding="utf-8")) != (p in FULL_PAGES)]
    print(f"[{'ok  ' if not leaks else 'GAGG'}] data-full scope hanya {', '.join(FULL_PAGES)}; "
          f"bocor: {leaks or '—'}")
    if leaks:
        fails.append("data-full scope")

    # 10. scaffold a11y yang jadi tanggung jawab HTML
    scaffold = []
    for p in pages:
        doc = (ROOT / p).read_text(encoding="utf-8")
        body = doc[doc.index("<body"):]
        # Marker @GENERATED adalah komentar, dan komentar bukan elemen:
        # skip link tetap anak pertama <body> secara DOM. Mengukur dengan
        # jarak byte membuat pemeriksaan ini selalu gagal setelah injeksi.
        body_no_comments = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        first = re.search(r'<a class="skip" href="#main">', body_no_comments)
        problems = []
        if not first:
            problems.append("skip link")
        elif first.start() > 40:
            problems.append("skip link bukan anak pertama <body>")
        if "<main id=\"main\">" not in doc:
            problems.append("<main id=main>")
        if 'aria-label="Navigasi utama"' not in doc:
            problems.append("nav aria-label")
        if '<html lang="id" class="is-loading">' not in doc:
            problems.append("html.is-loading")
        if problems:
            scaffold.append((p, problems))
    print(f"[{'ok  ' if not scaffold else 'GAGG'}] a11y scaffold   {len(scaffold)} halaman bolong")
    for p, problems in scaffold:
        print(f"        {p}: {', '.join(problems)}")
    if scaffold:
        fails.append("a11y scaffold")

    print("=" * 72)
    if soft:
        print(f"lunak (tidak menggagalkan, lihat catatan): {', '.join(soft)}")
    if fails:
        print(f"GAGAL: {', '.join(dict.fromkeys(fails))}")
        return 1
    print("LULUS semua gerbang keras.")
    return 0


# --------------------------------------------------------------------- main --
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Injector parsial + gerbang mutu situs Eskalaber.")
    ap.add_argument("--only", action="append", metavar="HALAMAN.html",
                    help="bangun satu halaman saja (boleh diulang)")
    ap.add_argument("--check", action="store_true",
                    help="jangan menulis; exit 1 kalau ada drift terhadap partial")
    ap.add_argument("--report", action="store_true", help="cetak gerbang mutu")
    ap.add_argument("--strict", action="store_true",
                    help="gagalkan juga pemeriksaan yang bergantung pada CSS yang masih dikerjakan")
    ap.add_argument("cmd", nargs="?", choices=("imgsizes",),
                    help="imgsizes = pasang width/height intrinsik semua <img>")
    args = ap.parse_args(argv)

    pages = args.only or list(PAGES)
    unknown = [p for p in pages if p not in PAGES]
    if unknown:
        ap.error(f"halaman tidak dikenal: {unknown}")

    if args.cmd == "imgsizes":
        cmd_imgsizes(pages)
        return 0

    if args.report:
        return print_report(pages, args.strict)

    if args.check:
        bad = False
        for p in pages:
            for name in check_page(p):
                print(f"DRIFT {p}: blok @{name.upper()} tidak sama dengan partialnya")
                bad = True
        if bad:
            print("--check: jalankan `python3 _build/build.py` lalu commit hasil build-nya")
            return 1
        print(f"--check: {len(pages)} halaman sinkron dengan partial + data oke")
        return 0

    changed = []
    for p in pages:
        try:
            text, moved = build_page(p)
        except MarkerError as exc:
            print(f"build.py: {p}: {exc}", file=sys.stderr)
            return 2
        if moved:
            (ROOT / p).write_text(text, encoding="utf-8")
            changed.append(p)
    print(f"build: {len(pages)} halaman dibaca, {len(changed)} ditulis"
          + (f" ({', '.join(changed)})" if changed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
