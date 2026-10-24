#!/usr/bin/env python3
"""verify.py — gerbang mutu untuk situs hasil build."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets/css/style.css"
PAGES = ["index.html", "profil.html", "jurusan.html", "berita.html", "galeri.html",
         "kegiatan.html", "ppdb.html", "pengumuman.html", "e-mading.html", "kontak.html"]

ok_all = True


def say(ok: bool, label: str, detail: str = "") -> None:
    global ok_all
    if not ok:
        ok_all = False
    print(f"[{'ok  ' if ok else 'GAGAL'}] {label:22s} {detail}")


def strip_comments(s: str) -> str:
    return re.sub(r"/\*.*?\*/", "", s, flags=re.S)


css_raw = CSS.read_text(encoding="utf-8")
css = strip_comments(css_raw)

# token dibaca dari CSS, bukan di-hardcode: gerbang harus menguji nilai nyata
def tokens(block: str) -> dict[str, str]:
    return dict(re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", block))

LIGHT = tokens(css.split("[data-theme=\"dark\"]")[0])
DARK = tokens(css.split("[data-theme=\"dark\"]")[1]) if '[data-theme="dark"]' in css else {}

def tok(name: str, dark: bool = False) -> str:
    src = DARK if dark else LIGHT
    v = src.get(name) or LIGHT.get(name) or ""
    m = re.match(r"var\((--[a-z0-9-]+)\)", v.strip())
    return LIGHT.get(m.group(1), v) if m else v

# 1. kelas CSS yang didefinisikan
defined = set(re.findall(r"\.([A-Za-z][\w-]*)", re.sub(r"url\([^)]*\)", "", css)))

# 2. kelas yang dipakai di HTML (dibersihkan dari marker/atribut lain)
used: dict[str, set[str]] = {}
for name in PAGES:
    text = (ROOT / name).read_text(encoding="utf-8")
    for attr in re.findall(r'class="([^"]*)"', text):
        for c in attr.split():
            if re.fullmatch(r"[A-Za-z][\w-]*", c):
                used.setdefault(c, set()).add(name)

# kelas yang hanya dipasang JS saat runtime
RUNTIME = {"is-open", "is-on", "is-in", "is-active", "is-show", "is-done", "is-tilt",
           "js", "locked", "has-img", "empty-row", "form__note", "tk", "prose", "content",
           "empty", "pager__gap", "acc__pane"}
undef = sorted(c for c in used if c not in defined and c not in RUNTIME)
say(not undef, "kelas tak terdefinisi", f"{len(undef)} — {' '.join(undef[:10]) if undef else '—'}")

unused = sorted(c for c in defined if c not in used and c not in RUNTIME)
say(not unused, "kelas tak terpakai", f"{len(unused)} — {' '.join(unused[:12]) if unused else '—'}")

# 3. inline style
inline = {n: (ROOT / n).read_text(encoding="utf-8").count('style="') for n in PAGES}
bad_inline = {k: v for k, v in inline.items() if v}
say(not bad_inline, "inline style", str(bad_inline) if bad_inline else "0 di 10 halaman")

# 4. h1 tunggal
h1 = {n: len(re.findall(r"<h1\b", (ROOT / n).read_text(encoding="utf-8"))) for n in PAGES}
say(all(v == 1 for v in h1.values()), "h1 per halaman", str(h1))

# 5. scaffold a11y
prob = []
for n in PAGES:
    t = (ROOT / n).read_text(encoding="utf-8")
    body = t[t.index("<body"):]
    clean = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    if not re.search(r'<a class="skip" href="#main">', clean):
        prob.append(f"{n}:skip")
    if not re.search(r'<main id="main"[ >]', t):
        prob.append(f"{n}:main")
    if 'aria-label="Navigasi utama"' not in t:
        prob.append(f"{n}:nav")
    if 'lang="id"' not in t:
        prob.append(f"{n}:lang")
    if t.count('aria-current="page"') < 1:
        prob.append(f"{n}:current")
say(not prob, "scaffold a11y", " ".join(prob) if prob else "10/10")

# 6. aset
missing = []
refs = 0
for n in PAGES:
    t = (ROOT / n).read_text(encoding="utf-8")
    for m in re.finditer(r'(?:src|href)="([^"#]+)"', t):
        u = m.group(1)
        if u.startswith(("http", "mailto:", "tel:", "data:", "#")) or "{" in u:
            continue
        refs += 1
        if not (ROOT / u).exists():
            missing.append(f"{n}:{u}")
say(not missing, "aset resolve", f"{refs} referensi, {len(missing)} bolong {missing[:5]}")

# 7. data
d = json.loads((ROOT / "assets/js/data.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
full = json.loads((ROOT / "assets/js/data-full.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
say(len(d["NEWS"]) == 300, "NEWS", str(len(d["NEWS"])))
say(len(full) == 290, "FULL", str(len(full)))
say(len(d["GALLERY"]) == 48, "GALLERY", str(len(d["GALLERY"])))
say(len(d["TEACHERS"]) == 89 and all(len(r) == 7 for r in d["TEACHERS"]), "TEACHERS", "89 × 7")
say(len(d["MOU"]) == 52, "MOU", str(len(d["MOU"])))

# 8. kontras token (dihitung, bukan diperkirakan)
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(x * 2 for x in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


pairs = [
    ("ink/bg", tok("--ink"), tok("--bg")),
    ("ink-body/bg", tok("--ink-body"), tok("--bg")),
    ("muted/bg", tok("--ink-muted"), tok("--bg")),
    ("muted/soft", tok("--ink-muted"), tok("--surface-soft")),
    ("faint/bg", tok("--ink-faint"), tok("--bg")),
    ("faint/soft", tok("--ink-faint"), tok("--surface-soft")),
    ("accent/bg", tok("--accent"), tok("--bg")),
    ("accent/soft", tok("--accent"), tok("--accent-soft")),
    ("on-accent/accent", tok("--on-accent"), tok("--accent")),
    ("on-accent/grad-end", tok("--on-accent"), tok("--on-accent-check")),
    ("warning/warn-soft", tok("--warning"), tok("--warning-soft")),
    ("gold-ink/gold-soft", tok("--gold-ink"), tok("--gold-soft")),
    ("gold-ink/bg", tok("--gold-ink"), tok("--bg")),
    ("on-gold/gold", tok("--on-gold"), tok("--gold")),
    ("on-deep/brand-900", tok("--on-deep"), tok("--brand-900")),
    ("on-deep-2/brand-600", tok("--on-deep-2"), tok("--brand-600")),
    ("gold-on-deep/brand-900", tok("--gold-on-deep"), tok("--brand-900")),
    ("brand-700/bg", tok("--brand-700"), tok("--bg")),
    ("cluster-blue/bg", tok("--cluster-informatika"), tok("--bg")),
    ("cluster-red/bg", tok("--cluster-omotif") or tok("--cluster-otomotif"), tok("--bg")),
    ("dark ink/bg", tok("--ink", True), tok("--bg", True)),
    ("dark muted/bg", tok("--ink-muted", True), tok("--bg", True)),
    ("dark faint/bg", tok("--ink-faint", True), tok("--bg", True)),
    ("dark accent/bg", tok("--accent", True), tok("--bg", True)),
    ("dark gold-ink/bg", tok("--gold-ink", True), tok("--bg", True)),
    ("dark on-gold/gold", tok("--on-gold", True), tok("--gold", True)),
]
fails = [(n, round(ratio(a, b), 2)) for n, a, b in pairs if ratio(a, b) < 4.5]
say(not fails, "kontras teks", f"{len(pairs)-len(fails)}/{len(pairs)} >= 4.5" + (f" — GAGAL {fails}" if fails else ""))

# 9. drift
sys.path.insert(0, str(ROOT / "_build"))
import pages  # noqa: E402

drift = []
for name, fn in [("index.html", pages.index), ("profil.html", pages.profil), ("jurusan.html", pages.jurusan),
                 ("berita.html", pages.berita), ("galeri.html", pages.galeri), ("kegiatan.html", pages.kegiatan),
                 ("ppdb.html", pages.ppdb), ("pengumuman.html", pages.pengumuman),
                 ("e-mading.html", pages.emading), ("kontak.html", pages.kontak)]:
    if (ROOT / name).read_text(encoding="utf-8") != fn():
        drift.append(name)
say(not drift, "drift templat", " ".join(drift) if drift else "0 halaman")

print()
print("LULUS semua gerbang." if ok_all else "ADA GERBANG GAGAL.")
raise SystemExit(0 if ok_all else 1)
