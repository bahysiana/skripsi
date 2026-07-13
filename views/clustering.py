import streamlit as st
import pandas as pd
import plotly.express as px

from utils.clustering import (
    perform_clustering,
    cluster_summary,
    cluster_profile
)


# ==========================================================
# HALAMAN CLUSTERING
# ==========================================================

def show_clustering():

    # ======================================================
    # HEADER
    # ======================================================

    st.title("📊 Hasil Clustering")

    st.caption(
        """
Analisis pola transaksi Shopee Food menggunakan
metode K-Means Clustering.
        """
    )

    st.divider()

    # ======================================================
    # CEK PREPROCESSING
    # ======================================================

    if "normalized_df" not in st.session_state:

        st.warning(
            """
Silakan lakukan **Preprocessing**
terlebih dahulu sebelum menjalankan
proses clustering.
            """
        )

        return

    normalized_df = st.session_state["normalized_df"]

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        """
Klik tombol **Jalankan Clustering**
untuk melakukan proses pengelompokan
data transaksi menggunakan metode
K-Means Clustering.
        """
    )

    # ======================================================
    # BUTTON
    # ======================================================

    col_btn, col_info = st.columns([1, 5])

    with col_btn:

        mulai = st.button(

            "🚀 Jalankan",

            type="primary",

            use_container_width=True

        )

    with col_info:

        st.empty()

    if not mulai:

        return

    # ======================================================
    # PROSES CLUSTERING
    # ======================================================

    with st.spinner("Sedang melakukan proses clustering..."):

        result_df, centroid_df = perform_clustering(

            normalized_df,

            n_clusters=2

        )

    st.success(
        "Proses clustering berhasil dilakukan."
    )

    # ======================================================
    # SESSION
    # ======================================================

    st.session_state["cluster_df"] = result_df

    st.session_state["centroid_df"] = centroid_df

    # ======================================================
    # RINGKASAN
    # ======================================================

    summary = cluster_summary(result_df)

    total_data = len(result_df)

    tinggi = int(summary.iloc[0]["Jumlah"])

    normal = int(summary.iloc[1]["Jumlah"])

    tinggi_pct = float(summary.iloc[0]["Persentase"])

    normal_pct = float(summary.iloc[1]["Persentase"])

    st.divider()

    # ======================================================
    # KPI
    # ======================================================

    st.subheader("📌 Ringkasan Hasil Clustering")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(

            "📦 Total Transaksi",

            total_data

        )

    with k2:

        st.metric(

            "🟧 Prioritas Tinggi",

            tinggi,

            f"{tinggi_pct:.2f}%"

        )

    with k3:

        st.metric(

            "🟩 Prioritas Normal",

            normal,

            f"{normal_pct:.2f}%"

        )

    with k4:

        st.metric(

            "🧠 Jumlah Cluster",

            "2"

        )

    st.divider()

    # ======================================================
    # RINGKASAN ANALISIS
    # ======================================================

    st.subheader("📖 Ringkasan Analisis")

    st.markdown(
        f"""
Berdasarkan proses **K-Means Clustering** terhadap
**{total_data} transaksi**, diperoleh:

- **{tinggi} transaksi ({tinggi_pct:.2f}%)**
  termasuk kelompok **Transaksi Prioritas Tinggi**.

- **{normal} transaksi ({normal_pct:.2f}%)**
  termasuk kelompok **Transaksi Prioritas Normal**.

Pengelompokan ini memberikan gambaran pola transaksi
yang dapat digunakan sebagai dasar dalam mendukung
pengambilan keputusan operasional pada Buffet The Padang Pasir.
        """
    )

    st.divider()
        # ======================================================
    # VISUALISASI HASIL CLUSTERING
    # ======================================================

    st.subheader("📈 Visualisasi Hasil Clustering")

    col_chart, col_table = st.columns([2, 1])

    # ======================================================
    # GRAFIK DISTRIBUSI
    # ======================================================

    with col_chart:

        chart_df = pd.DataFrame({

            "Kategori": [

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah": [

                tinggi,

                normal

            ]

        })

        fig = px.bar(

            chart_df,

            x="Kategori",

            y="Jumlah",

            text="Jumlah",

            color="Kategori",

            color_discrete_map={

                "Prioritas Tinggi": "#F57C00",

                "Prioritas Normal": "#34A853"

            }

        )

        fig.update_layout(

            height=430,

            showlegend=False,

            plot_bgcolor="white",

            paper_bgcolor="white",

            margin=dict(

                l=20,

                r=20,

                t=20,

                b=20

            )

        )

        fig.update_traces(

            textposition="outside"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ======================================================
    # RINGKASAN
    # ======================================================

    with col_table:

        st.subheader("📋 Ringkasan")

        ringkasan_df = pd.DataFrame({

            "Kategori": [

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah": [

                tinggi,

                normal

            ],

            "Persentase": [

                f"{tinggi_pct:.2f}%",

                f"{normal_pct:.2f}%"

            ]

        })

        st.dataframe(

            ringkasan_df,

            hide_index=True,

            use_container_width=True

        )

        st.markdown("### ℹ️ Informasi")

        st.info(

            """
Grafik menunjukkan jumlah transaksi
pada masing-masing cluster hasil
K-Means Clustering.

Semakin tinggi batang grafik,
semakin banyak transaksi
yang termasuk dalam cluster tersebut.
            """

        )

    st.divider()

    # ======================================================
    # DETAIL NILAI CENTROID
    # ======================================================

    st.subheader("📐 Detail Nilai Centroid")

    with st.expander("Lihat Nilai Centroid"):

        st.markdown(
            """
Centroid merupakan titik pusat dari setiap cluster
yang dihasilkan oleh algoritma K-Means.

Nilai centroid digunakan sebagai acuan
dalam menentukan karakteristik masing-masing cluster.
            """
        )

        st.dataframe(

            centroid_df.round(4),

            hide_index=True,

            use_container_width=True

        )

    st.divider()

    # ======================================================
    # INTERPRETASI
    # ======================================================

    st.subheader("🎯 Interpretasi Hasil Clustering")

    left, right = st.columns(2)
