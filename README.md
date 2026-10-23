# Website Resmi Mandiri — SMK Negeri 8 Jember "Eskalaber"

Website ini **100% mandiri**: tidak ada satu pun tautan ke website lama.
Seluruh artikel, foto, video, dokumen pengumuman, dan data tersimpan lokal di folder ini.
Sumber konten: dokumentasi & data resmi sekolah (dipindahkan menyeluruh), Instagram @smkn8_official.

## Cara membuka
Buka `index.html` di browser, atau:
```bash
python3 -m http.server 8080   # lalu buka http://localhost:8080
```

## 10 Halaman
| File | Isi |
|---|---|
| `index.html` | Beranda: hero, ticker berita, statistik animasi, sambutan kepsek, 7 jurusan, bento keunggulan, berita terbaru, kemitraan, CTA SPMB |
| `profil.html` | Tentang, linimasa sejarah 2008–2026, visi–misi–tujuan lengkap, sambutan penuh, struktur organisasi, sarpras, data siswa, LSP P-1, tabel 52 mitra MoU, tabel 89 guru + 25 karyawan (pencarian live) |
| `jurusan.html` | 7 konsentrasi keahlian + prospek lulusan + tombol **video profil jurusan** |
| `berita.html` | Arsip **300 artikel lengkap** (teks penuh + foto + video lokal): filter kategori, pencarian, paginasi, reader modal |
| `galeri.html` | 48 foto kurasi: masonry, filter, lightbox |
| `kegiatan.html` | 17 ekskul, papan prestasi 2024–2026, prestasi periode sebelumnya |
| `ppdb.html` | SPMB 2026: kuota 16 rombel (576 kursi), alur, FAQ, tautan dokumen hasil |
| `pengumuman.html` | Dokumen resmi hasil SPMB tersimpan lokal: jalur afirmasi (7 hal.) & jalur nilai rapor+TKA (13 hal.), layar penuh per halaman |
| `e-mading.html` | Kompilasi 8 edisi E-Mading digital karya siswa, layar penuh |
| `kontak.html` | Alamat, email, telepon, LSP, Instagram, peta, formulir pesan, **5 form survei kepuasan** (Google Form resmi sekolah) |

## Aset lokal (±69 MB)
- `assets/img/` — 773 file: sampul 300 berita, 225 foto isi artikel, 35 sampul YouTube, 48 galeri, 20 halaman dokumen pengumuman, 8 e-mading, foto jurusan/ekskul/fasilitas, logo, placeholder branded
- `assets/video/` — 4 video kegiatan sekolah (MP4 lokal, diputar langsung di artikel)
- `assets/js/data.js` — 300 artikel teks penuh, 89 guru, 25 karyawan, 52 MoU, 17 ekskul, misi/tujuan, form survei
- Video profil jurusan & video berita lain: sampul lokal + pemutar embed kanal YouTube resmi sekolah (klik untuk putar). Jika sekolah menaruh file MP4 sendiri, daftarkan di `VIDEOS` pada `data.js` — pemutar otomatis memakai file lokal.

## Fitur interaktif
Ticker berita · filter & pencarian berita · paginasi · reader artikel penuh · pemutar video bersampul YouTube · video lokal · lightbox foto & dokumen · modal video jurusan · tabel pencarian guru · accordion FAQ · counter animasi · scroll reveal · responsif penuh.

## Kredit
Konten, foto, video, dan dokumentasi: **SMK Negeri 8 Jember** (Humas Eskalaber) · Instagram @smkn8_official.
Site statis tanpa database & tanpa framework — siap deploy ke hosting mana pun.
