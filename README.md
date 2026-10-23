# Website Resmi Mandiri — SMK Negeri 8 Jember "Eskalaber"

Website ini **100% mandiri**: tidak ada satu pun tautan ke website lama, dan
**tidak ada satu pun permintaan ke pihak ketiga saat runtime** — font pun
di-self-host. Seluruh artikel, foto, video, dokumen pengumuman, dan data
tersimpan lokal di folder ini.
Sumber konten: dokumentasi & data resmi sekolah (dipindahkan menyeluruh),
Instagram @smkn8_official.

## Cara membuka

Buka `index.html` langsung di browser (dua klik, tanpa server), atau:

```bash
python3 -m http.server 8080   # lalu buka http://localhost:8080
```

Keduanya didukung. Karena itu proyek ini sengaja **tidak** memakai ES modules,
`fetch()` parsial, bundler, atau framework apa pun.

## Sistem desain: "Clean SaaS / Emerald"

Situs ini **dihasilkan**, bukan diedit tangan. `_build/build.py` merakit sepuluh
halaman dari `content.py` + `components.py` + `pages.py`; tidak ada markup yang
disalin antar halaman, dan tidak ada lapisan CSS bertumpuk.

### Palet

| Token | Nilai | Dipakai untuk |
|---|---|---|
| `--bg` / `--surface` | `#FFFFFF` | seluruh permukaan |
| `--surface-soft` | `#F7FAF8` | pita seksi, header tabel |
| `--ink` | `#0B1A14` | judul |
| `--ink-body` | `#26332D` | teks isi |
| `--ink-muted` | `#5B7268` | teks sekunder |
| `--ink-faint` | `#63756D` | label meta (4,89:1) |
| `--accent` | `#047857` | satu-satunya warna aksi |
| `--line` | `#E3EBE7` | hairline |

Warna rumpun keahlian dipakai **tipis** sebagai penanda, bukan sebagai latar:
biru `#0E63B8` (Teknologi Informasi), merah `#B42318` (Teknik Otomotif), hijau
`#047857` (Agribisnis). Bentuknya hanya strip 3px di tepi atas kartu plus
lencana — itulah yang membuatnya terasa disengaja.

Seluruh pasangan teks diukur: **16/16 ≥ 4,5:1**, dihitung dari token asli oleh
`_build/verify.py`, bukan diperkirakan.

### Tipografi

**DM Sans** (self-host, 2 berkas woff2, ±92 KB). Skala `clamp()`, tracking
negatif hanya pada display, `tabular-nums` untuk angka.

### Kartu — satu resep, satu garis dasar

```
.card          flex column, height 100%, gradient halus, shadow lembut
.card__media   aspect-ratio 16/10, object-fit cover
.card__title   clamp 2 baris
.card__text    clamp 2–3 baris
.card__foot    margin-top: auto   ← semua tombol duduk sejajar
```

Tinggi seragam datang dari `align-items: stretch` milik grid, bukan dari
memaksa tinggi tetap. Sisa baris tidak pernah dibiarkan menggantung: 7 kartu
jurusan pada grid 3 kolom menjadi 3 + 3 + **1 kartu melintang penuh**
(`.card--wide`, foto kiri, teks kanan).

### Font & media

Tidak ada permintaan runtime ke pihak ketiga. Tidak ada ES modules dan tidak
ada `fetch()` parsial, sehingga `index.html` tetap jalan saat dibuka langsung
dari berkas (`file://`).

## 10 Halaman

| File | Isi |
|---|---|
| `index.html` | Beranda: hero mozaik, ticker berita, statistik beranimasi, sambutan kepsek, 7 jurusan, bento keunggulan, berita terbaru, galeri, kemitraan, CTA SPMB |
| `profil.html` | Tentang, linimasa 2008–2026, visi–misi–tujuan, sambutan, struktur organisasi, sarpras, data siswa, LSP P-1, tabel 52 mitra MoU, 89 guru + 25 karyawan (pencarian langsung) |
| `jurusan.html` | 7 konsentrasi keahlian + prospek lulusan + video profil jurusan |
| `berita.html` | Arsip **300 artikel** (teks penuh + foto + video lokal): filter kategori, pencarian, paginasi, reader |
| `galeri.html` | 48 foto kurasi: masonry, filter, lightbox |
| `kegiatan.html` | 17 ekskul, papan prestasi 2024–2026, prestasi periode sebelumnya |
| `ppdb.html` | SPMB 2026: kuota 16 rombel (576 kursi), alur, FAQ, dokumen hasil |
| `pengumuman.html` | Dokumen hasil SPMB lokal: jalur afirmasi (7 hal.) & jalur nilai rapor+TKA (13 hal.), layar penuh per halaman |
| `e-mading.html` | Kompilasi 8 edisi E-Mading digital karya siswa |
| `kontak.html` | Alamat, email, telepon, LSP, Instagram, peta, formulir pesan, 5 survei kepuasan |

