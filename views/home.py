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
Penelitian ini bertujuan untuk menganalisis pola transaksi pelanggan
Shopee Food pada Toko Buffet The Padang Pasir menggunakan algoritma
K-Means Clustering.

Hasil clustering diharapkan mampu membantu pemilik toko
dalam memahami karakteristik transaksi pelanggan sehingga
dapat dijadikan dasar dalam pengambilan keputusan bisnis.
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
            f"Dataset tersedia sebanyak **{total_data}** data transaksi."
        )

    st.divider()

    # ======================================================
    # PETUNJUK
    # ======================================================

    st.subheader("🚀 Alur Penggunaan")

    st.markdown("""
1. Upload dataset pada menu **Kelola Data**.
2. Lakukan **Preprocessing** (Cleaning, Feature Engineering, Min-Max).
3. Jalankan proses **K-Means Clustering**.
4. Lihat hasil analisis dan interpretasi cluster.
5. Download hasil penelitian.
""")
