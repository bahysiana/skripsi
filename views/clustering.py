import streamlit as st
import pandas as pd
import plotly.express as px

from utils.clustering import (
    perform_clustering,
    cluster_summary,
    cluster_profile,
    identify_high_service_cluster,
    cluster_name
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
    # IDENTIFIKASI CLUSTER
    # ======================================================

    high_service_cluster = identify_high_service_cluster(
        profile_df
    )

    low_service_cluster = (
        1 if high_service_cluster == 0 else 0
    )

    summary = cluster_summary(result_df)

    total_produk = len(result_df)

    cluster_tinggi = int(

        summary.loc[
            summary["Cluster"] == high_service_cluster,
            "Jumlah"
        ].values[0]

    )

    cluster_rendah = int(

        summary.loc[
            summary["Cluster"] == low_service_cluster,
            "Jumlah"
        ].values[0]

    )

    persen_tinggi = float(

        summary.loc[
            summary["Cluster"] == high_service_cluster,
            "Persentase"
        ].values[0]

    )

    persen_rendah = float(

        summary.loc[
            summary["Cluster"] == low_service_cluster,
            "Persentase"
        ].values[0]

    )

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

    # ======================================================
    # VISUALISASI DISTRIBUSI CLUSTER
    # ======================================================

    st.subheader("📈 Visualisasi Distribusi Cluster")

    chart_df = summary.copy()

    chart_df["Nama Cluster"] = chart_df["Cluster"].apply(
        lambda x: cluster_name(
            x,
            high_service_cluster
        )
    )

    fig = px.bar(
        chart_df,
        x="Nama Cluster",
        y="Jumlah",
        color="Nama Cluster",
        text="Jumlah",
        title="Distribusi Produk pada Setiap Cluster"
    )

    fig.update_layout(
        xaxis_title="Cluster",
        yaxis_title="Jumlah Produk",
        showlegend=False
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # NILAI CENTROID
    # ======================================================

    st.subheader("🎯 Nilai Centroid")

    centroid_display = centroid_df.copy()

    centroid_display.insert(
        0,
        "Nama Cluster",
        [
            cluster_name(
                cluster,
                high_service_cluster
            )
            for cluster in centroid_display.index
        ]
    )

    st.dataframe(
        centroid_display,
        hide_index=True,
        use_container_width=True
    )

    st.info(
        """
Centroid merupakan titik pusat dari masing-masing cluster.
Nilai centroid menunjukkan karakteristik rata-rata setiap
variabel pada kelompok produk tersebut setelah proses
normalisasi Min-Max.
        """
    )

    st.divider()

    # ======================================================
    # PROFIL CLUSTER
    # ======================================================

    st.subheader("📊 Profil Cluster")

    profile_display = profile_df.copy()

    profile_display.insert(
        0,
        "Nama Cluster",
        [
            cluster_name(
                cluster,
                high_service_cluster
            )
            for cluster in profile_display.index
        ]
    )

    st.dataframe(
        profile_display,
        use_container_width=True
    )

    st.info(
        """
Profil cluster menunjukkan nilai rata-rata setiap variabel
penelitian pada masing-masing kelompok produk. Nilai yang
lebih tinggi menunjukkan karakteristik yang lebih dominan
dibandingkan cluster lainnya.
        """
    )

    st.divider()

    # ======================================================
    # INTERPRETASI CLUSTER
    # ======================================================

    st.subheader("📋 Interpretasi Hasil Clustering")

    profile_display = profile_df.copy()

    for cluster in profile_display.index:

        nama_cluster = cluster_name(
            cluster,
            high_service_cluster
        )

        data = profile_display.loc[cluster]

        with st.expander(f"📌 {nama_cluster}", expanded=True):

            st.markdown(f"""
**Karakteristik Cluster:**

- Rata-rata Jumlah Item Produk : **{data['Jumlah_Item_Produk']:.4f}**
- Rata-rata Frekuensi Produk : **{data['Frekuensi_Produk']:.4f}**
- Rata-rata Total Pendapatan : **{data['Total_Pendapatan']:.4f}**
- Rata-rata Waktu Persiapan Diberikan : **{data['Rata2_Waktu_Persiapan_Diberikan']:.4f}**
- Rata-rata Waktu Persiapan Digunakan : **{data['Rata2_Waktu_Persiapan_Digunakan']:.4f}**
            """)

            if cluster == high_service_cluster:

                st.success("""
Produk pada cluster ini memiliki karakteristik dengan tingkat aktivitas yang lebih tinggi dibandingkan cluster lainnya. Produk-produk tersebut cenderung lebih sering dipesan, menghasilkan pendapatan yang lebih besar, serta memerlukan perhatian lebih dalam proses pelayanan sehingga dapat dijadikan sebagai produk prioritas.
                """)

            else:

                st.info("""
Produk pada cluster ini memiliki karakteristik dengan tingkat aktivitas yang relatif lebih rendah. Produk-produk tersebut masih memberikan kontribusi terhadap penjualan, namun kebutuhan pelayanan dan intensitas pemesanannya tidak setinggi cluster prioritas.
                """)

    st.divider()

    # ======================================================
    # REKOMENDASI
    # ======================================================

    st.subheader("💡 Rekomendasi")

    st.markdown("""
Berdasarkan hasil pengelompokan menggunakan metode **K-Means Clustering**, diperoleh dua kelompok produk dengan karakteristik yang berbeda. Hasil tersebut dapat dimanfaatkan sebagai dasar pengambilan keputusan operasional pada Buffet The Padang Pasir.

### Rekomendasi untuk Cluster Beban Pelayanan Tinggi
- Menjaga ketersediaan stok bahan baku.
- Memastikan proses persiapan produk lebih optimal.
- Menjadikan produk sebagai prioritas pelayanan ketika pesanan meningkat.
- Melakukan evaluasi kapasitas produksi agar waktu pelayanan tetap terjaga.

### Rekomendasi untuk Cluster Beban Pelayanan Rendah
- Melakukan promosi terhadap produk yang masih jarang dipesan.
- Menawarkan paket atau bundling dengan produk prioritas.
- Mengevaluasi strategi pemasaran agar penjualan produk meningkat.
- Memantau perkembangan penjualan secara berkala.

Dengan adanya pengelompokan ini, pemilik usaha dapat lebih mudah menentukan prioritas pelayanan, pengelolaan stok, serta strategi penjualan berdasarkan karakteristik masing-masing kelompok produk.
    """)

    st.success(
        "Interpretasi dan rekomendasi berhasil dibuat berdasarkan hasil clustering."
    )

    st.divider()

    # ======================================================
    # HASIL AKHIR CLUSTERING
    # ======================================================

    st.subheader("📦 Hasil Akhir Clustering Produk")

    final_df = product_dataset.copy()

    final_df["Cluster"] = result_df["Cluster"].values

    final_df["Hasil Cluster"] = final_df["Cluster"].apply(
        lambda x: cluster_name(
            x,
            high_service_cluster
        )
    )

    final_df = final_df[
        [
            "Produk",
            "Jumlah_Item_Produk",
            "Frekuensi_Produk",
            "Total_Pendapatan",
            "Rata2_Waktu_Persiapan_Diberikan",
            "Rata2_Waktu_Persiapan_Digunakan",
            "Hasil Cluster"
        ]
    ]

    final_df = final_df.rename(
        columns={
            "Produk": "Produk",
            "Jumlah_Item_Produk": "Jumlah Item Produk",
            "Frekuensi_Produk": "Frekuensi Produk",
            "Total_Pendapatan": "Total Pendapatan",
            "Rata2_Waktu_Persiapan_Diberikan":
                "Rata-rata Waktu Persiapan Diberikan",
            "Rata2_Waktu_Persiapan_Digunakan":
                "Rata-rata Waktu Persiapan Digunakan"
        }
    )

    st.dataframe(
        final_df,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # KESIMPULAN
    # ======================================================

    st.subheader("✅ Kesimpulan")

    st.markdown(f"""
Proses analisis menggunakan metode **K-Means Clustering**
berhasil mengelompokkan **{total_produk} produk** ke dalam
**2 cluster**, yaitu:

- **Pola Transaksi dengan Beban Pelayanan Tinggi**
- **Pola Transaksi dengan Beban Pelayanan Rendah**

Hasil pengelompokan ini dapat dimanfaatkan sebagai dasar
pengambilan keputusan dalam menentukan prioritas pelayanan,
pengelolaan stok bahan baku, serta penyusunan strategi
penjualan pada Buffet The Padang Pasir.
    """)

    st.success(
        "Proses analisis K-Means Clustering selesai dilakukan."
    )
