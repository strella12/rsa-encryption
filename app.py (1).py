#!/usr/bin/env python
# coding: utf-8

# In[14]:


#%%writefile app.py
import html
import streamlit as st
# =====================================================
# 1. KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="RSA: Enkripsi & Dekripsi",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LEBAR_KODE = 3
KODE_MAKS = 255
BATAS_PRIMA = 10000
# =====================================================
# 2. TAMPILAN (CSS)
# =====================================================
# Palet warna:
#   teal tua   #0B4A4A  latar hero
#   teal       #0E7C7B  warna utama (tombol, slider, angka)
#   mint       #E3F3F1  latar kunci publik
#   kuning     #F5B83D  penanda langkah dan kunci privat
#   tinta      #10302F  teks utama
# Font:
#   Bricolage Grotesque untuk judul dan angka
#   Figtree untuk teks biasa
#   JetBrains Mono untuk angka kunci dan ciphertext

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

:root {
    --tinta: #10302F;
    --redup: #4B6A68;
    --teal: #0E7C7B;
    --teal-gelap: #0A5F5E;
    --teal-tua: #0B4A4A;
    --mint: #E3F3F1;
    --garis: #BFD9D6;
    --latar: #F2F8F7;
    --kuning: #F5B83D;
    --kuning-muda: #FFF1CF;
    --font-judul: 'Bricolage Grotesque', 'Trebuchet MS', sans-serif;
    --font-isi: 'Figtree', 'Segoe UI', sans-serif;
    --font-kode: 'JetBrains Mono', Consolas, monospace;
}

