import streamlit as st

from utils.database import (
    get_total_data,
    is_database_empty
)

from utils.components import (
    hero_card,
    metric_card,
    section_title,
    info_card,
    empty_card
)


# ==========================================================
# HOME
# ==========================================================

def show_home():

    # ======================================================
    # HERO
    # ======================================================

    hero_card(

        "🍽 Buffet The Padang Pasir",

        """
Aplikasi Analisis Pola Transaksi Shopee Food
Menggunakan Metode K-Means Clustering
Berdasarkan Data Pemesanan
Pada Toko Buffet The Padang Pasir.
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
    