## Bangun ulang: `_build/`

Chrome (skip link, topbar, nav, drawer, ticker, intro, footer, overlay, tag
script) **tidak ditulis ulang di tiap halaman**. Isinya ada di
`_build/partials/`, dan setiap halaman hanya punya satu daerah bertanda:

```html
<!-- @GENERATED:BEGIN chrome — edit site/_build/partials/chrome.html, lalu: python3 _build/build.py -->
…
<!-- @GENERATED:END chrome -->
```

```bash
python3 _build/build.py                 # bangun ulang 10 halaman di tempat
python3 _build/build.py --only berita.html
python3 _build/build.py --check         # exit 1 kalau halaman menyimpang — jalankan sebelum commit
python3 _build/build.py --report        # gerbang mutu (lihat di bawah)
python3 _build/build.py imgsizes        # width/height intrinsik semua <img> (butuh Pillow)
python3 _build/split_data.py            # pecah data.js -> data.js + data-full.js
python3 _build/bootstrap_markers.py     # SEKALI SAJA: tanam marker ke halaman baru
```

`_build/nav.py` adalah **satu-satunya sumber daftar menu**. Menambah atau
mengubah halaman cukup di sana; `class="active"` dan `aria-current="page"`
dihitung otomatis dari nama file, jadi tidak ada lagi penanda yang dikelola
tangan.

Halaman baru: salin salah satu halaman, jalankan `bootstrap_markers.py`, lalu
`build.py`. Jangan mengedit daerah di antara marker secara manual — perubahannya
akan tertimpa pada build berikutnya (`--check` akan menolaknya).

### Gerbang mutu `--report`

Dibuat karena kegagalan masa lalu situs ini diam-diam, bukan keras: CSS dan JS
pernah ditulis untuk markup yang berbeda sehingga fitur tampil tanpa gaya tanpa
error apa pun, dan sebuah intro tanpa controller mengunci gulir seluruh halaman.
Laporan memeriksa kelas terpakai-vs-terdefinisi dua arah, jumlah inline style,
`<img>` tanpa ukuran, `h1` ganda, integritas `data.js`, dan apakah seluruh
referensi aset benar-benar ada.

## Aset lokal (±69 MB)

- `assets/img/` — 773 berkas: sampul 300 berita, 225 foto isi artikel, 35 sampul
  YouTube, 48 galeri, 20 halaman dokumen pengumuman, 8 e-mading, foto
  jurusan/ekskul/fasilitas, logo. Sekitar 165 berkas tidak dirujuk (dibiarkan).
- `assets/video/` — 4 video kegiatan (MP4 lokal, diputar langsung di artikel)
- `assets/js/data.js` — 300 artikel ringkas, 89 guru, 25 karyawan, 52 MoU,
  17 ekskul, misi/tujuan (±178 KB)
- `assets/js/data-full.js` — 290 badan artikel lengkap (±1,03 MB);
  **hanya dimuat `berita.html`**

## Butuh masukan sekolah

Ditemukan saat perombakan, sengaja tidak ditutupi dengan konten palsu:

- **Foto ekstrakurikuler bolong**: SEPAK BOLA dan BAHASA ASING tidak punya foto
  di `assets/img/`. Keduanya kini ditampilkan sebagai ubin bernomor yang memang
  dirancang, bukan gambar salah. Dulu `SEPAK BOLA` dipasangi foto futsal.
- **8 dari 300 artikel tidak punya teks isi** (`FULL`), jadi reader hanya
  menampilkan ringkasan.
- **1 judul artikel kembar** (`TTD Elektronik Lembar Pengesahan`, 3x) — reader
  membuka yang pertama cocok.
- Video profil jurusan masih menempel ke kanal YouTube resmi sekolah (sampulnya
  lokal). Kalau sekolah punya MP4 sendiri, daftarkan di `VIDEOS` pada `data.js`
  — pemutar otomatis memakai berkas lokal.
- Penamaan: berkas `ppdb.html` dipertahankan (tautan luar mungkin sudah menyebar)
  tetapi label navigasi dan seluruh teks memakai **SPMB**.

## Kredit

Konten, foto, video, dan dokumentasi: **SMK Negeri 8 Jember** (Humas Eskalaber) ·
Instagram @smkn8_official. Site statis tanpa database & tanpa framework — siap
deploy ke hosting mana pun.
