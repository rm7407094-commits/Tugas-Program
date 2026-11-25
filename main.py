
import streamlit as st
import numpy as np
from PIL import Image

# =========================
# KONFIGURASI APLIKASI
# =========================

st.set_page_config(
    page_title="AI Skin Analyzer",
    page_icon="🔬",
    layout="wide"
)

# =========================
# JUDUL APLIKASI
# =========================

st.title("🔬 AI SKIN ANALYZER")
st.subheader("Analisis Citra Kulit Berbasis Computer Vision")

st.write(
    "Aplikasi pembelajaran untuk menganalisis "
    "karakteristik warna kemerahan pada gambar."
)

st.info(
    "Aplikasi ini bukan alat diagnosis medis dan "
    "tidak dapat memastikan jerawat atau penyakit kulit."
)

# =========================
# FUNGSI ANALISIS GAMBAR
# =========================

def analisis_kulit(image):

    # Ubah gambar menjadi RGB
    img = image.convert("RGB")

    # Ubah gambar menjadi array
    data = np.array(img).astype(np.int16)

    # Pisahkan warna RGB
    red = data[:, :, 0]
    green = data[:, :, 1]
    blue = data[:, :, 2]

    # Deteksi piksel dengan karakteristik kemerahan
    mask = (
        (red > 100) &
        (red > green * 1.20) &
        (red > blue * 1.15)
    )

    # Hitung persentase piksel kemerahan
    total_pixel = mask.size
    red_pixel = np.sum(mask)

    persentase = (red_pixel / total_pixel) * 100

    # Buat gambar hasil visualisasi
    hasil = data.copy()

    # Tandai area terpilih dengan warna biru
    hasil[mask] = (
        hasil[mask] * 0.5 +
        np.array([0, 100, 255]) * 0.5
    ).astype(np.uint8)

    hasil_image = Image.fromarray(hasil.astype(np.uint8))

    return persentase, hasil_image


# =========================
# UPLOAD GAMBAR
# =========================

st.header("📷 Upload Foto Wajah")

uploaded_file = st.file_uploader(
    "Pilih foto dari komputer",
    type=["jpg", "jpeg", "png"]
)

# =========================
# PROSES ANALISIS
# =========================

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    # Batasi ukuran gambar
    image.thumbnail((1000, 1000))

    st.success("Foto berhasil diunggah!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Foto Asli")
        st.image(image, use_container_width=True)

    # Tombol analisis
    if st.button("🔍 ANALISIS GAMBAR", use_container_width=True):

        persentase, hasil = analisis_kulit(image)

        st.header("📊 HASIL ANALISIS")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Hasil Visualisasi")
            st.image(hasil, use_container_width=True)

        with col2:
            st.metric(
                "Persentase Piksel Kemerahan",
                f"{persentase:.2f}%"
            )

            st.write(
                "Nilai ini menunjukkan proporsi piksel "
                "yang memenuhi aturan warna kemerahan, "
                "bukan persentase jerawat."
            )

        st.info(
            "Penandaan warna dapat dipengaruhi pencahayaan, "
            "kamera, warna kulit, dan kualitas gambar."
        )

else:
    st.warning("Silakan unggah foto terlebih dahulu.")

# =========================
# INFORMASI APLIKASI
# =========================

st.divider()

st.caption(
    "AI Skin Analyzer | Proyek Akhir Pemrograman Visual II"
)

st.caption(
    "Hasil hanya untuk demonstrasi computer vision, "
    "bukan diagnosis atau rekomendasi pengobatan."
)