/* ---------- Dasar halaman ---------- */
.stApp {
    background: var(--latar);
    color: var(--tinta);
    font-family: var(--font-isi);
}
.stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp button {
    font-family: var(--font-isi);
}
.block-container {
    max-width: 1040px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppDeployButton"] { display: none; }
[data-testid="InputInstructions"] { display: none; }

/* ---------- Hero ---------- */
.hero {
    background: var(--teal-tua);
    border-radius: 26px;
    padding: 2.3rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero-teks { flex: 1 1 auto; max-width: 29rem; }
.hero-judul {
    font-family: var(--font-judul);
    font-weight: 700;
    font-size: 2.7rem;
    line-height: 1.08;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    margin-bottom: 0.9rem;
}
.hero-ket {
    color: #CFE8E6;
    font-size: 1.05rem;
    line-height: 1.6;
    margin: 0;
}
.hero-prima {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    align-items: baseline;
    gap: 0.3rem 1rem;
    max-width: 25rem;
    font-family: var(--font-judul);
    font-weight: 700;
    line-height: 1;
    color: #1E7F7C;
    user-select: none;
}
.hero-prima .s { font-size: 1.4rem; }
.hero-prima .m { font-size: 2.2rem; }
.hero-prima .l { font-size: 3.4rem; }
.hero-prima .sorot { color: var(--kuning); }

/* ---------- Navigasi (radio dibuat seperti tombol pil) ---------- */
div[role="radiogroup"] { gap: 0.6rem; margin-bottom: 0.4rem; }
div[role="radiogroup"] > label {
    background: #FFFFFF;
    border: 1.5px solid var(--garis);
    border-radius: 999px;
    padding: 0.4rem 1.5rem;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
}
div[role="radiogroup"] > label > div:first-child { display: none; }
div[role="radiogroup"] > label p {
    font-weight: 600;
    color: var(--teal-gelap);
}
div[role="radiogroup"] > label:hover { border-color: var(--teal); }
div[role="radiogroup"] > label:has(input:checked) {
    background: var(--teal);
    border-color: var(--teal);
}
div[role="radiogroup"] > label:has(input:checked) p { color: #FFFFFF; }

/* ---------- Kotak langkah ---------- */
div[class*="st-key-kotak"] {
    background: #FFFFFF;
    border: 1.5px solid var(--garis);
    border-radius: 18px;
    padding: 1.4rem 1.6rem 1.5rem;
}
.langkah {
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    margin-bottom: 0.6rem;
}
.nomor {
    flex: 0 0 2.2rem;
    height: 2.2rem;
    border-radius: 50%;
    background: var(--kuning);
    color: var(--tinta);
    font-family: var(--font-judul);
    font-weight: 700;
    font-size: 1.05rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
.langkah-judul {
    font-family: var(--font-judul);
    font-weight: 700;
    font-size: 1.3rem;
    line-height: 1.2;
    color: var(--tinta);
}
.langkah-ket {
    color: var(--redup);
    font-size: 0.95rem;
    margin-top: 0.2rem;
}
.angka-besar {
    font-family: var(--font-judul);
    font-weight: 700;
    font-size: 3.4rem;
    line-height: 1;
    color: var(--teal);
    margin: 0.3rem 0 0.7rem;
}
.angka-besar span {
    font-size: 1.4rem;
    font-weight: 500;
    color: var(--redup);
    margin-right: 0.6rem;
}
.catatan {
    color: var(--redup);
    font-size: 0.88rem;
    margin-top: 0.2rem;
}

/* ---------- Strip rumus n ---------- */
.rumus {
    background: var(--mint);
    border: 1.5px dashed #7FB8B4;
    border-radius: 14px;
    padding: 0.85rem 1.2rem;
    margin: 0.2rem 0;
    font-family: var(--font-judul);
    font-size: 1.2rem;
    color: var(--tinta);
}
.rumus b { color: var(--teal-gelap); font-size: 1.35rem; }

/* ---------- Slider ---------- */
[data-testid="stSlider"] div[role="slider"] {
    background: var(--teal) !important;
    border: 3px solid #FFFFFF !important;
    box-shadow: 0 0 0 2px var(--teal) !important;
    height: 1.5rem;
    width: 1.5rem;
}
[data-testid="stThumbValue"] {
    color: var(--teal-gelap) !important;
    font-family: var(--font-judul);
    font-weight: 700;
}
[data-testid="stTickBarMin"], [data-testid="stTickBarMax"] {
    color: var(--redup);
}

/* ---------- Input teks ---------- */
div[data-baseweb="textarea"], div[data-baseweb="input"] {
    border: 1.5px solid var(--garis) !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
}
div[data-baseweb="base-input"] { background: #FFFFFF !important; }
div[data-baseweb="textarea"]:focus-within, div[data-baseweb="input"]:focus-within {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(14, 124, 123, 0.18);
}
.stTextArea textarea, .stTextInput input {
    color: var(--tinta);
    font-size: 1rem;
}

/* ---------- Tombol ---------- */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
    transition: background 0.15s, border-color 0.15s;
}
.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] {
    background: var(--teal) !important;
    border: none !important;
    color: #FFFFFF !important;
}
.stButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
    background: var(--teal-gelap) !important;
}
.stDownloadButton > button, [data-testid="stBaseButton-secondary"] {
    background: #FFFFFF !important;
    color: var(--teal-gelap) !important;
    border: 1.5px solid var(--teal) !important;
}
.stDownloadButton > button:hover, [data-testid="stBaseButton-secondary"]:hover {
    background: var(--mint) !important;
}
button:focus-visible {
    outline: 3px solid var(--kuning) !important;
    outline-offset: 2px;
}

/* ---------- Pesan peringatan ---------- */
[data-testid="stAlert"] { border-radius: 12px; }

/* ---------- Blok kode (plaintext, ciphertext) ---------- */
[data-testid="stCode"] {
    border: 1.5px solid var(--garis);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stCode"] pre, [data-testid="stCode"] code {
    background: #F0F7F6 !important;
    color: var(--tinta) !important;
    font-family: var(--font-kode) !important;
    font-size: 0.9rem !important;
    white-space: pre-wrap !important;
    word-break: break-word;
}
.label {
    font-weight: 600;
    color: var(--tinta);
    margin: 1rem 0 0.35rem;
    font-size: 0.95rem;
}

/* ---------- Kartu kunci ---------- */
.kunci-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 0.8rem 0 0.4rem;
}
.kunci {
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    border: 1.5px solid;
}
.kunci.publik { background: var(--mint); border-color: #7FB8B4; }
.kunci.privat { background: var(--kuning-muda); border-color: #E3B04B; }
.kunci-judul {
    font-family: var(--font-judul);
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: 0.5rem;
}
.kunci-baris {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
    font-family: var(--font-kode);
    font-weight: 500;
    font-size: 1.2rem;
    margin: 0.2rem 0;
    word-break: break-all;
}
.kunci-baris span { color: var(--redup); min-width: 1.2rem; }
.kunci-ket {
    margin-top: 0.7rem;
    color: var(--redup);
    font-size: 0.9rem;
}

/* ---------- Kondisi kosong dan hasil dekripsi ---------- */
.kosong {
    border: 1.5px dashed var(--garis);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    text-align: center;
    color: var(--redup);
}
.hasil-teks {
    background: var(--mint);
    border: 1.5px solid #7FB8B4;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    font-size: 1.25rem;
    white-space: pre-wrap;
    word-break: break-word;
}
.footer-kecil {
    color: var(--redup);
    font-size: 0.85rem;
    margin-top: 2.2rem;
}

/* ---------- Layar kecil ---------- */
@media (max-width: 760px) {
    .hero { padding: 1.6rem; }
    .hero-judul { font-size: 2rem; }
    .hero-prima { display: none; }
    .kunci-grid { grid-template-columns: 1fr; }
    div[class*="st-key-kotak"] { padding: 1.1rem 1.1rem 1.2rem; }
}
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# =====================================================
# 3. KOMPONEN TAMPILAN
# =====================================================

PRIMA_HERO = [
    (2, "s"), (3, "m"), (5, "s"), (7, "l"), (11, "s"), (13, "m"),
    (17, "s"), (19, "m"), (23, "l"), (29, "s"), (31, "m"), (37, "s"),
    (41, "m"), (43, "s"), (47, "l sorot"), (53, "s"), (59, "m"),
    (61, "s"), (67, "m"), (71, "l sorot"),
]


def tampilkan_hero():
    angka_prima = "".join(
        f'<span class="{kelas}">{angka}</span>'
        for angka, kelas in PRIMA_HERO
    )
    st.markdown(
        '<div class="hero"><div class="hero-teks">'
        '<div class="hero-judul">Pesan rahasia dari dua bilangan prima</div>'
        '<p class="hero-ket">Aplikasi belajar enkripsi dan dekripsi RSA. '
        'Pilih p dan q, tulis pesanmu, lalu lihat bagaimana pesan itu '
        'berubah menjadi deretan angka yang hanya bisa dibuka dengan '
        'kunci privat.</p></div>'
        f'<div class="hero-prima" aria-hidden="true">{angka_prima}</div>'
        '</div>',
        unsafe_allow_html=True
    )


def kepala_langkah(nomor, judul, keterangan):
    st.markdown(
        f'<div class="langkah"><div class="nomor">{nomor}</div>'
        f'<div><div class="langkah-judul">{judul}</div>'
        f'<div class="langkah-ket">{keterangan}</div></div></div>',
        unsafe_allow_html=True
    )


def angka_besar(huruf, nilai):
    st.markdown(
        f'<div class="angka-besar"><span>{huruf} =</span>{nilai}</div>',
        unsafe_allow_html=True
    )


def label_kecil(teks):
    st.markdown(f'<div class="label">{teks}</div>', unsafe_allow_html=True)


# =====================================================
# 4. FUNGSI BILANGAN PRIMA
# =====================================================

def cek_prima(n):
    """Memeriksa apakah n merupakan bilangan prima."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    pembagi = 3
    while pembagi * pembagi <= n:
        if n % pembagi == 0:
            return False
        pembagi += 2

    return True


@st.cache_data
def daftar_prima(batas):
    """Membuat daftar semua bilangan prima dari 2 sampai batas."""
    return [angka for angka in range(2, batas + 1) if cek_prima(angka)]


DAFTAR_PRIMA = daftar_prima(BATAS_PRIMA)


# =====================================================
# 5. FUNGSI MATEMATIKA RSA
# =====================================================

def pbb(a, b):
    """Menghitung Faktor Persekutuan Terbesar."""
    while b != 0:
        a, b = b, a % b
    return a


def euclid_diperluas(a, b):
    """Menghasilkan g, x, y sehingga a*x + b*y = g."""
    if b == 0:
        return a, 1, 0

    g, x, y = euclid_diperluas(b, a % b)
    return g, y, x - (a // b) * y


def balikan_mod(e, m):
    """Menghitung invers modulo."""
    g, x, _ = euclid_diperluas(e, m)

    if g != 1:
        raise ValueError("Balikan modulo tidak ditemukan.")

    return x % m


def pangkat_mod(b, e, n):
    """Menghitung b^e mod n dengan square-and-multiply."""
    hasil = 1
    b %= n

    while e > 0:
        if e % 2 == 1:
            hasil = (hasil * b) % n
        b = (b * b) % n
        e //= 2

    return hasil


# =====================================================
# 6. PEMBANGKITAN KUNCI RSA
# =====================================================

def bangkitkan_kunci(p, q):
    """Membuat kunci publik dan privat dari p dan q."""
    if not cek_prima(p):
        raise ValueError("Nilai p harus bilangan prima.")

    if not cek_prima(q):
        raise ValueError("Nilai q harus bilangan prima.")

    if p == q:
        raise ValueError("Nilai p dan q harus berbeda.")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Gunakan e = 65537 jika memenuhi syarat.
    e = 65537

    # Untuk contoh prima kecil, pilih e lain jika 65537 tidak sesuai.
    if e >= phi or pbb(e, phi) != 1:
        e = 3
        while e < phi and pbb(e, phi) != 1:
            e += 2

    if e >= phi:
        raise ValueError("Tidak ditemukan nilai e yang sesuai.")

    d = balikan_mod(e, phi)

    kunci_publik = (e, n)
    kunci_privat = (d, n)

    return kunci_publik, kunci_privat


# =====================================================
# 7. KONVERSI TEKS DAN ENKRIPSI/DEKRIPSI
# =====================================================

def teks_ke_kode(teks):
    """
    Mengubah setiap karakter menjadi kode ASCII 0–255.
    Mendukung huruf besar/kecil, angka, spasi, dan simbol ASCII.
    """
    karakter_tidak_didukung = [
        karakter for karakter in teks
        if ord(karakter) > KODE_MAKS
    ]

    if karakter_tidak_didukung:
        raise ValueError(
            "Ada karakter di luar rentang ASCII 0–255. "
            "Untuk versi ini, emoji dan beberapa karakter Unicode "
            "belum didukung."
        )

    return [ord(karakter) for karakter in teks]


def kode_ke_teks(kode):
    """Mengubah daftar kode ASCII kembali menjadi teks."""
    if any(angka < 0 or angka > KODE_MAKS for angka in kode):
        raise ValueError("Hasil dekripsi mengandung kode di luar 0–255.")

    return "".join(chr(angka) for angka in kode)


def enkripsi(daftar_kode, kunci_publik):
    """Mengenkripsi setiap kode karakter dengan kunci publik."""
    e, n = kunci_publik

    if n <= KODE_MAKS:
        raise ValueError(
            "n harus lebih besar dari 255. Pilih p dan q yang lebih besar."
        )

    return [pangkat_mod(angka, e, n) for angka in daftar_kode]


def dekripsi(ciphertext, kunci_privat):
    """Mendekripsi setiap angka ciphertext dengan kunci privat."""
    d, n = kunci_privat
    return [pangkat_mod(angka, d, n) for angka in ciphertext]


def parse_ciphertext(teks_cipher):
    """Membaca ciphertext berupa angka yang dipisahkan koma atau spasi."""
    teks_cipher = teks_cipher.replace(",", " ")
    bagian = teks_cipher.split()

    if not bagian:
        raise ValueError("Ciphertext belum diisi.")

    try:
        angka = [int(item) for item in bagian]
    except ValueError:
        raise ValueError(
            "Ciphertext harus berupa angka yang dipisahkan koma atau spasi."
        )

    if any(item < 0 for item in angka):
        raise ValueError("Ciphertext tidak boleh berisi angka negatif.")

    return angka


# =====================================================
# 8. STATE UNTUK SLIDER PRIMA p DAN q
# =====================================================
# Nilai p dan q disimpan terpisah dari widget slider supaya
# tidak hilang saat pengguna berpindah ke halaman Dekripsi.

if "nilai_p" not in st.session_state:
    st.session_state["nilai_p"] = 47

if "nilai_q" not in st.session_state:
    st.session_state["nilai_q"] = 71


def simpan_p():
    st.session_state["nilai_p"] = st.session_state["slider_p"]


def simpan_q():
    st.session_state["nilai_q"] = st.session_state["slider_q"]


# =====================================================
# 9. KEPALA HALAMAN DAN NAVIGASI
# =====================================================

tampilkan_hero()

halaman = st.radio(
    "Pilih halaman",
    ["Enkripsi", "Dekripsi"],
    key="pilihan_halaman",
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")


# =====================================================
# 10. HALAMAN ENKRIPSI
# =====================================================

if halaman == "Enkripsi":

    # ---------- LANGKAH 1: PILIH p ----------
    with st.container(key="kotak_p"):
        kepala_langkah(
            1,
            "Pilih bilangan prima p",
            "Geser ke kanan untuk prima yang lebih besar, "
            "ke kiri untuk prima yang lebih kecil."
        )
        angka_besar("p", st.session_state["nilai_p"])

        p = st.select_slider(
            "Bilangan prima p",
            options=DAFTAR_PRIMA,
            value=st.session_state["nilai_p"],
            key="slider_p",
            on_change=simpan_p,
            label_visibility="collapsed"
        )

        st.markdown(
            f'<div class="catatan">Tersedia {len(DAFTAR_PRIMA)} bilangan '
            f'prima, dari {DAFTAR_PRIMA[0]} sampai {DAFTAR_PRIMA[-1]}.</div>',
            unsafe_allow_html=True
        )

    st.write("")

    # ---------- LANGKAH 2: PILIH q ----------
    with st.container(key="kotak_q"):
        kepala_langkah(
            2,
            "Pilih bilangan prima q",
            "Pilih prima yang berbeda dari p. Semakin besar p dan q, "
            "semakin sulit kuncinya ditebak."
        )
        angka_besar("q", st.session_state["nilai_q"])

        q = st.select_slider(
            "Bilangan prima q",
            options=DAFTAR_PRIMA,
            value=st.session_state["nilai_q"],
            key="slider_q",
            on_change=simpan_q,
            label_visibility="collapsed"
        )

        st.markdown(
            f'<div class="catatan">Tersedia {len(DAFTAR_PRIMA)} bilangan '
            f'prima, dari {DAFTAR_PRIMA[0]} sampai {DAFTAR_PRIMA[-1]}.</div>',
            unsafe_allow_html=True
        )

    st.write("")

    # Ringkasan nilai n dan peringatan langsung
    if p == q:
        st.warning("p dan q harus berbeda agar dapat membentuk kunci RSA.")
    else:
        st.markdown(
            f'<div class="rumus">n = p × q = {p} × {q} = '
            f'<b>{p * q}</b></div>',
            unsafe_allow_html=True
        )
        if p * q <= KODE_MAKS:
            st.warning(
                f"Nilai n masih terlalu kecil. n harus lebih besar dari "
                f"{KODE_MAKS}, jadi geser p atau q ke kanan."
            )

    st.write("")

    # ---------- LANGKAH 3: PLAINTEXT ----------
    with st.container(key="kotak_pesan"):
        kepala_langkah(
            3,
            "Tulis pesan yang ingin dienkripsi",
            "Boleh huruf besar, huruf kecil, angka, spasi, dan simbol "
            "dengan kode ASCII 0–255."
        )

        plaintext = st.text_area(
            "Pesan (plaintext)",
            value="HARI itu 123!",
            placeholder="Contoh: Hari ini 17 Agustus!",
            key="input_plaintext",
            label_visibility="collapsed"
        )

        proses = st.button(
            "Bangkitkan kunci dan enkripsi",
            type="primary"
        )

    if proses:

        st.session_state.pop("hasil_enkripsi", None)

        try:
            if plaintext == "":
                raise ValueError("Plaintext tidak boleh kosong.")

            kunci_publik, kunci_privat = bangkitkan_kunci(p, q)
            daftar_kode = teks_ke_kode(plaintext)

            ciphertext = enkripsi(daftar_kode, kunci_publik)

            st.session_state["hasil_enkripsi"] = {
                "p": p,
                "q": q,
                "e": kunci_publik[0],
                "n": kunci_publik[1],
                "d": kunci_privat[0],
                "plaintext": plaintext,
                "daftar_kode": daftar_kode,
                "ciphertext": ciphertext
            }

            # Simpan juga ciphertext agar mudah dipakai pada halaman dekripsi.
            st.session_state["ciphertext_untuk_dekripsi"] = ", ".join(
                str(angka) for angka in ciphertext
            )
            st.session_state["d_untuk_dekripsi"] = str(kunci_privat[0])
            st.session_state["n_untuk_dekripsi"] = str(kunci_privat[1])

            st.success(
                "Kunci berhasil dibangkitkan dan pesan berhasil dienkripsi."
            )

        except Exception as error:
            st.error(str(error))

    st.write("")

    # ---------- HASIL ----------
    if "hasil_enkripsi" in st.session_state:

        hasil = st.session_state["hasil_enkripsi"]

        with st.container(key="kotak_hasil"):
            st.markdown(
                '<div class="langkah-judul">Kunci RSA</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="kunci-grid">'
                '<div class="kunci publik">'
                '<div class="kunci-judul">Kunci publik</div>'
                f'<div class="kunci-baris"><span>e</span>{hasil["e"]}</div>'
                f'<div class="kunci-baris"><span>n</span>{hasil["n"]}</div>'
                '<div class="kunci-ket">Boleh dibagikan. '
                'Dipakai untuk mengenkripsi pesan.</div>'
                '</div>'
                '<div class="kunci privat">'
                '<div class="kunci-judul">Kunci privat</div>'
                f'<div class="kunci-baris"><span>d</span>{hasil["d"]}</div>'
                f'<div class="kunci-baris"><span>n</span>{hasil["n"]}</div>'
                '<div class="kunci-ket">Simpan sendiri, jangan dibagikan. '
                'Dipakai untuk mendekripsi pesan.</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

            st.write("")
            st.markdown(
                '<div class="langkah-judul">Rincian proses enkripsi</div>',
                unsafe_allow_html=True
            )

            with st.expander("Tahap 1 — Perhitungan kunci RSA", expanded=True):
                phi = (hasil["p"] - 1) * (hasil["q"] - 1)
                st.markdown("**Nilai awal**")
                st.code(
                    f"p = {hasil['p']}\n"
                    f"q = {hasil['q']}\n"
                    f"n = p × q = {hasil['p']} × {hasil['q']} = {hasil['n']}\n"
                    f"φ(n) = (p − 1)(q − 1) = {phi}",
                    language=None
                )
                st.markdown(
                    f"Nilai **e = {hasil['e']}** dipilih dengan syarat "
                    f"1 < e < φ(n) dan FPB(e, φ(n)) = 1."
                )
                st.markdown(
                    f"Kunci privat adalah invers modulo: "
                    f"**d = e⁻¹ mod φ(n) = {hasil['d']}**."
                )
                st.info(
                    f"Kunci publik: (e, n) = ({hasil['e']}, {hasil['n']})\n\n"
                    f"Kunci privat: (d, n) = ({hasil['d']}, {hasil['n']})"
                )

            with st.expander("Tahap 2 — Mengubah plaintext menjadi kode ASCII", expanded=True):
                st.markdown("Setiap karakter diubah menjadi angka menggunakan fungsi `ord()`. ")
                st.code(hasil["plaintext"], language=None)
                tabel_ascii = []
                for posisi, (karakter, kode) in enumerate(
                    zip(hasil["plaintext"], hasil["daftar_kode"]), start=1
                ):
                    nama = "[SPASI]" if karakter == " " else karakter
                    tabel_ascii.append({
                        "Posisi": posisi,
                        "Karakter": nama,
                        "Konversi": f"ord({nama})",
                        "Kode ASCII (m)": kode
                    })
                st.dataframe(tabel_ascii, use_container_width=True, hide_index=True)
                st.caption("Contoh: H = 72, A = 65, R = 82, I = 73, dan spasi = 32.")

            with st.expander("Tahap 3 — Pembagian blok", expanded=True):
                st.markdown(
                    "Pada implementasi ini, **satu karakter ditetapkan sebagai satu blok**. "
                    "Jadi setiap kode ASCII menjadi nilai m tersendiri dan "
                    "dienkripsi secara terpisah. Setiap blok harus memenuhi m < n."
                )
                tabel_blok = []
                for i, (karakter, kode) in enumerate(
                    zip(hasil["plaintext"], hasil["daftar_kode"]), start=1
                ):
                    nama = "[SPASI]" if karakter == " " else karakter
                    tabel_blok.append({
                        "Blok": f"B{i}",
                        "Karakter": nama,
                        "Nilai blok (m)": kode,
                        "Syarat": f"{kode} < {hasil['n']}"
                    })
                st.dataframe(tabel_blok, use_container_width=True, hide_index=True)
                st.latex(r"0 \leq m_i < n")

            with st.expander("Tahap 4 — Proses enkripsi setiap blok", expanded=True):
                st.markdown("Setiap blok dihitung menggunakan rumus RSA:")
                st.latex(r"C_i = m_i^e \bmod n")
                st.markdown(
                    f"Dengan e = **{hasil['e']}** dan n = **{hasil['n']}**. "
                    "Perhitungan perpangkatan modular dilakukan dengan "
                    "metode *square-and-multiply*."
                )
                tabel_enkripsi = []
                for i, (karakter, m, c) in enumerate(zip(
                    hasil["plaintext"], hasil["daftar_kode"], hasil["ciphertext"]
                ), start=1):
                    nama = "[SPASI]" if karakter == " " else karakter
                    tabel_enkripsi.append({
                        "Blok": f"B{i}",
                        "Karakter": nama,
                        "m": m,
                        "Substitusi": f"{m}^{hasil['e']} mod {hasil['n']}",
                        "Ciphertext (C)": c
                    })
                st.dataframe(tabel_enkripsi, use_container_width=True, hide_index=True)
                m0 = hasil["daftar_kode"][0]
                c0 = hasil["ciphertext"][0]
                st.markdown("**Contoh perhitungan blok pertama:**")
                st.code(
                    f"C₁ = m₁^e mod n\n"
                    f"C₁ = {m0}^{hasil['e']} mod {hasil['n']}\n"
                    f"C₁ = {c0}",
                    language=None
                )

            st.markdown("### Tahap 5 — Ciphertext akhir")
            label_kecil("Plaintext")
            st.code(hasil["plaintext"], language=None)
            label_kecil("Deretan kode ASCII")
            st.code(str(hasil["daftar_kode"]), language=None)
            label_kecil("Ciphertext")
            ciphertext_teks = ", ".join(str(angka) for angka in hasil["ciphertext"])
            st.code(ciphertext_teks, language=None)
            st.download_button(
                "Unduh ciphertext",
                data=ciphertext_teks,
                file_name="ciphertext_rsa.txt",
                mime="text/plain"
            )
    else:
        st.markdown(
            '<div class="kosong">Kunci dan ciphertext akan muncul di sini '
            'setelah kamu menekan tombol <b>Bangkitkan kunci dan '
            'enkripsi</b>.</div>',
            unsafe_allow_html=True
        )


# =====================================================
# 11. HALAMAN DEKRIPSI
# =====================================================

elif halaman == "Dekripsi":

    # Nilai default diisi dari proses enkripsi pada sesi yang sama.
    ciphertext_awal = st.session_state.get(
        "ciphertext_untuk_dekripsi", ""
    )
    d_awal = st.session_state.get("d_untuk_dekripsi", "")
    n_awal = st.session_state.get("n_untuk_dekripsi", "")

    # ---------- LANGKAH 1: CIPHERTEXT ----------
    with st.container(key="kotak_cipher"):
        kepala_langkah(
            1,
            "Masukkan ciphertext",
            "Tempel deretan angka hasil enkripsi, dipisahkan dengan koma."
        )

        ciphertext_input = st.text_area(
            "Ciphertext",
            value=ciphertext_awal,
            placeholder="Contoh: 1234, 5678, 9012",
            key="input_ciphertext",
            label_visibility="collapsed"
        )

    st.write("")

    # ---------- LANGKAH 2: KUNCI PRIVAT ----------
    with st.container(key="kotak_privat"):
        kepala_langkah(
            2,
            "Masukkan kunci privat",
            "Kunci privat terdiri dari d dan n. Keduanya harus berasal "
            "dari pasangan kunci yang sama dengan ciphertext."
        )

        kolom_d, kolom_n = st.columns(2)

        with kolom_d:
            d_input = st.text_input(
                "Kunci privat d",
                value=d_awal,
                placeholder="Masukkan nilai d",
                key="input_d"
            )

        with kolom_n:
            n_input = st.text_input(
                "Nilai n",
                value=n_awal,
                placeholder="Masukkan nilai n",
                key="input_n"
            )

        proses_dekripsi = st.button("Dekripsi pesan", type="primary")

    if proses_dekripsi:

        try:
            if not ciphertext_input.strip():
                raise ValueError("Ciphertext belum diisi.")

            if not d_input.strip() or not n_input.strip():
                raise ValueError("Kunci privat d dan nilai n harus diisi.")

            d = int(d_input)
            n = int(n_input)

            if d <= 0 or n <= 1:
                raise ValueError(
                    "Nilai d harus positif dan n harus lebih besar dari 1."
                )

            ciphertext = parse_ciphertext(ciphertext_input)

            if any(angka >= n for angka in ciphertext):
                raise ValueError(
                    "Setiap angka ciphertext harus lebih kecil dari n."
                )

            hasil_kode = dekripsi(ciphertext, (d, n))
            plaintext_hasil = kode_ke_teks(hasil_kode)

            st.session_state["hasil_dekripsi"] = {
                "ciphertext": ciphertext,
                "hasil_kode": hasil_kode,
                "plaintext": plaintext_hasil,
                "d": d,
                "n": n
            }

        except Exception as error:
            st.session_state.pop("hasil_dekripsi", None)
            st.error(f"Dekripsi gagal: {error}")

    st.write("")

    # ---------- HASIL ----------
    if "hasil_dekripsi" in st.session_state:

        hasil = st.session_state["hasil_dekripsi"]

        with st.container(key="kotak_hasil_dekripsi"):
            st.markdown(
                '<div class="langkah-judul">Hasil dekripsi</div>',
                unsafe_allow_html=True
            )

            # Tahap 1: tampilkan ciphertext dan kunci privat yang digunakan.
            with st.expander("Tahap 1 — Ciphertext dan kunci privat", expanded=True):
                st.markdown("Ciphertext merupakan angka hasil enkripsi yang akan dikembalikan ke kode karakter.")
                st.code(", ".join(str(x) for x in hasil["ciphertext"]), language=None)
                st.code(
                    f"Kunci privat: (d, n) = ({hasil['d']}, {hasil['n']})\n"
                    f"d = {hasil['d']}\n"
                    f"n = {hasil['n']}",
                    language=None
                )

            # Tahap 2: lakukan operasi RSA pada setiap elemen ciphertext.
            with st.expander("Tahap 2 — Proses dekripsi setiap blok", expanded=True):
                st.markdown("Setiap angka ciphertext dihitung menggunakan rumus:")
                st.latex(r"m_i = C_i^d \bmod n")
                st.markdown(
                    f"Dengan d = **{hasil['d']}** dan n = **{hasil['n']}**. "
                    "Hasil m adalah kode karakter sebelum dienkripsi."
                )

                tabel_dekripsi = []
                for i, (c, m) in enumerate(zip(hasil["ciphertext"], hasil["hasil_kode"]), start=1):
                    karakter = chr(m)
                    nama = "[SPASI]" if karakter == " " else karakter
                    tabel_dekripsi.append({
                        "Blok": f"B{i}",
                        "Ciphertext (C)": c,
                        "Substitusi rumus": f"{c}^{hasil['d']} mod {hasil['n']}",
                        "Kode hasil (m)": m,
                        "Karakter": nama
                    })
                st.dataframe(tabel_dekripsi, use_container_width=True, hide_index=True)

                st.markdown("**Contoh perhitungan blok pertama:**")
                c0 = hasil["ciphertext"][0]
                m0 = hasil["hasil_kode"][0]
                st.code(
                    f"m₁ = C₁^d mod n\n"
                    f"m₁ = {c0}^{hasil['d']} mod {hasil['n']}\n"
                    f"m₁ = {m0}",
                    language=None
                )

                with st.expander("Lihat cara kerja perpangkatan modular (square-and-multiply)"):
                    st.markdown(
                        "Komputer menghitung perpangkatan modular secara bertahap. "
                        "Pada setiap iterasi, bit terakhir eksponen diperiksa; "
                        "jika bit bernilai 1, hasil dikalikan dengan basis modulo n. "
                        "Basis kemudian dikuadratkan modulo n dan eksponen dibagi dua."
                    )
                    c_detail = hasil["ciphertext"][0]
                    eksponen = hasil["d"]
                    basis = c_detail % hasil["n"]
                    akumulator = 1
                    langkah = []
                    iterasi = 1
                    while eksponen > 0:
                        eksponen_sebelum = eksponen
                        bit = eksponen % 2
                        if bit == 1:
                            akumulator = (akumulator * basis) % hasil["n"]
                        hasil_kali = akumulator
                        basis_baru = (basis * basis) % hasil["n"]
                        langkah.append({
                            "Iterasi": iterasi,
                            "Eksponen saat diperiksa": eksponen_sebelum,
                            "Bit terakhir": bit,
                            "Akumulator setelah proses": hasil_kali,
                            "Basis setelah dikuadratkan": basis_baru
                        })
                        basis = basis_baru
                        eksponen //= 2
                        iterasi += 1
                    st.dataframe(langkah, use_container_width=True, hide_index=True)
                    st.caption(
                        f"Nilai akhir akumulator = {m0}, sama dengan kode hasil dekripsi blok pertama."
                    )

            # Tahap 3: kode angka dikonversi kembali menjadi karakter.
            with st.expander("Tahap 3 — Mengubah kode ASCII kembali menjadi teks", expanded=True):
                st.markdown(
                    "Setelah dekripsi, setiap nilai m diubah kembali menjadi karakter "
                    "menggunakan fungsi `chr()`."
                )
                tabel_konversi = []
                for i, (m, karakter) in enumerate(zip(hasil["hasil_kode"], hasil["plaintext"]), start=1):
                    nama = "[SPASI]" if karakter == " " else karakter
                    tabel_konversi.append({
                        "Blok": f"B{i}",
                        "Kode ASCII (m)": m,
                        "Konversi": f"chr({m})",
                        "Karakter": nama
                    })
                st.dataframe(tabel_konversi, use_container_width=True, hide_index=True)
                st.code("[" + ", ".join(map(str, hasil["hasil_kode"])) + "]", language=None)

            # Tahap 4: tampilkan plaintext akhir.
            st.markdown("### Tahap 4 — Plaintext hasil dekripsi")
            st.markdown(
                f'<div class="hasil-teks">'
                f'{html.escape(hasil["plaintext"])}</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<div class="kosong">Pesan asli akan muncul di sini setelah '
            'kamu menekan tombol <b>Dekripsi pesan</b>.</div>',
            unsafe_allow_html=True
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.markdown(
    '<div class="footer-kecil">Aplikasi pembelajaran RSA, '
    'dibuat dengan Python dan Streamlit.</div>',
    unsafe_allow_html=True
)


# In[1]:


import os
print(os.getcwd())


# In[15]:


import os
print(os.listdir())

