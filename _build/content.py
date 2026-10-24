"""content.py — satu sumber kebenaran untuk seluruh isi situs.

Data artikel/guru/mitra dibaca dari assets/js/data.js (sudah tervalidasi).
Prosa khas tiap halaman ditaruh di sini sebagai struktur Python, bukan
tersebar di 10 file HTML. Template tidak pernah menulis teks sendiri.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "assets" / "js"

SCHOOL = {
    "name": "SMK Negeri 8 Jember",
    "name_short": "SMKN 8 Jember",
    "nick": "Eskalaber",
    "tagline": "Bisa & Hebat",
    "kind": "Sekolah Agro Industri",
    "status": "SMK Pusat Keunggulan · BLUD",
    "npsn": "20554690",
    "address": "Jl. Pelita No. 27, Sidomekar, Semboro, Jember, Jawa Timur 68157",
    "region": "Semboro, Jember",
    "phone": "0336-444112",
    "email": "smknegeri08jember@gmail.com",
    "lsp_email": "lspp1.smkn8jember@gmail.com",
    "instagram": "https://www.instagram.com/smkn8_official/",
    "instagram_handle": "@smkn8_official",
    "instagram_followers": "5,1K+ pengikut",
    "instagram_posts": "1.317 postingan",
    "youtube": "https://youtu.be/clMb3qcuWjQ",
    "tour": "https://app.lapentor.com/sphere/smkn-8-jember",
    "maps": "https://www.google.com/maps?q=SMK+Negeri+8+Jember&output=embed",
    "hours": "Senin–Jumat · 07.00–15.30 WIB",
    "head": "Hj. Rahmah Hidana, S.Pd., M.Si.",
    "head_role": "Kepala SMK Negeri 8 Jember",
    "founded": 2008,
}

# Statistik kartu metrik di beranda: (nilai, label, ikon, rona)
# rona "gold" hanya untuk satu kartu — kuning logo dipakai secukupnya.
HEADLINE_STATS = [
    ("1.712", "Peserta didik aktif · TP 2023/2024", "users", ""),
    ("7", "Konsentrasi keahlian", "book", ""),
    ("114", "Guru & tenaga kependidikan", "shield", ""),
    ("16", "Rombel SPMB 2026", "trophy", "gold"),
]

# ------------------------------------------------------------------ programs
# cluster: dipakai untuk penanda warna (lihat style.css --cluster-*)
PROGRAMS = [
    {
        "id": "dkv", "no": "01", "short": "DKV",
        "name": "Desain Komunikasi Visual",
        "cluster": "informatika", "cluster_label": "Komputer & Informatika",
        "rombel": 2, "img": "assets/img/IMG_2217-1536x862.webp",
        "video": "0V-NWXMqA7U",
        "desc": "Program keahlian DKV membentuk kreator visual yang menguasai seni rupa, desain grafis, fotografi, videografi, dan animasi. Gedung SMK Pusat Keunggulan DKV diresmikan 2024, didukung guru tamu JTV Jember, Jatim Times, serta magang industri di PT Indo Bismar dan percetakan Mulya Citra Grafika.",
        "prospects": ["Desainer grafis", "Fotografer & videografer", "Content creator", "Animator & illustrator"],
        "marks": ["Juara EPIM-TI 2025", "Gedung SMK PK 2024", "TeFa percetakan"],
    },
    {
        "id": "rpl", "no": "02", "short": "RPL",
        "name": "Rekayasa Perangkat Lunak",
        "cluster": "informatika", "cluster_label": "Komputer & Informatika",
        "rombel": 2, "img": "assets/img/RPL-1.webp",
        "video": "ZTmp69uUaC0",
        "desc": "RPL mempelajari seluruh cara pengembangan perangkat lunak: pembuatan, pemeliharaan, hingga manajemen mutu. Siswa mengikuti kelas industri bersama PT Humma Teknologi Indonesia dan konsisten menorehkan juara kompetisi web design & essay nasional.",
        "prospects": ["Web & mobile programmer", "Database programmer", "Game developer", "Software tester / IT support"],
        "marks": ["Juara 1 NECPE 2025", "Kelas industri Humma", "Juara web design"],
    },
    {
        "id": "tkj", "no": "03", "short": "TKJ",
        "name": "Teknik Komputer & Jaringan",
        "cluster": "informatika", "cluster_label": "Komputer & Informatika",
        "rombel": 2, "img": "assets/img/TKJ-1.webp",
        "video": "7KSfPCwF1k0",
        "desc": "TKJ menekankan keterampilan perakitan komputer, instalasi jaringan lokal hingga luas, dan administrasi server. Lulusan siap menjadi teknisi jaringan di perusahaan, instansi, maupun penyedia layanan internet.",
        "prospects": ["Network technician", "System administrator", "IT support & technical service", "Technopreneur"],
        "marks": ["Lab jaringan lengkap", "Sertifikasi kompetensi", "Projek teaching factory"],
    },
    {
        "id": "tkr", "no": "04", "short": "TKR",
        "name": "Teknik Kendaraan Ringan",
        "cluster": "otomotif", "cluster_label": "Teknik Otomotif",
        "rombel": 3, "img": "assets/img/TKR1-scaled.webp",
        "video": "4_YcgaZIXu0",
        "desc": "TKR membekali peserta didik ilmu perawatan & perbaikan mesin, sistem pemindah tenaga, chasis-suspensi, dan kelistrikan mobil sesuai standar pabrikan. Sekolah bermitra dengan Daihatsu (program PINTAR) untuk kurikulum, training dojo, hingga rekrutmen lulusan.",
        "prospects": ["Mekanik & service advisor", "Teknisi bengkel resmi", "Wirausahawan otomotif", "Inspektor kendaraan"],
        "marks": ["Mitra Daihatsu PINTAR", "Bengkel teaching factory", "Predikat B PINTAR Daihatsu"],
    },
    {
        "id": "tsm", "no": "05", "short": "TSM",
        "name": "Teknik Sepeda Motor",
        "cluster": "otomotif", "cluster_label": "Teknik Otomotif",
        "rombel": 3, "img": "assets/img/TSM-1.webp",
        "video": "mqffAsi5k4w",
        "desc": "TSM menekankan keterampilan jasa mekanik kendaraan roda dua dengan kurikulum tersinkron Yamaha. Alumni 2025 lolos Yamaha Engineering School batch 2025 dan kuliah di Yuan Ze University, Taiwan.",
        "prospects": ["Mekanik sepeda motor", "Teknisi perakitan industri", "Wirausahawan bengkel", "Service partner Yamaha"],
        "marks": ["Kurikulum Yamaha", "Yamaha Engineering School", "Alumni kuliah Taiwan"],
    },
    {
        "id": "atph", "no": "06", "short": "ATPH",
        "name": "Agribisnis Tanaman Pangan & Hortikultura",
        "cluster": "agribisnis", "cluster_label": "Teknologi Pertanian",
        "rombel": 2, "img": "assets/img/APH-1-1536x1021.webp",
        "video": "Ih0WPvyonOc",
        "desc": "ATPH menghasilkan lulusan agribisnis yang profesional dan berjiwa wirausaha, dengan fasilitas greenhouse tanaman hias, hidroponik sayur, anggrek, pembibitan buah, rumah kompos, serta lab hama & penyakit. Jurusan ini menjadi tuan rumah pelatihan pertanian perkotaan BIOTROP–IPB–SEAMEO.",
        "prospects": ["Agripreneur", "Teknisi budidaya & greenhouse", "Supervisor agribisnis", "Konsultan pertanian"],
        "marks": ["Juara 1 API 2025", "Tuan rumah BIOTROP/IPB", "Panen raya edamame"],
    },
    {
        "id": "apt", "no": "07", "short": "APT",
        "name": "Agribisnis Perbenihan Tanaman",
        "cluster": "agribisnis", "cluster_label": "Teknologi Pertanian",
        "rombel": 2, "img": "assets/img/PPT-1-1536x1021.webp",
        "video": "EohF00JrLeQ",
        "desc": "APT fokus pada proses perbenihan — tahap awal dan krusial budidaya tanaman — termasuk produksi benih, pemuliaan, dan perbanyakan tanaman via kultur jaringan, teknik perbanyakan paling modern di industri agribisnis.",
        "prospects": ["Teknisi industri benih", "Analis laboratorium mutu benih", "Pemulia tanaman muda", "Wirausaha perbenihan"],
        "marks": ["Lab kultur jaringan", "Beasiswa Petani Muda", "Uji mutu benih"],
    },
]

CLUSTERS = {
    "informatika": {"label": "Komputer & Informatika", "ids": ["dkv", "rpl", "tkj"], "rombel": 6},
    "otomotif": {"label": "Teknik Otomotif", "ids": ["tkr", "tsm"], "rombel": 6},
    "agribisnis": {"label": "Teknologi Pertanian", "ids": ["atph", "apt"], "rombel": 4},
}

# ------------------------------------------------------------------- indexes
HERO = {
    "badge": "SMK Pusat Keunggulan · Semboro, Jember",
    "title_top": "Sekolah agro industri",
    "title_accent": "yang mencetak juara",
    "lead": "SMK Negeri 8 Jember menyiapkan lulusan yang siap kerja, siap berwirausaha, dan siap melanjutkan pendidikan — melalui 7 konsentrasi keahlian, teaching factory, dan kemitraan industri nyata.",
    "points": ["Terakreditasi & BLUD", "Teaching Factory", "Juara LKS Provinsi", "17+ Ekstrakurikuler"],
    # Panggung hero: satu foto utama + dua pendamping, dengan capaian nyata di bawahnya
    "photo": "assets/img/lobi.webp",
    "photo_alt": "Lobi SMK Negeri 8 Jember",
    "live": "Kampus Semboro — lahan, bengkel, dan lab sendiri",
    "crest": "SMK Pusat Keunggulan",
    "kicker": "Capaian 2025",
    "note": "Juara 3 LKS Dikmen Provinsi Jawa Timur",
    "note_text": "Ditutup Best Completer Finisher Award pada SEASO Science Olympiad di Penang, Malaysia.",
    "note_foot": "Papan prestasi",
    "note_href": "kegiatan.html#prestasi-grid",
    "thumbs": [
        ("assets/img/TKR1-scaled.webp", "Praktik kendaraan di bengkel TKR", 1000, 667),
        ("assets/img/APH-1-1536x1021.webp", "Lahan praktik agribisnis ATPH", 1400, 931),
    ],
    "float_value": "1.712",
    "float_label": "Peserta didik aktif",
}

WELCOME = {
    "eyebrow": "Kata Sambutan",
    "title": "Selamat datang di rumah digital Eskalaber",
    "quote": "Website merupakan salah satu wujud kemajuan teknologi yang memudahkan masyarakat mendapatkan informasi. Semoga isi dan berita di dalamnya dapat diketahui masyarakat luas dan bisa diambil manfaat darinya.",
    "body": "Situs resmi ini merangkum profil, sejarah, data guru & siswa, tujuh konsentrasi keahlian, hingga ratusan berita kegiatan sekolah — seluruh foto, video, dan artikel tersimpan lokal di server sekolah.",
    "photo": "assets/img/BU-RAHMAH-BARU-EDIT.webp",
}

BENTO = [
    {"kind": "dark", "kicker": "Pusat Keunggulan", "big": "PK", "title": "SMK Pusat Keunggulan", "body": "Ditetapkan 2023, dengan gedung dan peralatan baru untuk DKV serta teaching factory.", "span": 1},
    {"kind": "photo", "img": "assets/img/TKR1-scaled.webp", "kicker": "Teaching Factory", "title": "Bengkel yang bekerja seperti industri", "body": "Siswa melayani kendaraan nyata dengan standar pabrikan, dibimbing instruktur bersertifikat.", "span": 2},
    {"kind": "sun", "kicker": "Kampus", "title": "Kampus Agro", "body": "Greenhouse, kultur jaringan, dan lahan praktik di atas tanah sendiri.", "span": 1},
    {"kind": "plain", "kicker": "Kemitraan", "title": "52 MoU dengan industri", "body": "Daihatsu, Yamaha, PT Humma, dan puluhan mitra lain.", "span": 1},
    {"kind": "plain", "kicker": "Global", "title": "Go Global", "body": "Alumni menembus Yamaha Engineering School dan kampus Taiwan.", "span": 1},
    {"kind": "plain", "kicker": "Wadah", "title": "17 Ekstrakurikuler & E-Mading", "body": "Dari Paskibra sampai hadrah, plus majalah digital karya siswa.", "span": 1},
]

# ------------------------------------------------------------------- profil
PROFIL = {
    "hero": {
        "crumb": "Profil",
        "title": "Profil SMK Negeri 8 Jember",
        "lead": "Sejarah, visi-misi, tujuan, struktur organisasi, sarana prasarana, LSP P-1, kemitraan, serta data guru dan tenaga kependidikan Eskalaber.",
    },
    "about": {
        "eyebrow": "Tentang Kami",
        "title": "SMK negeri paling selatan di Kabupaten Jember",
        "body": "SMKN 8 Jember adalah Sekolah Menengah Kejuruan yang terletak di Kecamatan Semboro, Kabupaten Jember. Berdiri sejak tahun 2008, kini memiliki 7 kompetensi keahlian yang terbagi atas 3 program keahlian: Teknik Otomotif (TBSM & TKR), Teknik Komputer dan Informatika (TKJ, RPL, DKV), serta Teknologi Pertanian (ATPH & APT).",
        "points": [
            ("Siap kerja", "kurikulum tersinkron industri & teaching factory"),
            ("Siap wirausaha", "kelas wirausaha dan unit produksi sekolah"),
            ("Siap kuliah", "20+ lulusan lolos SNBP/SNBT & beasiswa luar negeri"),
        ],
    },
    "timeline": [
        ("2008", "Berdiri sebagai SMKN 1 Semboro", "Berdasarkan surat rekomendasi Kepala Dinas Pendidikan Kab. Jember No. 421.3/3342/436.316/2008 tanggal 25 Agustus 2008; kepala sekolah pertama Drs. Suprayitno."),
        ("2008/2009", "KBM pertama di SMPN 4 Tanggul", "Kegiatan belajar mengajar tahun pertama bertempat di gedung barat SMP Negeri 4 Tanggul, Kecamatan Semboro, diampu sebagian besar guru SMPN 4 Tanggul."),
        ("2009/2010", "Pindah ke kampus Jl. Pelita No. 27", "Menempati gedung unit sekolah baru di Desa Sidomekar: 5 ruang kelas, bengkel Teknik Otomotif, praktik TIK, dan Agribisnis Produksi Tanaman."),
        ("2015", "LSP P-1 didirikan", "Lembaga Sertifikasi Profesi P-1 sekolah berdiri 2 Januari 2015 sebagai lembaga independen penguji kompetensi siswa."),
        ("2023–2024", "SMK Pusat Keunggulan", "Pembangunan gedung pusat keunggulan dan penandatanganan prasasti program keahlian Desain Komunikasi Visual (Feb 2024)."),
        ("2025", "HUT ke-17 & prestasi internasional", "Juara 3 LKS Dikmen Provinsi Jawa Timur dan Best Completer Finisher Award SEASO Science Olympiad di Penang, Malaysia."),
        ("2026", "16 rombel & 576 kursi", "SPMB 2026 membuka 16 rombel untuk 7 konsentrasi keahlian, dengan tiga jalur seleksi."),
    ],
    "vision": "Terwujudnya lulusan yang berprofil Pelajar Pancasila sehingga mampu bersaing di dunia kerja dan perguruan tinggi, serta tumbuh jiwa wirausaha.",
    "sarpras": [
        ("Gedung Pusat Keunggulan", "Diresmikan 2024 untuk DKV, dengan studio foto, ruang editing, dan peralatan produksi.", "assets/img/IMG_2217-1536x862.webp"),
        ("Bengkel Otomotif", "Training dojo bermitra Daihatsu dan Yamaha untuk praktik kendaraan nyata.", "assets/img/TKR1-scaled.webp"),
        ("Kampus Agro", "Greenhouse, hidroponik, kultur jaringan, rumah kompos, dan lahan praktik sendiri.", "assets/img/APH-1-1536x1021.webp"),
    ],
    "students": [
        ("Kelas X", "578"), ("Kelas XI", "555"), ("Kelas XII", "529"), ("Kelas XIII", "50"),
    ],
    "students_total": "1.712",
    "students_year": "TP 2023/2024",
}

# ---------------------------------------------------------------------- SPMB
SPMB = {
    "hero": {
        "crumb": "SPMB",
        "title": "SPMB 2026 — Penerimaan Murid Baru",
        "lead": "Kuota 16 rombel × 36 murid pada 7 konsentrasi keahlian. Simak jalur, tahapan, dan pengumuman hasilnya — semua tersimpan di situs ini.",
    },
    "quota_note": "Jumlah murid per kelas/rombel adalah 36 murid, tersebar pada tujuh konsentrasi keahlian berikut.",
    "quota": [
        ("Teknik Kendaraan Ringan", 3, 108),
        ("Teknik Sepeda Motor", 3, 108),
        ("Rekayasa Perangkat Lunak", 2, 72),
        ("Teknik Komputer dan Jaringan", 2, 72),
        ("Desain Komunikasi Visual", 2, 72),
        ("Agribisnis Tanaman Pangan & Hortikultura", 2, 72),
        ("Agribisnis Perbenihan Tanaman", 2, 72),
    ],
    "quota_total": (16, 576),
    "steps": [
        ("Tahap 1", "Pendaftaran", "Melalui portal SPMB Jawa Timur / panitia sekolah dengan melengkapi berkas rapor, kartu keluarga, dan dokumen pendukung."),
        ("Tahap 2", "Seleksi jalur", "Jalur afirmasi (termasuk prioritas terdekat), jalur nilai rapor + TKA, serta jalur prestasi akademik & non-akademik."),
        ("Tahap 3", "Pengumuman", "Hasil tiap jalur dipublikasikan resmi — dokumen pengumuman tersimpan di halaman Pengumuman."),
        ("Tahap 4", "Daftar ulang & MPLS", "Calon murid yang diterima melakukan daftar ulang lalu mengikuti Masa Pengenalan Lingkungan Sekolah."),
    ],
    "docs": [
        ("Hasil SPMB jalur afirmasi", "Dokumen 7 halaman tersimpan lokal", "pengumuman.html#afirmasi"),
        ("Hasil SPMB jalur nilai rapor + TKA", "Dokumen 13 halaman tersimpan lokal", "pengumuman.html#rapor"),
        ("Survei kepuasan pelanggan", "Form siswa, orang tua, DuDi, dan internal GTK", "kontak.html#survei"),
        ("Panitia PPDB", "smknegeri08jember@gmail.com · 0336-444112", "kontak.html"),
    ],
    "faq": [
        ("Apakah SMKN 8 Jember negeri & bebas biaya?", "Ya — SMKN 8 Jember adalah sekolah negeri (BLUD) sehingga mengikuti ketentuan biaya pendidikan sekolah negeri yang berlaku."),
        ("Jurusan apa yang paling banyak peminatnya?", "Seluruh jurusan memiliki peminat tersendiri; otomotif (TKR & TSM) membuka rombel terbanyak (masing-masing 3), sementara jurusan komputer & pertanian terus tumbuh berkat kemitraan industri."),
        ("Apakah ada kesempatan beasiswa & kuliah?", "Sangat ada: setiap tahun 20+ lulusan lolos SNBP/SNBT, serta program beasiswa Smart Scholarship YBM BRILiaN, Chinese Government Scholarship, Petani Muda, hingga kuliah ke Taiwan dan Malaysia."),
        ("Bagaimana menghubungi panitia PPDB?", "Melalui halaman Kontak, email smknegeri08jember@gmail.com, atau telepon 0336-444112 pada jam layanan Senin–Jumat 07.00–15.30 WIB."),
    ],
}

# --------------------------------------------------------------------- pages
PAGES = {
    "index": {"title": "SMKN 8 Jember — Bisa dan Hebat | Sekolah Agro Industri Semboro",
              "desc": "Website resmi SMK Negeri 8 Jember: 7 konsentrasi keahlian, berita, galeri, SPMB, dan profil sekolah agro industri di Semboro, Jember."},
    "profil": {"title": "Profil Sekolah — SMKN 8 Jember",
               "desc": "Sejarah, visi-misi, tujuan, struktur organisasi, sarana prasarana, LSP P-1, kemitraan, data guru dan tenaga kependidikan SMKN 8 Jember."},
    "jurusan": {"title": "Konsentrasi Keahlian — SMKN 8 Jember",
                "desc": "Tujuh konsentrasi keahlian SMKN 8 Jember: DKV, RPL, TKJ, TKR, TSM, ATPH, dan APT beserta prospek lulusan."},
    "berita": {"title": "Berita & Artikel — SMKN 8 Jember",
               "desc": "Arsip 300 artikel kegiatan, prestasi, dan pengumuman SMKN 8 Jember dengan foto dan video lokal."},
    "galeri": {"title": "Galeri — SMKN 8 Jember",
               "desc": "48 foto kurasi kegiatan, ekstrakurikuler, jurusan, prestasi, dan fasilitas SMKN 8 Jember."},
    "kegiatan": {"title": "Kegiatan, Ekstrakurikuler & Prestasi — SMKN 8 Jember",
                 "desc": "17 ekstrakurikuler dan papan prestasi SMKN 8 Jember dari tingkat kabupaten hingga internasional."},
    "ppdb": {"title": "SPMB 2026 — SMKN 8 Jember",
             "desc": "Kuota 16 rombel 576 kursi, alur pendaftaran, jalur seleksi, dan FAQ SPMB SMKN 8 Jember 2026."},
    "pengumuman": {"title": "Pengumuman Resmi SPMB 2026 — SMKN 8 Jember",
                   "desc": "Dokumen resmi hasil SPMB: jalur afirmasi dan jalur nilai rapor + TKA, tersimpan lokal."},
    "e-mading": {"title": "E-Mading — SMKN 8 Jember",
                 "desc": "Delapan edisi E-Mading digital karya siswa SMKN 8 Jember."},
    "kontak": {"title": "Kontak — SMKN 8 Jember",
               "desc": "Alamat, email, telepon, LSP, Instagram, peta, formulir pesan, dan lima survei kepuasan SMKN 8 Jember."},
}

NAV = [
    ("index.html", "Beranda"),
    ("profil.html", "Profil"),
    ("jurusan.html", "Jurusan"),
    ("berita.html", "Berita"),
    ("galeri.html", "Galeri"),
    ("kegiatan.html", "Kegiatan"),
    ("ppdb.html", "SPMB"),
    ("pengumuman.html", "Pengumuman"),
    ("e-mading.html", "E-Mading"),
    ("kontak.html", "Kontak"),
]

# --------------------------------------------------------------- data.js load
def load_data() -> dict:
    raw = (JS / "data.js").read_text(encoding="utf-8")
    payload = raw.split("=", 1)[1].strip().rstrip(";")
    return json.loads(payload)


def page_meta(stem: str) -> dict:
    return PAGES[stem]


def nav_for(stem: str) -> list[tuple[str, str, bool]]:
    return [(href, label, href == f"{stem}.html") for href, label in NAV]
