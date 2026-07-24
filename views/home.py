import streamlit as st

from utils.database import (
    get_total_data,
    is_database_empty
)


# ==========================================================
# HOME
# ==========================================================

def show_home():

    # ======================================================
    # HEADER
    # ======================================================

    st.title("🍽️ Buffet The Padang Pasir")

    st.caption(
        "Aplikasi Analisis Pola Transaksi Shopee Food Menggunakan Metode K-Means Clustering"
    )

    st.divider()

    # ======================================================
    # METRIC
    # ======================================================

    total_data = get_total_data()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 Total Data",
            value=total_data
        )

    with col2:
        st.metric(
            label="📊 Jumlah Cluster",
            value="2"
        )

    with col3:
        st.metric(
            label="🧠 Metode",
            value="K-Means"
        )

    with col4:
        st.metric(
            label="⚙️ Normalisasi",
            value="Min-Max"
        )

    st.divider()

    # ======================================================
    # INFORMASI PENELITIAN
    # ======================================================

    st.subheader("📖 Tentang Penelitian")

    st.info(
        """
Sistem ini dirancang untuk membantu Buffet The Padang Pasir dalam
menganalisis pola transaksi pemesanan melalui Shopee Food menggunakan
metode K-Means Clustering.

Hasil analisis digunakan untuk mengelompokkan produk berdasarkan
karakteristik transaksi sehingga dapat membantu pemilik usaha dalam
menentukan prioritas pelayanan, pengelolaan stok bahan baku, serta
mendukung pengambilan keputusan operasional.
"""
    )

    st.divider()

    # ======================================================
    # STATUS DATASET
    # ======================================================

    st.subheader("📂 Status Dataset")

    if is_database_empty():

        st.warning(
            "Belum ada dataset yang tersimpan.\n\nSilakan upload dataset pada menu **Kelola Data**."
        )

    else:

        st.success(
            f"Sebanyak **{total_data}** data transaksi Shopee Food telah tersedia dan siap untuk dianalisis."
        )

    st.divider()

    # ======================================================
    # PETUNJUK
    # ======================================================

    st.subheader("🚀 Alur Penggunaan")

    st.markdown("""
1. Tambahkan atau upload data transaksi Shopee Food pada menu **Kelola Data**.
2. Jalankan proses **Preprocessing** untuk menyiapkan data.
3. Lakukan proses **K-Means Clustering** untuk mengelompokkan produk.
4. Lihat hasil analisis, karakteristik, dan rekomendasi setiap cluster.
5. Unduh hasil analisis apabila diperlukan.
""")
