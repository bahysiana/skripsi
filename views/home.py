import streamlit as st

from utils.database import get_total_data

from utils.components import (
    hero_card,
    metric_card,
    section_title,
    info_card
)


# ==========================================================
# HOME
# ==========================================================

def show_home():

    # ======================================================
    # HERO
    # ======================================================

    hero_card(

        "Buffet The Padang Pasir",

        """
Aplikasi Analisis Pola Transaksi Shopee Food
Menggunakan Metode K-Means Clustering
berdasarkan Data Pemesanan pada
Toko Buffet The Padang Pasir.
        """

    )

    # ======================================================
    # TOTAL DATA
    # ======================================================

    total_data = get_total_data()

    # ======================================================
    # METRIC
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        metric_card(

            "Total Data",

            total_data,

            "📦"

        )

    with col2:

        metric_card(

            "Jumlah Cluster",

            "2",

            "📊"

        )

    with col3:

        metric_card(

            "Metode",

            "K-Means",

            "🧠"

        )

    with col4:

        metric_card(

            "Normalisasi",

            "Min-Max",

            "⚙️"

        )

    st.divider()

    # ======================================================
    # RINGKASAN
    # ======================================================

    section_title(

        "📋 Ringkasan Penelitian"

    )

    info_card(

        "Deskripsi",

        """
Penelitian ini bertujuan untuk menganalisis pola transaksi Shopee Food
pada Toko Buffet The Padang Pasir menggunakan metode
K-Means Clustering.

Hasil pengelompokan digunakan untuk mengetahui karakteristik
transaksi berdasarkan beban pelayanan sehingga dapat membantu
pemilik toko dalam menentukan prioritas pelayanan.
        """

    )

    st.divider()

    # ======================================================
    # INFORMASI
    # ======================================================

    section_title(

        "ℹ️ Informasi Sistem"

    )

    info_card(

        "Teknologi",

        """
• Python

• Streamlit

• Scikit-Learn

• SQLite

• Plotly

• Metode K-Means Clustering

• Min-Max Normalization
        """

    )
