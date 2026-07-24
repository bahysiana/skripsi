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
Analisis pola transaksi Shopee Food
menggunakan metode K-Means Clustering
berdasarkan data produk hasil preprocessing.
        """
    )

    st.divider()

    # ======================================================
    # CEK PREPROCESSING
    # ======================================================

    if (
        "normalized_df" not in st.session_state
        or
        "product_dataset" not in st.session_state
    ):

        st.warning(
            """
Silakan lakukan proses **Preprocessing**
terlebih dahulu sebelum menjalankan
proses K-Means Clustering.
            """
        )

        return

    normalized_df = st.session_state["normalized_df"]

    product_dataset = st.session_state["product_dataset"]

    # ======================================================
    # SESSION STATE
    # ======================================================

    if "cluster_df" not in st.session_state:

        st.session_state["cluster_df"] = None

    if "centroid_df" not in st.session_state:

        st.session_state["centroid_df"] = None

    if "profile_df" not in st.session_state:

        st.session_state["profile_df"] = None

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        """
Proses clustering dilakukan menggunakan
algoritma K-Means dengan jumlah cluster (K=2).

Objek yang dikelompokkan adalah produk,
berdasarkan lima variabel penelitian yang
telah melalui proses Min-Max Normalization.
        """
    )

    st.divider()

    # ======================================================
    # DATA SIAP DIKLASTER
    # ======================================================

    st.subheader("📦 Data Siap Clustering")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Jumlah Produk",
            len(product_dataset)
        )

    with col2:

        st.metric(
            "Jumlah Variabel",
            len(normalized_df.columns)
        )

    st.dataframe(
        product_dataset,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # BUTTON
    # ======================================================

    col_btn, col_info = st.columns([1,4])

    with col_btn:

        mulai = st.button(
            "🚀 Jalankan Clustering",
            type="primary",
            use_container_width=True
        )

    with col_info:

        st.empty()

    if not mulai and st.session_state["cluster_df"] is None:

        return

    # ======================================================
    # PROSES CLUSTERING
    # ======================================================

    if mulai:

        with st.spinner(
            "Sedang melakukan proses K-Means Clustering..."
        ):

            result_df, centroid_df = perform_clustering(
                normalized_df,
                n_clusters=2
            )

            profile_df = cluster_profile(result_df)

        st.session_state["cluster_df"] = result_df
        st.session_state["centroid_df"] = centroid_df
        st.session_state["profile_df"] = profile_df

        st.success(
            "Proses clustering berhasil dilakukan."
        )

    # ======================================================
    # CEK HASIL CLUSTERING
    # ======================================================

    if st.session_state["cluster_df"] is None:

        return

    result_df = st.session_state["cluster_df"]

    centroid_df = st.session_state["centroid_df"]

    profile_df = st.session_state["profile_df"]

    # ======================================================
    # RINGKASAN CLUSTER
    # ======================================================

    summary = cluster_summary(result_df)

    total_produk = len(result_df)

    cluster_tinggi = int(summary.iloc[0]["Jumlah"])

    cluster_rendah = int(summary.iloc[1]["Jumlah"])

    persen_tinggi = float(summary.iloc[0]["Persentase"])

    persen_rendah = float(summary.iloc[1]["Persentase"])

    st.divider()

    # ======================================================
    # KPI
    # ======================================================

    st.subheader("📌 Ringkasan Hasil Clustering")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "📦 Total Produk",
            total_produk
        )

    with k2:

        st.metric(
            "🟧 Beban Pelayanan Tinggi",
            cluster_tinggi,
            f"{persen_tinggi:.2f}%"
        )

    with k3:

        st.metric(
            "🟩 Beban Pelayanan Rendah",
            cluster_rendah,
            f"{persen_rendah:.2f}%"
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
Berdasarkan proses **K-Means Clustering**
terhadap **{total_produk} produk**,
diperoleh hasil pengelompokan sebagai berikut.

- **{cluster_tinggi} produk ({persen_tinggi:.2f}%)**
  termasuk ke dalam kelompok
  **Pola Transaksi dengan Beban Pelayanan Tinggi**.

- **{cluster_rendah} produk ({persen_rendah:.2f}%)**
  termasuk ke dalam kelompok
  **Pola Transaksi dengan Beban Pelayanan Rendah**.

Pengelompokan ini memberikan gambaran
mengenai karakteristik setiap produk
berdasarkan jumlah item yang terjual,
frekuensi pembelian,
total pendapatan,
serta rata-rata waktu persiapan,
sehingga dapat digunakan sebagai dasar
dalam mendukung pengambilan keputusan
operasional pada Buffet The Padang Pasir.
        """
    )

    st.divider()

